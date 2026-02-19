from django import template
from microsys.translations import get_strings

register = template.Library()

@register.filter
def translate_log(value, prefix=''):
    """
    Translates a log value (action, model_name) using the microsys translation system.
    Usage: {{ log.action|translate_log:'action' }} -> looks for 'action_LOGIN' (lowercase)
    Usage: {{ log.model_name|translate_log:'model' }} -> looks for 'model_user' (lowercase)
    """
    if not value:
        return ""
        
    # Get current language from context logic is tricky in a simple filter without context
    # ideally we should use a simple_tag with takes_context=True, 
    # but filters are cleaner in templates.
    # However, get_strings needs a lang code. 
    # Let's try to get it from the thread locals or assume 'ar' default if not passed.
    # OR, we can rely on the view passing 'MS_TRANS' and just look up in that dictionary?
    # BUT the user wants a filter. 
    
    # Better approach: The view already passes MS_TRANS.
    # But wait, looking up dynamic keys in a massive dict in template is verbose:
    # {{ MS_TRANS|get_item:log.action }} -> cumbersome if we need to prefix.
    
    # Let's stick to a filter that retrieves the thread language if possible, 
    # or better yet, accepts the MS_TRANS dict as an arg? No that's ugly.
    
    # Let's use the thread local middleware approach if available? 
    # No, let's keep it simple. We can try to access the language from the request 
    # if we change this to takes_context=True simple_tag.
    
    # Wait, the user prompt implies a simple filter.
    # Let's try to infer language or just use 'ar' as default for now, 
    # as the system seems predominantly Arabic focused based on translations.py.
    # Actually, let's try to get the language from the active translation object if possible.
    
    # Let's look at how `microsys.utils._get_request_translations` works.
    # It gets lang from session. We don't have request here easily.
    
    # Alternative: Use a simple tag that takes context.
    pass

@register.simple_tag(takes_context=True)
def translate_log_value(context, value, prefix=''):
    """
    Translates a log value using the MS_TRANS dictionary available in context.
    """
    if not value:
        return ""
        
    ms_trans = context.get('MS_TRANS', {})
    if not ms_trans:
        # Fallback if MS_TRANS not in context (shouldn't happen in profile)
        return str(value)
        
    # Construct key: e.g. 'action_login', 'model_user'
    key = f"{prefix}_{str(value).lower()}" if prefix else str(value).lower()
    
    # Look up
    return ms_trans.get(key, value)

@register.simple_tag
def format_log_details(details):
    """
    Format the details JSON into a readable HTML string.
    """
    if not details or not isinstance(details, dict):
        return ""
        
    html_parts = []
    
    # Check for specific types
    if 'filename' in details:
        # Download/Export
        fname = details.get('filename')
        count = details.get('count', 1)
        html_parts.append(f'<i class="bi bi-file-earmark-arrow-down me-1"></i> {fname} <span class="badge bg-light text-dark ms-1">{count} items</span>')
        
    else:
        # Update Diffs
        for field, changes in details.items():
            # Security Masking
            if field in ['password', 'backup_codes', 'token', 'secret']:
                 html_parts.append(f'<span class="badge bg-secondary me-1">{field}: ********</span>')
                 continue

            if isinstance(changes, dict) and 'old' in changes and 'new' in changes:
                old_val = changes['old']
                new_val = changes['new']
                
                # Truncate long values
                if old_val and len(str(old_val)) > 20: old_val = str(old_val)[:20] + "..."
                if new_val and len(str(new_val)) > 20: new_val = str(new_val)[:20] + "..."
                
                if not old_val:
                    # Set
                    html_parts.append(f'<span class="badge bg-success me-1 text-white">{field}: {new_val}</span>')
                elif not new_val:
                    # Unset
                    html_parts.append(f'<span class="badge bg-danger me-1 text-white">{field}: {old_val} <i class="bi bi-x"></i></span>')
                else:
                    # Change
                    html_parts.append(f'<span class="badge bg-light text-dark border me-1">{field}: <span class="text-secondary">{old_val}</span> <i class="bi bi-arrow-right mx-1"></i> <strong>{new_val}</strong></span>')
            else:
                # Generic key-value
                html_parts.append(f'<span class="badge bg-secondary me-1">{field}: {changes}</span>')

    return "".join(html_parts)
