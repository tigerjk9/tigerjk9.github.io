---
title: "업무는 빠르게, 배움은 느리게"
layout: lecture
permalink: /lectures/work-fast-learn-slow/
sitemap: false
noindex: true
date: 2026-11-24
author_profile: false
toc: true
toc_sticky: true
description: "2026 수업 나눔 토크 콘서트에서 'AI-교사 협업'을 주제로 한 10분 발표의 슬라이드 16장과 발표 대본을 내려받는다. 업무와 수업에 정반대의 기준을 두는 까닭을 학사일정 편성과 6학년 과학 전자석 학습지 사례로 풀었다."
header:
  teaser: /assets/lectures/work-fast-learn-slow/cover.jpg
  og_image: /assets/lectures/work-fast-learn-slow/cover.jpg
---

2026 수업 나눔 토크 콘서트에서 'AI-교사 협업'이라는 주제를 받아 10분 동안 발표한 자료다. 발표 슬라이드 16장과 발표 대본을 함께 둔다. 발표는 학교에서 누구보다 AI를 많이 쓰는 교사가 왜 수업 40분 가운데 20분은 AI를 끄는지에서 출발한다. 업무에는 "이거, 더 빨리 할 수 없나?"를, 수업에는 "이 아이가 지금 충분히 헤매고 있나?"를 묻는 두 기준을 2027학년도 학사일정 편성과 6학년 과학 전자석 학습지로 보여 주고, AI로 아낀 시간이 저절로 아이들에게 가지 않는다는 이야기로 이어 간다.

## 자료 개요

| 항목 | 내용 |
|------|------|
| 발표 | 김진관 (대전둔천초등학교 교사, 닷커넥터) |
| 자리 | 2026 수업 나눔 토크 콘서트, 주제 'AI-교사 협업' |
| 길이 | 10분 (대본의 시간 구간 0:00~10:00 기준) |
| 업무 사례 | 2027학년도 학사일정과 시수 편성 |
| 수업 사례 | 6학년 과학 생활 속 전자석 학습지, 다음 단원 전기 안전·절약 학습지 |
| 분량 | 발표 슬라이드 PDF 16장 (0.8MB), 발표 대본 PDF 5쪽 (0.4MB) |

## 자료 내려받기

내려받기 버튼을 누르면 원본 파일 이름 그대로 저장된다. 미리보기는 버튼을 눌렀을 때에만 PDF를 불러오며, PDF를 그릴 수 있는 데스크톱 브라우저에서 열린다. 모바일에서는 내려받아 열면 된다.

### 발표 슬라이드

<div class="gyoan-actions">
  <a class="gyoan-btn gyoan-btn--download" href="/assets/lectures/work-fast-learn-slow/work-fast-learn-slow-slides.pdf" download="AI-교사 협업_김진관.pdf"><i class="fas fa-download" aria-hidden="true"></i> 슬라이드 내려받기 <span class="gyoan-btn__meta">PDF · 16장 · 0.8MB</span></a>
  <button type="button" class="gyoan-btn gyoan-btn--preview" data-preview="slides-preview"><i class="fas fa-eye" aria-hidden="true"></i> <span class="gyoan-btn__label">미리보기 열기</span></button>
</div>

<div id="slides-preview" class="gyoan-preview-slot" data-pdf="/assets/lectures/work-fast-learn-slow/work-fast-learn-slow-slides.pdf"></div>

슬라이드는 대본의 열여섯 구간과 한 장씩 짝을 이룬다. 6~9번 화면에는 아이들이 직접 쓴 학습지 사진이, 10번 화면에는 그 결과를 보고 고친 다음 단원 학습지 일부가 들어 있다.

### 발표 대본

<div class="gyoan-actions">
  <a class="gyoan-btn gyoan-btn--download" href="/assets/lectures/work-fast-learn-slow/work-fast-learn-slow-script.pdf" download="AI-교사 협업_발표대본_김진관.pdf"><i class="fas fa-download" aria-hidden="true"></i> 대본 내려받기 <span class="gyoan-btn__meta">PDF · 5쪽 · 0.4MB</span></a>
  <button type="button" class="gyoan-btn gyoan-btn--preview" data-preview="script-preview"><i class="fas fa-eye" aria-hidden="true"></i> <span class="gyoan-btn__label">미리보기 열기</span></button>
</div>

<div id="script-preview" class="gyoan-preview-slot" data-pdf="/assets/lectures/work-fast-learn-slow/work-fast-learn-slow-script.pdf"></div>

화면 번호와 시간 구간을 붙여 열여섯 구간으로 나눈 대본이다. 슬라이드와 나란히 펴 두면 화면마다 어떤 말을 했는지 따라갈 수 있다.

<script>
(function () {
  document.querySelectorAll('.gyoan-btn--preview[data-preview]').forEach(function (btn) {
    var slot = document.getElementById(btn.getAttribute('data-preview'));
    if (!slot) return;
    btn.addEventListener('click', function () {
      var open = slot.classList.toggle('open');
      btn.querySelector('.gyoan-btn__label').textContent = open ? '미리보기 닫기' : '미리보기 열기';
      // iframe을 클릭 시점에 만들어야 모바일 브라우저가 페이지 진입만으로 PDF 다운로드를 시작하지 않는다
      if (open) {
        if (!slot.querySelector('iframe')) {
          var f = document.createElement('iframe');
          f.src = slot.getAttribute('data-pdf') + '#view=FitH';
          f.title = 'PDF 미리보기';
          slot.appendChild(f);
        }
        slot.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        // 닫을 때 뷰어를 비워 두면 숨은 PDF가 메모리를 쥐지 않고, 다시 열 때 첫 쪽부터 시작한다
        slot.innerHTML = '';
      }
    });
  });
})();
</script>

## 발표 흐름

대본의 시간 구간을 따라 정리했다.

| 화면 | 시간 | 제목 | 담은 내용 |
|:----:|------|------|----------|
| 1 | 0:00~0:10 | 소개 | 발표자 소개 |
| 2 | 0:10~1:00 | 40분 중 20분, AI를 껐습니다 | 수업 40분 가운데 한가운데 20분 동안 태블릿을 덮고 다시 연필을 쥐여 준 이야기로 연다 |
| 3 | 1:00~2:30 | 업무는 빠르게, 배움은 느리게 | 업무의 마찰은 낭비이고 배움의 마찰은 성장의 재료다. 학습과학이 바람직한 어려움(Bjork, 1994)이라 부르는 불편함 |
| 4 | 2:30~4:00 | 계산은 AI에게, 원칙은 교사에게 | 수업일수 191일, 조리실 공사 기간 50일, 전 학년 시수 편차 0, 서로 맞춘 문서 5종은 AI가 계산했다. 저학년부터 차례로 하교, 수요일은 4교시로 줄이지 않기, 1·2학년은 매일 같은 시각에 하교라는 원칙은 교사가 세웠다 |
| 5 | 4:00~4:40 | 내 생각 먼저, AI는 그다음 | 6학년 과학 전자석 학습지의 다섯 칸. 내 생각 먼저, 질문 다듬기, 기준으로 확인, 받아들일지 판단, 내 말로 정리 |
| 6 | 4:40~5:05 | 같은 AI의 말, 다른 판정 | 학습지 첫머리에 일부러 넣은 틀린 답 "냉장고 문에 붙이는 자석도 전자석입니다"를 두고 한 아이는 틀리다, 다른 아이는 맞다고 썼다 |
| 7 | 5:05~5:20 | 가장 위험한 아이 | 모르는 아이가 아니라 근거를 끌어다 AI의 말에 맞춰 주는 아이. 확인 없이 AI에게 판단을 넘기는 인지적 항복(Shaw & Nave) |
| 8 | 5:20~5:35 | 묻는 힘은 금방 자랐습니다 | 한 차시 만에 "전자석 알려 줘"가 대상, 범위, 개수, 이유가 담긴 질문으로 바뀌었다 |
| 9 | 5:35~5:45 | 의심하는 힘은 아직 자라는 중입니다 | 확인 칸의 판정은 모두 ○, 확인 방법은 네 줄 모두 인터넷 검색이었다 |
| 10 | 5:45~6:00 | 그래서 학습지를 고쳤습니다 | 검색 말고 다른 확인 방법을 하나 고르게 하고 ○에도 근거를 한 줄 쓰게 했다. 채점은 AI로 빨라질 수 있어도 아이가 왜 그렇게 썼는지 읽어 내는 일은 느려야 한다 |
| 11 | 6:00~6:50 | AI는 일을 줄여주지 않았습니다 | 200명 규모 기술 기업을 8개월 동안 관찰한 UC 버클리 하스 경영대학원 연구진의 하버드비즈니스리뷰 글. AI를 쓰는 사람은 더 빨리, 더 넓게, 더 오래 일했다 |
| 12 | 6:50~7:30 | 아낀 시간은 저절로 아이들에게 가지 않습니다 | 학사일정, 연구학교 신청서, 이 발표 준비가 한꺼번에 몰린 11월. 토대가 없고, 생각이 일찍 멈추고, 아낀 시간은 속도에 흡수된다 |
| 13 | 7:30~8:30 | 멈춤은 먼저 떼어 둔 시간 | 디기아수(디지털 기반 아날로그 수업). 연구진의 처방인 의도적 멈춤, 순서 정하기, 사람의 연결을 가운데 20분 AI 끄기, 내 생각 먼저 쓰기, 짝과 눈 맞추고 말하기로 옮겼다 |
| 14 | 8:30~9:30 | 혼자서는 멈출 수 없습니다 | 한 미술 선생님의 댓글과 "선생님은 어디서 AI를 켰고, 어디서 껐나요?"라는 물음. 대전 AI교육 교사 커뮤니티 AI 티처스쿨로의 초대 |
| 15 | 9:30~9:45 | 고속 기어와 저속 기어 | 업무는 고속 기어로 빠르게, 배움은 저속 기어로 느리게. 기어를 바꾸고 멈출 때를 정하는 손이 필요하다 |
| 16 | 9:45~10:00 | 여전히, 그리고 앞으로도 교실의 답은 교사입니다 | 1788년 노예선 브룩스호 적재 도면. AI의 질문은 얼마나 더 실을까이고, 깨어 있는 사람의 질문은 어떻게 해방시킬까다 |

## 발표가 세운 두 원칙

대본이 원칙이라고 이름 붙인 것은 둘이다. 하나는 같은 도구에 정반대의 기준을 적용하는 것이다. 업무에 느림의 기준을 대면 교사의 야근이 되고, 수업에 빠름의 기준을 대면 아이의 생각을 AI가 대신해 버린다. 다른 하나는 업무에서 아낀 시간이 저절로 아이들에게 가지 않는다는 것이다. 깊은 생각은 시간이 남는다고 생기지 않고 마찰이 있어야 생긴다. 그래서 남는 시간에 멈추는 대신, 수업을 설계할 때 AI를 끄는 20분부터 먼저 정해 둔다.

## 함께 읽을 글

- [AI를 끄는 24분이 지키는 것](/post/ai-off-24-minutes/), 2번 화면이 되짚는 에듀테크 코리아 페어 2026 발표 이야기
- [AI가 아껴준 시간은 고차원적 사고로 이어지고 있을까?](/post/ai-saved-time-higher-order-thinking/), 12번 화면이 출처로 든 글
- [AI와 협업, 인간은 왜 '인지적 항복'을 하는가?](/post/the-rise-of-cognitive-surrender/), 7번 화면이 인용한 인지적 항복
- [AI는 바람직한 어려움과 스캐폴딩의 균형을 찾을 수 있을까?](/post/desirable-difficulties-scaffolding/), 3번 화면의 바람직한 어려움

## 출처

- 김진관 (2026). 『업무는 빠르게, 배움은 느리게』 발표 슬라이드와 발표 대본. 2026 수업 나눔 토크 콘서트, AI-교사 협업.
- 발표가 인용한 자료. Bjork (1994), 바람직한 어려움. Shaw & Nave(와튼스쿨), 인지적 항복. Ranganathan, A. & Ye, X. M. (2026). AI Doesn't Reduce Work—It Intensifies It. *Harvard Business Review*. 김진관 (2026. 11. 7.). AI가 아껴준 시간은 고차원적 사고로 이어지고 있을까? 페이스북.
