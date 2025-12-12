/* api.js
   Simple API helpers and local cart storage.
   Update API_BASE to match your backend (e.g., http://localhost:8000/api)
*/
const API_BASE = 'http://localhost:8000/api'; // change to full URL if backend on different host, e.g. "http://localhost:8000/api"

async function apiFetch(path, opts = {}) {
  const headers = opts.headers || {};
  const token = getToken();
  if (token) headers['Authorization'] = 'Bearer ' + token;
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  opts.headers = headers;
  if (opts.body && typeof opts.body !== 'string') {
    opts.body = JSON.stringify(opts.body);
  }
  const res = await fetch(API_BASE + path, opts);
  if (!res.ok) {
    // try to parse error JSON
    const text = await res.text();
    let err = text;
    try { err = JSON.parse(text); } catch (e) { }
    throw new Error(err.message || res.statusText || text);
  }
  return res.json().catch(() => ({}));
}

/* Products */
async function apiGetProducts() {
  // Returns array of products. Fallback demo data when backend unavailable.
  try {
    return await apiFetch('/products', { method: 'GET' });
  } catch (err) {
    // demo fallback
    return [
      { id: 1, name: 'Banana (1kg)', price: 40, image: 'https://img.freepik.com/free-photo/background-sugar-cubes_93675-131274.jpg' },
      { id: 2, name: 'Tomato (1kg)', price: 60, image: 'https://via.placeholder.com/300x200?text=Tomato' },
      { id: 3, name: 'Milk (1L)', price: 45, image: 'https://via.placeholder.com/300x200?text=Milk' },
      { id: 4, name: 'Bread (loaf)', price: 35, image: 'https://via.placeholder.com/300x200?text=Bread' },
      { id: 5, name: 'Bread (loaf)', price: 35, image: 'https://via.placeholder.com/300x200?text=Bread' }
    ];
  }
}

/* Auth */
async function apiLogin(email, password) {
  return apiFetch('/login', { method: 'POST', body: { email, password } });
}
async function apiRegister(data) {
  return apiFetch('/register', { method: 'POST', body: data });
}
async function apiGetProfile() {
  return apiFetch('/users/me', { method: 'GET' });
}

/* Checkout */
async function apiCheckout(orderData) {
  return apiFetch('/checkout', { method: 'POST', body: orderData });
}

/* Helpers: token */
function saveToken(t) { localStorage.setItem('token', t); }
function getToken() { return localStorage.getItem('token'); }
function clearAuth() { localStorage.removeItem('token'); }

/* Cart helpers stored in localStorage under key 'grocery_cart' */
function getCartItems() {
  try {
    return JSON.parse(localStorage.getItem('grocery_cart') || '[]');
  } catch (e) { return []; }
}
function saveCart(items) {
  localStorage.setItem('grocery_cart', JSON.stringify(items));
}
function addToCart(product, qty = 1) {
  const items = getCartItems();
  const idx = items.findIndex(i => String(i.id) === String(product.id));
  if (idx >= 0) {
    items[idx].qty += qty;
  } else {
    items.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image_url: product.image_url,
      qty
    });
  }
  console.log("PRODUCT IMAGE:", product.image_url);
  saveCart(items);
}
function removeFromCart(productId) {
  const items = getCartItems().filter(i => String(i.id) !== String(productId));
  saveCart(items);
}
function updateCartQuantity(productId, qty) {
  const items = getCartItems().map(i => {
    if (String(i.id) === String(productId)) i.qty = qty;
    return i;
  });
  saveCart(items);
}
function clearCart() {
  localStorage.removeItem('grocery_cart');
}

function getCartTotal() {
  const items = getCartItems();
  return items.reduce((s, i) => s + (i.price || 0) * (i.qty || 0), 0);
}

function updateCartCountUI() {
  const count = getCartItems().reduce((s, i) => s + (i.qty || 0), 0);
  document.querySelectorAll('#cart-count').forEach(el => el.textContent = count);
}

// attach to window for pages to use
window.apiGetProducts = apiGetProducts;
window.apiCheckout = apiCheckout;
window.apiLogin = apiLogin;
window.apiRegister = apiRegister;
window.getCartItems = getCartItems;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateCartQuantity = updateCartQuantity;
window.clearCart = clearCart;
window.getCartTotal = getCartTotal;
window.saveToken = saveToken;
window.getToken = getToken;
window.clearAuth = clearAuth;
window.updateCartCountUI = updateCartCountUI;
