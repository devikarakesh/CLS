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

class Addworkingdayform(forms.ModelForm):
    class Meta:
        model=WorkingDay
        fields=['day','start_time','end_time']

class Addslotform(forms.ModelForm):
    class Meta:
        model=TimeSlot
        fields=['slot_start_time','slot_end_time']


class AddStudentform(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','address','email','semester','phone']

class UpdateStudentform(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name','address','email','semester','phone']



class AddLabstaffform(forms.ModelForm):
    class Meta:
        model=Staff
        fields=['name','address','email','phone']

class UpdateLabstaffform(forms.ModelForm):
    class Meta:
        model=Staff
        fields=['name','address','email','phone']

class Addnotificationbystaffform(forms.ModelForm):
    class Meta:
        model= Staffnotification
        fields=['notification','notificationdate']




        

