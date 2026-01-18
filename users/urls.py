from django.urls import path
from .views import RegisterAPIView, UserMeAPIView, AdminOnlyAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('me/', UserMeAPIView.as_view(), name='user-me'),
    path('admin-only/', AdminOnlyAPIView.as_view(), name='admin-only'),
]