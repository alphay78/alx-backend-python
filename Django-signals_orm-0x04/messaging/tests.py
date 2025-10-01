# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="12345")
        self.receiver = User.objects.create_user(username="bob", password="12345")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertFalse(notification.is_read)
