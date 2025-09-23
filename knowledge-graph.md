---
layout: wide
title: "지식 그래프 (Knowledge Graph)"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background-color: #0A192F !important; /* 페이지와 body 배경색을 강제 지정 */
  }

  .page__footer {
    background-color: transparent !important; /* 꼬리말 배경을 투명하게 만듭니다. */
  }

  /* 프레임 확장 */
  .page--knowledge-graph .page__inner-wrap {
    max-width: none !important;
  }

  /* 제목 가운데 정렬 */
  .page--knowledge-graph .page__title {
    text-align: center;
  }

  /* 콘텐츠 시작 위치 조정 */
  .page--knowledge-graph #main {
    margin-left: 320px; 
  }
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

        var options = {
          nodes: {
            shape: 'dot',
            borderWidth: 0,
            scaling: { 
              min: 10, 
              max: 40, 
              label: { 
                min: 14, 
                max: 30, 
                drawThreshold: 8, 
                maxVisible: 25 
              }
            },
            font: { 
              color: '#d3d3d3', 
              size: 16, 
              face: 'sans-serif', 
              strokeWidth: 0 
            }
          },
          edges: {
            width: 0.5,
            smooth: {
              type: 'dynamic'
            },
            arrows: {
              to: {
                enabled: true,
                scaleFactor: 0.5
              }
            },
            color: {
              inherit: 'both',
              opacity: 0.8
            }
          },
          physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -120,
              centralGravity: 0.001,
              springLength: 200,
              springConstant: 0.05,
              avoidOverlap: 0.8
            },
            minVelocity: 0.75,
            stabilization: {
              iterations: 300
            }
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
