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

class Teacherform(forms.ModelForm):
    class Meta:
        model=Teacher1
        fields=['name','address','email','phone']


# class Subjectform(forms.ModelForm):
#     class Meta:
#         model=Subject1
#         fields=['name','contacthour','teacher']