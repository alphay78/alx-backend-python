from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification

User = get_user_model()


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Log message edits before saving.
    """
    if not instance.pk:
        return  # new message, no edit

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.edited_by
        )
        instance.edited = True


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Delete all messages, notifications, and histories for a user
    when the user account is deleted.
    """
    # Fetch all messages where user is sender or recipient
    messages = Message.objects.filter(sender=instance) | Message.objects.filter(recipient=instance)
    message_ids = list(messages.values_list('id', flat=True))  # store IDs before deletion

    # Delete messages
    messages.delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories related to these messages
    MessageHistory.objects.filter(message_id__in=message_ids).delete()
