document.addEventListener('DOMContentLoaded', () => {
    // --- AUTH LOGIN CHECK (Optional) ---
    // If we want to show "Dashboard" button instead of "Login" if user is already logged in
    const token = localStorage.getItem('access_token');
    const userGreeting = document.getElementById('user-greeting');
    const logoutBtn = document.getElementById('logout-btn');
    const navbarUser = document.querySelector('.nav-user');

    // Default state: Hide user specific elements if not logged in
    if (!token) {
        // No specific user elements to hide in new design
    } else {
        // User is logged in - Update all Login/Start buttons to proper Dashboard links
        const loginLinks = document.querySelectorAll('a[href="/login"]');
        loginLinks.forEach(link => {
            link.textContent = "Go To The Dashboard To Enhance You Picture";
            link.href = '/dashboard';
            link.classList.remove('btn-nav-cta'); // Optional styling adjustment
            link.classList.add('btn-nav-cta'); // Keep the primary style
        });

        // Also handle any old buttons if they exist
        const ctaButtons = document.querySelectorAll('button[onclick*="login"]');
        ctaButtons.forEach(btn => {
            btn.textContent = "Go To The Dashboard To Enhance You Picture";
            btn.onclick = () => window.location.href = '/dashboard';
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.reload();
        });
    }

    // --- COMPARISON SLIDER ---
    const connectionSlider = document.getElementById('comparison-slider');
    const beforeImage = document.querySelector('.comp-img-layer.before');
    const sliderHandle = document.querySelector('.slider-handle');

    if (connectionSlider && beforeImage && sliderHandle) {
        let isDragging = false;

        const updateSlider = (x) => {
            const rect = connectionSlider.getBoundingClientRect();
            let position = ((x - rect.left) / rect.width) * 100;

            // Clamp 0-100
            position = Math.max(0, Math.min(100, position));

            beforeImage.style.width = `${position}%`;
            sliderHandle.style.left = `${position}%`;
        };

        // Mouse Events
        sliderHandle.addEventListener('mousedown', () => isDragging = true);
        window.addEventListener('mouseup', () => isDragging = false);
        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            updateSlider(e.clientX);
        });

        // Touch Events
        sliderHandle.addEventListener('touchstart', () => isDragging = true);
        window.addEventListener('touchend', () => isDragging = false);
        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            updateSlider(e.touches[0].clientX);
        });

        // Click on track
        connectionSlider.addEventListener('click', (e) => {
            updateSlider(e.clientX);
        });
    }

    // --- FAQ ACCORDION ---
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        item.querySelector('.faq-question').addEventListener('click', () => {
            // Close others (optional - standard accordion behavior)
            // faqItems.forEach(i => {
            //     if (i !== item) i.classList.remove('active');
            // });

            // Toggle current
            item.classList.toggle('active');

            // Icon rotation handled by CSS via .active class
        });
    });
});
