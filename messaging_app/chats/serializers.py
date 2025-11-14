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
            "role"
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    message_body = serializers.CharField(required=True)

    def validate_message_body(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "conversation",
        ]
        read_only_fields = ["conversation", "sender"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message_preview = serializers.SerializerMethodField()

    messages = MessageSerializer(many=True, read_only=True)

    def get_last_message_preview(self, obj):
        last_message = obj.messages.all().first()

        if last_message:
            return last_message.message_body[:50] + ('...' if len(last_message.message_body) > 50 else '')
        return "No messages yet."

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants',
                  'created_at', 'last_message_preview', 'messages']
