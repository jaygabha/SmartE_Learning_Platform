from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PaymentForm
from django.contrib.auth.models import User

from .models import Membership, Student


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/dashboard/')  # Redirect to the dashboard or any desired page
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None
    return render(request, 'SmartE_app/login.html', {'error_message': error_message})

@login_required
def dashboard(request):
    return render(request, 'SmartE_app/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('SmartE_app:login')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            sid = form.cleaned_data['sid']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            membership_type = form.cleaned_data['membership_type']

            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.first_name = name
            user.save()

            return redirect('SmartE_app:payment')  # Redirect to a success page
    else:
        form = RegistrationForm()

    return render(request, 'SmartE_app/registration.html', {'form': form})
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            membership_type = form.cleaned_data['membership_type']
            name = form.cleaned_data['name']
            cardnumber = form.cleaned_data['cardnumber']
            expiry = form.cleaned_data['expiry']
            cvv = form.cleaned_data['cvv']

            # Additional logic to process payment or display price
            # Example:
            if True:
                # Process the payment and update the necessary records
                # ...

                price = Membership.objects.get(type=membership_type).price
                return render(request, 'SmartE_app/payment_success.html', {'price': price})


    else:
        form = PaymentForm()

    return render(request, 'SmartE_app/payment.html', {'form': form})