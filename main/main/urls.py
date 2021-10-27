"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from chat.api import UserProfileDetailView
from chat.api import RoomListView
from chat.api import RoomCreateView
from chat.api import RoomView
# from chat.api import UserProfileListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path("api/profile/", UserProfileDetailView.as_view(), name="api_profile"),
    path("api/room/", RoomListView.as_view(), name="api_room"),
    path("api/room/<int:pk>", RoomView.as_view(), name="api_room"),
    path("api/room/create", RoomCreateView.as_view(), name="api_room"),

    path('chat/', include('chat.urls')),

]
