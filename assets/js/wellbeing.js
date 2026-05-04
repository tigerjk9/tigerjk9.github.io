/* wellbeing.js — 교사 웰빙 기능 모음 */
(function(W) {
  'use strict';

  // ===== 유틸 =====
  const $ = id => document.getElementById(id);
  const rand = arr => arr[Math.floor(Math.random() * arr.length)];
  const pad = n => String(n).padStart(2, '0');
  const today = () => new Date().toISOString().slice(0, 10);
  const store = {
    get: k => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };

  // ===== 데이터 상수 =====
  const DATA = {
    affirmations: [
      "가르친다는 것은 두 번 배우는 것이다.",
      "오늘 내가 심은 씨앗이 언제 꽃 피울지 모른다.",
      "완벽한 교사보다 솔직한 교사가 낫다.",
      "쉬는 것도 일의 일부다.",
      "지금 이 순간에 집중하는 것으로 충분하다.",
      "모든 학생이 같은 속도로 자라지는 않는다.",
      "실수는 배움의 시작이다.",
      "당신의 존재 자체가 누군가에게 영향을 준다.",
      "내가 지쳐 있을 때 학생들도 느낀다. 먼저 나를 돌보자.",
      "작은 성공도 성공이다. 오늘 하나만 찾아보자.",
      "교육은 마라톤이지 단거리가 아니다.",
      "비교는 기쁨을 빼앗는다.",
      "내 교실에서 일어나는 일은 세상에서 가장 중요한 일 중 하나다.",
      "지금 잘 하고 있다.",
      "완벽하지 않아도, 충분히 좋은 교사면 된다."
    ],
    prescriptions: {
      sunny:        ["이 에너지를 오늘 하루 나눠 쓰세요.", "기분 좋을 때 어려운 대화를 시도해보세요.", "오늘의 이 기분을 잠깐 글로 남겨두세요.", "동료에게 진심 어린 칭찬 한 마디 건네보세요.", "지금 이 맑음을 충분히 누리세요."],
      cloudy_light: ["완전히 맑지 않아도 괜찮아요.", "잠깐 창문 밖을 바라보는 시간을 가져보세요.", "점심은 혼자 조용히 드셔보세요.", "지금 느끼는 이 감정이 정답입니다.", "오늘 하루 작은 좋은 것 하나만 찾아보세요."],
      cloudy:       ["흐린 날은 쉬어가는 날입니다.", "따뜻한 물 한 잔이 생각보다 많이 도움이 됩니다.", "오늘은 기준을 조금 낮춰도 됩니다.", "다음 수업 계획은 내일의 나에게 맡기세요.", "잠깐 눈을 감고 호흡 세 번 해보세요."],
      rainy:        ["지금 이 감정, 지나갑니다.", "퇴근 후 좋아하는 것 하나만 하기로 약속해보세요.", "지금 당장 모든 걸 해결하지 않아도 됩니다.", "누군가에게 '힘들다'고 말하는 것도 용기입니다.", "버티고 있는 것만으로도 충분합니다."],
      storm:        ["지금 당장 아무것도 결정하지 마세요.", "잠깐 자리를 피해도 됩니다.", "이 감정이 당신을 지배하지만, 당신이 이 감정은 아닙니다.", "퇴근 후 전문가와 이야기 나눠보는 것도 방법입니다.", "숨을 천천히, 깊게. 그것만 지금 하세요."]
    },
    energyTips: {
      1: ["억지로 더 하려 하지 마세요. 지금은 쉬는 게 일입니다.", "물 한 잔 마시고 5분 앉아있기. 그게 전부여도 됩니다.", "오늘은 '최소한'만 하는 날로 정하세요.", "가벼운 스트레칭 2분이 도움이 됩니다.", "빠른 결정을 미루세요."],
      2: ["자연광 아래 5분만 있어보세요.", "점심 전화 없이 먹기 도전해보세요.", "오늘 가장 쉬운 것부터 시작하세요.", "짧은 산책 10분, 효과가 큽니다.", "퇴근 시간을 미리 정해두세요."],
      3: ["지금 이 상태를 유지하는 것으로 충분합니다.", "잠깐 눈 감고 호흡 3번 해보세요.", "오늘 완료한 것들을 되짚어보세요.", "동료와 짧은 잡담 한 번 나눠보세요.", "기존 루틴을 잘 마무리하는 날입니다."],
      4: ["이 에너지를 어려운 업무에 써보세요.", "동료를 도울 여유가 있는 날입니다.", "새로운 수업 아이디어를 메모해두기 좋습니다.", "퇴근 후 좋아하는 활동을 계획해보세요.", "오늘 일찍 쉬면 내일도 이어집니다."],
      5: ["지금 하고 싶었던 것을 시작해보세요.", "이런 날은 드뭅니다. 잘 기억해두세요.", "팀에 활력을 불어넣을 수 있는 날입니다.", "창의적인 기획에 이 에너지를 쓰세요.", "내일을 위한 에너지도 조금 아껴두세요."]
    },
    breakActivities: [
      {text: "책 한 챕터 읽기", type: "교육"},
      {text: "스트레칭 5분", type: "휴식"},
      {text: "좋아하는 음악 한 곡 듣기", type: "음악"},
      {text: "창밖 풍경 1분 바라보기", type: "휴식"},
      {text: "오래된 친구에게 메시지 보내기", type: "사교"},
      {text: "좋아하는 유튜브 영상 보기", type: "레크리에이션"},
      {text: "손글씨로 메모 쓰기", type: "만들기"},
      {text: "학교 텃밭이나 화분 물주기", type: "휴식"},
      {text: "관심 있는 뉴스 기사 하나 읽기", type: "교육"},
      {text: "커피나 차 한 잔 정성껏 내려 마시기", type: "휴식"},
      {text: "짧은 명상 앱 켜기", type: "휴식"},
      {text: "간단한 낙서나 스케치", type: "만들기"},
      {text: "동료와 짧은 잡담", type: "사교"},
      {text: "계단 오르내리기 3층", type: "레크리에이션"},
      {text: "내일 할 일 세 가지 적어보기", type: "교육"}
    ]
  };
  W.DATA = DATA;

  // ===== 공유 AudioContext =====
  let _ac = null;
  const getAC = () => {
    if (!_ac) {
      try { _ac = new (window.AudioContext || window.webkitAudioContext)(); } catch { _ac = null; }
    }
    return _ac;
  };

  // 노이즈 버퍼 (1초 분량 흰색 노이즈, 모든 노이즈 소스 공유)
  let _noiseBuf = null;
  const getNoiseBuffer = (ac) => {
    if (_noiseBuf) return _noiseBuf;
    const len = ac.sampleRate * 2;
    const buf = ac.createBuffer(1, len, ac.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    _noiseBuf = buf;
    return buf;
  };

  // ===== 인사말 =====
  W.greeting = {
    init() {
      const el = $('wb-greeting');
      if (!el) return;
      const h = new Date().getHours();
      let msg;
      if (h < 5)       msg = "아직 새벽이에요. 잠은 자야 합니다.";
      else if (h < 9)  msg = "좋은 아침이에요.";
      else if (h < 12) msg = "오전도 잘 하고 있어요.";
      else if (h < 14) msg = "점심 맛있게 드셨나요?";
      else if (h < 18) msg = "오후도 잘 버티고 있어요.";
      else if (h < 22) msg = "오늘도 수고 많았어요.";
      else             msg = "늦은 시간이에요. 곧 쉬어가세요.";
      el.textContent = msg;
    }
  };

  // ===== 다독임 (포스트 + 허브 양쪽) =====
  W.affirmation = {
    pick() { return rand(DATA.affirmations); },
    init() {
      const setOne = (textEl, btnEl) => {
        if (!textEl) return;
        textEl.textContent = this.pick();
        if (btnEl) {
          btnEl.addEventListener('click', () => { textEl.textContent = this.pick(); });
        }
      };
      setOne($('wb-affirmation-text'), $('wb-affirmation-btn'));
      const hub = $('wb-hub-affirmation');
      if (hub) {
        setOne(hub.querySelector('.wb-affirmation-text'), hub.querySelector('.wb-affirmation-btn'));
      }
    }
  };

  // ===== 감정 처방전 =====
  W.emotion = {
    init() {
      document.querySelectorAll('.wb-emotion-btn[data-emotion]').forEach(btn => {
        btn.addEventListener('click', () => {
          const key = btn.getAttribute('data-emotion');
          const list = DATA.prescriptions[key];
          if (!list) return;
          const wrapper = btn.closest('.wb-emotion, .wb-emotion-wrap, section, div');
          let target = null;
          if (wrapper) target = wrapper.querySelector('.wb-prescription');
          if (!target) target = document.querySelector('.wb-prescription');
          if (!target) return;
          target.textContent = rand(list);
          target.classList.add('wb-prescription--show');
        });
      });
    }
  };

  // ===== 호흡 타이머 (60초) =====
  W.breath = {
    init(rootId) {
      const root = $(rootId);
      if (!root) return;
      const display = root.querySelector('.wb-timer-display');
      const startBtn = root.querySelector('.wb-breath-start');
      const resetBtn = root.querySelector('.wb-breath-reset');
      if (!display || !startBtn) return;

      let remaining = 60;
      let timerId = null;
      const render = () => {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        display.textContent = `${pad(m)}:${pad(s)}`;
      };
      const stop = () => {
        if (timerId) { clearInterval(timerId); timerId = null; }
      };
      const finish = () => {
        stop();
        display.textContent = '완료 ✓';
        startBtn.disabled = false;
      };
      render();

      startBtn.addEventListener('click', () => {
        if (timerId) return;
        if (remaining <= 0) remaining = 60;
        startBtn.disabled = true;
        render();
        timerId = setInterval(() => {
          remaining--;
          if (remaining <= 0) finish();
          else render();
        }, 1000);
      });

      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          stop();
          remaining = 60;
          startBtn.disabled = false;
          render();
        });
      }
    }
  };

  // ===== 명상 (180초 + 배경음) =====
  W.meditation = {
    init() {
      const root = $('wb-hub-meditation');
      if (!root) return;
      const display = root.querySelector('.wb-timer-display');
      const startBtn = root.querySelector('.wb-breath-start') || root.querySelector('.wb-meditation-start');
      const resetBtn = root.querySelector('.wb-breath-reset') || root.querySelector('.wb-meditation-reset');
      const select = root.querySelector('.wb-sound-select');
      if (!display || !startBtn) return;

      let remaining = 180;
      let timerId = null;
      let nodes = null;

      const render = () => {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        display.textContent = `${pad(m)}:${pad(s)}`;
      };

      const stopSound = () => {
        if (!nodes) return;
        try { nodes.src && nodes.src.stop(); } catch {}
        try { nodes.lfo && nodes.lfo.stop(); } catch {}
        try { nodes.gain && nodes.gain.disconnect(); } catch {}
        nodes = null;
      };

      const startSound = (kind) => {
        const ac = getAC();
        if (!ac || kind === 'none') return;
        const buf = getNoiseBuffer(ac);
        const src = ac.createBufferSource();
        src.buffer = buf;
        src.loop = true;
        const gain = ac.createGain();
        gain.gain.value = 0.3;

        if (kind === 'whitenoise') {
          src.connect(gain).connect(ac.destination);
          src.start();
          nodes = { src, gain };
        } else if (kind === 'rain') {
          const hp = ac.createBiquadFilter();
          hp.type = 'highpass';
          hp.frequency.value = 1500;
          src.connect(hp).connect(gain).connect(ac.destination);
          src.start();
          nodes = { src, gain };
        } else if (kind === 'ocean') {
          const lp = ac.createBiquadFilter();
          lp.type = 'lowpass';
          lp.frequency.value = 600;
          const lfo = ac.createOscillator();
          lfo.frequency.value = 0.15;
          const lfoGain = ac.createGain();
          lfoGain.gain.value = 0.25;
          lfo.connect(lfoGain).connect(gain.gain);
          gain.gain.value = 0.35;
          src.connect(lp).connect(gain).connect(ac.destination);
          src.start();
          lfo.start();
          nodes = { src, gain, lfo };
        }
      };

      const stop = () => {
        if (timerId) { clearInterval(timerId); timerId = null; }
        stopSound();
      };

      const finish = () => {
        stop();
        display.textContent = '완료 ✓';
        startBtn.disabled = false;
      };
      render();

      startBtn.addEventListener('click', () => {
        if (timerId) return;
        if (remaining <= 0) remaining = 180;
        startBtn.disabled = true;
        const kind = select ? select.value : 'none';
        startSound(kind);
        render();
        timerId = setInterval(() => {
          remaining--;
          if (remaining <= 0) finish();
          else render();
        }, 1000);
      });

      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          stop();
          remaining = 180;
          startBtn.disabled = false;
          render();
        });
      }
    }
  };

  // ===== 사운드 믹서 (6채널) =====
  W.sound = {
    init() {
      const root = $('wb-hub-sound');
      if (!root) return;
      const channels = {};
      const channelNames = ['rain', 'ocean', 'whitenoise', 'bird', 'wind', 'bell'];
      let timerId = null;
      let timerCountdown = 0;
      const timerDisplay = root.querySelector('.wb-sound-timer-display');

      const stopChannel = (name) => {
        const ch = channels[name];
        if (!ch) return;
        try { ch.src && ch.src.stop(); } catch {}
        try { ch.lfo && ch.lfo.stop(); } catch {}
        try { ch.intervalId && clearInterval(ch.intervalId); } catch {}
        try { ch.gain && ch.gain.disconnect(); } catch {}
        delete channels[name];
      };

      const stopAll = () => {
        channelNames.forEach(stopChannel);
        if (timerId) { clearInterval(timerId); timerId = null; }
        if (timerDisplay) timerDisplay.textContent = '';
        root.querySelectorAll('.wb-sound-toggle').forEach(b => b.classList.remove('wb-sound-toggle--on'));
      };

      const startChannel = (name, vol) => {
        const ac = getAC();
        if (!ac) return;
        const gain = ac.createGain();
        gain.gain.value = vol;
        gain.connect(ac.destination);

        if (name === 'rain') {
          const src = ac.createBufferSource();
          src.buffer = getNoiseBuffer(ac);
          src.loop = true;
          const hp = ac.createBiquadFilter();
          hp.type = 'highpass';
          hp.frequency.value = 1500;
          src.connect(hp).connect(gain);
          src.start();
          channels[name] = { src, gain };
        } else if (name === 'ocean') {
          const src = ac.createBufferSource();
          src.buffer = getNoiseBuffer(ac);
          src.loop = true;
          const lp = ac.createBiquadFilter();
          lp.type = 'lowpass';
          lp.frequency.value = 600;
          const lfo = ac.createOscillator();
          lfo.frequency.value = 0.15;
          const lfoGain = ac.createGain();
          lfoGain.gain.value = vol * 0.6;
          lfo.connect(lfoGain).connect(gain.gain);
          src.connect(lp).connect(gain);
          src.start();
          lfo.start();
          channels[name] = { src, gain, lfo };
        } else if (name === 'whitenoise') {
          const src = ac.createBufferSource();
          src.buffer = getNoiseBuffer(ac);
          src.loop = true;
          src.connect(gain);
          src.start();
          channels[name] = { src, gain };
        } else if (name === 'bird') {
          const chirp = () => {
            if (!channels[name]) return;
            const t = ac.currentTime;
            const osc = ac.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800 + Math.random() * 2200, t);
            osc.frequency.exponentialRampToValueAtTime(1000 + Math.random() * 1500, t + 0.15);
            const env = ac.createGain();
            env.gain.setValueAtTime(0, t);
            env.gain.linearRampToValueAtTime(0.4, t + 0.02);
            env.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
            osc.connect(env).connect(gain);
            osc.start(t);
            osc.stop(t + 0.25);
          };
          chirp();
          const intervalId = setInterval(chirp, 3000 + Math.random() * 2000);
          channels[name] = { gain, intervalId };
        } else if (name === 'wind') {
          const src = ac.createBufferSource();
          src.buffer = getNoiseBuffer(ac);
          src.loop = true;
          const bp = ac.createBiquadFilter();
          bp.type = 'bandpass';
          bp.frequency.value = 500;
          bp.Q.value = 0.5;
          const lfo = ac.createOscillator();
          lfo.frequency.value = 0.1;
          const lfoGain = ac.createGain();
          lfoGain.gain.value = vol * 0.7;
          lfo.connect(lfoGain).connect(gain.gain);
          src.connect(bp).connect(gain);
          src.start();
          lfo.start();
          channels[name] = { src, gain, lfo };
        } else if (name === 'bell') {
          const ring = () => {
            if (!channels[name]) return;
            const t = ac.currentTime;
            const osc = ac.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = 528;
            const env = ac.createGain();
            env.gain.setValueAtTime(0.6, t);
            env.gain.exponentialRampToValueAtTime(0.001, t + 3);
            osc.connect(env).connect(gain);
            osc.start(t);
            osc.stop(t + 3.1);
          };
          ring();
          const intervalId = setInterval(ring, 15000);
          channels[name] = { gain, intervalId };
        }
      };

      // 채널 토글 + 볼륨
      channelNames.forEach(name => {
        const toggle = root.querySelector(`.wb-sound-toggle[data-channel="${name}"]`);
        const slider = root.querySelector(`.wb-volume-slider[data-channel="${name}"]`);
        if (toggle) {
          toggle.addEventListener('click', () => {
            if (channels[name]) {
              stopChannel(name);
              toggle.classList.remove('wb-sound-toggle--on');
            } else {
              const v = slider ? Number(slider.value) / 100 : 0.5;
              startChannel(name, v);
              toggle.classList.add('wb-sound-toggle--on');
            }
          });
        }
        if (slider) {
          slider.addEventListener('input', () => {
            const ch = channels[name];
            if (ch && ch.gain) ch.gain.gain.value = Number(slider.value) / 100;
          });
        }
      });

      // 타이머 시작 (옵션)
      const timerSelect = root.querySelector('.wb-sound-timer');
      const startBtn = root.querySelector('.wb-sound-start');
      if (startBtn) {
        startBtn.addEventListener('click', () => {
          if (timerId) { clearInterval(timerId); timerId = null; }
          const min = timerSelect ? Number(timerSelect.value) : 0;
          if (!min || min <= 0) {
            if (timerDisplay) timerDisplay.textContent = '무제한';
            return;
          }
          timerCountdown = min * 60;
          const renderT = () => {
            if (!timerDisplay) return;
            const m = Math.floor(timerCountdown / 60);
            const s = timerCountdown % 60;
            timerDisplay.textContent = `${pad(m)}:${pad(s)}`;
          };
          renderT();
          timerId = setInterval(() => {
            timerCountdown--;
            if (timerCountdown <= 0) {
              stopAll();
            } else {
              renderT();
            }
          }, 1000);
        });
      }

      const stopBtn = root.querySelector('.wb-sound-stop');
      if (stopBtn) stopBtn.addEventListener('click', stopAll);
    }
  };

  // ===== 감사일기 =====
  W.gratitude = {
    KEY: 'wb_gratitude',
    init() {
      const root = $('wb-hub-gratitude');
      if (!root) return;
      const inputs = root.querySelectorAll('.wb-gratitude-input');
      const saveBtn = root.querySelector('.wb-gratitude-save');
      const status = root.querySelector('.wb-gratitude-status');
      const history = root.querySelector('.wb-gratitude-history');

      const cleanOld = (data) => {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - 90);
        const cutoffStr = cutoff.toISOString().slice(0, 10);
        Object.keys(data).forEach(d => { if (d < cutoffStr) delete data[d]; });
        return data;
      };

      const renderHistory = () => {
        if (!history) return;
        const data = store.get(this.KEY) || {};
        const dates = Object.keys(data).sort().reverse().slice(0, 7);
        history.innerHTML = '';
        dates.forEach(d => {
          if (d === today()) return;
          const card = document.createElement('div');
          card.className = 'wb-gratitude-card';
          const items = (data[d] || []).filter(x => x && x.trim());
          card.innerHTML = `<div class="wb-gratitude-date">${d}</div>` +
            items.map(t => `<div class="wb-gratitude-item">· ${t.replace(/</g, '&lt;')}</div>`).join('');
          history.appendChild(card);
        });
      };

      const data = cleanOld(store.get(this.KEY) || {});
      store.set(this.KEY, data);
      const todayItems = data[today()] || [];
      inputs.forEach((inp, i) => { if (todayItems[i]) inp.value = todayItems[i]; });
      if (saveBtn && todayItems.length) saveBtn.textContent = '수정하기';
      renderHistory();

      if (saveBtn) {
        saveBtn.addEventListener('click', () => {
          const arr = Array.from(inputs).map(inp => inp.value.trim());
          const all = cleanOld(store.get(this.KEY) || {});
          all[today()] = arr;
          store.set(this.KEY, all);
          saveBtn.textContent = '수정하기';
          if (status) {
            status.textContent = '저장됐어요 ✓';
            setTimeout(() => { status.textContent = ''; }, 3000);
          }
          renderHistory();
        });
      }
    }
  };

  // ===== 에너지 로그 =====
  W.energy = {
    KEY: 'wb_energy',
    chartInstance: null,
    init() {
      const root = $('wb-hub-energy');
      if (!root) return;
      const tipEl = root.querySelector('.wb-energy-tip');
      const buttons = root.querySelectorAll('.wb-energy-btn[data-level]');
      const logBtn = root.querySelector('.wb-energy-log-btn');
      const canvas = $('wb-energy-chart');
      const chartSection = root.querySelector('.wb-energy-chart-wrap');

      buttons.forEach(btn => {
        btn.addEventListener('click', () => {
          const lvl = Number(btn.getAttribute('data-level'));
          if (!lvl) return;
          const arr = store.get(this.KEY) || [];
          arr.push({ date: today(), level: lvl, ts: Date.now() });
          store.set(this.KEY, arr);
          if (tipEl) tipEl.textContent = rand(DATA.energyTips[lvl] || []);
          this.renderChart();
        });
      });

      if (logBtn) logBtn.addEventListener('click', () => this.renderChart());

      if (typeof Chart === 'undefined') {
        if (chartSection) chartSection.style.display = 'none';
      } else if (canvas) {
        this.renderChart();
      }
    },
    renderChart() {
      const canvas = $('wb-energy-chart');
      if (!canvas || typeof Chart === 'undefined') return;
      const arr = store.get(this.KEY) || [];
      const days = [];
      const today0 = new Date();
      today0.setHours(0, 0, 0, 0);
      for (let i = 6; i >= 0; i--) {
        const d = new Date(today0);
        d.setDate(d.getDate() - i);
        days.push(d.toISOString().slice(0, 10));
      }
      const dailyAvg = days.map(d => {
        const items = arr.filter(x => x.date === d);
        if (!items.length) return null;
        return items.reduce((s, x) => s + x.level, 0) / items.length;
      });

      if (this.chartInstance) {
        try { this.chartInstance.destroy(); } catch {}
      }
      this.chartInstance = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: days.map(d => d.slice(5)),
          datasets: [{
            label: '에너지 레벨',
            data: dailyAvg,
            borderColor: 'rgba(130, 200, 160, 1)',
            backgroundColor: 'rgba(130, 200, 160, 0.2)',
            borderWidth: 2,
            tension: 0.3,
            spanGaps: true,
            pointRadius: 4,
            pointBackgroundColor: 'rgba(130, 200, 160, 0.8)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { min: 0, max: 5, ticks: { stepSize: 1 } }
          },
          plugins: { legend: { display: false } }
        }
      });
    }
  };

  // ===== 뽀모도로 =====
  W.pomodoro = {
    notifAsked: false,
    init() {
      const root = $('wb-hub-pomodoro');
      if (!root) return;
      const focusInp = root.querySelector('.wb-pomo-focus');
      const breakInp = root.querySelector('.wb-pomo-break');
      const startBtn = root.querySelector('.wb-pomo-start');
      const pauseBtn = root.querySelector('.wb-pomo-pause');
      const resetBtn = root.querySelector('.wb-pomo-reset');
      const display = root.querySelector('.wb-pomo-display');
      const status = root.querySelector('.wb-pomo-status');
      if (!startBtn || !display) return;

      let mode = 'focus';
      let remaining = (Number(focusInp?.value) || 25) * 60;
      let timerId = null;

      const render = () => {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        display.textContent = `${pad(m)}:${pad(s)}`;
        if (status) status.textContent = mode === 'focus' ? '집중 중 🍅' : '휴식 중 ☕';
      };

      const ding = () => {
        const ac = getAC();
        if (!ac) return;
        const t = ac.currentTime;
        const osc = ac.createOscillator();
        osc.type = 'sine';
        osc.frequency.value = 880;
        const g = ac.createGain();
        g.gain.setValueAtTime(0.4, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
        osc.connect(g).connect(ac.destination);
        osc.start(t);
        osc.stop(t + 0.35);
      };

      const notify = (text) => {
        if (!('Notification' in window)) return;
        if (Notification.permission === 'granted') {
          try { new Notification('웰빙 타이머', { body: text }); } catch {}
        } else if (Notification.permission !== 'denied' && !this.notifAsked) {
          this.notifAsked = true;
          Notification.requestPermission().then(p => {
            if (p === 'granted') {
              try { new Notification('웰빙 타이머', { body: text }); } catch {}
            }
          });
        }
      };

      const lockInputs = (lock) => {
        if (focusInp) focusInp.disabled = lock;
        if (breakInp) breakInp.disabled = lock;
      };

      const switchMode = () => {
        ding();
        if (mode === 'focus') {
          mode = 'break';
          remaining = (Number(breakInp?.value) || 5) * 60;
          notify('집중 끝. 휴식 시작 ☕');
        } else {
          mode = 'focus';
          remaining = (Number(focusInp?.value) || 25) * 60;
          notify('휴식 끝. 다시 집중 🍅');
        }
        render();
      };

      const tick = () => {
        remaining--;
        if (remaining <= 0) switchMode();
        else render();
      };

      const start = () => {
        if (timerId) return;
        lockInputs(true);
        timerId = setInterval(tick, 1000);
        // 권한 미리 요청
        if ('Notification' in window && Notification.permission === 'default' && !this.notifAsked) {
          this.notifAsked = true;
          Notification.requestPermission();
        }
      };
      const pause = () => {
        if (timerId) { clearInterval(timerId); timerId = null; }
        lockInputs(false);
      };
      const reset = () => {
        pause();
        mode = 'focus';
        remaining = (Number(focusInp?.value) || 25) * 60;
        render();
      };

      startBtn.addEventListener('click', start);
      if (pauseBtn) pauseBtn.addEventListener('click', pause);
      if (resetBtn) resetBtn.addEventListener('click', reset);
      [focusInp, breakInp].forEach(inp => {
        if (!inp) return;
        inp.addEventListener('change', () => { if (!timerId) reset(); });
      });
      render();
    }
  };

  // ===== 쉬는 시간 활동 추천 =====
  W.breakActivity = {
    init() {
      const root = $('wb-hub-break');
      if (!root) return;
      const textEl = root.querySelector('.wb-break-text');
      const typeEl = root.querySelector('.wb-break-type');
      const nextBtn = root.querySelector('.wb-break-next');
      const filterBtns = root.querySelectorAll('.wb-break-filter');
      let currentType = '전체';

      const pick = () => {
        const pool = currentType === '전체'
          ? DATA.breakActivities
          : DATA.breakActivities.filter(a => a.type === currentType);
        if (!pool.length) {
          if (textEl) textEl.textContent = '해당 유형 활동이 없습니다.';
          if (typeEl) typeEl.textContent = '';
          return;
        }
        const a = rand(pool);
        if (textEl) textEl.textContent = a.text;
        if (typeEl) typeEl.textContent = a.type;
      };

      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          filterBtns.forEach(b => b.classList.remove('wb-break-filter--on'));
          btn.classList.add('wb-break-filter--on');
          currentType = btn.getAttribute('data-type') || '전체';
          pick();
        });
      });
      if (nextBtn) nextBtn.addEventListener('click', pick);
      pick();
    }
  };

  // ===== 랜덤 포스트 (푸터) =====
  W.randomPost = function () {
    var container = document.getElementById('wb-footer-post');
    if (!container) return;
    var posts = window.__allPosts || [];
    if (posts.length === 0) {
      container.innerHTML = '<p style="font-size:.82em;opacity:.5">추천 글 준비 중</p>';
      return;
    }
    try {
      var post = posts[Math.floor(Math.random() * posts.length)];
      var title = post.title.replace(/</g,'&lt;').replace(/>/g,'&gt;');
      container.innerHTML =
        '<a class="wb-footer-post-card" href="' + post.url + '">' +
          '<img class="wb-footer-post-card__img" src="' + post.teaser + '" alt="' + title + '" loading="lazy" onerror="this.style.display=\'none\'">' +
          '<span class="wb-footer-post-card__title">' + title + '</span>' +
        '</a>';
    } catch(e) {
      container.innerHTML = '';
    }
  };

  // ===== 자동 초기화 =====
  W.init = function() {
    try { W.greeting.init(); } catch(e) { /* no greeting el */ }
    try { W.affirmation.init(); } catch(e) { /* no affirmation el */ }
    try { W.emotion.init(); } catch(e) { /* no emotion el */ }
    try { W.breath.init('wb-post-breath'); } catch(e) {}
    try { W.breath.init('wb-hub-breath'); } catch(e) {}
    if ($('wb-hub-meditation')) try { W.meditation.init(); } catch(e) {}
    if ($('wb-hub-sound'))      try { W.sound.init(); } catch(e) {}
    if ($('wb-hub-gratitude'))  try { W.gratitude.init(); } catch(e) {}
    if ($('wb-hub-energy'))     try { W.energy.init(); } catch(e) {}
    if ($('wb-hub-pomodoro'))   try { W.pomodoro.init(); } catch(e) {}
    if ($('wb-hub-break'))      try { W.breakActivity.init(); } catch(e) {}
    W.randomPost();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', W.init);
  } else {
    W.init();
  }
})(window.WB = window.WB || {});
