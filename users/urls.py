from django.urls import path
from .views import signup, login

urlpatterns = [
    path('signup/', signup, name='register'),
    path('login/', login, name='login'),
]