---
layout: wide
title: "포스트 활동 히트맵"
permalink: /heatmap/
class: "page--knowledge-graph"
---

<style>
  .cal-heatmap-container { display: block; padding: 2em; }
  .ch-tooltip { background: #333; color: #fff; padding: 10px; border-radius: 4px; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
</style>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/cal-heatmap@4.2.2/dist/cal-heatmap.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cal-heatmap@4.2.2/dist/cal-heatmap.css">

<div id="cal-heatmap" style="color: #eee;"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  
  fetch('/heatmap-data.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('heatmap-data.json 파일을 불러오는 데 실패했습니다.');
      }
      return response.json();
    })
    .then(posts => {

      const postsByDay = posts.reduce((acc, post) => {
        const date = post.date;
        acc[date] = (acc[date] || 0) + 1;
        return acc;
      }, {});

      const heatmapData = Object.keys(postsByDay).map(date => ({
        date: date,
        value: postsByDay[date]
      }));

      const cal = new CalHeatmap(); // 대문자 'C'로 되돌림

      cal.paint({
        data: {
          source: heatmapData,
          x: 'date',
          y: 'value'
        },
        date: {
          start: new Date(new Date().setFullYear(new Date().getFullYear() - 1)),
          locale: 'ko'
        },
        range: 12,
        scale: {
          color: {
            scheme: 'Greens', 
            type: 'threshold',
            domain: [1, 2, 3, 4]
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
      }
      // , // [수정] 플러그인 부분을 잠시 주석 처리하여 비활성화합니다.
      // [
      //   [
      //     CalHeatmap.Tooltip,
      //     {
      //       text: function (date, value, dayjsDate) {
      //         return (value ? value : 'No') + ' post' + (value > 1 ? 's' : '') + ' on ' + dayjsDate.format('LL');
      //       }
      //     }
      //   ]
      // ]
      );
    })
    .catch(error => {
      document.getElementById('cal-heatmap').innerHTML = '<h3 style="color:red;">오류 발생: ' + error.message + '</h3><p>개발자 도구(F12)의 Console 탭에서 더 자세한 정보를 확인하세요.</p>';
      console.error(error);
    });
});
</script>
