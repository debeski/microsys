# micro - System Integration Service

[![PyPI version](https://badge.fury.io/py/django-microsys.svg)](https://pypi.org/project/django-microsys/)

<p align="center">
  <img src="https://raw.githubusercontent.com/debeski/django-microsys/main/microsys/static/img/login_logo.webp" alt="microSys Logo" width="450"/>
</p>

**Arabic** lightweight, reusable Django app providing comprehensive system integration services, including user management, profile extension, permissions, localization, dynamic sidebar, automated activity logging and more.

## Requirements
- Python 3.11+
- Django 5.2+
- django-crispy-forms 2.4+
- crispy-bootstrap5 2025.5+
- django-tables2 2.8+
- django-filter 25+
- django-health-check 3.20+
- babel 2.1+
- psutil

## Features
- **System Integration**: Centralized management for users and system scopes.
- **Profile Extension**: Automatically links a `Profile` to your existing User model.
- **Scope Management**: Optional, dynamic scope isolation system with abstract `ScopedModel`.
- **Dynamic Sidebar**: Auto-discovery of list views and customizable menu items.
- **Permissions**: Custom grouped permission UI (App/Model/Action).
- **Automated Logging**: Full activity tracking (CRUD, Login/Logout) via Signals.
- **Localization**: Native Arabic support with dynamic language switching (RTL/LTR).
- **Theming & Accessibility**: Built-in dark/light modes and accessibility tools (High Contrast, Zoom, etc.).
- **Security**: CSP compliance, role-based access control (RBAC).

## Installation

```bash
pip install git+https://github.com/debeski/django-microsys.git
# OR
pip install django-microsys
```

## Quick Start & Configuration

1. **Add to `INSTALLED_APPS`:**
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       # ... dependencies
       'crispy_forms',
       'crispy_bootstrap5',
       'django_filters',
       'django_tables2',

       'microsys', # Place anywhere.
   ]
   ```

2. **Add Middleware:**
   Required for activity logging and request caching.
   ```python
   MIDDLEWARE = [
       # ...
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       # ... Must be below Auth Middleware
       'microsys.middleware.ActivityLogMiddleware',
   ]
   ```

3. **Add Context Processor:**
   Unified context processor for branding, sidebar, and scope settings.
   ```python
   TEMPLATES = [
       {
           # ...
           'OPTIONS': {
               'context_processors': [
                   # ...
                   'microsys.context_processors.microsys_context',
               ],
           },
       },
   ]
   ```

4. **Include URLs:**
   Mount at **root** for seamless Django auth integration:
   ```python
   from django.urls import path, include

   urlpatterns = [
       # ...
       path('', include('microsys.urls')),  # Mount at root
   ]
   ```
   
   This provides:
   - `/accounts/login/` and `/accounts/logout/` (Django defaults)
   - `/sys/` for all system management routes

   > ⚠️ **Warning:** If your project already uses `/accounts/` URLs (e.g., `django-allauth`), you'll have conflicts. In that case, mount with a prefix and configure custom auth URLs:
   > ```python
   > # urls.py
   > path('microsys/', include('microsys.urls')),
   > 
   > # settings.py
   > LOGIN_URL = '/microsys/accounts/login/'
   > LOGIN_REDIRECT_URL = '/microsys/sys/'
   > LOGOUT_REDIRECT_URL = '/microsys/accounts/login/'
   > ```

5. **Run Setup Command:**
   ```bash
   python manage.py microsys_setup
   ```
   This will create migrations, apply them, and validate your configuration.

## Management Commands

### `microsys_setup`
Initial setup command that handles migrations and configuration validation.

```bash
# Full setup (recommended for first install)
python manage.py microsys_setup

# Skip configuration check
python manage.py microsys_setup --skip-check

# Only validate config (skip migrations)
python manage.py microsys_setup --no-migrate
```

### `microsys_check`
Validates your Django settings and shows exact code snippets for any missing configuration.

```bash
python manage.py microsys_check
```

**Output example:**
```
🔍 MicroSys Configuration Check
==================================================

📋 INSTALLED_APPS: ✓ OK
📋 MIDDLEWARE: ✗ MISSING
📋 CONTEXT_PROCESSORS: ✓ OK
📋 URLS: ✓ OK
📋 CRISPY_FORMS: ✓ OK

==================================================
❌ REQUIRED CONFIGURATION MISSING:

▶ MIDDLEWARE:

MIDDLEWARE = [
    # ... after AuthenticationMiddleware
    'microsys.middleware.ActivityLogMiddleware',
]
```

> **Note:** microsys also validates your configuration at runtime and will emit warnings if required middleware or context processors are missing.

## App Configuration

Customize branding and behavior by adding `MICROSYS_CONFIG` and `SIDEBAR_AUTO` to your `settings.py`:

```python
MICROSYS_CONFIG = {
    'name': 'My System Name',           # App title in navbar/pages
    'verbose_name': 'ادارة النظام',      # App title in navbar/pages
    'logo': '/static/img/logo.png',     # Base/logo shown in the titlebar
    'login_logo': '/static/img/login_logo.webp',  # Logo on login screen
    'description': 'System Desc',       # Optional description
    'home_url': '/sys/',                 # Titlebar home link (default: /sys/)
    
    # ... branding fields only

    # Language switching (optional, Arabic-only by default)
    'languages': {
        'ar': {'name': 'العربية', 'dir': 'rtl', 'flag': '🇱🇾'},
        'en': {'name': 'English', 'dir': 'ltr', 'flag': '🇬🇧'},
    },
    'default_language': 'ar',  # Fallback language

    # Override or extend built-in translation strings (optional)
    # 'translations': {
    #     'en': {'dashboard_welcome': 'Welcome to My Custom System.'},
    # },
}

# Auth redirects (defaults are set by microsys if not provided)
LOGIN_REDIRECT_URL = '/sys/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

SIDEBAR_AUTO = {
    'ENABLED': True,                    # Enable auto-discovery
    'URL_PATTERNS': ['list'],           # Keywords to match in URL names for auto-menu
    'EXCLUDE_APPS': ['admin', 'auth'],  # Apps to exclude
    'CACHE_TIMEOUT': 3600,              # Cache timeout in seconds
    'DEFAULT_ICON': 'bi-list',          # Default Bootstrap icon

    # Built-in system group (accordion) can be disabled if desired
    'SYSTEM_GROUP_ENABLED': True,

    # Override auto-discovered items
    'DEFAULT_ITEMS': {
        'decree_list': {          # Key is the URL name
            'label': 'Decisions', # Override label
            'icon': 'bi-gavel',   # Override icon
            'order': 10,          # Sort order
        },
    },

    # Add manual items (e.g. for views without models)
    'EXTRA_ITEMS': {
        'الإدارة': {  # Accordion Group Name
            'icon': 'bi-gear',
            'items': [
                {
                    'url_name': 'manage_sections',
                    'label': 'إدارة الأقسام',
                    'icon': 'bi-diagram-3',
                    'permission': 'is_staff',
                },
            ]
        }
    }
}
```

## Language Switching

microsys ships with Arabic and English translations. Add more languages via `MICROSYS_CONFIG['languages']`.

**How it works:**
- Language is resolved: **user preference** → **`default_language`** → **`'ar'`**
- Templates use `{{ MS_TRANS.key }}` for all UI strings
- The `<html>` tag gets dynamic `lang`/`dir` attributes
- Bootstrap CSS auto-switches between RTL and LTR variants
- Users switch languages from the Options page; a page reload applies translated strings

**Template variables available:**
| Variable | Type | Description |
|---|---|---|
| `CURRENT_LANG` | `str` | Active language code (e.g. `'ar'`, `'en'`) |
| `CURRENT_DIR` | `str` | Active direction (`'rtl'` or `'ltr'`) |
| `LANGUAGES` | `dict` | All configured languages |
| `MS_TRANS` | `dict` | Translated strings for the active language |

**Adding custom strings:**
```python
# In microsys/translations.py or via MICROSYS_CONFIG['translations']
MICROSYS_CONFIG = {
    'translations': {
        'ar': {'my_key': 'قيمة مخصصة'},
        'en': {'my_key': 'Custom Value'},
    },
}
```
Then in templates: `{{ MS_TRANS.my_key }}`

## Core Components Usage

### 1. Profile Access
`microsys` automatically creates a `Profile` for every user via signals.
```python
# Accessing profile data
phone = user.profile.phone
scope = user.profile.scope
```

### 2. ScopedModel (Data Isolation)
To enable automatic scope filtering and soft-delete, **YOUR MODELS MUST** inherit from:
```python
from microsys.models import ScopedModel

class MyModel(ScopedModel):
    name = models.CharField(...)
    # ...
```
- **Automatic Scope Recognition**: `ScopedModel` already uses global scope settings, so you don't need to do anything.
- **Automatic Filtering**: Queries are automatically filtered by the current user's scope.
- **Soft Delete**: `MyModel.objects.get(pk=1).delete()` sets `deleted_at` instead of removing the row.

### 3. Sidebar Features
- **Auto-Discovery**: Automatically finds views like `*_list` and adds them to the sidebar.
- **Toggle**: Users can collapse/expand the sidebar; preference is saved in the session.
- **Reordering**: Drag-and-drop reordering is supported for authorized users.

### 4. Themes & Accessibility
Built-in support for:
- **Themes**: Dark / Light and colors.
- **Accessibility Modes**:
  - High Contrast
  - Grayscale
  - Invert Colors
  - x1.5 Zoom
  - Disable Animations
- **Location**: Accessible via the User Options menu (`options.html`) and Sidebar toolbar.

---

## Dynamic Section Mode

Microsys offers a powerful "Zero-Boilerplate" CRUD interface for managing auxiliary data models (like Departments, Categories, etc.).

### How It Works
1. **Mark Your Model**: Add `is_section = True` to your model attrs.
   ```python
   class Department(ScopedModel):
       name = models.CharField(...)
       is_section = True
   ```
2. **Auto-Discovery**: The system automatically generates a management UI with:
   - Searchable Table (with pagination & sorting)
   - Add/Edit Modals (using Crispy Forms)
   - Delete protection (checks for related records)
   - Filters (Keyword search + Date ranges if applicable)

   > **Note**: You can customize the auto-generated components by adding `form_exclude` and `table_exclude` lists to your model:
   > ```python
   > class Department(ScopedModel):
   >     # ...
   >     form_exclude = ['internal_notes']
   >     table_exclude = ['internal_notes', 'created_at']
   > ```

### Auto Subsections (Parent-Child Relations)
If a Section model has a `ManyToManyField` to another model that is **not** a standalone section (i.e. a "child" model), the system automatically nests it:

```python
class SubUnit(ScopedModel):  # Child model (no is_section=True)
    name = models.CharField(...)

class MainUnit(ScopedModel): # Parent section
    is_section = True
    sub_units = models.ManyToManyField(SubUnit)
```

**Result:**
- When editing a `MainUnit`, you will see a list of `SubUnits`.
- You can **Add/Edit/Delete** `SubUnits` directly from the `MainUnit` modal via AJAX.
- This creates a seamless "Master-Detail" management experience without writing a single view or form.

Notes:
- These attributes apply only to the auto-generated form/table.
- If you provide a custom Form/Table class, it takes full precedence.

---

## Templates & Theming

### Base Template
The system provides a robust base template located at `microsys/templates/microsys/base.html`.
You can extend this template in your own views to maintain consistent layout and functionality:

```html
{% extends "microsys/base.html" %}

{% block extra_head %}
    <!-- Extra CSS or Meta tags -->
{% endblock %}

{% block content %}
    <h1>Page Content</h1>
{% endblock %}

{% block scripts %}
    <!-- Extra JS scripts -->
{% endblock %}
```

> **Note:** The base template automatically handles the sidebar, title bar, messages, and theme loading. Replacing it entirely will break core system functionality.

### Theming
- **Framework**: Built on **Bootstrap 5 (RTL)**.
- **Colors**: The `primary` color automatically adapts to the selected theme. Secondary/Success/Danger colors are slightly desaturated for better visual ergonomics.
- **Customization**:
  - Use standard Bootstrap classes (`btn-primary`, `text-success`, etc.).
  - Dark mode is supported out of the box. If you encounter issues, you can override styles via `extra_head` or report them.
### Unified User Preferences (DB-Backed)
The system now centralizes user UI settings in the database instead of relying on `localStorage` or server sessions. This ensures that a user's chosen theme, sidebar state, and item ordering are consistent across all their devices.

- **Storage**: Preferences are stored in a `JSONField` named `preferences` within the `Profile` model.
- **Syncing**: An API endpoint (`/sys/api/preferences/update/`) handles real-time updates from the frontend.
- **Persistence**:
  - **Sidebar**: Collapsed/Expanded state and open accordion groups are persisted.
  - **Reordering**: Drag-and-drop order of sidebar items is saved globally.
  - **Theme**: Selected UI theme (Light, Dark, Royal, etc.) is synced.

> [!IMPORTANT]
> To enable this feature, ensure you have applied migrations (`makemigrations microsys` and `migrate microsys`).

---

## 🎨 Customizing Head & Scripts (Injection)

You can inject custom HTML, CSS, or JavaScript into the `microsys` base template globally without overriding the entire template.
This is useful for adding analytics scripts, global styles, or meta tags.

### How to use:
Create the following files in your project's `templates/` directory:

1.  **Head Content (Meta, CSS)**: `microsys/includes/custom_head.html`
    - Renders in `<head>`, **before** `{% block extra_head %}`.
    - Ideal for global CSS overrides or meta tags.

2.  **Scripts**: `microsys/includes/custom_scripts.html`
    - Renders just before `</body>`.
    - Ideal for global JS libraries or analytics.

> **Note**: Because these are templates (not static files), you can use template tags like `{% static %}` or `{% url %}` inside them, in addition to conditional logic!

### Dashboard Activity Chart
The dashboard now includes a built-in activity chart powered by **Plotly.js**:
- **Visualizes**: System activity for the last 24 hours.
- **Design**: Seamless, transparent, lightweight line chart with no axis labels for a clean look.
- **Data Source**: Aggregates `UserActivityLog` entries.
- **Responsive**: Automatically resizes with the window and sidebar toggles using `ResizeObserver`.

----

## File Structure

```
microsys/
├── management/             # Custom Management commands.
├── migrations/             # App Migrations.
├── static/                 # microsys/ (js/css/img).
├── templates/              # microsys/ (flattened structure).
├── templatetags/           # Custom template tags.
├── tests/                  # Development tests.
├── admin.py                # Admin Panel Registration.
├── api.py                  # Autofill Api Configuration, Permission Checker, Serializer.
├── apps.py                 # Django App configuration.
├── context_processors.py   # Branding, Scope, Sidebar order and Themes.
├── discovery.py            # Sidebar auto-discovery logic.
├── fetcher.py              # Universal Dynamic Downlolader.
├── filters.py              # User and ActivityLog filters.
├── forms.py                # User, Profile, Permissions, and Section forms
├── managers.py             # ScopedModel Manager.
├── middleware.py           # ActivityLog middleware.
├── models.py               # Profile, Scope, Logs.
├── signals.py              # Auto-create profile logic, Auto soft-delete logic, ActivityLog.
├── tables.py               # User, ActivityLog, and Scope tables.
├── urls.py                 # URL routing.
├── utils.py                # Helping Dynamic functions.
└── views.py                # User and Scope management, Dynamic Zero-Boilerplate Section management.
```

## Version History

| Version  | Changes |
|----------|---------|
| v1.0.0   | • Initial release as pip package |
| v1.1.0   | • URL restructure: auth at `/accounts/`, system at `/sys/` • Added `microsys_setup` and `microsys_check` management commands • Runtime configuration validation |
| v1.2.0   | • Name changed to `django-microsys` • Section model discovery hardened (dynamic app resolution, generic forms/tables/filters) • Scope fields now hide automatically when scopes are disabled • System sidebar group ships by default (configurable) • `is_staff` moved into the permissions UI |
| v1.3.0   | • Fixed subsection display: subsections now show correctly regardless of user scope • Fixed SessionInterrupted error: reduced session writes in section management • Scope toggle now accepts explicit target state to prevent race conditions • Improved error messaging in Arabic for scope operations |
| v1.4.0   | • Section table context menu: right-click on table rows for Edit/Delete actions • View Subsections modal: sections with M2M subsections show linked items • AJAX-based section deletion with related-record protection • Auto-generated tables now include row data attributes for JS binding |
| v1.5.0   | • Auto-generated section filters now include date range pickers (from/to) with flatpickr integration • Added clarifying inline comments to complex view logic • Fixed login Enter key submission • Pypi Release |
| v1.5.1   | • Fixed Readme file and added detailed instructions |
| v1.5.2   | • Optimized form and filters auto generation and layout |
| v1.5.3   | • Added global head and scripts injection |
| v1.5.4   | • Switch to Database JSON attached to user profile for consistent prefrences accross devices |
| v1.5.5   | • Fixed theme picker popup positioning in LTR mode (CSS logical properties) • Comprehensive i18n: table headers, filter labels/placeholders, and template strings now resolved from `translations.py` per user language • Tables, filters, and templates (`manage_users`, `user_activity_log`, `manage_sections`) fully translated |
| v1.5.6   | • Reset Defaults now purges sidebar reordering from DB and localStorage • Reset UI redesigned to match other options (inline Confirm/Cancel animation) • Fixed activity log actions always showing in Arabic regardless of language (duplicate `get_table_kwargs`) • Fixed hardcoded Arabic model name 'مصادقة' in login/logout signals — now uses translatable key |