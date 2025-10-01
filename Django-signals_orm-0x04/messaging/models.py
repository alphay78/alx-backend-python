from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageHistory(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id}"


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Only unread messages for this user, optimized with only()
        return self.filter(recipient=user, read=False).only('id', 'sender', 'content', 'created_at')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager for unread messages

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"
