import { initAuthValidation, confirmLogout } from './modules/auth.js';
import { handleCartUpdate, placeOrder } from './modules/cart.js';

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Auth Poka-Yoke
    initAuthValidation();

    // Global Event Delegation for Cart Buttons
    document.body.addEventListener('click', (e) => {
        // Handle +/- buttons
        const container = e.target.closest('.cart-controls');
        if (container) {
            const itemId = container.getAttribute('data-item-id');
            let action = '';

            if (e.target.closest('.btn-increment') || e.target.closest('.btn-add-initial')) action = 'add';
            else if (e.target.closest('.btn-decrement')) action = 'remove';

            if (action) handleCartUpdate(itemId, action);
        }

        // Handle Place Order
        if (e.target.id === 'place-order-btn') {
            placeOrder();
        }
    });
});

// Attach to window for old-school HTML onclick events if needed
window.confirmLogout = confirmLogout;