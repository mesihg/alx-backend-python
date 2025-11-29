from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    A Signal to trigger a notification when a new message instance is created.
    """
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
    """
    A Signal for logging message edits
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    edited_by=instance.sender,
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

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    A Signal for deleting user-related data
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
