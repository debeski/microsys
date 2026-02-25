# Imports of the required python modules and libraries
######################################################
from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import ScopedManager


class Scope(models.Model):
    name = models.CharField(max_length=100, verbose_name="النطاق")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Scope"
        verbose_name_plural = "Scopes"


class ScopeSettings(models.Model):
    is_enabled = models.BooleanField(default=False, verbose_name="تفعيل النطاقات")

    class Meta:
        verbose_name = "Scope Settings"
        verbose_name_plural = "Scope Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(ScopeSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "إعدادات النطاق"


class ScopeForeignKey(models.ForeignKey):
    """
    ForeignKey that hides itself from ModelForms when scopes are disabled.
    Keeps schema identical to a normal ForeignKey.
    """

    def formfield(self, **kwargs):
        try:
            from .utils import is_scope_enabled
            if not is_scope_enabled():
                return None
        except Exception:
            pass
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Treat as a normal ForeignKey in migrations to avoid churn.
        path = "django.db.models.ForeignKey"
        return name, path, args, kwargs


class ScopedModel(models.Model):
    """
    Abstract base class for models that should be isolated by Scope.
    Provides built-in audit trail (timestamps + actor tracking) and soft-delete.
    All audit fields are editable=False — auto-excluded from ModelForms.
    """
    scope = ScopeForeignKey('microsys.Scope', on_delete=models.PROTECT, null=True, blank=True, verbose_name="النطاق")

    # Timestamps (auto-managed)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="تاريخ التعديل")

    # Audit trail (auto-populated via save() override)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='+',
        on_delete=models.SET_NULL, editable=False, verbose_name="أنشئ بواسطة"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='+',
        on_delete=models.SET_NULL, editable=False, verbose_name="عدّل بواسطة"
    )

    # Soft-delete
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="تاريخ الحذف")
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='+',
        on_delete=models.SET_NULL, editable=False, verbose_name="حذف بواسطة"
    )

    objects = ScopedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Auto-populate created_by/updated_by from thread-local user."""
        from .middleware import get_current_user
        user = get_current_user()
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            if not self.pk:
                if not self.created_by_id:
                    self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Override: ALL deletes become soft-deletes. Actor auto-detected."""
        from .middleware import get_current_user
        self.deleted_at = timezone.now()
        user = get_current_user()
        if user and hasattr(user, 'is_authenticated') and user.is_authenticated:
            self.deleted_by = user
        self.save(update_fields=['deleted_at', 'deleted_by'])

    def soft_delete(self):
        """Explicit soft-delete (delegates to overridden delete)."""
        self.delete()

    def restore(self):
        """Undo soft-delete."""
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['deleted_at', 'deleted_by'])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently remove from database (escape hatch)."""
        super().delete(using=using, keep_parents=keep_parents)


class Profile(ScopedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name="المستخدم")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # deleted_at is inherited from ScopedModel
    preferences = models.JSONField(default=dict, blank=True, verbose_name="تفضيلات المستخدم")
    
    # 2FA Fields
    is_email_2fa_enabled = models.BooleanField(default=False, verbose_name="2FA via Email")
    is_phone_2fa_enabled = models.BooleanField(default=False, verbose_name="2FA via Phone")
    is_totp_2fa_enabled = models.BooleanField(default=False, verbose_name="2FA via App")
    totp_secret = models.CharField(max_length=32, blank=True, null=True, verbose_name="TOTP Secret")
    backup_codes = models.JSONField(default=list, blank=True, verbose_name="Backup Codes")

    @property
    def is_2fa_enabled(self):
        """Returns True if any 2FA method is enabled."""
        return self.is_email_2fa_enabled or self.is_phone_2fa_enabled or self.is_totp_2fa_enabled

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        default_permissions = ()
        permissions = [
            ("manage_staff", "Can manage staff"),
        ]


class UserActivityLog(ScopedModel):
    """
    Activity log model. Uses inherited ScopedModel fields:
    - created_by → the user who performed the action (was 'user')
    - created_at → when the action occurred (was 'timestamp')
    """
    # created_by (inherited) → replaces old 'user' field
    # created_at (inherited) → replaces old 'timestamp' field
    action = models.CharField(max_length=50, verbose_name="العملية")
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="القسم")
    object_id = models.IntegerField(blank=True, null=True, verbose_name="ID")
    number = models.CharField(max_length=50, null=True, blank=True, verbose_name="المستند")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="عنوان IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="agent")
    details = models.JSONField(default=dict, blank=True, null=True, verbose_name="التفاصيل")

    # Backward-compat properties for templates and tables
    @property
    def user(self):
        """Alias for created_by (backward compat)."""
        return self.created_by

    @property
    def timestamp(self):
        """Alias for created_at (backward compat)."""
        return self.created_at

    def __str__(self):
        return f"{self.created_by} {self.action} {self.model_name or 'General'} at {self.created_at}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        default_permissions = ()
        permissions = [
            ("view_activity_log", "View activity log"),
        ]

    @classmethod
    def safe_log(cls, user, action, model_name=None, object_id=None, number=None, details=None, ip_address=None, user_agent=None, scope=None):
        """
        Log an action only if a duplicate entry hasn't been created in the last 2 seconds.
        """
        from django.utils.timezone import now
        from datetime import timedelta
        
        # Debounce window
        time_threshold = now() - timedelta(seconds=2)
        
        # Check for duplicates
        duplicate = cls.objects.filter(
            created_by=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            created_at__gte=time_threshold
        )
        
        if details:
             duplicate = duplicate.filter(details=details)
             
        if duplicate.exists():
            return None

        # Automatically use actor's scope if not provided
        if not scope and user and hasattr(user, 'profile'):
            scope = user.profile.scope

        return cls.objects.create(
            created_by=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            number=number,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            scope=scope,
        )

class Section(models.Model):
    """Dummy Model for section permissions."""
    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ("view_sections", "View sections"),
            ("manage_sections", "Manage sections"),
        ]
