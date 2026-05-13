/**
 * Mizsoft - Mobile GSAP Animations
 * Premium scroll-based interactions and entrance animations for mobile layout.
 */

document.addEventListener("DOMContentLoaded", (event) => {
    gsap.registerPlugin(ScrollTrigger);

    // Xoá transition mặc định để GSAP xử lý
    document.querySelectorAll('.reveal').forEach(el => {
        el.style.opacity = 1;
        el.style.transform = 'none';
        el.style.transition = 'none';
        el.classList.remove('reveal');
    });

    // 1. Mobile Hero Section
    const heroTl = gsap.timeline({ defaults: { ease: "power4.out" } });
    
    heroTl.fromTo(".m-hero-bg-text", 
        { scale: 0.5, opacity: 0 }, 
        { scale: 1, opacity: 0.15, duration: 2, ease: "power2.out" }
    )
    .fromTo(".m-hero-badge",
        { y: -20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8 },
        "-=1.5"
    )
    .fromTo(".m-hero-title",
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=1.2"
    )
    .fromTo(".m-hero-desc",
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=0.8"
    )
    .fromTo(".m-hero-cta",
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=0.6"
    );

    // 2. Swipe Cards (Work)
    gsap.from(".swipe-card", {
        scrollTrigger: {
            trigger: ".swipe-track",
            scroller: ".app",
            start: "top 85%"
        },
        x: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: "power2.out"
    });

    // 3. Stats Grid
    gsap.from(".stat-item", {
        scrollTrigger: {
            trigger: ".stats-grid",
            scroller: ".app",
            start: "top 90%"
        },
        scale: 0.8,
        y: 20,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: "back.out(1.5)"
    });

    // 4. Services List
    gsap.from(".svc-item", {
        scrollTrigger: {
            trigger: ".svc-list",
            scroller: ".app",
            start: "top 90%"
        },
        x: -20,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: "power2.out"
    });
});
