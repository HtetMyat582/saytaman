"""
ASGI config for saytaman project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saytaman.settings')

# Initialize the ASGI application first
application = get_asgi_application()

# Safely provision a superuser if none exists
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Use environment variables, with secure defaults for your hobby app
    su_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'Admin')
    su_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'htetmyatmin582@gmail.com')
    su_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'hmm582zb')

    if not User.objects.filter(username=su_username).exists():
        User.objects.create_superuser(
            username=su_username,
            email=su_email,
            password=su_password
        )
        print(f"Superuser '{su_username}' created successfully via ASGI startup hook.")
except Exception as e:
    # Prevents crashing during early deployment/migration phases before tables are built
    print(f"Skipping automated superuser creation: {e}")