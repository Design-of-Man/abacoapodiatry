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
  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  // Close mobile nav when a link is chosen
  $$(".site-nav a").forEach(function (a) {
    a.addEventListener("click", function () {
      document.body.classList.remove("nav-open");
    });
  });
  // Submenu toggles (mobile tap + keyboard)
  $$(".nav-toggle-sub").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var li = btn.closest("li");
      var wasOpen = li.classList.contains("open");
      $$(".nav > li.open").forEach(function (o) { o.classList.remove("open"); });
      li.classList.toggle("open", !wasOpen);
      btn.setAttribute("aria-expanded", !wasOpen ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav")) {
      $$(".nav > li.open").forEach(function (o) { o.classList.remove("open"); });
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.body.classList.remove("nav-open");
      $$(".nav > li.open").forEach(function (o) { o.classList.remove("open"); });
    }
  });

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
          if (p < 1) requestAnimationFrame(step);
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
     Foot pain map
     ------------------------------------------------------------------ */
  var hotspots = $$(".hotspot");
  if (hotspots.length) {
    var showSpot = function (id) {
      $$(".painmap-card").forEach(function (c) {
        c.classList.toggle("active", c.getAttribute("data-spot") === id);
      });
      hotspots.forEach(function (h) {
        h.classList.toggle("active", h.getAttribute("data-spot") === id);
      });
    };
    hotspots.forEach(function (h) {
      var activate = function () { showSpot(h.getAttribute("data-spot")); };
      h.addEventListener("click", activate);
      h.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); activate(); }
      });
    });
    // show the first card by default
    var first = $(".painmap-card");
    if (first) showSpot(first.getAttribute("data-spot"));
  }

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
    // Cinematic half-speed drift
    var setRate = function () { heroVideo.playbackRate = 0.5; };
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
    // If the video can't load, hide the control so it isn't a dead button.
    heroVideo.addEventListener("error", function () { videoToggle.style.display = "none"; }, true);
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
})();
