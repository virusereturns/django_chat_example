from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Room


class RoomListView(ListView):
    # Making a CBV because why not at this point. We'll make other function views later.
    model = Room
    template_name = 'room_list.html'
    context_object_name = "chatrooms"  # Just demonstrating that you can change the context object name.


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'
    slug_field = "slug"

