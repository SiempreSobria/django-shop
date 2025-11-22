// script base.html

document.addEventListener('DOMContentLoaded', function() {
    console.log('Cart script initialized');
    
    function initializeCartHandlers() {
        const addToCartButtons = document.querySelectorAll('.add-to-cart');
        addToCartButtons.forEach(button => {
            button.removeEventListener('click', handleAddToCart);
            button.addEventListener('click', handleAddToCart);
        });

        const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
        removeFromCartButtons.forEach(button => {
            button.removeEventListener('click', handleRemoveFromCart);
            button.addEventListener('click', handleRemoveFromCart);
        });
    }

    function handleAddToCart(e) {
        e.preventDefault();
        const productId = this.dataset.productId;
        const url = this.dataset.url || `/cart/add/${productId}/`;
        addToCart(productId, url, this);
    }

    function handleRemoveFromCart(e) {
        e.preventDefault();
        const productId = this.dataset.productId;
        const url = this.dataset.url || `/cart/remove/${productId}/`;
        removeFromCart(productId, url, this);
    }

    initializeCartHandlers();

    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                initializeCartHandlers();
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

function addToCart(productId, url, button) {
    const originalText = button.innerHTML;
    const originalDisabled = button.disabled;
    
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Добавляем...';
    button.disabled = true;
    
    const formData = new FormData();
    const csrfToken = getCSRFToken();
    if (csrfToken) {
        formData.append('csrfmiddlewaretoken', csrfToken);
    }
    
    fetch(url, {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCounter(data.cart_total_items);
            showNotification(data.message, 'success');
        }
    })
    .catch(() => showNotification('Ошибка при добавлении в корзину', 'error'))
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = originalDisabled;
    });
}

function removeFromCart(productId, url, button) {
    const originalText = button.innerHTML;
    const originalDisabled = button.disabled;
    
    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    button.disabled = true;
    
    const formData = new FormData();
    const csrfToken = getCSRFToken();
    if (csrfToken) {
        formData.append('csrfmiddlewaretoken', csrfToken);
    }
    
    fetch(url, {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        updateCartCounter(data.cart_total_items);
        const cartItem = document.getElementById(`cart-item-${productId}`);
        if (cartItem) cartItem.remove();
        updateCartTotals(data.cart_total_price, data.cart_total_items);
        if (data.cart_total_items === 0) location.reload();
    })
    .catch(() => showNotification('Ошибка при удалении товара', 'error'))
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = originalDisabled;
    });
}

function updateCartCounter(count) {
    const cartCounter = document.getElementById('cart-counter');
    if (cartCounter) {
        cartCounter.textContent = count;
        cartCounter.classList.add('pulse');
        setTimeout(() => cartCounter.classList.remove('pulse'), 300);
    }
}

function updateCartTotals(totalPrice, totalQuantity) {
    const totalPriceElement = document.getElementById('cart-total-price');
    if (totalPriceElement) totalPriceElement.textContent = `${totalPrice} ₽`;
}

function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) return csrfInput.value;
    const cookie = document.cookie.split('; ').find(r => r.startsWith('csrftoken='));
    return cookie?.split('=')[1] || '';
}

function showNotification(message, type='info') {
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:1050;';
        document.body.appendChild(container);
    }
    
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} fade show`;
    notification.style.marginBottom = '10px';
    notification.innerHTML = message;
    container.appendChild(notification);
    setTimeout(() => notification.remove(), 4000);
}
