---
layout: single
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
---

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
        // 옵시디언 스타일을 위한 그래프 옵션 (대폭 수정)
        // =================================================================
        var options = {
          nodes: {
            shape: 'dot',
            borderWidth: 0, // 노드 테두리 제거
            scaling: {
              min: 10,
              max: 40,
              label: {
                min: 14,
                max: 30,
                drawThreshold: 8, // 줌 레벨이 8 이상일 때만 라벨 표시
                maxVisible: 25   // 최대 25개 라벨만 동시 표시
              }
            },
            font: {
              color: '#d3d3d3', // 폰트 색상을 밝은 회색으로 변경
              size: 16,
              face: 'sans-serif',
              strokeWidth: 0 // 폰트 테두리 제거
            }
          },
          edges: {
            width: 0.5, // 연결선을 더 가늘게
            color: {
              color: '#505050', // 연결선 색상을 은은한 회색으로
              highlight: '#848484'
            },
            smooth: {
              type: 'continuous'
            }
          },
          physics: {
            // 노드 간 거리를 확보하고 자연스러운 배치를 위한 물리엔진 설정
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -100, // 서로 밀어내는 힘을 강하게 (노드 간격 확보)
              centralGravity: 0.01,
              springLength: 200, // 연결된 노드 간의 기본 거리를 길게
              springConstant: 0.05,
              avoidOverlap: 0.5 // 노드가 겹치지 않도록 하는 강도
            },
            minVelocity: 0.75,
            stabilization: {
              iterations: 200
            }
          },
          interaction: {
            hover: true, // 마우스를 올렸을 때 하이라이트
            tooltipDelay: 200,
            hideEdgesOnDrag: true
          }
        };
        // =================================================================

        var network = new vis.Network(container, data, options);

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
