from importlib.resources import path
from unittest.mock import patch
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('me/', views.RetrieveUserView.as_view()),
]

