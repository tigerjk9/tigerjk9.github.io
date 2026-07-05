---
title: "퍼셉트론으로 살펴보는 인공신경망(딥러닝)의 원리"
layout: lecture
permalink: /lectures/perceptron-neural-network/
date: 2022-10-06
author_profile: false
toc: true
toc_sticky: true
header:
  teaser: /assets/lectures/perceptron-neural-network/cover.jpg
  og_image: /assets/lectures/perceptron-neural-network/cover.jpg
---

인공신경망은 어디에서 왔고 어떻게 학습하는가. 이 강의는 딥러닝의 가장 작은 단위인 퍼셉트론에서 출발해, 신경망이 학습하는 원리를 그림 한 장씩으로 풀어낸다. 슬라이드 43장 전체를 아래 PDF로 내려받을 수 있고, 그 아래 갤러리에서 바로 넘겨볼 수 있다.

## 강의 개요

| 항목 | 내용 |
|------|------|
| 강사 | 김진관 (닷커넥터) |
| 제작일 | 2022-10-06 |
| 대상 | 인공지능·딥러닝 입문자, 정보 교과 교사 |
| 분량 | 슬라이드 43장 |
| 핵심 개념 | 퍼셉트론 · 가중합 · 활성화 함수 · 가중치 학습 · 다층 퍼셉트론 · XOR |

## 자료 내려받기

- **[슬라이드 전체 내려받기 (PDF · 43장 · 약 2.6MB)](/assets/lectures/perceptron-neural-network/slides.pdf){:target="_blank"}**

## 강의 내용

인공신경망의 뿌리는 생물의 자기 제어 원리를 기계 장치에 적용하려던 사이버네틱스와 생물학적 뉴런에 있다. 여기서 착안한 퍼셉트론은 프랭크 로젠블랫이 제안한 신경망의 기본 단위다. 퍼셉트론은 여러 입력에 각각 가중치를 곱해 더한 값, 곧 가중합(z = Σ xᵢwᵢ + b, b는 바이어스)을 구하고, 이 값을 활성화 함수에 통과시켜 출력을 낸다.

이 강의가 거듭 강조하는 명제는 하나다. 학습은 가중치의 값을 조정하는 것이다. 신경망의 학습은 네 단계로 돌아간다. 먼저 입력에서 출력으로 순방향 계산을 하고, 손실 함수로 예측값과 실제값의 오차를 구하며, 그 오차에 따라 가중치를 조정하고, 이 과정을 반복한다. 강의는 가중치를 볼륨 손잡이에 빗댄다. 손잡이를 조금씩 돌려 오차를 줄여 가는 것이 학습의 실체다.

하나의 퍼셉트론은 직선 하나로 나눌 수 있는 문제만 풀 수 있어, XOR처럼 직선으로 가를 수 없는 문제 앞에서 멈춘다. 이 한계는 은닉층을 더한 다층 퍼셉트론이 해결한다. 럼멜하트와 매클렐런드의 병렬 분산 처리(Parallel Distributed Processing) 연구가 보여주듯, 입력층과 출력층 사이에 은닉층을 두면 XOR 같은 비선형 문제도 풀 수 있다. 인공지능은 병렬적이고 분산된 처리를 해야 한다는 관점이 그 바탕에 있다.

## 슬라이드

각 슬라이드를 누르면 크게 볼 수 있고, 좌우 화살표나 키보드로 넘긴다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p001.jpg" alt="슬라이드 1">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p002.jpg" alt="슬라이드 2">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p003.jpg" alt="슬라이드 3">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p004.jpg" alt="슬라이드 4">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p005.jpg" alt="슬라이드 5">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p006.jpg" alt="슬라이드 6">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p007.jpg" alt="슬라이드 7">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p008.jpg" alt="슬라이드 8">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p009.jpg" alt="슬라이드 9">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p010.jpg" alt="슬라이드 10">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p011.jpg" alt="슬라이드 11">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p012.jpg" alt="슬라이드 12">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p013.jpg" alt="슬라이드 13">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p014.jpg" alt="슬라이드 14">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p015.jpg" alt="슬라이드 15">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p016.jpg" alt="슬라이드 16">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p017.jpg" alt="슬라이드 17">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p018.jpg" alt="슬라이드 18">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p019.jpg" alt="슬라이드 19">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p020.jpg" alt="슬라이드 20">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p021.jpg" alt="슬라이드 21">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p022.jpg" alt="슬라이드 22">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p023.jpg" alt="슬라이드 23">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p024.jpg" alt="슬라이드 24">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p025.jpg" alt="슬라이드 25">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p026.jpg" alt="슬라이드 26">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p027.jpg" alt="슬라이드 27">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p028.jpg" alt="슬라이드 28">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p029.jpg" alt="슬라이드 29">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p030.jpg" alt="슬라이드 30">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p031.jpg" alt="슬라이드 31">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p032.jpg" alt="슬라이드 32">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p033.jpg" alt="슬라이드 33">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p034.jpg" alt="슬라이드 34">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p035.jpg" alt="슬라이드 35">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p036.jpg" alt="슬라이드 36">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p037.jpg" alt="슬라이드 37">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p038.jpg" alt="슬라이드 38">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p039.jpg" alt="슬라이드 39">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p040.jpg" alt="슬라이드 40">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p041.jpg" alt="슬라이드 41">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p042.jpg" alt="슬라이드 42">
<img loading="lazy" src="/assets/lectures/perceptron-neural-network/slides/p043.jpg" alt="슬라이드 43">
</div>

## 참고와 출처

- 강사: 김진관 (닷커넥터)
- 제작일: 2022-10-06 · 슬라이드 43장(16:9)
- 주요 인용: David E. Rumelhart & James L. McClelland, 《Parallel Distributed Processing》

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
