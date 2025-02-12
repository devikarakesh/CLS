from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from loginapp.models import Userprofile
from django.conf import settings
import uuid

# Create your models here.
class notifications(models.Model):
    notification=models.CharField(max_length=200,null=True,blank=True)
    notificationdate=models.CharField(max_length=100,null=True,blank=True)

class Faculty1(models.Model):
    loginid=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    department=models.CharField(max_length=100,null=True,blank=True)
    def _str_(self):
        return self.name

class Subject1(models.Model):
    name = models.CharField(max_length=100)
    contact_hours = models.IntegerField()
    faculty = models.ForeignKey(Faculty1, on_delete=models.CASCADE)
    def _str_(self):
        return self.name

class Class1(models.Model):
    Semester = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject1)

@receiver(post_delete, sender=Subject1)
def delete_classes_with_subject(sender, instance, **kwargs):
    for class_instance in Class1.objects.filter(subjects=instance):
        class_instance.delete()
class TimetableEntry1(models.Model):
    day = models.CharField(max_length=10)
    period = models.IntegerField()
    cls = models.ForeignKey(Class1, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject1, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty1, on_delete=models.CASCADE)

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .tasks import send_email_notification
from datetime import timedelta,datetime
from django.utils.timezone import now,make_aware
from django.core.mail import send_mail
from .tasks import *


# Lab Model
class Lab(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=200)

    def _str_(self):
        return self.name

# Model for defining working days and slots
class WorkingDay(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)  # Example: 'Monday', 'Tuesday', etc.
    start_time = models.TimeField()  # Example: 09:00 AM
    end_time = models.TimeField()    # Example: 05:00 PM

    def _str_(self):
        return f"{self.day} - {self.start_time} to {self.end_time}"

# Time Slot model
class TimeSlot(models.Model):
    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    slot_start_time = models.TimeField()  # Example: 09:00 AM
    slot_end_time = models.TimeField()    # Example: 10:00 AM

    def _str_(self):
        return f"{self.slot_start_time} to {self.slot_end_time}"
import threading
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_aware
from datetime import datetime, timedelta


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email="no-reply@example.com",
            recipient_list=self.recipient_list,
            fail_silently=False,
        )
# Booking model for managing reservations
class Booking(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255, null=True, blank=True)  # Added field for purpose

    def _str_(self):
        return f"{self.lab.name} booked by {self.user.username} on {self.date} ({self.time_slot})"
@receiver(post_save, sender=Booking)
def schedule_email_notification(sender, instance, created, **kwargs):
    if created:
        try:
            print("Booking created. Preparing email notification...")

            slot_start_datetime = datetime.combine(instance.date, instance.time_slot.slot_start_time)
            slot_start_aware = make_aware(slot_start_datetime)

            # Send email 5 seconds before the booking time
            notification_time = slot_start_aware - timedelta(seconds=5)
            now_time = datetime.now()

            countdown = (notification_time - now_time).total_seconds()

            if countdown > 0:
                print(f"Scheduling email in {countdown} seconds...")

                def send_email():
                    EmailThread(
                        subject="Lab Booking Reminder",
                        message=f"Reminder: Your lab booking is scheduled at {instance.time_slot.slot_start_time}.",
                        recipient_list=[instance.user.email]
                    ).start()

                # Schedule email to be sent after `countdown` seconds
                threading.Timer(countdown, send_email).start()
            else:
                print("Notification time is in the past. Email will not be scheduled.")
        except Exception as e:
            print(f"Error scheduling email notification: {e}")
# @receiver(post_save, sender=Booking)
# def schedule_email_notification(sender, instance, created, **kwargs):
#     if created:
#         try:
#             # Ensure booking_time is timezone-aware
#             print("hhhhhh")
#             slot_start_datetime = datetime.combine(instance.date, instance.time_slot.slot_start_time)
#             slot_start_aware = make_aware(slot_start_datetime)
#             # Calculate the notification time (5 seconds before the slot st
#             notification_time = slot_start_aware - timedelta(seconds=5)

#             # # Ensure booking_time is timezone-aware
#             # notification_time = instance.booking_time - timedelta(hours=24)
#             now_time = now()

#             # Calculate countdown in seconds
#             countdown = (notification_time - now_time).total_seconds()

#             if countdown > 0:
#                 # Schedule the task using Celery
#                 send_email_notification.apply_async(
#                     (instance.id,), 
#                     countdown=countdown
#                 )
#                 print(f"Email notification scheduled in {countdown} seconds.")
#             else:
#                 print("Notification time is in the past. Email will not be scheduled.")
#         except Exception as e:
#             print(f"Error scheduling email notification: {e}")


# pip install celery django-celery-beat redis

# run redisserver
# redis-server
# run celery
# celery -A projectlabschedule worker --loglevel=info
# stop redis
# sudo systemctl stop redis
# redis status
# ps aux | grep redis
@receiver(post_save, sender=Booking)
def booking_cancelled_notification(sender, instance, **kwargs):
    # Send email for cancellation
    print("hhhhhh")
    subject = f'Booked: {instance.lab.name}'
    message = (f'Dear {instance.user.username},\n\n'
               f'Your booking for {instance.lab.name} on {instance.date} has been booked.\n\n'
               f'Best Regards,\nTeam')

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [instance.user.email],
        fail_silently=False,
    )

@receiver(post_delete, sender=Booking)
def booking_cancelled_notification(sender, instance, **kwargs):
    # Send email for cancellation
    print("hhhhhh")
    subject = f'Booking Cancelled: {instance.lab.name}'
    message = (f'Dear {instance.user.username},\n\n'
               f'Your booking for {instance.lab.name} on {instance.date} has been cancelled.\n\n'
               f'Best Regards,\nTeam')

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [instance.user.email],
        fail_silently=False,
    )


class Staffnotification(models.Model):
    notification=models.CharField(max_length=20)
    notificationdate=models.CharField(max_length=100)



class Staff(models.Model):
    
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    def _str_(self):
        return self.name

class Student(models.Model):
    loginid=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    semester=models.ForeignKey(Class1,on_delete=models.CASCADE,null=True,blank=True)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    def _str_(self):
        return self.name

class Labstaff(models.Model):
    loginid=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    lab=models.ForeignKey(Lab,on_delete=models.CASCADE,null=True,blank=True)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    def _str_(self):
        return self.name



