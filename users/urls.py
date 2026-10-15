from django.urls import path
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
] 