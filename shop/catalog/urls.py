from django.urls import path
from .views import PostListView, PostDetailView, ToggleLikeView, PostListFavorites

urlpatterns = [
    path('', PostListView.as_view(), name='view'),
    path('product/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('toggle-like/', ToggleLikeView.as_view(), name='toggle_like'),
    path('favorites/', PostListFavorites.as_view(), name='favorites'),
]