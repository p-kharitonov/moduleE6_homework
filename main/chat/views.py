from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import viewsets
from .models import Room







def index(request):
    return render(request, 'chat/index.html')


class RoomView(DetailView):
    model = Room
    template_name = 'chat/room.html'
    context_object_name = 'room'
