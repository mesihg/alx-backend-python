from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "conversation",
        ]
        read_only_fields = ["message_id", "sent_at", "sender"]


class ConversationSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]
