/* ==========================================================================
   Theme Toggle (Dark / Light)
   ========================================================================== */

(function () {
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  // 이벤트 위임: 정적 버튼(masthead)과 동적 주입 버튼(사이드바) 모두 처리
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.theme-toggle')) return;
    var current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'light' ? 'dark' : 'light');
  });

  // 모바일: 외부 이미지(hits 배지 등) 로드 완료 후 greedy-nav 재계산 트리거
  if (window.innerWidth < 1024) {
    window.addEventListener('load', function () {
      window.dispatchEvent(new Event('resize'));
    });
  }
})();
