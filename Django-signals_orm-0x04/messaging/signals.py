from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

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


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.is_edited = True

                if old_message.sender != instance.receiver:
                    Notification.objects.create(
                        user=old_message.receiver,
                        message=instance,
                        notification_type='edit',
                        content=f"{instance.sender.username} edited their message"
                    )

        except Message.DoesNotExist:
            pass
