// Dependency-free formative-assessment widgets.
// Loaded as a <script type="module">; scans for div.forma-* and mounts each.

function mk(tag, cls, txt) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (txt !== undefined) el.textContent = txt;
  return el;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

// Create the .forma container plus an optional .forma-question.
function initWidget(question) {
  const container = mk('div', 'forma');
  if (question) container.appendChild(mk('div', 'forma-question', question));
  return container;
}

function showFeedback(ok, feedbackEl, explanationEl, explanation) {
  feedbackEl.textContent = ok ? '✓ Correct!' : '✗ Incorrect';
  feedbackEl.className = `forma-feedback ${ok ? 'forma-correct' : 'forma-incorrect'}`;
  feedbackEl.style.display = 'block';
  if (explanation) {
    explanationEl.textContent = explanation;
    explanationEl.className = 'forma-explanation';
    explanationEl.style.display = 'block';
  }
}

function createOptions(options, onSelect) {
  const opts = mk('div', 'forma-options');
  options.forEach((text, i) => {
    const div = mk('div', 'forma-option');
    const radio = mk('input');
    radio.type = 'radio'; radio.name = 'answer'; radio.value = i;
    radio.id = `opt-${i}`; radio.style.marginRight = '10px';
    const lbl = mk('label');
    lbl.htmlFor = `opt-${i}`; lbl.textContent = text; lbl.style.cursor = 'pointer';
    div.append(radio, lbl);
    const select = () => onSelect(i, radio, opts);
    div.addEventListener('click', select);
    radio.addEventListener('change', select);
    opts.appendChild(div);
  });
  return opts;
}

function setupDropZone(zone, onDrop, isSubmitted) {
  zone.addEventListener('dragover', e => {
    if (isSubmitted()) return;
    e.preventDefault(); zone.classList.add('forma-drop-target');
  });
  zone.addEventListener('dragleave', () => zone.classList.remove('forma-drop-target'));
  zone.addEventListener('drop', e => {
    if (isSubmitted()) return;
    e.preventDefault(); zone.classList.remove('forma-drop-target');
    onDrop(e);
  });
}

function createSubmitRow(submitLabel) {
  const btnRow = mk('div');
  const submitBtn = mk('button', 'forma-btn forma-btn-primary', submitLabel);
  submitBtn.style.marginRight = '12px';
  const tryAgainBtn = mk('button', 'forma-btn forma-btn-secondary', 'Try Again');
  tryAgainBtn.style.display = 'none';
  return { btnRow, submitBtn, tryAgainBtn };
}

function addHelpButton(container, lang, helpText) {
  const text = helpText[lang] || helpText['en'];

  const popup = document.createElement('div');
  popup.className = 'forma-help-popup';
  popup.textContent = text;
  popup.hidden = true;

  const btn = document.createElement('button');
  btn.className = 'forma-help-btn';
  btn.textContent = '?';
  btn.setAttribute('aria-label', 'Help');

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    popup.hidden = !popup.hidden;
  });

  document.addEventListener('click', () => { popup.hidden = true; });

  container.append(popup, btn);
}

// --- multiple-choice ---

const MULTIPLE_CHOICE_HELP_TEXT = {
  en: 'Select the answer you think is correct by clicking on it. You\'ll see whether you were right. Click Try Again to reset and retry.',
  fr: 'Cliquez sur la réponse que vous pensez correcte. Vous verrez si vous aviez raison. Cliquez sur Réessayer pour recommencer.',
  es: 'Seleccione la respuesta que crea correcta haciendo clic en ella. Verá si acertó. Haga clic en Reintentar para volver a intentarlo.',
};

function parseMultipleChoice(div) {
  const question = div.querySelector('p')?.textContent.trim() ?? '';
  const lang = div.dataset.lang ?? 'en';
  const dl = div.querySelector('dl');
  const dts = dl ? [...dl.querySelectorAll('dt')] : [];
  const dds = dl ? [...dl.querySelectorAll('dd')] : [];
  const options = dts.map(dt => dt.textContent.trim());
  const explanations = dds.map(dd => dd.textContent.trim());
  const correct_answer = dds.findIndex(dd => /^correct\b/i.test(dd.textContent.trim()));
  return { question, options, correct_answer: correct_answer === -1 ? 0 : correct_answer, explanations, lang };
}

function renderMultipleChoice(el, config) {
  const container = initWidget(config.question);

  const correct = config.correct_answer;
  let answered = false;

  const feedbackEl = mk('div'); feedbackEl.style.display = 'none';
  const explanationEl = mk('div'); explanationEl.style.display = 'none';
  const tryAgainBtn = mk('button', 'forma-btn forma-btn-secondary', 'Try Again');
  tryAgainBtn.style.display = 'none';

  const opts = createOptions(config.options, (i, radio, opts) => {
    if (answered) return;
    radio.checked = true;
    answered = true;
    [...opts.children].forEach((opt, j) => {
      opt.classList.add('forma-answered', j === correct ? 'forma-correct' : j === i ? 'forma-incorrect' : 'forma-faded');
    });
    const ok = i === correct;
    const explanations = config.explanations;
    showFeedback(ok, feedbackEl, explanationEl, (explanations && explanations[i]) || config.explanation);
    tryAgainBtn.style.display = 'inline-block';
  });

  tryAgainBtn.addEventListener('click', () => {
    answered = false;
    [...opts.children].forEach(opt => {
      opt.classList.remove('forma-answered', 'forma-correct', 'forma-incorrect', 'forma-faded');
      opt.querySelector('input').checked = false;
    });
    feedbackEl.style.display = 'none';
    explanationEl.style.display = 'none';
    tryAgainBtn.style.display = 'none';
  });

  container.append(opts, feedbackEl, explanationEl, tryAgainBtn);
  addHelpButton(container, config.lang, MULTIPLE_CHOICE_HELP_TEXT);
  el.appendChild(container);
}

// --- flashcard ---

const FLASHCARD_HELP_TEXT = {
  en: 'Read the front of each card, then click Flip to see the answer. Rate how well you knew it: Got it (you knew it), Almost (close but not quite), or No (didn\'t know it). Cards rated Almost or No will reappear until you get them right.',
  fr: 'Lisez le recto de la carte, puis cliquez sur Retourner pour voir la réponse. Évaluez : Compris (vous le saviez), Presque (proche) ou Non (vous ne le saviez pas). Les cartes notées Presque ou Non réapparaîtront.',
  es: 'Lea el frente de la tarjeta y haga clic en Voltear para ver la respuesta. Califique: Entendido (lo sabía), Casi (cerca) o No (no lo sabía). Las tarjetas con Casi o No reaparecerán hasta que las domine.',
};

function parseFlashcard(div) {
  const question = div.querySelector('p')?.textContent.trim() ?? '';
  const cards = [...div.querySelectorAll('dt')].map(dt => ({
    front: dt.textContent.trim(),
    back:  dt.nextElementSibling?.textContent.trim() ?? '',
  }));
  return { question, cards, shuffle: true, lang: div.dataset.lang ?? 'en' };
}

function renderFlashcard(el, config) {
  const container = initWidget(config.question);

  const cards = config.cards;
  const total = cards.length;
  const done = new Set();
  const results = {};

  let queue = cards.map((_, i) => i);
  if (config.shuffle) shuffle(queue);

  const progressWrap = mk('div', 'forma-progress');
  const progressFill = mk('div', 'forma-progress-fill'); progressFill.style.width = '0%';
  progressWrap.appendChild(progressFill);
  container.appendChild(progressWrap);

  const counterEl = mk('div', 'forma-instructions');
  container.appendChild(counterEl);

  const cardEl = mk('div', 'forma-card forma-card-front');
  const cardContent = mk('span');
  cardEl.appendChild(cardContent);
  container.appendChild(cardEl);

  const flipBtn = mk('button', 'forma-btn forma-btn-secondary', 'Flip');
  flipBtn.style.marginBottom = '12px';
  container.appendChild(flipBtn);

  const ratingRow = mk('div', 'forma-rating-btns'); ratingRow.style.display = 'none';
  const gotItBtn  = mk('button', 'forma-btn forma-btn-primary', '✓ Got it');
  const almostBtn = mk('button', 'forma-btn forma-btn-secondary', '~ Almost');
  const noBtn     = mk('button', 'forma-btn forma-btn-danger', '✗ No');
  ratingRow.append(gotItBtn, almostBtn, noBtn);
  container.appendChild(ratingRow);

  function updateCounter() {
    if (queue.length === 0) return;
    counterEl.textContent = `Card ${done.size + 1} of ${total} — ${queue.length} remaining in queue`;
  }

  function showCard() {
    if (queue.length === 0) return;
    const idx = queue[0];
    cardContent.textContent = cards[idx].front;
    cardEl.className = 'forma-card forma-card-front';
    flipBtn.style.display = '';
    ratingRow.style.display = 'none';
    updateCounter();
  }

  function showComplete() {
    cardContent.textContent = '🎉 All cards reviewed!';
    cardEl.className = 'forma-card forma-card-back';
    counterEl.textContent = `Completed ${total} card${total !== 1 ? 's' : ''}.`;
    flipBtn.style.display = 'none';
    ratingRow.style.display = 'none';
    progressFill.style.width = '100%';
    const restartBtn = mk('button', 'forma-btn forma-btn-secondary', 'Restart');
    restartBtn.addEventListener('click', () => {
      done.clear();
      queue = cards.map((_, i) => i);
      if (config.shuffle) shuffle(queue);
      restartBtn.remove();
      showCard();
    });
    container.appendChild(restartBtn);
  }

  flipBtn.addEventListener('click', () => {
    const idx = queue[0];
    cardContent.textContent = cards[idx].back;
    cardEl.className = 'forma-card forma-card-back';
    flipBtn.style.display = 'none';
    ratingRow.style.display = 'flex';
  });

  function rate(rating) {
    const idx = queue.shift();
    if (!results[idx]) results[idx] = { attempts: 0 };
    results[idx].rating = rating;
    results[idx].attempts++;
    if (rating === 'got_it') {
      done.add(idx);
    } else if (rating === 'almost') {
      queue.splice(Math.min(2, queue.length), 0, idx);
    } else {
      queue.splice(Math.min(1, queue.length), 0, idx);
    }
    progressFill.style.width = `${Math.round(done.size / total * 100)}%`;
    if (done.size === total) showComplete(); else showCard();
  }

  gotItBtn.addEventListener('click', () => rate('got_it'));
  almostBtn.addEventListener('click', () => rate('almost'));
  noBtn.addEventListener('click', () => rate('no'));

  showCard();
  addHelpButton(container, config.lang, FLASHCARD_HELP_TEXT);
  el.appendChild(container);
}

// --- ordering ---

const ORDERING_HELP_TEXT = {
  en: 'Drag the items up or down to arrange them in the correct order. Click Check Order to submit your answer, Reset to shuffle and start over, or Try Again after submitting.',
  fr: 'Faites glisser les éléments vers le haut ou le bas pour les mettre dans le bon ordre. Cliquez sur Vérifier l\'ordre pour soumettre, Réinitialiser pour recommencer, ou Réessayer après soumission.',
  es: 'Arrastre los elementos hacia arriba o abajo para ordenarlos correctamente. Haga clic en Verificar orden para enviar, Restablecer para mezclar de nuevo, o Reintentar después de enviar.',
};

function parseOrdering(div) {
  const question = div.querySelector('p')?.textContent.trim() ?? '';
  const items    = [...div.querySelectorAll('ol li')].map(li => li.textContent.trim());
  const current_order = [...items];
  shuffle(current_order);
  return { question, items, current_order, shuffle: true, lang: div.dataset.lang ?? 'en' };
}

function renderOrdering(el, config) {
  const container = initWidget(config.question);
  container.appendChild(mk('div', 'forma-instructions', 'Drag items to arrange them in the correct order:'));

  const correct = config.items;
  let current = config.current_order || [...correct];
  let submitted = false;

  const itemsEl = mk('div', 'forma-ordering-items');
  const feedbackEl = mk('div'); feedbackEl.style.display = 'none';

  function renderItems() {
    itemsEl.innerHTML = '';
    current.forEach((text, i) => {
      const item = mk('div', 'forma-ordering-item');
      item.draggable = !submitted;
      item.append(mk('div', 'forma-position', i + 1), mk('div', 'forma-ordering-text', text));
      if (!submitted) {
        item.addEventListener('dragstart', e => { item.classList.add('forma-dragging'); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', i); });
        item.addEventListener('dragend', () => item.classList.remove('forma-dragging'));
        item.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (itemsEl.querySelector('.forma-dragging') !== item) item.classList.add('forma-drop-target'); });
        item.addEventListener('dragleave', () => item.classList.remove('forma-drop-target'));
        item.addEventListener('drop', e => {
          e.preventDefault(); item.classList.remove('forma-drop-target');
          const from = parseInt(e.dataTransfer.getData('text/plain'));
          if (from !== i) { current.splice(i, 0, current.splice(from, 1)[0]); renderItems(); }
        });
      }
      itemsEl.appendChild(item);
    });
  }

  renderItems();

  const { btnRow, submitBtn: checkBtn, tryAgainBtn } = createSubmitRow('Check Order');
  const resetBtn = mk('button', 'forma-btn forma-btn-secondary', 'Reset');
  resetBtn.style.marginRight = '12px';
  btnRow.style.marginBottom = '16px';

  checkBtn.addEventListener('click', () => {
    if (submitted) return;
    submitted = true; checkBtn.disabled = true; resetBtn.style.display = 'none';
    const ok = current.every((v, i) => v === correct[i]);
    [...itemsEl.querySelectorAll('.forma-ordering-item')].forEach((el, i) => {
      el.draggable = false; el.style.cursor = 'default';
      el.classList.add(current[i] === correct[i] ? 'forma-correct' : 'forma-incorrect');
    });
    feedbackEl.textContent = ok ? '✓ Correct order!' : '✗ Incorrect order';
    feedbackEl.className = `forma-feedback ${ok ? 'forma-correct' : 'forma-incorrect'}`;
    feedbackEl.style.display = 'block';
    tryAgainBtn.style.display = 'inline-block';
  });

  resetBtn.addEventListener('click', () => {
    if (submitted) return;
    current = [...correct];
    if (config.shuffle) shuffle(current);
    renderItems(); feedbackEl.style.display = 'none';
  });

  tryAgainBtn.addEventListener('click', () => {
    submitted = false;
    checkBtn.disabled = false;
    tryAgainBtn.style.display = 'none';
    resetBtn.style.display = 'inline-block';
    current = [...correct];
    if (config.shuffle) shuffle(current);
    renderItems();
    feedbackEl.style.display = 'none';
  });

  btnRow.append(checkBtn, resetBtn, tryAgainBtn);
  container.append(itemsEl, btnRow, feedbackEl);
  addHelpButton(container, config.lang, ORDERING_HELP_TEXT);
  el.appendChild(container);
}

// --- labeling ---

const LABELING_HELP_TEXT = {
  en: 'Drag the numbered labels from the left panel and drop them onto the correct text lines on the right. You can remove a placed label by dragging it outside the text area. Click Check Labels when done. Click Try Again to reset and retry.',
  fr: 'Faites glisser les étiquettes numérotées du panneau gauche et déposez-les sur les lignes de texte correctes à droite. Supprimez une étiquette en la faisant glisser hors de la zone de texte. Cliquez sur Vérifier les étiquettes quand vous avez terminé. Cliquez sur Réessayer pour recommencer.',
  es: 'Arrastre las etiquetas numeradas del panel izquierdo y suéltelas en las líneas de texto correctas de la derecha. Elimine una etiqueta arrastrándola fuera del área de texto. Haga clic en Verificar etiquetas cuando termine. Haga clic en Reintentar para volver a intentarlo.',
};

function parseLabeling(div) {
  const question = div.querySelector('p')?.textContent.trim() ?? '';
  const rows = [...div.querySelectorAll('tr')].filter(
    r => r.closest('thead') === null && r.querySelector('th') === null
  );
  const labelNames = [];
  rows.forEach(r => {
    r.cells[1].textContent.split(',').map(s => s.trim()).forEach(name => {
      if (name && !labelNames.includes(name)) labelNames.push(name);
    });
  });
  const text_lines     = rows.map(r => r.cells[0].textContent.trim());
  const correct_labels = Object.fromEntries(rows.map((r, i) => [
    i,
    r.cells[1].textContent.split(',').map(s => labelNames.indexOf(s.trim())),
  ]));
  return { question, labels: labelNames, text_lines, correct_labels, lang: div.dataset.lang ?? 'en' };
}

function renderLabeling(el, config) {
  const container = initWidget(config.question);
  container.appendChild(mk('div', 'forma-instructions', 'Drag label numbers to text lines. Drag outside to remove.'));

  const labels = config.labels, textLines = config.text_lines, correctLabels = config.correct_labels;
  const placed = {};
  let submitted = false;

  const area = mk('div', 'forma-labeling-area');
  const labelsCol = mk('div', 'forma-labeling-labels'), textCol = mk('div', 'forma-labeling-text');
  labelsCol.appendChild(mk('div', 'forma-labeling-title', 'Available Labels:'));
  textCol.appendChild(mk('div', 'forma-labeling-title', 'Text:'));

  labels.forEach((text, i) => {
    const item = mk('div', 'forma-label-item');
    const num = mk('span', 'forma-label-num', i + 1); num.draggable = true;
    num.addEventListener('dragstart', e => { if (submitted) return; e.dataTransfer.effectAllowed = 'copy'; e.dataTransfer.setData('text/plain', i); num.classList.add('forma-dragging'); });
    num.addEventListener('dragend', () => num.classList.remove('forma-dragging'));
    item.append(num, mk('span', 'forma-label-text', text));
    labelsCol.appendChild(item);
  });

  const linesEl = mk('div', 'forma-text-lines');

  function renderBadges(zone, lineIdx) {
    zone.innerHTML = '';
    (placed[lineIdx] || []).forEach(li => {
      const b = mk('span', 'forma-label-badge', li + 1); b.draggable = !submitted; b.dataset.labelIndex = li;
      if (!submitted) {
        b.addEventListener('dragstart', e => { e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', JSON.stringify({ li, from: lineIdx })); b.classList.add('forma-dragging'); });
        b.addEventListener('dragend', e => {
          b.classList.remove('forma-dragging');
          if (e.clientX < textCol.getBoundingClientRect().left) {
            placed[lineIdx] = placed[lineIdx].filter(x => x !== li);
            if (!placed[lineIdx].length) delete placed[lineIdx];
            renderBadges(zone, lineIdx);
          }
        });
      }
      zone.appendChild(b);
    });
  }

  textLines.forEach((text, lineIdx) => {
    const line = mk('div', 'forma-text-line');
    const zone = mk('div', 'forma-label-drop-zone');
    setupDropZone(zone, e => {
      let li, from = null;
      const raw = e.dataTransfer.getData('text/plain');
      try { const d = JSON.parse(raw); if (typeof d === 'object' && d !== null) { li = d.li; from = d.from; } else { li = d; } } catch { li = parseInt(raw); }
      if (from !== null && from !== lineIdx) {
        placed[from] = placed[from].filter(x => x !== li);
        if (!placed[from].length) delete placed[from];
        renderBadges(linesEl.children[from].querySelector('.forma-label-drop-zone'), from);
      }
      if (!placed[lineIdx]) placed[lineIdx] = [];
      if (!placed[lineIdx].includes(li)) placed[lineIdx].push(li);
      renderBadges(zone, lineIdx);
    }, () => submitted);
    line.append(zone, mk('div', 'forma-text-content', text));
    linesEl.appendChild(line);
  });

  textCol.appendChild(linesEl);
  area.append(labelsCol, textCol);
  container.appendChild(area);

  const { btnRow, submitBtn, tryAgainBtn } = createSubmitRow('Check Labels');
  btnRow.style.marginTop = '16px';

  submitBtn.addEventListener('click', () => {
    if (submitted) return;
    submitted = true; submitBtn.disabled = true;
    labelsCol.querySelectorAll('.forma-label-num').forEach(n => { n.draggable = false; n.style.cursor = 'default'; });
    const total = Object.values(correctLabels).reduce((s, a) => s + a.length, 0);
    let score = 0;
    linesEl.querySelectorAll('.forma-text-line').forEach((line, lineIdx) => {
      line.querySelectorAll('.forma-label-badge').forEach(b => {
        const ok = (correctLabels[lineIdx] || []).includes(parseInt(b.dataset.labelIndex));
        if (ok) score++;
        b.classList.add(ok ? 'forma-correct' : 'forma-incorrect');
      });
    });
    const pct = total ? Math.round(score / total * 100) : 0;
    container.appendChild(mk('div', `forma-feedback ${score === total ? 'forma-correct' : 'forma-incorrect'}`, `Score: ${score}/${total} correct (${pct}%)`));
    tryAgainBtn.style.display = 'inline-block';
  });

  tryAgainBtn.addEventListener('click', () => {
    submitted = false;
    submitBtn.disabled = false;
    tryAgainBtn.style.display = 'none';
    labelsCol.querySelectorAll('.forma-label-num').forEach(n => { n.draggable = true; n.style.cursor = ''; });
    Object.keys(placed).forEach(k => delete placed[k]);
    linesEl.querySelectorAll('.forma-text-line').forEach((line, lineIdx) => {
      renderBadges(line.querySelector('.forma-label-drop-zone'), lineIdx);
    });
    const fb = container.querySelector('.forma-feedback');
    if (fb) fb.remove();
  });

  btnRow.append(submitBtn, tryAgainBtn);
  container.appendChild(btnRow);
  addHelpButton(container, config.lang, LABELING_HELP_TEXT);
  el.appendChild(container);
}

// --- registry + auto-mount ---

const WIDGETS = {
  'forma-multiple-choice': [renderMultipleChoice, parseMultipleChoice],
  'forma-flashcard':       [renderFlashcard, parseFlashcard],
  'forma-ordering':        [renderOrdering, parseOrdering],
  'forma-labeling':        [renderLabeling, parseLabeling],
};

export function autoMount(root = document) {
  for (const [cls, [render, parse]] of Object.entries(WIDGETS)) {
    root.querySelectorAll(`.${cls}`).forEach(div => {
      const container = document.createElement('div');
      div.replaceWith(container);
      render(container, parse(div));
    });
  }
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => autoMount());
  } else {
    autoMount();
  }
}
