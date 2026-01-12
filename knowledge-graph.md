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

  /* --- 스피너 CSS (z-index 수정됨) --- */
  .loader {
    border: 8px solid #f3f3f3; /* Light grey */
    border-top: 8px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 1.5s linear infinite;
    
    /* 부모(#graph-wrapper)의 정중앙에 배치 */
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -30px;
    margin-left: -30px;
    /* 그래프(z-index: 1)보다 항상 위에 있도록 z-index를 높게 설정 */
    z-index: 1000;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="graph-wrapper" style="width: 100%; height: 100vh; position: relative;">
  
  <div id="graph-spinner" class="loader"></div>
  
  <div id="mynetwork" style="width: 100%; height: 100%; background-color: #0A192F; z-index: 1;"></div>

</div>


<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    // 컨테이너와 스피너를 각각 가져옵니다.
    var container = document.getElementById('mynetwork');
    var spinner = document.getElementById('graph-spinner');
    
    var startTime = new Date().getTime();

    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        const a_edges = graphData.edges.map(edge => {
          edge.width = edge.value ? Math.max(0.5, Math.min(edge.value * 0.8, 5)) : 1;
          return edge;
        });

        const a_nodes = graphData.nodes.map(node => {
          const degree = graphData.edges.filter(edge => edge.from === node.id || edge.to === node.id).length;
          node.value = Math.max(degree, 1); 
          return node;
        });

        var data = {
          nodes: a_nodes,
          edges: a_edges
        };

        var options = {
          // ... (기존 옵션) ...
          nodes: { shape: 'dot', borderWidth: 0, scaling: { min: 15, max: 50, label: { min: 14, max: 30, drawThreshold: 8, maxVisible: 25 } }, font: { color: '#d3d3d3', size: 16, face: 'sans-serif', strokeWidth: 0 }, shadow: { enabled: true, color: '#255784', size: 15 } },
          edges: { smooth: { type: 'dynamic' }, arrows: { to: { enabled: true, scaleFactor: 0.5 } }, color: { color: '#84A9C0', highlight: '#FFFFFF' }, shadow: { enabled: true, color: '#255784', size: 10 }, scaling: { min: 0.5, max: 5, label: false } },
          physics: { solver: 'forceAtlas2Based', forceAtlas2Based: { gravitationalConstant: -120, centralGravity: 0.02, springLength: 150, springConstant: 0.05, avoidOverlap: 0.8 }, minVelocity: 0.75, stabilization: { iterations: 300 } },
          interaction: { hover: true, tooltipDelay: 200, hideEdgesOnDrag: true }
        };

        // vis.js는 이제 #mynetwork만 제어합니다. 스피너는 안전합니다.
        var network = new vis.Network(container, data, options);
        
        var hideSpinner = function() {
          var endTime = new Date().getTime();
          var duration = endTime - startTime; 
          var minDuration = 1000; // 최소 1초 (1000ms)

          if (duration < minDuration) {
            setTimeout(function() {
              spinner.style.display = 'none';
            }, minDuration - duration);
          } else {
            spinner.style.display = 'none';
          }
        };

        network.on("stabilizationIterationsDone", function () {
          network.setOptions( { physics: false } );
          hideSpinner(); 
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
        console.error('Error loading graph data:', error);
        spinner.style.display = 'none';
      });
  });
</script>
