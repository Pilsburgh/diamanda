#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
# add / edit posts and topics
from django.utils.translation import ugettext as _
from django import forms

from diamandas.myghtyboard.models import *
from diamandas.recaptchawidget.fields import ReCaptchaField 


class AddTopicForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea)
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	class Meta:
		model = Topic

class AddTopicWithCaptchaForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea)
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	recaptcha = ReCaptchaField()
	class Meta:
		model = Topic

class AddPostForm(forms.ModelForm):
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	class Meta:
		model = Post

class AddPostWithCaptchaForm(forms.ModelForm):
	nick = forms.CharField(required=False, initial=_('Anonymous'))
	recaptcha = ReCaptchaField()
	class Meta:
		model = Post
