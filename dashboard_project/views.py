from django.http import JsonResponse
from django.conf import settings
from django.db import connection

def health_check(request):
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        db_status = "connected"
        db_engine = settings.DATABASES['default']['ENGINE']
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_engine = "unknown"
    
    return JsonResponse({
        "status": "ok",
        "debug": settings.DEBUG,
        "database": {
            "engine": db_engine,
            "status": db_status
        },
        "allowed_hosts": settings.ALLOWED_HOSTS,
    })
