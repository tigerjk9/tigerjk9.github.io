---
layout: wide
title: "포스트 활동 히트맵"
permalink: /heatmap/
class: "page--knowledge-graph" # 지식그래프와 동일한 다크모드/전체너비 스타일 적용
---

<style>
  /* Cal-Heatmap 라이브러리 기본 스타일 */
  .cal-heatmap-container {
    display: block;
    padding: 2em;
  }
  /* 툴팁 스타일 (옵션) */
  .ch-tooltip {
    background: #333;
    color: #fff;
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
  }
</style>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/cal-heatmap@4.2.2/dist/cal-heatmap.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cal-heatmap@4.2.2/dist/cal-heatmap.css">

<div id="cal-heatmap" style="color: #eee;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  
  // 1단계에서 생성한 JSON 데이터 가져오기
  fetch('/heatmap-data.json')
    .then(response => response.json())
    .then(posts => {

      // 날짜별로 게시물 수를 계산 (데이터 가공)
      const postsByDay = posts.reduce((acc, post) => {
        const date = post.date;
        acc[date] = (acc[date] || 0) + 1;
        return acc;
      }, {});

      const heatmapData = Object.keys(postsByDay).map(date => ({
        date: date,
        value: postsByDay[date]
      }));

      // Cal-Heatmap 인스턴스 생성
      const cal = new CalHeatmap();

      // 히트맵 그리기
      cal.paint({
        data: {
          source: heatmapData,
          x: 'date',
          y: 'value'
        },
        date: {
          start: new Date(new Date().setFullYear(new Date().getFullYear() - 1)), // 1년 전부터
          locale: 'ko' // 한글 요일/월 표시
        },
        range: 12, // 12개월(1년) 범위
        scale: {
          color: {
            // 색상 범위: 0개(어두운 회색) ~ 최대(밝은 녹색)
            scheme: 'Greens', 
            type: 'threshold',
            domain: [1, 2, 3, 4] // 1개, 2개, 3개, 4개 이상일 때 색상 변경
          }
        },
        domain: {
          type: 'month',
          gutter: 4,
          label: { text: 'MMM', textAlign: 'start', position: 'top' }
        },
        subDomain: {
          type: 'day',
          radius: 2,
          width: 15,
          height: 15,
          gutter: 4
        }
      }, 
      [
        // 툴팁 플러그인: 각 날짜에 마우스를 올리면 게시물 수를 보여줌
        [
          Tooltip,
          {
            text: function (date, value, dayjsDate) {
              return (value ? value : 'No') + ' post' + (value > 1 ? 's' : '') + ' on ' + dayjsDate.format('LL');
            }
          }
        ]
      ]);
    });
});
</script>
