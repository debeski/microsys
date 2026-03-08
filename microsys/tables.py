import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.apps import apps
from django.utils.safestring import mark_safe
from .translations import get_strings
from .utils import filter_context_actions
from django.conf import settings

User = get_user_model()


def _get_default_strings():
    """Get translation strings using the project default language."""
    from .utils import get_system_config
    config_dict = get_system_config()
    lang = config_dict.get('default_language', 'ar')
    overrides = config_dict.get('translations', None)
    return get_strings(lang, overrides=overrides)


from django.urls import reverse
import json

class UserTable(tables.Table):
    username = tables.Column(verbose_name="اسم المستخدم")
    phone = tables.Column(verbose_name="رقم الهاتف", accessor='profile.phone', default='-')
    email = tables.Column(verbose_name="البريد الالكتروني")
    scope = tables.Column(verbose_name="النطاق", accessor='profile.scope.name', default='-')
    full_name = tables.Column(
        verbose_name="الاسم الكامل",
        accessor='profile.full_name', # Assuming profile has full_name property, or use user.get_full_name
        order_by='first_name'
    )
    is_staff = tables.BooleanColumn(verbose_name="مسؤول")
    is_active = tables.BooleanColumn(verbose_name="نشط")
    last_login = tables.DateColumn(
        format="H:i Y-m-d ",
        verbose_name="اخر دخول"
    )
    # actions = tables.TemplateColumn(
    #     template_name='microsys/users/user_actions.html',
    #     orderable=False,
    #     verbose_name='',
    # )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap5.html"
        fields = ("username", "phone", "email", "full_name", "scope", "is_staff", "is_active","last_login")
        attrs = {'class': 'table table-hover align-middle'}
        row_attrs = {
            "data-micro-context": "true",
            "data-micro-actions": lambda record: json.dumps([
                {"label": "view_label", "icon": "bi bi-eye", "type": "event", "event": "micro:view-user-details", "data": {"url": reverse('user_detail_modal', args=[record.pk])}, "dblclick": True},
                {"type": "divider"},
                {"label": "edit_label", "icon": "bi bi-pencil", "type": "event", "event": "micro:record:edit", "data": {"model": "user", "id": record.pk, "name": getattr(record, 'full_name', record.username) or record.username}},
                {"label": "reset_password", "icon": "bi bi-key", "type": "event", "event": "micro:reset-password", "data": {"id": record.pk, "username": record.username, "url": reverse('reset_password', args=[record.pk])}},
            ]) # Simplified for now, auto-patch will handle labels if we use keys
        }
        # row_attrs is handled in __init__ to allow dynamic behavior

class UserActivityLogTable(tables.Table):
    timestamp = tables.DateColumn(
        format="H:i Y-m-d ",
        verbose_name="وقت العملية",
        accessor='created_at'  # Use inherited field via accessor
    )
    full_name = tables.Column(
        verbose_name="الاسم الكامل",
        accessor='created_by.profile.full_name',
        order_by='created_by__first_name'
    )
    scope = tables.Column(
        verbose_name="النطاق",
        accessor='created_by.profile.scope.name',
        default='عام'
    )
    # Explicitly declare to prevent django-tables2 from using get_FOO_display()
    action = tables.Column(verbose_name="الإجراء")
    model_name = tables.Column(verbose_name="النموذج")

    class Meta:
        model = apps.get_model('microsys', 'UserActivityLog')
        template_name = "django_tables2/bootstrap5.html"
        fields = ("timestamp", "created_by", "full_name", "model_name", "action", "object_id", "number", "scope")
        exclude = ("id", "ip_address", "user_agent", "created_at", "updated_at", "updated_by", "deleted_at", "deleted_by")
        attrs = {'class': 'table table-hover align-middle'}
        row_attrs = {
            "data-micro-context": "true",
            "data-micro-actions": lambda record: json.dumps([
                {"label": "view_details", "icon": "bi bi-eye", "type": "event", "event": "micro:view-log-details", "data": {"url": reverse('user_activity_log_detail', args=[record.pk])}, "dblclick": True}
            ]),
        }

    def render_action(self, value, record):
        """Translate action type dynamically."""
        from .utils import _get_request_translations
        s = _get_request_translations(getattr(self, 'request', None))
        raw_value = record.action
        if not raw_value:
            return "-"
        return s.get(f"action_{raw_value.lower()}", raw_value)

    def render_model_name(self, value):
        """Translate model name dynamically."""
        if not value:
            return "-"
        from .utils import _get_request_translations
        s = _get_request_translations(getattr(self, 'request', None))
        keys_to_try = [
            f"model_{value.lower().replace('.', '_')}", 
            f"model_{value.split('.')[-1].lower()}"
        ]
        for key in keys_to_try:
            if key in s:
                return s[key]
        return value




class UserActivityLogTableNoUser(UserActivityLogTable):
    class Meta(UserActivityLogTable.Meta):
        exclude = ("user", "user.full_name", "scope")

class ScopeTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='microsys/scopes/scope_actions.html',
        orderable=False,
        verbose_name=''
    )
    class Meta:
        model = apps.get_model('microsys', 'Scope')
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "actions")
        attrs = {'class': 'table table-hover align-middle'}
