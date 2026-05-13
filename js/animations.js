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
    const heroTimeline = gsap.timeline({ defaults: { ease: "power4.out" } });

    // Cực quang phía sau nở dần ra
    heroTimeline.fromTo(".hero-bg-text", 
        { scale: 0.8, opacity: 0 }, 
        { scale: 1, opacity: 0.15, duration: 2.5, ease: "power2.out" }
    )
    // Các dải glow sáng lên
    .fromTo(".ambient-glow .glow-1, .ambient-glow .glow-2, .ambient-glow .glow-3",
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 0.8, duration: 2, stagger: 0.2 },
        "-=2"
    )
    // Huy hiệu Tokyo x Vietnam rơi xuống nhẹ nhàng
    .fromTo(".hero-badge",
        { y: -30, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=1.5"
    )
    // Tiêu đề chính hiện lên theo từng dòng
    .fromTo(".hero-title, .hero-title span",
        { y: 40, opacity: 0, rotationX: -20 },
        { y: 0, opacity: 1, rotationX: 0, duration: 1.2, stagger: 0.1, transformOrigin: "0% 50% -50" },
        "-=1.2"
    )
    // Chữ mô tả và các nút fade in lên
    .fromTo(".hero-desc",
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=0.8"
    )
    .fromTo(".hero-cta",
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 1 },
        "-=0.6"
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
