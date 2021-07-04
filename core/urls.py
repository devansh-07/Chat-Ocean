from django.urls import path
from . import views

urlpatterns = [
    path('', views.room, name='home'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('_searchContact', views._searchContact, name='searchContact'),
    path('_loadChats', views._loadChats, name='loadChats'),
    path('searchUser', views.searchUser, name='searchUser'),
    path('sendRequest', views.send_request, name='sendRequest'),
    path('loadRequests', views.load_requests, name='loadRequests'),
    path('removeSentRequest', views.removeSentRequest, name='removeSentRequest'),
    path('removeReceivedRequest', views.removeReceivedRequest, name='removeReceivedRequest'),
    path('acceptReceivedRequest', views.acceptReceivedRequest, name='acceptReceivedRequest'),
    path('deleteCurrUser', views.deleteCurrUser, name='deleteCurrUser'),
    path('deleteContact/<str:username>', views.deleteContact, name='deleteContact'),
]
