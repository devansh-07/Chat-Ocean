from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Chat, Message, Contact, User

def home(request):
    return render(request, 'core/index.html')

@login_required
def room(request, room_name=None):
    username = request.user.username
    user_contact = request.user.contacts.first()

    try:
        chats = Chat.objects.get(id=int(room_name))
    except:
        return render(request, 'core/room.html', {'username': username, 'user': user_contact, "friend": None})

    if user_contact in chats.members.all():
        friend = Chat.objects.get(id=int(room_name)).members.exclude(id=user_contact.id).first()

        return render(request, 'core/room.html', {'room_name': room_name, 'username': username, 'user': user_contact, "friend": friend})
    else:
        return render(request, 'core/room.html', {'room_name': room_name, 'username': username, 'user': user_contact, "friend": None})

def _searchContact(request):
    return render(request, "core/searchContact.html")

def _loadChats(request):
    user_contact = request.user.contacts.first()
    return render(request, "core/allChats.html", {'user': user_contact})

@csrf_exempt
def searchUser(request):
    username = request.POST['username']
    searched_user = User.objects.filter(username=username).exclude(username=request.user.username).first()

    if not searched_user:
        return render(request, 'core/searchUserResults.html', {"user": searched_user, "curr_user": request.user})

    searched_user_contact = searched_user.contacts.first()
    curr_user_contact = request.user.contacts.first()

    if searched_user_contact in curr_user_contact.contacts.all():
        for chat in curr_user_contact.chats.all():
            if searched_user_contact in chat.members.all():
                return render(request, 'core/searchUserResults.html', {"user": searched_user, "curr_user": request.user, "chat": chat, "areFriends": True})

    return render(request, 'core/searchUserResults.html', {"user": searched_user, "curr_user": request.user, "curr_user_contact": curr_user_contact})

@login_required
@csrf_exempt
def send_request(request):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(request.POST['username'])

    if not user_contact:
        return HttpResponse(status=404)

    curr_user_contact.sent_requests.add(user_contact)
    user_contact.received_requests.add(curr_user_contact)

    return HttpResponse(status=200)

@login_required
def load_requests(request):
    curr_user = request.user
    curr_user_contact = curr_user.contacts.first()

    return render(request, 'core/allRequests.html', {'sent_requests': curr_user_contact.sent_requests.all(), 'received_requests': curr_user_contact.received_requests.all()})

@login_required
@csrf_exempt
def removeSentRequest(request):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(request.POST['username'])

    if not user_contact:
        return HttpResponse(status=404)

    # Deleting request
    curr_user_contact.sent_requests.remove(user_contact)
    user_contact.received_requests.remove(curr_user_contact)

    return HttpResponse(status=200)

@login_required
@csrf_exempt
def removeReceivedRequest(request):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(request.POST['username'])

    if not user_contact:
        return HttpResponse(status=404)

    # Deleting requests
    curr_user_contact.received_requests.remove(user_contact)
    user_contact.sent_requests.remove(curr_user_contact)

    return HttpResponse(status=200)

@login_required
@csrf_exempt
def acceptReceivedRequest(request):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(request.POST['username'])

    if not user_contact:
        return HttpResponse(status=404)

    # Creating Empty chats
    curr_user_contact.received_requests.remove(user_contact)
    user_contact.sent_requests.remove(curr_user_contact)

    # Adding to contacts
    curr_user_contact.contacts.add(user_contact)

    for chats in curr_user_contact.chats.all():
        if user_contact in chats.members.all():
            return HttpResponse(status=200)

    newConnection = Chat.objects.create()
    newConnection.members.add(curr_user_contact)
    newConnection.members.add(user_contact)
    newConnection.save()

    return HttpResponse(status=200)

@login_required
def clearMessages(request, username):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(username)

    for chats in curr_user_contact.chats.all():
        if user_contact in chats.members.all():
            chats.delete()
            break

    return HttpResponse(status=200)

@login_required
def deleteContact(request, username):
    curr_user_contact = getUserContact(request.user.username)
    user_contact = getUserContact(username)

    for chats in curr_user_contact.chats.all():
        if user_contact in chats.members.all():
            for msg in chats.messages.all():
                msg.delete()

            chats.delete()
            break

    curr_user_contact.contacts.remove(user_contact)

    return redirect('home')

def getUserContact(username):
    user = User.objects.filter(username=username.strip()).first()
    if not user:
        return

    user_contact = user.contacts.first()
    return user_contact

@login_required
def deleteCurrUser(request):
    uname = request.user.username
    request.user.delete()

    messages.info(request, f'Account for {uname} deleted.')
    return redirect('home')
