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

  #stats-panel {
    position: absolute;
    bottom: 20px;
    left: 20px;
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
    min-width: 250px;
  }

  #stats-panel h4 {
    margin: 0 0 10px 0;
    color: #64FFDA;
    font-size: 14px;
    border-bottom: 1px solid #64FFDA;
    padding-bottom: 5px;
  }

  #stats-panel .stat-item {
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
  }

  #stats-panel .stat-label {
    color: #8892B0;
  }

  #stats-panel .stat-value {
    color: #64FFDA;
    font-weight: bold;
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

  <div id="stats-panel">
    <h4>📊 네트워크 통계</h4>
    <div class="stat-item">
      <span class="stat-label">노드 수:</span>
      <span class="stat-value" id="stat-nodes">0</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">엣지 수:</span>
      <span class="stat-value" id="stat-edges">0</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">평균 연결도:</span>
      <span class="stat-value" id="stat-avg-degree">0</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">네트워크 밀도:</span>
      <span class="stat-value" id="stat-density">0</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">최대 연결 노드:</span>
      <span class="stat-value" id="stat-max-node" style="font-size: 10px;">-</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">고립 노드:</span>
      <span class="stat-value" id="stat-isolated">0</span>
    </div>
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

        // 구형 뇌 신경망 3D 분포 함수 (폭과 깊이 확대)
        function getBrainPosition(index, total) {
          // 피보나치 구 분포 알고리즘 (균등 분포)
          const goldenRatio = (1 + Math.sqrt(5)) / 2;
          const angleIncrement = Math.PI * 2 * goldenRatio;
          
          const t = index / total;
          const inclination = Math.acos(1 - 2 * t);
          const azimuth = angleIncrement * index;
          
          // 구형 뇌 반지름 (폭과 깊이 대폭 확대)
          const baseRadius = 400;  // 기본 반지름 2배 증가
          
          // 반지름에 약간의 변화를 주어 뇌 표면의 불규칙성 표현
          const radiusVariation = 1 + Math.sin(inclination * 8) * 0.15 + Math.sin(azimuth * 6) * 0.1;
          const radius = baseRadius * radiusVariation;
          
          // 구면 좌표를 직교 좌표로 변환
          let x = radius * Math.sin(inclination) * Math.cos(azimuth);
          let y = radius * Math.sin(inclination) * Math.sin(azimuth);
          let z = radius * Math.cos(inclination);
          
          // 뇌의 주름 효과 (대뇌 피질)
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
          
          // 약간의 랜덤성 추가 (신경망의 자연스러움)
          x += (Math.random() - 0.5) * 60;
          y += (Math.random() - 0.5) * 60;
          z += (Math.random() - 0.5) * 60;
          
          return { x, y, z };
        }
        
        const nodes = graphData.nodes.map((node, index) => {
          const nodeEdges = edges.filter(e => e.source === node.id || e.target === node.id);
          const degree = nodeEdges.length;
          
          // 뇌 모양 3D 공간에 초기 위치 배치
          const pos = getBrainPosition(index, graphData.nodes.length);
          
          return {
            id: node.id,
            name: node.label,
            group: node.group,
            url: node.url,
            val: Math.max(degree * 3 + 5, 5),  // 연결 많은 노드 크기 차별화 강화
            connections: degree,
            edges: nodeEdges,
            x: pos.x,
            y: pos.y,
            z: pos.z
          };
        });
        
        console.log('Nodes loaded:', nodes.length);
        console.log('Edges loaded:', edges.length);

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

        // ForceGraph3D 초기화
        const Graph = ForceGraph3D()(elem);
        
        // 그래프 데이터 및 기본 설정
        Graph
          .graphData(data)
          .nodeLabel('name')
          .nodeVal(node => Math.pow(node.connections + 1, 0.6) * 5)
          .nodeColor(node => categoryColors[node.group] || categoryColors['default'])
          .nodeOpacity(0.95)
          .nodeResolution(20)
          .linkWidth(link => Math.max(link.value * 1.5, 0.5))
          .linkColor(link => {
            const intensity = Math.min(link.value / 5, 1);
            return `rgba(100, 255, 218, ${0.3 + intensity * 0.5})`;
          })
          .linkOpacity(0.8)
          .linkDirectionalParticles(link => Math.min(link.value * 2, 8))
          .linkDirectionalParticleWidth(link => 1 + link.value * 0.3)
          .linkDirectionalParticleSpeed(0.006)
          .linkDirectionalParticleColor(() => '#64FFDA')
          .backgroundColor('#0A192F')
          .showNavInfo(false)
          .enableNodeDrag(true)
          .enableNavigationControls(true)
          .width(elem.clientWidth)
          .height(elem.clientHeight);
        
        // D3 포스 설정
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
        
        // 노드 클릭 이벤트 (모달창 표시)
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
        
        // 노드 더블클릭 이벤트 (페이지 이동)
        Graph.onNodeDblClick(node => {
          if (node.url) {
            window.open(node.url, '_blank');
          }
        });
        
        // 배경 클릭 시 모달창 닫기
        Graph.onBackgroundClick(() => {
          infoPanel.style.display = 'none';
        });
        
        // 링크 포스 설정
        Graph.d3Force('link').links(data.links);
        
        // 시뮬레이션 재가열
        Graph.d3ReheatSimulation();
        
        console.log('✓ Graph initialized successfully');

        // ===== 분석 알고리즘 구현 =====
        
        // 1. 중심성 분석 (Centrality Analysis)
        function calculateCentrality() {
          // Degree Centrality (이미 계산됨)
          nodes.forEach(node => {
            node.degreeCentrality = node.connections;
          });
          
          // Betweenness Centrality - 노드가 많으면 생략 (성능 이슈)
          if (nodes.length < 100) {
            const betweenness = {};
            nodes.forEach(n => betweenness[n.id] = 0);
            
            // 샘플링된 노드 쌍만 계산
            const sampleSize = Math.min(nodes.length, 50);
            const sampledNodes = nodes.slice(0, sampleSize);
            
            sampledNodes.forEach(source => {
              sampledNodes.forEach(target => {
                if (source.id !== target.id) {
                  const paths = findAllPaths(source.id, target.id, data);
                  paths.forEach(path => {
                    path.slice(1, -1).forEach(nodeId => {
                      betweenness[nodeId] += 1 / paths.length;
                    });
                  });
                }
              });
            });
            
            nodes.forEach(node => {
              node.betweennessCentrality = betweenness[node.id] || 0;
            });
          }
          
          // PageRank (간단한 버전)
          const pagerank = simplePageRank(data, 10);
          nodes.forEach(node => {
            node.pagerank = pagerank[node.id] || 0;
          });
        }
        
        function simplePageRank(graph, iterations = 10) {
          const d = 0.85;
          const N = graph.nodes.length;
          const ranks = {};
          
          graph.nodes.forEach(node => ranks[node.id] = 1 / N);
          
          for (let i = 0; i < iterations; i++) {
            const newRanks = {};
            graph.nodes.forEach(node => newRanks[node.id] = (1 - d) / N);
            
            graph.links.forEach(link => {
              const sourceId = link.source.id || link.source;
              const targetId = link.target.id || link.target;
              const sourceNode = graph.nodes.find(n => n.id === sourceId);
              const outDegree = graph.links.filter(l => 
                (l.source.id || l.source) === sourceId
              ).length;
              
              if (outDegree > 0) {
                newRanks[targetId] += d * ranks[sourceId] / outDegree;
              }
            });
            
            Object.assign(ranks, newRanks);
          }
          
          return ranks;
        }
        
        // 2. 커뮤니티 탐지 (Community Detection) - Louvain-like algorithm
        function detectCommunities() {
          const communities = {};
          let communityId = 0;
          
          nodes.forEach(node => {
            if (!communities[node.id]) {
              const community = [];
              const visited = new Set();
              const queue = [node.id];
              
              while (queue.length > 0) {
                const current = queue.shift();
                if (visited.has(current)) continue;
                visited.add(current);
                community.push(current);
                
                const neighbors = data.links
                  .filter(l => (l.source.id || l.source) === current || (l.target.id || l.target) === current)
                  .map(l => {
                    const sourceId = l.source.id || l.source;
                    const targetId = l.target.id || l.target;
                    return sourceId === current ? targetId : sourceId;
                  })
                  .filter(n => !visited.has(n));
                
                // 강한 연결만 커뮤니티로 포함
                neighbors.forEach(neighbor => {
                  const edge = data.links.find(l => {
                    const sourceId = l.source.id || l.source;
                    const targetId = l.target.id || l.target;
                    return (sourceId === current && targetId === neighbor) ||
                           (sourceId === neighbor && targetId === current);
                  });
                  if (edge && edge.value >= 2) {
                    queue.push(neighbor);
                  }
                });
              }
              
              community.forEach(nodeId => {
                communities[nodeId] = communityId;
              });
              communityId++;
            }
          });
          
          nodes.forEach(node => {
            node.community = communities[node.id];
          });
          
          return communityId;
        }
        
        // 3. 경로 탐색 (Path Finding) - BFS
        function findShortestPath(startId, endId) {
          const queue = [[startId]];
          const visited = new Set([startId]);
          
          while (queue.length > 0) {
            const path = queue.shift();
            const current = path[path.length - 1];
            
            if (current === endId) {
              return path;
            }
            
            const neighbors = data.links
              .filter(l => {
                const sourceId = l.source.id || l.source;
                const targetId = l.target.id || l.target;
                return sourceId === current || targetId === current;
              })
              .map(l => {
                const sourceId = l.source.id || l.source;
                const targetId = l.target.id || l.target;
                return sourceId === current ? targetId : sourceId;
              });
            
            neighbors.forEach(neighbor => {
              if (!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push([...path, neighbor]);
              }
            });
          }
          
          return null;
        }
        
        function findAllPaths(startId, endId, graph, maxDepth = 3) {
          const paths = [];
          const visited = new Set();
          
          function dfs(current, target, path, depth) {
            if (depth > maxDepth) return;
            if (current === target) {
              paths.push([...path]);
              return;
            }
            
            visited.add(current);
            
            const neighbors = graph.links
              .filter(l => {
                const sourceId = l.source.id || l.source;
                const targetId = l.target.id || l.target;
                return sourceId === current || targetId === current;
              })
              .map(l => {
                const sourceId = l.source.id || l.source;
                const targetId = l.target.id || l.target;
                return sourceId === current ? targetId : sourceId;
              });
            
            neighbors.forEach(neighbor => {
              if (!visited.has(neighbor)) {
                dfs(neighbor, target, [...path, neighbor], depth + 1);
              }
            });
            
            visited.delete(current);
          }
          
          dfs(startId, endId, [startId], 0);
          return paths.slice(0, 5);
        }
        
        // 네트워크 통계 계산 (완전 재작성)
        function calculateStatistics() {
          console.log('=== Calculating Network Statistics ===');
          
          const nodeCount = nodes.length;
          const edgeCount = data.links.length;
          
          console.log('Raw data:', { nodeCount, edgeCount });
          
          // 평균 연결도 = (총 엣지 수 × 2) / 노드 수
          const avgDegree = nodeCount > 0 ? ((edgeCount * 2) / nodeCount).toFixed(2) : 0;
          
          // 네트워크 밀도 = 실제 엣지 수 / 가능한 최대 엣지 수
          const maxPossibleEdges = nodeCount * (nodeCount - 1) / 2;
          const density = maxPossibleEdges > 0 ? (edgeCount / maxPossibleEdges).toFixed(4) : 0;
          
          // 최대 연결 노드 찾기
          let maxNode = nodes[0];
          nodes.forEach(node => {
            if (node.connections > maxNode.connections) {
              maxNode = node;
            }
          });
          
          // 고립 노드 (연결이 0인 노드)
          const isolatedNodes = nodes.filter(n => n.connections === 0).length;
          
          console.log('Calculated values:', {
            nodeCount,
            edgeCount,
            avgDegree,
            density,
            maxNodeName: maxNode.name,
            maxNodeConnections: maxNode.connections,
            isolatedNodes
          });
          
          // DOM 업데이트
          document.getElementById('stat-nodes').textContent = nodeCount;
          document.getElementById('stat-edges').textContent = edgeCount;
          document.getElementById('stat-avg-degree').textContent = avgDegree;
          document.getElementById('stat-density').textContent = density;
          document.getElementById('stat-max-node').textContent = maxNode.name;
          document.getElementById('stat-isolated').textContent = isolatedNodes;
          
          console.log('✓ Statistics updated in DOM');
        }
        
        // 통계 계산 및 표시
        calculateStatistics();

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
