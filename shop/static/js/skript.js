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

const likedImageUrl = '{% static "images/Vector1.png" %}';
const unlikedImageUrl = '{% static "images/Vector.png" %}';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-img').forEach(img => {
        img.addEventListener('click', () => {
            const productId = img.dataset.productId;
            fetch('/toggle-like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({product_id: productId}),
            })
            .then(response => response.json())
            .then(data => {
                const timestamp = new Date().getTime();
                if (data.status === 'liked') {
                    img.setAttribute('src', likedImageUrl + '?t=' + timestamp);
                } else {
                    img.setAttribute('src', unlikedImageUrl + '?t=' + timestamp);
                }
                location.reload(); // перезагружает страницу
            });
        });
    });
});

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