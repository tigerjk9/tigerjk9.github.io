---
title: "바이브 코딩을 위한 Git & GitHub 완벽 가이드"
layout: lecture
permalink: /lectures/vibe-coding-git-github/
date: 2026-05-09
author_profile: false
toc: true
toc_sticky: true
header:
  teaser: /assets/lectures/vibe-coding-git-github/cover.jpg
  og_image: /assets/lectures/vibe-coding-git-github/cover.jpg
---

AI에게 자연어로 지시해 소프트웨어를 만드는 바이브 코딩에서, 결과물의 품질은 감이 아니라 세 가지 체계가 좌우한다. 무엇을 만들지 정의하는 PRD, 어떻게 지시할지 다듬는 프롬프트, 어떤 맥락을 넘겨줄지 관리하는 컨텍스트다. 이 세미나는 그 원리를 먼저 세운 뒤, 코드를 안전하게 쌓아 올리는 도구인 Git과 GitHub를 비전공자도 따라 할 수 있게 처음부터 짚는다. 슬라이드 40장 전체를 아래 PDF로 내려받을 수 있고, 주요 슬라이드는 그 아래 갤러리에서 바로 넘겨볼 수 있다.

## 강의 개요

| 항목 | 내용 |
|------|------|
| 강사 | 김진관 (닷커넥터) |
| 주최·형식 | AI Teacher School(AITS) 3rd 교사자율연수 온라인 세미나 · ZOOM 라이브 |
| 일시 | 2026-05-09 (토) 21:00–22:30 (90분) |
| 대상 | 비전공자·초보자를 포함한 교사 및 바이브 코딩 입문자 |
| 분량 | 슬라이드 40장 · 2부 구성(원리 + 실습) |
| 핵심 개념 | PRD · 프롬프트 엔지니어링 · 컨텍스트 엔지니어링 · Git · GitHub |

## 자료 내려받기

- **[슬라이드 전체 내려받기 (PDF · 40장 · 약 4.7MB)](/assets/lectures/vibe-coding-git-github/slides.pdf){:target="_blank"}**

## 1부. 바이브 코딩의 원리

1부는 바이브 코딩을 '운에 맡기는 마법'이 아니라 '체계적인 시스템'으로 다시 정의한다. 그 시스템은 세 축으로 이뤄진다. 개발 목표와 기능을 정의하는 **PRD(제품요구사항 문서)**, 원하는 결과물을 얻도록 지시를 구조화하는 **프롬프트 엔지니어링**, 관련 코드·데이터·환경 설정 같은 맥락을 AI에게 일관되게 공급하는 **컨텍스트 엔지니어링**이다.

프롬프트의 핵심은 구체화다. "퀴즈 앱 만들어줘" 같은 모호한 요청(Bad)은 "4지선다 객관식 퀴즈 앱, 문제은행 20문항, 점수와 정답 피드백 화면을 포함해서 만들어줘"처럼 조건을 명시한 요청(Good)으로 바꿔야 원하는 결과가 나온다.

작업은 한 번에 끝나지 않고 반복과 개선의 순환으로 진행된다. 목표 정의와 지시에서 출발해, 대화 히스토리와 자료를 컨텍스트로 관리하고, 프롬프트와 컨텍스트를 함께 조정하며 결과물을 다듬는다. 이때 세미나가 인용하는 연구가 대화형 AI의 약점을 설명한다. LLM은 대화가 여러 턴 길어질수록 맥락을 잃고 헤매는 경향이 있다(Laban et al., 2025). 대응 전략은 단순하다. 일관성을 잃은 AI와 논쟁하지 말고 대화창을 초기화해, 정리된 PRD와 맥락으로 다시 명확하게 출발하는 것이다. 흐트러진 여러 턴(Multi-Turn Confusion)을 리셋해 한 번의 선명한 지시(Single-Turn Clarity)로 되돌리는 방식이다.

학습은 단계로 쌓인다. 작은 PRD를 써 보는 1단계, 프롬프트를 설계하는 2단계, 컨텍스트를 관리하는 3단계로 나아가며, 바이브 코딩은 결국 인간의 직관을 AI의 연산 능력과 결합해 소프트웨어를 효율적으로 짓는 현대적 공학으로 정리된다. 시스템은 Logic(PRD), Language(프롬프트), Structure(컨텍스트) 세 조각이 맞물려 돌아간다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p001.jpg" alt="슬라이드 1">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p002.jpg" alt="슬라이드 2">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p003.jpg" alt="슬라이드 3">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p004.jpg" alt="슬라이드 4">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p005.jpg" alt="슬라이드 5">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p006.jpg" alt="슬라이드 6">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p007.jpg" alt="슬라이드 7">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p008.jpg" alt="슬라이드 8">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p009.jpg" alt="슬라이드 9">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p010.jpg" alt="슬라이드 10">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p011.jpg" alt="슬라이드 11">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p012.jpg" alt="슬라이드 12">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p013.jpg" alt="슬라이드 13">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p014.jpg" alt="슬라이드 14">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p015.jpg" alt="슬라이드 15">
</div>

## 2부. Git & GitHub 실습

2부는 비전공자와 초보자를 위해 GitHub를 회원가입부터 데스크탑 활용까지 처음부터 따라 하도록 구성한다. 작업의 순서는 다음과 같다.

먼저 Git을 설치한다. Windows는 git-scm.com의 Install 페이지에서 내려받아 설치하고, Git Bash에서 사용자 이름과 이메일을 등록한 뒤 등록이 정상인지 명령어로 확인한다. 이어 GitHub에 가입한다. 이메일·비밀번호·사용자 이름·국가를 입력해 계정을 만들고, 메일로 받은 코드로 인증한 뒤 프로필과 테마를 설정한다. 계정 보안을 위해 2단계 인증(2FA)을 켜고, 명령어 없이도 다룰 수 있도록 GitHub Desktop을 설치한다.

핵심 실습은 세 동작으로 이뤄진 기본 사이클이다. 원격 저장소를 내 컴퓨터로 가져오는 Clone, 변경 사항을 기록하는 Commit, 그 기록을 원격에 올리는 Push다. 이 Clone–Commit–Push 사이클을 익히면 바이브 코딩으로 만든 결과물을 버전으로 안전하게 쌓고 되돌릴 수 있다.

다음 단계는 협업으로 넘어간다. 실험적 작업을 본류와 분리하는 Branch(브랜치), 그 작업을 반영해 달라고 요청하는 Pull Request(PR)로 확장하면, 혼자 만드는 코드를 여럿이 함께 다듬는 흐름으로 나아간다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p017.jpg" alt="슬라이드 17">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p018.jpg" alt="슬라이드 18">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p019.jpg" alt="슬라이드 19">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p020.jpg" alt="슬라이드 20">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p021.jpg" alt="슬라이드 21">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p022.jpg" alt="슬라이드 22">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p023.jpg" alt="슬라이드 23">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p024.jpg" alt="슬라이드 24">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p025.jpg" alt="슬라이드 25">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p026.jpg" alt="슬라이드 26">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p027.jpg" alt="슬라이드 27">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p028.jpg" alt="슬라이드 28">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p029.jpg" alt="슬라이드 29">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p030.jpg" alt="슬라이드 30">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p031.jpg" alt="슬라이드 31">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p032.jpg" alt="슬라이드 32">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p033.jpg" alt="슬라이드 33">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p034.jpg" alt="슬라이드 34">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p035.jpg" alt="슬라이드 35">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p036.jpg" alt="슬라이드 36">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p037.jpg" alt="슬라이드 37">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p038.jpg" alt="슬라이드 38">
<img loading="lazy" src="/assets/lectures/vibe-coding-git-github/slides/p039.jpg" alt="슬라이드 39">
</div>

## 참고와 출처

- 강사: 김진관 (닷커넥터)
- 주최·형식: AI Teacher School(AITS) 3rd 교사자율연수 온라인 세미나 · ZOOM 라이브 · 2026-05-09
- 주요 인용: Laban, P., Hayashi, H., Zhou, Y., & Neville, J. (2025). LLMs Get Lost In Multi-Turn Conversation. arXiv:2505.06120
- Git 설치 참고: [git-scm.com/install/windows](https://git-scm.com/install/windows){:target="_blank"}

<script>
(function(){
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.slide-gallery img'));
  if(!imgs.length) return;
  var ov = document.createElement('div');
  ov.className = 'slb-overlay';
  ov.innerHTML =
    '<button class="slb-close" aria-label="닫기">×</button>' +
    '<button class="slb-prev" aria-label="이전 슬라이드">‹</button>' +
    '<img alt="확대 슬라이드">' +
    '<button class="slb-next" aria-label="다음 슬라이드">›</button>' +
    '<div class="slb-counter"></div>';
  document.body.appendChild(ov);
  var big = ov.querySelector('img'),
      counter = ov.querySelector('.slb-counter'),
      cur = 0;
  function show(i){ cur = (i + imgs.length) % imgs.length; big.src = imgs[cur].src; counter.textContent = (cur + 1) + ' / ' + imgs.length; }
  function open(i){ show(i); ov.classList.add('open'); document.body.style.overflow = 'hidden'; }
  function close(){ ov.classList.remove('open'); document.body.style.overflow = ''; }
  imgs.forEach(function(im, i){ im.addEventListener('click', function(){ open(i); }); });
  ov.querySelector('.slb-close').addEventListener('click', close);
  ov.querySelector('.slb-prev').addEventListener('click', function(e){ e.stopPropagation(); show(cur - 1); });
  ov.querySelector('.slb-next').addEventListener('click', function(e){ e.stopPropagation(); show(cur + 1); });
  ov.addEventListener('click', function(e){ if(e.target === ov) close(); });
  document.addEventListener('keydown', function(e){
    if(!ov.classList.contains('open')) return;
    if(e.key === 'Escape') close();
    else if(e.key === 'ArrowLeft') show(cur - 1);
    else if(e.key === 'ArrowRight') show(cur + 1);
  });
})();
</script>
