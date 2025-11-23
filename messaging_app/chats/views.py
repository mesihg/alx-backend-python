from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    filter_backends = [filters.OrderingFilter]

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
