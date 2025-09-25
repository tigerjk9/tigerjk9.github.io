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
    margin-left: 0; /* 사이드바 여백 제거 */
    padding: 0;
  }
  
  /* --- [추가] 태그 버튼 및 레이아웃 스타일 --- */
  #graph-container {
    position: relative;
    width: 100vw;
    height: 100vh;
  }
  #tag-buttons {
    position: absolute;
    top: 20px;
    left: 20px;
    z-index: 10;
    max-height: 90vh;
    overflow-y: auto;
    background: rgba(10, 25, 47, 0.85);
    border-radius: 8px;
    padding: 10px;
  }
  #tag-buttons button {
    display: block;
    width: 100%;
    padding: 8px 15px;
    margin-bottom: 5px;
    font-size: 14px;
    color: #d3d3d3;
    background-color: #112240;
    border: 1px solid #255784;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    text-align: left;
  }
  #tag-buttons button:hover, #tag-buttons button.active {
    background-color: #255784;
    color: #ffffff;
  }
  /* --- [추가] --- */

</style>

<div id="graph-container">
  <div id="tag-buttons"></div>
  <div id="mynetwork" style="width: 100%; height: 100vh; background-color: #0A192F;"></div>
</div>

<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('mynetwork');
    var tagButtonsContainer = document.getElementById('tag-buttons');

    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        const a_nodes = graphData.nodes.map(node => {
          const degree = graphData.edges.filter(edge => edge.from === node.id || edge.to === node.id).length;
          node.value = Math.max(degree, 1);
          // [추가] 원본 색상 정보 저장
          node.originalColor = '#97C2FC'; // vis.js 기본 노드 색상
          return node;
        });

        // [수정] vis.DataSet 사용
        var nodesDataSet = new vis.DataSet(a_nodes);
        var edgesDataSet = new vis.DataSet(graphData.edges);

        var data = {
          nodes: nodesDataSet,
          edges: edgesDataSet
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
            smooth: { type: 'dynamic' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            color: { color: '#84A9C0', highlight: '#FFFFFF' },
            shadow: { enabled: true, color: '#255784', size: 10 },
            scaling: {
              min: 0.5, 
              max: 5, 
              label: false
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
                var node = nodesDataSet.get(nodeId);
                if (node && node.url) {
                    window.open(node.url, '_blank');
                }
            }
        });

        // --- [추가] 태그 버튼 생성 및 하이라이트 기능 ---

        // 1. 모든 태그 추출 및 버튼 생성
        const allTags = new Set();
        nodesDataSet.forEach(node => {
          if (node.tags) {
            node.tags.forEach(tag => allTags.add(tag));
          }
        });
        
        // '전체 보기' 버튼 추가
        const resetButton = document.createElement('button');
        resetButton.innerText = '전체 보기';
        resetButton.className = 'active'; // 처음엔 활성화 상태
        resetButton.onclick = () => highlightByTag(null);
        tagButtonsContainer.appendChild(resetButton);

        // 태그 버튼들 추가
        Array.from(allTags).sort().forEach(tag => {
          const button = document.createElement('button');
          button.innerText = tag;
          button.onclick = () => highlightByTag(tag);
          tagButtonsContainer.appendChild(button);
        });
        
        // 2. 하이라이트 함수
        function highlightByTag(tag) {
          // 모든 버튼의 active 클래스 제거 후, 현재 클릭된 버튼에만 추가
          const buttons = tagButtonsContainer.getElementsByTagName('button');
          for (let btn of buttons) {
            if (btn.innerText === (tag || '전체 보기')) {
              btn.className = 'active';
            } else {
              btn.className = '';
            }
          }

          if (tag === null) {
            // 전체 보기: 모든 노드와 엣지를 원래 스타일로 복구
            const allNodes = nodesDataSet.map(node => {
              delete node.color;
              delete node.font.color;
              return node;
            });
            const allEdges = edgesDataSet.map(edge => {
              delete edge.color;
              return edge;
            });
            nodesDataSet.update(allNodes);
            edgesDataSet.update(allEdges);
            return;
          }

          const dimmedNodeColor = 'rgba(40, 60, 80, 0.4)';
          const dimmedFontColor = 'rgba(211, 211, 211, 0.4)';
          const dimmedEdgeColor = 'rgba(132, 169, 192, 0.2)';

          // 하이라이트할 노드 ID 집합 생성
          const highlightedNodeIds = new Set();
          nodesDataSet.forEach(node => {
            if (node.tags && node.tags.includes(tag)) {
              highlightedNodeIds.add(node.id);
              // 직접 연결된 이웃 노드 추가
              const connectedEdges = network.getConnectedEdges(node.id);
              connectedEdges.forEach(edgeId => {
                const edge = edgesDataSet.get(edgeId);
                if (edge.from === node.id) highlightedNodeIds.add(edge.to);
                if (edge.to === node.id) highlightedNodeIds.add(edge.from);
              });
            }
          });

          // 노드 스타일 업데이트
          const nodesToUpdate = nodesDataSet.map(node => {
            if (highlightedNodeIds.has(node.id)) {
              delete node.color;
              delete node.font.color;
            } else {
              node.color = dimmedNodeColor;
              node.font = { color: dimmedFontColor };
            }
            return node;
          });

          // 엣지 스타일 업데이트
          const edgesToUpdate = edgesDataSet.map(edge => {
            if (highlightedNodeIds.has(edge.from) && highlightedNodeIds.has(edge.to)) {
              delete edge.color;
            } else {
              edge.color = dimmedEdgeColor;
            }
            return edge;
          });

          nodesDataSet.update(nodesToUpdate);
          edgesDataSet.update(edgesToUpdate);
        }
        // --- [추가] 종료 ---
      });
  });
</script>
