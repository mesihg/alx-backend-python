from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation, IsMessageOwnerOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsParticipantOfConversation,
        IsMessageOwnerOrReadOnly
    ]
    queryset = Message.objects.all()

    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied(
                "You are not a participant in this conversation",
                code=status.HTTP_403_FORBIDDEN,
            )
        queryset = Message.objects.filter(conversation=conversation)
        queryset = self.filter_queryset(queryset)

        return queryset.select_related("sender", "conversation").order_by("-sent_at")

    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save()
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsParticipantOfConversation]
    queryset = Conversation.objects.all()

    filter_backends = [filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        conversations = self.get_queryset()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )
