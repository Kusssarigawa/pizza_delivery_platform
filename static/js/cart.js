document.addEventListener('DOMContentLoaded', function() {
    const sizeButtons = document.querySelectorAll('.size-btn');
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');


    sizeButtons.forEach(button => {
        button.addEventListener('click', updatePrice);
    });

    addToCartButtons.forEach(button => {
        button.addEventListener('click', addToCart);
    });

    function updatePrice(event) {
        const card = event.target.closest('.card');
        const priceElement = card.querySelector('.pizza-price');
        const basePrice = parseFloat(priceElement.dataset.basePrice);
        const extraCost = parseFloat(event.target.dataset.extraCost);
        const newPrice = basePrice + extraCost;
        priceElement.textContent = newPrice.toFixed(2);
        priceElement.dataset.currentPrice = newPrice.toFixed(2);

        card.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }

    function addToCart(event) {
        event.preventDefault();
        console.log('addToCart function called');
    
        const button = event.currentTarget;
        const card = button.closest('.card');
        const productId = button.dataset.productId;
        const productType = button.dataset.productType;
        const quantityElement = card.querySelector('.pizza-quantity');
        const quantity = parseInt(quantityElement.value) || 1;
        
        // Определяем размер в зависимости от типа продукта
        let size;
        let price;
        
        if (productType === 'burger') {
            // Для бургеров устанавливаем размер по умолчанию
            size = 'standard';
            const priceElement = card.querySelector('.pizza-price');
            price = parseFloat(priceElement.dataset.basePrice);
        } else {
            // Для остальных продуктов проверяем выбранный размер
            const sizeButton = card.querySelector('.size-btn.active');
            if (!sizeButton) {
                alert('Пожалуйста, выберите размер!');
                return;
            }
            size = sizeButton.dataset.size;
            const priceElement = card.querySelector('.pizza-price');
            price = parseFloat(priceElement.dataset.currentPrice) || parseFloat(priceElement.dataset.basePrice);
        }
    
        const data = {
            quantity: quantity,
            size: size,
            price: price
        };
    
        console.log('Sending data:', data);
    
        fetch(`/cart/add/${productId}/${productType}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })  
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartItemCount(data.cart_item_count);
                alert('Товар добавлен в корзину!');
            } else {
                alert('Ошибка при добавлении товара в корзину.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при добавлении товара в корзину.');
        });
    }
    function updateCartItemCount(count) {
        const cartItemCount = document.getElementById('cart-item-count');
        if (cartItemCount) {
            cartItemCount.textContent = count;
        }
    }

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

    document.getElementById('cartButton').addEventListener('click', function() {
        fetch('/cart/')
            .then(response => response.json())
            .then(data => {
                const modalBody = document.querySelector('#myModal .modal-body');
                modalBody.innerHTML = '';
                
                if (data.cart_items && data.cart_items.length > 0) {
                    const cartTable = document.createElement('table');
                    cartTable.className = 'table table-borderless';
                    
                    data.cart_items.forEach(item => {
                        const price = parseFloat(item.price) || 0;
                        const quantity = parseInt(item.quantity) || 0;
                        const totalPrice = price * quantity;
                        const priceDisplay = isNaN(price) ? '0.00' : price.toFixed(2);
                        const totalPriceDisplay = isNaN(totalPrice) ? '0.00' : totalPrice.toFixed(2);
                        
                        const row = cartTable.insertRow();
                        row.innerHTML = `
                            <td>
                                <img src="${item.image}" alt="${item.product_name}" width="50" height="50" class="rounded">
                            </td>
                            <td>
                                <strong class="text-danger">${item.product_name}</strong><br>
                                <small>Размер: ${item.size}см</small>
                            </td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-secondary btn-sm decrement" data-item-id="${item.id}">-</button>
                                    <span class="btn btn-outline-secondary btn-sm" disabled>${quantity}</span>
                                    <button type="button" class="btn btn-outline-secondary btn-sm increment" data-item-id="${item.id}">+</button>
                                </div>
                            </td>
                            <td class="text-right">
                                <div>Цена за шт</div>
                                <strong>${priceDisplay} грн.</strong>
                            </td>
                            <td class="text-right">
                                <div>Всего</div>
                                <strong>${totalPriceDisplay} грн.</strong>
                            </td>
                            <td>
                                <button type="button" class="btn btn-link text-danger remove-item" data-item-id="${item.id}">
                                   <img src="http://127.0.0.1:8000/static/images/trash_logo.jpg" alt="Remove" width="16" height="16">
                                </button>
                            </td>
                        `;
                    });
                    
                    modalBody.appendChild(cartTable);
                    
                    const cartTotal = parseFloat(data.cart_total) || 0;
                    const totalRow = document.createElement('div');
                    totalRow.className = 'text-right mt-3';
                    totalRow.innerHTML = `<h5>Итого: ${cartTotal.toFixed(2)} грн.</h5>`;
                    modalBody.appendChild(totalRow);
    
                    // Добавляем кнопку "Перейти к оформлению", если есть товары в корзине
                    const checkoutButtonWrapper = document.createElement('div');
                    checkoutButtonWrapper.className = 'checkout-btn-wrapper text-center mt-4';
                    checkoutButtonWrapper.innerHTML = `
                        <a href="/checkout/" class="btn btn-success" id="checkout-button">Перейти к оформлению</a>
                    `;
                    modalBody.appendChild(checkoutButtonWrapper);
    
                } else {
                    const emptyMessage = document.createElement('p');
                    emptyMessage.className = 'empty-cart-message';  // Класс для стилизации
                    emptyMessage.textContent = 'Ваша корзина пуста';
                    modalBody.appendChild(emptyMessage);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    });
    
    
    function updateCartTotal(total) {
        const totalElement = document.querySelector('#myModal .modal-body h5');
        if (totalElement) {
            totalElement.textContent = `Итого: ${total.toFixed(2)} грн.`;
        }
    }

    document.querySelector('#myModal .modal-body').addEventListener('click', function(event) {
        if (event.target.classList.contains('increment') || event.target.classList.contains('decrement')) {
            const itemId = event.target.dataset.itemId;
            const action = event.target.classList.contains('increment') ? 'increment' : 'decrement';
            updateCartItem(itemId, action);
        } else if (event.target.classList.contains('remove-item') || event.target.closest('.remove-item')) {
            const itemId = event.target.dataset.itemId || event.target.closest('.remove-item').dataset.itemId;
            removeCartItem(itemId);
        } else if (event.target.id === 'checkout-button') {
            window.location.href = '/checkout/';
        }
    });

    function updateCartItem(itemId, action) {
        const quantityElement = document.querySelector(`.decrement[data-item-id="${itemId}"]`).nextElementSibling;
        let currentQuantity = parseInt(quantityElement.textContent);
    
        if (action === 'increment') {
            currentQuantity++;
        } else if (action === 'decrement' && currentQuantity > 1) {
            currentQuantity--;
        }
    
        fetch(`/cart/update/${itemId}/${action}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                quantity: currentQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                quantityElement.textContent = currentQuantity;
                
                // Update the price display for this item
                const row = quantityElement.closest('tr');
                const priceElement = row.querySelector('td:nth-child(4) strong');
                const totalPriceElement = row.querySelector('td:nth-child(5) strong');
                
                const newPrice = parseFloat(data.item_price);
                const newTotalPrice = newPrice * currentQuantity;
                
                priceElement.textContent = `${newPrice.toFixed(2)} грн.`;
                totalPriceElement.textContent = `${newTotalPrice.toFixed(2)} грн.`;
                
                updateCartTotal(data.cart_total);
                updateCartItemCount(data.cart_item_count);
            } else {
                alert('Ошибка при обновлении товара.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }

    function removeCartItem(itemId) {
        const csrfToken = getCookie('csrftoken');
    
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const itemRow = document.querySelector(`[data-item-id="${itemId}"]`).closest('tr');
                if (itemRow) {
                    itemRow.remove();
                }
                
                updateCartTotal(data.cart_total);
                updateCartItemCount(data.cart_item_count);
                
                if (data.cart_item_count === 0) {
                    const modalBody = document.querySelector('#myModal .modal-body');
                    modalBody.innerHTML = '<p class="text-center">Ваша корзина пуста.</p>';
                }
            } else {
                alert('Не удалось удалить товар из корзины.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении товара.');
        });
    }
});