---
layout: single # 사용하시는 테마의 기본 페이지 레이아웃으로 변경하셔도 됩니다. (예: page)
title: "태그 지식 그래프!"
permalink: /knowledge-graph/
---

<div id="graph-container" style="width: 100%; height: 70vh; background-color: #f9f9f9; border: 1px solid #e1e1e1; border-radius: 8px;"></div>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('graph-container');

    // 그래프의 모양, 물리 효과 등 옵션을 설정합니다.
    const options = {
      nodes: {
        shape: 'dot',
        borderWidth: 2,
        font: { size: 16 },
        scaling: {
          min: 10,
          max: 40,
          label: { enabled: true, min: 14, max: 22 }
        }
      },
      edges: {
        width: 0.5,
        color: { inherit: 'from' },
        smooth: { type: 'continuous' }
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -70,
          centralGravity: 0.01,
          springLength: 200,
          springConstant: 0.09
        }
      },
      interaction: {
        hover: true, 
        tooltipDelay: 200
      }
    };

    // 1단계에서 만든 graph-data.json 파일을 불러옵니다.
    fetch('/graph-data.json')
      .then(response => response.json())
      .then(data => {
        // 마지막 빈 edge 객체 제거
        data.edges = data.edges.filter(edge => edge.from);

        const graphData = {
            nodes: new vis.DataSet(data.nodes),
            edges: new vis.DataSet(data.edges)
        };

        // 네트워크(그래프)를 생성하고 화면에 그립니다.
        const network = new vis.Network(container, graphData, options);

        // 노드를 클릭하면 해당 태그 페이지로 이동하는 이벤트
        network.on("click", function (params) {
          if (params.nodes.length > 0) {
            const clickedNodeId = params.nodes[0];
            // 블로그의 태그 URL 구조에 맞게 수정하세요. (보통 /tags/#태그명 형식입니다)
            window.open(`/tags/#${clickedNodeId}`, '_blank');
          }
        });
      })
      .catch(error => console.error('그래프 데이터를 불러오는 중 오류 발생:', error));
  });
</script>
