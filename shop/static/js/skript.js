document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');
  const navMenu = document.querySelector('.nav-menu');
  const overlay = document.querySelector('.overlay');


  logo.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    overlay.classList.toggle('active');
  });

  // Закрытие меню при клике на затемненную область
  overlay.addEventListener('click', () => {
    navMenu.classList.remove('active');
    overlay.classList.remove('active');
  });

  // Закрытие меню при клике на ссылку в меню (опционально)
  const menuLinks = navMenu.querySelectorAll('a');
  menuLinks.forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('active');
      overlay.classList.remove('active');
    });
  });

});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-img').forEach(img => {
        img.addEventListener('click', () => {
            const productId = img.dataset.productId; // Получаем ID товара из data-атрибута
            // Отправляем POST-запрос на сервер
            fetch('/toggle-like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Передача CSRF-токена
                    'Content-Type': 'application/json', // Тип данных
                },
                body: JSON.stringify({product_id: productId}), // Передача ID продукта
            })
            .then(response => response.json()) // Обработка ответа как JSON
            .then(data => {
                // Меняем изображение в зависимости от статуса
                const timestamp = new Date().getTime();
                if (data.status === 'liked') {
                    img.src = likedImageUrl + '?t=' + timestamp;
                } else {
                    img.src = unlikedImageUrl + '?t=' + timestamp;
                }
                location.reload(); // перезагружает страницу
            });
        });
    });
});

// Функция для получения CSRF-токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i=0; i<cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length+1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}

// Обеспечим выполнение скрипта после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const profileLink = document.querySelector('.profile-link');

    if (profileLink) {
        const menu = profileLink.querySelector('.burger-menu');

        profileLink.addEventListener('mouseenter', function() {
            if (menu) {
                menu.style.display = 'block';
            }
        });
        profileLink.addEventListener('mouseleave', function() {
            if (menu) {
                menu.style.display = 'none';
            }
        });
    }
});