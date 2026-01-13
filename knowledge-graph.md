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

  #controls-panel {
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: rgba(10, 25, 47, 0.95);
    border: 2px solid #64FFDA;
    border-radius: 10px;
    padding: 15px 20px;
    color: #CCD6F6;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    z-index: 100;
    box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
    backdrop-filter: blur(10px);
  }

  #controls-panel h4 {
    margin: 0 0 10px 0;
    color: #64FFDA;
    font-size: 15px;
    border-bottom: 1px solid #64FFDA;
    padding-bottom: 5px;
  }

  #controls-panel ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  #controls-panel li {
    margin: 8px 0;
    color: #CCD6F6;
    line-height: 1.4;
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

  #nav-buttons {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 101;
  }

  .nav-btn {
    background: rgba(10, 25, 47, 0.95);
    border: 2px solid #64FFDA;
    color: #64FFDA;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 13px;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
    backdrop-filter: blur(10px);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }

  .nav-btn:hover {
    background: rgba(100, 255, 218, 0.2);
    box-shadow: 0 0 25px rgba(100, 255, 218, 0.6);
    transform: translateY(-2px);
  }
</style>

<script src="https://unpkg.com/three@0.149.0/build/three.min.js"></script>
<script src="https://unpkg.com/d3@7"></script>
<script src="https://unpkg.com/3d-force-graph@1.73.3"></script>

<div id="graph-wrapper" style="width: 100%; height: 100vh; position: relative;">
  <div id="nav-buttons">
    <a href="/" class="nav-btn">
      <span>🏠</span>
      <span>홈</span>
    </a>
    <button class="nav-btn" onclick="window.history.back()">
      <span>←</span>
      <span>이전</span>
    </button>
  </div>
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

  <div id="controls-panel">
    <h4>🎮 조작법</h4>
    <ul>
      <li>🖱️ 드래그: 회전</li>
      <li>🔍 스크롤: 줌</li>
      <li>👆 클릭: 정보 표시</li>
    </ul>
  </div>

</div>

<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    const elem = document.getElementById('3d-graph');
    const spinner = document.getElementById('graph-spinner');
    const infoPanel = document.getElementById('info-panel');

    fetch('/knowledge-graph.json')
      .then(response => response.json())
      .then(graphData => {
        
        graphData.edges = graphData.edges.filter(edge => edge.from && edge.to);

        const edges = graphData.edges.map(edge => ({
          source: edge.from,
          target: edge.to,
          value: edge.value || 1
        }));

        // 구형 뇌 신경망 3D 분포 함수
        function getBrainPosition(index, total) {
          const goldenRatio = (1 + Math.sqrt(5)) / 2;
          const angleIncrement = Math.PI * 2 * goldenRatio;
          
          const t = index / total;
          const inclination = Math.acos(1 - 2 * t);
          const azimuth = angleIncrement * index;
          
          const baseRadius = 400;
          const radiusVariation = 1 + Math.sin(inclination * 8) * 0.15 + Math.sin(azimuth * 6) * 0.1;
          const radius = baseRadius * radiusVariation;
          
          let x = radius * Math.sin(inclination) * Math.cos(azimuth);
          let y = radius * Math.sin(inclination) * Math.sin(azimuth);
          let z = radius * Math.cos(inclination);
          
          const wrinkleFreq = 12;
          const wrinkleAmp = 30;
          const wrinkle = Math.sin(inclination * wrinkleFreq) * Math.cos(azimuth * wrinkleFreq) * wrinkleAmp;
          
          const wrinkleDir = {
            x: Math.sin(inclination) * Math.cos(azimuth),
            y: Math.sin(inclination) * Math.sin(azimuth),
            z: Math.cos(inclination)
          };
          
          x += wrinkle * wrinkleDir.x;
          y += wrinkle * wrinkleDir.y;
          z += wrinkle * wrinkleDir.z;
          
          x += (Math.random() - 0.5) * 60;
          y += (Math.random() - 0.5) * 60;
          z += (Math.random() - 0.5) * 60;
          
          return { x, y, z };
        }
        
        const nodes = graphData.nodes.map((node, index) => {
          const nodeEdges = edges.filter(e => e.source === node.id || e.target === node.id);
          const degree = nodeEdges.length;
          const pos = getBrainPosition(index, graphData.nodes.length);
          
          return {
            id: node.id,
            name: node.label,
            group: node.group,
            url: node.url,
            val: Math.max(degree * 3 + 5, 5),
            connections: degree,
            edges: nodeEdges,
            x: pos.x,
            y: pos.y,
            z: pos.z
          };
        });
        
        console.log('Nodes loaded:', nodes.length);
        console.log('Edges loaded:', edges.length);

        const data = {
          nodes: nodes,
          links: edges
        };

        const categoryColors = {
          'AI': '#A78BFA',
          'Machine Learning': '#60A5FA',
          'Deep Learning': '#F472B6',
          'NLP': '#34D399',
          'Computer Vision': '#FBBF24',
          'Robotics': '#FB923C',
          'default': '#64FFDA'
        };

        const Graph = ForceGraph3D()(elem);
        
        Graph
          .graphData(data)
          .nodeLabel(node => `<div style="background: rgba(10, 25, 47, 0.95); padding: 8px 12px; border-radius: 6px; border: 2px solid #64FFDA; color: #CCD6F6; font-family: 'Consolas', monospace; font-size: 14px; font-weight: bold; box-shadow: 0 0 20px rgba(100, 255, 218, 0.5);">${node.name}</div>`)
          .nodeVal(node => Math.pow(node.connections + 1, 0.6) * 5)
          .nodeColor(node => categoryColors[node.group] || categoryColors['default'])
          .nodeOpacity(0.9)
          .nodeResolution(16)
          .linkWidth(link => Math.max(link.value * 1.2, 0.4))
          .linkColor(() => 'rgba(148, 163, 184, 0.4)')
          .linkOpacity(0.6)
          .linkDirectionalParticles(link => Math.min(link.value * 1.5, 6))
          .linkDirectionalParticleWidth(link => 0.8 + link.value * 0.2)
          .linkDirectionalParticleSpeed(0.005)
          .linkDirectionalParticleColor(() => 'rgba(100, 255, 218, 0.6)')
          .backgroundColor('#0A192F')
          .showNavInfo(false)
          .enableNodeDrag(true)
          .enableNavigationControls(true)
          .width(elem.clientWidth)
          .height(elem.clientHeight);
        
        Graph
          .d3Force('charge', d3.forceManyBody().strength(-400).distanceMax(600))
          .d3Force('link', d3.forceLink().distance(link => {
            const baseDistance = 120;
            const similarityFactor = Math.max(0.6, 6 - link.value);
            return baseDistance * similarityFactor;
          }).strength(0.5))
          .d3Force('center', d3.forceCenter())
          .d3Force('collision', d3.forceCollide().radius(node => Math.pow(node.connections + 1, 0.6) * 8).strength(0.6))
          .d3Force('sphere', function(alpha) {
            const brainRadius = 400;
            const strength = 0.02 * alpha;
            
            nodes.forEach(node => {
              const dist = Math.sqrt(node.x*node.x + node.y*node.y + node.z*node.z);
              
              if (dist > brainRadius * 1.3) {
                const factor = strength * (dist / brainRadius - 1.3);
                node.vx -= node.x * factor / dist;
                node.vy -= node.y * factor / dist;
                node.vz -= node.z * factor / dist;
              }
              else if (dist < brainRadius * 0.5) {
                const factor = strength * (0.5 - dist / brainRadius);
                node.vx += node.x * factor / (dist + 1);
                node.vy += node.y * factor / (dist + 1);
                node.vz += node.z * factor / (dist + 1);
              }
            });
          })
          .cooldownTime(8000)
          .warmupTicks(100);
        
        Graph.onNodeClick(node => {
          try {
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
          } catch (e) {
            console.error('Node click error:', e);
          }
        });
        
        Graph.onNodeDblClick(node => {
          if (node.url) {
            window.open(node.url, '_blank');
          }
        });
        
        Graph.onBackgroundClick(() => {
          infoPanel.style.display = 'none';
        });
        
        Graph.d3Force('link').links(data.links);
        Graph.d3ReheatSimulation();
        
        console.log('✓ Graph initialized successfully');

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
