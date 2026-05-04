---
title: "웰빙 코너"
layout: wide
permalink: /wellbeing/
---

<style>
.wb-hub{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem;margin:1.5rem 0}
.wb-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:1.5rem}
.wb-card--wide{grid-column:span 2}
.wb-card-header{display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem}
.wb-card-emoji{font-size:1.3em}
.wb-card-title{font-size:1em;font-weight:600;margin:0;border:none;padding:0}
.wb-card-desc{font-size:.83em;opacity:.6;margin-bottom:1rem}
.wb-card-actions{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.8rem}
.wb-timer-display{font-size:2.5rem;font-weight:300;letter-spacing:.05em;color:#82c8a0;margin:.8rem 0;font-variant-numeric:tabular-nums}
.wb-btn{padding:.4rem .9rem;border-radius:8px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);color:inherit;cursor:pointer;font-size:.88em}
.wb-btn:hover{background:rgba(255,255,255,.12)}
.wb-btn:disabled{opacity:.4;cursor:not-allowed}
.wb-btn-primary{background:rgba(130,200,160,.2);border-color:rgba(130,200,160,.5);color:#82c8a0}
.wb-btn-sm{padding:.25rem .6rem;font-size:.82em}
.wb-btn.active{background:rgba(130,200,160,.2);border-color:rgba(130,200,160,.5)}
.wb-sound-channels{display:flex;flex-direction:column;gap:.6rem;margin:.8rem 0}
.wb-sound-channel{display:flex;align-items:center;gap:.7rem}
.wb-sound-label{font-size:.85em;min-width:80px}
.wb-volume-slider{flex:1;accent-color:#82c8a0;cursor:pointer}
.wb-sound-footer{margin-top:.8rem;display:flex;gap:.5rem;align-items:center}
.wb-sound-footer select{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);color:inherit;padding:.3rem .5rem;border-radius:6px;font-size:.85em}
.wb-energy-buttons{display:flex;gap:.5rem;justify-content:space-between;margin:.8rem 0}
.wb-energy-btn{flex:1;background:none;border:1px solid rgba(255,255,255,.12);border-radius:10px;cursor:pointer;padding:.5rem .2rem;font-size:1.4em;text-align:center}
.wb-energy-tip{font-size:.85em;color:#82c8a0;min-height:1.2em;margin:.5rem 0}
.wb-chart-container{margin-top:1rem;max-height:180px}
.wb-gratitude-inputs{display:flex;flex-direction:column;gap:.5rem;margin-bottom:.8rem}
.wb-gratitude-input{width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.15);border-radius:8px;color:inherit;padding:.5rem .7rem;font-size:.88em;resize:vertical;font-family:inherit}
.wb-break-filters{display:flex;gap:.4rem;flex-wrap:wrap;margin:.8rem 0}
.wb-break-result{margin:.8rem 0;padding:.8rem;background:rgba(255,255,255,.04);border-radius:8px;min-height:3em}
.wb-break-text{font-size:.9em;margin:0}
.wb-break-type{font-size:.75em;opacity:.6}
.wb-pomo-settings{display:flex;gap:1rem;margin-bottom:.5rem}
.wb-pomo-settings label{font-size:.85em;display:flex;align-items:center;gap:.3rem}
.wb-pomo-settings input[type=number]{width:52px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);color:inherit;padding:.2rem .4rem;border-radius:6px;font-size:.88em;text-align:center}
.wb-pomo-status{font-size:.85em;opacity:.7;margin:.3rem 0}
.wb-emotion-row{display:flex;gap:.3rem;flex-wrap:wrap}
.wb-emotion-btn{background:none;border:1px solid rgba(255,255,255,.15);border-radius:8px;cursor:pointer;font-size:1.3em;padding:.2rem .3rem}
.wb-prescription{font-size:.82em;color:#82c8a0;min-height:1.2em;margin-top:.5rem;opacity:0;transition:opacity .4s}
.wb-prescription--show{opacity:1}
.wb-affirmation-text{font-size:.9em;font-style:italic;line-height:1.6;margin-bottom:.8rem;min-height:2em}
.wb-sound-select{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);color:inherit;padding:.3rem .5rem;border-radius:6px;font-size:.85em}
@media(max-width:768px){.wb-card--wide{grid-column:span 1}}
</style>

<div class="wb-hub">

  <!-- 1. 1분 고요 호흡 -->
  <div class="wb-card" id="wb-hub-breath">
    <div class="wb-card-header"><span class="wb-card-emoji">💨</span><h3 class="wb-card-title">1분 고요 호흡</h3></div>
    <p class="wb-card-desc">잠깐 멈추고 숨 한 번 고르세요.</p>
    <div class="wb-timer-display">01:00</div>
    <div class="wb-card-actions">
      <button class="wb-btn wb-btn-primary wb-breath-start" type="button">시작</button>
      <button class="wb-btn wb-breath-reset" type="button">리셋</button>
    </div>
  </div>

  <!-- 2. 3분 집중 명상 -->
  <div class="wb-card" id="wb-hub-meditation">
    <div class="wb-card-header"><span class="wb-card-emoji">🧘</span><h3 class="wb-card-title">3분 집중 명상</h3></div>
    <p class="wb-card-desc">배경음과 함께 3분 명상.</p>
    <div class="wb-timer-display">03:00</div>
    <div class="wb-card-actions">
      <select class="wb-sound-select">
        <option value="none">배경음 없음</option>
        <option value="whitenoise">백색소음</option>
        <option value="rain">빗소리</option>
        <option value="ocean">파도소리</option>
      </select>
      <button class="wb-btn wb-btn-primary wb-breath-meditation-start" type="button">시작</button>
      <button class="wb-btn wb-breath-meditation-reset" type="button">리셋</button>
    </div>
  </div>

  <!-- 3. 소리 풍경 -->
  <div class="wb-card wb-card--wide" id="wb-hub-sound">
    <div class="wb-card-header"><span class="wb-card-emoji">🎵</span><h3 class="wb-card-title">소리 풍경</h3></div>
    <p class="wb-card-desc">원하는 소리를 조합해 나만의 배경음을 만드세요.</p>
    <div class="wb-sound-channels">
      <div class="wb-sound-channel">
        <span class="wb-sound-label">🌧 빗소리</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="rain" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="rain" type="range" min="0" max="100" value="50">
      </div>
      <div class="wb-sound-channel">
        <span class="wb-sound-label">🌊 파도소리</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="ocean" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="ocean" type="range" min="0" max="100" value="50">
      </div>
      <div class="wb-sound-channel">
        <span class="wb-sound-label">📻 백색소음</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="whitenoise" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="whitenoise" type="range" min="0" max="100" value="50">
      </div>
      <div class="wb-sound-channel">
        <span class="wb-sound-label">🐦 새소리</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="bird" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="bird" type="range" min="0" max="100" value="50">
      </div>
      <div class="wb-sound-channel">
        <span class="wb-sound-label">💨 바람소리</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="wind" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="wind" type="range" min="0" max="100" value="50">
      </div>
      <div class="wb-sound-channel">
        <span class="wb-sound-label">🔔 종소리</span>
        <button class="wb-sound-toggle wb-btn wb-btn-sm" data-channel="bell" type="button">OFF</button>
        <input class="wb-volume-slider" data-channel="bell" type="range" min="0" max="100" value="50">
      </div>
    </div>
    <div class="wb-sound-footer">
      <select class="wb-sound-timer">
        <option value="0">무제한</option>
        <option value="300">5분</option>
        <option value="600">10분</option>
        <option value="900">15분</option>
      </select>
    </div>
  </div>

  <!-- 4. 감정 날씨 -->
  <div class="wb-card" id="wb-hub-emotion">
    <div class="wb-card-header"><span class="wb-card-emoji">🌤</span><h3 class="wb-card-title">감정 날씨</h3></div>
    <p class="wb-card-desc">지금 내 마음의 날씨는?</p>
    <div class="wb-emotion-row">
      <button class="wb-emotion-btn" data-emotion="sunny"        type="button" title="맑음">☀️</button>
      <button class="wb-emotion-btn" data-emotion="cloudy_light" type="button" title="구름조금">⛅</button>
      <button class="wb-emotion-btn" data-emotion="cloudy"       type="button" title="흐림">☁️</button>
      <button class="wb-emotion-btn" data-emotion="rainy"        type="button" title="비">🌧️</button>
      <button class="wb-emotion-btn" data-emotion="storm"        type="button" title="폭풍">⛈️</button>
    </div>
    <p class="wb-prescription"></p>
  </div>

  <!-- 5. 오늘의 다독임 -->
  <div class="wb-card" id="wb-hub-affirmation">
    <div class="wb-card-header"><span class="wb-card-emoji">💬</span><h3 class="wb-card-title">오늘의 다독임</h3></div>
    <p class="wb-card-desc">짧은 위로 한 마디.</p>
    <p class="wb-affirmation-text"></p>
    <button class="wb-btn wb-btn-sm wb-affirmation-btn" type="button">새 다독임</button>
  </div>

  <!-- 6. 감사 일기 -->
  <div class="wb-card wb-card--wide" id="wb-hub-gratitude">
    <div class="wb-card-header"><span class="wb-card-emoji">📓</span><h3 class="wb-card-title">감사 일기</h3></div>
    <p class="wb-card-desc">오늘 감사한 것 세 가지를 적어보세요.</p>
    <div class="wb-gratitude-inputs">
      <textarea class="wb-gratitude-input" placeholder="감사한 것 1..." rows="2"></textarea>
      <textarea class="wb-gratitude-input" placeholder="감사한 것 2..." rows="2"></textarea>
      <textarea class="wb-gratitude-input" placeholder="감사한 것 3..." rows="2"></textarea>
    </div>
    <button class="wb-btn wb-btn-primary wb-gratitude-save" type="button">저장하기</button>
    <div class="wb-gratitude-history"></div>
  </div>

  <!-- 7. 에너지 트래커 -->
  <div class="wb-card wb-card--wide" id="wb-hub-energy">
    <div class="wb-card-header"><span class="wb-card-emoji">⚡</span><h3 class="wb-card-title">에너지 트래커</h3></div>
    <p class="wb-card-desc">오늘의 에너지 레벨을 기록하세요.</p>
    <div class="wb-energy-buttons">
      <button class="wb-energy-btn" data-level="1" type="button">😩<br><small>매우 낮음</small></button>
      <button class="wb-energy-btn" data-level="2" type="button">😟<br><small>낮음</small></button>
      <button class="wb-energy-btn" data-level="3" type="button">🙂<br><small>보통</small></button>
      <button class="wb-energy-btn" data-level="4" type="button">😊<br><small>높음</small></button>
      <button class="wb-energy-btn" data-level="5" type="button">🤩<br><small>매우 높음</small></button>
    </div>
    <p class="wb-energy-tip"></p>
    <div class="wb-chart-container">
      <canvas id="wb-energy-chart"></canvas>
    </div>
  </div>

  <!-- 8. 집중-휴식 타이머 (뽀모도로) -->
  <div class="wb-card" id="wb-hub-pomodoro">
    <div class="wb-card-header"><span class="wb-card-emoji">🍅</span><h3 class="wb-card-title">집중-휴식 타이머</h3></div>
    <p class="wb-card-desc">집중과 휴식의 리듬을 만들어요.</p>
    <div class="wb-pomo-settings">
      <label>집중 <input class="wb-pomo-focus" type="number" value="25" min="1" max="60">분</label>
      <label>휴식 <input class="wb-pomo-break" type="number" value="5" min="1" max="30">분</label>
    </div>
    <div class="wb-timer-display wb-pomo-display">25:00</div>
    <p class="wb-pomo-status">대기 중</p>
    <div class="wb-card-actions">
      <button class="wb-btn wb-btn-primary wb-pomo-start" type="button">시작</button>
      <button class="wb-btn wb-pomo-pause" type="button" disabled>일시정지</button>
      <button class="wb-btn wb-pomo-reset" type="button">초기화</button>
    </div>
  </div>

  <!-- 9. 쉬는 시간 활동 추천 -->
  <div class="wb-card" id="wb-hub-break">
    <div class="wb-card-header"><span class="wb-card-emoji">🎲</span><h3 class="wb-card-title">쉬는 시간 활동 추천</h3></div>
    <p class="wb-card-desc">어떤 종류의 활동을 원하세요?</p>
    <div class="wb-break-filters">
      <button class="wb-break-filter wb-btn wb-btn-sm active" data-type="전체" type="button">전체</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="휴식" type="button">휴식</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="교육" type="button">교육</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="사교" type="button">사교</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="레크리에이션" type="button">레크리에이션</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="만들기" type="button">만들기</button>
      <button class="wb-break-filter wb-btn wb-btn-sm" data-type="음악" type="button">음악</button>
    </div>
    <div class="wb-break-result">
      <p class="wb-break-text">버튼을 눌러 활동을 추천받으세요</p>
      <span class="wb-break-type"></span>
    </div>
    <button class="wb-btn wb-btn-primary wb-break-next" type="button">다른 활동 보기</button>
  </div>

</div>

<!-- Chart.js (에너지 트래커용) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
