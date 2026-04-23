(function () {
  function isMobile() { return window.innerWidth < 1024; }

  var tocEl = document.querySelector('.sidebar__right .toc');
  if (!tocEl) return;

  // 플로팅 버튼
  var btn = document.createElement('button');
  btn.id = 'mobile-toc-btn';
  btn.setAttribute('aria-label', '목차 열기/닫기');
  btn.innerHTML = '<i class="fas fa-list-ul"></i>';
  document.body.appendChild(btn);

  // 오버레이
  var overlay = document.createElement('div');
  overlay.id = 'mobile-toc-overlay';
  document.body.appendChild(overlay);

  // 드로어
  var drawer = document.createElement('div');
  drawer.id = 'mobile-toc-drawer';

  var header = document.createElement('div');
  header.className = 'mobile-toc-drawer__header';
  header.innerHTML =
    '<span>목차</span>' +
    '<button class="mobile-toc-drawer__close" aria-label="닫기"><i class="fas fa-times"></i></button>';

  var tocClone = tocEl.cloneNode(true);

  drawer.appendChild(header);
  drawer.appendChild(tocClone);
  document.body.appendChild(drawer);

  function open() {
    drawer.classList.add('open');
    overlay.classList.add('open');
    btn.classList.add('active');
  }

  function close() {
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    btn.classList.remove('active');
  }

  btn.addEventListener('click', function () {
    drawer.classList.contains('open') ? close() : open();
  });

  overlay.addEventListener('click', close);

  header.querySelector('.mobile-toc-drawer__close').addEventListener('click', close);

  // TOC 링크 클릭 시 드로어 닫기
  drawer.addEventListener('click', function (e) {
    if (e.target.closest('a')) close();
  });

  function updateVisibility() {
    btn.style.display = isMobile() ? 'flex' : 'none';
    if (!isMobile()) close();
  }

  updateVisibility();
  window.addEventListener('resize', updateVisibility);
})();
