from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)   # track if edited
    edited_by = models.ForeignKey(                # track who edited
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages"
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(               # who made the edit
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_history"
    )

    def __str__(self):
        return f"History of {self.message.id} at {self.edited_at}"
