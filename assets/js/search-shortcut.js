/* 검색 키보드 단축키
   '/' 또는 Ctrl/Cmd+K 로 검색 오버레이 열기.
   (자동 포커스·Esc 닫기는 테마 main.min.js가 이미 처리) */
(function () {
  function isTyping(el) {
    if (!el) return false;
    var tag = el.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || el.isContentEditable;
  }

  function isSearchOpen() {
    var sc = document.querySelector('.search-content');
    return !!(sc && sc.classList.contains('is--visible'));
  }

  function openSearch() {
    if (isSearchOpen()) return;
    var toggle = document.querySelector('.search__toggle');
    if (toggle) toggle.click(); // 테마의 열기 로직 재사용(가시화 + 입력 포커스)
  }

  document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + K → 검색 열기 (브라우저 기본 동작 억제)
    if ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      openSearch();
      return;
    }

    // '/' → 검색 열기 (입력 중이거나 조합키일 땐 무시)
    if (
      e.key === '/' &&
      !e.ctrlKey && !e.metaKey && !e.altKey &&
      !isTyping(document.activeElement)
    ) {
      if (isSearchOpen()) return;
      e.preventDefault();
      openSearch();
    }
  });
})();
