from typing import Iterable
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'

    )
    thread_root = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='thread_messages'
    )

    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_edited = models.BooleanField(default=False)  

    class Meta:
        ordering = ['timestamp']
  

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:50]}..."
    
    
    def save(self, *args, **kwargs):
        if self.parent_message and not self.thread_root:
            self.thread_root = self.parent_message.thread_root or self.parent_message
        super().save(*args, **kwargs)

    def is_thread_starter(self):
        return self.parent_message is None
    
    def get_replies(self):
        return self.replies.select_related(
            "sender", "receiver"
        ).prefetch_related("replies")
    

    def get_threaded_message(self):
        return Message.objects.filter(
            thread_root=self.thread_root or self
        ).select_related("sender", "receiver")
    
    
class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_history',
    )
    edited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='editor'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-edited_at']
    def __str__(self):
        return f"Edit history for message {self.message} at {self.edited_at}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('reply', 'Message Reply'),
        ('edit', 'Message Edited'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    content = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='message'
    )

    is_read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'

    )
    created_at = models.DateTimeField(default=timezone.now)
    


    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"Notification for {self.user}"