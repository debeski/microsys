# microsys Translation System Analysis

The [microsys](file:///home/debeski/xPy/microsys-pkg/microsys/context_processors.py#109-231) translation framework is a lightweight, high-performance, and entirely dynamic localization system built for Django. It bypasses Django's standard `gettext` (`.po`/`.mo` files) in favor of dynamic Python dictionaries, allowing rapid updates, JSON-based runtime overrides, side-by-side language loading, and automated DB-backed preferences.

## 1. High-Level Pipeline & Workflow

1. **Auto-Discovery:** Upon application startup or the first translation lookup, [microsys](file:///home/debeski/xPy/microsys-pkg/microsys/context_processors.py#109-231) scans all installed Django apps for a [translations.py](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py) file containing an `MS_TRANSLATIONS` dictionary.
2. **Merging & Caching:** All discovered dictionaries are deep-merged into a monolithic cache alongside the base `MICROSYS_STRINGS`.
3. **Language Resolution:** On each request, the system determines the target language through a cascading fallback mechanism (Profile > Session > SystemSettings > get_language() > 'ar').
4. **Context Injection:** [microsys_context](file:///home/debeski/xPy/microsys-pkg/microsys/context_processors.py#109-231) injects the evaluated language code, direction (RTL/LTR), and the flat translated dictionary (`MS_TRANS`) into the template context.
5. **Auto-Patching:** Using monkey-patching techniques initialized in `AppConfig.ready()`, generic system classes like `ModelForm`, `django_filters.FilterSet`, and `django_tables2.Table` are intercepted. Their fields and columns are injected with a [lazy_translator](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#1001-1013) proxy to dynamically translate labels at render-time.

---

## 2. Core Components

### [microsys/translations.py](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py)
This is the heart of the engine.
- **`MICROSYS_STRINGS`**: The base nested dictionary containing fallback 'ar' and 'en' keys for the core application.
- **[_discover_and_merge_translations()](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#899-936)**: Wraps standard `django.apps.get_app_configs()` behind an `@lru_cache(maxsize=1)`. It dynamically imports `{app_name}.translations`, extracting `MS_TRANSLATIONS` and deep-merging them globally.
- **[get_strings(lang_code=None, overrides=None)](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#937-1000)**: The evaluation engine. It merges strings in this strict order:
  1. Base Arabic (`'ar'`) strings as the ultimate fallback.
  2. The requested language strings (e.g., `'en'`).
  3. JSON `overrides` obtained from the `SystemSettings` singleton (configured via the Options UI).
- **[lazy_translator(key, default_val)](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#1001-1013)**: An essential piece for patching Django class attributes (like `verbose_name`). It returns a lazy string proxy that evaluates [get_strings()](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#937-1000) only when the Django template engine renders it, ensuring the string correctly adapts to the active language of the request thread processing it.

### `microsys.context_processors.microsys_context`
This injects translation data globally into HTML templates:
```python
context['CURRENT_LANG'] = current_lang
context['CURRENT_DIR'] = current_dir
context['LANGUAGES'] = languages
context['LANG_CONFIG'] = ...
context['MS_TRANS'] = ms_trans # The flat dictionary of translated keys
```

### Auto-Patching Engine ([microsys/patches.py](file:///home/debeski/xPy/microsys-pkg/microsys/patches.py) & [apps.py](file:///home/debeski/xPy/microsys-pkg/microsys/apps.py))
To achieve "Zero-Boilerplate" translation for auxiliary models and UI elements without adding [_()](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#1008-1011) translation markers everywhere, [microsys/apps.py](file:///home/debeski/xPy/microsys-pkg/microsys/apps.py) invokes [apply_scoped_patches()](file:///home/debeski/xPy/microsys-pkg/microsys/patches.py#304-310). This effectively intercepts Django's core UI generation:
- **`ModelForm` / `FilterSet`**: Iterates over `.fields` and `.filters`. It looks up keys recursively: `label_{name} -> label_{raw_label} -> {name} -> {raw_label}`. If a match is found in `MS_TRANS`, it wraps the field `label` with [lazy_translator](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#1001-1013).
- **`django_tables2.Table`**: Patches table headers by hooking into the underlying `column.column.verbose_name` and wrapping it with [lazy_translator](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#1001-1013), searching for prefixes like `tbl_{name}` and `label_{name}`.

### Template Tags ([microsys/templatetags/microsys_translation.py](file:///home/debeski/xPy/microsys-pkg/microsys/templatetags/microsys_translation.py))
Template utilities for formatting runtime data structures smoothly:
- **`{% translate_log_value value 'prefix' %}`**: Safely intercepts dynamic string variables (like activity log actions or tracked model names) and translates them by assembling a composite key string (e.g., `action_login`, `model_user`) to fetch securely from the `MS_TRANS` dictionary.
- *(Note)* Typical template strings are accessed via standard dictionary lookup without any custom tags: `{{ MS_TRANS.manage_users }}`.

---

## 3. Language Resolution Logic

The [get_strings()](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#937-1000) function resolves the active language for a specific request using a strict hierarchy to guarantee a bulletproof localized response:

1. **User Database Profile**: `request.user.profile.preferences.get('language')`. This stores the interface language globally, surviving session expirations and cross-device authentications.
2. **Session Storage**: `request.session.get('lang')` or `django_language`. Tracks anonymous users or unrecorded transient changes when the user utilizes the language toggle.
3. **Database Configuration**: Default language defined in `SystemSettings` (e.g., `MICROSYS_CONFIG.get('default_language')`) configured by an admin.
4. **Django Utility**: `django.utils.translation.get_language()` (Usually resolves browser's `Accept-Language` header).
5. **Hard Fallback**: Defaults to `'ar'` (Arabic) ensuring there's always a defined key dictionary loaded if all pipelines return null.

---

## 4. Extending and Customizations

The system accommodates localized strings dynamically scaling outwards avoiding rigid modifications to [microsys](file:///home/debeski/xPy/microsys-pkg/microsys/context_processors.py#109-231) core modules: 

### A. Code-Level Extension
Developers can add a [translations.py](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py) in the root of any standalone Django app within their project:
```python
# reports_app/translations.py
MS_TRANSLATIONS = {
    'ar': { 'reports_title': 'التقارير المتقدمة' },
    'en': { 'reports_title': 'Advanced Reports' }
}
```
**Effect**: [microsys](file:///home/debeski/xPy/microsys-pkg/microsys/context_processors.py#109-231) automatically discovers and incorporates `reports_title` during initialization into the global `MS_TRANS` context, making it instantly available everywhere.

### B. UI-Level (Dynamic) Overrides
The *System Settings* page (managed by Superusers) includes a generic `Translations Override (JSON)` field mapping directly to `SystemSettings.translations_override`.
```json
{
    "en": {
        "app_microsys": "Core Administration Environment" 
    }
}
```
**Effect**: Overwrites the hardcoded base `'app_microsys': 'System Management'` key value instantly without deployment or code edits by intercepting the final execution leg of [get_strings()](file:///home/debeski/xPy/microsys-pkg/microsys/translations.py#937-1000).
