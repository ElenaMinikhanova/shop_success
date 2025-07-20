from django.views.generic import ListView, DetailView, UpdateView, View, TemplateView
from .models import Catalog
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
from django.urls import reverse
from django.shortcuts import render, redirect
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


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('view')  # или куда нужно
        return render(request, 'registration.html', {'form': form})