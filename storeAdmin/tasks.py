from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_order_email(user_email, subject, from_email, message):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[user_email],
    )
    email.send(fail_silently=False)