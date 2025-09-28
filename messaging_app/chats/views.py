from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsMessageOwner  # ✅ custom permissions


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]
    permission_classes = [IsAuthenticated, IsParticipant]  # ✅ enforce ownership

    def get_queryset(self):
        # ✅ Only conversations the logged-in user is a participant of
        return Conversation.objects.filter(participants=self.request.user).prefetch_related(
            "participants", "messages"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]
    permission_classes = [IsAuthenticated, IsMessageOwner]  # ✅ enforce ownership

    def get_queryset(self):
        # ✅ Only messages in conversations the user is a participant of
        return Message.objects.filter(conversation__participants=self.request.user).select_related(
            "sender", "conversation"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
