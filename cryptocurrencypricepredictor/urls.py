from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.logout_user, name='logout_user'),
    path('predict', views.predict, name='predict'),
]
