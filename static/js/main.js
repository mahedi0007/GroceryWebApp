// main.js - common UI initialization
document.addEventListener('DOMContentLoaded', async () => {
  updateCartCountUI();

  // Show/hide login/profile nav
  const token = getToken();
  document.getElementById('nav-login')?.style && (document.getElementById('nav-login').style.display = token ? 'none' : 'inline');
  document.getElementById('nav-profile')?.style && (document.getElementById('nav-profile').style.display = token ? 'inline' : 'none');

  // on index.html, populate featured
  const featuredGrid = document.getElementById('featured-grid');
  if (featuredGrid) {
    const products = await apiGetProducts();
    featuredGrid.innerHTML = '';
    products.slice(0,5).forEach(p => {
      const d = document.createElement('div');
      d.className = 'card';
      d.innerHTML = `<img src="${p.image_url||'https://img.freepik.com/free-photo/background-sugar-cubes_93675-131274.jpg'}" alt="${p.name}">
        <h3>${p.name}</h3>
        <p class="price">₹${p.price.toFixed(2)}</p>
        <div class="card-actions">
          <button class="btn" onclick='addToCart(${JSON.stringify(p)},1); updateCartCountUI();'>Add</button>
        </div>`;
      featuredGrid.appendChild(d);
    });
  }

//products.html all products display
  const productGrid = document.getElementById('products-grid');
  if (productGrid) {
    const products = await apiGetProducts();
    productGrid.innerHTML = '';
    products.slice(0,25).forEach(p => {
      const d = document.createElement('div');
      d.className = 'card';
      d.innerHTML = `<img src="${p.image_url||'https://img.freepik.com/free-photo/background-sugar-cubes_93675-131274.jpg'}" alt="${p.name}">
        <h3>${p.name}</h3>
        <p class="price">₹${p.price.toFixed(2)}</p>
        <div class="card-actions">
          <button class="btn" onclick='addToCart(${JSON.stringify(p)},1); updateCartCountUI();'>Add</button>
        </div>`;
      productGrid.appendChild(d);
    });
  }



});