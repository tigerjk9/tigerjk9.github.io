---
title: Mobile Feature Parity - tigerjk9.github.io
date: 2026-04-14
status: approved
---

## 목표

PC에서 동작하는 모든 커스텀 기능을 모바일(iOS Safari + Android Chrome)에서 동일하게 작동시킨다.

## 발견된 문제

1. **카테고리 "튕겨나와" 버그**: hits 배지 img가 visible-links 안에 있어 greedy-nav 너비 계산 오염 → 드롭다운이 뷰포트 이탈
2. **테마 토글 모바일 접근 불가**: 사이드바 오버레이(z-index 999)가 masthead(z-index 20)를 덮어버려 theme toggle에 접근 불가
3. **iOS 100vh 버그**: 사이드바가 height:100vh 사용 → iOS Safari 주소창 포함 높이로 계산되어 하단 잘림
4. **라이트 모드 드롭다운 색상 미지정**: hidden-links 드롭다운에 라이트모드 오버라이드 없음

## 변경 파일

### 1. `_includes/masthead.html`
- hits 배지 `<li>`를 `visible-links` 밖으로 분리
- `<a class="masthead-hits">` 독립 요소로 배치

### 2. `assets/js/theme-toggle.js`
- `getElementById('theme-toggle')` → `document.addEventListener('click', e.target.closest('.theme-toggle'))` 이벤트 위임
- 동적 주입된 버튼도 자동 처리

### 3. `assets/js/sidebar-toggle.js`
- `initSidebarToggle()`에 `injectMobileSidebarHeader()` 추가
- 사이드바 상단에 `.sidebar-mobile-header` div 주입 (메뉴 타이틀 + theme-toggle 버튼)
- 데스크톱에서는 CSS로 숨김

### 4. `assets/css/main.scss`
- `.masthead-hits` 스타일 추가
- `@media (max-width: 1023px)`: hidden-links max-width, iOS dvh, 모바일 헤더, 터치 타겟
- light mode dropdown 오버라이드 추가
- `@media (min-width: 1024px)`: .sidebar-mobile-header display:none

## 성공 기준

- [ ] 모바일에서 햄버거 메뉴 → Categories/Tags/지식그래프 정상 표시, 뷰포트 이탈 없음
- [ ] 모바일 사이드바 열린 상태에서 테마 토글 가능
- [ ] iOS Safari 사이드바 하단 잘림 없음
- [ ] 라이트/다크 모드 전환 시 드롭다운 색상 정상
- [ ] PC 기능 전혀 영향받지 않음
