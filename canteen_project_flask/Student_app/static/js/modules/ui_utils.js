export function updateCartBadge(count) {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;

    badge.innerText = count;
    count > 0 ? badge.classList.remove('d-none') : badge.classList.add('d-none');

    // Visual Feedback: Scaling animation
    badge.style.transition = "transform 0.2s ease";
    badge.style.transform = "scale(1.3)";
    setTimeout(() => { badge.style.transform = "scale(1)"; }, 200);
}