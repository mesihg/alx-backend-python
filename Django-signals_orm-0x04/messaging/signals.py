from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        notification_type = 'reply' if instance.parent_message else 'message'
        if notification_type == 'reply':
            content = f"{instance.sender.username} replied to your message: {instance.content[:50]}..."
        else:
            content = f"{instance.sender.username} sent you a message: {instance.content[:50]}..."

        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_type=notification_type,
            content=content
        )
