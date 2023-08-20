from django import forms

from . import models


class UserRegisterForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone', 'data-mask': '+0 (000) 000-00-00',
               'style': 'font-size: 13px; text-transform:capitalize'}))


class ReferralCode(forms.Form):
    referral_user = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder': 'Enter Code', 'style': 'font-size: 13px; text-transform:capitalize'}))


class ActivationCodeForm(forms.Form):
    activation_code = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder': 'Enter Code', 'style': 'font-size: 13px; text-transform:capitalize'}))


class ReferralCodeForm(forms.Form):
    referral_code = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder': 'Enter Code', 'style': 'font-size: 13px; text-transform:capitalize'}))
