from django.db import models

# Create your models here.
class notifications(models.Model):
    notification=models.CharField(max_length=200,null=True,blank=True)
    notificationdate=models.CharField(max_length=100,null=True,blank=True)