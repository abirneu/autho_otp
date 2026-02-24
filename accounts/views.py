from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import UserRegistrationForm, ForgotPasswordForm, VerifyOTPForm, ResetPasswordForm
from .models import OTP
from django.contrib.auth.decorators import login_required
import random
import string

User = get_user_model()

def home(request):
    return render(request, 'accounts/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully. You can now login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_code = ''.join(random.choices(string.digits, k=6))
            
            # Delete old OTPs for this email
            OTP.objects.filter(user_email=email).delete()
            
            # Create new OTP
            OTP.objects.create(user_email=email, otp_code=otp_code)
            
            # Send Email
            subject = "Your Password Reset OTP"
            message = f"Your OTP for password reset is: {otp_code}. Valid for 5 minutes."
            try:
                from_email = 'abir60006@gmail.com'  # Hardcoded verified sender
                to_email = [email.strip()]
                
                print(f"DEBUG: Attempting send from '{from_email}' to '{to_email}'")
                
                send_mail(subject, message, from_email, to_email)
                request.session['reset_email'] = email
                messages.success(request, f"OTP sent to {email}")
                return redirect('verify_otp')
            except Exception as e:
                print(f"DEBUG: Email error: {str(e)}")
                messages.error(request, f"Error sending email: {str(e)}")
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['otp']
            otp_obj = OTP.objects.filter(user_email=email, otp_code=code).first()
            
            if otp_obj:
                if otp_obj.is_expired():
                    messages.error(request, "OTP has expired. Please request a new one.")
                elif otp_obj.attempts >= 5:
                    messages.error(request, "Too many failed attempts. Request a new OTP.")
                else:
                    otp_obj.is_verified = True
                    otp_obj.save()
                    request.session['otp_verified'] = True
                    return redirect('reset_password')
            else:
                # Increment attempts
                otp_obj = OTP.objects.filter(user_email=email).first()
                if otp_obj:
                    otp_obj.attempts += 1
                    otp_obj.save()
                messages.error(request, "Invalid OTP.")
    else:
        form = VerifyOTPForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email})

def resend_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
    
    otp_code = ''.join(random.choices(string.digits, k=6))
    OTP.objects.filter(user_email=email).delete()
    OTP.objects.create(user_email=email, otp_code=otp_code)
    
    send_mail("New OTP", f"Your new OTP is: {otp_code}", settings.DEFAULT_FROM_EMAIL, [email])
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect('verify_otp')

def reset_password(request):
    email = request.session.get('reset_email')
    verified = request.session.get('otp_verified')
    
    if not email or not verified:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=email)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            
            # Clean up
            OTP.objects.filter(user_email=email).delete()
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, "Password reset successful. You can now login.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
        
    return render(request, 'accounts/reset_password.html', {'form': form})
