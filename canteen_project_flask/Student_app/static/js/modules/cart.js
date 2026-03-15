import { updateCartBadge } from './ui_utils.js';

export function handleCartUpdate(itemId, action) {
    // Note: Ensure your modular routes (menu.add_to_cart) match the URL path
    const url = action === 'add' ? `/add_to_cart/${itemId}` : `/remove_from_cart/${itemId}`;

    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartBadge(data.cart_count);
                location.reload(); // Syncs Jinja2 session data
            }
        })
        .catch(err => console.error("Cart Error:", err));
}

export function placeOrder() {
    if (confirm("Confirm your order? This will finalize your tray.")) {
        window.location.href = "/place_order";
    }
}