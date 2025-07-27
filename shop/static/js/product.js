const images = document.querySelectorAll('.foto_product_dop');

images.forEach((img) => {
  img.addEventListener('click', () => {
    // Увеличиваем картинку
    img.classList.toggle('enlarged');

    // Если увеличилась — добавляем обработчик на весь документ
    if (img.classList.contains('enlarged')) {
      document.addEventListener('click', outsideClickListener);
    } else {
      document.removeEventListener('click', outsideClickListener);
    }

    // Функция для проверки клика вне картинки
    function outsideClickListener(e) {
      if (!img.contains(e.target)) {
        img.classList.remove('enlarged');
        document.removeEventListener('click', outsideClickListener);
      }
    }
  });
});


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
                if (count > 0) {
                    updateBasketDisplay(productId, count);
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

    function updateBasketDisplay(productId, count) {
        const quantityDiv = document.querySelector(`.quantity[data-product-id="${productId}"]`);
        if (quantityDiv) {
            quantityDiv.textContent = count;
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
});