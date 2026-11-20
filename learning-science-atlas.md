---
layout: wide
title: "학습과학 아틀라스"
permalink: /learning-science-atlas/
class: "page--lsa"
description: "인지부하이론, 정보처리이론, 인지심리학, 체화된 인지에서 뇌과학과 AI까지, 학습과학 연구 162편의 계보와 영향을 3D로 탐색하는 지도. 투어 10개, 개념 사전 70개, 경로 찾기, 인출 연습 퀴즈."
header:
  og_image: /assets/learning-science-atlas-teaser.jpg
---

<style>
  html, body.page--lsa { background: #05070d !important; overflow: hidden; margin: 0; padding: 0; }
  .page--lsa .page__inner-wrap, .page--lsa #main, .page--lsa .page__content { margin: 0 !important; padding: 0 !important; max-width: none !important; width: 100% !important; }
  .page--lsa .page__footer, .page--lsa .page__title, .page--lsa .page__meta, .page--lsa .page__share, .page--lsa .sidebar, .page--lsa .page__related { display: none !important; }
  #lsa-frame { display: block; width: 100vw; height: calc(100dvh - var(--lsa-top, 70px)); border: 0; background: #05070d; }
  #lsa-noscript { color: #cbd5e1; padding: 24px; }
</style>

<iframe id="lsa-frame" src="/tools/learning-science-atlas/?inblog=1" title="학습과학 아틀라스, 학습과학 연구 162편의 3D 계보 지도" allow="clipboard-write; fullscreen" allowfullscreen></iframe>
<noscript><p id="lsa-noscript">학습과학 아틀라스는 자바스크립트가 필요합니다. <a href="/tools/learning-science-atlas/?text=1">텍스트 버전</a>이나 <a href="/post/learning-science-atlas/">소개 글</a>을 이용해 주세요.</p></noscript>

<script>
(function () {
  function fit() {
    var f = document.getElementById('lsa-frame'); if (!f) return;
    var top = Math.max(0, Math.round(f.getBoundingClientRect().top + window.scrollY));
    document.documentElement.style.setProperty('--lsa-top', top + 'px');
  }
  window.addEventListener('load', fit); window.addEventListener('resize', fit); fit();
  // 공유 링크(#연구ID, ?tour= 등)를 지도 안으로 전달
  var f = document.getElementById('lsa-frame');
  var qs = location.search ? location.search.replace(/^\?/, '&') : '';
  if (qs || location.hash) f.src = '/tools/learning-science-atlas/?inblog=1' + qs + location.hash;
})();
</script>
