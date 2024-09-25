from django import forms
from .models import *

class Addnotificationform(forms.ModelForm):
    class Meta:
        model= notifications
        fields=['notification','notificationdate']

class Updatenotificationform(forms.ModelForm):
    class Meta:
        model=notifications
        fields=['notification','notificationdate']