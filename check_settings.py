import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_otp.settings')
django.setup()

print(f"DEBUG: {settings.DEBUG}")
print(f"EMAIL_HOST: '{settings.EMAIL_HOST}'")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: '{settings.EMAIL_HOST_USER}'")
print(f"EMAIL_HOST_PASSWORD: '{settings.EMAIL_HOST_PASSWORD}'")
print(f"DEFAULT_FROM_EMAIL: '{settings.DEFAULT_FROM_EMAIL}'")
