from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user, 
            read=False
        ).only(
            'id', 'sender_id', 'content', 'timestamp', 'parent_message_id', 'is_edited'
        ).select_related('sender', 'parent_message')