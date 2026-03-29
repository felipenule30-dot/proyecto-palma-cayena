/* ============================================================
   PALMA CAYENA — JavaScript principal
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* --- Navbar scroll effect --- */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    const updateNavbar = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    };
    updateNavbar();
    window.addEventListener('scroll', updateNavbar, { passive: true });
  }

  /* --- Mobile menu --- */
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  const menuClose = document.querySelector('.mobile-menu-close');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  }
  if (menuClose && mobileMenu) {
    menuClose.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  }

  /* --- Fade-in al scroll --- */
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    fadeEls.forEach(el => observer.observe(el));
  }

  /* --- Product gallery (miniatura → principal) --- */
  const galleryMain = document.querySelector('.product-gallery-main img');
  const thumbs = document.querySelectorAll('.product-gallery-thumb');
  if (galleryMain && thumbs.length) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        const src = thumb.querySelector('img').src;
        galleryMain.src = src;
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      });
    });
  }

  /* --- Selector de variantes --- */
  const sizeOptions = document.querySelectorAll('.size-option');
  const colorOptions = document.querySelectorAll('.color-option');
  const variantInput = document.getElementById('id_variant_id');
  const stockMessage = document.getElementById('stock-message');
  const addToCartBtn = document.getElementById('add-to-cart-btn');

  let selectedSize = null;
  let selectedColor = null;

  sizeOptions.forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.classList.contains('out-of-stock')) return;
      sizeOptions.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      selectedSize = btn.dataset.sizeId;
      updateVariant();
    });
  });

  colorOptions.forEach(btn => {
    btn.addEventListener('click', () => {
      colorOptions.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      selectedColor = btn.dataset.colorId;
      updateVariant();
    });
  });

  function updateVariant() {
    const variantsData = window.PALMA_VARIANTS || [];
    const match = variantsData.find(v => {
      const sizeMatch = !selectedSize || String(v.size_id) === String(selectedSize);
      const colorMatch = !selectedColor || String(v.color_id) === String(selectedColor);
      return sizeMatch && colorMatch;
    });
    if (match && variantInput) {
      variantInput.value = match.id;
      if (stockMessage) {
        stockMessage.textContent = match.stock > 0
          ? (match.stock < 4 ? `¡Solo ${match.stock} disponibles!` : 'En stock')
          : 'Sin stock';
        stockMessage.style.color = match.stock > 0 ? '#27ae60' : '#e74c3c';
      }
      if (addToCartBtn) {
        addToCartBtn.disabled = match.stock === 0;
        addToCartBtn.textContent = match.stock === 0 ? 'Sin stock' : 'Agregar al carrito';
      }
    }
  }

  /* --- Agregar al carrito (AJAX) --- */
  const addToCartForm = document.getElementById('add-to-cart-form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(addToCartForm);
      try {
        const res = await fetch('/carrito/agregar/', {
          method: 'POST',
          body: data,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const json = await res.json();
        if (json.success) {
          updateCartBadge(json.cart_count);
          showNotification('¡Agregado al carrito!', 'success');
        }
      } catch (err) {
        console.error('Error al agregar al carrito:', err);
      }
    });
  }

  /* --- Cart quantity controls --- */
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const action = btn.dataset.action;
      const variantId = btn.dataset.variantId;
      const input = btn.closest('.qty-control').querySelector('.qty-input');
      let qty = parseInt(input.value);
      if (action === 'decrease') qty = Math.max(1, qty - 1);
      if (action === 'increase') qty += 1;
      input.value = qty;

      const formData = new FormData();
      formData.append('variant_id', variantId);
      formData.append('quantity', qty);
      formData.append('csrfmiddlewaretoken', getCsrf());

      const res = await fetch('/carrito/actualizar/', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      const data = await res.json();
      if (data.success) {
        updateCartBadge(data.cart_count);
        location.reload();
      }
    });
  });

  /* --- Remove from cart --- */
  document.querySelectorAll('.cart-remove-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const variantId = btn.dataset.variantId;
      const formData = new FormData();
      formData.append('variant_id', variantId);
      formData.append('csrfmiddlewaretoken', getCsrf());

      const res = await fetch('/carrito/eliminar/', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      const data = await res.json();
      if (data.success) {
        btn.closest('.cart-item').remove();
        updateCartBadge(data.cart_count);
      }
    });
  });

  /* --- Newsletter AJAX --- */
  document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      data.append('csrfmiddlewaretoken', getCsrf());
      try {
        const res = await fetch('/newsletter/suscribirse/', {
          method: 'POST',
          body: data,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const json = await res.json();
        if (json.success) {
          form.innerHTML = '<p class="text-cream" style="font-size:.9rem;opacity:.8;">¡Gracias! Te has suscrito exitosamente.</p>';
        }
      } catch(e) {}
    });
  });

  /* --- Shop filters (mobile toggle) --- */
  const filterToggle = document.querySelector('.filter-toggle');
  const sidebar = document.querySelector('.shop-sidebar');
  if (filterToggle && sidebar) {
    filterToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  /* --- FAQ accordion --- */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });

  /* --- Helpers --- */
  function getCsrf() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  }

  function updateCartBadge(count) {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    }
  }

  function showNotification(msg, type = 'success') {
    const notif = document.createElement('div');
    notif.className = `notification notification-${type}`;
    notif.textContent = msg;
    notif.style.cssText = `
      position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
      background: ${type === 'success' ? 'var(--color-brown)' : 'var(--color-crimson)'};
      color: var(--color-cream); padding: 1rem 1.75rem;
      border-radius: var(--radius-full); font-size: 0.88rem;
      box-shadow: var(--shadow-lg); opacity: 0;
      transition: opacity 0.3s ease, transform 0.3s ease;
      transform: translateY(10px);
    `;
    document.body.appendChild(notif);
    requestAnimationFrame(() => {
      notif.style.opacity = '1';
      notif.style.transform = 'translateY(0)';
    });
    setTimeout(() => {
      notif.style.opacity = '0';
      setTimeout(() => notif.remove(), 400);
    }, 3000);
  }

});
