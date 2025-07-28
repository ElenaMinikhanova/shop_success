from django.db.models import Sum
from django.views.generic import ListView, DetailView, UpdateView, View, TemplateView
from django.views import View
from .models import Product, UserLike, UserProduct
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
import json
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

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
        product = self.object

        # Ваши текущие переменные
        if user.is_authenticated:
            user_product = user.user_products.filter(product=product).first()
            context['user_product_count'] = user_product.count if user_product else 0
            context['liked'] = user.user_likes.filter(like=product).exists()
            context['like_count'] = user.user_likes.count()
            context['basket'] = user.user_products.filter(product=product).exists()
            context['basket_count'] = user.user_products.count()
        else:
            context['basket'] = False
            context['liked'] = False
            context['like_count'] = 0
            context['basket_count'] = 0
            context['user_product_count'] = 0

        # Получение рекомендаций
        same_category_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:3]

        # Добавляем атрибут is_liked для рекомендаций
        recommendations = list(same_category_products)
        if user.is_authenticated:
            user_likes_qs = user.user_likes.filter(like__in=recommendations)
            user_likes_ids = set(user_likes_qs.values_list('like_id', flat=True))
            for prod in recommendations:
                prod.is_liked = prod.id in user_likes_ids
        else:
            for prod in recommendations:
                prod.is_liked = False

        context['recommendations'] = recommendations

        return context

class AddToBasketView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        user_product, created = UserProduct.objects.get_or_create(user=user, product=product)
        if not created:
            user_product.count += 1
            user_product.save()

        total_count = user.user_products.aggregate(total=Sum('count'))['total'] or 0

        return JsonResponse({'message': 'Добавлено', 'basket_count': total_count})

class UpdateBasketView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        user = request.user
        data = json.loads(request.body)
        delta = int(data.get('delta', 0))
        user_product, created = UserProduct.objects.get_or_create(user=user, product=product)

        user_product.count += delta

        if user_product.count <= 0:
            user_product.delete()
            current_count = 0
        else:
            user_product.save()
            current_count = user_product.count

        return JsonResponse({'basket_count': current_count})

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



class BasketView(LoginRequiredMixin, ListView):
    model = UserProduct
    template_name = 'basket.html'
    context_object_name = 'user_products'

    def get_queryset(self):
        user = self.request.user
        user_products_qs = user.user_products.select_related('product')
        liked_ids = set(user.user_likes.values_list('like_id', flat=True))
        for user_product in user_products_qs:
            user_product.product.is_liked = user_product.product.id in liked_ids
        return user_products_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['like_count'] = user.user_likes.count()
        context['basket_count'] = user.user_products.count()
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            product_id_str = data.get('product_id')
            delta = int(data.get('delta', 0))
            if not product_id_str:
                return JsonResponse({'error': 'No product_id provided'}, status=400)
            try:
                product_id = int(product_id_str)
            except ValueError:
                return JsonResponse({'error': 'Invalid product_id'}, status=400)

            product = Product.objects.filter(id=product_id).first()
            if not product:
                return JsonResponse({'error': 'Product not found'}, status=404)

            user_product, created = UserProduct.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'count': 0}
            )
            # Обновляем количество
            new_count = user_product.count + delta
            if new_count <= 0:
                user_product.delete()
            else:
                user_product.count = new_count
                user_product.save()

            discount_percentage = 0

            if product.stock:
                discount_percentage = product.stock.discount or 0

            new_count = max(0, user_product.count + delta)

            if new_count == 0:
                user_product.delete()
            else:
                user_product.count = new_count
                user_product.save()

            # Расчёт итоговой суммы
            original_price = float(product.price)
            discount_amount = original_price * (discount_percentage / 100)
            discounted_price = original_price - discount_amount
            total_price_value = round(discounted_price * new_count, 2)

            basket_count = request.user.user_products.count()

            return JsonResponse({
                'basket_count': basket_count,
                'product_count': new_count if new_count > 0 else 0,
                'total_price': total_price_value
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


