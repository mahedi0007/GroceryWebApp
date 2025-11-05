// cart.js
function renderCart() {
  const items = getCartItems();
  const container = document.getElementById('cart-items');
  if (!container) return;
  container.innerHTML = '';
  if (!items.length) {
    container.innerHTML = '<p>Your cart is empty. <a href="products.html">Shop now</a></p>';
    document.getElementById('cart-total').innerText = '₹0.00';
    return;
  }

  items.forEach(i => {
    const row = document.createElement('div');
    row.className = 'card';
    row.innerHTML = `
      <div style="display:flex;gap:12px;align-items:center">
        <img src="${i.image||'https://via.placeholder.com/120'}" style="width:100px;height:80px;object-fit:cover;border-radius:6px">
        <div style="flex:1">
          <h3>${i.name}</h3>
          <p>₹${(i.price||0).toFixed(2)} x 
            <input type="number" min="1" value="${i.qty}" data-id="${i.id}" style="width:70px" class="qty-input" />
          </p>
        </div>
        <div>
          <button class="btn" data-remove="${i.id}">Remove</button>
        </div>
      </div>
    `;
    container.appendChild(row);
  });

  // wire up quantity changes
  container.querySelectorAll('.qty-input').forEach(input => {
    input.addEventListener('change', (e) => {
      const id = e.target.dataset.id;
      let q = parseInt(e.target.value) || 1;
      updateCartQuantity(id, q);
      renderCart();
      updateCartCountUI();
    });
  });

  // remove buttons
  container.querySelectorAll('[data-remove]').forEach(b => {
    b.addEventListener('click', (ev) => {
      const id = ev.target.dataset.remove;
      removeFromCart(id);
      renderCart();
      updateCartCountUI();
    });
  });

  document.getElementById('cart-total').innerText = '₹' + getCartTotal().toFixed(2);
  document.getElementById('checkout-btn')?.addEventListener('click', () => {
    location.href = 'checkout.html';
  });
}

renderCart();
