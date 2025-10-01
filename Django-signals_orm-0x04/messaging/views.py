from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from messaging.models import Message


@cache_page(60)  # cache the view for 60 seconds
def conversation_list(request):
    user = request.user
    messages = Message.objects.filter(recipient=user).select_related('sender')
    return render(request, 'chats/conversation_list.html', {'messages': messages})


def get_threaded_conversation(message_id):
    """
    Fetch a message and all its replies recursively in a threaded format.
    """
    root_message = get_object_or_404(Message.objects.select_related('sender', 'recipient'), pk=message_id)

    # Prefetch replies
    root_message = Message.objects.prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
    ).get(pk=message_id)

    def fetch_replies(msg):
        return {
            "id": msg.id,
            "sender": msg.sender.username,
            "recipient": msg.recipient.username,
            "content": msg.content,
            "replies": [fetch_replies(reply) for reply in msg.replies.all()]
        }

    return fetch_replies(root_message)
