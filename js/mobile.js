/**
 * MIZSOFT — MOBILE FLUID JS
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Bottom Navigation Interactions ---
    const navItems = document.querySelectorAll('.nav-item');
    const appContainer = document.querySelector('.app-container');
    const sections = Array.from(document.querySelectorAll('.app-view'));

    // Update Active Tab based on scroll
    appContainer.addEventListener('scroll', () => {
        let currentSectionIndex = 0;
        const scrollPos = appContainer.scrollTop;

        sections.forEach((sec, index) => {
            // Small offset for better trigger
            if (sec.offsetTop <= scrollPos + 100) {
                currentSectionIndex = index;
            }
        });

        navItems.forEach(item => item.classList.remove('active'));
        if (navItems[currentSectionIndex]) {
            navItems[currentSectionIndex].classList.add('active');
        }
    });

    // --- FAB Menu Toggle ---
    const fabBtn = document.getElementById('fab-btn');
    const fabMenu = document.getElementById('fab-menu');

    fabBtn.addEventListener('click', () => {
        fabBtn.classList.toggle('open');
        fabMenu.classList.toggle('active');
    });

    // Automatically close FAB when clicking outside
    document.addEventListener('click', (e) => {
        if (!fabBtn.contains(e.target) && !fabMenu.contains(e.target) && fabMenu.classList.contains('active')) {
            fabBtn.classList.remove('open');
            fabMenu.classList.remove('active');
        }
    });

    // --- iOS Bottom Sheet ---
    const bottomSheet = document.getElementById('bottom-sheet');
    const overlay = document.getElementById('overlay');
    const openSheetBtns = document.querySelectorAll('[data-open-sheet]');

    const openSheet = () => {
        bottomSheet.classList.add('open');
        overlay.classList.add('active');
        appContainer.style.overflow = 'hidden'; // prevent background scrolling
    }

    const closeSheet = () => {
        bottomSheet.classList.remove('open');
        overlay.classList.remove('active');
        appContainer.style.overflow = '';
    }

    openSheetBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            // Close FAB if open
            fabBtn.classList.remove('open');
            fabMenu.classList.remove('active');

            openSheet();
        });
    });

    overlay.addEventListener('click', closeSheet);

    // Sheet drag down to close (Simple Implementation)
    const sheetDrag = document.querySelector('.sheet-drag');
    let startY;

    sheetDrag.addEventListener('touchstart', (e) => {
        startY = e.touches[0].clientY;
    }, { passive: true });

    sheetDrag.addEventListener('touchmove', (e) => {
        const y = e.touches[0].clientY;
        if (y > startY + 50) { // Threshold reached
            closeSheet();
        }
    }, { passive: true });

});
