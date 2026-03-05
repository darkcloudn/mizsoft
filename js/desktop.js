/**
 * MIZSOFT — DESKTOP FLUID JS
 * Smooth water animations, GSAP interactions
 */

document.addEventListener('DOMContentLoaded', () => {

    // 1. Create floating water droplets for Hero
    const hero = document.querySelector('.hero');
    if (hero) {
        for (let i = 0; i < 15; i++) {
            const drop = document.createElement('div');
            drop.classList.add('droplet');

            // Random properties for water droplets
            const size = Math.random() * 40 + 10;
            const left = Math.random() * 100;
            const duration = Math.random() * 10 + 10;
            const delay = Math.random() * -20; // negative delay so they start immediately

            drop.style.width = `${size}px`;
            drop.style.height = `${size}px`;
            drop.style.left = `${left}%`;
            drop.style.animationDuration = `${duration}s`;
            drop.style.animationDelay = `${delay}s`;

            hero.appendChild(drop);
        }
    }

    // 2. Slide-in Contact Panel
    const panel = document.getElementById('slide-panel');
    const overlay = document.getElementById('overlay');
    const openBtns = document.querySelectorAll('[data-open-panel]');
    const closeBtns = document.querySelectorAll('[data-close-panel]');

    const openPanel = () => {
        panel.classList.add('open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    const closePanel = () => {
        panel.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    };

    openBtns.forEach(btn => btn.addEventListener('click', (e) => {
        e.preventDefault();
        openPanel();
    }));

    closeBtns.forEach(btn => btn.addEventListener('click', closePanel));
    overlay.addEventListener('click', closePanel);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closePanel();
    });

    // 3. Ultra-smooth GSAP Scroll Animations (Fluid Up)
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Hero Text Stagger (flows up gently)
        gsap.from('.hero h1, .hero p, .hero-actions, .hero-badge', {
            y: 50,
            opacity: 0,
            duration: 1.2,
            stagger: 0.15,
            ease: 'power3.out',
            delay: 0.2
        });

        // Sections ripple up
        const sections = gsap.utils.toArray('.gs-reveal');
        sections.forEach(sec => {
            gsap.from(sec, {
                scrollTrigger: {
                    trigger: sec,
                    start: 'top 85%',
                },
                y: 80,
                opacity: 0,
                duration: 1.2,
                ease: 'power3.out'
            });
        });

        // Project grid stagger
        gsap.from('.project-card', {
            scrollTrigger: {
                trigger: '.project-grid',
                start: 'top 80%',
            },
            y: 60,
            opacity: 0,
            duration: 1,
            stagger: 0.15,
            ease: 'back.out(1.4)'
        });
    }

});
