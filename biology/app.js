/* ==========================================================================
   Плеер презентации: навигация, миниатюры, заметки учителя, полный экран
   ========================================================================== */
(function () {
  "use strict";

  var slides = (window.SLIDES || []).slice().sort(function (a, b) { return a.n - b.n; });
  var total = slides.length;
  var index = 0;

  var slideImg   = document.getElementById("slideImg");
  var slideChip  = document.getElementById("slideChip");
  var notesTitle = document.getElementById("notesTitle");
  var notesBody  = document.getElementById("notesBody");
  var notesPanel = document.getElementById("notesPanel");
  var notesToggle= document.getElementById("notesToggle");
  var progressFill = document.getElementById("progressFill");
  var thumbsEl   = document.getElementById("thumbs");
  var prevBtn    = document.getElementById("prevBtn");
  var nextBtn    = document.getElementById("nextBtn");
  var prevBtn2   = document.getElementById("prevBtn2");
  var nextBtn2   = document.getElementById("nextBtn2");
  var fullBtn    = document.getElementById("fullBtn");
  var stageWrap  = document.getElementById("stageWrap");

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function src(n) { return "assets/slides/slide-" + pad(n) + ".png"; }
  function thumbSrc(n) { return "assets/thumbs/slide-" + pad(n) + ".png"; }

  /* ------------------------------ Миниатюры ------------------------------ */
  function buildThumbs() {
    var frag = document.createDocumentFragment();
    slides.forEach(function (s, i) {
      var b = document.createElement("button");
      b.className = "thumb";
      b.type = "button";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-label", "Слайд " + s.n + ": " + s.title);
      b.dataset.i = i;
      b.innerHTML = '<img loading="lazy" src="' + thumbSrc(s.n) + '" alt="">' +
                    "<span>" + s.n + "</span>";
      b.addEventListener("click", function () { go(i); });
      frag.appendChild(b);
    });
    thumbsEl.appendChild(frag);
  }

  /* ------------------------------- Отрисовка ----------------------------- */
  function render() {
    var s = slides[index];
    if (!s) return;

    slideImg.src = src(s.n);
    slideImg.alt = "Слайд " + s.n + ": " + s.title;
    slideChip.textContent = s.n + " / " + total;
    notesTitle.textContent = s.title;
    notesBody.textContent = s.notes || "Для этого слайда заметок нет.";

    progressFill.style.width = ((index + 1) / total * 100) + "%";

    prevBtn.disabled = nextBtn.disabled = index === 0;
    prevBtn2.disabled = index === 0;
    nextBtn2.disabled = index === total - 1;

    var active = thumbsEl.querySelector(".thumb.active");
    if (active) active.classList.remove("active");
    var cur = thumbsEl.children[index];
    if (cur) {
      cur.classList.add("active");
      var l = cur.offsetLeft - thumbsEl.clientWidth / 2 + cur.clientWidth / 2;
      thumbsEl.scrollTo({ left: Math.max(0, l), behavior: "smooth" });
    }

    document.title = s.title + " — Многощетинковые черви. Пиявки";
  }

  function go(i) {
    index = Math.max(0, Math.min(total - 1, i));
    render();
  }
  function next() { if (index < total - 1) go(index + 1); }
  function prev() { if (index > 0) go(index - 1); }

  /* ------------------------------- События ------------------------------- */
  prevBtn.addEventListener("click", prev);
  prevBtn2.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);
  nextBtn2.addEventListener("click", next);

  document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    switch (e.key) {
      case "ArrowRight":
      case "PageDown":
      case " ": e.preventDefault(); next(); break;
      case "ArrowLeft":
      case "PageUp": e.preventDefault(); prev(); break;
      case "Home": e.preventDefault(); go(0); break;
      case "End": e.preventDefault(); go(total - 1); break;
      case "n": case "N": case "т": case "Т": toggleNotes(); break;
      case "f": case "F": case "а": case "А": toggleFull(); break;
    }
  });

  /* --------------------------- Заметки учителя --------------------------- */
  function toggleNotes() {
    var hidden = notesPanel.classList.toggle("hidden");
    notesToggle.setAttribute("aria-pressed", hidden ? "false" : "true");
  }
  notesToggle.addEventListener("click", toggleNotes);

  /* ------------------------------ Полный экран --------------------------- */
  function toggleFull() {
    if (!document.fullscreenElement) {
      (stageWrap.requestFullscreen || stageWrap.webkitRequestFullscreen || function () {}).call(stageWrap);
    } else {
      (document.exitFullscreen || document.webkitExitFullscreen || function () {}).call(document);
    }
  }
  fullBtn.addEventListener("click", toggleFull);

  /* --------------------------- Свайпы (моб.) ----------------------------- */
  var tx = 0;
  stageWrap.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
  stageWrap.addEventListener("touchend", function (e) {
    var dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); }
  }, { passive: true });

  /* -------------------------------- Старт -------------------------------- */
  buildThumbs();
  render();
})();
