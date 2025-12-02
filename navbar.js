document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Mobile Menu Logic
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isOpen = mobileMenu.classList.contains('open');
            if (isOpen) {
                mobileMenu.classList.remove('open');
                mobileMenuBtn.innerHTML = '<i data-lucide="menu" class="w-7 h-7"></i>';
            } else {
                mobileMenu.classList.add('open');
                mobileMenuBtn.innerHTML = '<i data-lucide="x" class="w-7 h-7"></i>';
            }
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        });
    }

    // QR Code Logic
    const phone = "469-625-1127";
    const normalizedPhone = phone.replace(/\D/g, '');
    const qrContainer = document.getElementById('qr-code-container');

    if (qrContainer) {
        // Clear previous content just in case
        qrContainer.innerHTML = '';

        if (typeof QRCode !== 'undefined') {
            const canvas = document.createElement('canvas');
            qrContainer.appendChild(canvas);

            QRCode.toCanvas(canvas, `tel:${normalizedPhone}`, {
                width: 120,
                margin: 1,
                color: { dark: '#FF3B30', light: '#141414' }
            }, function (error) {
                if (error) console.error("QR Code Error:", error);
            });
        } else {
            console.warn("QRCode library not loaded");
        }
    }

    // Prevent default click on desktop for call link
    const navCallLink = document.getElementById('nav-call-link');
    if (navCallLink) {
        navCallLink.addEventListener('click', function(e) {
            if (window.innerWidth > 1024) {
                e.preventDefault();
            }
        });
    }

    // Navbar Gradient Scroll Effect
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            const threshold = 100; // Pixel value to reach full opacity
            let opacity = Math.min(scrollY / threshold, 1);
            nav.style.setProperty('--nav-bg-opacity', opacity);
        });
    }
});
