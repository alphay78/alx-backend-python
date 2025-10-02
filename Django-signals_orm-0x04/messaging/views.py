from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Q
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def user_inbox(request):
    """
    Fetch all root messages for the logged-in user (sent or received)
    and prefetch their replies efficiently.
    """
    user = request.user  # logged-in user

    # Prefetch replies for all messages (with sender & recipient)
    replies_prefetch = Prefetch(
        'replies',
        queryset=Message.objects.select_related('sender', 'recipient')
    )

    # Root messages sent or received by this user
    messages = (
        Message.objects.filter(
            Q(sender=user) | Q(recipient=user),  # include both sender & recipient
            parent_message__isnull=True  # only root messages
        )
        .select_related('sender', 'recipient')
        .prefetch_related(replies_prefetch)
        .order_by('-created_at')
    )

    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def threaded_conversation(request, message_id):
    """
    Fetch a root message and all its replies recursively in a threaded format.
    Ensures that only messages belonging to the logged-in user are accessible.
    """
    user = request.user

    # Build base queryset with select_related & prefetch
    queryset = (
        Message.objects
        .select_related('sender', 'recipient')
        .prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'recipient')
            )
        )
        .filter(Q(sender=user) | Q(recipient=user))  # filter applied here
    )

    # Now safely fetch the root message
    root_message = get_object_or_404(queryset, pk=message_id)

    # Recursive helper to build nested conversation dict
    def fetch_replies(msg):
        return {
            "id": msg.id,
            "sender": msg.sender.username,
            "recipient": msg.recipient.username,
            "content": msg.content,
            "replies": [fetch_replies(reply) for reply in msg.replies.all()]
        }

    conversation_data = fetch_replies(root_message)

    return render(
        request,
        'messaging/threaded_conversation.html',
        {'conversation': conversation_data}
    )
