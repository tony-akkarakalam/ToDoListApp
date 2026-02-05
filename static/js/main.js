document.addEventListener('DOMContentLoaded', () => {
    // Splash Screen Logic
    const splash = document.getElementById('splash-screen');
    if (splash) {
        setTimeout(() => {
            splash.style.opacity = '0';
            splash.style.visibility = 'hidden';

            // Wait for transition, then remove
            setTimeout(() => {
                if (splash.parentNode) {
                    splash.parentNode.removeChild(splash);
                }
            }, 500); // 0.5s matches CSS transition
        }, 2500);
    }

    // Theme Toggle Logic
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    toggleBtn.className = 'btn btn-primary theme-toggle';
    toggleBtn.style.position = 'fixed';
    toggleBtn.style.bottom = '20px';
    toggleBtn.style.left = '20px';
    toggleBtn.style.borderRadius = '50%';
    toggleBtn.style.width = '50px';
    toggleBtn.style.height = '50px';
    toggleBtn.style.padding = '0';
    toggleBtn.style.zIndex = '1000';
    toggleBtn.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';

    document.body.appendChild(toggleBtn);

    // Check saved preference
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'light') {
        document.body.classList.add('light-mode');
        toggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }

    toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');

        let theme = 'dark';
        if (document.body.classList.contains('light-mode')) {
            theme = 'light';
            toggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            toggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
        localStorage.setItem('theme', theme);
    });
});
