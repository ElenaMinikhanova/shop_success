from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Catalog
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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

class ToggleLikeView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Catalog, pk=product_id)
        product.like = not product.like
        product.save()
        return JsonResponse({'like': product.like})

class PostListFavorites(ListView):
    model = Catalog
    template_name = 'favorites.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(like=True)