---
layout: single
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
---

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<div id="mynetwork" style="width: 100%; height: 800px; border: 1px solid #ddd;"></div>

<script type="text/javascript">
  // DOM이 로드되면 스크립트 실행
  document.addEventListener('DOMContentLoaded', function() {
    // 그래프가 그려질 컨테이너
    var container = document.getElementById('mynetwork');

    // 1단계에서 생성한 JSON 데이터 가져오기
    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        // 빈 엣지 데이터 제거 (JSON 생성 시 마지막 쉼표 처리용)
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        // 노드 크기 계산: 각 노드가 얼마나 많은 연결(엣지)을 가졌는지 계산
        const a_nodes = graphData.nodes.map(node => {
          const degree = graphData.edges.filter(edge => edge.from === node.id || edge.to === node.id).length;
          // 연결 수에 비례하여 노드 크기(value) 설정 (최소값 1)
          node.value = Math.max(degree, 1); 
          return node;
        });

        // 데이터 객체 생성
        var data = {
          nodes: a_nodes,
          edges: graphData.edges
        };

        // 그래프 옵션 설정
        var options = {
          nodes: {
            shape: 'dot', // 노드 모양
            scaling: {
              min: 10,
              max: 40,
              label: {
                min: 8,
                max: 20
              }
            },
            font: {
              size: 14,
              face: 'Tahoma'
            }
          },
          edges: {
            width: 0.15,
            color: { inherit: 'from' },
            smooth: {
              type: 'continuous'
            }
          },
          physics: {
            // 물리 엔진 설정으로 노드들이 자연스럽게 퍼지도록 함
            forceAtlas2Based: {
              gravitationalConstant: -26,
              centralGravity: 0.005,
              springLength: 230,
              springConstant: 0.18
            },
            maxVelocity: 146,
            solver: 'forceAtlas2Based',
            timestep: 0.35,
            stabilization: { iterations: 150 }
          },
          interaction: {
            // 마우스 오버, 드래그 등 상호작용 설정
            tooltipDelay: 200,
            hideEdgesOnDrag: true
          }
        };

        // 네트워크 생성
        var network = new vis.Network(container, data, options);

        // 노드를 클릭했을 때 해당 게시물 URL로 이동하는 이벤트 추가
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
