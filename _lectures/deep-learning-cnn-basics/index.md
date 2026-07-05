---
title: "딥러닝의 기초 — 합성곱 신경망을 중심으로"
layout: lecture
permalink: /lectures/deep-learning-cnn-basics/
date: 2026-07-05
author_profile: false
toc: true
toc_sticky: true
header:
  teaser: /assets/lectures/deep-learning-cnn-basics/cover.jpg
  og_image: /assets/lectures/deep-learning-cnn-basics/cover.jpg
---

인공지능이 무엇인지부터 합성곱 신경망(CNN)으로 이미지를 분류하는 원리까지, 딥러닝의 기초를 한 흐름으로 정리한 교원 연수 교재다. 개념과 역사에서 출발해 인공신경망의 학습 원리를 거쳐 CNN 구조와 실습, 성능 개선까지 89쪽·4개 차시로 이어진다. 교재 전체는 아래에서 PDF로 내려받을 수 있고, 주요 지면은 그 아래 미리보기에서 확인할 수 있다.

## 강의 개요

| 항목 | 내용 |
|------|------|
| 저자 | 김진관 |
| 원자료 | 2022년 금요 교육 프로그램 Ⅰ 정보중급과정 교재 |
| 대상 | 인공지능·딥러닝 입문자, 정보 교과 교사 |
| 분량 | 89쪽 · 4개 차시 |
| 실습 도구 | 파이썬 · 케라스(Keras) 기반 이미지 분류 실습 포함 |
| 다루는 개념 | 퍼셉트론 · 활성화 함수 · 역전파 · 합성곱·풀링 · CNN · 하이퍼파라미터 튜닝 |

## 자료 내려받기

- **[교재 전체 내려받기 (PDF · 89쪽 · 약 6.6MB)](/assets/lectures/deep-learning-cnn-basics/manual.pdf){:target="_blank"}**

## 교재 구성

네 개 차시가 인공지능의 개념에서 CNN 실습, 성능 개선까지 단계적으로 이어진다.

| 차시 | 제목 | 핵심 내용 |
|------|------|----------|
| 15 | 인공지능 개요 | AI 개념·역사, 머신러닝의 종류, 퍼셉트론으로 본 신경망 원리, 머신러닝·딥러닝 비교 |
| 16 | 딥러닝과 인공신경망 | 활성화 함수(계단·시그모이드·tanh·ReLU), 오차 함수, 경사 하강법, 역전파 |
| 17 | 합성곱 신경망 | CNN 구조, 합성곱·커널·필터·특징 맵·풀링, 이미지 분류 실습, 드롭아웃, 컬러 이미지 프로젝트 |
| 18 | 하이퍼파라미터 튜닝 | 성능 지표, 데이터 분할·전처리, 모델 평가, 최적화·조기 종료·규제화·배치 정규화 |

## 인공지능 개요

인공지능의 개념을 정의에서 출발한다. 인공지능은 '지능을 가진 컴퓨터'를 뜻하지만, 단순 계산기와 달리 사람이 알려준 것 이상을 스스로 판단할 수 있어야 한다. 강인공지능과 약인공지능을 구분하고, 현재의 인공지능은 특정 목적을 수행하는 약인공지능임을 짚는다. 역사는 1956년 다트머스 회의에서 시작해 1세대 대화형 컴퓨터(엘리자, 튜링 테스트, 중국어 방), 2세대 전문가 시스템, 3세대 머신러닝·딥러닝으로 이어진다. 머신러닝은 지도학습·비지도학습·강화학습으로 나뉜다. 퍼셉트론(로젠블랫, 1957)으로 인공신경망의 원리를 설명하며, 단층 퍼셉트론의 한계(XOR 문제)와 다층 퍼셉트론, 두 번의 인공지능 겨울, 그리고 역전파와 ReLU로 이룬 극복까지 다룬다. 마지막으로 딥러닝의 장단점, 머신러닝과 딥러닝의 비교, 인공지능·머신러닝·딥러닝의 포함 관계를 정리한다.

## 딥러닝과 인공신경망

신경망 학습의 핵심 원리를 다룬다. 먼저 여러 활성화 함수를 비교한다. 계단 함수에서 시그모이드로, 다시 은닉층에서 더 나은 성능을 내는 tanh와 현재 널리 쓰이는 ReLU, 그 변종인 Leaky ReLU까지 각 함수의 출력 범위와 장단점을 그래프로 설명한다. 이어 오차(손실) 함수로 신경망의 성능을 측정하고, 경사 하강법으로 오차가 작아지는 방향으로 가중치를 수정하는 과정을 다룬다. 배치 경사 하강법과 확률적 경사 하강법을 비교하고, 다층 신경망의 가중치를 조정하는 역전파 알고리즘으로 학습 원리를 마무리한다.

## 합성곱 신경망

교재의 중심 주제다. 다층 퍼셉트론으로 이미지를 분류할 때의 한계에서 출발해, 2차원 이미지를 그대로 입력받는 합성곱 신경망의 구조(입력층·합성곱층·전결합층·출력층)를 제시한다. 합성곱층에서 특징을 추출하고 전결합층에서 분류하는 전체 흐름을 손글씨 숫자 예시로 보여준다. 기본 요소로 합성곱 연산, 커널(필터)과 특징 맵, 모서리 탐지 커널의 계산 예시, 필터 수와 출력 깊이의 관계, 회색조와 컬러 이미지의 계산 복잡도 차이, 풀링을 다룬다. 이어 CNN으로 이미지를 분류하는 실습, 과적합을 막는 드롭아웃층 추가, 컬러 이미지 분류 프로젝트로 이어진다.

## 하이퍼파라미터 튜닝

모델의 성능을 측정하고 끌어올리는 방법을 다룬다. 정확도 같은 성능 지표의 개념에서 시작해, 베이스라인 모델을 세우고 훈련·검증·테스트 데이터를 나눈다(80:20, 60:20:20 등). 회색조 변환·크기 조절·정규화 같은 전처리를 적용하고, 모델을 평가한 뒤 성능 지표를 해석한다. 이어 하이퍼파라미터 튜닝으로 성능을 개선하며, 최적화 알고리즘, 조기 종료, 규제화 기법, 배치 정규화를 차례로 다루고 이미지 분류 정확도 개선 프로젝트로 마무리한다. 실습은 파이썬 케라스 코드로 진행된다.

## 주요 지면 미리보기

각 지면을 누르면 크게 볼 수 있다. 교재 전체는 위 PDF에 담겨 있다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p05.jpg" alt="본문 5쪽 — 튜링 테스트와 중국어 방">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p18.jpg" alt="본문 18쪽 — 활성화 함수 그래프">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p42.jpg" alt="본문 42쪽 — 신경망의 특징 추출 과정">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p46.jpg" alt="본문 46쪽 — 합성곱 연산과 모서리 탐지 커널">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p62.jpg" alt="본문 62쪽 — 컬러 이미지의 합성곱">
<img loading="lazy" src="/assets/lectures/deep-learning-cnn-basics/pages/p74.jpg" alt="본문 74쪽 — 데이터 분할과 정규화">
</div>

## 참고와 출처

- 저자: 김진관
- 원자료: 2022년 금요 교육 프로그램 Ⅰ 정보중급과정 교재 (인공지능 개요 · 딥러닝과 인공신경망 · 합성곱 신경망 · 하이퍼파라미터 튜닝)
- 형식: 89쪽 A4 교재 · 파이썬 케라스 실습 포함

<script>
(function(){
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.slide-gallery img'));
  if(!imgs.length) return;
  var ov = document.createElement('div');
  ov.className = 'slb-overlay';
  ov.innerHTML =
    '<button class="slb-close" aria-label="닫기">×</button>' +
    '<button class="slb-prev" aria-label="이전 지면">‹</button>' +
    '<img alt="확대 지면">' +
    '<button class="slb-next" aria-label="다음 지면">›</button>' +
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
