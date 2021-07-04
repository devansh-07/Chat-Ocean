from django import template
from core.models import Chat

register = template.Library()

@register.filter(name='name_of_member_except')
def exclude(contacts, contact):
    return contacts.exclude(id=contact.id).first().user.first_name

@register.filter(name='chats_with')
def exclude(user, friend):
    for chat in user.chats.all():
        if friend in chat.members.all():
            return chat.messages.all()
