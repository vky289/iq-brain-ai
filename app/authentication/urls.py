from django.urls import path

from app.authentication.views.common_view import index
from app.authentication.views.api_views import login_view, register_user, profile_user
from django.contrib.auth.views import LogoutView

app_name = 'auth'
urlpatterns = [
    path(r'', index, name='home'),
    path(r'accounts/login/', login_view, name='login'),
    path(r'login/', login_view, name='login'),
    #path(r'register/', register_user, name='register'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    path(r'profile/', profile_user, name='profile'),
]
