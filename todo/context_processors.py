# todo/context_processors.py
from .models import Version

def version_context(request):
    try:
        # Order by release_date and version_number (if applicable)
        latest_version = Version.objects.order_by('-release_date', '-version_number').first()
    except Version.DoesNotExist:
        latest_version = None
    return {
        'latest_version': latest_version
    }
