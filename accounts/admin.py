from django.contrib import admin
from .models import User, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email',)

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'otp_code', 'created_at', 'is_verified', 'attempts')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user_email',)
