from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from .models import Message

def delete_user(request):
    """
    Delete user account and all its related data
    """
    user = request.user
    try:
        with transaction.atomic():
            logout(request)
            user.delete()
    except Exception as e:
        return JsonResponse({"error": "An error occurred during account deletion."}, status=500)

def user_inbox(request):
    inbox_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        "sender",
        "receiver",
        "thread_root"
    ).distinct()

    return inbox_messages
   
def build_thread_tree(queryset):
    messages_by_id = {msg.id: msg for msg in queryset}
    tree = []
    for message in messages_by_id.values():
        message.replies_list = []
        if message.parent_message_id in messages_by_id:
            parent = messages_by_id[message.parent_message_id]
            parent.replies_list.append(message)
        elif message.is_thread_starter():
            tree.append(message)
    return tree

def serialize_message(message_list):
    serialized_list = []
    for message in message_list:
        data = {
            "id": message.id,
            "content": message.content,
            "timestamp": message.timestamp.isoformat() ,
            "is_edited": message.is_edited,
            "parent_message_id": message.parent_message_id,
            "thread_root_id": message.thread_root_id,
            "sender": {"id": message.sender.id, "username": message.sender.username},
            "receiver": {"id": message.receiver.id, "username": message.receiver.username},
            "replies": serialize_message(message.replies_list) 
        }
        serialized_list.append(data)
    return serialized_list

def message_thread(request, root_message_id):
    try:
        root_message = get_object_or_404(Message, pk=root_message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found"}, status=404)
    
    thread_queryset = Message.objects.filter(
        thread_root=root_message.thread_root or root_message
    ).select_related(
        "sender", "receiver", "parent_message"
    ).order_by("timestamp")
    thread_tree = build_thread_tree(thread_queryset)

    serialized_data = serialize_message(thread_tree)

    return JsonResponse(serialized_data, safe=False)
 
