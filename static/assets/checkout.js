document.addEventListener('DOMContentLoaded', () => {

const cartTable = document.querySelector('tbody');
const orderSummary = document.querySelector('.bg-gray-950');

async function AddCartItem(slug) {
    try {
        const url = `/api/products/${slug}/cart/`;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error updating cart');
        }

        return true;
    } catch (error) {
        console.error('Cart update failed:', error);
        alert(error.message);
        return false;
    }
}

async function ReduceCartItem(slug) {
    try {
        const url = `/api/products/${slug}/cart/`;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error updating cart');
        }

        return true;
    } catch (error) {
        console.error('Cart update failed:', error);
        alert(error.message);
        return false;
    }
}function updateItemTotal(row) {
    const priceElements = row.querySelector('td:nth-child(2)').querySelectorAll('span');
    const quantityInput = row.querySelector('[data-input-counter]');
    const totalElement = row.querySelector('td:nth-child(4)');
    
    const quantity = parseInt(quantityInput.value);
    
    // First handle original price (first span)
    const originalPrice = parseFloat(priceElements[0].textContent.replace('$', ''));
    
    // Then handle discounted price (second span, if exists)
    const discountedPriceSpan = priceElements[1];
    const price = discountedPriceSpan 
        ? parseFloat(discountedPriceSpan.textContent.replace('$', '')) 
        : originalPrice;
    
    const total = (price * quantity).toFixed(2);
    
    totalElement.textContent = `$${total}`;
    
    calculateOrderTotal();
}

function calculateOrderTotal() {
    const rows = document.querySelectorAll('tbody tr');
    const discountCodePrice = parseFloat(document.querySelector('[data-discount-code]').textContent.replace('$', '')) * -1
    let totalOriginalPrice = 0;
    let totalDiscountedPrice = discountCodePrice * -1;
    
    rows.forEach(row => {
        const priceElements = row.querySelector('td:nth-child(2)').querySelectorAll('span');
        const quantity = parseInt(row.querySelector('[data-input-counter]').value);
        
        const originalPrice = parseFloat(priceElements[0].textContent.replace('$', ''));
        const discountedPriceSpan = priceElements[1];
        
        totalOriginalPrice += originalPrice * quantity;
        
        // If discounted price exists, use it, otherwise use original price
        const price = discountedPriceSpan 
            ? parseFloat(discountedPriceSpan.textContent.replace('$', '')) 
            : originalPrice;
        
        totalDiscountedPrice += price * quantity;
    });
    const discountAmount = totalOriginalPrice - totalDiscountedPrice - discountCodePrice;
    
    document.querySelector('[data-total]').textContent = `$${totalOriginalPrice.toFixed(2)}`;
    document.querySelector('[data-discount]').textContent = `-$${discountAmount.toFixed(2)}`;
    document.querySelector('[data-payable]').textContent = `$${totalDiscountedPrice.toFixed(2)}`;
}
cartTable.addEventListener('click', async (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    const row = button.closest('tr');
    const slug = row.dataset.productSlug;
    const input = row.querySelector(`#counter-input-${slug}`);
    let currentQuantity = parseInt(input.value);

    if (button.id === 'increment-button') {
        const success = await AddCartItem(slug);
    } 
    else if (button.id === 'decrement-button') {
        if (currentQuantity >= 1) {
            const success = await ReduceCartItem(slug);
        } 
        else if (currentQuantity === 0) {
            const success = await ReduceCartItem(slug);
            if (success) {
                row.remove();
                calculateOrderTotal();
            }
        }
    }

    document.querySelectorAll('tbody tr').forEach(updateItemTotal);
});
});
