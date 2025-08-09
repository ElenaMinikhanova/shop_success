from django.db.models import Sum
from django.views.generic import ListView, DetailView, UpdateView, View, TemplateView
from django.views import View
from .models import Product, UserLike, UserProduct, Order, OrderHistory
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
import json
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
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

        # Получение профиля пользователя
        profile = getattr(user, 'profile', None)

        # Добавляем данные о пользователе в контекст
        context['user_name'] = user.first_name or ''
        context['user_email'] = user.email or ''
        context['user_phone'] = profile.phone_number if profile else ''
        context['like_count'] = user.user_likes.count()
        context['basket_count'] = user.user_products.count()

        # Расчет общей суммы скидки и итоговой суммы
        total_discount = 0
        total_price_for_all = 0
        total_price_for_all_orig = 0

        user_products_qs = user.user_products.select_related('product', 'product__stock')
        for up in user_products_qs:
            product = up.product
            count = up.count
            price = float(product.price)
            discount_percentage = 0

            if product.stock and product.stock.discount is not None:
                try:
                    discount_percentage = float(product.stock.discount)
                except (ValueError, TypeError):
                    discount_percentage = 0

            # Сумма скидки для этого товара
            discount_amount = price * (discount_percentage / 100) * count
            total_discount += discount_amount

            # Итоговая цена с учетом скидки для этого товара
            discounted_price = price - (price * (discount_percentage / 100))
            total_price_for_all += discounted_price * count

            total_price_for_all_orig += price * count

        # Округление, если нужно
        context['total_discount'] = round(total_discount, 2)
        context['total_price'] = round(total_price_for_all, 2)
        context['total_price_all'] = round(total_price_for_all_orig, 2)

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

            # Попытка получить существующий UserProduct
            user_product = UserProduct.objects.filter(user=request.user, product=product).first()

            if user_product:
                # Обновляем существующий товар
                new_count = user_product.count + delta
                if new_count <= 0:
                    user_product.delete()
                    new_count = 0
                else:
                    user_product.count = new_count
                    user_product.save()
            else:
                # Создаём новый, если delta > 0
                if delta > 0:
                    user_product = UserProduct.objects.create(
                        user=request.user,
                        product=product,
                        count=delta
                    )
                    new_count = delta
                else:
                    # Если delta отрицательный и товара нет, ничего не делаем
                    new_count = 0

            # Получение скидки
            discount_percentage = 0
            if product.stock and product.stock.discount is not None:
                try:
                    discount_percentage = float(product.stock.discount)
                except (ValueError, TypeError):
                    discount_percentage = 0

            original_price = float(product.price)
            discount_amount = original_price * (discount_percentage / 100)
            discounted_price = original_price - discount_amount
            total_price_value = round(discounted_price * new_count, 2)

            # Общее количество товаров в корзине
            basket_count = request.user.user_products.aggregate(total=Sum('count'))['total'] or 0

            return JsonResponse({
                'basket_count': basket_count,
                'product_count': new_count,
                'total_price': total_price_value
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class SubmitOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Получение данных из формы
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        comment = request.POST.get('comment', '')

        user = request.user

        # Собираем список товаров из корзины
        user_products = user.user_products.select_related('product')
        order_items = []
        total_order_price = 0

        for up in user_products:
            product = up.product
            count = up.count
            price = float(product.price)
            discount_percentage = 0
            if product.stock and product.stock.discount is not None:
                try:
                    discount_percentage = float(product.stock.discount)
                except (ValueError, TypeError):
                    discount_percentage = 0
            discounted_price = price - (price * (discount_percentage / 100))
            line_total = discounted_price * count
            total_order_price += line_total

            order_items.append(f"{product.name} x {count} - {line_total:.2f} ₽")

        # Создаем OrderHistory с статусом "processing"
        order_history = OrderHistory.objects.create(
            user=user,
            status='processing',
            date_order=timezone.now()
        )

        # Создаем Order для каждого продукта
        for up in user_products:
            product = up.product
            count = up.count
            price = product.price
            category_name = product.category.name if product.category else ''
            Order.objects.create(
                order_number=order_history,
                name_product=product.name,
                category_product=category_name,
                price_product=price,
                count_product=count
            )

        # Отправляем письмо
        message = f"""
        Новый заказ от {name}
        Контактная информация:
        Телефон: {phone}
        E-mail: {email}
        Комментарий: {comment}

        Заказанные товары:
        {'\n'.join(order_items)}

        Итоговая сумма: {total_order_price:.2f} ₽
        """

        send_mail(
            subject='Новый заказ',
            message=message,
            from_email='alena.minihanova@yandex.ru',  # замените на свой email
            recipient_list=['toxinka89@bk.ru'],  # адрес получателя
            fail_silently=False,
        )

        # Очищаем корзину
        user.user_products.all().delete()

        return redirect('basket')  # или другая страница


