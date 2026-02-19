# Imports of the required python modules and libraries
######################################################
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.utils.timezone import now
from django.apps import apps
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from .middleware import get_current_user, get_current_request

# Models to exclude from activity logging (e.g., internal Django models with non-integer PKs)
EXCLUDED_MODELS = [
    'django.contrib.sessions.models.Session',
]

def get_model_path(sender):
    """Get full model path for comparison."""
    return f"{sender.__module__}.{sender.__name__}"

def get_client_ip(request):
    """Extract client IP address from request."""
    if not request:
        return None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    """Log user login actions."""
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    UserActivityLog.objects.create(
        user=user,
        action="LOGIN",
        model_name="auth",
        object_id=None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        timestamp=now(),
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    """Log user logout actions."""
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    UserActivityLog.objects.create(
        user=user,
        action="LOGOUT",
        model_name="auth",
        object_id=None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        timestamp=now(),
    )

@receiver(pre_save)
def capture_original_state(sender, instance, **kwargs):
    """Capture state before save to calculate diffs."""
    # Skip log model itself
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    if sender == UserActivityLog:
        return

    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._original_state = {}
            for field in instance._meta.fields:
                try:
                    val = getattr(old_instance, field.name)
                    # Store simple types, skip binary or large text if needed
                    instance._original_state[field.name] = val
                except Exception:
                    pass
                    
            # Check for soft delete restoration or deletion
            instance._was_not_deleted = (getattr(old_instance, 'deleted_at', None) is None)
        except sender.DoesNotExist:
            pass

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    """Log create and update actions for all models."""
    # Prevent infinite recursion by skipping the log model itself
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    if sender == UserActivityLog:
        return
    
    # Skip excluded models (like Session)
    if get_model_path(sender) in EXCLUDED_MODELS:
        return

    # Skip if instance explicitly requests no logging
    if getattr(instance, 'skip_signal_logging', False):
        return

    # Get the current user from thread locals
    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    update_fields = kwargs.get('update_fields')
    
    # Ignore implicit updates to last_login (handled by user_logged_in signal)
    if update_fields and 'last_login' in update_fields and len(update_fields) == 1:
        return

    # Ignore Profile preference updates alone (often automated)
    if instance._meta.app_label == 'microsys' and instance._meta.object_name == 'Profile':
        if update_fields and 'preferences' in update_fields and len(update_fields) == 1:
            return

    action = "CREATE" if created else "UPDATE"
    details = {}
    
    # Check for soft delete transition
    if not created and getattr(instance, '_was_not_deleted', False) and getattr(instance, 'deleted_at', None):
        action = "DELETE"
    
    # Compare with original state for updates
    if not created and action == "UPDATE" and hasattr(instance, '_original_state'):
        original = instance._original_state
        for field in instance._meta.fields:
            field_name = field.name
            
            # Skip irrelevant fields
            if field_name in ['last_login', 'date_joined', 'updated_at', 'modified_at']:
                continue
                
            try:
                new_val = getattr(instance, field_name)
                old_val = original.get(field_name)
                
                # Handle Password and Backup Codes
                if field_name == 'password' or field_name == 'backup_codes':
                    if new_val != old_val:
                         details[field_name] = {'old': '********', 'new': '********'}
                    continue

                if new_val != old_val:
                    # Format values for display
                    if hasattr(new_val, '__str__'): new_val = str(new_val)
                    if hasattr(old_val, '__str__'): old_val = str(old_val)
                    
                    details[field_name] = {'old': old_val, 'new': new_val}
            except Exception:
                pass

    # Normalize Model and Object ID for User/Profile unification
    is_user_entry = False
    target_user_id = None
    
    # Use proper class checks instead of string matching
    User = get_user_model()
    Profile = apps.get_model('microsys', 'Profile')
    
    if isinstance(instance, User):
        is_user_entry = True
        target_user_id = instance.pk
        model_name = "User Profile" # Logical name for both User and Profile
        obj_id = int(instance.pk)
    elif isinstance(instance, Profile):
        is_user_entry = True
        target_user_id = instance.user_id
        model_name = "User Profile"
        obj_id = int(instance.user_id) # Log against the User ID for unification
    else:
        model_name = instance._meta.verbose_name
        try:
            obj_id = int(instance.pk) if instance.pk is not None else None
        except (ValueError, TypeError):
            obj_id = None

    # Capture initial state for creations (User/Profile)
    if is_user_entry and created:
        for field in instance._meta.fields:
            if field.name in ['password', 'last_login', 'date_joined', 'updated_at', 'modified_at', 'deleted_at', 'preferences']:
                continue
            val = getattr(instance, field.name)
            if val is not None and val != '':
                details[field.name] = {'old': None, 'new': str(val)}

    # Aggressive Grouping: Look for log in the SAME SECOND
    if is_user_entry:
        # Search for a log created by the same actor for the same target in the last 1 second
        recent_log = UserActivityLog.objects.filter(
            user=user,
            model_name="User Profile",
            object_id=obj_id,
            timestamp__gte=now().replace(microsecond=0) # Round to the current second
        ).order_by('-timestamp').first()
        
        if recent_log:
            # Merge details
            if details:
                if not recent_log.details:
                    recent_log.details = {}
                recent_log.details.update(details)
                
                # If current action is CREATE, promote the log to CREATE
                if action == "CREATE":
                    recent_log.action = "CREATE"
                
                recent_log.save()
            return # Skip creating new log entry

    # Use string representation of the object for 'number' or reference
    try:
        obj_str = str(instance)
    except TypeError:
        # Fallback if __str__ returns non-string (e.g. int)
        obj_str = str(instance.pk)

    request = get_current_request()
    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "") if request else ""

    # Determine target scope
    scope = getattr(instance, 'scope', None)
    if not scope and is_user_entry:
        # For User/Profile, if not directly on instance, check profile
        if isinstance(instance, User) and hasattr(instance, 'profile'):
            scope = instance.profile.scope
        elif isinstance(instance, Profile):
            scope = instance.scope # From Profile model directly

    UserActivityLog.safe_log(
        user=user,
        action=action,
        model_name=model_name,
        object_id=obj_id,
        number=obj_str[:50] if obj_str else None,
        details=details,
        ip_address=ip,
        user_agent=user_agent,
        scope=scope,
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    """Log delete actions for all models."""
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    if sender == UserActivityLog:
        return
    
    # Skip excluded models (like Session)
    if get_model_path(sender) in EXCLUDED_MODELS:
        return

    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    action = "DELETE"
    # Normalize Model and Object ID for User/Profile unification
    is_user_entry = False
    User = get_user_model()
    Profile = apps.get_model('microsys', 'Profile')
    
    if isinstance(instance, User):
        is_user_entry = True
        model_name = "User Profile"
        obj_id = int(instance.pk)
    elif isinstance(instance, Profile):
        is_user_entry = True
        model_name = "User Profile"
        obj_id = int(instance.user_id) # Profile's User ID
    else:
        model_name = instance._meta.verbose_name
        try:
            obj_id = int(instance.pk) if instance.pk is not None else None
        except (ValueError, TypeError):
            obj_id = None

    # Aggressive Grouping for Delete as well
    if is_user_entry:
        recent_log = UserActivityLog.objects.filter(
            user=user,
            model_name="User Profile",
            action="DELETE",
            object_id=obj_id,
            timestamp__gte=now().replace(microsecond=0)
        ).first()
        if recent_log:
            return # Already logged deletion of this pair

    try:
        obj_str = str(instance)
    except TypeError:
        obj_str = str(instance.pk)

    request = get_current_request()
    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "") if request else ""

    UserActivityLog.safe_log(
        user=user,
        action=action,
        model_name=model_name,
        object_id=obj_id,
        number=obj_str[:50] if obj_str else None,
        details=None,
        ip_address=ip,
        user_agent=user_agent,
    )
