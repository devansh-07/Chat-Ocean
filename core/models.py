from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    contacts = models.ManyToManyField('self', blank=True)
    sent_requests = models.ManyToManyField('self', related_name="sent", blank=True, symmetrical=False)
    received_requests = models.ManyToManyField('self', related_name="received", blank=True, symmetrical=False)

class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

class Chat(models.Model):
    members = models.ManyToManyField(Contact, related_name="chats")
    messages = models.ManyToManyField(Message, blank=True)

    def last(self):
        return self.messages.all().last()

    def tail(n=10):
        return self.messages.objects.order_by("-timestamp").all()[:n][::-1]

    def __str__(self):
        return f"{self.pk}"
