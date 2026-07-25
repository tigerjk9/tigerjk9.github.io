/* '이미 읽은 글' 표시
   방문한 글을 localStorage(readPosts)에 기록하고, 리스트·검색 결과에서
   해당 항목에 .is-read 클래스 + '읽음' 배지를 붙인다.
   (기존 recentPosts는 최근 8개 한정이라 전체 추적용으로 별도 키 사용) */
(function () {
  var KEY = 'readPosts';
  var MAX = 800;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function save(a) {
    try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {}
  }
  function norm(u) {
    if (!u) return '';
    try { u = new URL(u, location.origin).pathname; } catch (e) {}
    return u.replace(/\/+$/, ''); // 끝 슬래시 제거 후 비교
  }

  var read = load();

  // 1) 현재 페이지가 콘텐츠(포스트·강의·페이지)면 읽음 기록
  if (window.__currentPost && window.__currentPost.url) {
    var cur = norm(location.pathname);
    if (cur && read.indexOf(cur) === -1) {
      read.push(cur);
      if (read.length > MAX) read = read.slice(-MAX);
      save(read);
    }
  }

  // 2) 리스트·검색 결과에서 읽은 항목 표시
  var set = {};
  read.forEach(function (u) { set[norm(u)] = 1; });

  function makeBadge() {
    var s = document.createElement('span');
    s.className = 'entry-read';
    s.title = '읽은 글';
    s.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i> 읽음';
    return s;
  }

  function mark(root) {
    var items = (root || document).querySelectorAll(
      '.recent-posts .archive__item, .search-results .archive__item'
    );
    Array.prototype.forEach.call(items, function (item) {
      if (item.classList.contains('is-read')) return;
      var a = item.querySelector('.archive__item-title a');
      if (!a || !set[norm(a.getAttribute('href'))]) return;
      item.classList.add('is-read');
      var eyebrow = item.querySelector('.entry-eyebrow');
      if (eyebrow) eyebrow.appendChild(makeBadge());
    });
  }

  mark(document);

  // 검색 결과는 타이핑마다 비동기로 다시 그려짐 → 관찰해서 재표시
  var results = document.getElementById('results');
  if (results && window.MutationObserver) {
    new MutationObserver(function () { mark(results); })
      .observe(results, { childList: true, subtree: true });
  }
})();
