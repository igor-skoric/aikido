document.querySelectorAll('.accordion-toggle').forEach((btn) => {
  if (!btn.hasAttribute('aria-expanded')) {
    btn.setAttribute('aria-expanded', 'false');
  }

  btn.addEventListener('click', () => {
    const panel = btn.nextElementSibling;
    if (!panel || !panel.classList.contains('accordion-panel')) return;

    const icon = btn.querySelector('.icon');
    const isOpen = btn.getAttribute('aria-expanded') === 'true';

    const parent = btn.closest('.accordion-group') || btn.parentElement?.parentElement;
    if (parent) {
      parent.querySelectorAll(':scope > * > .accordion-toggle, :scope > .accordion-toggle').forEach((other) => {
        if (other === btn) return;
        const otherPanel = other.nextElementSibling;
        if (otherPanel?.classList.contains('accordion-panel')) {
          otherPanel.style.maxHeight = '0px';
          other.setAttribute('aria-expanded', 'false');
          const otherIcon = other.querySelector('.icon');
          if (otherIcon) otherIcon.textContent = '+';
        }
      });
    }

    if (isOpen) {
      panel.style.maxHeight = '0px';
      btn.setAttribute('aria-expanded', 'false');
      if (icon) icon.textContent = '+';
    } else {
      panel.style.maxHeight = panel.scrollHeight + 'px';
      btn.setAttribute('aria-expanded', 'true');
      if (icon) icon.textContent = '−';

      let ancestor = panel.parentElement;
      while (ancestor) {
        if (ancestor.classList.contains('accordion-panel')) {
          ancestor.style.maxHeight = 'none';
        }
        ancestor = ancestor.parentElement;
      }
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const show = (el) => el.classList.add('is-visible');

  document.querySelectorAll('.reveal-stagger').forEach((parent) => {
    const children = parent.querySelectorAll(':scope > .reveal, :scope > li > .reveal, :scope > * > .reveal');
    const seen = new Set();
    let index = 0;
    children.forEach((el) => {
      if (seen.has(el)) return;
      seen.add(el);
      if (!el.style.getPropertyValue('--reveal-delay')) {
        el.style.setProperty('--reveal-delay', `${index * 90}ms`);
      }
      index += 1;
    });
  });

  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(show);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          show(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -8% 0px' }
  );

  reveals.forEach((el) => {
    const rect = el.getBoundingClientRect();
    const inView = rect.top < window.innerHeight * 0.92 && rect.bottom > 0;
    if (inView) show(el);
    else observer.observe(el);
  });
});
