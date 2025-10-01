from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory


class MessageSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="testpass")
        self.receiver = User.objects.create_user(username="bob", password="testpass")
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )

    def test_message_edit_creates_history(self):
        # Edit message
        self.message.content = "Hello Bob! How are you?"
        self.message.save()

        # Check if history is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Hello Bob!")
        self.assertTrue(self.message.edited)
