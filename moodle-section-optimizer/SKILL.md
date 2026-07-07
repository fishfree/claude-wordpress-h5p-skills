---
name: moodle-section-optimizer
description: Optimiert Moodle-Kursabschnitte mit HTML5/CSS/JS-Komponenten, Gamification und Storytelling. Erstellt interaktive Quizze, Flashcards, Simulationen und narrative Rahmen direkt in Moodle. H5P nur auf Anweisung. Nutze nach moodle-section-analyzer oder wenn konkrete Verbesserungen umgesetzt werden sollen.
license: MIT
version: "2.0"
date: 2026-03-12
---

# Moodle Section Optimizer v2.0

Setzt konkrete Optimierungen für Moodle-Abschnitte um: Interaktive HTML5/CSS/JS-Komponenten, Gamification-Systeme, Storytelling-Rahmen und visuelle Aufwertung.

**Paradigma:** HTML5/CSS/JS/React sind Standard. H5P nur auf explizite Anweisung oder wenn technisch überlegen.

## Wann nutzen

- Nach Analyse mit `moodle-section-analyzer`
- Konkrete 4K-Lücken schließen
- Storytelling-Rahmen aufbauen
- Gamification einführen
- Abschnitt interaktiv und visuell aufwerten

## Voraussetzungen

- **MCP Server**: moodle-mcp (v3.3.0) mit Label/Page/Quiz-Tools
- **Analyse**: Idealerweise vorher `moodle-section-analyzer` ausführen
- **Optional**: `h5p-generator` (nur bei H5P-Bedarf)

---

## Technologie-Entscheidungsbaum

```
Brauche ich Interaktivität?
├── Einfach (Quiz, Flashcards, Akkordeon, Timer)
│   └── → Inline JS in Moodle Label oder Page
├── Mittel (Drag&Drop, Sortierung, Simulation)
│   └── → Inline JS in Moodle Page
├── Komplex (Multi-Level-Trainer, State über Sessions)
│   └── → React-App auf lernmodule-Server, iframe in Moodle
└── H5P wird explizit gewünscht ODER Interactive Video / xAPI-Tracking nötig
    └── → H5P via h5p-generator + moodle_upload_h5p
```

---

## Storytelling-Bausteine

### Story-Rahmen: "Der Auftrag"

```html
<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee; padding: 24px; border-radius: 8px; margin: 12px 0;
            border-left: 5px solid #e94560; font-family: Arial, sans-serif;">
  <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
    <span style="font-size: 28px;">📧</span>
    <div>
      <div style="font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 1px;">Neue Nachricht</div>
      <div style="font-size: 16px; font-weight: bold; color: #e94560;">Von: M. Jungkuhn (Geschäftsführung)</div>
    </div>
  </div>
  <p style="margin: 0; line-height: 1.6;">
    Guten Morgen! Unser Online-Shop hat im letzten Quartal eine Abbruchrate von 68% im Checkout.
    <strong>Ihr Auftrag:</strong> Analysieren Sie den Checkout-Prozess und entwickeln Sie
    drei konkrete Optimierungsvorschläge. Die Ergebnisse brauche ich bis Freitag.
  </p>
  <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #333;
              font-size: 12px; color: #888;">
    Anhang: checkout-daten-q4.xlsx | Priorität: Hoch
  </div>
</div>
```

### Story-Rahmen: "Die Ermittlung"

```html
<div style="background: #fafafa; padding: 24px; border-radius: 8px; margin: 12px 0;
            border: 2px solid #333; font-family: Arial, sans-serif; position: relative;">
  <div style="position: absolute; top: -12px; left: 20px; background: #ff6b35;
              color: white; padding: 4px 16px; border-radius: 4px; font-size: 12px;
              font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
    Fallakte #[NR]
  </div>
  <h3 style="margin: 8px 0 12px; color: #333;">🔍 [TITEL DES FALLS]</h3>
  <p style="color: #555; line-height: 1.6; margin: 0;">[FALLBESCHREIBUNG]</p>
  <div style="display: flex; gap: 16px; margin-top: 16px; flex-wrap: wrap;">
    <div style="background: #fff3e0; padding: 8px 14px; border-radius: 4px; font-size: 13px;">
      📊 <strong>Beweisstück 1:</strong> [DATEN]
    </div>
    <div style="background: #e3f2fd; padding: 8px 14px; border-radius: 4px; font-size: 13px;">
      👤 <strong>Zeuge:</strong> [PERSON]
    </div>
  </div>
</div>
```

### Story-Rahmen: "Die Challenge"

```html
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 24px; border-radius: 8px; margin: 12px 0;
            text-align: center; font-family: Arial, sans-serif;">
  <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 2px;
              opacity: 0.8; margin-bottom: 8px;">Challenge</div>
  <h2 style="margin: 0 0 8px; font-size: 24px;">🏆 [CHALLENGE-TITEL]</h2>
  <p style="margin: 0 0 16px; opacity: 0.9; max-width: 500px; margin: 0 auto 16px;">
    [CHALLENGE-BESCHREIBUNG]
  </p>
  <div style="display: inline-flex; gap: 24px; background: rgba(255,255,255,0.15);
              padding: 12px 24px; border-radius: 8px;">
    <div><div style="font-size: 24px; font-weight: bold;">[N]</div>
         <div style="font-size: 11px; opacity: 0.8;">Aufgaben</div></div>
    <div><div style="font-size: 24px; font-weight: bold;">[N] XP</div>
         <div style="font-size: 11px; opacity: 0.8;">Punkte</div></div>
    <div><div style="font-size: 24px; font-weight: bold;">[N] Min</div>
         <div style="font-size: 11px; opacity: 0.8;">Zeit</div></div>
  </div>
</div>
```

### Story-Fortschritt (zwischen Phasen)

```html
<div style="background: #f8f9fa; padding: 16px 24px; border-radius: 8px; margin: 12px 0;
            display: flex; align-items: center; gap: 16px; font-family: Arial, sans-serif;">
  <div style="font-size: 32px;">✅</div>
  <div style="flex: 1;">
    <div style="font-weight: bold; color: #333; margin-bottom: 4px;">
      Phase [N] abgeschlossen: [TITEL]
    </div>
    <div style="color: #666; font-size: 13px;">
      [WAS WURDE ERREICHT]. Weiter mit: [NÄCHSTES ZIEL]
    </div>
  </div>
  <div style="background: #4caf50; color: white; padding: 6px 14px; border-radius: 20px;
              font-size: 13px; font-weight: bold; white-space: nowrap;">
    +[N] XP
  </div>
</div>
```

---

## Gamification-Bausteine

### Fortschrittsbalken (CSS-only)

```html
<div style="background: #e9ecef; border-radius: 20px; padding: 3px; margin: 12px 0;
            font-family: Arial, sans-serif;">
  <div style="background: linear-gradient(90deg, #667eea, #764ba2);
              border-radius: 18px; padding: 8px 16px; width: [PROZENT]%;
              color: white; font-size: 13px; font-weight: bold; text-align: right;
              min-width: 80px; box-sizing: border-box;">
    [PROZENT]% — Phase [N]/[TOTAL]
  </div>
</div>
```

### XP-Anzeige (CSS-only)

```html
<div style="display: inline-flex; align-items: center; gap: 8px; background: #1a1a2e;
            color: #ffd700; padding: 8px 16px; border-radius: 20px; font-family: Arial, sans-serif;
            font-size: 14px; font-weight: bold;">
  ⭐ [N] XP gesammelt | Level: [LEVEL-NAME]
</div>
```

### Badge/Achievement (CSS-only)

```html
<div style="display: inline-flex; align-items: center; gap: 10px; background: white;
            border: 2px solid #ffd700; border-radius: 8px; padding: 12px 20px;
            font-family: Arial, sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #ffd700, #ff8c00);
              border-radius: 50%; display: flex; align-items: center; justify-content: center;
              font-size: 24px;">🏆</div>
  <div>
    <div style="font-weight: bold; color: #333; font-size: 15px;">[BADGE-NAME]</div>
    <div style="color: #888; font-size: 12px;">[BESCHREIBUNG]</div>
  </div>
</div>
```

---

## Interaktive JS-Komponenten

### JS-Quiz (in Moodle Label oder Page)

```html
<div id="quiz-[ID]" style="font-family: Arial, sans-serif; max-width: 700px; margin: 16px 0;">
  <style>
    #quiz-[ID] .q-card { background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 12px 0;
      border-left: 4px solid #667eea; }
    #quiz-[ID] .q-btn { display: block; width: 100%; text-align: left; padding: 12px 16px;
      margin: 6px 0; border: 2px solid #ddd; border-radius: 6px; background: white;
      cursor: pointer; font-size: 14px; transition: all 0.2s; }
    #quiz-[ID] .q-btn:hover { border-color: #667eea; background: #f0f0ff; }
    #quiz-[ID] .q-btn.correct { border-color: #4caf50; background: #e8f5e9; }
    #quiz-[ID] .q-btn.wrong { border-color: #f44336; background: #fce4ec; }
    #quiz-[ID] .q-btn.disabled { pointer-events: none; opacity: 0.7; }
    #quiz-[ID] .q-feedback { padding: 10px 14px; border-radius: 6px; margin-top: 8px;
      font-size: 13px; display: none; }
    #quiz-[ID] .q-score { text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2);
      color: white; border-radius: 8px; font-size: 18px; }
  </style>
  <div id="quiz-[ID]-questions"></div>
  <div id="quiz-[ID]-result" style="display:none;"></div>
</div>
<script>
(function(){
  const Q = [
    { q: "[FRAGE 1]", a: ["[ANTWORT A]","[ANTWORT B]","[ANTWORT C]","[ANTWORT D]"], c: 0,
      fb: "[ERKLÄRUNG]" },
    // weitere Fragen...
  ];
  const id = "quiz-[ID]";
  let score = 0, current = 0;
  const container = document.getElementById(id + "-questions");
  const result = document.getElementById(id + "-result");

  function show(i) {
    if (i >= Q.length) {
      const pct = Math.round(score/Q.length*100);
      result.style.display = "block";
      result.innerHTML = '<div class="q-score">🎯 ' + score + '/' + Q.length +
        ' richtig (' + pct + '%)<br><span style="font-size:14px;opacity:0.8;">+' +
        (score*10) + ' XP</span></div>';
      container.style.display = "none";
      return;
    }
    const q = Q[i];
    let html = '<div class="q-card"><div style="font-size:12px;color:#888;margin-bottom:8px;">Frage ' +
      (i+1) + '/' + Q.length + '</div><p style="font-weight:bold;margin:0 0 12px;">' + q.q + '</p>';
    q.a.forEach(function(a, j) {
      html += '<button class="q-btn" onclick="window._qz' + id.replace(/-/g,'') +
        '(' + i + ',' + j + ')">' + a + '</button>';
    });
    html += '<div class="q-feedback" id="' + id + '-fb-' + i + '"></div></div>';
    container.innerHTML = html;
  }

  window['_qz' + id.replace(/-/g,'')] = function(qi, ai) {
    const q = Q[qi];
    const btns = container.querySelectorAll('.q-btn');
    btns.forEach(function(b, j) {
      b.classList.add('disabled');
      if (j === q.c) b.classList.add('correct');
      if (j === ai && j !== q.c) b.classList.add('wrong');
    });
    if (ai === q.c) score++;
    const fb = document.getElementById(id + '-fb-' + qi);
    fb.style.display = 'block';
    fb.style.background = ai === q.c ? '#e8f5e9' : '#fce4ec';
    fb.textContent = ai === q.c ? '✅ Richtig! ' + q.fb : '❌ ' + q.fb;
    current++;
    setTimeout(function(){ show(current); }, 1500);
  };
  show(0);
})();
</script>
```

### JS-Flashcards (in Moodle Label oder Page)

```html
<div id="fc-[ID]" style="font-family: Arial, sans-serif; max-width: 500px; margin: 16px auto;">
  <style>
    #fc-[ID] .fc-card { perspective: 1000px; height: 200px; cursor: pointer; margin: 12px 0; }
    #fc-[ID] .fc-inner { width: 100%; height: 100%; transition: transform 0.6s;
      transform-style: preserve-3d; position: relative; }
    #fc-[ID] .fc-card.flipped .fc-inner { transform: rotateY(180deg); }
    #fc-[ID] .fc-front, #fc-[ID] .fc-back { position: absolute; width: 100%; height: 100%;
      backface-visibility: hidden; border-radius: 12px; display: flex; align-items: center;
      justify-content: center; padding: 24px; box-sizing: border-box; text-align: center; }
    #fc-[ID] .fc-front { background: linear-gradient(135deg, #667eea, #764ba2); color: white;
      font-size: 18px; font-weight: bold; }
    #fc-[ID] .fc-back { background: #f8f9fa; border: 2px solid #667eea; transform: rotateY(180deg);
      font-size: 15px; color: #333; }
    #fc-[ID] .fc-nav { display: flex; justify-content: center; gap: 12px; margin-top: 8px; }
    #fc-[ID] .fc-nav button { padding: 8px 20px; border: 2px solid #667eea; border-radius: 6px;
      background: white; cursor: pointer; font-size: 14px; }
    #fc-[ID] .fc-nav button:hover { background: #667eea; color: white; }
    #fc-[ID] .fc-counter { text-align: center; color: #888; font-size: 13px; margin-bottom: 8px; }
  </style>
  <div class="fc-counter" id="fc-[ID]-counter"></div>
  <div class="fc-card" id="fc-[ID]-card" onclick="this.classList.toggle('flipped')">
    <div class="fc-inner">
      <div class="fc-front" id="fc-[ID]-front"></div>
      <div class="fc-back" id="fc-[ID]-back"></div>
    </div>
  </div>
  <div class="fc-nav">
    <button onclick="window._fc[ID]prev()">← Zurück</button>
    <button onclick="window._fc[ID]next()">Weiter →</button>
  </div>
</div>
<script>
(function(){
  const cards = [
    { front: "[BEGRIFF 1]", back: "[DEFINITION 1]" },
    { front: "[BEGRIFF 2]", back: "[DEFINITION 2]" },
    // weitere Karten...
  ];
  let idx = 0;
  const card = document.getElementById("fc-[ID]-card");
  const front = document.getElementById("fc-[ID]-front");
  const back = document.getElementById("fc-[ID]-back");
  const counter = document.getElementById("fc-[ID]-counter");

  function render() {
    card.classList.remove("flipped");
    front.textContent = cards[idx].front;
    back.textContent = cards[idx].back;
    counter.textContent = (idx+1) + " / " + cards.length;
  }
  window["_fc[ID]prev"] = function() { idx = (idx - 1 + cards.length) % cards.length; render(); };
  window["_fc[ID]next"] = function() { idx = (idx + 1) % cards.length; render(); };
  render();
})();
</script>
```

### JS-Akkordeon (in Moodle Label)

```html
<div id="acc-[ID]" style="font-family: Arial, sans-serif; max-width: 700px; margin: 12px 0;">
  <style>
    #acc-[ID] details { background: #f8f9fa; border-radius: 8px; margin: 6px 0;
      border: 1px solid #ddd; overflow: hidden; }
    #acc-[ID] summary { padding: 14px 18px; cursor: pointer; font-weight: bold;
      color: #333; list-style: none; display: flex; justify-content: space-between;
      align-items: center; }
    #acc-[ID] summary::-webkit-details-marker { display: none; }
    #acc-[ID] summary::after { content: "▸"; transition: transform 0.2s; font-size: 18px; }
    #acc-[ID] details[open] summary::after { transform: rotate(90deg); }
    #acc-[ID] details[open] summary { background: #667eea; color: white; }
    #acc-[ID] .acc-content { padding: 16px 18px; line-height: 1.6; color: #555; }
  </style>
  <details>
    <summary>[TITEL 1]</summary>
    <div class="acc-content">[INHALT 1]</div>
  </details>
  <details>
    <summary>[TITEL 2]</summary>
    <div class="acc-content">[INHALT 2]</div>
  </details>
  <!-- weitere Abschnitte -->
</div>
```

### JS-Entscheidungsbaum / Szenario (in Moodle Page)

```html
<div id="scenario-[ID]" style="font-family: Arial, sans-serif; max-width: 600px; margin: 16px auto;">
  <style>
    #scenario-[ID] .sc-card { background: white; border-radius: 12px; padding: 24px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin: 12px 0; }
    #scenario-[ID] .sc-text { font-size: 15px; line-height: 1.7; color: #333; margin-bottom: 16px; }
    #scenario-[ID] .sc-choice { display: block; width: 100%; text-align: left; padding: 14px 18px;
      margin: 8px 0; border: 2px solid #ddd; border-radius: 8px; background: #fafafa;
      cursor: pointer; font-size: 14px; transition: all 0.2s; }
    #scenario-[ID] .sc-choice:hover { border-color: #667eea; background: #f0f0ff;
      transform: translateX(4px); }
    #scenario-[ID] .sc-result { text-align: center; padding: 32px; }
  </style>
  <div id="scenario-[ID]-content"></div>
</div>
<script>
(function(){
  const scenes = {
    start: {
      text: "[SZENARIO-TEXT]",
      choices: [
        { text: "[OPTION A]", next: "scene_a" },
        { text: "[OPTION B]", next: "scene_b" },
      ]
    },
    scene_a: {
      text: "[FOLGE-TEXT A]",
      choices: [
        { text: "[OPTION]", next: "result_good" },
      ]
    },
    scene_b: {
      text: "[FOLGE-TEXT B]",
      choices: [
        { text: "[OPTION]", next: "result_bad" },
      ]
    },
    result_good: {
      text: "🎉 [GUTES ERGEBNIS]",
      result: true, xp: 20
    },
    result_bad: {
      text: "💡 [LERNERGEBNIS]",
      result: true, xp: 10
    }
  };

  const container = document.getElementById("scenario-[ID]-content");

  function render(key) {
    const s = scenes[key];
    let html = '<div class="sc-card"><div class="sc-text">' + s.text + '</div>';
    if (s.result) {
      html += '<div class="sc-result"><div style="font-size:24px;margin-bottom:8px;">+' +
        s.xp + ' XP</div></div>';
    } else {
      s.choices.forEach(function(c) {
        html += '<button class="sc-choice" onclick="window._sc[ID](\'' +
          c.next + '\')">' + c.text + '</button>';
      });
    }
    html += '</div>';
    container.innerHTML = html;
  }

  window["_sc[ID]"] = render;
  render("start");
})();
</script>
```

### JS-Timer-Challenge (in Moodle Label oder Page)

```html
<div id="timer-[ID]" style="font-family: Arial, sans-serif; text-align: center; margin: 16px 0;">
  <div style="font-size: 48px; font-weight: bold; color: #333; font-variant-numeric: tabular-nums;"
       id="timer-[ID]-display">00:00</div>
  <div style="color: #888; margin: 8px 0;" id="timer-[ID]-status">
    Starte den Timer wenn du bereit bist!
  </div>
  <button onclick="window._timer[ID]()" id="timer-[ID]-btn"
    style="padding: 10px 28px; background: #667eea; color: white; border: none;
           border-radius: 6px; font-size: 15px; cursor: pointer; margin-top: 8px;">
    ▶ Start
  </button>
</div>
<script>
(function(){
  let running = false, seconds = 0, interval;
  const display = document.getElementById("timer-[ID]-display");
  const status = document.getElementById("timer-[ID]-status");
  const btn = document.getElementById("timer-[ID]-btn");

  window["_timer[ID]"] = function() {
    if (!running) {
      running = true; seconds = 0;
      btn.textContent = "⏹ Stop";
      status.textContent = "Aufgabe läuft...";
      interval = setInterval(function() {
        seconds++;
        const m = String(Math.floor(seconds/60)).padStart(2,"0");
        const s = String(seconds%60).padStart(2,"0");
        display.textContent = m + ":" + s;
      }, 1000);
    } else {
      running = false;
      clearInterval(interval);
      btn.textContent = "↻ Nochmal";
      const bonus = seconds <= [ZIELZEIT] ? " 🏆 Bonus: +10 XP!" : "";
      status.textContent = "Fertig in " + seconds + " Sekunden." + bonus;
    }
  };
})();
</script>
```

---

## Optimierungs-Rezepte

### Rezept 1: "Storytelling Kickstart" (20 Min)

```yaml
schritte:
  1. Szenario-Rahmen als Einführungs-Label (Story-Template wählen)
  2. Lernziele als Story-Ziel formulieren ("Am Ende können Sie...")
  3. Fortschritts-Label zwischen Phasen
  4. Abschluss-Label mit Story-Auflösung + XP-Badge

aufwand: ⭐⭐
impact:
  storytelling: 0→2
  gamification: 0→1
  engagement: +15%
```

### Rezept 2: "Gamified Learning" (30 Min)

```yaml
schritte:
  1. Challenge-Einführung mit Punktesystem
  2. JS-Quiz mit XP-Vergabe (8-10 Fragen)
  3. Flashcards für Kernbegriffe
  4. Fortschrittsbalken (CSS)
  5. Abschluss-Badge für Phase

aufwand: ⭐⭐
impact:
  gamification: 0→2
  kritisches_denken: +1
  engagement: +25%
```

### Rezept 3: "Interactive Deep Dive" (45 Min)

```yaml
schritte:
  1. Szenario-Einführung (Auftrag/Ermittlung)
  2. Akkordeon mit Hintergrundinfos
  3. Entscheidungsbaum-Simulation
  4. JS-Quiz als Abschlusstest
  5. Timer-Challenge (optional)
  6. XP-Zusammenfassung + Badge

aufwand: ⭐⭐⭐
impact:
  storytelling: 0→3
  gamification: 0→2
  kreativität: +1
  kritisches_denken: +2
  engagement: +35%
```

### Rezept 4: "Full Transformation" (90 Min)

```yaml
schritte:
  1. Gesamte Rahmenhandlung definieren (Story-Arc)
  2. Challenge-Einführung mit Level-System
  3. Phase 1: Story-Start + Akkordeon + Flashcards
  4. Phase 2: Szenario-Simulation + Quiz
  5. Phase 3: Timer-Challenge + Drag&Drop
  6. Abschluss: Story-Auflösung + Gesamtpunkte + Badge
  7. Forum-Aufgabe neu formulieren (Story-Bezug)

aufwand: ⭐⭐⭐
impact: Alle 6 Dimensionen verbessert
```

---

## Phasen-Labels (visuelle Struktur)

### Phase-Start

```html
<div style="background: linear-gradient(135deg, [FARBE1] 0%, [FARBE2] 100%);
            color: white; padding: 18px 24px; border-radius: 8px; margin: 12px 0;
            display: flex; justify-content: space-between; align-items: center;
            font-family: Arial, sans-serif;">
  <div>
    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px;
                opacity: 0.8;">Phase [N] von [TOTAL]</div>
    <h3 style="margin: 4px 0 0; font-size: 18px;">[EMOJI] [TITEL]</h3>
  </div>
  <div style="text-align: right; font-size: 13px; opacity: 0.9;">
    ⏱ ca. [N] Min<br>+[N] XP
  </div>
</div>
```

**Farb-Schema nach Phase:**

| Phase | Gradient | Emoji |
|-------|----------|-------|
| Orientierung | #667eea → #764ba2 | 🧭 |
| Motivation/Start | #e94560 → #ff6b6b | 🚀 |
| Erarbeitung | #2196f3 → #00bcd4 | 📚 |
| Analyse | #ff9800 → #ffc107 | 🔍 |
| Anwendung | #4caf50 → #8bc34a | 💡 |
| Reflexion | #9c27b0 → #e040fb | 🪞 |
| Abschluss | #ffd700 → #ff8c00 | 🏆 |

### Lernziel-Label

```html
<div style="background: #e8f5e9; padding: 16px 20px; border-radius: 8px;
            border-left: 4px solid #4caf50; margin: 12px 0; font-family: Arial, sans-serif;">
  <h4 style="margin: 0 0 10px; color: #2e7d32;">🎯 Lernziele</h4>
  <ul style="margin: 0; padding-left: 20px; color: #333; line-height: 1.8;">
    <li>[LERNZIEL 1]</li>
    <li>[LERNZIEL 2]</li>
    <li>[LERNZIEL 3]</li>
  </ul>
</div>
```

### Info/Tipp/Warnung-Boxen

```html
<!-- Info -->
<div style="background: #e3f2fd; padding: 14px 18px; border-radius: 8px;
            border-left: 4px solid #2196f3; margin: 10px 0; font-family: Arial, sans-serif;">
  <strong>💡 Info:</strong> [TEXT]
</div>

<!-- Tipp -->
<div style="background: #e8f5e9; padding: 14px 18px; border-radius: 8px;
            border-left: 4px solid #4caf50; margin: 10px 0; font-family: Arial, sans-serif;">
  <strong>🔑 Tipp:</strong> [TEXT]
</div>

<!-- Warnung -->
<div style="background: #fff3e0; padding: 14px 18px; border-radius: 8px;
            border-left: 4px solid #ff9800; margin: 10px 0; font-family: Arial, sans-serif;">
  <strong>⚠️ Wichtig:</strong> [TEXT]
</div>

<!-- Arbeitsauftrag -->
<div style="background: #f3e5f5; padding: 14px 18px; border-radius: 8px;
            border-left: 4px solid #9c27b0; margin: 10px 0; font-family: Arial, sans-serif;">
  <strong>📋 Arbeitsauftrag:</strong>
  <ol style="margin: 8px 0 0; padding-left: 20px; line-height: 1.8;">[SCHRITTE]</ol>
</div>
```

---

## React-Apps (für komplexe Anforderungen)

Wenn Inline-JS nicht reicht (Multi-Level, persistenter State, komplexe UI):

### Deployment-Pfad

```
React-App bauen → lernmodule.dirk-schulenburg.net/[app-name]/
→ In Moodle als iframe einbetten
```

**Referenz-Implementierungen:**
- Excel-Trainer: 6 Level, 24 Übungen, Gamification
- Word-Trainer: 6 Level, 24 Übungen, DE+UA
- KI-im-Handel: 4 Blöcke, PromptSandbox, Quiz, DragDrop

### iframe-Einbettung in Moodle

```html
<div style="position: relative; width: 100%; padding-bottom: 75%; margin: 12px 0;">
  <iframe src="https://lernmodule.dirk-schulenburg.net/[app-name]/"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                 border: none; border-radius: 8px;"
          allowfullscreen></iframe>
</div>
```

---

## H5P (nur auf Anweisung)

H5P wird **nur** eingesetzt wenn:

| Grund | Beispiel |
|-------|---------|
| User fordert es explizit | "Mach ein H5P-Quiz" |
| Interactive Video | Video mit Fragen/Hotspots (zu komplex als JS) |
| Branching Scenario | Komplexe Verzweigung mit Medien |
| xAPI-Tracking | Ergebnisse MÜSSEN im Moodle-Gradebook landen |
| Kurs-Export | H5P reist im Moodle-Backup mit |

**Workflow wenn H5P nötig:**
1. H5P generieren mit `h5p-generator` Skill
2. Upload via `moodle_upload_h5p`
3. Aktivität erstellen via `moodle_create_h5p_activity`

---

## Workflow

### Schritt 1: Analyse-Ergebnis prüfen

```yaml
input:
  kurs_id: [ID]
  abschnitt_num: [N]
  diagnose:
    4k_defizite: [Kreativität, Kritisches Denken]
    storytelling: 0
    gamification: 0
    fehlend: [Interaktivität, roter Faden, Feedback]
```

### Schritt 2: Story-Rahmen wählen

Basierend auf Fachgebiet und Diagnose:
- Kaufmännisch → "Der Auftrag" oder "Die Ermittlung"
- IT/Technik → "Die Challenge" oder "Die Ermittlung"
- Allgemein → "Die Reise" oder "Der Experten-Aufstieg"

### Schritt 3: Komponenten erstellen

```javascript
// 1. Story-Rahmen als Label
moodle_create_label({ courseId: "6", sectionNum: "2",
  labelText: "[STORY-TEMPLATE HTML]" })

// 2. JS-Quiz als Page
moodle_create_page({ courseId: "6", sectionNum: "2",
  name: "Quiz: [THEMA]",
  content: "[JS-QUIZ HTML+SCRIPT]" })

// 3. Fortschritts-Label
moodle_create_label({ courseId: "6", sectionNum: "2",
  labelText: "[FORTSCHRITTSBALKEN HTML]" })

// 4. Module sortieren
moodle_reorder_modules({ courseId: "6", sectionNum: "2",
  moduleOrder: [id1, id2, id3, ...] })
```

---

## Abschnitts-Zielstruktur

```
📁 Abschnitt X: [Thema]
├── 🏷️ Challenge-Einführung / Story-Rahmen
├── 🏷️ Lernziele
├── 🏷️ Fortschrittsbalken (Phase 1/N)
├── 📄 Theorie (Page mit Akkordeon)
├── 🔗 Externe Ressource (optional)
├── 🏷️ Story-Fortschritt
├── 📄 JS-Quiz (8-10 Fragen mit XP)
├── 📄 Flashcards oder Szenario-Simulation
├── 📋 Arbeitsauftrag / Assignment
├── 💬 Forum (mit Story-Bezug)
├── 🏷️ Abschluss-Badge + XP-Zusammenfassung
└── 🏷️ Story-Auflösung / Teaser nächste Phase
```

---

## Best Practices

1. **Story first**: Erst den roten Faden definieren, dann Komponenten
2. **Konsistente IDs**: Jede JS-Komponente braucht unique IDs (z.B. `quiz-checkout-1`)
3. **Mobile-tauglich**: Inline-Styles responsive halten (max-width, flex-wrap)
4. **Nicht überladen**: Max. 3-4 interaktive Elemente pro Abschnitt
5. **Gamification dosiert**: XP-Werte konsistent (10 pro Quiz-Frage, 20 pro Phase)
6. **Testen**: Nach jeder Änderung im Browser prüfen (Moodle rendert HTML manchmal anders)
7. **Arial**: Immer `font-family: Arial, sans-serif` für BS:WI-Konsistenz

## Limitations

| Limitation | Workaround |
|------------|------------|
| **JS in Labels kann vom Theme blockiert werden** | Page statt Label nutzen, oder Admin-Einstellung prüfen |
| **Foren erstellen** | Moodle-API-Limitation → Manuell anlegen |
| **Assignments erstellen** | Benötigt mod_assign Plugin → Manuell oder Template |
| **localStorage in Moodle** | Funktioniert, aber nicht zwischen Geräten synchronisiert |

**Verfügbare MCP-Tools:**
- ✅ Labels, Pages, URLs erstellen
- ✅ Quizze mit Fragen erstellen
- ✅ Module verschieben und sortieren
- ✅ H5P upload + Activity (wenn nötig)
- ❌ Foren, Assignments (manuell)

## Moodle-Berechtigungen

Nach CLI-Befehlen:
```bash
docker exec moodle chown -R www-data:www-data /var/www/html/
```

---

*Skill Version: 2.0*
*Abhängigkeiten: moodle-mcp (v3.3.0, 73 Tools)*
*Letzte Aktualisierung: 2026-03-12*
*Paradigma: HTML5/CSS/JS/React + Gamification + Storytelling first, H5P nur auf Anweisung*
