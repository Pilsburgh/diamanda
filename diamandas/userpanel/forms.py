#!/usr/bin/python
# -*- coding: utf-8 -*-
# Diamanda Application Set
# User Panel

from diamandas.userpanel.models import *
from django import forms
from django.utils.translation import ugettext as _

from diamandas.recaptchawidget.fields import ReCaptchaField 

class RegisterForm(forms.Form):
        """
        Standard registration form
        """
        login = forms.CharField(min_length=3, max_length=30)
        password1 = forms.CharField(min_length=6, widget=forms.PasswordInput)
        password2 = forms.CharField(min_length=6, widget=forms.PasswordInput)
        email = forms.EmailField()
        recaptcha = ReCaptchaField()
        def clean(self):
                # check if passwords match
                if 'password2' in self.cleaned_data and 'password1' in self.cleaned_data and self.cleaned_data['password2'] != self.cleaned_data['password1'] :
                        raise forms.ValidationError(_("Passwords do not match."))
                # check if login is free
                try:
                        User.objects.get(username=self.cleaned_data['login'])
                except:
                        pass
                else:
                        raise forms.ValidationError(_("Login already taken"))
                # check if email isn't used already
                try:
                        User.objects.get(email=self.cleaned_data['email'])
                except:
                        pass
                else:
                        raise forms.ValidationError(_("Email already taken"))
                
                return self.cleaned_data


class EditUserData(forms.ModelForm):
        class Meta:
                model = User
                fields = ['email']


class AssignRPXForm(forms.Form):
        login = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput())
        password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
