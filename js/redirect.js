/**
 * Mizsoft — Device Detection & Auto-Redirect
 * index.html (desktop) ↔ mobile.html (mobile)
 */
(function () {
    'use strict';

    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
        || (window.innerWidth <= 768);

    var currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // Cho phép override bằng query param ?force=desktop hoặc ?force=mobile
    var params = new URLSearchParams(window.location.search);
    var force = params.get('force');

    if (force === 'desktop' || force === 'mobile') {
        return; // Không redirect nếu có force param
    }

    if (isMobile && (currentPage === 'index.html' || currentPage === '')) {
        window.location.replace('mobile.html');
    } else if (!isMobile && currentPage === 'mobile.html') {
        window.location.replace('index.html');
    }
})();
