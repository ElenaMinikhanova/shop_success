from django.views.generic import ListView, DetailView, UpdateView, View, TemplateView
from .models import Product, UserLike
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class PostListView(ListView):
    model = Product
    template_name = 'base.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            # Количество лайков этого пользователя
            context['like_count'] = user.user_likes.count()

            # Количество товаров в корзине этого пользователя
            context['basket_count'] = user.user_products.count()
        else:
            # Для не авторизованных можно оставить 0 или None
            context['like_count'] = 0
            context['basket_count'] = 0

        return context

class PostDetailView(DetailView):
    model = Product
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
            login(request, user)
            return redirect('view')  # или куда нужно
        return render(request, 'registration.html', {'form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
