from django.urls import path

from . import views
from django.urls import include, path
from .views import RoomView


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', RoomView.as_view(), name='room'),

]