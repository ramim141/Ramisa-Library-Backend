from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView, UserLogoutView


urlpatterns = [
    path('signup/',UserRegistrationView.as_view(),name='signup'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('profile/',UserProfileView.as_view(),name='profile'),
]