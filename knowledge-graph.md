---
layout: single
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
---

<style>
  .page__inner-wrap {
    max-width: 100% !important;
    padding-left: 1em !important;
    padding-right: 1em !important;
  }
</style>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="mynetwork" style="width: 100%; height: 90vh; background-color: #202020;"></div>

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

        // =================================================================
        // 2번 요청: 무작위성 강화를 위한 물리 엔진 옵션 수정
        // =================================================================
        var options = {
          nodes: { /* 이전과 동일 */
            shape: 'dot',
            borderWidth: 0,
            scaling: { min: 10, max: 40, label: { min: 14, max: 30, drawThreshold: 8, maxVisible: 25 }},
            font: { color: '#d3d3d3', size: 16, face: 'sans-serif', strokeWidth: 0 }
          },
          edges: { /* 이전과 동일 */
            width: 0.5,
            color: { color: '#505050', highlight: '#848484' },
            smooth: { type: 'continuous' }
          },
          physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -120,
              centralGravity: 0.001, // 중앙으로 당기는 힘을 거의 0에 가깝게 대폭 줄임
              springLength: 200,
              springConstant: 0.05,
              avoidOverlap: 0.8 // 겹침 방지 강도를 높임
            },
            minVelocity: 0.75,
            stabilization: {
              iterations: 300 // 안정화 계산을 더 많이 하여 노드가 충분히 퍼지도록 함
            }
          },
          interaction: { /* 이전과 동일 */
            hover: true,
            tooltipDelay: 200,
            hideEdgesOnDrag: true
          }
        };
        // =================================================================

        var network = new vis.Network(container, data, options);
        
        // (선택 사항) 그래프가 안정화된 후 물리 엔진을 꺼서 노드를 고정
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
