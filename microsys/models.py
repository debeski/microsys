# Imports of the required python modules and libraries
######################################################
from django.db import models
from django.conf import settings
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
    """
    scope = ScopeForeignKey('microsys.Scope', on_delete=models.PROTECT, null=True, blank=True, verbose_name="النطاق")
    
    objects = ScopedManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class Profile(ScopedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name="المستخدم")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الحذف")
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="اسم المستخدم", null=True, blank=True)
    action = models.CharField(max_length=50, verbose_name="العملية")
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="القسم")
    object_id = models.IntegerField(blank=True, null=True, verbose_name="ID")
    number = models.CharField(max_length=50, null=True, blank=True, verbose_name="المستند")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="عنوان IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="agent")
    details = models.JSONField(default=dict, blank=True, null=True, verbose_name="التفاصيل")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="الوقت")

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name or 'General'} at {self.timestamp}"

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
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            timestamp__gte=time_threshold
        )
        
        if details:
             # Basic check if details match. precise match for JSON might be strict but good for duplicates.
             duplicate = duplicate.filter(details=details)
             
        if duplicate.exists():
            return None

        # Automatically use actor's scope if not provided
        if not scope and user and hasattr(user, 'profile'):
            scope = user.profile.scope

        return cls.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            number=number,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            scope=scope,
            timestamp=now()
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
