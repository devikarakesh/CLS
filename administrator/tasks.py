from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_notification(booking_id):
    try:
        print("send email")
        # Import AuditoriumBooking here to avoid circular import
        from .models import Booking  
        
        booking = Booking.objects.get(id=booking_id)
        print("mmmmmmmm")
        send_mail(
            subject="Lab Booking Reminder",
            message=f"Reminder: Your lab booking is scheduled at {booking.time_slot.slot_start_time}.",
            from_email="no-reply@example.com",
            recipient_list=[booking.user.email],
            fail_silently=False,
        )
    except Booking.DoesNotExist:
        pass