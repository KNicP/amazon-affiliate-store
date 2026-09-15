// SmartTech & Deals Hub - Main Frontend Application

let storeConfig = {
  store_name: "SmartTech & Deals Hub",
  store_tag_id: "nick3003-21",
  amazon_domain: "amazon.in",
  currency_symbol: "₹"
};

let allProducts = [];
let activeCategory = "All";

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

async function initApp() {
  await loadConfig();
  await loadProducts();
  setupEventListeners();
  renderProducts();
}

async function loadConfig() {
  try {
    const res = await fetch('./config.json');
    if (res.ok) {
      storeConfig = await res.json();
    }
  } catch (err) {
    console.log("Using default storeConfig:", storeConfig);
  }
  
  // Display active Tag ID in header
  const tagEl = document.getElementById("activeTagBadge");
  if (tagEl) {
    tagEl.innerText = `Tag: ${storeConfig.store_tag_id}`;
  }
}

async function loadProducts() {
  try {
    const res = await fetch('./data/products.json');
    if (res.ok) {
      allProducts = await res.json();
    }
  } catch (err) {
    console.error("Error loading products:", err);
  }
}

function buildAffiliateUrl(asin) {
  return `https://www.${storeConfig.amazon_domain}/dp/${asin}?tag=${storeConfig.store_tag_id}&linkCode=osi&th=1&psc=1`;
}

function setupEventListeners() {
  // Category Filtering
  const catButtons = document.querySelectorAll(".cat-btn");
  catButtons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      catButtons.forEach(b => b.classList.remove("active"));
      e.target.classList.add("active");
      activeCategory = e.target.getAttribute("data-category");
      renderProducts();
    });
  });

  // Search Input
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      renderProducts();
    });
  }

  // Modal Close
  const closeModalBtn = document.getElementById("closeModalBtn");
  const modalOverlay = document.getElementById("modalOverlay");
  if (closeModalBtn && modalOverlay) {
    closeModalBtn.addEventListener("click", () => {
      modalOverlay.classList.remove("open");
    });
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove("open");
      }
    });
  }
}

function renderProducts() {
  const container = document.getElementById("productsGrid");
  const searchVal = (document.getElementById("searchInput")?.value || "").toLowerCase().trim();

  if (!container) return;

  const filtered = allProducts.filter(prod => {
    const matchesCat = (activeCategory === "All") || (prod.category === activeCategory);
    const matchesSearch = prod.title.toLowerCase().includes(searchVal) || 
                          prod.category.toLowerCase().includes(searchVal) ||
                          prod.summary.toLowerCase().includes(searchVal);
    return matchesCat && matchesSearch;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full text-center py-16">
        <div class="text-5xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-gray-700">No deals found</h3>
        <p class="text-gray-500">Try adjusting your search or category filter.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(product => {
    const affiliateUrl = buildAffiliateUrl(product.asin);
    const formattedPrice = `${storeConfig.currency_symbol}${product.price.toLocaleString()}`;
    const formattedOrigPrice = product.original_price ? `${storeConfig.currency_symbol}${product.original_price.toLocaleString()}` : '';

    return `
      <div class="product-card">
        <div class="product-image-container">
          ${product.badge ? `<span class="badge-tag">${product.badge}</span>` : ''}
          ${product.discount ? `<span class="discount-tag">${product.discount}</span>` : ''}
          <img src="${product.image}" alt="${product.title}" loading="lazy">
        </div>
        
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <div class="text-xs font-semibold text-amber-600 uppercase tracking-wider mb-1">${product.category}</div>
            <h3 class="font-bold text-gray-900 text-lg leading-snug mb-2 line-clamp-2">${product.title}</h3>
            
            <div class="flex items-center gap-2 mb-3">
              <div class="star-rating text-sm">
                ★ <span>${product.rating}</span>
              </div>
              <span class="text-xs text-gray-400">(${product.reviews_count} reviews)</span>
            </div>

            <p class="text-sm text-gray-600 mb-4 line-clamp-2">${product.summary}</p>
          </div>

          <div>
            <div class="flex items-baseline gap-2 mb-4">
              <span class="text-2xl font-extrabold text-gray-900">${formattedPrice}</span>
              ${formattedOrigPrice ? `<span class="text-sm text-gray-400 line-through">${formattedOrigPrice}</span>` : ''}
            </div>

            <div class="flex gap-2">
              <a href="${affiliateUrl}" target="_blank" rel="noopener sponsored" class="btn-amazon flex-1">
                <span>Check on Amazon</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
              <button onclick="openReviewModal('${product.id}')" class="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg text-sm transition" title="Quick Specs & Review">
                ℹ️
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function openReviewModal(productId) {
  const product = allProducts.find(p => p.id === productId);
  if (!product) return;

  const modalContent = document.getElementById("modalContent");
  const modalOverlay = document.getElementById("modalOverlay");
  const affiliateUrl = buildAffiliateUrl(product.asin);

  modalContent.innerHTML = `
    <div class="flex flex-col md:flex-row gap-6">
      <div class="w-full md:w-1/3 flex items-center justify-center p-4 bg-gray-50 rounded-xl">
        <img src="${product.image}" alt="${product.title}" class="max-h-64 object-contain">
      </div>
      <div class="w-full md:w-2/3">
        <span class="text-xs font-bold text-amber-600 uppercase">${product.category}</span>
        <h2 class="text-2xl font-extrabold text-gray-900 mb-2">${product.title}</h2>
        
        <div class="flex items-center gap-2 mb-4">
          <span class="text-amber-500 font-bold">★ ${product.rating}</span>
          <span class="text-gray-400 text-sm">(${product.reviews_count} ratings)</span>
          <span class="text-green-600 bg-green-50 px-2 py-0.5 rounded text-xs font-semibold">${product.discount || 'Available Now'}</span>
        </div>

        <p class="text-gray-600 text-sm mb-4 leading-relaxed">${product.summary}</p>

        <h4 class="font-bold text-gray-900 text-sm mb-2">Key Features:</h4>
        <ul class="list-disc list-inside text-sm text-gray-600 space-y-1 mb-4">
          ${product.features.map(f => `<li>${f}</li>`).join('')}
        </ul>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div class="bg-green-50 p-3 rounded-lg border border-green-200">
            <span class="font-bold text-green-800 text-xs block mb-1">👍 PROS</span>
            <ul class="text-xs text-green-900 space-y-1">
              ${product.pros.map(p => `<li>• ${p}</li>`).join('')}
            </ul>
          </div>
          <div class="bg-red-50 p-3 rounded-lg border border-red-200">
            <span class="font-bold text-red-800 text-xs block mb-1">👎 CONS</span>
            <ul class="text-xs text-red-900 space-y-1">
              ${product.cons.map(c => `<li>• ${c}</li>`).join('')}
            </ul>
          </div>
        </div>

        <div class="flex items-center justify-between border-t pt-4">
          <div>
            <span class="text-xs text-gray-400 block">Offer Price</span>
            <span class="text-2xl font-black text-gray-900">${storeConfig.currency_symbol}${product.price.toLocaleString()}</span>
          </div>
          <a href="${affiliateUrl}" target="_blank" rel="noopener sponsored" class="btn-amazon px-6 py-3 text-base">
            Buy on Amazon (${storeConfig.store_tag_id}) 🚀
          </a>
        </div>
      </div>
    </div>
  `;

  modalOverlay.classList.add("open");
}
