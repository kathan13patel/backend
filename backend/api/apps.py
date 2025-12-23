from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """Initialize database indexes when app is ready"""
        from .models import UserRegistration
        try:
            UserRegistration.create_indexes()
        except Exception as e:
            print(f"Note: Could not create indexes: {e}")
