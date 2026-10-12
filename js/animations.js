/**
 * Mizsoft - GSAP Animations (The WOW Factor)
 * Premium scroll-based interactions and entrance animations.
 */

document.addEventListener("DOMContentLoaded", (event) => {
    // Đăng ký plugin ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // Xoá class reveal tĩnh cũ (nếu có CSS transition mặc định) để GSAP điều khiển hoàn toàn
    document.querySelectorAll('.reveal').forEach(el => {
        el.style.opacity = 1;
        el.style.transform = 'none';
        el.style.transition = 'none';
        el.classList.remove('reveal');
    });

    // 1. Hiệu ứng mở đầu (Hero Section)
    const heroTimeline = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Huy hiệu và các thẻ capsule
    heroTimeline.fromTo(".hero-eyebrow-wrap",
        { y: -20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6 }
    )
    // Tiêu đề chính hiện lên theo từng dòng dứt khoát
    .fromTo(".hero-title .line",
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08 },
        "-=0.3"
    )
    // Chữ mô tả
    .fromTo(".hero-desc",
        { y: 15, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5 },
        "-=0.3"
    )
    // Các nút CTA
    .fromTo(".hero-actions",
        { y: 15, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5 },
        "-=0.3"
    );

    // 2. Hiệu ứng cuộn cho Bento Grid (Dịch vụ)
    gsap.from(".bento-card", {
        scrollTrigger: {
            trigger: ".bento-grid",
            start: "top 80%", // Khi top của lưới chạm tới 80% chiều cao màn hình
            toggleActions: "play none none reverse"
        },
        y: 60,
        opacity: 0,
        rotationX: -10,
        duration: 1,
        stagger: 0.15, // Lên lần lượt
        ease: "power3.out"
    });

    // 3. Hiệu ứng cuộn cho Các dự án (Work)
    gsap.from(".work-card", {
        scrollTrigger: {
            trigger: ".work-grid",
            start: "top 85%",
        },
        y: 50,
        scale: 0.95,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "power2.out"
    });

    // 4. Hiệu ứng cuộn cho Các thông số (Stats)
    gsap.from(".stat-item", {
        scrollTrigger: {
            trigger: ".stats",
            start: "top 90%",
        },
        scale: 0.5,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "back.out(1.5)"
    });

    // 5. Hiệu ứng cuộn cho Banner cuối (CTA Band)
    gsap.from(".cta-band", {
        scrollTrigger: {
            trigger: ".cta-band",
            start: "top 90%",
        },
        y: 40,
        opacity: 0,
        duration: 1,
        ease: "power3.out"
    });
});
