---
layout: default
title: "학습과학 아틀라스"
permalink: /learning-science-atlas/
description: "인지부하이론, 정보처리이론, 인지심리학, 체화된 인지에서 뇌과학과 AI까지, 학습과학 연구 162편의 계보와 영향을 3D로 탐색하는 지도. 투어 10개, 개념 사전 70개, 경로 찾기, 인출 연습 퀴즈."
header:
  og_image: /assets/learning-science-atlas-teaser.jpg
---

<style>
  html, body { background: #05070d !important; overflow: hidden !important; }
  .initial-content, #main { margin: 0 !important; padding: 0 !important; max-width: none !important; width: 100% !important; }
  .page__footer, footer.page__footer, .sidebar, .page__related { display: none !important; }
  #lsa-wrap { position: fixed; left: 0; right: 0; bottom: 0; top: var(--lsa-top, 70px); background: #05070d; z-index: 1; }
  #lsa-frame { display: block; width: 100%; height: 100%; border: 0; }
  #lsa-noscript { color: #cbd5e1; padding: 24px; }
</style>

<div id="lsa-wrap"><iframe id="lsa-frame" src="/tools/learning-science-atlas/?inblog=1" title="학습과학 아틀라스, 학습과학 연구 162편의 3D 계보 지도" allow="clipboard-write; fullscreen" allowfullscreen></iframe></div>
<noscript><p id="lsa-noscript">학습과학 아틀라스는 자바스크립트가 필요합니다. <a href="/tools/learning-science-atlas/?text=1">텍스트 버전</a>이나 <a href="/post/learning-science-atlas/">소개 글</a>을 이용해 주세요.</p></noscript>

<script>
(function () {
  function fit() {
    var m = document.querySelector('.masthead');
    var top = m ? Math.round(m.getBoundingClientRect().bottom) : 0;
    document.documentElement.style.setProperty('--lsa-top', Math.max(0, top) + 'px');
  }
  window.addEventListener('load', fit); window.addEventListener('resize', fit); fit(); setTimeout(fit, 400);
  var f = document.getElementById('lsa-frame');
  var qs = location.search ? location.search.replace(/^\?/, '&') : '';
  if (qs || location.hash) f.src = '/tools/learning-science-atlas/?inblog=1' + qs + location.hash;
})();
</script>
