from django.views.generic import ListView, DetailView, UpdateView, View, TemplateView
from .models import Product, UserLike
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
import json
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class PostListView(ListView):
    model = Product
    template_name = 'base.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        # Передать список liked ID для каждого пользователя
        user = self.request.user
        if user.is_authenticated:
            liked_ids = set(user.user_likes.values_list('like_id', flat=True))
        else:
            liked_ids = set()
        # добавляем атрибут к каждому продукту
        for product in qs:
            product.is_liked = product.id in liked_ids
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['like_count'] = user.user_likes.count()
            context['basket_count'] = user.user_products.count()
        else:
            context['like_count'] = 0
            context['basket_count'] = 0
        return context

class PostDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['like_count'] = user.user_likes.count()
            context['basket_count'] = user.user_products.count()
        else:
            context['like_count'] = 0
            context['basket_count'] = 0
        return context

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['like_count'] = user.user_likes.count()
            context['basket_count'] = user.user_products.count()
        else:
            context['like_count'] = 0
            context['basket_count'] = 0
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['like_count'] = user.user_likes.count()
            context['basket_count'] = user.user_products.count()
        else:
            context['like_count'] = 0
            context['basket_count'] = 0
        return context

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Обработка POST-запроса для переключения лайка
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)
        # Проверка, есть ли уже лайк этого пользователя для этого продукта
        user_like = UserLike.objects.filter(user=request.user, like=product).first()

        if user_like:
            # Если лайк есть — удаляем его (значит пользователь удаляет из избранного)
            user_like.delete()
            status = 'disliked'
        else:
            # Если лайка нет — создаем его (добавление в избранное)
            UserLike.objects.create(user=request.user, like=product)
            status = 'liked'

        # Возвращаем JSON-ответ с текущим статусом
        return JsonResponse({'status': status})

class AboutUs(TemplateView):
    template_name = 'about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['like_count'] = user.user_likes.count()
            context['basket_count'] = user.user_products.count()
        else:
            context['like_count'] = 0
            context['basket_count'] = 0
        return context

class ExitView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('view')  # укажите URL или имя маршрута для редиректа
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

