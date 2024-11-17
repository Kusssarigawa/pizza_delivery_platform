document.addEventListener('DOMContentLoaded', function () {
    const pickupOption = document.getElementById('pickupOption');
    const deliveryOption = document.getElementById('deliveryOption');
    const pickupSection = document.getElementById('pickupSection');
    const checkoutForm = document.getElementById('checkoutForm');
    const generalErrorContainer = document.getElementById('generalErrorContainer');
    const messageContainer = document.getElementById('messageContainer'); // Элемент для отображения сообщения
    
    const addressSection = document.getElementById('deliverySection');


    checkoutForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        let isValid = true;
        generalErrorContainer.innerHTML = ''; // Очищаем предыдущие ошибки

        // Проверка точки получения при выборе самовывоза
        if (pickupOption.checked) {
            const pickupLocation = document.querySelector('select[name="pickup_location"]');
            if (!pickupLocation.value || pickupLocation.value === "") {
                isValid = false;
                generalErrorContainer.innerHTML = '<div class="form-error">Пожалуйста, выберите точку получения.</div>';
            }
        }

        // Если форма валидна, отправляем данные
        if (isValid) {
            const formData = new FormData(checkoutForm); // Собираем данные формы
            const csrfToken = getCookie('csrftoken'); // Получаем CSRF-токен

            fetch(checkoutForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Очищаем предыдущее сообщение
                messageContainer.innerHTML = '';

                if (data.success) {
                    // Успех — показать сообщение
                    messageContainer.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                    // checkoutForm.reset(); // Очищаем форму
                    // toggleSections(); // Сбросим видимость
                    window.location.href = '../';
                    alert("Подтвердите отправку формы")
                    
                } else {
                    // Если есть ошибки, показать их пользователю
                    displayFormErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        }
    });
    // Отображаем/скрываем раздел самовывоза на основе выбора
    pickupOption.addEventListener('change', function () {
        if (pickupOption.checked) {
            pickupSection.style.display = 'block';
            addressSection.style.display = 'none';
        }
        // else{
        //     addressSection.style.display = 'block';
        //     pickupSection.style.display = 'none';
        // }
    });
    pickupOption.addEventListener('change', function () {
        if (pickupOption.checked) {
            pickupSection.style.display = 'block';
            addressSection.style.display = 'none';
        }
    });

    deliveryOption.addEventListener('change', function () {
        if (deliveryOption.checked) {
            addressSection.style.display = 'block';
            pickupSection.style.display = 'none';
        }
    });

    // Проверка формы перед отправкой


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

    function displayFormErrors(errors) {
        // Очищаем предыдущие ошибки
        generalErrorContainer.innerHTML = '';

        // Перебираем и отображаем ошибки
        for (const key in errors) {
            if (errors.hasOwnProperty(key)) {
                const errorMessage = errors[key];
                const errorDiv = document.createElement('div');
                errorDiv.className = 'form-error';
                errorDiv.textContent = errorMessage;
                generalErrorContainer.appendChild(errorDiv);
            }
        }
    }
     // Обработчики удаления товаров
     document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            removeCartItem(itemId);
        });
    });

    // Функция удаления товара
    function removeCartItem(itemId) {
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const itemElement = document.querySelector(`.cart-item button[data-id="${itemId}"]`).closest('.cart-item');
                itemElement.remove();
                document.getElementById('subtotal').textContent = `${data.cart_total.toFixed(2)} грн.`;
                document.getElementById('itemCount').textContent = data.cart_item_count;
                updateTotals();

                if (data.cart_item_count === 0) {
                    window.location.href = '/'; // Редирект на главную, если корзина пуста
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

    
