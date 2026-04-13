/* ==========================================================================
   Post Content Copy Button
   ========================================================================== */

(function () {
  var btn = document.getElementById('post-copy-btn');
  if (!btn) return;

  btn.addEventListener('click', function () {
    var content = document.querySelector('.page__content');
    if (!content) return;

    // 클론 후 불필요한 요소 제거
    var clone = content.cloneNode(true);
    // "On this page" TOC 제거
    clone.querySelectorAll('.sidebar__right, .toc, nav.toc').forEach(function (el) { el.remove(); });
    // Permalink 앵커 제거
    clone.querySelectorAll('[rel="permalink"], .sr-only').forEach(function (el) { el.remove(); });

    var text = clone.innerText || clone.textContent || '';

    function onSuccess() {
      btn.innerHTML = '<i class="fas fa-fw fa-check"></i> 복사됨!';
      btn.classList.add('post-copy-btn--done');
      setTimeout(function () {
        btn.innerHTML = '<i class="fas fa-fw fa-copy"></i> 본문 복사';
        btn.classList.remove('post-copy-btn--done');
      }, 2000);
    }

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(function () {
        fallbackCopy(text, onSuccess);
      });
    } else {
      fallbackCopy(text, onSuccess);
    }
  });

  function fallbackCopy(text, callback) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    textarea.setAttribute('readonly', '');
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      callback();
    } catch (e) {
      console.error('복사 실패:', e);
    }
    document.body.removeChild(textarea);
  }
})();
