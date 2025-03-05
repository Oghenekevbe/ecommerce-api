from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Cart
from .tasks import send_order_email
from django.conf import settings

@receiver(post_save, sender=Cart)
def send_status_update_email(sender, instance, **kwargs):
    """Send an email when order status is updated."""
    
    if 'status' in instance.__dict__:  # Check if status is present
        subject = f"Update on Your Order: {instance.order_number}"
        
        status_messages = {
            'pending': "Your order has been placed and is currently pending confirmation.",
            'confirmed': "Your order has been confirmed and is being processed.",
            'processing': "Your order is being prepared for shipment.",
            'shipped': "Great news! Your order has been shipped.",
            'delivered': "Your order has been successfully delivered.",
            'returned': "We've received your return request. Our team will process it soon.",
            'completed': "Your order has been completed. Thank you for shopping with us!",
            'canceled': "Your order has been canceled. If this was a mistake, please contact support."
        }

        message = f"Dear {instance.user.email},\n\n {instance.order_number} \n\n{status_messages.get(instance.status, 'Your order status has been updated.')}\n\nThank you for choosing us!"

        print('message = ', message)
        from_email = settings.EMAIL_HOST_USER 
        user_email = instance.user.email
        print('from and user email = ', from_email, user_email)

        send_order_email.delay(user_email, subject, from_email, message)
