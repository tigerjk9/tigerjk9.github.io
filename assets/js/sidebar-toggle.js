/**
 * 접이식 사이드바 토글 기능
 * - 데스크톱: 사이드바 접기/펼치기
 * - 모바일: 오버레이 방식
 * - localStorage로 사용자 선택 기억
 */

(function() {
  'use strict';

  // 초기화
  function initSidebarToggle() {
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
  }

  // DOM 로드 완료 후 초기화
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebarToggle);
  } else {
    initSidebarToggle();
  }
})();
