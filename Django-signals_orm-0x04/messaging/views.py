from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Message

def delete_user(request):
    """
    Delete user account and all its related data
    """
    user = request.user
    logout(request)
    user.delete()

def user_inbox(request):
    user = request.user
    inbox_messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).select_related(
        "sender",
        "receiver",
        "thread_root"
    ).distinct()

    return inbox_messages
   
 
