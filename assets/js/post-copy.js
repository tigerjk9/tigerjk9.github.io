/* ==========================================================================
   Post Content Copy Button
   ========================================================================== */

(function () {
  function getDecodedUrl() {
    try {
      return decodeURIComponent(window.location.href);
    } catch (e) {
      return window.location.href;
    }
  }

  function copyToClipboard(text, onSuccess) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(function () {
        fallbackCopy(text, onSuccess);
      });
    } else {
      fallbackCopy(text, onSuccess);
    }
  }

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

  // 본문 복사 버튼
  var btn = document.getElementById('post-copy-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var content = document.querySelector('.page__content');
      if (!content) return;

      var clone = content.cloneNode(true);
      clone.querySelectorAll('.sidebar__right, .toc, nav.toc').forEach(function (el) { el.remove(); });
      clone.querySelectorAll('[rel="permalink"], .sr-only').forEach(function (el) { el.remove(); });

      var text = clone.innerText || clone.textContent || '';
      text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      text = text.replace(/\n{3,}/g, '\n\n');
      text = text.trim();

      // 원문링크를 <출처> 앞에 삽입, 없으면 맨 끝에 추가
      var urlLine = '원문링크: ' + getDecodedUrl();
      var sourceIdx = text.indexOf('<출처>');
      if (sourceIdx !== -1) {
        text = text.slice(0, sourceIdx).trimEnd() + '\n\n' + urlLine + '\n\n' + text.slice(sourceIdx);
      } else {
        text = text + '\n\n' + urlLine;
      }

      copyToClipboard(text, function () {
        btn.innerHTML = '<i class="fas fa-fw fa-check"></i> 복사됨!';
        btn.classList.add('post-copy-btn--done');
        setTimeout(function () {
          btn.innerHTML = '<i class="fas fa-fw fa-copy"></i> 본문 복사';
          btn.classList.remove('post-copy-btn--done');
        }, 2000);
      });
    });
  }

  // 링크 복사 버튼
  var urlBtn = document.getElementById('post-url-btn');
  if (urlBtn) {
    urlBtn.addEventListener('click', function () {
      copyToClipboard(getDecodedUrl(), function () {
        urlBtn.innerHTML = '<i class="fas fa-fw fa-check"></i> 복사됨!';
        urlBtn.classList.add('post-copy-btn--done');
        setTimeout(function () {
          urlBtn.innerHTML = '<i class="fas fa-fw fa-link"></i> 링크 복사';
          urlBtn.classList.remove('post-copy-btn--done');
        }, 2000);
      });
    });
  }
})();
