from django.urls import path
from django.views.generic import TemplateView
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='view'),
    path('product/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('favorites/', TemplateView.as_view(template_name='favorites.html'), name='favorites'),
]