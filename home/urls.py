from django.urls import path
from .views import index  # Import the index view

urlpatterns = [
    path('', index, name='index'),
]