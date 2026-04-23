/**
 * 접이식 사이드바 토글 기능
 * - 데스크톱: 사이드바 접기/펼치기
 * - 모바일: 오버레이 방식
 * - localStorage로 사용자 선택 기억
 */

(function() {
  'use strict';

  // 모바일 사이드바 상단 헤더 주입 (테마 토글 포함)
  function injectMobileSidebarHeader() {
    var sidebarEl = document.querySelector('.sidebar');
    if (!sidebarEl || sidebarEl.querySelector('.sidebar-mobile-header')) return;

    var header = document.createElement('div');
    header.className = 'sidebar-mobile-header';
    header.innerHTML =
      '<span class="sidebar-mobile-header__title">메뉴</span>' +
      '<button class="theme-toggle" type="button" aria-label="다크/라이트 모드 전환">' +
      '<i class="fas fa-sun theme-toggle__sun"></i>' +
      '<i class="fas fa-moon theme-toggle__moon"></i>' +
      '</button>';
    sidebarEl.insertBefore(header, sidebarEl.firstChild);
  }

  // 초기화
  function initSidebarToggle() {
    // 모바일 사이드바 헤더 주입
    injectMobileSidebarHeader();

    // 토글 버튼 생성
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.setAttribute('aria-label', '사이드바 토글');
    toggleBtn.innerHTML = '<span>☰</span>';
    document.body.appendChild(toggleBtn);

    // 모바일용 오버레이 생성
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // localStorage에서 저장된 상태 불러오기
    const savedState = localStorage.getItem('sidebarState');
    const isDesktop = window.innerWidth >= 1024;

    // 데스크톱: 기본값은 펼쳐진 상태, 저장된 값이 있으면 그것 사용
    // 모바일: 기본값은 접힌 상태
    if (isDesktop) {
      if (savedState === 'collapsed') {
        document.body.classList.add('sidebar-collapsed');
        toggleBtn.innerHTML = '<span>☰</span>';
      } else {
        document.body.classList.remove('sidebar-collapsed');
        toggleBtn.innerHTML = '<span>✕</span>';
      }
    } else {
      // 모바일은 기본 접힌 상태
      document.body.classList.remove('sidebar-expanded');
      toggleBtn.innerHTML = '<span>☰</span>';
    }

    // 토글 버튼 클릭 이벤트
    toggleBtn.addEventListener('click', function() {
      const isDesktop = window.innerWidth >= 1024;

      if (isDesktop) {
        // 데스크톱: collapsed 클래스 토글
        document.body.classList.toggle('sidebar-collapsed');
        const isCollapsed = document.body.classList.contains('sidebar-collapsed');
        
        // 버튼 아이콘 변경
        toggleBtn.innerHTML = isCollapsed ? '<span>☰</span>' : '<span>✕</span>';
        
        // localStorage에 상태 저장
        localStorage.setItem('sidebarState', isCollapsed ? 'collapsed' : 'expanded');
      } else {
        // 모바일: expanded 클래스 토글
        document.body.classList.toggle('sidebar-expanded');
        const isExpanded = document.body.classList.contains('sidebar-expanded');
        
        // 버튼 아이콘 변경
        toggleBtn.innerHTML = isExpanded ? '<span>✕</span>' : '<span>☰</span>';
      }
    });

    // 오버레이 클릭 시 사이드바 닫기 (모바일)
    overlay.addEventListener('click', function() {
      if (window.innerWidth < 1024) {
        document.body.classList.remove('sidebar-expanded');
        toggleBtn.innerHTML = '<span>☰</span>';
      }
    });

    // 윈도우 리사이즈 시 처리
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        const isDesktop = window.innerWidth >= 1024;
        
        if (isDesktop) {
          // 데스크톱으로 전환: expanded 클래스 제거, 저장된 상태 복원
          document.body.classList.remove('sidebar-expanded');
          const savedState = localStorage.getItem('sidebarState');
          
          if (savedState === 'collapsed') {
            document.body.classList.add('sidebar-collapsed');
            toggleBtn.innerHTML = '<span>☰</span>';
          } else {
            document.body.classList.remove('sidebar-collapsed');
            toggleBtn.innerHTML = '<span>✕</span>';
          }
        } else {
          // 모바일로 전환: collapsed 클래스 제거, 기본 접힌 상태
          document.body.classList.remove('sidebar-collapsed');
          document.body.classList.remove('sidebar-expanded');
          toggleBtn.innerHTML = '<span>☰</span>';
        }
      }, 250);
    });

    // ESC 키로 모바일 사이드바 닫기
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && window.innerWidth < 1024) {
        if (document.body.classList.contains('sidebar-expanded')) {
          document.body.classList.remove('sidebar-expanded');
          toggleBtn.innerHTML = '<span>☰</span>';
        }
      }
    });

    // 스와이프 제스처 (모바일)
    var swipeStartX = 0;
    var swipeStartY = 0;

    document.addEventListener('touchstart', function(e) {
      swipeStartX = e.touches[0].clientX;
      swipeStartY = e.touches[0].clientY;
    }, { passive: true });

    document.addEventListener('touchend', function(e) {
      if (window.innerWidth >= 1024) return;

      var dx = e.changedTouches[0].clientX - swipeStartX;
      var dy = e.changedTouches[0].clientY - swipeStartY;

      // 수직 스크롤이 주 방향이면 무시
      if (Math.abs(dy) > Math.abs(dx)) return;

      var THRESHOLD = 60;
      var EDGE = 35;

      if (dx > THRESHOLD && swipeStartX < EDGE) {
        // 왼쪽 엣지에서 오른쪽으로 스와이프 → 열기
        if (!document.body.classList.contains('sidebar-expanded')) {
          document.body.classList.add('sidebar-expanded');
          toggleBtn.innerHTML = '<span>✕</span>';
        }
      } else if (dx < -THRESHOLD && document.body.classList.contains('sidebar-expanded')) {
        // 왼쪽으로 스와이프 → 닫기
        document.body.classList.remove('sidebar-expanded');
        toggleBtn.innerHTML = '<span>☰</span>';
      }
    }, { passive: true });
  }

  // 사이드바 섹션 접기/펼치기
  function initSectionCollapse() {
    document.querySelectorAll('.sidebar-section__toggle').forEach(function(toggle) {
      var section = toggle.closest('.sidebar-section');
      if (!section) return;

      // localStorage에서 상태 복원 (기본값: 펼쳐진 상태)
      var key = 'sidebar-sec-' + (toggle.dataset.section || 'unknown');
      var saved = localStorage.getItem(key);
      if (saved === '1') {
        section.classList.add('collapsed');
      }

      toggle.addEventListener('click', function() {
        section.classList.toggle('collapsed');
        var collapsed = section.classList.contains('collapsed');
        localStorage.setItem(key, collapsed ? '1' : '0');
      });
    });
  }

  // DOM 로드 완료 후 초기화
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initSidebarToggle();
      initSectionCollapse();
    });
  } else {
    initSidebarToggle();
    initSectionCollapse();
  }
})();
