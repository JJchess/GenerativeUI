<html lang="en" data-astro-cid-bvzihdzo="">
  <head>
    <!-- Global Metadata -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="color-scheme" content="light dark" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <link rel="sitemap" href="/sitemap-index.xml" />
    <link
      rel="alternate"
      type="application/rss+xml"
      title="/dev/michael"
      href="https://michaellivs.com/rss.xml"
    />
    <meta name="generator" content="Astro v5.16.2" />
    <!-- Canonical URL -->
    <link
      rel="canonical"
      href="https://michaellivs.com/blog/reverse-engineering-claude-generative-ui/"
    />
    <!-- Primary Meta Tags -->
    <title>
      Reverse-engineering Claude's generative UI - then building it for the
      terminal
    </title>
    <meta
      name="title"
      content="Reverse-engineering Claude's generative UI - then building it for the terminal"
    />
    <meta
      name="description"
      content="Extracting Anthropic's design system from a conversation export and rebuilding generative UI for the terminal."
    />
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article" />
    <meta
      property="og:url"
      content="https://michaellivs.com/blog/reverse-engineering-claude-generative-ui/"
    />
    <meta
      property="og:title"
      content="Reverse-engineering Claude's generative UI - then building it for the terminal"
    />
    <meta
      property="og:description"
      content="Extracting Anthropic's design system from a conversation export and rebuilding generative UI for the terminal."
    />
    <meta
      property="og:image"
      content="https://michaellivs.com/og/reverse-engineering-claude-generative-ui.png"
    />
    <meta
      property="article:published_time"
      content="2026-03-13T00:00:00.000Z"
    />
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image" />
    <meta
      property="twitter:url"
      content="https://michaellivs.com/blog/reverse-engineering-claude-generative-ui/"
    />
    <meta
      property="twitter:title"
      content="Reverse-engineering Claude's generative UI - then building it for the terminal"
    />
    <meta
      property="twitter:description"
      content="Extracting Anthropic's design system from a conversation export and rebuilding generative UI for the terminal."
    />
    <meta
      property="twitter:image"
      content="https://michaellivs.com/og/reverse-engineering-claude-generative-ui.png"
    />
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json" data-astro-exec="">
      {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "Reverse-engineering Claude's generative UI - then building it for the terminal",
        "description": "Extracting Anthropic's design system from a conversation export and rebuilding generative UI for the terminal.",
        "url": "https://michaellivs.com/blog/reverse-engineering-claude-generative-ui/",
        "datePublished": "2026-03-13T00:00:00.000Z",
        "dateModified": "2026-03-13T00:00:00.000Z",
        "author": {
          "@type": "Person",
          "name": "Michael Livshits",
          "url": "https://michaellivs.com"
        },
        "publisher": { "@type": "Person", "name": "Michael Livshits" },
        "image": "https://michaellivs.com/og/reverse-engineering-claude-generative-ui.png"
      }
    </script>
    <!-- Vercel Speed Insights -->
    <script
      src="/_vercel/speed-insights/script.js"
      defer=""
      data-sdkn="@vercel/speed-insights/astro"
      data-sdkv="1.3.1"
      data-route="/blog/[slug]/"
      data-astro-exec=""
    ></script>
    <script
      src="/_vercel/insights/script.js"
      defer=""
      data-sdkn="@vercel/analytics/astro"
      data-sdkv="1.6.1"
      data-disable-auto-track="1"
    ></script>
    <link
      rel="prefetch"
      href="https://michaellivs.com/blog/sandbox-comparison-2026"
    />
    <link rel="prefetch" href="https://michaellivs.com/tags/agents/" />
    <link
      rel="prefetch"
      href="https://michaellivs.com/tags/reverse-engineering/"
    />
  </head>
  <body data-astro-cid-bvzihdzo="">
    <vercel-speed-insights
      data-props="{}"
      data-params='{"slug":"reverse-engineering-claude-generative-ui"}'
      data-pathname="/blog/reverse-engineering-claude-generative-ui/"
    ></vercel-speed-insights>
    <script type="module" data-astro-exec="">
      var o = "@vercel/speed-insights",
        u = "1.3.1",
        f = () => {
          window.si ||
            (window.si = function (...r) {
              (window.siq = window.siq || []).push(r);
            });
        };
      function l() {
        return typeof window < "u";
      }
      function h() {
        try {
          const e = "production";
        } catch {}
        return "production";
      }
      function d() {
        return h() === "development";
      }
      function v(e, r) {
        if (!e || !r) return e;
        let n = e;
        try {
          const t = Object.entries(r);
          for (const [s, i] of t)
            if (!Array.isArray(i)) {
              const a = c(i);
              a.test(n) && (n = n.replace(a, `/[${s}]`));
            }
          for (const [s, i] of t)
            if (Array.isArray(i)) {
              const a = c(i.join("/"));
              a.test(n) && (n = n.replace(a, `/[...${s}]`));
            }
          return n;
        } catch {
          return e;
        }
      }
      function c(e) {
        return new RegExp(`/${g(e)}(?=[/?#]|$)`);
      }
      function g(e) {
        return e.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      }
      function m(e) {
        return e.scriptSrc
          ? e.scriptSrc
          : d()
            ? "https://va.vercel-scripts.com/v1/speed-insights/script.debug.js"
            : e.dsn
              ? "https://va.vercel-scripts.com/v1/speed-insights/script.js"
              : e.basePath
                ? `${e.basePath}/speed-insights/script.js`
                : "/_vercel/speed-insights/script.js";
      }
      function w(e = {}) {
        var r;
        if (!l() || e.route === null) return null;
        f();
        const n = m(e);
        if (document.head.querySelector(`script[src*="${n}"]`)) return null;
        e.beforeSend &&
          ((r = window.si) == null ||
            r.call(window, "beforeSend", e.beforeSend));
        const t = document.createElement("script");
        return (
          (t.src = n),
          (t.defer = !0),
          (t.dataset.sdkn = o + (e.framework ? `/${e.framework}` : "")),
          (t.dataset.sdkv = u),
          e.sampleRate && (t.dataset.sampleRate = e.sampleRate.toString()),
          e.route && (t.dataset.route = e.route),
          e.endpoint
            ? (t.dataset.endpoint = e.endpoint)
            : e.basePath &&
              (t.dataset.endpoint = `${e.basePath}/speed-insights/vitals`),
          e.dsn && (t.dataset.dsn = e.dsn),
          d() && e.debug === !1 && (t.dataset.debug = "false"),
          (t.onerror = () => {
            console.log(
              `[Vercel Speed Insights] Failed to load script from ${n}. Please check if any content blockers are enabled and try again.`,
            );
          }),
          document.head.appendChild(t),
          {
            setRoute: (s) => {
              t.dataset.route = s ?? void 0;
            },
          }
        );
      }
      function p() {
        try {
          return;
        } catch {}
      }
      customElements.define(
        "vercel-speed-insights",
        class extends HTMLElement {
          constructor() {
            super();
            try {
              const r = JSON.parse(this.dataset.props ?? "{}"),
                n = JSON.parse(this.dataset.params ?? "{}"),
                t = v(this.dataset.pathname ?? "", n);
              w({
                route: t,
                ...r,
                framework: "astro",
                basePath: p(),
                beforeSend: window.speedInsightsBeforeSend,
              });
            } catch (r) {
              throw new Error(`Failed to parse SpeedInsights properties: ${r}`);
            }
          }
        },
      );
    </script>
    <!-- SPA-style navigation --><meta
      name="astro-view-transitions-enabled"
      content="true"
    /><meta name="astro-view-transitions-fallback" content="animate" />
    <script
      type="module"
      src="/_astro/ClientRouter.astro_astro_type_script_index_0_lang.Byby6A5n.js"
      data-astro-exec=""
    ></script>
    <link rel="stylesheet" href="/_astro/_slug_.G0zg84ml.css" />
    <style>
      .newsletter[data-astro-cid-motrwrji] {
        margin-bottom: 1.5rem;
      }
      .newsletter-actions[data-astro-cid-motrwrji] {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 0.75rem;
      }
      .share-btn[data-astro-cid-motrwrji] {
        font-family:
          Geist Mono,
          monospace;
        cursor: pointer;
        background: none;
      }
      .share-btn[data-astro-cid-motrwrji]:hover {
        background-color: var(--accent);
        color: var(--accent-text);
        border-color: var(--accent-text);
      }
      main[data-astro-cid-bvzihdzo] {
        max-width: 820px !important;
        margin: 0 auto;
        padding: 2.5rem 1.5rem;
      }
      .post-header[data-astro-cid-bvzihdzo] {
        margin-bottom: 1.5rem;
      }
      .post-header[data-astro-cid-bvzihdzo] h1[data-astro-cid-bvzihdzo] {
        margin-top: 0.5rem;
        font-size: 2.5rem;
        font-weight: 400;
        letter-spacing: 0.05em;
        line-height: 1.5;
        text-transform: uppercase;
      }
      .post-meta[data-astro-cid-bvzihdzo] {
        margin-top: 1.25rem;
      }
      .meta-inline[data-astro-cid-bvzihdzo] {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        padding-top: 0.5rem;
        font-family:
          Geist Mono,
          monospace;
        font-size: 12px;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: -0.01em;
      }
      .meta-date[data-astro-cid-bvzihdzo] {
        color: var(--text-light);
      }
      .meta-updated[data-astro-cid-bvzihdzo] {
        color: var(--text-light);
        font-style: italic;
      }
      .meta-tags[data-astro-cid-bvzihdzo] {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
      }
      .content[data-astro-cid-bvzihdzo] {
        overflow-wrap: break-word;
      }
      .content[data-astro-cid-bvzihdzo] pre {
        max-width: 100%;
      }
      .content[data-astro-cid-bvzihdzo] p {
        font-size: 1.0625rem;
        font-weight: 300;
        line-height: 1.65;
        letter-spacing: -0.01em;
      }
      .content[data-astro-cid-bvzihdzo] li {
        font-size: 1.0625rem;
        font-weight: 300;
        line-height: 1.65;
      }
      .related[data-astro-cid-bvzihdzo] {
        margin-top: 3rem;
      }
      .related-item[data-astro-cid-bvzihdzo] {
        display: block;
        padding: 8px 0;
        border-bottom: 1px dotted var(--border-dotted);
        text-decoration: none;
      }
      .related-item[data-astro-cid-bvzihdzo]:hover {
        background: var(--accent);
        color: var(--accent-text);
      }
      .related-title[data-astro-cid-bvzihdzo] {
        display: block;
        color: var(--text);
        font-size: 0.9rem;
        letter-spacing: -0.02em;
        line-height: 1.35;
      }
      .related-item[data-astro-cid-bvzihdzo]:hover
        .related-title[data-astro-cid-bvzihdzo] {
        color: var(--accent-text);
      }
      .post-nav[data-astro-cid-bvzihdzo] {
        margin-top: 3rem;
      }
      .nav-links[data-astro-cid-bvzihdzo] {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
      }
      .nav-link[data-astro-cid-bvzihdzo] {
        flex: 1;
        padding: 0.75rem 0;
        text-decoration: none;
        border-bottom: none;
      }
      .nav-link[data-astro-cid-bvzihdzo]:hover {
        background: transparent;
      }
      .nav-link[data-astro-cid-bvzihdzo]:hover
        .nav-title[data-astro-cid-bvzihdzo] {
        background: var(--accent);
        color: var(--accent-text);
      }
      .nav-label[data-astro-cid-bvzihdzo] {
        display: block;
        font-family:
          Geist Mono,
          monospace;
        font-size: 12px;
        font-weight: 300;
        text-transform: uppercase;
        color: var(--text-light);
        margin-bottom: 4px;
      }
      .nav-title[data-astro-cid-bvzihdzo] {
        display: inline;
        color: var(--text);
        font-size: 0.875rem;
        letter-spacing: -0.02em;
        transition: background-color 0.1s linear;
      }
      .nav-link[data-astro-cid-bvzihdzo].next {
        text-align: right;
      }
      @media (max-width: 640px) {
        main[data-astro-cid-bvzihdzo] {
          padding: 1.5rem 1rem;
        }
        .post-header[data-astro-cid-bvzihdzo] h1[data-astro-cid-bvzihdzo] {
          font-size: 2rem;
        }
        .nav-links[data-astro-cid-bvzihdzo] {
          flex-direction: column;
        }
        .nav-link[data-astro-cid-bvzihdzo].next {
          text-align: left;
        }
      }
    </style>
    <header data-astro-cid-3ef6ksr2="">
      <nav data-astro-cid-3ef6ksr2="">
        <div class="nav-left" data-astro-cid-3ef6ksr2="">
          <a href="/" class="site-title" data-astro-cid-3ef6ksr2=""
            >/dev/michael</a
          >
          <span class="tagline desktop-only" data-astro-cid-3ef6ksr2=""
            >Build, Break, Repeat</span
          >
        </div>
        <div class="nav-right" data-astro-cid-3ef6ksr2="">
          <a href="/about" class="nav-btn" data-astro-cid-3ef6ksr2="">About</a>
          <a href="/subscribe" class="nav-btn" data-astro-cid-3ef6ksr2=""
            >Subscribe</a
          >
          <a href="/rss.xml" class="nav-btn" data-astro-cid-3ef6ksr2="">RSS</a>
          <a
            href="https://github.com/Michaelliv"
            target="_blank"
            class="nav-btn"
            data-astro-cid-3ef6ksr2=""
            >GitHub</a
          >
        </div>
      </nav>
      <div class="tagline-mobile" data-astro-cid-3ef6ksr2="">
        <span class="tagline" data-astro-cid-3ef6ksr2=""
          >Build, Break, Repeat</span
        >
      </div>
      <div class="topics" data-astro-cid-3ef6ksr2="">
        <span class="topics-label" data-astro-cid-3ef6ksr2=""
          >Read more about:</span
        >
        <a href="/tags/agents/" class="tag" data-astro-cid-3ef6ksr2="">agents</a
        ><a href="/tags/infrastructure/" class="tag" data-astro-cid-3ef6ksr2=""
          >infrastructure</a
        ><a href="/tags/claude-code/" class="tag" data-astro-cid-3ef6ksr2=""
          >claude-code</a
        ><a
          href="/tags/context-engineering/"
          class="tag"
          data-astro-cid-3ef6ksr2=""
          >context-engineering</a
        ><a href="/tags/tool-design/" class="tag" data-astro-cid-3ef6ksr2=""
          >tool-design</a
        >
      </div>
    </header>
    <main data-astro-cid-bvzihdzo="">
      <div class="section-label" data-astro-cid-bvzihdzo="">
        <span data-astro-cid-bvzihdzo="">/</span>Article
      </div>
      <article data-astro-cid-bvzihdzo="">
        <header class="post-header" data-astro-cid-bvzihdzo="">
          <h1 data-astro-cid-bvzihdzo="">
            Reverse-engineering Claude's generative UI - then building it for
            the terminal
          </h1>
          <div class="post-meta" data-astro-cid-bvzihdzo="">
            <div class="section-label" data-astro-cid-bvzihdzo="">
              <span data-astro-cid-bvzihdzo="">/</span>Metadata
            </div>
            <div class="meta-inline" data-astro-cid-bvzihdzo="">
              <span class="meta-date" data-astro-cid-bvzihdzo=""
                ><time datetime="2026-03-13T00:00:00.000Z">
                  Mar 13, 2026
                </time></span
              >
              <span class="meta-tags" data-astro-cid-bvzihdzo="">
                <a href="/tags/agents/" class="tag" data-astro-cid-bvzihdzo=""
                  >agents</a
                ><a
                  href="/tags/generative-ui/"
                  class="tag"
                  data-astro-cid-bvzihdzo=""
                  >generative-ui</a
                ><a href="/tags/claude/" class="tag" data-astro-cid-bvzihdzo=""
                  >claude</a
                ><a
                  href="/tags/reverse-engineering/"
                  class="tag"
                  data-astro-cid-bvzihdzo=""
                  >reverse-engineering</a
                ><a href="/tags/pi/" class="tag" data-astro-cid-bvzihdzo=""
                  >pi</a
                ><a
                  href="/tags/extensions/"
                  class="tag"
                  data-astro-cid-bvzihdzo=""
                  >extensions</a
                ><a
                  href="/tags/streaming/"
                  class="tag"
                  data-astro-cid-bvzihdzo=""
                  >streaming</a
                >
              </span>
            </div>
          </div>
        </header>
        <div class="newsletter" data-astro-cid-motrwrji="">
          <div class="section-label" data-astro-cid-motrwrji="">
            <span data-astro-cid-motrwrji="">/</span>Actions
          </div>
          <div class="newsletter-actions" data-astro-cid-motrwrji="">
            <button
              type="button"
              class="share-btn tag"
              aria-label="Share this post"
              data-astro-cid-motrwrji=""
            >
              <span class="share-text" data-astro-cid-motrwrji="">Share</span>
            </button>
            <a href="/subscribe" class="tag" data-astro-cid-motrwrji=""
              >Subscribe</a
            >
          </div>
        </div>
        <div class="content" data-astro-cid-bvzihdzo="">
          <p>
            <img
              src="/images/generative-ui/dashboard.gif"
              alt="SaaS dashboard widget rendered in a native macOS window"
            />
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="bash"
          ><code><span class="line"><span style="color:#B392F0">pi</span><span style="color:#9ECBFF"> install</span><span style="color:#9ECBFF"> npm:pi-generative-ui</span></span></code></pre>
          <p>
            Source:
            <a href="https://github.com/Michaelliv/pi-generative-ui"
              >github.com/Michaelliv/pi-generative-ui</a
            >
          </p>
          <h2 id="the-discovery">The Discovery</h2>
          <p>
            Anthropic
            <a href="https://x.com/claudeai/status/2032124273587077133"
              >announced generative UI for Claude</a
            >
            a couple of hours ago. Interactive widgets - sliders, charts,
            animations - rendered inline in claude.ai conversations. Not images.
            Not code blocks. Living HTML applications with JavaScript running
            inside the chat.
          </p>
          <p>
            This wasn’t a surprise. Generative UI has been pushed by Vercel and
            others for a while, and I knew Anthropic would do something with it.
            This also isn’t the first time I’ve dug into Anthropic’s
            implementation details - I’ve previously
            <a href="/blog/sandboxed-execution-environment"
              >reverse-engineered their sandbox architecture</a
            >
            and written about their
            <a href="/blog/sandbox-comparison-2026">sandbox</a>.
          </p>
          <p>
            So I went to claude.ai with a specific purpose: understand exactly
            how they implemented it. I ended up building my own version for
            <a href="https://github.com/badlogic/pi-mono">pi</a>, the
            terminal-based coding agent.
          </p>
          <hr />
          <h2 id="part-1-interrogating-claude-about-its-own-ui">
            Part 1: Interrogating Claude About Its Own UI
          </h2>
          <h3 id="the-tool-not-the-markdown">The Tool, Not the Markdown</h3>
          <p>
            My first assumption was wrong. I thought Claude was outputting HTML
            as part of its markdown response and the frontend was rendering it
            inline. Claude corrected me:
          </p>
          <blockquote>
            <p>
              “Ha, yes! Caught me - it’s not ‘part of the markdown output’ at
              all. I call a tool called <code>show_widget</code> and pass the
              HTML as a parameter.”
            </p>
          </blockquote>
          <p>
            So it’s a <strong>tool call</strong>. The same mechanism as web
            search or file operations. The HTML is a parameter payload, not
            streamed text. Here’s the shape Claude described:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="json"
          ><code><span class="line"><span style="color:#E1E4E8">{</span></span>
<span class="line"><span style="color:#79B8FF">  "i_have_seen_read_me"</span><span style="color:#E1E4E8">: </span><span style="color:#79B8FF">true</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">  "title"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"snake_case_identifier"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">  "loading_messages"</span><span style="color:#E1E4E8">: [</span><span style="color:#9ECBFF">"First loading message"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"Second loading message"</span><span style="color:#E1E4E8">],</span></span>
<span class="line"><span style="color:#79B8FF">  "widget_code"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"...styles...</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">...html content...</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">..."</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>Four parameters:</p>
          <ul>
            <li>
              <strong><code>i_have_seen_read_me</code></strong> - A boolean
              forcing function. Claude must call a <code>read_me</code> tool
              first to load design guidelines before it can use
              <code>show_widget</code>. It’s a compile-time check for
              documentation compliance.
            </li>
            <li>
              <strong><code>title</code></strong> - A snake_case identifier for
              the widget.
            </li>
            <li>
              <strong><code>loading_messages</code></strong> - 1-4 short strings
              shown while the widget renders (the “Spinning up particles…”
              messages you see before content appears).
            </li>
            <li>
              <strong><code>widget_code</code></strong> - Raw HTML fragment. No
              <code>&lt;!DOCTYPE&gt;</code>, no <code>&lt;html&gt;</code>, no
              <code>&lt;head&gt;</code>, no <code>&lt;body&gt;</code>. Just
              content.
            </li>
          </ul>
          <h3 id="the-read_me-pattern---progressive-disclosure">
            The <code>read_me</code> Pattern - Progressive Disclosure
          </h3>
          <p>
            Before Claude can call <code>show_widget</code>, it must call
            <code>read_me</code> with a <code>modules</code> parameter:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="json"
          ><code><span class="line"><span style="color:#E1E4E8">{</span></span>
<span class="line"><span style="color:#79B8FF">  "modules"</span><span style="color:#E1E4E8">: [</span><span style="color:#9ECBFF">"interactive"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"chart"</span><span style="color:#E1E4E8">]</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>
            Available modules: <code>diagram</code>, <code>mockup</code>,
            <code>interactive</code>, <code>chart</code>, <code>art</code>.
          </p>
          <p>
            Each module returns different design guidelines - the
            <code>chart</code> module gives Chart.js patterns,
            <code>art</code> gives illustration rules, <code>mockup</code> gives
            UI component tokens. Claude described it perfectly:
          </p>
          <blockquote>
            <p>
              “It’s a lazy documentation system - instead of dumping the entire
              design system into my context upfront (which would be expensive
              tokens on every message), it loads only the relevant subset on
              demand.”
            </p>
          </blockquote>
          <p>
            This is
            <strong
              >progressive disclosure applied to the model’s own
              instructions</strong
            >. The base system prompt stays lean; specialized knowledge loads
            on-demand when the task requires it.
          </p>
          <h3 id="not-an-iframe---live-dom-injection">
            Not an Iframe - Live DOM Injection
          </h3>
          <p>
            I noticed the widget rendered <strong>live</strong> as Claude
            streamed its response. The sliders and cards appeared before Claude
            finished generating the <code>widget_code</code> parameter. That’s
            not how iframes work - an iframe would need the complete HTML before
            rendering.
          </p>
          <p>
            Claude initially claimed it was a sandboxed iframe, but I pushed
            back:
          </p>
          <blockquote>
            <p>
              “It renders live on my screen, meaning that it somehow handles
              partial rendering of the HTML. It’s not a sandbox.”
            </p>
          </blockquote>
          <p>Claude’s revised analysis:</p>
          <blockquote>
            <p>
              “The streaming behavior gives it away completely. If it were a
              sandboxed iframe, it would have to wait for the complete HTML
              before rendering. But you’re seeing it render as tokens stream in.
              That’s only possible if it’s
              <strong>direct DOM injection into the parent page</strong>.”
            </p>
          </blockquote>
          <p>The evidence:</p>
          <ul>
            <li>
              <strong>CSS variables work</strong> -
              <code>var(--color-text-primary)</code> resolves correctly because
              it’s the same document, same cascade
            </li>
            <li>
              <strong><code>sendPrompt()</code> works</strong> - a function on
              the parent page, accessible to injected code
            </li>
            <li>
              <strong>Background is transparent</strong> - no iframe container,
              just nodes in the DOM
            </li>
            <li>
              <strong>No loading flash</strong> - no iframe border, no
              scrollbar, no white-background box
            </li>
          </ul>
          <p>
            The “sandbox” is almost certainly just a
            <strong>Content Security Policy</strong> on the parent page
            restricting which CDN domains <code>script src</code> tags can load
            from:
          </p>
          <ul>
            <li><code>cdnjs.cloudflare.com</code></li>
            <li><code>cdn.jsdelivr.net</code></li>
            <li><code>unpkg.com</code></li>
            <li><code>esm.sh</code></li>
          </ul>
          <h3 id="how-it-differs-from-artifacts">
            How It Differs from Artifacts
          </h3>
          <p>This was a key insight from the conversation:</p>

          <table>
            <thead>
              <tr>
                <th></th>
                <th>Artifacts</th>
                <th>Visualizer (<code>show_widget</code>)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Purpose</strong></td>
                <td>Deliverables - files you keep, download, share</td>
                <td>Inline enhancements - part of the conversation flow</td>
              </tr>
              <tr>
                <td><strong>Display</strong></td>
                <td>Side panel with download button</td>
                <td>Inline in the chat, transparent background</td>
              </tr>
              <tr>
                <td><strong>Libraries</strong></td>
                <td>Closed set of pre-bundled libraries</td>
                <td>Any library from CDN allowlist, downloaded live</td>
              </tr>
              <tr>
                <td><strong>Persistence</strong></td>
                <td>Survives across sessions</td>
                <td>Ephemeral, tied to the message</td>
              </tr>
              <tr>
                <td><strong>Trigger</strong></td>
                <td>”Build me a calculator” (deliverable language)</td>
                <td>
                  “Show me how compound interest works” (explanatory language)
                </td>
              </tr>
            </tbody>
          </table>
          <p>
            The CDN point is crucial. Artifacts have a fixed set of available
            libraries. The visualizer downloads Chart.js, D3, Three.js -
            whatever it needs - live from CDNs. This is why the CSP allowlist
            exists: it’s the security boundary for arbitrary CDN fetches.
          </p>
          <h3 id="the-streaming-architecture">The Streaming Architecture</h3>
          <p>
            Putting it all together, here’s how claude.ai renders generative UI:
          </p>
          <ol>
            <li>
              LLM starts generating the <code>show_widget</code> tool call
            </li>
            <li>
              The <code>widget_code</code> parameter streams token by token as
              JSON string chunks
            </li>
            <li>
              The client does incremental HTML parsing on the partial content
            </li>
            <li>
              DOM nodes are inserted into the page in real-time via
              <code>innerHTML</code> or similar
            </li>
            <li>CSS variables resolve immediately (same document)</li>
            <li>
              <code>style</code> blocks and HTML structure render as they arrive
            </li>
            <li>
              <code>script</code> tags execute once streaming completes (which
              is why scripts go last)
            </li>
            <li>
              CDN libraries load asynchronously; charts/interactivity activate
              after scripts run
            </li>
          </ol>
          <p>
            This explains the design guideline that says “Structure code so
            useful content appears early: <code>style</code> (short) → content
            HTML → <code>script</code> last.” The content renders progressively;
            the scripts activate it at the end.
          </p>
          <hr />
          <h2 id="part-2-building-it-for-pi">Part 2: Building It for Pi</h2>
          <h3 id="the-problem">The Problem</h3>
          <p>
            <a href="https://github.com/badlogic/pi-mono">Pi</a> is a
            terminal-based coding agent (I’ve
            <a href="/blog/cli-coding-agents-compared"
              >compared every CLI coding agent</a
            >
            if you’re curious). Terminals render text and (in modern ones)
            inline images. There is
            <strong
              >no way to render interactive HTML with JavaScript inside a
              terminal</strong
            >. The moment you need a <code>&lt;canvas&gt;</code>, an
            <code>&lt;input type="range"&gt;</code>, or Chart.js, you need a
            browser engine.
          </p>
          <p>My initial options were:</p>
          <ol>
            <li>
              <strong>Terminal image protocols</strong> (Sixel, Kitty graphics)
              - render HTML to a screenshot, display inline. No interactivity.
            </li>
            <li>
              <strong>Local web server + browser</strong> - serve HTML on
              localhost, auto-open browser tab. Full interactivity but exits the
              terminal.
            </li>
            <li>
              <strong>TUI approximation</strong> - parse HTML, render a
              simplified text version. Extremely limited.
            </li>
          </ol>
          <p>None of these matched the claude.ai experience.</p>
          <h3 id="enter-glimpse">Enter Glimpse</h3>
          <p>
            Then I found
            <a href="https://github.com/hazat/glimpse">Glimpse</a> - a native
            macOS micro-UI library. It opens a WKWebView window in under 50ms
            via a tiny Swift binary with a Node.js wrapper. No Electron, no
            browser, no runtime dependencies.
          </p>
          <p>Key capabilities:</p>
          <ul>
            <li>
              <strong>Native WKWebView</strong> - full browser engine (CSS, JS,
              Canvas, CDN libraries)
            </li>
            <li><strong>Sub-50ms startup</strong> - feels instant</li>
            <li>
              <strong>Bidirectional JSON</strong> -
              <code>window.glimpse.send(data)</code> sends data from the page
              back to Node.js
            </li>
            <li>
              <strong>Window modes</strong> - floating, frameless, transparent,
              click-through, follow-cursor
            </li>
            <li>
              <strong><code>setHTML()</code></strong> - replace page content at
              runtime
            </li>
            <li>
              <strong><code>send(js)</code></strong> - evaluate JavaScript in
              the WebView
            </li>
          </ul>
          <p>
            This was the missing piece. A real browser engine, spawnable from a
            pi extension, with bidirectional communication.
          </p>
          <h3 id="the-extension-architecture">The Extension Architecture</h3>
          <p>
            Pi extensions are TypeScript modules that can register custom tools,
            subscribe to lifecycle events, and render custom TUI components. The
            architecture:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="plaintext"
          ><code><span class="line"><span>LLM generates show_widget tool call</span></span>
<span class="line"><span>            │</span></span>
<span class="line"><span>            ▼</span></span>
<span class="line"><span>   ┌───────────────────┐</span></span>
<span class="line"><span>   │ message_update    │──── streaming: intercept partial tool call JSON</span></span>
<span class="line"><span>   │    event          │     extract widget_code, open Glimpse window early</span></span>
<span class="line"><span>   └────────┬──────────┘     feed partial HTML as tokens arrive</span></span>
<span class="line"><span>            │</span></span>
<span class="line"><span>            ▼</span></span>
<span class="line"><span>   ┌───────────────────┐</span></span>
<span class="line"><span>   │  tool_call        │──── complete: final widget_code available</span></span>
<span class="line"><span>   │    event          │</span></span>
<span class="line"><span>   └────────┬──────────┘</span></span>
<span class="line"><span>            │</span></span>
<span class="line"><span>            ▼</span></span>
<span class="line"><span>   ┌───────────────────┐</span></span>
<span class="line"><span>   │   execute()       │──── reuse streaming window or open fresh</span></span>
<span class="line"><span>   │                   │     wait for user interaction or window close</span></span>
<span class="line"><span>   └────────┬──────────┘     return interaction data as tool result</span></span>
<span class="line"><span>            │</span></span>
<span class="line"><span>            ▼</span></span>
<span class="line"><span>   ┌───────────────────┐</span></span>
<span class="line"><span>   │  renderCall       │──── TUI: "show_widget compound interest 800×600"</span></span>
<span class="line"><span>   │  renderResult     │──── TUI: "✓ compound interest 800×600"</span></span>
<span class="line"><span>   └───────────────────┘</span></span></code></pre>
          <h3 id="two-tools-mirroring-claudes-pattern">
            Two Tools, Mirroring Claude’s Pattern
          </h3>
          <p>
            <strong><code>visualize_read_me</code></strong> - Lazy documentation
            loader. Returns design guidelines by module (interactive, chart,
            mockup, art, diagram). The LLM calls this silently before its first
            widget, loading only the relevant guidelines into context.
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#E1E4E8">pi.</span><span style="color:#B392F0">registerTool</span><span style="color:#E1E4E8">({</span></span>
<span class="line"><span style="color:#E1E4E8">  name: </span><span style="color:#9ECBFF">"visualize_read_me"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  label: </span><span style="color:#9ECBFF">"Read Guidelines"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  description: </span><span style="color:#9ECBFF">"Returns design guidelines for show_widget..."</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  promptGuidelines: [</span></span>
<span class="line"><span style="color:#9ECBFF">    "Call visualize_read_me once before your first show_widget call."</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#9ECBFF">    "Do NOT mention the read_me call to the user."</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  ],</span></span>
<span class="line"><span style="color:#E1E4E8">  parameters: Type.</span><span style="color:#B392F0">Object</span><span style="color:#E1E4E8">({</span></span>
<span class="line"><span style="color:#E1E4E8">    modules: Type.</span><span style="color:#B392F0">Array</span><span style="color:#E1E4E8">(</span><span style="color:#B392F0">StringEnum</span><span style="color:#E1E4E8">(</span><span style="color:#79B8FF">AVAILABLE_MODULES</span><span style="color:#E1E4E8">)),</span></span>
<span class="line"><span style="color:#E1E4E8">  }),</span></span>
<span class="line"><span style="color:#F97583">  async</span><span style="color:#B392F0"> execute</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">_toolCallId</span><span style="color:#E1E4E8">, </span><span style="color:#FFAB70">params</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">    return</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#E1E4E8">      content: [{ type: </span><span style="color:#9ECBFF">"text"</span><span style="color:#E1E4E8">, text: </span><span style="color:#B392F0">getGuidelines</span><span style="color:#E1E4E8">(params.modules) }],</span></span>
<span class="line"><span style="color:#E1E4E8">      details: { modules: params.modules },</span></span>
<span class="line"><span style="color:#E1E4E8">    };</span></span>
<span class="line"><span style="color:#E1E4E8">  },</span></span>
<span class="line"><span style="color:#E1E4E8">});</span></span></code></pre>
          <p>
            <strong><code>show_widget</code></strong> - Takes HTML/SVG code,
            opens a native macOS window via Glimpse, returns user interaction
            data.
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#E1E4E8">pi.</span><span style="color:#B392F0">registerTool</span><span style="color:#E1E4E8">({</span></span>
<span class="line"><span style="color:#E1E4E8">  name: </span><span style="color:#9ECBFF">"show_widget"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  label: </span><span style="color:#9ECBFF">"Show Widget"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  description: </span><span style="color:#9ECBFF">"Show visual content in a native macOS window..."</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">  parameters: Type.</span><span style="color:#B392F0">Object</span><span style="color:#E1E4E8">({</span></span>
<span class="line"><span style="color:#E1E4E8">    i_have_seen_read_me: Type.</span><span style="color:#B392F0">Boolean</span><span style="color:#E1E4E8">(),</span></span>
<span class="line"><span style="color:#E1E4E8">    title: Type.</span><span style="color:#B392F0">String</span><span style="color:#E1E4E8">(),</span></span>
<span class="line"><span style="color:#E1E4E8">    widget_code: Type.</span><span style="color:#B392F0">String</span><span style="color:#E1E4E8">(),</span></span>
<span class="line"><span style="color:#E1E4E8">    width: Type.</span><span style="color:#B392F0">Optional</span><span style="color:#E1E4E8">(Type.</span><span style="color:#B392F0">Number</span><span style="color:#E1E4E8">()),</span></span>
<span class="line"><span style="color:#E1E4E8">    height: Type.</span><span style="color:#B392F0">Optional</span><span style="color:#E1E4E8">(Type.</span><span style="color:#B392F0">Number</span><span style="color:#E1E4E8">()),</span></span>
<span class="line"><span style="color:#E1E4E8">    floating: Type.</span><span style="color:#B392F0">Optional</span><span style="color:#E1E4E8">(Type.</span><span style="color:#B392F0">Boolean</span><span style="color:#E1E4E8">()),</span></span>
<span class="line"><span style="color:#E1E4E8">  }),</span></span>
<span class="line"><span style="color:#F97583">  async</span><span style="color:#B392F0"> execute</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">_toolCallId</span><span style="color:#E1E4E8">, </span><span style="color:#FFAB70">params</span><span style="color:#E1E4E8">, </span><span style="color:#FFAB70">signal</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">    const</span><span style="color:#E1E4E8"> { </span><span style="color:#79B8FF">open</span><span style="color:#E1E4E8"> } </span><span style="color:#F97583">=</span><span style="color:#F97583"> await</span><span style="color:#B392F0"> import</span><span style="color:#E1E4E8">(</span><span style="color:#79B8FF">GLIMPSE_PATH</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#F97583">    const</span><span style="color:#79B8FF"> win</span><span style="color:#F97583"> =</span><span style="color:#B392F0"> open</span><span style="color:#E1E4E8">(</span><span style="color:#B392F0">wrapHTML</span><span style="color:#E1E4E8">(params.widget_code), {</span></span>
<span class="line"><span style="color:#E1E4E8">      width: params.width </span><span style="color:#F97583">??</span><span style="color:#79B8FF"> 800</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">      height: params.height </span><span style="color:#F97583">??</span><span style="color:#79B8FF"> 600</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#E1E4E8">      title: params.title.</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#DBEDFF">_</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">" "</span><span style="color:#E1E4E8">),</span></span>
<span class="line"><span style="color:#E1E4E8">    });</span></span>
<span class="line"></span>
<span class="line"><span style="color:#F97583">    return</span><span style="color:#F97583"> new</span><span style="color:#79B8FF"> Promise</span><span style="color:#E1E4E8">((</span><span style="color:#FFAB70">resolve</span><span style="color:#E1E4E8">) </span><span style="color:#F97583">=&gt;</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#E1E4E8">      win.</span><span style="color:#B392F0">on</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"message"</span><span style="color:#E1E4E8">, (</span><span style="color:#FFAB70">data</span><span style="color:#E1E4E8">) </span><span style="color:#F97583">=&gt;</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#B392F0">        resolve</span><span style="color:#E1E4E8">({ content: [{ type: </span><span style="color:#9ECBFF">"text"</span><span style="color:#E1E4E8">, text: </span><span style="color:#9ECBFF">`User data: ${</span><span style="color:#79B8FF">JSON</span><span style="color:#9ECBFF">.</span><span style="color:#B392F0">stringify</span><span style="color:#9ECBFF">(</span><span style="color:#E1E4E8">data</span><span style="color:#9ECBFF">)</span><span style="color:#9ECBFF">}`</span><span style="color:#E1E4E8"> }] });</span></span>
<span class="line"><span style="color:#E1E4E8">      });</span></span>
<span class="line"><span style="color:#E1E4E8">      win.</span><span style="color:#B392F0">on</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"closed"</span><span style="color:#E1E4E8">, () </span><span style="color:#F97583">=&gt;</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#B392F0">        resolve</span><span style="color:#E1E4E8">({ content: [{ type: </span><span style="color:#9ECBFF">"text"</span><span style="color:#E1E4E8">, text: </span><span style="color:#9ECBFF">"Window closed."</span><span style="color:#E1E4E8"> }] });</span></span>
<span class="line"><span style="color:#E1E4E8">      });</span></span>
<span class="line"><span style="color:#E1E4E8">    });</span></span>
<span class="line"><span style="color:#E1E4E8">  },</span></span>
<span class="line"><span style="color:#E1E4E8">});</span></span></code></pre>
          <h3 id="custom-tui-rendering">Custom TUI Rendering</h3>
          <p>
            Pi extensions can provide <code>renderCall</code> and
            <code>renderResult</code> functions for custom terminal display.
            Instead of dumping raw HTML into the terminal, we show compact
            summaries:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#B392F0">renderCall</span><span style="color:#E1E4E8">(args, theme) {</span></span>
<span class="line"><span style="color:#F97583">  const</span><span style="color:#79B8FF"> title</span><span style="color:#F97583"> =</span><span style="color:#E1E4E8"> args.title.</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#DBEDFF">_</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">" "</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#F97583"> new</span><span style="color:#B392F0"> Text</span><span style="color:#E1E4E8">(</span></span>
<span class="line"><span style="color:#E1E4E8">    theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"toolTitle"</span><span style="color:#E1E4E8">, theme.</span><span style="color:#B392F0">bold</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"show_widget "</span><span style="color:#E1E4E8">)) </span><span style="color:#F97583">+</span></span>
<span class="line"><span style="color:#E1E4E8">    theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"accent"</span><span style="color:#E1E4E8">, title) </span><span style="color:#F97583">+</span></span>
<span class="line"><span style="color:#E1E4E8">    theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"dim"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">` ${</span><span style="color:#E1E4E8">args</span><span style="color:#9ECBFF">.</span><span style="color:#E1E4E8">width</span><span style="color:#9ECBFF">}×${</span><span style="color:#E1E4E8">args</span><span style="color:#9ECBFF">.</span><span style="color:#E1E4E8">height</span><span style="color:#9ECBFF">}`</span><span style="color:#E1E4E8">),</span></span>
<span class="line"><span style="color:#79B8FF">    0</span><span style="color:#E1E4E8">, </span><span style="color:#79B8FF">0</span></span>
<span class="line"><span style="color:#E1E4E8">  );</span></span>
<span class="line"><span style="color:#E1E4E8">},</span></span>
<span class="line"></span>
<span class="line"><span style="color:#B392F0">renderResult</span><span style="color:#E1E4E8">(result, { isPartial, expanded }, theme) {</span></span>
<span class="line"><span style="color:#F97583">  if</span><span style="color:#E1E4E8"> (isPartial) </span><span style="color:#F97583">return</span><span style="color:#F97583"> new</span><span style="color:#B392F0"> Text</span><span style="color:#E1E4E8">(theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"warning"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"⟳ Widget rendering..."</span><span style="color:#E1E4E8">), </span><span style="color:#79B8FF">0</span><span style="color:#E1E4E8">, </span><span style="color:#79B8FF">0</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#F97583">  const</span><span style="color:#79B8FF"> details</span><span style="color:#F97583"> =</span><span style="color:#E1E4E8"> result.details;</span></span>
<span class="line"><span style="color:#F97583">  let</span><span style="color:#E1E4E8"> text </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"success"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"✓ "</span><span style="color:#E1E4E8">) </span><span style="color:#F97583">+</span><span style="color:#E1E4E8"> theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"accent"</span><span style="color:#E1E4E8">, details.title);</span></span>
<span class="line"><span style="color:#F97583">  if</span><span style="color:#E1E4E8"> (expanded </span><span style="color:#F97583">&amp;&amp;</span><span style="color:#E1E4E8"> details.messageData) {</span></span>
<span class="line"><span style="color:#E1E4E8">    text </span><span style="color:#F97583">+=</span><span style="color:#9ECBFF"> "</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">"</span><span style="color:#F97583"> +</span><span style="color:#E1E4E8"> theme.</span><span style="color:#B392F0">fg</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"dim"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">`  Data: ${</span><span style="color:#79B8FF">JSON</span><span style="color:#9ECBFF">.</span><span style="color:#B392F0">stringify</span><span style="color:#9ECBFF">(</span><span style="color:#E1E4E8">details</span><span style="color:#9ECBFF">.</span><span style="color:#E1E4E8">messageData</span><span style="color:#9ECBFF">)</span><span style="color:#9ECBFF">}`</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#E1E4E8">  }</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#F97583"> new</span><span style="color:#B392F0"> Text</span><span style="color:#E1E4E8">(text, </span><span style="color:#79B8FF">0</span><span style="color:#E1E4E8">, </span><span style="color:#79B8FF">0</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#E1E4E8">},</span></span></code></pre>
          <p>
            <img
              src="/images/generative-ui/simulator.gif"
              alt="Projectile motion simulator with planet selection"
            />
          </p>
          <hr />
          <h2 id="part-3-the-streaming-challenge">
            Part 3: The Streaming Challenge
          </h2>
          <h3 id="the-goal">The Goal</h3>
          <p>
            On claude.ai, the widget renders progressively as tokens stream in.
            The HTML builds up visually - you see the styles apply, the
            structure form, cards and tables appear piece by piece, and then the
            chart pops in when the <code>script</code> executes at the end.
          </p>
          <p>
            We wanted the same experience: the Glimpse window should open early
            and show content building up live.
          </p>
          <h3 id="how-pi-streams-tool-calls">How Pi Streams Tool Calls</h3>
          <p>
            Pi’s AI layer (pi-ai) normalizes streaming events across all
            providers (Anthropic, OpenAI, Google, etc.) into a unified format:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#F97583">type</span><span style="color:#B392F0"> AssistantMessageEvent</span><span style="color:#F97583"> =</span></span>
<span class="line"><span style="color:#F97583">  |</span><span style="color:#E1E4E8"> { </span><span style="color:#FFAB70">type</span><span style="color:#F97583">:</span><span style="color:#9ECBFF"> "toolcall_start"</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">contentIndex</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> number</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">partial</span><span style="color:#F97583">:</span><span style="color:#B392F0"> AssistantMessage</span><span style="color:#E1E4E8"> }</span></span>
<span class="line"><span style="color:#F97583">  |</span><span style="color:#E1E4E8"> { </span><span style="color:#FFAB70">type</span><span style="color:#F97583">:</span><span style="color:#9ECBFF"> "toolcall_delta"</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">contentIndex</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> number</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">delta</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> string</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">partial</span><span style="color:#F97583">:</span><span style="color:#B392F0"> AssistantMessage</span><span style="color:#E1E4E8"> }</span></span>
<span class="line"><span style="color:#F97583">  |</span><span style="color:#E1E4E8"> { </span><span style="color:#FFAB70">type</span><span style="color:#F97583">:</span><span style="color:#9ECBFF"> "toolcall_end"</span><span style="color:#E1E4E8">;   </span><span style="color:#FFAB70">contentIndex</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> number</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">toolCall</span><span style="color:#F97583">:</span><span style="color:#B392F0"> ToolCall</span><span style="color:#E1E4E8">; </span><span style="color:#FFAB70">partial</span><span style="color:#F97583">:</span><span style="color:#B392F0"> AssistantMessage</span><span style="color:#E1E4E8"> }</span></span></code></pre>
          <p>
            The key discovery:
            <strong>pi-ai already parses partial JSON on every delta</strong>.
            Looking at the Anthropic provider source:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="javascript"
          ><code><span class="line"><span style="color:#E1E4E8">block.partialJson </span><span style="color:#F97583">+=</span><span style="color:#E1E4E8"> event.delta.partial_json;</span></span>
<span class="line"><span style="color:#E1E4E8">block.arguments </span><span style="color:#F97583">=</span><span style="color:#B392F0"> parseStreamingJson</span><span style="color:#E1E4E8">(block.partialJson);</span></span></code></pre>
          <p>
            So <code>partial.content[index].arguments</code> is a
            progressively-parsed object. On every <code>toolcall_delta</code>,
            we can read <code>arguments.widget_code</code> and get the HTML
            accumulated so far - no need for a partial JSON parser library.
          </p>
          <p>
            We initially installed <code>partial-json</code> from npm before
            discovering this. Removed it immediately.
          </p>
          <h3 id="attempt-1-sethtml-on-every-delta">
            Attempt 1: <code>setHTML()</code> on Every Delta
          </h3>
          <p>
            The first approach: listen to <code>message_update</code>, detect
            <code>show_widget</code> tool calls streaming, open a Glimpse
            window, and call <code>win.setHTML(wrappedHTML)</code> on every
            delta.
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#E1E4E8">pi.</span><span style="color:#B392F0">on</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">"message_update"</span><span style="color:#E1E4E8">, </span><span style="color:#F97583">async</span><span style="color:#E1E4E8"> (</span><span style="color:#FFAB70">event</span><span style="color:#E1E4E8">) </span><span style="color:#F97583">=&gt;</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#F97583">  const</span><span style="color:#79B8FF"> raw</span><span style="color:#F97583"> =</span><span style="color:#E1E4E8"> event.assistantMessageEvent;</span></span>
<span class="line"><span style="color:#F97583">  if</span><span style="color:#E1E4E8"> (raw.type </span><span style="color:#F97583">===</span><span style="color:#9ECBFF"> "toolcall_delta"</span><span style="color:#F97583"> &amp;&amp;</span><span style="color:#E1E4E8"> streaming) {</span></span>
<span class="line"><span style="color:#F97583">    const</span><span style="color:#79B8FF"> block</span><span style="color:#F97583"> =</span><span style="color:#E1E4E8"> raw.partial.content[raw.contentIndex];</span></span>
<span class="line"><span style="color:#F97583">    const</span><span style="color:#79B8FF"> html</span><span style="color:#F97583"> =</span><span style="color:#E1E4E8"> block.arguments?.widget_code;</span></span>
<span class="line"><span style="color:#F97583">    if</span><span style="color:#E1E4E8"> (html </span><span style="color:#F97583">&amp;&amp;</span><span style="color:#E1E4E8"> html.</span><span style="color:#79B8FF">length</span><span style="color:#F97583"> &gt;</span><span style="color:#79B8FF"> 20</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#E1E4E8">      streaming.window.</span><span style="color:#B392F0">setHTML</span><span style="color:#E1E4E8">(</span><span style="color:#B392F0">wrapHTML</span><span style="color:#E1E4E8">(html));</span></span>
<span class="line"><span style="color:#E1E4E8">    }</span></span>
<span class="line"><span style="color:#E1E4E8">  }</span></span>
<span class="line"><span style="color:#E1E4E8">});</span></span></code></pre>
          <p>
            <strong>Result</strong>: It worked! The window opened and showed
            content building up. But it was <strong>choppy as hell</strong>.
            Every <code>setHTML()</code> call replaced the entire document -
            full page reflow, loss of scroll position, flash of unstyled
            content. Every 80ms, the entire page blinked.
          </p>
          <h3 id="attempt-2-shell-page--innerhtml-via-js-eval">
            Attempt 2: Shell Page + <code>innerHTML</code> via JS Eval
          </h3>
          <p>
            Instead of replacing the entire document, we opened the window once
            with a shell HTML page containing an empty
            <code>&lt;div id="root"&gt;</code>. Then we used
            <code>win.send()</code> (JavaScript evaluation in the WebView) to
            update just the innerHTML of that container:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#6A737D">// Shell HTML loaded once - contains a &lt;div id="root"&gt; and a script</span></span>
<span class="line"><span style="color:#6A737D">// that defines window._setContent(html) to update root's innerHTML</span></span>
<span class="line"><span style="color:#F97583">function</span><span style="color:#B392F0"> shellHTML</span><span style="color:#E1E4E8">() {</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#9ECBFF"> `...</span></span>
<span class="line"><span style="color:#9ECBFF">    &lt;div id="root"&gt;&lt;/div&gt;</span></span>
<span class="line"><span style="color:#9ECBFF">    // _setContent: sets root.innerHTML to the provided html</span></span>
<span class="line"><span style="color:#9ECBFF">  ...`</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span>
<span class="line"></span>
<span class="line"><span style="color:#6A737D">// On each delta, eval JS to update content</span></span>
<span class="line"><span style="color:#E1E4E8">streaming.window.</span><span style="color:#B392F0">send</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">`window._setContent('${</span><span style="color:#B392F0">escapeJS</span><span style="color:#9ECBFF">(</span><span style="color:#E1E4E8">html</span><span style="color:#9ECBFF">)</span><span style="color:#9ECBFF">}')`</span><span style="color:#E1E4E8">);</span></span></code></pre>
          <p>
            <strong>Result</strong>: Better - no full document replacement. But
            still choppy. <code>innerHTML</code> replaces all child nodes, so
            existing content gets destroyed and recreated on every update.
            There’s no visual continuity.
          </p>
          <h3 id="attempt-3-naive-dom-appending">
            Attempt 3: Naive DOM Appending
          </h3>
          <p>
            We tried tracking the previous content length and only appending new
            child nodes:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#E1E4E8">window.</span><span style="color:#B392F0">_setContent</span><span style="color:#F97583"> =</span><span style="color:#F97583"> function</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">html</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">  var</span><span style="color:#E1E4E8"> root </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> document.</span><span style="color:#B392F0">getElementById</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">'root'</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#F97583">  var</span><span style="color:#E1E4E8"> tmp </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> document.</span><span style="color:#B392F0">createElement</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">'div'</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#E1E4E8">  tmp.innerHTML </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> html;</span></span>
<span class="line"><span style="color:#6A737D">  // Only append nodes beyond what we already have</span></span>
<span class="line"><span style="color:#F97583">  for</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">var</span><span style="color:#E1E4E8"> i </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> root.childNodes.</span><span style="color:#79B8FF">length</span><span style="color:#E1E4E8">; i </span><span style="color:#F97583">&lt;</span><span style="color:#E1E4E8"> tmp.childNodes.</span><span style="color:#79B8FF">length</span><span style="color:#E1E4E8">; i</span><span style="color:#F97583">++</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">    var</span><span style="color:#E1E4E8"> node </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> tmp.childNodes[i].</span><span style="color:#B392F0">cloneNode</span><span style="color:#E1E4E8">(</span><span style="color:#79B8FF">true</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#E1E4E8">    node.style.animation </span><span style="color:#F97583">=</span><span style="color:#9ECBFF"> '_fadeIn 0.3s ease both'</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#E1E4E8">    root.</span><span style="color:#B392F0">appendChild</span><span style="color:#E1E4E8">(node);</span></span>
<span class="line"><span style="color:#E1E4E8">  }</span></span>
<span class="line"><span style="color:#6A737D">  // Update the last existing node (it was probably incomplete)</span></span>
<span class="line"><span style="color:#6A737D">  // ...</span></span>
<span class="line"><span style="color:#E1E4E8">};</span></span></code></pre>
          <p>
            <strong>Result</strong>: Elements appeared but
            <strong>never faded in</strong>. The problem: the browser
            auto-closes unclosed HTML tags when parsing partial content.
            <code>&lt;div class="cards"&gt;&lt;div class="c"&gt;</code> becomes:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="html"
          ><code><span class="line"><span style="color:#E1E4E8">&lt;</span><span style="color:#85E89D">div</span><span style="color:#B392F0"> class</span><span style="color:#E1E4E8">=</span><span style="color:#9ECBFF">"cards"</span><span style="color:#E1E4E8">&gt;</span></span>
<span class="line"><span style="color:#E1E4E8">  &lt;</span><span style="color:#85E89D">div</span><span style="color:#B392F0"> class</span><span style="color:#E1E4E8">=</span><span style="color:#9ECBFF">"c"</span><span style="color:#E1E4E8">&gt;&lt;/</span><span style="color:#85E89D">div</span><span style="color:#E1E4E8">&gt;  </span><span style="color:#6A737D">&lt;!-- browser auto-closed this --&gt;</span></span>
<span class="line"><span style="color:#E1E4E8">&lt;/</span><span style="color:#85E89D">div</span><span style="color:#E1E4E8">&gt;</span></span></code></pre>
          <p>
            On the next update with more content, the tree structure changes
            fundamentally - it’s not “new nodes appended at the end,” it’s a
            completely different tree. The append logic couldn’t track what was
            actually new.
          </p>
          <h3 id="attempt-4-morphdom---dom-diffing-the-solution">
            Attempt 4: morphdom - DOM Diffing (The Solution)
          </h3>
          <p>
            We introduced
            <a href="https://github.com/patrick-steele-idem/morphdom"
              >morphdom</a
            >, a fast DOM diffing library (used by frameworks like Marko).
            Instead of replacing innerHTML, morphdom compares the old and new
            DOM trees and applies <strong>minimal patches</strong> - updating
            changed nodes, adding new ones, leaving unchanged ones alone.
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#F97583">function</span><span style="color:#B392F0"> shellHTML</span><span style="color:#E1E4E8">() {</span></span>
<span class="line"><span style="color:#6A737D">  // Returns a full HTML document with:</span></span>
<span class="line"><span style="color:#6A737D">  // 1. A _fadeIn CSS animation (opacity 0→1, translateY 4px→0)</span></span>
<span class="line"><span style="color:#6A737D">  // 2. morphdom loaded from cdn.jsdelivr.net</span></span>
<span class="line"><span style="color:#6A737D">  // 3. A _setContent(html) function that:</span></span>
<span class="line"><span style="color:#6A737D">  //    - Buffers calls until morphdom loads (_morphReady flag)</span></span>
<span class="line"><span style="color:#6A737D">  //    - Creates a target div with the new HTML</span></span>
<span class="line"><span style="color:#6A737D">  //    - Calls morphdom(root, target) with callbacks:</span></span>
<span class="line"><span style="color:#6A737D">  //      onBeforeElUpdated: skip if from.isEqualNode(to)</span></span>
<span class="line"><span style="color:#6A737D">  //      onNodeAdded: apply _fadeIn animation to new elements</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#9ECBFF"> `...`</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>The morphdom callbacks:</p>
          <ul>
            <li>
              <strong><code>onBeforeElUpdated</code></strong
              >: If the old node and new node are identical
              (<code>isEqualNode</code>), skip the update entirely. Existing
              content stays untouched in the DOM.
            </li>
            <li>
              <strong><code>onNodeAdded</code></strong
              >: When a genuinely new node appears in the tree, apply a CSS
              <code>_fadeIn</code> animation - 0.3s ease, subtle translateY for
              a “slide up” effect.
            </li>
          </ul>
          <p>
            <strong>Loading race condition</strong>: morphdom loads
            asynchronously from CDN. If <code>_setContent</code> is called
            before it loads, the call silently does nothing. We solved this with
            a pending buffer:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="javascript"
          ><code><span class="line"><span style="color:#E1E4E8">window._morphReady </span><span style="color:#F97583">=</span><span style="color:#79B8FF"> false</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#E1E4E8">window._pending </span><span style="color:#F97583">=</span><span style="color:#79B8FF"> null</span><span style="color:#E1E4E8">;</span></span>
<span class="line"></span>
<span class="line"><span style="color:#E1E4E8">window.</span><span style="color:#B392F0">_setContent</span><span style="color:#F97583"> =</span><span style="color:#F97583"> function</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">html</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">  if</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">!</span><span style="color:#E1E4E8">window._morphReady) { window._pending </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> html; </span><span style="color:#F97583">return</span><span style="color:#E1E4E8">; }</span></span>
<span class="line"><span style="color:#6A737D">  // ... morphdom diffing</span></span>
<span class="line"><span style="color:#E1E4E8">};</span></span>
<span class="line"></span>
<span class="line"><span style="color:#6A737D">// On morphdom load, flush:</span></span>
<span class="line"><span style="color:#E1E4E8">onload</span><span style="color:#F97583">=</span><span style="color:#9ECBFF">"window._morphReady=true</span><span style="color:#FDAEB7;font-style:italic">;</span></span>
<span class="line"><span style="color:#F97583">  if</span><span style="color:#E1E4E8">(window._pending){window.</span><span style="color:#B392F0">_setContent</span><span style="color:#E1E4E8">(window._pending);window._pending</span><span style="color:#F97583">=</span><span style="color:#79B8FF">null</span><span style="color:#E1E4E8">;}</span><span style="color:#9ECBFF">"</span></span></code></pre>
          <h3 id="script-execution">Script Execution</h3>
          <p>
            <code>innerHTML</code> doesn’t execute <code>script</code> tags.
            When the complete HTML arrives (on <code>toolcall_end</code>), we
            need to activate the scripts (Chart.js initialization, event
            listeners, etc.):
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="javascript"
          ><code><span class="line"><span style="color:#E1E4E8">window.</span><span style="color:#B392F0">_runScripts</span><span style="color:#F97583"> =</span><span style="color:#F97583"> function</span><span style="color:#E1E4E8">() {</span></span>
<span class="line"><span style="color:#E1E4E8">  document.</span><span style="color:#B392F0">querySelectorAll</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">'#root script'</span><span style="color:#E1E4E8">).</span><span style="color:#B392F0">forEach</span><span style="color:#E1E4E8">(</span><span style="color:#F97583">function</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">old</span><span style="color:#E1E4E8">) {</span></span>
<span class="line"><span style="color:#F97583">    var</span><span style="color:#E1E4E8"> s </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> document.</span><span style="color:#B392F0">createElement</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">'script'</span><span style="color:#E1E4E8">);</span></span>
<span class="line"><span style="color:#F97583">    if</span><span style="color:#E1E4E8"> (old.src) { s.src </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> old.src; }</span></span>
<span class="line"><span style="color:#F97583">    else</span><span style="color:#E1E4E8"> { s.textContent </span><span style="color:#F97583">=</span><span style="color:#E1E4E8"> old.textContent; }</span></span>
<span class="line"><span style="color:#E1E4E8">    old.parentNode.</span><span style="color:#B392F0">replaceChild</span><span style="color:#E1E4E8">(s, old);</span></span>
<span class="line"><span style="color:#E1E4E8">  });</span></span>
<span class="line"><span style="color:#E1E4E8">};</span></span></code></pre>
          <p>
            This clones each <code>script</code> tag into a fresh element (which
            the browser will execute) and replaces the inert original.
          </p>
          <h3 id="the-complete-streaming-flow">The Complete Streaming Flow</h3>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="plaintext"
          ><code><span class="line"><span>toolcall_start (show_widget detected)</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ├── streaming state initialized</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ▼</span></span>
<span class="line"><span>toolcall_delta (repeated, every ~token)</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ├── read partial.content[index].arguments.widget_code</span></span>
<span class="line"><span>  ├── debounce 150ms</span></span>
<span class="line"><span>  ├── first time: open Glimpse window with shellHTML()</span></span>
<span class="line"><span>  │   └── morphdom loads from CDN in background</span></span>
<span class="line"><span>  ├── subsequent: win.send(`_setContent('${escapedHTML}')`)</span></span>
<span class="line"><span>  │   └── morphdom diffs old vs new DOM</span></span>
<span class="line"><span>  │   └── new nodes get _fadeIn animation</span></span>
<span class="line"><span>  │   └── unchanged nodes stay untouched</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ▼</span></span>
<span class="line"><span>toolcall_end</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ├── final _setContent with complete HTML</span></span>
<span class="line"><span>  ├── _runScripts() activates script tags</span></span>
<span class="line"><span>  │   └── Chart.js loads from CDN</span></span>
<span class="line"><span>  │   └── charts render</span></span>
<span class="line"><span>  │   └── event listeners attach</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ▼</span></span>
<span class="line"><span>execute() called</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ├── reuses existing streaming window (no double-open)</span></span>
<span class="line"><span>  ├── waits for:</span></span>
<span class="line"><span>  │   ├── window.glimpse.send(data) → user interaction</span></span>
<span class="line"><span>  │   ├── window close → user dismissed</span></span>
<span class="line"><span>  │   └── 120s timeout → auto-resolve</span></span>
<span class="line"><span>  ├── returns tool result with interaction data</span></span>
<span class="line"><span>  │</span></span>
<span class="line"><span>  ▼</span></span>
<span class="line"><span>TUI renders compact summary:</span></span>
<span class="line"><span>  "✓ compound interest 800×600"</span></span></code></pre>
          <h3 id="string-escaping">String Escaping</h3>
          <p>
            One subtle but critical detail: the HTML content is injected as a
            JavaScript string literal via <code>win.send()</code>. This means we
            need to escape:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#F97583">function</span><span style="color:#B392F0"> escapeJS</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">s</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> string</span><span style="color:#E1E4E8">)</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> string</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#E1E4E8"> s</span></span>
<span class="line"><span style="color:#E1E4E8">    .</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#85E89D;font-weight:bold">\\</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">'</span><span style="color:#79B8FF">\\\\</span><span style="color:#9ECBFF">'</span><span style="color:#E1E4E8">)      </span><span style="color:#6A737D">// backslashes</span></span>
<span class="line"><span style="color:#E1E4E8">    .</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#DBEDFF">'</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"</span><span style="color:#79B8FF">\\</span><span style="color:#9ECBFF">'"</span><span style="color:#E1E4E8">)         </span><span style="color:#6A737D">// single quotes (our string delimiter)</span></span>
<span class="line"><span style="color:#E1E4E8">    .</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">'</span><span style="color:#79B8FF">\\</span><span style="color:#9ECBFF">n'</span><span style="color:#E1E4E8">)        </span><span style="color:#6A737D">// newlines</span></span>
<span class="line"><span style="color:#E1E4E8">    .</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#79B8FF">\r</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">g</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">'</span><span style="color:#79B8FF">\\</span><span style="color:#9ECBFF">r'</span><span style="color:#E1E4E8">)        </span><span style="color:#6A737D">// carriage returns</span></span>
<span class="line"><span style="color:#E1E4E8">    .</span><span style="color:#B392F0">replace</span><span style="color:#E1E4E8">(</span><span style="color:#9ECBFF">/</span><span style="color:#DBEDFF">&lt;</span><span style="color:#85E89D;font-weight:bold">\/</span><span style="color:#DBEDFF">script&gt;</span><span style="color:#9ECBFF">/</span><span style="color:#F97583">gi</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">'&lt;</span><span style="color:#79B8FF">\\</span><span style="color:#9ECBFF">/script&gt;'</span><span style="color:#E1E4E8">);  </span><span style="color:#6A737D">// closing script tags</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>
            The <code>&lt;\/script&gt;</code> replacement prevents the browser
            from interpreting a literal <code>/script</code> inside our
            JavaScript string as closing the outer script block.
          </p>
          <p>
            <img
              src="/images/generative-ui/diagram.gif"
              alt="Architecture diagram streaming live"
            />
          </p>
          <hr />
          <h2 id="part-4-extracting-the-design-guidelines---verbatim">
            Part 4: Extracting the Design Guidelines - Verbatim
          </h2>
          <p>
            I opened the browser devtools, inspected the network requests, and
            found the full tool call payloads in the response bodies - including
            the complete <code>read_me</code> tool results containing
            Anthropic’s actual design guidelines.
          </p>
          <p>The response JSON has this structure:</p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="json"
          ><code><span class="line"><span style="color:#E1E4E8">{</span></span>
<span class="line"><span style="color:#79B8FF">  "chat_messages"</span><span style="color:#E1E4E8">: [</span></span>
<span class="line"><span style="color:#E1E4E8">    {</span></span>
<span class="line"><span style="color:#79B8FF">      "content"</span><span style="color:#E1E4E8">: [</span></span>
<span class="line"><span style="color:#E1E4E8">        {</span></span>
<span class="line"><span style="color:#79B8FF">          "type"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"tool_use"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">          "name"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"visualize:read_me"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">          "input"</span><span style="color:#E1E4E8">: { </span><span style="color:#79B8FF">"modules"</span><span style="color:#E1E4E8">: [</span><span style="color:#9ECBFF">"interactive"</span><span style="color:#E1E4E8">, </span><span style="color:#9ECBFF">"chart"</span><span style="color:#E1E4E8">] }</span></span>
<span class="line"><span style="color:#E1E4E8">        },</span></span>
<span class="line"><span style="color:#E1E4E8">        {</span></span>
<span class="line"><span style="color:#79B8FF">          "type"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"tool_result"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">          "name"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"visualize:read_me"</span><span style="color:#E1E4E8">,</span></span>
<span class="line"><span style="color:#79B8FF">          "content"</span><span style="color:#E1E4E8">: [{ </span><span style="color:#79B8FF">"type"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"text"</span><span style="color:#E1E4E8">, </span><span style="color:#79B8FF">"text"</span><span style="color:#E1E4E8">: </span><span style="color:#9ECBFF">"# Imagine - Visual Creation Suite</span><span style="color:#79B8FF">\n\n</span><span style="color:#9ECBFF">## Modules</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">..."</span><span style="color:#E1E4E8"> }]</span></span>
<span class="line"><span style="color:#E1E4E8">        }</span></span>
<span class="line"><span style="color:#E1E4E8">      ]</span></span>
<span class="line"><span style="color:#E1E4E8">    }</span></span>
<span class="line"><span style="color:#E1E4E8">  ]</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>
            That <code>text</code> field in the <code>tool_result</code>? That’s
            the <strong>complete design guidelines</strong> that Anthropic feeds
            to Claude. Not a summary. Not Claude’s description of it. The actual
            system content, verbatim.
          </p>
          <h3 id="reconstructing-the-module-system">
            Reconstructing the Module System
          </h3>
          <p>
            By triggering <code>read_me</code> with different module
            combinations across multiple messages, we extracted all 5 module
            responses:
          </p>

          <table>
            <thead>
              <tr>
                <th>Modules requested</th>
                <th>Response size</th>
                <th>Unique sections included</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>["interactive"]</code></td>
                <td>19K</td>
                <td>Core + UI components + Color palette</td>
              </tr>
              <tr>
                <td><code>["chart"]</code></td>
                <td>22K</td>
                <td>
                  Core + UI components + Color palette + Charts (Chart.js)
                </td>
              </tr>
              <tr>
                <td><code>["mockup"]</code></td>
                <td>19K</td>
                <td>Core + UI components + Color palette</td>
              </tr>
              <tr>
                <td><code>["art"]</code></td>
                <td>17K</td>
                <td>Core + SVG setup + Art and illustration</td>
              </tr>
              <tr>
                <td><code>["diagram"]</code></td>
                <td>59K</td>
                <td>Core + Color palette + SVG setup + Diagram types</td>
              </tr>
            </tbody>
          </table>
          <p>
            Every response shares the same <strong>core</strong> (philosophy,
            streaming rules, typography, CSS variables,
            <code>sendPrompt()</code> docs). Then each module appends its
            specific sections. Some sections are shared across modules -
            <code>UI components</code> appears in interactive, chart, and
            mockup; <code>SVG setup</code> appears in both art and diagram.
          </p>
          <p>We wrote a script to:</p>
          <ol>
            <li>Parse the conversation JSON</li>
            <li>
              Split each <code>read_me</code> response at
              <code>##</code> heading boundaries
            </li>
            <li>Deduplicate shared sections</li>
            <li>
              Verify that recombining sections produces byte-identical output to
              the originals
            </li>
          </ol>
          <p>
            The result: <strong>10 unique sections</strong> that can be
            recombined to reproduce any module response exactly (4/5 exact
            match, 1 has a single whitespace character difference).
          </p>
          <h3 id="whats-inside---the-design-system">
            What’s Inside - The Design System
          </h3>
          <p>
            The guidelines are <em>thorough</em>. This isn’t a “use nice colors”
            pamphlet. It’s a production design system with hard rules:
          </p>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/core_design_system.md"
              ><strong>Core</strong></a
            >
            - The foundation every widget must follow:
          </p>
          <ul>
            <li>
              Streaming-first architecture: <code>style</code> → HTML →
              <code>script</code> last
            </li>
            <li>
              No gradients, shadows, blur - they flash during streaming DOM
              diffs
            </li>
            <li>
              No <code>&lt;!-- comments --&gt;</code> - waste tokens and break
              streaming
            </li>
            <li>Two font weights only (400, 500) - never 600 or 700</li>
            <li>Sentence case everywhere, never Title Case or ALL CAPS</li>
            <li>
              CSS variables for all colors (<code>--color-text-primary</code>,
              <code>--color-background-secondary</code>)
            </li>
            <li>
              Dark mode is mandatory - every color must work in both modes
            </li>
            <li>
              CDN allowlist: <code>cdnjs.cloudflare.com</code>,
              <code>cdn.jsdelivr.net</code>, <code>unpkg.com</code>,
              <code>esm.sh</code>
            </li>
          </ul>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/color_palette.md"
              ><strong>Color palette</strong></a
            >
            - Nine color ramps, each with 7 stops from lightest to darkest:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="plaintext"
          ><code><span class="line"><span>Purple: #EEEDFE → #CECBF6 → #AFA9EC → #7F77DD → #534AB7 → #3C3489 → #26215C</span></span>
<span class="line"><span>Teal:   #E1F5EE → #9FE1CB → #5DCAA5 → #1D9E75 → #0F6E56 → #085041 → #04342C</span></span>
<span class="line"><span>Coral:  #FAECE7 → #F5C4B3 → #F0997B → #D85A30 → #993C1D → #712B13 → #4A1B0C</span></span>
<span class="line"><span>...</span></span></code></pre>
          <p>
            With strict rules: color encodes meaning, not sequence. 2-3 ramps
            per widget max. Text on colored backgrounds must use the 800/900
            stop from the same ramp - never black.
          </p>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/svg_setup.md"
              ><strong>SVG setup</strong></a
            >
            - A masterclass in SVG diagram engineering:
          </p>
          <ul>
            <li>
              ViewBox safety checklist (5 verification steps before finalizing)
            </li>
            <li>
              Font width calibration table with actual rendered pixel
              measurements
            </li>
            <li>
              Pre-built CSS classes (<code>c-blue</code>, <code>c-teal</code>,
              <code>t</code>, <code>ts</code>, <code>th</code>,
              <code>box</code>, <code>node</code>, <code>arr</code>)
            </li>
            <li>
              Arrow markers that auto-inherit stroke color via
              <code>context-stroke</code>
            </li>
            <li>
              Rules about <code>fill="none"</code> on connector paths (SVG
              defaults to <code>fill: black</code>)
            </li>
          </ul>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/diagram_types.md"
              ><strong>Diagram types</strong></a
            >
            - The largest section by far:
          </p>
          <ul>
            <li>
              Two rules that “cause most diagram failures” (arrow intersection
              checks, box width from label length)
            </li>
            <li>
              Decision framework: route on the verb, not the noun (“how do LLMs
              work” → Illustrative, “transformer architecture” → Structural)
            </li>
            <li>
              Flowchart, structural, and illustrative diagram sub-specifications
            </li>
            <li>
              Complexity budgets: ≤5 words per subtitle, ≤4 boxes per horizontal
              tier
            </li>
          </ul>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/ui_components.md"
              ><strong>UI components</strong></a
            >
            - Tokens for building mockups:
          </p>
          <ul>
            <li>
              Cards: white bg, 0.5px border, radius-lg, padding 1rem 1.25rem
            </li>
            <li>Buttons pre-styled with hover/active states</li>
            <li>Metric cards, form elements, skeleton loading patterns</li>
            <li>Layout rules for editorial vs card vs comparison views</li>
          </ul>
          <p>
            <a
              href="https://github.com/Michaelliv/pi-generative-ui/blob/main/.pi/extensions/generative-ui/claude-guidelines/sections/charts_chart_js.md"
              ><strong>Charts</strong></a
            >
            - Chart.js-specific guidance:
          </p>
          <ul>
            <li>
              Canvas wrapper sizing (<code>position: relative</code>, explicit
              height)
            </li>
            <li>Always disable default legend, build custom HTML legends</li>
            <li>Number formatting: <code>-$5M</code> not <code>$-5M</code></li>
            <li>Dashboard layout patterns</li>
          </ul>
          <h3 id="using-the-real-guidelines">Using the Real Guidelines</h3>
          <p>
            We replaced our hand-written guidelines with the extracted
            originals. The <code>guidelines.ts</code> file is now verbatim
            Anthropic content, organized as lazy-loaded sections:
          </p>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="typescript"
          ><code><span class="line"><span style="color:#F97583">export</span><span style="color:#F97583"> function</span><span style="color:#B392F0"> getGuidelines</span><span style="color:#E1E4E8">(</span><span style="color:#FFAB70">modules</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> string</span><span style="color:#E1E4E8">[])</span><span style="color:#F97583">:</span><span style="color:#79B8FF"> string</span><span style="color:#E1E4E8"> {</span></span>
<span class="line"><span style="color:#F97583">  let</span><span style="color:#E1E4E8"> content </span><span style="color:#F97583">=</span><span style="color:#79B8FF"> CORE</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#F97583">  const</span><span style="color:#79B8FF"> seen</span><span style="color:#F97583"> =</span><span style="color:#F97583"> new</span><span style="color:#B392F0"> Set</span><span style="color:#E1E4E8">&lt;</span><span style="color:#79B8FF">string</span><span style="color:#E1E4E8">&gt;();</span></span>
<span class="line"><span style="color:#F97583">  for</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">const</span><span style="color:#79B8FF"> mod</span><span style="color:#F97583"> of</span><span style="color:#E1E4E8"> modules) {</span></span>
<span class="line"><span style="color:#F97583">    const</span><span style="color:#79B8FF"> sections</span><span style="color:#F97583"> =</span><span style="color:#79B8FF"> MODULE_SECTIONS</span><span style="color:#E1E4E8">[mod];</span></span>
<span class="line"><span style="color:#F97583">    if</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">!</span><span style="color:#E1E4E8">sections) </span><span style="color:#F97583">continue</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#F97583">    for</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">const</span><span style="color:#79B8FF"> section</span><span style="color:#F97583"> of</span><span style="color:#E1E4E8"> sections) {</span></span>
<span class="line"><span style="color:#F97583">      if</span><span style="color:#E1E4E8"> (</span><span style="color:#F97583">!</span><span style="color:#E1E4E8">seen.</span><span style="color:#B392F0">has</span><span style="color:#E1E4E8">(section)) {</span></span>
<span class="line"><span style="color:#E1E4E8">        seen.</span><span style="color:#B392F0">add</span><span style="color:#E1E4E8">(section);</span></span>
<span class="line"><span style="color:#E1E4E8">        content </span><span style="color:#F97583">+=</span><span style="color:#9ECBFF"> "</span><span style="color:#79B8FF">\n\n\n</span><span style="color:#9ECBFF">"</span><span style="color:#F97583"> +</span><span style="color:#E1E4E8"> section;</span></span>
<span class="line"><span style="color:#E1E4E8">      }</span></span>
<span class="line"><span style="color:#E1E4E8">    }</span></span>
<span class="line"><span style="color:#E1E4E8">  }</span></span>
<span class="line"><span style="color:#F97583">  return</span><span style="color:#E1E4E8"> content </span><span style="color:#F97583">+</span><span style="color:#9ECBFF"> "</span><span style="color:#79B8FF">\n</span><span style="color:#9ECBFF">"</span><span style="color:#E1E4E8">;</span></span>
<span class="line"><span style="color:#E1E4E8">}</span></span></code></pre>
          <p>
            The deduplication matters: if you request
            <code>["interactive", "chart"]</code>, the shared
            <code>UI components</code> and <code>Color palette</code> sections
            are included once, not twice. This matches exactly how claude.ai’s
            <code>read_me</code> tool behaves.
          </p>
          <hr />
          <h2 id="part-5-what-we-learned">Part 5: What We Learned</h2>
          <h3 id="1-claudes-generative-ui-is-simpler-than-it-looks">
            1. Claude’s Generative UI is Simpler Than It Looks
          </h3>
          <p>
            It’s not a special rendering engine. It’s a tool call that returns
            HTML, injected into the DOM with incremental parsing as tokens
            stream. The sophistication is in the
            <strong>design guidelines</strong> - thousands of tokens of rules
            about colors, typography, dark mode, streaming-friendly structure,
            and when to use each pattern.
          </p>
          <h3 id="2-the-read_me-pattern-is-brilliant">
            2. The <code>read_me</code> Pattern is Brilliant
          </h3>
          <p>
            Lazy-loading documentation into the model’s context on demand is a
            pattern worth stealing. Instead of a massive system prompt, you load
            specialized knowledge only when the task requires it. Our extension
            uses the same architecture: 5 modules, loaded selectively.
          </p>
          <h3 id="3-dom-diffing-solves-streaming-smoothness">
            3. DOM Diffing Solves Streaming Smoothness
          </h3>
          <p>
            You can’t just <code>innerHTML</code> on every token - it causes
            full-page flashes. You can’t naively append nodes - partial HTML
            parsing creates unpredictable tree structures. You need DOM diffing
            (morphdom, idiomorph, or similar) to apply minimal patches and
            animate only genuinely new nodes.
          </p>
          <h3 id="4-glimpse-makes-terminal-agents-visual">
            4. Glimpse Makes Terminal Agents Visual
          </h3>
          <p>
            The terminal doesn’t need to render HTML. It needs to
            <strong>spawn</strong> something that renders HTML. Glimpse’s
            sub-50ms WKWebView windows with bidirectional JSON communication
            bridge the gap perfectly. The terminal stays a terminal; the visual
            content gets a real browser engine.
          </p>
          <h3 id="5-pi-ais-normalized-streaming-events-are-gold">
            5. pi-ai’s Normalized Streaming Events Are Gold
          </h3>
          <p>
            Pi’s AI layer normalizes streaming events across all providers into
            <code>toolcall_start</code> / <code>toolcall_delta</code> /
            <code>toolcall_end</code> with progressively-parsed
            <code>arguments</code>. This means the streaming approach works
            identically whether the model is Anthropic, OpenAI, Google, or any
            other provider. We didn’t need a partial JSON parser - pi-ai already
            does it.
          </p>
          <hr />
          <h2 id="the-code">The Code</h2>
          <p>
            The complete extension is ~350 lines of TypeScript in two files:
          </p>
          <ul>
            <li>
              <strong><code>index.ts</code></strong> - Tool registration,
              streaming interception, Glimpse integration, TUI rendering
            </li>
            <li>
              <strong><code>guidelines.ts</code></strong> - Modular design
              guidelines (core + 5 lazy-loaded modules)
            </li>
          </ul>
          <p>Dependencies:</p>
          <ul>
            <li><code>glimpseui</code> - Native macOS WKWebView windows</li>
            <li>
              <code>morphdom</code> (CDN, loaded at runtime in the WebView) -
              DOM diffing for smooth streaming
            </li>
          </ul>
          <p>
            The extension lives in
            <code>.pi/extensions/generative-ui/</code> and is auto-discovered by
            pi on startup. No configuration needed.
          </p>
          <h3 id="project-structure">Project Structure</h3>
          <pre
            class="astro-code github-dark"
            style="background-color: #24292e; color: #e1e4e8; overflow-x: auto"
            tabindex="0"
            data-language="plaintext"
          ><code><span class="line"><span>pi-generative-ui/</span></span>
<span class="line"><span>├── .pi/</span></span>
<span class="line"><span>│   └── extensions/</span></span>
<span class="line"><span>│       └── generative-ui/</span></span>
<span class="line"><span>│           ├── index.ts        # Extension entry point</span></span>
<span class="line"><span>│           └── guidelines.ts   # Lazy-loaded design modules</span></span>
<span class="line"><span>├── node_modules/</span></span>
<span class="line"><span>│   └── glimpseui/             # Native macOS WKWebView</span></span>
<span class="line"><span>├── package.json</span></span>
<span class="line"><span>└── BLOG.md</span></span></code></pre>
          <hr />
          <h2 id="whats-next">What’s Next</h2>
          <ul>
            <li>
              <strong>Dark mode adaptation</strong> - Glimpse provides
              <code>appearance.darkMode</code> on the <code>ready</code> event.
              The shell could inject CSS variables matching the system
              appearance.
            </li>
            <li>
              <strong><code>sendPrompt()</code> equivalent</strong> -
              claude.ai’s widgets have a <code>sendPrompt(text)</code> function
              that sends a message to the chat as if the user typed it. We could
              implement this via
              <code>window.glimpse.send({ type: 'prompt', text: '...' })</code>
              and have the extension call <code>pi.sendUserMessage()</code>.
            </li>
            <li>
              <strong>Persistent widgets</strong> - Keep a widget window open
              across multiple turns, pushing live updates from tool results.
            </li>
            <li>
              <strong>Widget gallery</strong> - Pre-built templates for common
              patterns (confirm dialogs, data tables, form wizards) that the LLM
              can reference by name.
            </li>
          </ul>
          <hr />
          <h2 id="acknowledgments">Acknowledgments</h2>
          <ul>
            <li>
              <strong>Claude</strong> - for being surprisingly transparent about
              its own implementation when asked the right questions
            </li>
            <li>
              <strong>Anthropic</strong> - for the generative UI system that
              inspired this
            </li>
            <li>
              <strong
                ><a href="https://github.com/hazat/glimpse">Glimpse</a></strong
              >
              (Daniel Griesser) - the native macOS micro-UI that made this
              possible
            </li>
            <li>
              <strong
                ><a href="https://github.com/badlogic/pi-mono">pi</a></strong
              >
              (Mario Zechner) - the extensible coding agent that gave us the
              hooks to build on
            </li>
            <li>
              <strong
                ><a href="https://github.com/patrick-steele-idem/morphdom"
                  >morphdom</a
                ></strong
              >
              - fast DOM diffing that solved the streaming smoothness problem
            </li>
          </ul>
        </div>
      </article>
      <div class="related" data-astro-cid-bvzihdzo="">
        <div class="section-label" data-astro-cid-bvzihdzo="">
          <span data-astro-cid-bvzihdzo="">/</span>Related
        </div>
        <a
          href="/blog/web-search-for-agents-2026/"
          class="related-item"
          data-astro-cid-bvzihdzo=""
        >
          <span class="related-title" data-astro-cid-bvzihdzo=""
            >Web Search for Agents in 2026</span
          > </a
        ><a
          href="/blog/system-reminders-steering-agents/"
          class="related-item"
          data-astro-cid-bvzihdzo=""
        >
          <span class="related-title" data-astro-cid-bvzihdzo=""
            >System reminders - how Claude Code steers itself</span
          > </a
        ><a
          href="/blog/building-napkin-memory-system-for-agents/"
          class="related-item"
          data-astro-cid-bvzihdzo=""
        >
          <span class="related-title" data-astro-cid-bvzihdzo=""
            >Building napkin - a memory system for agents</span
          >
        </a>
      </div>
      <nav class="post-nav" data-astro-cid-bvzihdzo="">
        <div class="section-label" data-astro-cid-bvzihdzo="">
          <span data-astro-cid-bvzihdzo="">/</span>Navigation
        </div>
        <div class="nav-links" data-astro-cid-bvzihdzo="">
          <a
            href="/blog/software-engineering-anarchist/"
            class="nav-link prev"
            data-astro-cid-bvzihdzo=""
          >
            <span class="nav-label" data-astro-cid-bvzihdzo="">← Previous</span>
            <span class="nav-title" data-astro-cid-bvzihdzo=""
              >The Software Engineering Anarchist</span
            >
          </a>
          <a
            href="/blog/building-napkin-memory-system-for-agents/"
            class="nav-link next"
            data-astro-cid-bvzihdzo=""
          >
            <span class="nav-label" data-astro-cid-bvzihdzo="">Next →</span>
            <span class="nav-title" data-astro-cid-bvzihdzo=""
              >Building napkin - a memory system for agents</span
            >
          </a>
        </div>
      </nav>
    </main>
    <footer data-astro-cid-sz7xmlte="">
      <div class="section-label" data-astro-cid-sz7xmlte="">
        <span data-astro-cid-sz7xmlte="">/</span>Footer
      </div>
      <div class="footer-content" data-astro-cid-sz7xmlte="">
        <div class="footer-left" data-astro-cid-sz7xmlte="">
          <span class="author" data-astro-cid-sz7xmlte=""
            >Michael Livshits</span
          >
          <span class="copyright" data-astro-cid-sz7xmlte="">© 2026</span>
        </div>
        <div class="footer-links" data-astro-cid-sz7xmlte="">
          <a href="/about" class="tag" data-astro-cid-sz7xmlte="">About</a>
          <a
            href="https://github.com/Michaelliv"
            target="_blank"
            class="tag"
            data-astro-cid-sz7xmlte=""
            >GitHub</a
          >
          <a href="/subscribe" class="tag" data-astro-cid-sz7xmlte=""
            >Subscribe</a
          >
          <a href="/rss.xml" class="tag" data-astro-cid-sz7xmlte="">RSS</a>
        </div>
      </div>
    </footer>
    <vercel-analytics
      data-props='{"data-astro-cid-bvzihdzo":true}'
      data-params='{"slug":"reverse-engineering-claude-generative-ui"}'
      data-pathname="/blog/reverse-engineering-claude-generative-ui/"
    ></vercel-analytics>
    <script type="module" data-astro-exec="">
      var f = "@vercel/analytics",
        l = "1.6.1",
        w = () => {
          window.va ||
            (window.va = function (...r) {
              (window.vaq = window.vaq || []).push(r);
            });
        };
      function d() {
        return typeof window < "u";
      }
      function u() {
        try {
          const e = "production";
        } catch {}
        return "production";
      }
      function v(e = "auto") {
        if (e === "auto") {
          window.vam = u();
          return;
        }
        window.vam = e;
      }
      function m() {
        return (d() ? window.vam : u()) || "production";
      }
      function c() {
        return m() === "development";
      }
      function b(e, r) {
        if (!e || !r) return e;
        let n = e;
        try {
          const t = Object.entries(r);
          for (const [a, i] of t)
            if (!Array.isArray(i)) {
              const o = s(i);
              o.test(n) && (n = n.replace(o, `/[${a}]`));
            }
          for (const [a, i] of t)
            if (Array.isArray(i)) {
              const o = s(i.join("/"));
              o.test(n) && (n = n.replace(o, `/[...${a}]`));
            }
          return n;
        } catch {
          return e;
        }
      }
      function s(e) {
        return new RegExp(`/${h(e)}(?=[/?#]|$)`);
      }
      function h(e) {
        return e.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      }
      function y(e) {
        return e.scriptSrc
          ? e.scriptSrc
          : c()
            ? "https://va.vercel-scripts.com/v1/script.debug.js"
            : e.basePath
              ? `${e.basePath}/insights/script.js`
              : "/_vercel/insights/script.js";
      }
      function g(e = { debug: !0 }) {
        var r;
        if (!d()) return;
        (v(e.mode),
          w(),
          e.beforeSend &&
            ((r = window.va) == null ||
              r.call(window, "beforeSend", e.beforeSend)));
        const n = y(e);
        if (document.head.querySelector(`script[src*="${n}"]`)) return;
        const t = document.createElement("script");
        ((t.src = n),
          (t.defer = !0),
          (t.dataset.sdkn = f + (e.framework ? `/${e.framework}` : "")),
          (t.dataset.sdkv = l),
          e.disableAutoTrack && (t.dataset.disableAutoTrack = "1"),
          e.endpoint
            ? (t.dataset.endpoint = e.endpoint)
            : e.basePath && (t.dataset.endpoint = `${e.basePath}/insights`),
          e.dsn && (t.dataset.dsn = e.dsn),
          (t.onerror = () => {
            const a = c()
              ? "Please check if any ad blockers are enabled and try again."
              : "Be sure to enable Web Analytics for your project and deploy again. See https://vercel.com/docs/analytics/quickstart for more information.";
            console.log(
              `[Vercel Web Analytics] Failed to load script from ${n}. ${a}`,
            );
          }),
          c() && e.debug === !1 && (t.dataset.debug = "false"),
          document.head.appendChild(t));
      }
      function p({ route: e, path: r }) {
        var n;
        (n = window.va) == null ||
          n.call(window, "pageview", { route: e, path: r });
      }
      function k() {
        try {
          return;
        } catch {}
      }
      customElements.define(
        "vercel-analytics",
        class extends HTMLElement {
          constructor() {
            super();
            try {
              const r = JSON.parse(this.dataset.props ?? "{}"),
                n = JSON.parse(this.dataset.params ?? "{}");
              g({
                ...r,
                disableAutoTrack: !0,
                framework: "astro",
                basePath: k(),
                beforeSend: window.webAnalyticsBeforeSend,
              });
              const t = this.dataset.pathname;
              p({ route: b(t ?? "", n), path: t });
            } catch (r) {
              throw new Error(`Failed to parse WebAnalytics properties: ${r}`);
            }
          }
        },
      );
    </script>
    <script data-astro-exec="">
      (function () {
        const title =
          "Reverse-engineering Claude's generative UI - then building it for the terminal";

        const shareBtn = document.querySelector(".share-btn");
        const shareText = shareBtn?.querySelector(".share-text");

        shareBtn?.addEventListener("click", async () => {
          const url = window.location.href;

          if (navigator.share) {
            try {
              await navigator.share({ title, url });
            } catch (err) {
              if (err.name !== "AbortError") {
                copyToClipboard(url);
              }
            }
          } else {
            copyToClipboard(url);
          }
        });

        function copyToClipboard(text) {
          navigator.clipboard.writeText(text).then(() => {
            if (shareText) {
              const original = shareText.textContent;
              shareText.textContent = "Copied!";
              setTimeout(() => {
                shareText.textContent = original;
              }, 2000);
            }
          });
        }
      })();
    </script>
  </body>
  <chatgpt-sidebar
    data-rendered="true"
    data-gpts-theme="light"
  ></chatgpt-sidebar>
</html>
