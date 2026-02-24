import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_auth_otp.settings')
django.setup()

def test_connection():
    try:
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD[:2]}...{settings.EMAIL_HOST_PASSWORD[-2:]}")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        print("Attempting to send test email...")
        send_mail(
            "Test Subject",
            "This is a test message from Django.",
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER], # send to self
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
