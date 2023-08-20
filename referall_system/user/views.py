import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, ActivationCodeForm, ReferralCodeForm
from .models import Account, Referrals


def index(request):
    return render(request, 'index.html')


def register_phone(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = Account.objects.get(phone=form.cleaned_data.get('phone'))
                request.session['pk'] = user.pk
            except:
                request.session['phone'] = form.cleaned_data.get('phone')

            return redirect('user:verify')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})


def verify_code(request):
    code = 9214
    if request.method == 'POST':
        form = ActivationCodeForm(request.POST)
        if request.session.get('pk'):
            user = Account.objects.get(pk=request.session.get('pk'))
            if form.is_valid():
                num = form.cleaned_data.get('activation_code')
                if str(code) == str(num):
                    user = authenticate(phone=user.phone)
                    login(request, user)
                    return redirect('user:home')
        else:
            if form.is_valid():
                num = form.cleaned_data.get('activation_code')
                if str(code) == str(num):
                    user = Account.objects.create(phone=request.session['phone'])
                    user = authenticate(phone=user.phone)
                    user.is_active = True
                    login(request, user)
                    return redirect('user:home')

        return render(request, 'confirm_code.html', {'form': form})
    else:
        form = ActivationCodeForm()
        return render(request, 'confirm_code.html', {'form': form})


@login_required
def home(request):
    user = request.user
    recommendations = user.referral.all()
    try:
        referral = Referrals.objects.get(referrals=user)
        return render(request, 'home.html', {'rec': recommendations, 'referral': referral})
    except Referrals.DoesNotExist:
        pass

    if request.method == 'POST':
        code_form = ReferralCodeForm(request.POST)

        if code_form.is_valid():
            if not code_form.cleaned_data.get('referral_code') == user.referral_code:
                try:
                    user_ = Account.objects.get(referral_code=code_form.cleaned_data.get('referral_code'))
                    Referrals.objects.create(user_id=user_, referrals=user)
                    return redirect('user:home')
                except Account.DoesNotExist:
                    pass
    else:
        code_form = ReferralCodeForm()
        return render(request, 'home.html', {'form': code_form, 'rec': recommendations})

    return render(request, 'home.html', {'form': code_form, 'rec': recommendations})
