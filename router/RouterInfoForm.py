from django import forms
from router.models import RouterAd
from parsley.decorators import parsleyfy

@parsleyfy
class RouterInfo(forms.Form):
    host_name=forms.CharField(max_length=32)
    host_ip=forms.CharField(max_length=32)
    user_name=forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

@parsleyfy
class ip_lookup(forms.Form):
    ip_field=forms.CharField(max_length=32)
    mask_field=forms.CharField(max_length=32)
