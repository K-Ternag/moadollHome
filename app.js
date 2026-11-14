/* Progressive enhancement only. Reading, links, FAQs and email work without JS. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#navigation');
  if (menu && nav) {
    menu.hidden = false;
    const closeMenu = (restoreFocus = false) => {
      nav.classList.remove('is-open');
      menu.setAttribute('aria-expanded', 'false');
      if (restoreFocus) menu.focus();
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) closeMenu(true);
    });
    document.addEventListener('click', e => {
      if (!e.target.closest('.site-header')) closeMenu();
    });
    matchMedia('(min-width: 801px)').addEventListener('change', e => { if (e.matches) closeMenu(); });
  }

  const tablist = document.querySelector('.feature-tabs');
  if (tablist) {
    const tabs = [...tablist.querySelectorAll('.feature-tab')];
    const panels = tabs.map(tab => document.querySelector(tab.getAttribute('href')));
    tablist.setAttribute('role', 'tablist');
    const activate = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      const select = next => {
        activate(next, true);
        history.replaceState(null, '', '#' + panels[next].id);
      };
      tab.addEventListener('click', event => { event.preventDefault(); select(index); });
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next); }
      });
    });
    const fromHash = () => {
      const index = panels.findIndex(panel => '#' + panel.id === location.hash);
      if (index >= 0) activate(index);
      return index;
    };
    if (fromHash() < 0) activate(0);
    window.addEventListener('hashchange', fromHash);
  }

  // Preserve the corresponding section when changing languages.
  document.querySelectorAll('.language-link').forEach(link => {
    link.addEventListener('click', () => {
      const active = document.querySelector('.feature-tab[aria-selected="true"]');
      const anchor = location.hash.startsWith('#feature-') && active ? active.getAttribute('href') : location.hash;
      link.href = link.getAttribute('href').split('#')[0] + anchor;
    });
  });

  const dialog = document.querySelector('#lightbox');
  if (dialog && typeof dialog.showModal === 'function') {
    let trigger;
    const close = () => dialog.close();
    document.querySelectorAll('[data-zoom]').forEach(link => {
      link.addEventListener('click', event => {
        event.preventDefault();
        trigger = link;
        const img = dialog.querySelector('img');
        img.src = link.href;
        img.alt = link.dataset.caption || link.querySelector('img')?.alt || '';
        document.querySelector('#lightbox-caption').textContent = img.alt;
        dialog.showModal();
        document.body.classList.add('dialog-open');
        dialog.querySelector('.close-dialog').focus();
      });
    });
    dialog.querySelector('.close-dialog').addEventListener('click', close);
    dialog.addEventListener('click', event => {
      const box = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
      trigger?.focus();
    });
  }
})();
