from django.urls import path
from .views import CustomLogoutView, manage_user, user_list, login_user, logoutview

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logoutview, name='logout'),
    path('register/', manage_user, name='register_user'),
    path('users/', user_list, name='user_list'),
]
