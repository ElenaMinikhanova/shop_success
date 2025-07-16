from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Catalog
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse

class PostListView(ListView):
    model = Catalog
    template_name = 'base.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Catalog.objects.order_by('?')[:9]

class PostDetailView(DetailView):
    model = Catalog
    template_name = 'product.html'
    context_object_name = 'product'
