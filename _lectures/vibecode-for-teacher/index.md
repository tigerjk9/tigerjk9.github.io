---
title: "바이브 코딩 신간 — 교사를 위한 웹앱 만들기 (정리본)"
layout: lecture
permalink: /lectures/vibecode-for-teacher/
date: 2026-07-21
author_profile: false
toc: true
toc_sticky: true
header:
  teaser: /assets/lectures/books/book-08-cover.jpg
  og_image: /assets/lectures/books/book-08-cover.jpg
---

한빛미디어에서 출간 예정인 바이브 코딩 신간의 조판원고를 큐레이션한 정리본이다. 이 책은 코드를 직접 쓰지 않고도 교실의 불편함을 웹앱으로 해결하는 과정을, 문제 발견부터 로컬 개발·배포까지 한 흐름으로 담았다. 정식 서명은 아직 확정되지 않았으며, 아래는 4부 8장과 부록의 구성·핵심 내용·실습을 요약한 것이다. 원문 전체는 싣지 않는다.

## 도서 개요

| 항목 | 내용 |
|------|------|
| 저자 | 이상선 · 김진관 · 김상섭 · 이대형 · 윤신영 (공저) |
| 출판사 | 한빛미디어 |
| 대상 | 코딩 경험이 없는 교사·비개발자 |
| 구성 | 4부 8장 + 부록 |
| 핵심 흐름 | 문제 발견(PRD·MVP) → 외부 연결(API·AI) → 클라우드 저장(Supabase) → 로컬 개발·배포(Antigravity·Git·Vercel) |
| 주요 도구 | Lovable · Google AI Studio · Supabase · Google Antigravity IDE · GitHub · Vercel |
| 실습 저장소 | [github.com/lifeofpi-ux/vibecode-for-teacher](https://github.com/lifeofpi-ux/vibecode-for-teacher){:target="_blank"} |

## 함께 보는 실습 저장소

이 책의 예제 코드와 실습 자료는 아래 GitHub 저장소에서 함께 제공된다. 각 장에서 만드는 앱의 프롬프트·코드·설정을 순서대로 따라 할 수 있다.

- **[vibecode-for-teacher · GitHub 저장소](https://github.com/lifeofpi-ux/vibecode-for-teacher){:target="_blank"}**

## 목차

**PART 01. 문제 발견 — 내 불편함이 앱이 되기까지**
- 1장 모든 아이디어는 교실에서 시작된다
- 2장 브라우저에서 동작하는 나의 첫 프로그램
- 3장 AI와 함께 만드는 첫 웹 서비스, 러버블과 웹앱의 개념

**PART 02. 앱에 지식을 더하다 — 고립된 섬에서 연결된 대륙으로**
- 4장 서비스는 혼자가 아니야 (API 연동)
- 5장 눈과 귀, 생각을 가진 AI 웹앱 만들기 (웹캠·마이크 활용)

**PART 03. 앱에 클라우드 기능을 심다 — 앱에 날개 달기**
- 6장 왜 데이터베이스가 필요할까요?

**PART 04. 로컬환경에서 진짜 개발자처럼 일하기**
- 7장 내 컴퓨터를 리액트 개발 서버로 만들기
- 8장 개발부터 배포까지 모든 것을 내가 직접
- 부록 그 밖의 인공지능 도구들 (Cursor · Claude Code)

## 파트별 핵심 요약

### PART 01. 문제 발견

앱 개발의 출발점은 거창한 기획서가 아니라 교사가 매일 겪는 작은 불편함이다. 급식 알리미, 공정성 시비를 없앤 발표자 룰렛, 흩어지던 상담 일지를 데이터로 만드는 기록부, 청소 구역 배정기, 우리 반만의 커스텀 타이머 같은 실제 사례가 그 씨앗을 보여준다. 서술형 답안 200장을 채점하며 '반복의 늪'과 '디지털 역설'에 빠진 혜심 선생님 이야기를 통해, 불편함을 입력·판단·출력의 문제로 차갑게 정의하는 법을 익힌다.

핵심 원칙은 "바이브 코딩을 위한 바이브 코딩은 하지 말라"이다. 기술 자체가 아니라 교사의 삶을 실제로 개선하는 도구를 만드는 것이 목적이며, 좋은 문제일수록 구체적이다. 이 구체화를 돕는 장치로 ADDIE 모형, 사용자 스토리, 기능의 삼총사(입력–처리–출력), MVP(최소 기능 제품), 그리고 한 장짜리 PRD 템플릿을 제시한다. 교사는 무엇을 왜 만들지 정하는 PM이 되고, AI는 그것을 구현하는 개발자가 된다.

2장은 이 설계도를 실제로 움직이는 프로그램으로 바꾼다. '출석 체크' 앱을 프롬프트만으로 만들며 웹의 삼총사인 HTML(구조)·CSS(스타일)·JavaScript(동작)를 이해하고, 바닐라의 의미, 새로고침해도 사라지지 않는 로컬 스토리지, React와 라이브러리·프레임워크의 차이, NextJS까지 개념을 넓힌다. 3장은 AI 웹앱 빌더 러버블(Lovable)로 '글쓰기 타임라인 SNS'라는 풀스택 서비스를 만들며 프론트엔드·백엔드·데이터베이스·배포·풀스택을 식당(홀·주방·창고·개업·오너 셰프)에 비유해 설명하고, CSR(React)과 SSR(NextJS)의 차이, SEO까지 짚는다.

### PART 02. 앱에 지식을 더하다

혼자 뚝딱거리던 앱을 세상의 데이터·지능과 연결하는 파트다. 4장은 API를 '내 앱이 외부 서비스에 정보를 달라고 말을 거는 통로'로 정의하고, 생성형 AI 개발의 베이스캠프인 Google AI Studio의 Build·App Gallery·Remix를 익힌다. JSON 구조를 읽는 눈, 오픈 API와 명세서를 찾는 법을 배운 뒤 NEIS 오픈 API를 연결해 매일 아침 자동으로 갱신되는 급식 메뉴 앱을 만든다. REST API와 API Key의 개념도 이 과정에서 자연스럽게 잡힌다.

5장은 앱에 눈과 귀, 생각을 심는다. 웹캠·마이크를 활용한 실시간 사물 인식 영어 학습 앱(Snap & Learn English)을 PRD에서 프롬프트, 제작까지 완성하고, AI 글쓰기 튜터에 OCR 기능을 더한다. 나아가 메타 프롬프팅으로 프롬프트를 고도화하고, 엔드포인트와 모델(OpenAI·Gemini), 온도(Temperature)와 최대 토큰 설정을 다루며, 배포 시 API 키 노출·통신 속도 제한·과금·개인정보 보호 같은 실무 유의점까지 정리한다.

### PART 03. 앱에 클라우드 기능을 심다

프론트엔드 위주였던 앱에 영구적인 기억력을 부여하는 파트다. 새로고침 한 번에 데이터가 사라지는 이유를 메모리(RAM)와 변수·상태 개념으로 설명하고, 지워지지 않는 '디지털 서랍장'인 데이터베이스와 그 4대 작동 원리(CRUD)를 이해시킨다. 서버 없이 백엔드를 빌려 쓰는 BaaS를 '공유 주방'에 비유하며 Airtable·Firebase·Supabase를 비교하고, 최종 선택인 Supabase로 실제 데이터가 오가는 앱을 만든다.

실습에서는 Supabase 프로젝트를 개설해 API 키를 발급받고, 복잡한 SQL 쿼리는 AI Studio에 맡겨 데이터를 실시간으로 저장·조회한다. 이어서 Supabase의 가장 강력한 무기인 Auth(사용자 인증)와 RLS(행 수준 보안)를 설정해 허락받은 사람만 접근하는 안전한 앱으로 발전시킨다. 마지막으로 규칙에 깐깐한 관계형 데이터베이스(RDBMS)와 유연한 NoSQL을 비교하며 어떤 앱에 어떤 구조가 맞는지 탐구한다.

### PART 04. 로컬환경에서 진짜 개발자처럼 일하기

남의 공유 오피스(웹 도구)에서 나와 내 컴퓨터에 개인 스튜디오를 차리는 파트다. 인터넷이 끊기거나 서비스가 유료로 바뀌어도 흔들리지 않는 로컬 개발 환경의 필요성을 짚고, VS Code 계보(Cursor·Windsurf·Antigravity) 안에서 이 책의 메인 도구인 Google Antigravity IDE(2.0, Agent-First)를 선택한 이유를 설명한다. localhost와 포트의 원리, Node.js 설치, Vite로 리액트 프로젝트 만들기, npm install과 npm run dev, Hot Reload 체험을 거쳐 '우리 반 실시간 칭찬 보드'를 만든다. 환경변수와 .env로 비밀 키를 안전하게 관리하는 법도 함께 배운다.

8장은 개발부터 배포까지 전 과정을 스스로 통제하게 한다. Git·GitHub·GitHub Desktop의 차이를 정리하고 커밋·푸시·풀 세 가지로 버전 관리를 익히며, 실수했을 때 과거로 되돌리는 법을 실습한다. 이어 Vercel에 GitHub를 연결하고 환경변수를 설정해 배포하며, 코드를 고치면 자동으로 반영되는 CI/CD의 마법을 경험한다. 부록에서는 Cursor와 Claude Code를 로컬에 설치·실행하는 법을 안내해 다른 AI 개발 도구로 확장할 길을 연다.

## 이 책에서 직접 만들어 보는 것

| 장 | 실습 결과물 | 핵심 도구 |
|----|------------|-----------|
| 1장 | 나만의 1페이지 PRD 초안 | PRD 템플릿 |
| 2장 | 출석 체크 웹앱 | 바닐라 JS · 로컬 스토리지 |
| 3장 | 글쓰기 타임라인 SNS (풀스택) | Lovable · Supabase |
| 4장 | 급식 메뉴 조회 앱 | NEIS 오픈 API · Google AI Studio |
| 5장 | 실시간 사물 인식 영어 학습 앱 | 웹캠 · Gemini |
| 5장 | AI 글쓰기 튜터 (+ OCR) | Google AI Studio |
| 6장 | 클라우드 To-Do 앱 (보안 적용) | Supabase · Auth · RLS |
| 7장 | 우리 반 실시간 칭찬 보드 | Antigravity IDE · Vite · React |
| 8장 | GitHub 버전 관리 + Vercel 배포 | GitHub Desktop · Vercel · CI/CD |
| 부록 | 로컬 AI 개발 도구 세팅 | Cursor · Claude Code |

## 등장하는 도구·서비스

| 분류 | 도구 |
|------|------|
| AI 웹앱 빌더 | Lovable(러버블) |
| AI 개발·멀티모달 | Google AI Studio(Gemini) · OpenAI API |
| 백엔드·데이터(BaaS) | Supabase · Firebase · Airtable |
| 공공 데이터 | NEIS 오픈 API |
| 로컬 개발 | Google Antigravity IDE(2.0) · Cursor · Windsurf · VS Code · Node.js · Vite · npm |
| 버전 관리·배포 | Git · GitHub · GitHub Desktop · Vercel |
| 핵심 개념 | PRD · MVP · HTML/CSS/JS · React/NextJS · CSR/SSR · SEO · REST API · JSON · API Key · CRUD · RLS · 환경변수(.env) · CI/CD |

## 정리

이 책은 교사가 코드를 배우지 않고도 교실의 문제를 스스로 웹앱으로 풀어내는 전 과정을 다룬다. 문제를 정의하는 PRD에서 시작해, 외부 데이터와 AI를 연결하고, 클라우드에 데이터를 저장하고, 마침내 내 컴퓨터에서 진짜 개발자처럼 배포하기까지의 흐름이 하나로 이어진다. 각 장의 실습은 위 GitHub 저장소에서 코드와 함께 따라 할 수 있다.

> 이 페이지는 한빛미디어 출간 예정 원고의 구성과 내용을 요약·정리한 큐레이션 자료다. 원문 전체(조판원고)와 도서 내 이미지는 포함하지 않는다.
