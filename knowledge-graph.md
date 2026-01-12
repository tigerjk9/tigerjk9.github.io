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
    max-width: 400px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 0 30px rgba(100, 255, 218, 0.5), 0 0 60px rgba(100, 255, 218, 0.2);
    display: none;
    backdrop-filter: blur(10px);
    animation: panelGlow 2s ease-in-out infinite alternate;
  }

  @keyframes panelGlow {
    from { box-shadow: 0 0 30px rgba(100, 255, 218, 0.5), 0 0 60px rgba(100, 255, 218, 0.2); }
    to { box-shadow: 0 0 40px rgba(100, 255, 218, 0.7), 0 0 80px rgba(100, 255, 218, 0.3); }
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
    box-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
  }

  #top-connections-list li {
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 5px;
    border-radius: 4px;
  }

  #top-connections-list li:hover {
    background: rgba(100, 255, 218, 0.1);
    transform: translateX(5px);
    box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
  }

  #node-link {
    transition: all 0.3s ease;
  }

  #node-link:hover {
    background: rgba(100, 255, 218, 0.2);
    box-shadow: 0 0 20px rgba(100, 255, 218, 0.5);
    transform: scale(1.05);
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

  #3d-graph {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }
</style>

<script src="//unpkg.com/d3"></script>
<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/3d-force-graph"></script>

<div id="graph-wrapper" style="width: 100%; height: 100vh; position: relative;">
  <div id="graph-spinner" class="loader"></div>
  <div id="3d-graph"></div>
  
  <div id="info-panel">
    <h3 id="node-title">게시물 제목</h3>
    <p><span class="category" id="node-category"></span></p>
    <p id="node-connections"></p>
    <div id="top-connections" style="margin-top: 10px; font-size: 12px;">
      <strong style="color: #64FFDA;">주요 연결:</strong>
      <ul id="top-connections-list" style="margin: 5px 0; padding-left: 20px; list-style: none;"></ul>
    </div>
    <p style="margin-top: 10px;">
      <a id="node-link" href="#" target="_blank" style="color: #64FFDA; text-decoration: none; font-size: 12px; border: 1px solid #64FFDA; padding: 5px 10px; border-radius: 5px; display: inline-block;">
        🧠 본 게시물로 이동
      </a>
    </p>
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
          const nodeEdges = edges.filter(e => e.source === node.id || e.target === node.id);
          const degree = nodeEdges.length;
          return {
            id: node.id,
            name: node.label,
            group: node.group,
            url: node.url,
            val: Math.max(degree * 0.5, 2),
            connections: degree,
            edges: nodeEdges
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

        function createGlowTexture(node) {
          const canvas = document.createElement('canvas');
          canvas.width = 64;
          canvas.height = 64;
          const ctx = canvas.getContext('2d');
          
          const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
          const color = categoryColors[node.group] || categoryColors['default'];
          
          gradient.addColorStop(0, color);
          gradient.addColorStop(0.4, color + 'CC');
          gradient.addColorStop(0.7, color + '66');
          gradient.addColorStop(1, color + '00');
          
          ctx.fillStyle = gradient;
          ctx.fillRect(0, 0, 64, 64);
          
          return canvas;
        }

        const Graph = ForceGraph3D()(elem)
          .graphData(data)
          .nodeLabel('name')
          .nodeVal('val')
          .nodeColor(node => categoryColors[node.group] || categoryColors['default'])
          .nodeOpacity(0.95)
          .nodeResolution(20)
          .linkWidth(link => link.value * 0.8)
          .linkColor(link => {
            const intensity = Math.min(link.value / 10, 1);
            return `rgba(100, 255, 218, ${0.2 + intensity * 0.4})`;
          })
          .linkOpacity(0.7)
          .linkDirectionalParticles(link => Math.min(link.value * 2, 8))
          .linkDirectionalParticleWidth(link => 1 + link.value * 0.3)
          .linkDirectionalParticleSpeed(0.006)
          .linkDirectionalParticleColor(() => '#64FFDA')
          .backgroundColor('#0A192F')
          .showNavInfo(false)
          .enableNodeDrag(true)
          .enableNavigationControls(true)
          .width(elem.clientWidth)
          .height(elem.clientHeight)
          .nodeThreeObject(node => {
            if (typeof THREE === 'undefined') return null;
            
            try {
              const sprite = new THREE.Sprite(
                new THREE.SpriteMaterial({
                  map: new THREE.CanvasTexture(createGlowTexture(node)),
                  transparent: true,
                  blending: THREE.AdditiveBlending
                })
              );
              sprite.scale.set(12, 12, 1);
              return sprite;
            } catch (e) {
              console.warn('Failed to create glow sprite:', e);
              return null;
            }
          })
          .onNodeClick(node => {
            document.getElementById('node-title').textContent = node.name;
            document.getElementById('node-category').textContent = node.group || 'default';
            document.getElementById('node-connections').textContent = `연결: ${node.connections}개`;
            
            const nodeLink = document.getElementById('node-link');
            nodeLink.href = node.url;
            nodeLink.onclick = (e) => {
              e.preventDefault();
              window.open(node.url, '_blank');
            };
            
            const topConnectionsList = document.getElementById('top-connections-list');
            topConnectionsList.innerHTML = '';
            
            const connectedEdges = data.links.filter(link => 
              link.source.id === node.id || link.target.id === node.id
            );
            
            const connectionMap = connectedEdges.map(link => {
              const connectedNode = link.source.id === node.id ? link.target : link.source;
              return {
                node: connectedNode,
                weight: link.value
              };
            });
            
            connectionMap.sort((a, b) => b.weight - a.weight);
            const top10 = connectionMap.slice(0, 10);
            
            top10.forEach(conn => {
              const li = document.createElement('li');
              li.style.margin = '3px 0';
              li.style.color = '#CCD6F6';
              li.innerHTML = `<span style="color: #64FFDA;">[${conn.weight}]</span> ${conn.node.name || conn.node.id}`;
              li.onclick = () => {
                if (conn.node.url) {
                  window.open(conn.node.url, '_blank');
                }
              };
              topConnectionsList.appendChild(li);
            });
            
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
          });

        setTimeout(() => {
          spinner.style.display = 'none';
        }, 2000);
        
      })
      .catch(error => {
        console.error('Error loading graph data:', error);
        spinner.style.display = 'none';
      });
  });
</script>
