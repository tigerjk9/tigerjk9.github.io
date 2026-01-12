---
layout: wide
title: "지식 그래프 3D (Knowledge Graph 3D)"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background-color: #0A192F !important;
    overflow: hidden;
    margin: 0;
    padding: 0;
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
    color: #64FFDA;
    text-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
  }
  .page--knowledge-graph #main {
    margin-left: 320px; 
  }

  #info-panel {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(10, 25, 47, 0.95);
    border: 2px solid #64FFDA;
    border-radius: 10px;
    padding: 15px 20px;
    color: #CCD6F6;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    z-index: 100;
    max-width: 350px;
    box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
    display: none;
    backdrop-filter: blur(10px);
  }

  #info-panel h3 {
    margin: 0 0 10px 0;
    color: #64FFDA;
    font-size: 18px;
    border-bottom: 1px solid #64FFDA;
    padding-bottom: 5px;
  }

  #info-panel p {
    margin: 5px 0;
    line-height: 1.6;
  }

  #info-panel .category {
    display: inline-block;
    background: rgba(100, 255, 218, 0.2);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
    color: #64FFDA;
  }

  #controls {
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(10, 25, 47, 0.95);
    border: 2px solid #64FFDA;
    border-radius: 10px;
    padding: 15px;
    color: #CCD6F6;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    z-index: 100;
    box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
    backdrop-filter: blur(10px);
  }

  #controls h4 {
    margin: 0 0 10px 0;
    color: #64FFDA;
    font-size: 14px;
  }

  #controls ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  #controls li {
    margin: 5px 0;
    padding: 3px 0;
  }

  .loader {
    border: 8px solid #233554;
    border-top: 8px solid #64FFDA;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 1.5s linear infinite;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -30px;
    margin-left: -30px;
    z-index: 1000;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>

<script src="//unpkg.com/3d-force-graph"></script>

<div id="graph-wrapper" style="width: 100%; height: 100vh; position: relative;">
  <div id="graph-spinner" class="loader"></div>
  <div id="3d-graph"></div>
  
  <div id="info-panel">
    <h3 id="node-title">게시물 제목</h3>
    <p><span class="category" id="node-category"></span></p>
    <p id="node-connections"></p>
    <p style="color: #64FFDA; font-size: 11px; margin-top: 10px;">💡 더블클릭하여 게시물로 이동</p>
  </div>

  <div id="controls">
    <h4>🎮 조작법</h4>
    <ul>
      <li>🖱️ 드래그: 회전</li>
      <li>🔍 스크롤: 줌</li>
      <li>👆 클릭: 정보 표시</li>
      <li>👆👆 더블클릭: 게시물 이동</li>
    </ul>
  </div>
</div>

<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    const elem = document.getElementById('3d-graph');
    const spinner = document.getElementById('graph-spinner');
    const infoPanel = document.getElementById('info-panel');
    
    const startTime = new Date().getTime();

    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        const edges = graphData.edges.map(edge => ({
          source: edge.from,
          target: edge.to,
          value: edge.value || 1
        }));

        const nodes = graphData.nodes.map(node => {
          const degree = edges.filter(e => e.source === node.id || e.target === node.id).length;
          return {
            id: node.id,
            name: node.label,
            group: node.group,
            url: node.url,
            val: Math.max(degree * 2, 5),
            connections: degree
          };
        });

        const data = { nodes, links: edges };

        const categoryColors = {
          'default': '#8892B0',
          'AI': '#64FFDA',
          'ML': '#64FFDA',
          'Deep Learning': '#64FFDA',
          'Data Science': '#5EEAD4',
          'Programming': '#A78BFA',
          'Web': '#F472B6',
          'Algorithm': '#FBBF24',
          'Database': '#34D399',
          'System': '#60A5FA'
        };

        const Graph = ForceGraph3D()
          (elem)
          .graphData(data)
          .nodeLabel('name')
          .nodeAutoColorBy('group')
          .nodeVal('val')
          .nodeColor(node => categoryColors[node.group] || categoryColors['default'])
          .nodeOpacity(0.9)
          .nodeResolution(16)
          .linkWidth(link => Math.sqrt(link.value) * 0.5)
          .linkColor(() => 'rgba(132, 169, 192, 0.4)')
          .linkOpacity(0.6)
          .linkDirectionalParticles(link => link.value)
          .linkDirectionalParticleWidth(2)
          .linkDirectionalParticleSpeed(0.005)
          .backgroundColor('#0A192F')
          .showNavInfo(false)
          .enableNodeDrag(true)
          .enableNavigationControls(true)
          .onNodeClick(node => {
            document.getElementById('node-title').textContent = node.name;
            document.getElementById('node-category').textContent = node.group || 'default';
            document.getElementById('node-connections').textContent = `연결: ${node.connections}개`;
            infoPanel.style.display = 'block';
            
            Graph.cameraPosition(
              { x: node.x * 1.5, y: node.y * 1.5, z: node.z * 1.5 },
              node,
              1000
            );
          })
          .onNodeDblClick(node => {
            if (node.url) {
              window.open(node.url, '_blank');
            }
          })
          .onBackgroundClick(() => {
            infoPanel.style.display = 'none';
          })
          .d3Force('charge', d3.forceManyBody().strength(-120))
          .d3Force('link', d3.forceLink().distance(80).strength(1))
          .d3Force('center', d3.forceCenter());

        setTimeout(() => {
          spinner.style.display = 'none';
        }, 2000);

        Graph.d3Force('link').links(data.links);
        
      })
      .catch(error => {
        console.error('Error loading graph data:', error);
        spinner.style.display = 'none';
      });
  });
</script>
