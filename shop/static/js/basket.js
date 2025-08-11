document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('orderForm');
    const submitBtn = document.getElementById('submitOrderBtn');

    if (submitBtn && form) {
        submitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // Очистка сообщений

            var nameInput = form.querySelector('input[name="name"]');
            var phoneInput = form.querySelector('input[name="phone"]');
            var emailInput = form.querySelector('input[name="email"]');
            var checkbox = form.querySelector('input[name="subscribe"]');

            var name = nameInput.value.trim();
            var phone = phoneInput.value.trim();
            var email = emailInput.value.trim();

            var valid = true;

            // Проверка имени
            document.getElementById('error-name').textContent = '';
            if (!name) {
                document.getElementById('error-name').textContent = 'Пожалуйста, введите ваше имя.';
                valid = false;
            }

            // Проверка телефона
            if (!phone) {
                document.getElementById('error-phone').textContent = 'Пожалуйста, введите ваш телефон.';
                valid = false;
            }

            // Проверка email
            if (!email) {
                document.getElementById('error-email').textContent = 'Пожалуйста, введите ваш email.';
                valid = false;
            } else {
                var emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
                if (!emailPattern.test(email)) {
                    document.getElementById('error-email').textContent = 'Пожалуйста, введите корректный email.';
                    valid = false;
                }
            }

            // Проверка галки
            if (!checkbox.checked) {
                alert('Пожалуйста, подтвердите согласие на обработку персональных данных.');
                valid = false;
            }

            if (valid) {
                form.submit();
            }
        });
    }
});



if (isAuthenticated) {
document.addEventListener('DOMContentLoaded', function() {
    // Обработка кнопки "В корзину"
    document.querySelectorAll('.basket_put_product').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            fetch(addToBasketUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({product_id: productId})
            })
            .then(response => response.json())
            .then(data => {
                updateBasketDisplay(productId, data.basket_count);
            });
        });
    });

    // Обработка кнопок "+" и "-"
    document.querySelectorAll('.increase, .decrease').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const url = `${updateBasketBaseUrl}${productId}/`; // формируем URL динамически
            const delta = this.classList.contains('increase') ? 1 : -1;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({product_id: productId, delta: delta})
            })
            .then(response => response.json())
            .then(data => {
                const count = data.basket_count;
                const totalPrice = data.total_price;
                if (count > 0) {
                    updateBasketDisplay(productId, count, totalPrice);
                } else {
                    removeBasketDisplay(productId);
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateBasketDisplay(productId, count, totalPrice) {
        const quantityDiv = document.querySelector(`.quantity[data-product-id="${productId}"]`);
        if (quantityDiv) {
            quantityDiv.textContent = count;
        }
        const priceDiv = document.querySelector('.price_total');
        if (priceDiv && totalPrice !== undefined) {
            priceDiv.textContent = totalPrice + ' ₽';
        }
        location.reload();
    }
    function removeBasketDisplay(productId) {
        const container = document.querySelector(`.basket-item[data-product-id="${productId}"]`);
        if (container) {
            container.remove();
        }
        // Перезагружаем страницу, чтобы обновить отображение
        location.reload();
    }
});}
document.querySelectorAll('.delete-item').forEach(deleteBtn => {
    deleteBtn.addEventListener('click', function() {
        const productId = this.dataset.productId;
        const url = `/basket/`; // URL для обновления корзины

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({product_id: productId, delta: -9999}) // очень большое число для удаления
        })
        .then(response => response.json())
        .then(data => {
            if (data.basket_count >= 0) {
                // Удаляем элемент из DOM
                const itemDiv = document.querySelector(`.basket-item[data-product-id="${productId}"]`);
                if (itemDiv) {
                    itemDiv.remove();
                }
                // Обновляем счетчики
                // Можно обновить счетчики или перезагрузить страницу
                location.reload();
            }
        });
    });
});