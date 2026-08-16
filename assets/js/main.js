/* Jupiter Laser & Regenerative Medicine — site interactivity
   Vanilla JS, no dependencies. Loaded with `defer`. */
(function () {
  "use strict";

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ------------------------------------------------------------------
     Sticky header shadow
     ------------------------------------------------------------------ */
  var header = $(".site-header");
  if (header) {
    var onScrollHeader = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScrollHeader, { passive: true });
    onScrollHeader();
  }

  /* ------------------------------------------------------------------
     Mobile nav + dropdowns
     ------------------------------------------------------------------ */
  var burger = $(".nav-burger");

  /* Every close path routes through these two helpers. Closing used to be done
     by stripping the class alone, which left aria-expanded="true" on the burger
     and on any open submenu button — so a screen reader announced the menu as
     open long after it had slid away. */
  function closeSubmenus() {
    $$(".nav > li.open").forEach(function (o) {
      o.classList.remove("open");
      var t = $(".nav-toggle-sub", o);
      if (t) t.setAttribute("aria-expanded", "false");
    });
  }
  function closeNav() {
    document.body.classList.remove("nav-open");
    if (burger) burger.setAttribute("aria-expanded", "false");
    closeSubmenus();
  }

  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open) closeSubmenus();
    });
  }
  // Close mobile nav when a link is chosen
  $$(".site-nav a").forEach(function (a) {
    a.addEventListener("click", closeNav);
  });
  // Submenu toggles (mobile tap + keyboard)
  $$(".nav-toggle-sub").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var li = btn.closest("li");
      var wasOpen = li.classList.contains("open");
      closeSubmenus();
      li.classList.toggle("open", !wasOpen);
      btn.setAttribute("aria-expanded", !wasOpen ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav")) closeSubmenus();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      var wasOpen = document.body.classList.contains("nav-open");
      closeNav();
      // Escape must hand focus back to the control that opened the panel,
      // otherwise focus is left on a node that is now visibility:hidden.
      if (wasOpen && burger) burger.focus();
    }
  });
  /* Rotating a phone with the menu open used to leave body.nav-open set. Past
     1080px the panel reverts to the desktop bar, so the state was invisible but
     still reported as expanded. */
  var deskQuery = window.matchMedia("(min-width: 1080px)");
  var onDesktop = function (e) { if (e.matches) closeNav(); };
  if (deskQuery.addEventListener) deskQuery.addEventListener("change", onDesktop);
  else if (deskQuery.addListener) deskQuery.addListener(onDesktop);

  /* ------------------------------------------------------------------
     Active nav highlighting (from body[data-nav])
     ------------------------------------------------------------------ */
  var navKey = document.body.getAttribute("data-nav");
  if (navKey) {
    var activeLink = $('.nav a[data-nav="' + navKey + '"], .nav button[data-nav="' + navKey + '"]');
    if (activeLink) activeLink.classList.add("active");
  }

  /* ------------------------------------------------------------------
     Reveal on scroll
     ------------------------------------------------------------------ */
  var revealEls = $$("[data-reveal]");
  if ("IntersectionObserver" in window && revealEls.length) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("revealed");
          ro.unobserve(en.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { ro.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("revealed"); });
  }
  // Failsafe: nothing may stay invisible. If an observer callback never fires
  // (fast scroll, restored scroll position, background tab), reveal anyway.
  window.setTimeout(function () {
    revealEls.forEach(function (el) { el.classList.add("revealed"); });
  }, 2500);
  window.addEventListener("beforeprint", function () {
    revealEls.forEach(function (el) { el.classList.add("revealed"); });
  });

  /* ------------------------------------------------------------------
     Animated counters  <b data-counter="90" data-suffix="%">0</b>
     ------------------------------------------------------------------ */
  var counters = $$("[data-counter]");
  if (counters.length && "IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        co.unobserve(en.target);
        var el = en.target;
        var target = parseFloat(el.getAttribute("data-counter"));
        var suffix = el.getAttribute("data-suffix") || "";
        var prefix = el.getAttribute("data-prefix") || "";
        var dur = 1600;
        var start = null;
        var step = function (ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          var val = Math.round(target * eased);
          el.textContent = prefix + val.toLocaleString() + suffix;
          if (p < 1) { requestAnimationFrame(step); }
          else { el.classList.add("counted"); }
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* ------------------------------------------------------------------
     FAQ search + category filter
     ------------------------------------------------------------------ */
  var faqSearch = $("#faq-search");
  var faqItems = $$("details.faq");
  var faqEmpty = $("#faq-empty");
  var activeCat = "all";

  function applyFaqFilter() {
    if (!faqItems.length) return;
    var q = faqSearch ? faqSearch.value.trim().toLowerCase() : "";
    var visible = 0;
    faqItems.forEach(function (d) {
      var matchesCat = activeCat === "all" || (d.getAttribute("data-cat") || "") === activeCat;
      var matchesQ = !q || d.textContent.toLowerCase().indexOf(q) !== -1;
      var show = matchesCat && matchesQ;
      d.classList.toggle("hidden", !show);
      if (show) visible++;
      if (q && show && q.length > 2) d.open = true;
    });
    $$(".faq-group-title").forEach(function (t) {
      var group = t.getAttribute("data-group");
      var any = faqItems.some(function (d) {
        return !d.classList.contains("hidden") && d.getAttribute("data-cat") === group;
      });
      t.style.display = any ? "" : "none";
    });
    if (faqEmpty) faqEmpty.classList.toggle("visible", visible === 0);
  }
  if (faqSearch) faqSearch.addEventListener("input", applyFaqFilter);
  $$(".faq-cat").forEach(function (btn) {
    btn.addEventListener("click", function () {
      $$(".faq-cat").forEach(function (b) {
        b.classList.remove("active");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      activeCat = btn.getAttribute("data-cat") || "all";
      applyFaqFilter();
    });
  });

  /* ------------------------------------------------------------------
     Testimonial slider (scroll-snap + buttons + gentle autoplay)
     ------------------------------------------------------------------ */
  $$("[data-slider]").forEach(function (slider) {
    var track = $(".testi-track", slider);
    if (!track) return;
    var prev = $("[data-prev]", slider);
    var next = $("[data-next]", slider);
    var cardW = function () {
      var card = track.firstElementChild;
      if (!card) return 320;
      var gap = parseFloat(getComputedStyle(track).columnGap || 20);
      return card.getBoundingClientRect().width + gap;
    };
    var go = function (dir) {
      var max = track.scrollWidth - track.clientWidth - 4;
      var target = track.scrollLeft + dir * cardW();
      if (dir > 0 && track.scrollLeft >= max) target = 0;
      if (dir < 0 && track.scrollLeft <= 2) target = track.scrollWidth;
      track.scrollTo({ left: target, behavior: "smooth" });
    };
    if (prev) prev.addEventListener("click", function () { go(-1); });
    if (next) next.addEventListener("click", function () { go(1); });
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduced) {
      var timer = setInterval(function () { go(1); }, 6500);
      ["pointerdown", "touchstart", "mouseenter"].forEach(function (ev) {
        slider.addEventListener(ev, function () { clearInterval(timer); }, { once: true, passive: true });
      });
    }
  });

  /* ------------------------------------------------------------------
     "Is laser therapy right for me?" quiz
     ------------------------------------------------------------------ */
  var quiz = $("#laser-quiz");
  if (quiz) {
    var steps = $$(".quiz-step", quiz);
    var bar = $(".quiz-progress i", quiz);
    var idx = 0;
    var score = 0;
    var setStep = function (i) {
      idx = i;
      steps.forEach(function (s, n) { s.classList.toggle("active", n === i); });
      if (bar) bar.style.width = Math.round((i / (steps.length - 1)) * 100) + "%";
    };
    $$(".quiz-opt", quiz).forEach(function (btn) {
      btn.addEventListener("click", function () {
        score += parseInt(btn.getAttribute("data-pts") || "0", 10);
        if (idx < steps.length - 2) {
          setStep(idx + 1);
        } else {
          // result step
          var res = $(".quiz-result", quiz);
          var strong = score >= 6;
          var mid = score >= 3 && score < 6;
          $(".quiz-icon", res).textContent = strong ? "🎯" : (mid ? "👍" : "💬");
          $(".quiz-title", res).textContent = strong
            ? "You look like a strong candidate for laser therapy"
            : mid
              ? "Laser therapy may be a great fit — let's confirm"
              : "Let's talk through your options together";
          $(".quiz-copy", res).textContent = strong
            ? "Based on your answers, your symptoms match the conditions MLS laser therapy treats most successfully — chronic pain, inflammation, and slow-healing soft tissue. The next step is a quick evaluation with Dr. Cedeno to build your treatment plan."
            : mid
              ? "Several of your answers suggest you could benefit from drug-free laser or regenerative treatment. An in-person evaluation with Dr. Cedeno will confirm whether it's the right first step for your specific condition."
              : "Your situation may need a closer look before choosing a treatment path. Dr. Cedeno will examine your foot and ankle, explain what's going on, and walk you through every option — conservative to advanced.";
          setStep(steps.length - 1);
        }
      });
    });
    var restart = $(".quiz-restart", quiz);
    if (restart) restart.addEventListener("click", function () { score = 0; setStep(0); });
    setStep(0);
  }

  /* ------------------------------------------------------------------
     Hero video: pause control (WCAG 2.2.2 — auto-playing motion longer
     than 5s must be pausable) + honor prefers-reduced-motion.
     ------------------------------------------------------------------ */
  var heroVideo = $("#hero-video");
  var videoToggle = $("#video-toggle");
  if (heroVideo && videoToggle) {
    // Attach exactly one source so only that file is ever downloaded. Under
    // prefers-reduced-motion we attach nothing at all and leave the poster —
    // no reason to spend 25MB of someone's data on motion they asked not to see.
    if (!heroVideo.querySelector("source") && heroVideo.dataset.mp4Full) {
      var wantsMotion = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (wantsMotion) {
        var small = window.matchMedia("(max-width: 767px)").matches;
        // MP4 first: it is the smaller file in both tiers and every mainstream
        // browser decodes H.264. WebM second, for builds without proprietary
        // codecs (some Linux Firefox/Chromium) that would otherwise show only
        // the poster. The browser downloads the FIRST source it can play, so
        // normal visitors never fetch both.
        [
          [small ? heroVideo.dataset.mp4Mobile : heroVideo.dataset.mp4Full, "video/mp4"],
          [small ? heroVideo.dataset.webmMobile : heroVideo.dataset.webmFull, "video/webm"]
        ].forEach(function (pair) {
          if (!pair[0]) return;
          var s = document.createElement("source");
          s.src = pair[0];
          s.type = pair[1];
          heroVideo.appendChild(s);
        });
        heroVideo.load();
        var kick = heroVideo.play();
        if (kick && kick.catch) kick.catch(function () {});
      }
    }
    // Cinematic drift — 0.75x, not 0.5x: on a 30fps source half speed lands at
    // an effective 15fps and judders.
    var setRate = function () { heroVideo.playbackRate = 0.75; };
    setRate();
    heroVideo.addEventListener("loadeddata", setRate);
    heroVideo.addEventListener("play", setRate);
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    var setPaused = function (paused) {
      if (paused) {
        heroVideo.pause();
      } else {
        var playing = heroVideo.play();
        if (playing && playing.catch) playing.catch(function () {});
      }
      videoToggle.setAttribute("aria-pressed", paused ? "true" : "false");
      videoToggle.setAttribute("aria-label", paused ? "Play background video" : "Pause background video");
    };
    if (reducedMotion.matches) setPaused(true);
    reducedMotion.addEventListener("change", function (e) { setPaused(e.matches); });
    videoToggle.addEventListener("click", function () {
      setPaused(videoToggle.getAttribute("aria-pressed") !== "true");
    });
    // Hide the control only when there is genuinely nothing to pause. A <source>
    // that fails bubbles an error event here too — that is the normal MP4 ->
    // WebM fallback, and swallowing it used to strip the pause control off a
    // perfectly good playing video (WCAG 2.2.2 needs it).
    var hideToggle = function () { videoToggle.style.display = "none"; };
    heroVideo.addEventListener("error", function (e) {
      if (e.target !== heroVideo) return;              // a <source> failing is fine
      hideToggle();
    }, true);
    // NETWORK_NO_SOURCE: every candidate failed, so only the poster is showing.
    heroVideo.addEventListener("loadstart", function () {
      if (heroVideo.networkState === 3) hideToggle();
    });
    // Under prefers-reduced-motion we attach no sources at all, so there is no
    // motion to pause either.
    if (!heroVideo.querySelector("source")) hideToggle();
  }

  /* ------------------------------------------------------------------
     Back to top
     ------------------------------------------------------------------ */
  var toTop = $(".to-top");
  if (toTop) {
    window.addEventListener("scroll", function () {
      toTop.classList.toggle("visible", window.scrollY > 700);
    }, { passive: true });
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ------------------------------------------------------------------
     Contact form (Formspree-style endpoint; graceful fallback)
     ------------------------------------------------------------------ */
  var form = $("#contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = $("#form-status");
      var action = form.getAttribute("action") || "";
      var btn = $('button[type="submit"]', form);
      btn.disabled = true;
      btn.textContent = "Sending…";
      fetch(action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      }).then(function (r) {
        if (r.ok) {
          status.className = "form-status ok";
          status.textContent = "Thank you! Your request has been received — our team will call you shortly to confirm your appointment.";
          form.reset();
        } else {
          throw new Error("bad status");
        }
      }).catch(function () {
        status.className = "form-status err";
        status.textContent = "Something went wrong sending your request. Please call us at (561) 915-1934 and we'll take care of you.";
      }).finally(function () {
        btn.disabled = false;
        btn.textContent = "Request Appointment";
      });
    });
  }

  /* ------------------------------------------------------------------
     Current year in footer
     ------------------------------------------------------------------ */
  $$("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
  /* ------------------------------------------------------------------
     Horizontally scrolling comparison tables
     table.compare carries min-width:640px, so below ~700px it scrolls inside
     .table-scroll. Two things were missing: the region was unreachable by
     keyboard (a scroll container needs to be focusable to be scrolled without
     a mouse — WCAG 2.1.1), and nothing on screen said it scrolled, so on a
     phone the table simply looked cropped at the right edge.
     ------------------------------------------------------------------ */
  $$(".table-scroll").forEach(function (box) {
    // The hint is injected rather than authored into each page so all three
    // comparison tables stay in step. aria-hidden: the region label already
    // tells assistive tech the table scrolls, so this would only repeat it.
    var hint = document.createElement("p");
    hint.className = "table-hint";
    hint.setAttribute("aria-hidden", "true");
    hint.textContent = "Swipe the table sideways to compare →";
    if (box.parentNode) box.parentNode.insertBefore(hint, box.nextSibling);

    var sync = function () {
      var scrollable = box.scrollWidth > box.clientWidth + 1;
      box.toggleAttribute("data-scrollable", scrollable);
      if (scrollable) {
        if (!box.hasAttribute("tabindex")) box.setAttribute("tabindex", "0");
        box.setAttribute("role", "region");
        if (!box.hasAttribute("aria-label")) {
          // Name the region after the heading it sits under, so a screen
          // reader announces "Comparison table: <heading>" rather than "region".
          var h = box.closest("section, article, div.wrap");
          var head = h && h.querySelector("h2, h3");
          box.setAttribute("aria-label", head
            ? "Comparison table: " + head.textContent.trim()
            : "Comparison table, scrolls horizontally");
        }
      } else {
        box.removeAttribute("tabindex");
        box.removeAttribute("role");
      }
    };
    sync();
    window.addEventListener("resize", sync, { passive: true });
  });

})();


/* ==========================================================================
   Dynamic layer: scroll rail, live open/closed status, stat rings, parallax.
   Appended as its own IIFE so it can't disturb the code above.
   ========================================================================== */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Scroll progress rail ---- */
  var rail = document.querySelector(".scroll-rail i");
  if (rail) {
    var onScroll = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      rail.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
  }

  /* ---- Live open/closed pill (visitor's own clock) ----
     Mon–Thu 8:00–17:00, Fri 8:00–14:00, lunch 12:30–13:30, closed weekends. */
  var pill = document.getElementById("live-status");
  if (pill) {
    var render = function () {
      var now = new Date();
      var day = now.getDay();            // 0 Sun .. 6 Sat
      var mins = now.getHours() * 60 + now.getMinutes();
      var open = false, note = "Closed";
      if (day >= 1 && day <= 5) {
        var close = day === 5 ? 14 * 60 : 17 * 60;
        var lunch = mins >= 12 * 60 + 30 && mins < 13 * 60 + 30;
        if (mins >= 8 * 60 && mins < close && !lunch) {
          open = true;
          note = "Open now";
        } else if (lunch) {
          note = "Back at 1:30";
        } else if (mins < 8 * 60) {
          note = "Opens 8:00 AM";
        } else {
          note = "Closed";
        }
      } else {
        note = day === 6 ? "Sat — by appt" : "Closed Sunday";
      }
      pill.hidden = false;
      pill.classList.toggle("closed", !open);
      pill.querySelector(".txt").textContent = note;
      pill.setAttribute("title", open ? "Our office is open right now" : "Office hours: Mon–Thu 8–5, Fri 8–2");
    };
    render();
    setInterval(render, 60000);
  }

  /* ---- Stat rings draw in on scroll ---- */
  var rings = Array.prototype.slice.call(document.querySelectorAll(".statring-dial .fill"));
  if (rings.length) {
    var C = 2 * Math.PI * 40; // r=40
    rings.forEach(function (r) { r.style.strokeDasharray = C; r.style.strokeDashoffset = C; });
    if ("IntersectionObserver" in window && !reduced) {
      var ro = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          ro.unobserve(e.target);
          var pct = parseFloat(e.target.getAttribute("data-ring")) || 0;
          e.target.style.strokeDashoffset = C * (1 - pct / 100);
        });
      }, { threshold: 0.4 });
      rings.forEach(function (r) { ro.observe(r); });
    } else {
      rings.forEach(function (r) {
        var pct = parseFloat(r.getAttribute("data-ring")) || 0;
        r.style.strokeDashoffset = C * (1 - pct / 100);
      });
    }
  }

  /* ---- Hero parallax drift ---- */
  var media = document.querySelector(".hero-media");
  if (media && !reduced) {
    media.classList.add("parallax");
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        if (y < window.innerHeight * 1.2) {
          media.style.transform = "translate3d(0," + (y * 0.18).toFixed(1) + "px,0) scale(1.06)";
        }
        ticking = false;
      });
    }, { passive: true });
  }
})();
