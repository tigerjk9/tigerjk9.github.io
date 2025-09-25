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
</style>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="mynetwork" style="width: 100%; height: 100vh; background-color: #0A192F;"></div>

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

        var options = {
          nodes: {
            shape: 'dot',
            borderWidth: 0,
            scaling: { 
              min: 15, 
              max: 50, 
              label: { min: 14, max: 30, drawThreshold: 8, maxVisible: 25 }
            },
            font: { 
              color: '#d3d3d3', 
              size: 16, 
              face: 'sans-serif', 
              strokeWidth: 0 
            },
            shadow: { enabled: true, color: '#255784', size: 15 }
          },
          edges: {
            // width 속성 삭제 -> scaling이 제어하도록 함
            smooth: { type: 'dynamic' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            color: { color: '#84A9C0', highlight: '#FFFFFF' },
            shadow: { enabled: true, color: '#255784', size: 10 },
            
            // [추가] 연결선 가중치에 따른 굵기 조절
            scaling: {
              min: 0.5,  // 최소 굵기
              max: 5,    // 최대 굵기
              label: false // 굵기 값을 텍스트로 표시하지 않음
            }
          },
          physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -120,
              centralGravity: 0.02,
              springLength: 150,
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
