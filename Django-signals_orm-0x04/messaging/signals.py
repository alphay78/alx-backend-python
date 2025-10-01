from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits and save old content into MessageHistory
    whenever a Message is updated.
    """
    if not instance.pk:
        # If no primary key yet, it's a new message -> skip
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Only log if content has actually changed
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=instance.edited_by   
        )
        instance.edited = True
