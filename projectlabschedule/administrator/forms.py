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

class Addfacultyform(forms.ModelForm):
    class Meta:
        model=Faculty1
        fields=['name','address','email','phone']


class Addsubjectform(forms.ModelForm):
    class Meta:
        model=Subject1
        fields=['name','contact_hours','faculty']

class Addclassform(forms.ModelForm):
    class Meta:
        model=Class1
        fields=['Semester','subjects']

class Updatefacultyform(forms.ModelForm):
    class Meta:
        model=Faculty1
        fields=['name','address','email','phone']

class Updatesubjectsform(forms.ModelForm):
    class Meta:
        model=Subject1
        fields=['name','contact_hours','faculty']

class Updateclassform(forms.ModelForm):
    class Meta:
        model=Class1
        fields=['Semester','subjects']