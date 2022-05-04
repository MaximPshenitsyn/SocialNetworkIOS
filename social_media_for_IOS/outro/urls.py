from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.log_out, name='log_out'),
    path('users/', views.users, name='users'),
    path('users/accept-user/<email>', views.accept_user, name='accept_user'),
    path('users/refuse-user/<email>', views.refuse_user, name='refuse_user'),
]
