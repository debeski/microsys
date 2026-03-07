# Fundemental imports
import json
import os
import re
import sys
import platform
import urllib.request

import django
import psutil
from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncHour


# Dashboard View — Landing page with activity charts and dynamic branding
@login_required
def dashboard(request):
    """
    Dashboard/Landing page that reflects dynamic branding.
    """
    # Prepare Activity Chart Data
    UserActivityLog = apps.get_model('microsys', 'UserActivityLog')
    now = timezone.now()
    
    # 1. Last 24 Hours (Group by Hour)
    last_24h = now - timezone.timedelta(hours=24)
    activity_24h = UserActivityLog.objects.filter(created_at__gte=last_24h) \
        .annotate(hour=TruncHour('created_at')) \
        .values('hour') \
        .annotate(count=Count('id')) \
        .order_by('hour')
    
    data_24h_labels = [entry['hour'].strftime('%H:00') for entry in activity_24h]
    data_24h_values = [entry['count'] for entry in activity_24h]

    context = {
        'current_time': now,
        'chart_data': {
            'last_24h': json.dumps({'labels': data_24h_labels, 'values': data_24h_values}),
        }
    }
    return render(request, 'microsys/includes/dashboard.html', context)

# System Options — Displays accessibility settings, system info, and README specs
@login_required
def options_view(request):
    """
    View for system options, accessibility settings, and system info.
    Reads documented specs from README.md.
    """
    readme_path = os.path.join(settings.BASE_DIR, "README.md")
    readme_content = ""
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
        except:
            pass

    # Helper to pull version strings from README using regex capture groups
    def extract_spec(pattern):
        match = re.search(pattern, readme_content)
        return match.group(1).strip() if match else "N/A"

    # API Health Check (Targeting project's own API via loopback)
    api_reachable = False
    api_error = ""
    try:
        # Hit the loopback address to verify the API is responding inside the container
        api_url = "http://127.0.0.1:8000/api/decrees/" 
        
        req = urllib.request.Request(api_url)
        req.add_header("X-API-KEY", getattr(settings, "X_API_KEY", ""))
        req.add_header("X-SECRET-KEY", getattr(settings, "X_SECRET_KEY", ""))
        
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                api_reachable = True
            else:
                api_error = f"Status: {response.status}"
    except Exception as e:
        api_reachable = False
        api_error = str(e)

    # System Stats
    try:
        # RAM
        mem = psutil.virtual_memory()
        ram_total_gb = mem.total / (1024 ** 3)
        ram_used_gb = mem.used / (1024 ** 3)
        ram_percent = mem.percent
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_percent = disk.percent
    except Exception as e:
        ram_total_gb = ram_used_gb = ram_percent = 0
        disk_total_gb = disk_used_gb = disk_percent = 0

    context = {
        'current_time': timezone.now(),
        'os_info': f"{platform.system()} {platform.release()}",
        'python_version': sys.version.split()[0],
        'django_version': django.get_version(),
        'api_reachable': api_reachable,
        'api_error': api_error,
        'db_info': extract_spec(r'PostgreSQL ([\d.]+)'),
        'redis_info': extract_spec(r'Redis ([\d.]+)'),
        'celery_info': extract_spec(r'Celery ([\d.]+)'),
        'version': settings.VERSION,
        
        # System Stats
        'ram_total': f"{ram_total_gb:.1f}",
        'ram_used': f"{ram_used_gb:.1f}",
        'ram_percent': ram_percent,
        'disk_total': f"{disk_total_gb:.1f}",
        'disk_used': f"{disk_used_gb:.1f}",
        'disk_percent': disk_percent,
    }
    return render(request, 'microsys/includes/options.html', context)
