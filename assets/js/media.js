/* Media page: renders the full video library as a thumbnail grid and plays
   any video in an expanding lightbox. Manifest comes from
   assets/data/videos.js (generated at deploy time). With no manifest, the
   embedded playlist player fallback stays visible instead. */
(function () {
  "use strict";

  var videos = window.JL_VIDEOS || [];
  var grid = document.getElementById("video-grid");
  var fallback = document.getElementById("playlist-fallback");
  var counter = document.getElementById("video-count");
  if (!grid) return;

  if (!videos.length) {
    // No manifest — keep the playlist embed, hide the empty grid shell.
    grid.parentElement.style.display = "none";
    return;
  }

  if (counter) counter.textContent = videos.length + " videos in the library";

  /* ---- Build the grid ---- */
  videos.forEach(function (v) {
    var card = document.createElement("button");
    card.type = "button";
    card.className = "video-card";
    card.setAttribute("aria-label", "Play video: " + v.title);
    card.innerHTML =
      '<span class="video-thumb">' +
      '<img loading="lazy" src="https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg" alt="">' +
      '<span class="video-play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.2v13.6a1 1 0 0 0 1.5.9l11-6.8a1 1 0 0 0 0-1.7l-11-6.8a1 1 0 0 0-1.5.8Z"/></svg></span>' +
      "</span>" +
      '<span class="video-title"></span>';
    card.querySelector(".video-title").textContent = v.title;
    card.addEventListener("click", function () { openModal(v); });
    grid.appendChild(card);
  });

  /* ---- Hydrate real titles (best-effort; placeholders stay on failure) ---- */
  videos.forEach(function (v, i) {
    if (!/Abacoa Podiatry — Foot & Ankle Care/.test(v.title)) return; // already real
    fetch("https://noembed.com/embed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + v.id)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.title) {
          v.title = d.title;
          var el = grid.children[i] && grid.children[i].querySelector(".video-title");
          if (el) el.textContent = d.title;
          grid.children[i].setAttribute("aria-label", "Play video: " + d.title);
        }
      }).catch(function () {});
  });

  /* ---- Lightbox ---- */
  var modal = document.createElement("div");
  modal.className = "video-modal";
  modal.hidden = true;
  modal.innerHTML =
    '<div class="video-modal-backdrop"></div>' +
    '<div class="video-modal-box" role="dialog" aria-modal="true" aria-label="Video player">' +
    '<button class="video-modal-close" aria-label="Close video">&times;</button>' +
    '<div class="video-modal-frame"></div>' +
    '<p class="video-modal-title"></p>' +
    "</div>";
  document.body.appendChild(modal);

  var frame = modal.querySelector(".video-modal-frame");
  var titleEl = modal.querySelector(".video-modal-title");
  var closeBtn = modal.querySelector(".video-modal-close");
  var lastFocus = null;

  function openModal(v) {
    lastFocus = document.activeElement;
    titleEl.textContent = v.title;
    frame.innerHTML =
      '<iframe src="https://www.youtube-nocookie.com/embed/' + v.id +
      '?autoplay=1&rel=0" title="' + v.title.replace(/"/g, "&quot;") +
      '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    closeBtn.focus();
  }

  function closeModal() {
    modal.hidden = true;
    frame.innerHTML = ""; // stops playback
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }

  closeBtn.addEventListener("click", closeModal);
  modal.querySelector(".video-modal-backdrop").addEventListener("click", closeModal);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) closeModal();
  });
})();
