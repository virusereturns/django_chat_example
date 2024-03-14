from django.urls import path
from . import views


urlpatterns = [
    path('', views.RoomListView.as_view(), name='room_list'),
    path('room/<slug:slug>/', views.RoomDetailView.as_view(), name='room_detail'),
]

