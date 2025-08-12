from django.urls import path
from .views import UserRegistrationView, UserLoginView, ChatAPIView, TokenBalanceAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('chat/', ChatAPIView.as_view(), name='chat'),
    path('tokens/', TokenBalanceAPIView.as_view(), name='tokens'),
]
