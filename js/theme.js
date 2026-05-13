(function() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlRoot = document.getElementById('html-root');
    
    // Moon icon for dark mode
    const moonIcon = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
    // Sun icon for light mode
    const sunIcon = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';

    function setTheme(theme) {
        if(htmlRoot) htmlRoot.setAttribute('data-theme', theme);
        localStorage.setItem('mizsoft-theme', theme);
        if(themeIcon) {
            themeIcon.innerHTML = theme === 'light' ? sunIcon : moonIcon;
        }
    }

    // Initialize theme
    const savedTheme = localStorage.getItem('mizsoft-theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        // default to dark
        setTheme('dark');
    }

    if(themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlRoot.getAttribute('data-theme') || 'dark';
            setTheme(currentTheme === 'light' ? 'dark' : 'light');
        });
    }
})();
