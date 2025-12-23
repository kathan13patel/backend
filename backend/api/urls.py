from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('users/', views.get_all_users, name='get_users'),
    path('users/count/', views.get_users_count, name='users_count'),
]