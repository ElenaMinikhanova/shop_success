from django.urls import path
from django.views.generic import TemplateView
from .views import PostListView, PostDetailView, RegisterView

urlpatterns = [
    path('', PostListView.as_view(), name='view'),
    path('product/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('about_us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('register/', RegisterView.as_view(), name='register'),
]