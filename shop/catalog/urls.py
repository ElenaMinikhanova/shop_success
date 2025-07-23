from django.urls import path
from django.views.generic import TemplateView
from .views import PostListView, PostDetailView, RegisterView, ProfileView, ToggleLikeView, AboutUs
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', PostListView.as_view(), name='view'),
    path('product/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
    path('register/', RegisterView.as_view(), name='register'),
    path('exit/', LogoutView.as_view(), name='exit'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
]