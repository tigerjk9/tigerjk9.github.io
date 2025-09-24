---
layout: wide
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background-color: #0A192F !important;
  }
  .page__footer {
    background-color: transparent !important;
  }
  .page--knowledge-graph .page__inner-wrap {
    max-width: none !important;
  }
  .page--knowledge-graph .page__title {
    text-align: center;
  }
  /* 데스크톱 여백은 main.scss에서 제어하므로 여기서는 삭제 또는 주석처리 합니다. */
  /*
  .page--knowledge-graph #main {
    margin-left: 320px; 
  }
  */
</style>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="mynetwork" style="width: 100%; height: 90vh; background-color: #0A192F;"></div>

<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('mynetwork');

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

        // --- 화면 크기에 따른 옵션 분기 ---
        const isMobile = window.innerWidth < 768;

        var options = {
          nodes: {
            shape: 'dot',
            borderWidth: 0,
            // 모바일일 경우 노드와 라벨 크기를 작게 조절
            scaling: { 
              min: isMobile ? 10 : 15, 
              max: isMobile ? 35 : 50, 
              label: { min: 12, max: 25, drawThreshold: 8, maxVisible: 20 }
            },
            font: { 
              color: '#d3d3d3', 
              size: isMobile ? 12 : 16, // 모바일일 경우 폰트 크기 축소
              face: 'sans-serif', 
              strokeWidth: 0 
            },
            shadow: {
              enabled: true,
              color: '#255784',
              size: 15
            }
          },
          edges: {
            width: 1,
            smooth: { type: 'dynamic' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            color: { color: '#84A9C0', highlight: '#FFFFFF' },
            shadow: { enabled: true, color: '#255784', size: 10 }
          },
          physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -120,
              centralGravity: 0.02,
              springLength: isMobile ? 100 : 150, // 모바일일 경우 간격 축소
              springConstant: 0.05,
              avoidOverlap: 0.8
            },
            minVelocity: 0.75,
            stabilization: { iterations: 300 }
          },
          interaction: {
            hover: true,
            tooltipDelay: 200,
            hideEdgesOnDrag: true
          }
        };

        var network = new vis.Network(container, data, options);
        
        network.on("stabilizationIterationsDone", function () {
          network.setOptions( { physics: false } );
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
      });
  });
</script>
