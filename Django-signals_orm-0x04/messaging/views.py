from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Q
from django.contrib.auth.decorators import login_required
from messaging.models import Message

@login_required
def user_inbox(request):
    """
    Fetch all messages sent to the logged-in user along with threaded replies,
    optimized using select_related and prefetch_related.
    """
    user = request.user

    # Prefetch replies for all messages sent to or from this user
    replies_prefetch = Prefetch(
        'replies',
        queryset=Message.objects.select_related('sender', 'recipient').all()
    )

    # Fetch all root messages for this user (either sent or received) with optimized queries
    messages = Message.objects.filter(
        Q(sender=user) | Q(recipient=user),
        parent_message__isnull=True  # Only root messages
    ).select_related('sender', 'recipient').prefetch_related(replies_prefetch).order_by('-created_at')

    context = {
        'messages': messages
    }
    return render(request, 'messaging/inbox.html', context)


def get_threaded_conversation(message_id):
    """
    Recursive fetch of a message and all replies in threaded format.
    Optimized with select_related + prefetch_related.
    """
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'recipient').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
        ),
        pk=message_id
    )

    def fetch_replies(msg):
        return {
            "id": msg.id,
            "sender": msg.sender.username,
            "recipient": msg.recipient.username,
            "content": msg.content,
            "replies": [fetch_replies(reply) for reply in msg.replies.all()]
        }

    return fetch_replies(root_message)
