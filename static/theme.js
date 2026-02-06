// static/theme.js

document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Check for saved user preference, if any, on load
    const currentTheme = localStorage.getItem('theme');

    // If the user's preference in localStorage is dark...
    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        updateIcon('light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateIcon('dark');
    }

    // Toggle theme on click
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let theme = document.documentElement.getAttribute('data-theme');

            if (theme === 'light') {
                theme = 'dark';
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                updateIcon('dark');
            } else {
                theme = 'light';
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                updateIcon('light');
            }
        });
    }

    function updateIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'light') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
});
