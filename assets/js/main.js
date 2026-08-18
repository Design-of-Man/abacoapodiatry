/* Abacoa Podiatry & Leg Vein Center — site interactivity
   Vanilla JS, no dependencies. Loaded with `defer`. */
(function () {
  "use strict";

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ------------------------------------------------------------------
     Lead tracking

     The phone is this practice's main lead channel and nothing counted it,
     so there was no way to answer "did leads fall?" -- the question the
     whole site is judged on. Two events are real leads (a call started, a
     form sent); appointment_cta is the funnel step between them.

     Deliberately no condition detail in the payload. Vercel already records
     which page an event fired on, and that is aggregate and anonymous;
     attaching "plantar fasciitis" to an individual visitor's action is the
     line that turns analytics into a health-privacy problem. Placement only.
     ------------------------------------------------------------------ */
  var track = function (name, data) {
    if (typeof window.va === "function") window.va("event", { name: name, data: data || {} });
  };

  var placementOf = function (el) {
    if (el.closest(".call-bar, .cb-call")) return "mobile-call-bar";
    if (el.closest(".site-header")) return "header";
    if (el.closest(".assistant, .assist-note")) return "assistant";
    if (el.closest("footer, .site-footer")) return "footer";
    return "body";
  };

  // Delegated so it covers every tel: and /contact/ link on any page, including
  // markup added later, without each template having to opt in.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("tel:") === 0) {
      track("call_click", { placement: placementOf(a) });
    } else if (href === "/contact/" || href === "/request-an-appointment/") {
      track("appointment_cta", { placement: placementOf(a) });
    }
  }, { passive: true, capture: true });

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
    // no reason to spend the encode on motion they asked not to see.
    if (!heroVideo.querySelector("source") && heroVideo.dataset.mp4Full) {
      var wantsMotion = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      // Save-Data is an explicit "don't spend my bandwidth", and 2g is a
      // connection that cannot afford a decorative hero at any encode. Both
      // keep the poster, which is what the video is layered over anyway.
      var conn = navigator.connection || {};
      var starved = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || "");
      if (wantsMotion && !starved) {
        // 1024, not 767. The HD encode was 25MB when this breakpoint was set;
        // it is 5.7MB now, but the tier split still earns its keep because the
        // mobile encode is smaller again.
        var small = window.matchMedia("(max-width: 1024px)").matches;
        // MP4 first: it is the smaller file in both tiers and every mainstream
        // browser decodes H.264. The browser downloads the FIRST source it can
        // play, so normal visitors never fetch both.
        //
        // The small tier is MP4-only on purpose. WebM exists here as a fallback
        // for builds without proprietary codecs, but the mobile WebM is 4.6MB
        // against the mobile MP4's 2.2MB -- larger than the file it exists to
        // improve on. On the tier where data costs the most it earns nothing,
        // so those browsers keep the poster instead of spending 4.6MB.
        (small
          ? [[heroVideo.dataset.mp4Mobile, "video/mp4"]]
          : [[heroVideo.dataset.mp4Full, "video/mp4"],
             [heroVideo.dataset.webmFull, "video/webm"]]
        ).forEach(function (pair) {
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
    // The drift used to be done here with playbackRate = 0.75. On a 30fps
    // source that plays 22.5 frames a second, and at 60Hz each frame then
    // occupies 2.67 refreshes -- so the browser holds some frames for two
    // refreshes and others for three. That uneven cadence is what read as
    // judder on a slow drone pan. The encode is now slowed in the file itself
    // with motion interpolation to a true 30fps, so it plays at 1.0x and every
    // frame gets exactly two refreshes. Do not reintroduce playbackRate here.
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
      // JSON rather than FormData: Vercel's Node runtime parses
      // application/json into req.body, and does not parse multipart.
      var payload = {};
      new FormData(form).forEach(function (v, k) { payload[k] = v; });
      fetch(action, {
        method: "POST",
        body: JSON.stringify(payload),
        headers: { "Content-Type": "application/json", Accept: "application/json" }
      }).then(function (r) {
        // A 2xx is still not proof on its own, and the reason is worth keeping
        // even though the backend changed. Under FormSubmit this endpoint
        // answered 200 with {"success":"false"} whenever the recipient address
        // had never been activated, so trusting the status code alone would
        // thank the patient, fire a conversion and drop the lead all at once.
        // api/contact.js now answers success:"true" only after the request is
        // written to the database. Read the body and believe that instead.
        if (!r.ok) throw new Error("http " + r.status);
        return r.json();
      }).then(function (data) {
        // success comes back as the string "true" rather than a boolean.
        var delivered = data && String(data.success).toLowerCase() === "true";
        if (!delivered) throw new Error("not delivered");
        status.className = "form-status ok";
        status.textContent = "Thank you! Your request has been received — our team will call you shortly to confirm your appointment.";
        // Fires on confirmed delivery, not on submit, so a failed send is
        // never counted as a lead. No field values are sent -- the visitor
        // typed their name and symptoms into this form.
        track("form_submit", { form: "contact" });
        form.reset();
      }).catch(function () {
        // Anything unexpected -- non-JSON body, network failure, a 502 because
        // the database write failed, a 400 because the request was incomplete
        // -- lands here and sends the patient to the phone. Erring toward a
        // visible failure is the right direction: a wasted phone call costs
        // less than a lead that silently evaporates.
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
   Dynamic layer: scroll rail, live open/closed status, stat rings.
   Appended as its own IIFE so it can't disturb the code above.
   ========================================================================== */
(function () {
  "use strict";

  /* ---- Scroll progress rail ---- */
  var rail = document.querySelector(".scroll-rail i");
  if (rail) {
    // Two things used to make this the worst jank on the page. It wrote
    // style.width on every scroll event, which is a layout property, and it
    // read scrollHeight first -- a forced synchronous reflow, every event, the
    // whole length of the page. Now the height is cached, the write is a
    // composited scaleX, and the work is rAF-throttled to one per frame.
    var railH = 0;
    var railTicking = false;
    var measureRail = function () {
      railH = document.documentElement.scrollHeight - window.innerHeight;
    };
    var paintRail = function () {
      var p = railH > 0 ? window.scrollY / railH : 0;
      if (p < 0) p = 0; else if (p > 1) p = 1;
      rail.style.transform = "scaleX(" + p.toFixed(4) + ")";
      railTicking = false;
    };
    var onScroll = function () {
      if (railTicking) return;
      railTicking = true;
      requestAnimationFrame(paintRail);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { measureRail(); onScroll(); });
    measureRail();
    paintRail();
  }

  /* ---- Live open/closed pill: removed 2026-08-15 ----
     This read getElementById("live-status"), and no element with that id has
     ever existed -- not in the template, not in any page, not in locations.py.
     It had never rendered, so its hours were never visibly wrong, which is
     also why nobody noticed they were only ever Jupiter's.

     It is not coming back in this shape. The practice now runs two offices on
     different schedules -- Jupiter Mon-Thu 8-5 / Fri 8-2, Palm Beach Gardens
     Mon & Wed 8-4:30 -- and a single sitewide pill has no way to know which
     office a visitor on /services/mls-laser-therapy/ means. On a Tuesday at
     10am it would read "Open now", which is true for Jupiter and false for the
     Gardens. It also used the visitor's own clock rather than America/New_York,
     so it was wrong for anyone travelling.

     If it returns it belongs on the office cards on /locations/ and the Palm
     Beach Gardens office page, reading a per-office data-hours attribute and
     resolving time in America/New_York. */

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

  /* ---- Hero parallax drift: removed 2026-08-14 ----
     This transformed .hero-media on every scroll frame, and .hero-media holds
     the playing background video. Moving and scaling a live video layer makes
     the compositor resample every decoded frame against a changing matrix, so
     the hero visibly stuttered while scrolling even though the handler was
     already rAF-throttled. The drift was worth a few pixels of depth and cost
     the smoothness of the first thing anyone sees. If it comes back, apply it
     to .hero-glass or the beams -- never to the video. */
})();
