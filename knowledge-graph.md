---
layout: wide
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background-color: #0A192F !important;
    overflow-y: hidden;
  }
  .page__footer {
    background-color: transparent !important;
    border: none;
  }
  .page--knowledge-graph .page__inner-wrap {
    max-width: none !important;
  }
  .page--knowledge-graph .page__title {
    text-align: center;
  }
  .page--knowledge-graph #main {
    margin-left: 320px; 
  }

  /* --- 스피너 CSS --- */
  .loader {
    border: 8px solid #f3f3f3; /* Light grey */
    border-top: 8px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 1.5s linear infinite;
    
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -30px;
    margin-left: -30px;
    z-index: 10;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="mynetwork" style="width: 100%; height: 100vh; background-color: #0A192F; position: relative;">
  <div id="graph-spinner" class="loader"></div>
</div>


<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('mynetwork');
    var spinner = document.getElementById('graph-spinner');
    
    // 로딩 시작 시간 기록
    var startTime = new Date().getTime();

    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        const a_nodes = graphData.nodes.map(node => {
          const degree = graphData.edges.filter(edge => edge.from === node.id || edge.to === node.id).length;
          node.value = Math.max(degree, 1); 
          return node;
        });

        var data = {
          nodes: a_nodes,
          edges: graphData.edges
        };

        var options = {
          // ... (기존 옵션) ...
          nodes: { shape: 'dot', borderWidth: 0, scaling: { min: 15, max: 50, label: { min: 14, max: 30, drawThreshold: 8, maxVisible: 25 } }, font: { color: '#d3d3d3', size: 16, face: 'sans-serif', strokeWidth: 0 }, shadow: { enabled: true, color: '#255784', size: 15 } },
          edges: { smooth: { type: 'dynamic' }, arrows: { to: { enabled: true, scaleFactor: 0.5 } }, color: { color: '#84A9C0', highlight: '#FFFFFF' }, shadow: { enabled: true, color: '#255784', size: 10 }, scaling: { min: 0.5, max: 5, label: false } },
          physics: { solver: 'forceAtlas2Based', forceAtlas2Based: { gravitationalConstant: -120, centralGravity: 0.02, springLength: 150, springConstant: 0.05, avoidOverlap: 0.8 }, minVelocity: 0.75, stabilization: { iterations: 300 } },
          interaction: { hover: true, tooltipDelay: 200, hideEdgesOnDrag: true }
        };

        var network = new vis.Network(container, data, options);
        
        // --- 1. 스피너 숨기기 로직 (수정됨) ---
        var hideSpinner = function() {
          var endTime = new Date().getTime();
          var duration = endTime - startTime; // 로드에 걸린 시간 (ms)
          var minDuration = 1000; // 최소 1초 (1000ms)

          if (duration < minDuration) {
            // 1초가 안 걸렸으면, 1초를 채운 후에 스피너 숨김
            setTimeout(function() {
              spinner.style.display = 'none';
            }, minDuration - duration);
          } else {
            // 1초 이상 걸렸으면, 즉시 스피너 숨김
            spinner.style.display = 'none';
          }
        };

        network.on("stabilizationIterationsDone", function () {
          network.setOptions( { physics: false } );
          hideSpinner(); // <-- 스피너 숨기기 함수 호출
        });

        network.on("click", function (params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                var node = data.nodes.find(n => n.id === nodeId);
                if (node && node.url) {
                    window.open(node.url, '_blank');
                }
            }
        });
      })
      .catch(error => {
        // --- 2. 에러 발생 시에도 스피너 숨김 (수정됨) ---
        console.error('Error loading graph data:', error);
        // 에러 시에는 즉시 숨김
        spinner.style.display = 'none';
      });
  });
</script>
