/*
 * 게시글 링크 새 탭 열기
 * 목록(홈·카테고리·태그)·검색 결과·관련 글·최근 방문 사이드바에서
 * 게시글 제목을 클릭하면 새 탭(창)에서 열리도록 target="_blank"를 부여한다.
 * 본문 내부 링크·마스트헤드·단일 글 제목(.page__title)은 대상이 아니다.
 * 검색 결과·최근 방문처럼 JS로 나중에 그려지는 목록은 MutationObserver로 처리한다.
 */
(function () {
  'use strict';

  // 목록/검색/관련글 제목 링크 + 최근 방문 사이드바 링크
  var SELECTOR = '.archive__item-title a, .recent-posts__list a';

  function mark() {
    var links = document.querySelectorAll(SELECTOR);
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (a.getAttribute('target') === '_blank') continue;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#') continue;
      a.setAttribute('target', '_blank');
      var rel = a.getAttribute('rel') || '';
      if (rel.indexOf('noopener') === -1) {
        a.setAttribute('rel', (rel + ' noopener').trim());
      }
    }
  }

  function init() {
    mark();
    // 검색 결과·최근 방문 등 동적 렌더 목록 대응 (디바운스된 전체 재스캔)
    if (window.MutationObserver && document.body) {
      // 비시각적 작업이라 rAF(백그라운드 탭 throttle) 대신 setTimeout으로 디바운스
      var scheduled = false;
      var obs = new MutationObserver(function () {
        if (scheduled) return;
        scheduled = true;
        window.setTimeout(function () { scheduled = false; mark(); }, 16);
      });
      obs.observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
