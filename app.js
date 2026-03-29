document.addEventListener('DOMContentLoaded', () => {
  // === PASSWORD PROTECTION ===
  const passScreen = document.getElementById('password-screen');
  const passInput = document.getElementById('pass-input');
  const passBtn = document.getElementById('pass-btn');
  const authError = document.getElementById('auth-error');

  // Check if already authenticated in this session
  if (sessionStorage.getItem('authenticated') === 'true') {
      passScreen.classList.add('hidden');
      document.body.style.overflow = 'auto';
  } else {
      passInput.focus();
  }

  function checkPassword() {
      if (passInput.value === "349") {
          sessionStorage.setItem('authenticated', 'true');
          passScreen.classList.add('hidden');
          document.body.style.overflow = 'auto'; // Re-enable scrolling
      } else {
          authError.textContent = "Mã truy cập không hợp lệ. Vui lòng thử lại.";
          passInput.value = '';
          passInput.focus();
          
          // Shake effect
          const box = document.querySelector('.auth-box');
          box.style.transform = 'translateX(-10px)';
          setTimeout(() => box.style.transform = 'translateX(10px)', 100);
          setTimeout(() => box.style.transform = 'translateX(-10px)', 200);
          setTimeout(() => box.style.transform = 'translateX(0)', 300);
      }
  }

  passBtn.addEventListener('click', checkPassword);
  passInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') checkPassword();
  });

  // === TAB NAVIGATION ===
  const tabBtns = document.querySelectorAll('.nav-tabs button');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
          // Remove active class from all
          tabBtns.forEach(b => b.classList.remove('active'));
          tabContents.forEach(c => c.classList.remove('active'));

          // Add active class to clicked
          btn.classList.add('active');
          const targetId = btn.getAttribute('data-target');
          document.getElementById(targetId).classList.add('active');
      });
  });

  // === LIGHTBOX FUNCTIONALITY ===
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxClose = document.querySelector('.lightbox-close');
  const galleryItems = document.querySelectorAll('.gallery-item');

  galleryItems.forEach(item => {
      item.addEventListener('click', () => {
          const imgSrc = item.getAttribute('data-src');
          if (imgSrc) {
              lightboxImg.src = imgSrc;
              lightbox.classList.add('active');
          }
      });
  });

  function closeLightbox() {
      lightbox.classList.remove('active');
      // Delay removing source to keep transition smooth
      setTimeout(() => { lightboxImg.src = ''; }, 300);
  }

  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
          closeLightbox();
      }
  });
  
  // Create MRI Gallery dynamically
  renderGallery('mri-gallery', 'Don Thuoc/BV 108/Kham Dot Quy Dot 1_22.01.2026/MRI_', 12);
  // Create CT Gallery dynamically
  renderGallery('ct-gallery', 'Don Thuoc/BV 108/Kham Cap Cuu_12.02.2026/CT Scan_', 10);
});

// Function to dynamically generate image gallery
function renderGallery(containerId, basePath, count) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  let html = '';
  for (let i = 1; i <= count; i++) {
      const numStr = i.toString().padStart(2, '0');
      const imgSrc = `${basePath}${numStr}.jpg`;
      
      html += `
          <div class="gallery-item" data-src="${imgSrc}">
              <img src="${imgSrc}" alt="Scan ${numStr}" loading="lazy">
              <div class="gallery-overlay"><i class="fa-solid fa-magnifying-glass-plus"></i></div>
              <div class="item-label">Ảnh ${numStr}</div>
          </div>
      `;
  }
  container.innerHTML = html;
  
  // Re-attach lightbox listeners for new elements
  const newItems = container.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  
  newItems.forEach(item => {
      item.addEventListener('click', () => {
          lightboxImg.src = item.getAttribute('data-src');
          lightbox.classList.add('active');
      });
  });
}
