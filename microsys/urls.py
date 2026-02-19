# Imports of the required python modules and libraries
######################################################
from django.urls import path
from . import views, utils, api
from django.contrib.auth import views as auth_views

# app_name = 'microsys'

urlpatterns = [
    # Auth URLs (Django defaults - no prefix needed when mounted at root)
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    
    # System URLs (all prefixed with sys/)
    path('sys/', views.dashboard, name='sys_dashboard'),
    path('sys/users/', views.UserListView.as_view(), name='manage_users'),
    path('sys/users/create/', views.create_user, name='create_user'),
    path('sys/users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('sys/users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('sys/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('sys/users/<int:pk>/modal/', views.UserDetailModalView.as_view(), name='user_detail_modal'),

    path('sys/logs/', views.UserActivityLogView.as_view(), name='user_activity_log'),
    path('sys/logs/<int:pk>/details/', views.ActivityLogDetailView.as_view(), name='user_activity_log_detail'),
    path('sys/reset_password/<int:pk>/', views.reset_password, name='reset_password'),
    
    # Scope Management URLs
    path('sys/scopes/manage/', views.manage_scopes, name='manage_scopes'),
    path('sys/scopes/form/', views.get_scope_form, name='get_scope_form'),
    path('sys/scopes/form/<int:pk>/', views.get_scope_form, name='get_scope_form'),
    path('sys/scopes/save/', views.save_scope, name='save_scope'),
    path('sys/scopes/save/<int:pk>/', views.save_scope, name='save_scope'),
    path('sys/scopes/delete/<int:pk>/', views.delete_scope, name='delete_scope'),
    path('sys/scopes/toggle/', views.toggle_scopes, name='toggle_scopes'),

    # Sections Management URLs
    path('sys/options/', views.options_view, name='options_view'),
    path('sys/sections/', views.core_models_view, name='manage_sections'),
    path('sys/subsection/add/', views.add_subsection, name='add_subsection'),
    path('sys/subsection/edit/<int:pk>/', views.edit_subsection, name='edit_subsection'),
    path('sys/subsection/delete/<int:pk>/', views.delete_subsection, name='delete_subsection'),
    path('sys/section/delete/', views.delete_section, name='delete_section'),
    path('sys/section/details/', views.get_section_details, name='get_section_details'),
    
    # 2FA URLs
    path('sys/2fa/verify/enable/', views.verify_otp_view, {'intent': 'enable'}, name='verify_otp_enable'), # Maps to generic enable if needed, or specific
    path('sys/2fa/verify/login/', views.verify_otp_view, {'intent': 'login'}, name='verify_otp_login'),
    
    path('sys/2fa/verify/', views.verify_otp_view, name='verify_otp_generic'),
    path('sys/2fa/enable/', views.enable_2fa, name='enable_2fa'),
    path('sys/2fa/setup/totp/', views.setup_totp, name='setup_totp'),
    path('sys/2fa/disable/', views.disable_2fa, name='disable_2fa'),
    path('sys/2fa/backup-codes/generate/', views.generate_backup_codes, name='generate_backup_codes'),
    path('sys/2fa/resend/<str:intent>/', views.resend_otp, name='resend_otp'), # Generic resend
    path('sys/2fa/resend/', views.resend_otp, {'intent': 'login'}, name='resend_otp_login'),

    # Sidebar Toggle URL
    path('sys/toggle-sidebar/', utils.toggle_sidebar, name='toggle_sidebar'),

    # Autofill API
    path('sys/api/last-entry/<str:app_label>/<str:model_name>/', api.get_last_entry, name='api_get_last_entry'),
    path('sys/api/details/<str:app_label>/<str:model_name>/empty_schema/', api.get_model_details, {'pk': 'empty_schema'}, name='api_get_empty_schema'),
    path('sys/api/details/<str:app_label>/<str:model_name>/<int:pk>/', api.get_model_details, name='api_get_model_details'),
    path('sys/api/preferences/update/', views.update_preferences, name='update_preferences'),
    path('sys/api/preferences/reset/', views.reset_preferences, name='reset_preferences'),
]

