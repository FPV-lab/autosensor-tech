/* ==========================================================
   AutoSensor Tech — Shared JavaScript
   ========================================================== */
(function () {
  'use strict';

  /* ---------- Mobile Hamburger ---------- */
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('hamburger--open');
      mobileNav.classList.toggle('mobile-nav--open');
      document.body.style.overflow = mobileNav.classList.contains('mobile-nav--open') ? 'hidden' : '';
    });
    // Close on link click
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('hamburger--open');
        mobileNav.classList.remove('mobile-nav--open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Active Nav Highlighting ---------- */
  const currentPath = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href) {
      const linkPath = href.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
      if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
        link.classList.add('nav__link--active');
      }
    }
  });

  /* ---------- Back to Top ---------- */
  const backBtn = document.querySelector('.back-to-top');
  if (backBtn) {
    window.addEventListener('scroll', () => {
      backBtn.classList.toggle('back-to-top--visible', window.scrollY > 400);
    }, { passive: true });
    backBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Smooth scroll for anchor links ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ---------- Tabs ---------- */
  document.querySelectorAll('.tabs').forEach(tabGroup => {
    const btns = tabGroup.querySelectorAll('.tabs__btn');
    const panels = tabGroup.querySelectorAll('.tabs__panel');
    btns.forEach((btn, i) => {
      btn.addEventListener('click', () => {
        btns.forEach(b => b.classList.remove('tabs__btn--active'));
        panels.forEach(p => p.classList.remove('tabs__panel--active'));
        btn.classList.add('tabs__btn--active');
        panels[i].classList.add('tabs__panel--active');
      });
    });
  });

  /* ---------- News Filter ---------- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const newsCards = document.querySelectorAll('.news-card');
  if (filterBtns.length && newsCards.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('filter-btn--active'));
        btn.classList.add('filter-btn--active');
        const cat = btn.dataset.filter;
        newsCards.forEach(card => {
          card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
        });
      });
    });
  }

  /* ---------- Header scroll effect ---------- */
  const header = document.querySelector('.header');
  if (header) {
    let last = 0;
    window.addEventListener('scroll', () => {
      header.style.background = window.scrollY > 50
        ? 'rgba(10,22,40,0.95)'
        : 'rgba(10,22,40,0.85)';
    }, { passive: true });
  }
})();
