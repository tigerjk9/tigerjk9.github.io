/* ==========================================================================
   포스트 소셜 공유 (카카오톡 · X · 링크드인 · 페이스북 · 스레드 · 링크복사)
   window.__currentPost { title, url, description, image } 를 활용한다.
   카카오톡은 SDK(키 설정 시) → OS 공유시트 → 링크복사 순으로 점진적 폴백.
   ========================================================================== */

(function () {
  var panel = document.querySelector('.post-share');
  if (!panel) return;

  var post = window.__currentPost || {};
  var shareUrl = post.url || window.location.href;
  var shareTitle = post.title || document.title;
  var shareDesc = post.description || '';
  var shareImage = post.image || '';

  function openPopup(url) {
    window.open(url, '_blank', 'noopener,noreferrer,width=600,height=640');
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

  var toastTimer = null;
  function toast(msg) {
    var el = document.getElementById('share-toast');
    if (!el) {
      el = document.createElement('div');
      el.id = 'share-toast';
      el.className = 'share-toast';
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add('share-toast--show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.classList.remove('share-toast--show');
    }, 2200);
  }

  function shareKakao(btn) {
    if (window.Kakao && window.__kakaoKey) {
      try {
        if (!window.Kakao.isInitialized()) window.Kakao.init(window.__kakaoKey);
        window.Kakao.Share.sendDefault({
          objectType: 'feed',
          content: {
            title: shareTitle,
            description: shareDesc,
            imageUrl: shareImage,
            link: { mobileWebUrl: shareUrl, webUrl: shareUrl }
          },
          buttons: [{
            title: '글 보러가기',
            link: { mobileWebUrl: shareUrl, webUrl: shareUrl }
          }]
        });
        return;
      } catch (e) {
        console.error('카카오 공유 실패:', e);
      }
    }
    // 폴백: 모바일 OS 공유시트 → 링크복사
    if (navigator.share) {
      navigator.share({ title: shareTitle, url: shareUrl }).catch(function () {});
    } else {
      copyToClipboard(window.location.href, function () {
        toast('링크를 복사했어요. 카카오톡에 붙여넣어 공유하세요.');
      });
    }
  }

  var handlers = {
    kakao: shareKakao,
    x: function () {
      openPopup('https://twitter.com/intent/tweet?text=' +
        encodeURIComponent(shareTitle) + '&url=' + encodeURIComponent(shareUrl));
    },
    linkedin: function () {
      openPopup('https://www.linkedin.com/sharing/share-offsite/?url=' +
        encodeURIComponent(shareUrl));
    },
    facebook: function () {
      openPopup('https://www.facebook.com/sharer/sharer.php?u=' +
        encodeURIComponent(shareUrl));
    },
    threads: function () {
      openPopup('https://www.threads.net/intent/post?text=' +
        encodeURIComponent(shareTitle + ' ' + shareUrl));
    }
  };

  panel.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-share]');
    if (!btn) return;
    var kind = btn.getAttribute('data-share');
    if (handlers[kind]) handlers[kind](btn);
  });
})();
