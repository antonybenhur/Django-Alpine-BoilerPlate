from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import io
import base64

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return render(request, 'home.html')

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@login_required
def settings_view(request):
    user = request.user
    otp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    return render(request, 'account/settings.html', {'otp_device': otp_device})

@login_required
def otp_setup_view(request):
    user = request.user
    if request.method == 'POST':
        token = request.POST.get('token')
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if device and device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, 'Two-factor authentication enabled.')
            return redirect('settings')
        else:
            messages.error(request, 'Invalid token. Please try again.')
    
    # Create a new unconfirmed device if one doesn't exist
    device, created = TOTPDevice.objects.get_or_create(user=user, confirmed=False)
    
    # Generate QR code
    otp_url = device.config_url
    qr = qrcode.make(otp_url)
    stream = io.BytesIO()
    qr.save(stream, format='PNG')
    qr_image = base64.b64encode(stream.getvalue()).decode('utf-8')
    
    return render(request, 'account/otp_setup.html', {'qr_image': qr_image})

@login_required
def otp_disable_view(request):
    if request.method == 'POST':
        user = request.user
        TOTPDevice.objects.filter(user=user).delete()
        messages.success(request, 'Two-factor authentication disabled.')
    return redirect('settings')
