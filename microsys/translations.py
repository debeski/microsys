# microsys/translations.py
# ========================
# Lightweight translation string table for the microsys framework.
# Developers can override any key via MICROSYS_CONFIG['translations'] in settings.py,
# or add new language dicts entirely. This dict is unlimited — add as many keys as needed.
#
# Usage in templates:  {{ MS_TRANS.key_name }}
# Usage in Python:     from microsys.translations import get_strings
#                      strings = get_strings('en')

MICROSYS_STRINGS = {
    # ───────────────────────────── Arabic (default) ─────────────────────────────
    'ar': {
        # Titlebar
        'help': 'مساعدة',
        'tour_title': 'جولة تعريفية',
        'profile': 'الملف الشخصي',
        'logout': 'تسجيل الخروج',
        'login': 'تسجيل الدخول',

        # Login page
        'username': 'اسم المستخدم',
        'password': 'كلمة المرور',
        'login_submit': 'دخول',

        # Dashboard
        'dashboard_welcome': 'مرحباً بك في النظام المتكامل لإدارة الموارد العامة.',
        'work_scope': 'نطاق العمل',
        'manage_users': 'إدارة المستخدمين',
        'manage_users_desc': 'إدارة حسابات المستخدمين والصلاحيات.',
        'manage_sections': 'إدارة الأقسام',
        'manage_sections_desc': 'هيكلة الأقسام والجهات والوحدات الإدارية.',
        'activity_log': 'سجل النشاط',
        'activity_log_desc': 'متابعة نشاطات المستخدمين والتغييرات.',
        'settings': 'الإعدادات',
        'settings_desc': 'خيارات النظام ومعلومات النسخة.',
        'go': 'الذهاب',
        'activity_24h': 'النشاط (آخر 24 ساعة)',

        # Options page
        'options_title': 'خيارات التطبيق',
        'accessibility': 'سهولة الوصول',
        'accessibility_desc': 'تخصيص العرض لمساعدة ذوي الإعاقة البصرية أو عمى الألوان.',
        'high_contrast': 'تباين عالي (High Contrast)',
        'grayscale': 'تدرج رمادي (Grayscale)',
        'invert': 'عكس الألوان (Invert)',
        'large_text': 'تكبير العرض (x1.5)',
        'no_animations': 'الحد من التحركات (Disable Animations)',
        'system_info': 'معلومات النظام',
        'server_time': 'وقت الخادم (Backend)',
        'storage': 'التخزين (Storage)',
        'os_info': 'نظام التشغيل (OS)',
        'python_version': 'نسخة Python',
        'django_version': 'نسخة Django',
        'drf_version': 'نسخة DRF',
        'api_status': 'حالة الـ API',
        'api_online': 'متاح (Online)',
        'api_offline': 'غير متاح (Offline)',
        'database': 'قاعدة البيانات (Database)',
        'cache': 'التخزين المؤقت (Cache)',
        'tasks': 'خادم المهام (Tasks)',
        'app_version': 'إصدار التطبيق (Version)',
        'themes': 'سمة الألوان',
        'themes_desc': 'اختر مظهر الألوان المفضل لديك لواجهة المنظومة.',
        'theme_white': 'أبيض',
        'theme_royal': 'ملكي',
        'theme_gold': 'ذهبي',
        'theme_green': 'أخضر',
        'theme_red': 'أحمر',
        'theme_dark': 'ليلي',
        'autofill': 'التعبئة التلقائية',
        'autofill_desc': 'تفعيل تعبئة البيانات تلقائياً من آخر خيار تم إدخاله (تاريخ, رقم, ...).',
        'on_off': 'تشغيل / إيقاف',
        'reset_defaults': 'استعادة الافتراضيات',
        'reset_desc': 'إعادة تعيين كافة تفضيلات المستخدم إلى الوضع الافتراضي (المظهر، اللغة، الخ).',
        'reset_btn': 'إعادة التعيين الآن',
        'reset_success': 'تمت استعادة الافتراضيات بنجاح.',
        'reset_confirm': 'هل أنت متأكد من رغبتك في استعادة كافة الإعدادات الافتراضية؟ سيتم تحديث الصفحة.',
        'language': 'اللغة',
        'language_desc': 'اختر لغة العرض المفضلة.',

        # Autofill toast
        'autofill_enabled': 'تم تفعيل التعبئة التلقائية.',
        'autofill_disabled': 'تم إيقاف التعبئة التلقائية.',

        # Auth / Admin verbose names (used by apps.py)
        'auth_system': 'نظام المصادقة',
        'permission_manage': 'ادارة الصلاحيات',
        'permissions': 'الصلاحيات',

        # Sidebar system group
        'sidebar_system': 'إدارة النظام',

        # Table headers (used by tables.py)
        'tbl_username': 'اسم المستخدم',
        'tbl_phone': 'رقم الهاتف',
        'tbl_email': 'البريد الالكتروني',
        'tbl_scope': 'النطاق',
        'tbl_full_name': 'الاسم الكامل',
        'tbl_is_staff': 'مسؤول',
        'tbl_is_active': 'نشط',
        'tbl_last_login': 'اخر دخول',
        'tbl_timestamp': 'وقت العملية',
        'tbl_model_name': 'النموذج',
        'tbl_action': 'الإجراء',
        'tbl_object_id': 'رقم العنصر',
        'tbl_number': 'الهدف',
        'tbl_scope_default': 'عام',

        # Filter placeholders
        'filter_search': 'البحث',
        'filter_year': 'السنة',
        'filter_scope': 'النطاق',
        'filter_all': 'الكل',
        'filter_from': 'من ',
        'filter_to': 'إلى ',

        # Template strings (manage_users)
        'add_user': 'إضافة مستخدم جديد',
        'manage_scopes_btn': 'إدارة النطاقات',
        'enable_scopes': 'تفعيل النطاقات',
        'confirm_delete': 'تأكيد الحذف',
        'delete_user_msg': 'هل انت متأكد انك تريد حذف المستخدم',
        'yes_delete': 'نعم، احذف',
        'cancel': 'إلغاء',
        'confirm': 'تأكيد',
        'loading': 'جاري التحميل...',
        'scope_warning_title': 'تحذير هام',
        'scope_warning_msg': 'هل أنت متأكد من رغبتك في تفعيل نظام النطاقات؟',
        'scope_warning_detail': 'تنبيه: بعد تفعيل النظام وتعيين المستخدمين لنطاقات محددة، لن تتمكن من تعطيله لاحقاً دون المخاطرة بفقدان بيانات هيكلية المستخدمين أو تعطل الصلاحيات، او فقدان امكانية الوصول الى البيانات الموجودة على التطبيق.',
        'scope_warning_note': 'لا يمكن تفعيل او الغاء تفعيل هذه الميزة الا بواسطة مدير النظام (Superuser).',
        'yes_activate': 'نعم، قم بالتفعيل',
        'cannot_disable_scopes': 'لا يمكن التعطيل لوجود مستخدمين مرتبطين بنطاقات',

        # Template strings (sections)
        'manage_label': 'إدارة',
        'list_label': 'قائمة',
        'save': 'حفظ',
        'add_label': 'إضافة',
        'edit_label': 'تعديل',
        'delete_label': 'حذف',
        'subsections': 'الأقسام الفرعية',
        'error_generic': 'حدث خطأ ما!',
        'no_models': 'لا توجد موديلات متاحة.',
        'model_load_error': 'هناك خطأ في تحميل المودل.',
        'view_label': 'عرض',

        # Activity log page
        # Activity log page
        'log_title': 'سجل النشاط',
        'no_items': 'لا توجد عناصر',
        'select_all': 'تحديد الكل',
        'unit_items': 'وحدة',

        # Apps & Models (Permissions / Sidebar)
        'app_microsys': 'إدارة النظام',
        'app_auth': 'نظام المصادقة',
        'app_admin': 'لوحة التحكم',
        'app_sessions': 'الجلسات',
        'app_contenttypes': 'أنواع المحتوى',
        'model_user': 'المستخدمين',
        'model_group': 'المجموعات',
        'model_permission': 'الصلاحيات',
        'model_scope': 'النطاقات',
        'model_log': 'سجل النشاط',
        'model_scope_settings': 'إعدادات النطاق',
        'model_section': 'الأقسام',
        'model_subsection': 'الأقسام الفرعية',
        'model_profile': 'ملف المستخدم',
        'model_useractivitylog': 'سجل النشاط',
        'model_password': 'كلمة المرور',
        'model_user profile': 'بيانات المستخدم',
        'model_auth': 'المصادقة',

        # Theme picker
        'theme_pick_color': 'اختر اللون',
        'theme_change': 'تغيير المظهر',
        'theme_light': 'أبيض',
        'theme_blue': 'ملكي',
        'theme_gold': 'ذهبي',
        'theme_green': 'أخضر',
        'theme_red': 'أحمر',
        'theme_dark': 'ليلي',
        'sidebar_reorder': 'إعادة الترتيب',

        # User form Labels
        'user_label': 'مستخدم',
        'reset_password': 'إعادة تعيين كلمة المرور',
        'form_username': 'اسم المستخدم',
        'form_password': 'كلمة المرور',
        'form_password_confirm': 'تأكيد كلمة المرور',
        'form_firstname': 'الاسم الأول',
        'form_lastname': 'اللقب',
        'form_email': 'البريد الإلكتروني',
        'form_phone': 'رقم الهاتف',
        'form_scope': 'النطاق',
        'form_permissions': 'الصلاحيات',
        'form_is_staff': 'صلاحيات انشاء و تعديل المستخدمين',
        'form_is_active': 'تفعيل الحساب',
        'form_profile_pic': 'الصورة الشخصية',
        'form_new_password': 'كلمة المرور الجديدة',
        'form_confirm_new_password': 'تأكيد كلمة المرور الجديدة',
        'form_old_password': 'كلمة المرور القديمة',
        'form_scope_name': 'اسم النطاق',
        
        # User form Help Text
        'help_username': 'اسم المستخدم يجب أن يكون فريدًا، 20 حرفًا أو أقل. فقط حروف، أرقام و @ . + - _',
        'help_email': 'أدخل عنوان البريد الإلكتروني الصحيح (اختياري)',
        'help_phone': 'أدخل رقم الهاتف الصحيح (اختياري)',
        'help_password_common': """
        <ul class="mb-0 ps-3"><li>كلمة المرور يجب ألا تكون مشابهة لمعلوماتك الشخصية.</li>
        <li>كلمة المرور يجب ان تحتوي على 8 حروف وارقام على الاقل.</li>
        <li>كلمة المرور يجب الا تكون شائعة والا تكون رقمية بالكامل.</li></ul>
        """,
        'help_password_match': 'أدخل نفس كلمة المرور مجددا للتحقق.',
        'help_is_active': 'يحدد ما إذا كان يجب اعتبار هذا الحساب نشطًا. قم بإلغاء تحديد هذا الخيار بدلاً من الحذف.',
        'help_is_staff': 'يحدد ما إذا كان يمكن للمستخدم عرض وادارة المستخدمين.',
        'help_is_staff_no_perm': 'ليس لديك صلاحية لتعيين هذا المستخدم كمسؤول.',
        'help_scope_self': 'لا يمكنك تغيير نطاقك الخاص لمنع تجريد نفسك من صلاحيات المدير العام.',
        
        # Buttons
        'btn_add': 'إضافة',
        'btn_update': 'تحديث',
        'btn_cancel': 'إلغاء',
        'btn_change_password': 'تغيير كلمة المرور',
        
        # Permissions UI
        'perm_staff_access': 'صلاحيات الإدارة',
        'perm_manage_users': 'إدارة المستخدمين',
        'perm_view_sections': 'عرض الأقسام',
        'perm_manage_sections': 'إدارة الأقسام',
        'perm_manage_staff': 'صلاحيات مستخدم مسؤول',
        'help_perm_manage_staff': 'يمنح المستخدم صلاحية تعيين مستخدمين آخرين كمسؤولين.',
        'perm_view_activity_log': 'عرض سجل النشاط',

        # Activity Log Actions
        'action_login': 'تسجيل دخول',
        'action_logout': 'تسجيل خروج',
        'action_create': 'إنشاء',
        'action_update': 'تحديث',
        'action_delete': 'حذف',
        'action_view': 'عرض',
        'action_download': 'تحميل',
        'action_confirm': 'تأكيد',
        'action_reject': 'رفض',
        'action_reset': 'إعادة تعيين',
        
        # Activity Log Modal
        'view_details': 'عرض التفاصيل',
        'activity_details': 'تفاصيل النشاط',
        'label_related_object': 'الكائن المرتبط',
        'label_changes': 'التغييرات / التفاصيل',
        'no_details': 'لا توجد تفاصيل مسجلة.',
        'btn_close': 'إغلاق',

        # Profile
        'role_superuser': 'مدير النظام',
        'role_staff': 'مستخدم مسؤول',
        'role_user': 'مستخدم عادي',
        'btn_update_data': 'تحديث البيانات',
        'btn_home': 'الرئيسية',
        'btn_confirm_password_change': 'تأكيد تغيير كلمة المرور',
        'profile_update_title': 'تحديث الملف الشخصي',
        'save_changes': 'حفظ التغييرات',
        'profile_picture': 'صورة الملف الشخصي',
        
        # Messages
        'msg_password_changed': 'تم تغيير كلمة المرور بنجاح!',
        'msg_form_error': 'هناك خطأ في البيانات المدخلة',

        # User Detail View
        'user_details_title': 'تفاصيل مستخدم',
        'user_details_header': 'تفاصيل المستخدم',
        'account_active': 'فعال',
        'account_inactive': 'معطل',
        'account_active_tooltip': 'حساب مفعل',
        'account_inactive_tooltip': 'حساب معطل',
        'staff_permissions_tooltip': 'لديه صلاحيات إدارية',
        'role_type': 'نوع الصلاحيات',
        'date_joined': 'تاريخ الانضمام',
        'back_to_users': 'العودة إلى إدارة المستخدمين',

        # Profile Enhancements
        'stats_total_actions': 'إجمالي العمليات',
        'stats_docs_created': 'ادخالات جديدة',
        'stats_edits': 'التعديلات',
        'stats_downloads': 'التنزيلات',
        'stats_recent_activity': 'آخر النشاطات',
        'stats_system_interactions': 'تفاعلات النظام',
        'profile_completeness': 'اكتمال الملف الشخصي',
        'account_health': 'حالة الحساب',
        'account_health_good': 'جيد',
        'account_health_attention': 'يحتاج انتباه',
        'badge_verified': 'موثق',
        'badge_admin': 'مسؤول',
        'badge_staff': 'موظف',
        'timeline_empty': 'لا يوجد نشاط حديث',

        # 2FA
        '2fa_title': 'المصادقة الثنائية',
        '2fa_desc': 'قم بتأمين حسابك باستخدام رمز تحقق يتم إرساله إلى بريدك الإلكتروني.',
        '2fa_enable': 'تفعيل المصادقة الثنائية',
        '2fa_disable': 'تعطيل المصادقة الثنائية',
        '2fa_enabled_msg': 'تم تفعيل المصادقة الثنائية بنجاح.',
        '2fa_disabled_msg': 'تم تعطيل المصادقة الثنائية.',
        '2fa_verify_title': 'تحقق من هويتك',
        '2fa_verify_desc': 'لقد أرسلنا رمز تحقق إلى بريدك الإلكتروني. الرجاء إدخاله أدناه.',
        'totp_scan_instruction': 'قم بمسح رمز QR هذا باستخدام تطبيق المصادقة الخاص بك (مثلاً Google Authenticator أو Authy).',
        'otp_sent_instruction': 'أدخل الرمز المرسل إلى',
        '2fa_code': 'رمز التحقق',
        '2fa_verify_btn': 'تحقق',
        '2fa_resend_btn': 'إعادة إرسال الرمز',
        '2fa_code_sent': 'تم إرسال رمز جديد إلى بريدك الإلكتروني.',
        '2fa_invalid_code': 'رمز غير صحيح أو منتهي الصلاحية.',
        '2fa_setup_email_subject': 'رمز تفعيل المصادقة الثنائية - microsys',
        '2fa_login_email_subject': 'رمز الدخول - microsys',
        '2fa_email_body': 'رمز التحقق الخاص بك هو: {code}. صلاحية الرمز 5 دقائق.',
        '2fa_method_backup': 'رموز الاسترداد',
        'backup_codes_title': 'رموز الاسترداد الاحتياطية',
        'backup_codes_desc': 'احتفظ بهذه الرموز في مكان آمن. يمكنك استخدامها لتسجيل الدخول في حال فقدان طرق المصادقة الاخرى.',
        'btn_view_generate': 'عرض / إنشاء',
        'btn_download_txt': 'تحميل كملف نصي',
        'btn_close': 'إغلاق',
        '2fa_backup_instruction': 'أدخل أحد رموز الاسترداد المكون من 8 أرقام.',
        '2fa_enabled_success': 'تم تفعيل المصادقة الثنائية بنجاح!',
        'backup_codes_warning': '<strong>تنبيه:</strong> سيتم عرض رموز الاسترداد هذه <strong>مرة واحدة فقط</strong>. احفظها فوراً.',
        'btn_close_reload': 'لقد حفظت الرموز',
        '2fa_method_email': 'المصادقة عبر البريد الإلكتروني',
        '2fa_method_phone': 'المصادقة عبر الهاتف (SMS)',
        '2fa_method_totp': 'تطبيق المصادقة (Authenticator App)',
        'btn_edit': 'تعديل',
        'btn_reset': 'إعادة تعيين',
        'modal_confirm_title': 'هل أنت متأكد؟',
        'modal_confirm_msg': 'هل تريد الاستمرار في هذا الإجراء؟',
        'msg_confirm_generate_backup': 'سيؤدي إنشاء رموز احتياطية جديدة إلى إلغاء صلاحية أي رموز سابقة. هل أنت متأكد من رغبتك في الاستمرار؟',
        'msg_confirm_disable_2fa': 'هل أنت متأكد من رغبتك في تعطيل المصادقة الثنائية لهذه الطريقة؟',
        'status_enabled': 'مفعل',
        'btn_generate_new': 'إنشاء رموز جديدة',
        'duration_minute': 'دقيقة',
        'duration_minutes': 'دقائق',
        'duration_hour': 'ساعة',
        'duration_hours': 'ساعات',
        'duration_day': 'يوم',
        'duration_days': 'أيام',
        'duration_week': 'أسبوع',
        'duration_weeks': 'أسابيع',
        'duration_month': 'شهر',
        'duration_months': 'شهور',
        'duration_and': 'و',
        'ago': 'منذ',
        'no_activity_recorded': 'لم يتم تسجيل نشاط بعد.',
    },

    # ───────────────────────────── English ─────────────────────────────
    'en': {
        # Titlebar
        'help': 'Help',
        'tour_title': 'Guided Tour',
        'profile': 'Profile',
        'logout': 'Logout',
        'login': 'Login',

        # Login page
        'username': 'Username',
        'password': 'Password',
        'login_submit': 'Sign In',

        # Dashboard
        'dashboard_welcome': 'Welcome to the integrated resource management system.',
        'work_scope': 'Work Scope',
        'manage_users': 'User Management',
        'manage_users_desc': 'Manage user accounts and permissions.',
        'manage_sections': 'Section Management',
        'manage_sections_desc': 'Structure departments, entities, and administrative units.',
        'activity_log': 'Activity Log',
        'activity_log_desc': 'Track user activities and changes.',
        'settings': 'Settings',
        'settings_desc': 'System options and version info.',
        'go': 'Go',
        'activity_24h': 'Activity (Last 24 Hours)',

        # Options page
        'options_title': 'Application Options',
        'accessibility': 'Accessibility',
        'accessibility_desc': 'Customize the display to assist users with visual impairments or color blindness.',
        'high_contrast': 'High Contrast',
        'grayscale': 'Grayscale',
        'invert': 'Invert Colors',
        'large_text': 'Large Text (x1.5)',
        'no_animations': 'Reduce Animations',
        'system_info': 'System Info',
        'server_time': 'Server Time (Backend)',
        'storage': 'Storage',
        'os_info': 'Operating System (OS)',
        'python_version': 'Python Version',
        'django_version': 'Django Version',
        'drf_version': 'DRF Version',
        'api_status': 'API Status',
        'api_online': 'Online',
        'api_offline': 'Offline',
        'database': 'Database',
        'cache': 'Cache',
        'tasks': 'Task Server',
        'app_version': 'App Version',
        'themes': 'Themes',
        'themes_desc': 'Choose your preferred color scheme for the interface.',
        'theme_white': 'White',
        'theme_royal': 'Royal',
        'theme_gold': 'Gold',
        'theme_green': 'Green',
        'theme_red': 'Red',
        'theme_dark': 'Dark',
        'autofill': 'Autofill',
        'autofill_desc': 'Auto-fill data from the last entered record (date, number, ...).',
        'on_off': 'On / Off',
        'reset_defaults': 'Reset Defaults',
        'reset_desc': 'Reset all user preferences to default (Theme, Language, etc).',
        'reset_btn': 'Reset Now',
        'reset_success': 'Preferences reset successfully.',
        'reset_confirm': 'Are you sure you want to reset all preferences? Page will reload.',
        'language': 'Language',
        'language_desc': 'Choose your preferred display language.',

        # Autofill toast
        'autofill_enabled': 'Autofill enabled.',
        'autofill_disabled': 'Autofill disabled.',

        # Auth / Admin verbose names (used by apps.py)
        'auth_system': 'Authentication System',
        'permission_manage': 'Permission Management',
        'permissions': 'Permissions',

        # Sidebar system group
        'sidebar_system': 'System Management',

        # Table headers (used by tables.py)
        'tbl_username': 'Username',
        'tbl_phone': 'Phone',
        'tbl_email': 'Email',
        'tbl_scope': 'Scope',
        'tbl_full_name': 'Full Name',
        'tbl_is_staff': 'Staff',
        'tbl_is_active': 'Active',
        'tbl_last_login': 'Last Login',
        'tbl_timestamp': 'Timestamp',
        'tbl_model_name': 'Model',
        'tbl_action': 'Action',
        'tbl_object_id': 'Object ID',
        'tbl_number': 'Target',
        'tbl_scope_default': 'General',

        # Filter placeholders
        'filter_search': 'Search',
        'filter_year': 'Year',
        'filter_scope': 'Scope',
        'filter_all': 'All',
        'filter_from': 'From ',
        'filter_to': 'To ',

        # Template strings (manage_users)
        'add_user': 'Add New User',
        'manage_scopes_btn': 'Manage Scopes',
        'enable_scopes': 'Enable Scopes',
        'confirm_delete': 'Confirm Delete',
        'delete_user_msg': 'Are you sure you want to delete user',
        'yes_delete': 'Yes, Delete',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'loading': 'Loading...',
        'scope_warning_title': 'Important Warning',
        'scope_warning_msg': 'Are you sure you want to enable the scopes system?',
        'scope_warning_detail': 'Warning: After enabling and assigning users to scopes, you will not be able to disable it later without risking loss of user structure data, permissions, or access to existing application data.',
        'scope_warning_note': 'Only a Superuser can enable or disable this feature.',
        'yes_activate': 'Yes, Activate',
        'cannot_disable_scopes': 'Cannot disable — users are assigned to scopes',

        # Template strings (sections)
        'manage_label': 'Manage',
        'list_label': 'List of',
        'save': 'Save',
        'add_label': 'Add',
        'edit_label': 'Edit',
        'delete_label': 'Delete',
        'subsections': 'Subsections',
        'error_generic': 'An error occurred!',
        'no_models': 'No models available.',
        'model_load_error': 'Error loading model.',
        'view_label': 'View',

        # Activity log page
        'log_title': 'Activity Log',
        'no_items': 'No items found',
        'select_all': 'Select All',
        'unit_items': 'items',

        # Apps & Models (Permissions / Sidebar)
        'app_microsys': 'System Management',
        'app_auth': 'Authentication System',
        'app_admin': 'Administration',
        'app_sessions': 'Sessions',
        'app_contenttypes': 'Content Types',
        'model_user': 'Users',
        'model_group': 'Groups',
        'model_permission': 'Permissions',
        'model_scope': 'Scopes',
        'model_log': 'Activity Logs',
        'model_scope_settings': 'Scope Settings',
        'model_section': 'Sections',
        'model_subsection': 'Subsections',
        'model_profile': 'User Profile',
        'model_useractivitylog': 'Activity Log',
        'model_password': 'Password',
        'model_user profile': 'User Data',
        'model_auth': 'Authentication',

        # Theme picker
        'theme_pick_color': 'Pick Color',
        'theme_change': 'Change Theme',
        'theme_light': 'Light',
        'theme_blue': 'Royal',
        'theme_gold': 'Gold',
        'theme_green': 'Green',
        'theme_red': 'Red',
        'theme_dark': 'Dark',
        'sidebar_reorder': 'Reorder',

        # User form Labels
        'user_label': 'User',
        'reset_password': 'Reset Password',
        'form_username': 'Username',
        'form_password': 'Password',
        'form_password_confirm': 'Confirm Password',
        'form_firstname': 'First Name',
        'form_lastname': 'Last Name',
        'form_email': 'Email Address',
        'form_phone': 'Phone Number',
        'form_scope': 'Scope',
        'form_permissions': 'Permissions',
        'form_is_staff': 'User Management Permissions',
        'form_is_active': 'Active Account',
        'form_profile_pic': 'Profile Picture',
        'form_new_password': 'New Password',
        'form_confirm_new_password': 'Confirm New Password',
        'form_old_password': 'Current Password',
        'form_scope_name': 'Scope Name',
        
        # User form Help Text
        'help_username': 'Username must be unique, 20 characters or fewer. Letters, digits and @/./+/-/_ only.',
        'help_email': 'Enter a valid email address (optional).',
        'help_phone': 'Enter a valid phone number (optional).',
        'help_password_common': """
        <ul class="mb-0 ps-3"><li>Password must be at least 8 characters long.</li>
        <li>Password can’t be too similar to your other personal information.</li>
        <li>Password can’t be a commonly used password or entirely numeric.</li></ul>
        """,
        'help_password_match': 'Enter the same password again, for verification.',
        'help_is_active': 'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        'help_is_staff': 'Designates whether the user can view and manage users.',
        'help_is_staff_no_perm': 'You do not have permission to assign this user as staff.',
        'help_scope_self': 'You cannot change your own scope to prevent removing yourself from admin privileges.',
        
        # Buttons
        'btn_add': 'Add',
        'btn_update': 'Update',
        'btn_cancel': 'Cancel',
        'btn_change_password': 'Change Password',
        
        # Permissions UI
        'perm_staff_access': 'Management Access',
        'perm_manage_users': 'User Management',
        'perm_view_sections': 'View Sections',
        'perm_manage_sections': 'Sections Management',
        'perm_manage_staff': 'Can manage staff',
        'help_perm_manage_staff': 'Grants the user permission to assign other users as staff.',
        'perm_view_activity_log': 'View activity log',

        # Activity Log Actions
        'action_login': 'Login',
        'action_logout': 'Logout',
        'action_create': 'Create',
        'action_update': 'Update',
        'action_delete': 'Delete',
        'action_view': 'View',
        'action_download': 'Download',
        'action_confirm': 'Confirm',
        'action_reject': 'Reject',
        'action_reset': 'Reset',

        # Activity Log Modal
        'view_details': 'View Details',
        'activity_details': 'Activity Details',
        'label_related_object': 'Related Object',
        'label_changes': 'Changes / Details',
        'no_details': 'No specific details recorded.',
        'btn_close': 'Close',

        # Profile
        'role_superuser': 'Superuser',
        'role_staff': 'Staff User',
        'role_user': 'Standard User',
        'btn_update_data': 'Update Info',
        'btn_home': 'Home',
        'btn_confirm_password_change': 'Confirm Password Change',
        'profile_update_title': 'Update Profile',
        'save_changes': 'Save Changes',
        'profile_picture': 'Profile Picture',
        
        # Messages
        'msg_password_changed': 'Password changed successfully!',
        'msg_form_error': 'There was an error with the submitted data',

        # User Detail View
        'user_details_title': 'User Details',
        'user_details_header': 'User Detail',
        'account_active': 'Active',
        'account_inactive': 'Inactive',
        'account_active_tooltip': 'Account is active',
        'account_inactive_tooltip': 'Account is inactive',
        'staff_permissions_tooltip': 'Has administrative permissions',
        'role_type': 'Role Type',
        'date_joined': 'Date Joined',
        'back_to_users': 'Back to User Management',

        # Profile Enhancements
        'stats_total_actions': 'Total Actions',
        'stats_docs_created': 'Documents Created',
        'stats_recent_activity': 'Recent Activity',
        'stats_system_interactions': 'System Interactions',
        'profile_completeness': 'Profile Completeness',
        'account_health': 'Account Health',
        'account_health_good': 'Good',
        'account_health_attention': 'Needs Attention',
        'badge_verified': 'Verified',
        'badge_admin': 'Admin',
        'badge_staff': 'Staff',
        'timeline_empty': 'No recent activity',

        # 2FA
        '2fa_title': 'Two-Factor Authentication',
        '2fa_desc': 'Secure your account with a verification code sent to your email.',
        '2fa_enable': 'Enable 2FA',
        '2fa_disable': 'Disable 2FA',
        '2fa_enabled_msg': 'Two-Factor Authentication enabled successfully.',
        '2fa_disabled_msg': 'Two-Factor Authentication disabled.',
        '2fa_verify_title': 'Verify Your Identity',
        '2fa_verify_desc': 'We sent a verification code to your email. Please enter it below.',
        'totp_scan_instruction': 'Scan this QR code with your authenticator app (e.g., Google Authenticator or Authy).',
        'otp_sent_instruction': 'Enter the code sent to your',
        '2fa_code': 'Verification Code',
        '2fa_verify_btn': 'Verify',
        '2fa_resend_btn': 'Resend Code',
        '2fa_code_sent': 'A new code has been sent to your email.',
        '2fa_invalid_code': 'Invalid or expired code.',
        '2fa_setup_email_subject': '2FA Activation Code - microsys',
        '2fa_login_email_subject': 'Login Code - microsys',
        '2fa_email_body': 'Your verification code is: {code}. Valid for 5 minutes.',
        '2fa_method_backup': 'Backup Codes',
        'backup_codes_title': 'Backup Codes',
        'backup_codes_desc': 'Use these codes to access your account if you lose your device. Each code can be used once.',
        'btn_view_generate': 'View / Generate',
        'btn_download_txt': 'Download as TXT',
        'btn_close': 'Close',
        '2fa_backup_instruction': 'Enter one of your 8-digit backup codes.',
        '2fa_enabled_success': 'Two-Factor Authentication Enabled!',
        'backup_codes_warning': '<strong>Warning:</strong> These recovery codes will only be shown <strong>once</strong>. Save them immediately.',
        'btn_close_reload': 'I have saved my codes',
        '2fa_method_email': 'Email Authentication',
        '2fa_method_phone': 'Phone Authentication',
        '2fa_method_totp': 'Authenticator App',
        'btn_edit': 'Edit',
        'btn_reset': 'Reset',
        'modal_confirm_title': 'Are you sure?',
        'modal_confirm_msg': 'Proceed with this action?',
        'msg_confirm_generate_backup': 'Generating new backup codes will invalidate any existing codes. Are you sure you want to proceed?',
        'msg_confirm_disable_2fa': 'Are you sure you want to disable 2FA for this method?',
        'status_enabled': 'Enabled',
        'btn_generate_new': 'Generate New Codes',
        'duration_minute': 'minute',
        'duration_minutes': 'minutes',
        'duration_hour': 'hour',
        'duration_hours': 'hours',
        'duration_day': 'day',
        'duration_days': 'days',
        'duration_week': 'week',
        'duration_weeks': 'weeks',
        'duration_month': 'month',
        'duration_months': 'months',
        'duration_and': ',',
        'ago': 'ago',
        'no_activity_recorded': 'No activity recorded yet.',
    },
}


from django.apps import apps
from importlib import import_module
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def _discover_and_merge_translations():
    """
    Auto-discover translations from all installed apps.
    Looks for 'translations.py' in each app and 'MS_TRANSLATIONS' dict.
    Returns a merged dictionary of all translations.
    """
    # Start with core strings
    merged_strings = dict(MICROSYS_STRINGS)

    for app_config in apps.get_app_configs():
        # Skip microsys itself as we already loaded it
        if app_config.name == 'microsys':
            continue
            
        try:
            # Try to import translations module
            module = import_module(f"{app_config.name}.translations")
            
            # Look for MS_TRANSLATIONS
            app_strings = getattr(module, 'MS_TRANSLATIONS', None)
            
            if app_strings and isinstance(app_strings, dict):
                # Deep merge logic
                for lang, keys in app_strings.items():
                    if lang not in merged_strings:
                        merged_strings[lang] = {}
                    merged_strings[lang].update(keys)
                    
        except ImportError:
            # App has no translations.py, just skip
            continue
        except Exception as e:
            logger.warning(f"Error loading translations from {app_config.name}: {e}")
            continue
            
    return merged_strings

def get_strings(lang_code, overrides=None):
    """
    Get the translation dict for a given language code.
    Falls back to 'ar' if the language is not found.
    Merges optional overrides on top.
    """
    # Get all discovered strings (cached)
    all_strings = _discover_and_merge_translations()
    
    # Start with Arabic as base fallback
    base = dict(all_strings.get('ar', {}))

    # Layer the requested language on top
    if lang_code != 'ar':
        lang_strings = all_strings.get(lang_code, {})
        base.update(lang_strings)

    # Layer project-level overrides on top
    if overrides and isinstance(overrides, dict):
        lang_overrides = overrides.get(lang_code, {})
        base.update(lang_overrides)

    return base
