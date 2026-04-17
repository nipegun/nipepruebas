(function() {
  'use strict';

  var sidebar = document.getElementById('sidebar');
  var sidebarToggle = document.getElementById('sidebarToggle');
  var sidebarOverlay = document.getElementById('sidebarOverlay');
  var storageKey = 'saas-dark-sidebar-collapsed';

  function isSmallScreen() {
    return window.innerWidth <= 1024;
  }

  function applyCollapsedState() {
    if (isSmallScreen()) return;
    var collapsed = localStorage.getItem(storageKey) === '1';
    if (collapsed) {
      document.body.classList.add('sidebar-collapsed');
    } else {
      document.body.classList.remove('sidebar-collapsed');
    }
  }

  function toggleCollapse() {
    if (isSmallScreen()) {
      if (sidebar.classList.contains('open')) {
        closeMobileSidebar();
      } else {
        openMobileSidebar();
      }
      return;
    }
    var isCollapsed = document.body.classList.toggle('sidebar-collapsed');
    localStorage.setItem(storageKey, isCollapsed ? '1' : '0');
  }

  function openMobileSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    if (sidebarOverlay) sidebarOverlay.classList.add('active');
    document.body.classList.add('sidebar-open');
  }

  function closeMobileSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    document.body.classList.remove('sidebar-open');
  }

  applyCollapsedState();

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function(ev) {
      ev.preventDefault();
      toggleCollapse();
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', function() {
      closeMobileSidebar();
    });
  }

  document.addEventListener('keydown', function(ev) {
    if (ev.key === 'Escape') {
      closeMobileSidebar();
    }
  });

  var indicators = document.getElementById('indicators');
  var sidebarIndicators = document.getElementById('sidebarIndicators');
  if (indicators && sidebarIndicators) {
    var observer = new MutationObserver(function() {
      while (indicators.firstChild) {
        sidebarIndicators.appendChild(indicators.firstChild);
      }
    });
    observer.observe(indicators, { childList: true });
  }
})();
