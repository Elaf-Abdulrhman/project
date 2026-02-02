from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    sender_deleted = models.BooleanField(default=False)
    recipient_deleted = models.BooleanField(default=False)

    def soft_delete(self, user):
        if user == self.sender:
            self.sender_deleted = True
        elif user == self.recipient:
            self.recipient_deleted = True
        self.save()