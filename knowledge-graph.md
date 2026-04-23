---
layout: wide
title: "지식 그래프 3D (Knowledge Graph 3D)"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background-color: #0f0f13 !important;
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
    color: #a78bfa;
  }
  .page--knowledge-graph #main {
    margin-left: 320px;
  }

  #info-panel {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(18, 18, 26, 0.97);
    border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 8px;
    padding: 14px 18px;
    color: #c4c4d4;
    font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
    font-size: 13px;
    z-index: 100;
    max-width: 320px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.6);
    display: none;
    backdrop-filter: blur(12px);
  }

  #info-panel h3 {
    margin: 0 0 10px 0;
    color: #e2e2f0;
    font-size: 15px;
    font-weight: 600;
    border-bottom: 1px solid rgba(139, 92, 246, 0.25);
    padding-bottom: 8px;
    line-height: 1.4;
  }

  #info-panel p {
    margin: 5px 0;
    line-height: 1.6;
  }

  #info-panel .category {
    display: inline-block;
    background: rgba(139, 92, 246, 0.15);
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    color: #a78bfa;
    border: 1px solid rgba(139, 92, 246, 0.3);
  }

  #top-connections-list li {
    cursor: pointer;
    transition: background 0.15s ease;
    padding: 4px 6px;
    border-radius: 4px;
    color: #b0b0c8;
  }

  #top-connections-list li:hover {
    background: rgba(139, 92, 246, 0.1);
    color: #e2e2f0;
  }

  #node-link {
    transition: all 0.2s ease;
    color: #a78bfa !important;
    text-decoration: none;
    font-size: 12px;
    border: 1px solid rgba(139, 92, 246, 0.4);
    padding: 5px 10px;
    border-radius: 4px;
    display: inline-block;
  }

  #node-link:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.7);
  }

  #controls-panel {
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: rgba(18, 18, 26, 0.92);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 8px;
    padding: 12px 16px;
    color: #888899;
    font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
    font-size: 12px;
    z-index: 100;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
  }

  #controls-panel h4 {
    margin: 0 0 8px 0;
    color: #a78bfa;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    padding-bottom: 6px;
  }

  #controls-panel ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  #controls-panel li {
    margin: 6px 0;
    color: #888899;
    line-height: 1.4;
  }

  .loader {
    border: 3px solid rgba(139, 92, 246, 0.15);
    border-top: 3px solid #a78bfa;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -20px;
    margin-left: -20px;
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
    gap: 8px;
    z-index: 101;
  }

  .nav-btn {
    background: rgba(18, 18, 26, 0.92);
    border: 1px solid rgba(139, 92, 246, 0.3);
    color: #a78bfa;
    padding: 7px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
    font-size: 13px;
    transition: all 0.2s ease;
    backdrop-filter: blur(12px);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }

  .nav-btn:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.6);
    color: #c4b5fd;
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
      <strong style="color: #a78bfa;">주요 연결:</strong>
      <ul id="top-connections-list" style="margin: 5px 0; padding-left: 20px; list-style: none;"></ul>
    </div>
    <p style="margin-top: 10px;">
      <a id="node-link" href="#" target="_blank">
        본 게시물로 이동 →
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
          'AI': '#8b5cf6',
          '교육': '#6366f1',
          '학습과학': '#3b82f6',
          '철학': '#ec4899',
          '코딩': '#10b981',
          '인지과학': '#f59e0b',
          '바이브코딩': '#06b6d4',
          'tag': '#52525b',
          'default': '#6b6b8a'
        };

        const Graph = ForceGraph3D()(elem);
        
        Graph
          .graphData(data)
          .nodeLabel(node => `<div style="background: rgba(15,15,22,0.95); padding: 6px 10px; border-radius: 4px; border: 1px solid rgba(139,92,246,0.4); color: #e2e2f0; font-family: -apple-system, sans-serif; font-size: 12px;">${node.name}</div>`)
          .nodeVal(node => Math.pow(node.connections + 1, 0.6) * 5)
          .nodeColor(node => categoryColors[node.group] || categoryColors['default'])
          .nodeOpacity(0.85)
          .nodeResolution(16)
          .linkWidth(link => Math.max(link.value * 0.6, 0.2))
          .linkColor(() => 'rgba(100, 100, 130, 0.25)')
          .linkOpacity(0.5)
          .linkDirectionalParticles(link => Math.min(link.value * 1.5, 4))
          .linkDirectionalParticleWidth(link => 0.5 + link.value * 0.15)
          .linkDirectionalParticleSpeed(0.004)
          .linkDirectionalParticleColor(() => 'rgba(167, 139, 250, 0.7)')
          .backgroundColor('#0f0f13')
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
              li.innerHTML = `<span style="color: #a78bfa; font-size: 10px;">[${conn.weight}]</span> ${conn.node.name || conn.node.id}`;
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
