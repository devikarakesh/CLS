from django.db import models

# Create your models here.
class notifications(models.Model):
    notification=models.CharField(max_length=200,null=True,blank=True)
    notificationdate=models.CharField(max_length=100,null=True,blank=True)

class Faculty1(models.Model):
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    def _str_(self):
        return self.name

class Subject1(models.Model):
    name = models.CharField(max_length=100)
    contact_hours = models.IntegerField()
    faculty = models.ForeignKey(Faculty1, on_delete=models.CASCADE)
    def _str_(self):
        return self.name

class Class1(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject1)

class TimetableEntry1(models.Model):
    day = models.CharField(max_length=10)
    period = models.IntegerField()
    cls = models.ForeignKey(Class1, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject1, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Faculty1, on_delete=models.CASCADE)