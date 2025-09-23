---
layout: single
title: "지식 네트워크"
permalink: /knowledge-graph/
---

<div id="graph-container" style="width: 100%; height: 80vh; background-color: #0d1117; border: 1px solid #30363d; border-radius: 8px;"></div>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('graph-container');

    // 그래프의 모양, 물리 효과 등 옵션을 설정합니다.
    const options = {
      groups: {
        tag: {
          color: { background: '#6A5ACD', border: '#9370DB' }, // 태그는 보라색 계열
          shape: 'dot',
          font: { color: '#ffffff' }
        },
        post: {
          color: { background: '#FFA500', border: '#FFDAB9' }, // 게시물은 주황색 계열
          shape: 'box', // 게시물은 사각형 모양
          font: { color: '#ffffff', size: 14 }
        }
      },
      nodes: {
        borderWidth: 2,
        scaling: {
          min: 15,
          max: 40
        },
        font: {
          size: 16,
          face: 'tahoma',
          strokeWidth: 3,
          strokeColor: '#0d1117'
        }
      },
      edges: {
        width: 1,
        color: { color: '#4B525B' },
        smooth: { type: 'continuous' }
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -150,
          centralGravity: 0.01,
          springLength: 250,
          avoidOverlap: 0.8
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 200
      }
    };

    // '게시물'과 '태그' 데이터가 모두 포함된 JSON 파일을 최상위 경로에서 불러옵니다.
    fetch('/graph-data.json')
      .then(response => response.json())
      .then(data => {
        // Vis.js 데이터 형식에 맞게 변환
        const graphData = {
          nodes: new vis.DataSet(data.nodes),
          edges: new vis.DataSet(data.edges)
        };
        
        // 네트워크(그래프)를 생성하고 화면에 그립니다.
        const network = new vis.Network(container, graphData, options);

        // 노드 클릭 이벤트를 수정하여 게시물과 태그를 구분합니다.
        network.on("click", function (params) {
          if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = graphData.nodes.get(nodeId); // 클릭한 노드의 전체 정보 가져오기

            if (node.group === 'post') {
              // 노드가 'post' 그룹이면 해당 게시물 URL로 이동
              window.open(node.id, '_blank');
            } else if (node.group === 'tag') {
              // 노드가 'tag' 그룹이면 해당 태그 페이지로 이동
              window.open(`/tags/#${node.id}`, '_blank');
            }
          }
        });
      })
      .catch(error => console.error('그래프 데이터를 불러오는 중 오류 발생:', error));
  });
</script>
