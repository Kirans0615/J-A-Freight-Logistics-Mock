#!/usr/bin/env python3
"""Generates the J&A Freight Systems static site (8 pages, shared chrome)."""
import os

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/logo-40years.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>

<div class="topbar">
  <div class="wrap">
    <span>Family-built 3PL &middot; Chicago, IL &middot; Since 1986</span>
    <div class="tb-right">
      <a href="tel:+17735550140">(773) 555-0140</a>
      <a href="mailto:dispatch@jafreightsystems.com">dispatch@jafreightsystems.com</a>
      <span class="tb-addr">Mon&ndash;Fri 7:00&ndash;19:00 CT</span>
    </div>
  </div>
</div>

<header class="site">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="J&A Freight Systems home">
      <img src="assets/logo-main.png" alt="J&A Freight Systems — Transportation Specialists">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="main" aria-label="Primary">
      <a href="index.html">Home</a>
      <a href="shippers.html">Shippers</a>
      <a href="carriers.html">Carriers</a>
      <a href="technology.html">Technology</a>
      <a href="about.html">About</a>
      <a href="careers.html">Careers</a>
      <a href="contact.html">Contact</a>
      <a href="contact.html#quote" class="btn btn-gold nav-cta">Get a Quote</a>
    </nav>
  </div>
</header>
"""

FOOTER = """
<div class="cta-band">
  <div class="wrap">
    <div class="cta-inner reveal">
      <div class="cta-star" aria-hidden="true"></div>
      <div>
        <h2>{cta_h}</h2>
        <p>{cta_p}</p>
      </div>
      <a href="{cta_href}" class="btn btn-navy">{cta_btn} <span class="arrow">&rarr;</span></a>
    </div>
  </div>
</div>

<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="foot-logo" src="assets/logo-main.png" alt="J&A Freight Systems">
        <p class="foot-about">A non-asset-based third-party logistics provider moving freight across North America since 1986. Family-built, knowledge-driven, and accountable on every load.</p>
        <div class="foot-badges">
          <span class="badge">FMCSA Registered</span>
          <span class="badge">Surety Bonded</span>
          <span class="badge">MercuryGate TMS</span>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="shippers.html">Full Truckload</a></li>
          <li><a href="shippers.html">Less-Than-Truckload</a></li>
          <li><a href="shippers.html">Refrigerated</a></li>
          <li><a href="shippers.html">Drayage &amp; Intermodal</a></li>
          <li><a href="shippers.html">Managed Transportation</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="technology.html">Technology</a></li>
          <li><a href="carriers.html">For Carriers</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="positions.html">Open Positions</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Market Brief</h4>
        <p style="font-size:.93rem;margin-bottom:6px">Monthly freight market insights for mid-market shippers. No spam — just rates, capacity, and what they mean for you.</p>
        <form class="news-form" data-demo>
          <input type="email" placeholder="Work email" required aria-label="Email for market brief">
          <button class="btn btn-gold" type="submit">Join</button>
        </form>
        <div class="form-success">You're on the list. First brief lands next month.</div>
      </div>
    </div>
    <div class="legal">
      <span>&copy; 2026 J&A Freight Systems, Inc. All rights reserved.</span>
      <span>MC# 123456 &middot; DOT# 7891011 &middot; Chicago, Illinois</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
"""

DEFAULT_CTA = dict(
    cta_h="Forty years in. Just getting started.",
    cta_p="Tell us what you ship, where it goes, and what's been going wrong. We'll show you what a knowledge-driven 3PL looks like on your freight.",
    cta_href="contact.html#quote",
    cta_btn="Talk to an Expert",
)

# SVG icons (inline, stroke style)
IC = {
 'truck':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 7h12v9H1zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
 'box':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
 'snow':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 2v20M4 6l16 12M20 6L4 18M12 2l-2 3h4zM12 22l-2-3h4z"/></svg>',
 'anchor':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><path d="M12 7.5V21M4 13H2c0 5 4.5 8 10 8s10-3 10-8h-2M12 21c-4 0-7-3-7-8"/></svg>',
 'chart':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-5 3 3 5-7"/></svg>',
 'shield':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
 'eye':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
 'dollar':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 6.5C17 4.5 14.8 3.5 12 3.5S7 4.7 7 7s2 3.2 5 4 5 1.8 5 4.5-2.2 4-5 4-5-1.2-5-3.5"/></svg>',
 'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.13.96.36 1.9.7 2.8a2 2 0 0 1-.45 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.45c.9.34 1.84.57 2.8.7A2 2 0 0 1 22 16.9z"/></svg>',
 'mail':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 'grad':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 9L12 4 2 9l10 5 10-5z"/><path d="M6 11.5V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-4.5M22 9v5"/></svg>',
 'hand':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 12l4.5-4.5a2 2 0 0 1 3 2.6L13 16l-4 1 1-4 4.5-4.5M3 21l5-5"/></svg>',
 'route':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="5" r="2.5"/><path d="M7 17.5C10 15 8 11 12 10s7-1.5 5.5-3.5" stroke-dasharray="3 3"/></svg>',
}

# Route map SVG used as decorative hero/visual element
def routemap(opacity="0.5"):
    return f"""<svg class="hero-route" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1.5">
    <path d="M80,470 Q280,300 460,360 T840,250 T1160,150" stroke-dasharray="6 8"/>
    <path d="M150,540 Q420,480 640,420 T1100,330" stroke-dasharray="6 8"/>
  </g>
  <g fill="#FFC20D">
    <circle cx="80" cy="470" r="5"/><circle cx="460" cy="360" r="5"/>
    <circle cx="840" cy="250" r="5"/><circle cx="1160" cy="150" r="5"/>
    <circle cx="640" cy="420" r="4" opacity=".7"/><circle cx="1100" cy="330" r="4" opacity=".7"/>
  </g>
  <g fill="rgba(255,255,255,.9)">
    <path d="M460 336 l5 14 14 5 -14 5 -5 14 -5 -14 -14 -5 14 -5z" opacity=".35"/>
    <path d="M840 226 l5 14 14 5 -14 5 -5 14 -5 -14 -14 -5 14 -5z" opacity=".25"/>
  </g>
</svg>"""


def compass(cx, cy, s=1.0):
    """J&A compass star: gold circle, navy ring, quartered 4-point star, diagonal chevrons."""
    return f"""<g transform="translate({cx},{cy}) scale({s})">
<circle r="86" fill="#FFC20D" stroke="#14365C" stroke-width="11"/>
<g transform="rotate(45)">
  <path d="M0,-58 L13,-30 L0,-40 L-13,-30 Z" fill="#FFFFFF"/>
  <path d="M0,-58 L13,-30 L0,-40 L-13,-30 Z" fill="#14365C" transform="rotate(90)"/>
  <path d="M0,-58 L13,-30 L0,-40 L-13,-30 Z" fill="#FFFFFF" transform="rotate(180)"/>
  <path d="M0,-58 L13,-30 L0,-40 L-13,-30 Z" fill="#14365C" transform="rotate(270)"/>
</g>
<path d="M0,-122 L19,-19 L122,0 L19,19 L0,122 Z" fill="#14365C" stroke="#FFFFFF" stroke-width="3"/>
<path d="M0,-122 L-19,-19 L-122,0 L-19,19 L0,122 Z" fill="#FFFFFF" stroke="#14365C" stroke-width="3"/>
</g>"""

def brand_lockup(cx, cy, s=1.0, fill="#FFC20D"):
    """Compass + J&A LOGISTICS wordmark, centered lockup."""
    return f"""<g transform="translate({cx},{cy}) scale({s})">
{compass(-150, 0, 0.42)}
<text x="-100" y="-2" font-family="Barlow Condensed" font-weight="700" font-size="46" fill="{fill}" letter-spacing="2">J&amp;A LOGISTICS</text>
<text x="-100" y="24" font-family="Barlow" font-weight="600" font-size="15" fill="rgba(255,255,255,.75)" letter-spacing="5">TRANSPORTATION SPECIALISTS</text>
</g>"""

def truck_svg():
    """Flat-style branded semi truck, navy trailer with gold J&A LOGISTICS livery."""
    return f"""<svg viewBox="0 0 480 360" aria-hidden="true">
<circle cx="400" cy="70" r="38" fill="#FFC20D" opacity=".9"/>
<g fill="none" stroke="rgba(255,255,255,.15)" stroke-width="1.5">
  <path d="M20,90 Q120,40 220,70 T460,40" stroke-dasharray="5 7"/>
</g>
<rect x="0" y="288" width="480" height="72" fill="#0B2138"/>
<g stroke="#FFC20D" stroke-width="4" stroke-dasharray="26 22"><path d="M0 324 H480"/></g>
<!-- trailer -->
<rect x="48" y="120" width="280" height="140" rx="8" fill="#0E2A47" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="2"/>
{compass(108, 190, 0.46)}
<text x="160" y="183" font-family="Barlow Condensed" font-weight="700" font-size="38" fill="#FFC20D" letter-spacing="1.5">J&amp;A LOGISTICS</text>
<text x="160" y="208" font-family="Barlow" font-weight="600" font-size="12.5" fill="rgba(255,255,255,.7)" letter-spacing="3.5">TRANSPORTATION SPECIALISTS</text>
<rect x="48" y="244" width="280" height="6" fill="#FFC20D"/>
<!-- cab -->
<path d="M336 260 V160 q0 -10 10 -10 h44 q8 0 13 7 l24 36 q5 8 5 17 v50 z" fill="#FFC20D" stroke="#E2A900" stroke-width="2"/>
<path d="M392 158 l22 33 q3 5 3 10 v8 h-44 v-51 z" fill="#0E2A47" opacity=".85"/>
<rect x="336" y="232" width="96" height="28" fill="#14365C"/>
<!-- wheels -->
<g fill="#10151B" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="3">
  <circle cx="100" cy="276" r="22"/><circle cx="152" cy="276" r="22"/>
  <circle cx="372" cy="276" r="22"/>
</g>
<g fill="#FFC20D"><circle cx="100" cy="276" r="7"/><circle cx="152" cy="276" r="7"/><circle cx="372" cy="276" r="7"/></g>
<!-- motion lines -->
<g stroke="#FFC20D" stroke-width="4" stroke-linecap="round" opacity=".7">
  <path d="M14 160 H40"/><path d="M4 196 H36"/><path d="M18 232 H40"/>
</g>
</svg>"""

def container_svg():
    """Gold shipping container on crane cables — homage to the original site's signature image."""
    return f"""<svg viewBox="0 0 560 420" aria-hidden="true">
<!-- crane cables -->
<g stroke="rgba(255,255,255,.5)" stroke-width="2.5">
  <path d="M180 0 L196 96"/><path d="M380 0 L364 96"/>
</g>
<g stroke="#FFC20D" stroke-width="5"><path d="M150 96 H410"/></g>
<g stroke="rgba(255,255,255,.5)" stroke-width="2.5">
  <path d="M168 96 L168 128"/><path d="M392 96 L392 128"/>
</g>
<!-- container body -->
<rect x="110" y="128" width="340" height="190" rx="6" fill="#FFC20D" stroke="#E2A900" stroke-width="3"/>
<!-- corrugation -->
<g stroke="#E2A900" stroke-width="3" opacity=".75">
  <path d="M138 136 V310"/><path d="M166 136 V310"/><path d="M394 136 V310"/><path d="M422 136 V310"/>
</g>
<!-- brand panel -->
<rect x="184" y="158" width="192" height="130" rx="6" fill="#FFFFFF"/>
{compass(280, 200, 0.36)}
<text x="280" y="258" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="30" fill="#14365C" letter-spacing="1.5">J&amp;A LOGISTICS</text>
<text x="280" y="276" text-anchor="middle" font-family="Barlow" font-weight="600" font-size="10.5" fill="#5A6B7E" letter-spacing="3">TRANSPORTATION SPECIALISTS</text>
<!-- container id -->
<text x="120" y="345" font-family="Barlow Condensed" font-weight="600" font-size="17" fill="rgba(255,255,255,.85)" letter-spacing="3">JALU 1986 040 &middot; 45G1</text>
<!-- ground shadow -->
<ellipse cx="280" cy="380" rx="200" ry="14" fill="rgba(0,0,0,.3)"/>
</svg>"""

def card(icon, h, p, gold=False):
    return f"""<div class="card{' gold-top' if gold else ''} reveal">
  <div class="icon">{IC[icon]}</div>
  <h3>{h}</h3>
  <p>{p}</p>
</div>"""

PAGES = {}

# ============================================================ HOME
PAGES['index.html'] = dict(
 title="J&A Freight Systems | Family-Built 3PL — Chicago, IL Since 1986",
 desc="J&A Freight Systems is a non-asset-based 3PL moving freight across North America since 1986. FTL, LTL, refrigerated, drayage, and managed transportation for mid-market shippers.",
 cta=DEFAULT_CTA,
 body=f"""
<section class="hero">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Non-Asset 3PL &middot; Est. 1986</span>
        <h1>Global Reach.<br>Local Expertise.<br><span class="gold-text">Every Shipment.</span></h1>
        <p class="lead">For four decades, mid-market manufacturers, distributors, and retailers have trusted J&A to move their freight across North America — with the accountability of a family business and the muscle of an enterprise network.</p>
        <div class="hero-actions">
          <a href="contact.html#quote" class="btn btn-gold">Get a Free Quote <span class="arrow">&rarr;</span></a>
          <a href="shippers.html" class="btn btn-ghost">Ship With Us</a>
        </div>
        <div class="hero-badges">
          <span class="badge">FMCSA Registered</span>
          <span class="badge">Surety Bonded</span>
          <span class="badge">MercuryGate TMS</span>
        </div>
      </div>
      <div>
        <img class="hero-40" src="assets/logo-40years.png" alt="J&A Freight Systems — 40 Years">
      </div>
    </div>
  </div>
  <div class="ticker-wrap">
    <div class="ticker" aria-hidden="true">
      <span><b>32+</b> States Served</span><span><b>200</b> Vetted Carrier Partners</span><span><b>1.5M+</b> Miles Coordinated Annually</span><span><b>97%</b> On-Time Delivery</span><span><b>40</b> Years of Service</span><span><b>10&ndash;35%</b> Avg. Freight Savings</span>
      <span><b>32+</b> States Served</span><span><b>200</b> Vetted Carrier Partners</span><span><b>1.5M+</b> Miles Coordinated Annually</span><span><b>97%</b> On-Time Delivery</span><span><b>40</b> Years of Service</span><span><b>10&ndash;35%</b> Avg. Freight Savings</span>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">What We Move</span>
      <h2>Streamlined logistics, on time, every time</h2>
      <p class="lead">One point of contact. One platform. Every mode your freight needs.</p>
    </div>
    <div class="grid-3">
      {card('truck','Full Truckload','Dry van, flatbed, and specialized FTL with vetted, fully insured carriers across all 48 contiguous states and cross-border lanes.', True)}
      {card('box','Less-Than-Truckload','Consolidated LTL programs that cut cost on partial loads without sacrificing transit time or visibility.', True)}
      {card('snow','Refrigerated','Temperature-controlled capacity for food, beverage, and pharma — monitored from pickup to proof of delivery.', True)}
      {card('anchor','Drayage & Intermodal','Port and rail moves coordinated end-to-end, so containers never sit accruing demurrage on your dime.', True)}
      {card('chart','Managed Transportation','We become your freight department: routing guides, carrier procurement, audit, and reporting under one roof.', True)}
      {card('eye','Real-Time Visibility','MercuryGate TMS tracking on every load. Know where your freight is before your customer asks.', True)}
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why J&A</span>
        <h2>A broker quotes rates. A partner solves problems.</h2>
        <p class="lead">Every member of our team pairs ongoing logistics education with seasoned transportation experts — because knowledge-driven logistics is the difference between a broker and a true strategic partner.</p>
        <ul class="checks">
          <li>Strict multi-point carrier vetting: safety, authority, and insurance verified before any carrier touches your freight</li>
          <li>Client relationships lasting over a decade — and growing</li>
          <li>Family-built accountability: a real person owns every load, start to finish</li>
          <li>Non-asset model means we work for your freight, not our trucks</li>
        </ul>
        <div class="hero-actions">
          <a href="about.html" class="btn btn-navy">Our Story <span class="arrow">&rarr;</span></a>
        </div>
      </div>
      <div class="visual reveal">{truck_svg()}</div>
    </div>
  </div>
</section>

<section class="stats">
  <div class="route-line" aria-hidden="true"></div>
  <div class="wrap">
    <div class="split" style="margin-bottom:58px">
      <div class="reveal on-dark">
        <span class="eyebrow">Industry Standards</span>
        <h2>Setting industry standards in freight solutions</h2>
        <p class="lead" style="color:rgba(255,255,255,.8)">Four decades of measurable performance. These aren't marketing numbers — they come straight out of our TMS, and we'll show you the reports.</p>
      </div>
      <div class="reveal container-visual">{container_svg()}</div>
    </div>
    <div class="stats-grid">
      <div class="stat reveal"><div class="num" data-count="2">0</div><div class="lbl">Avg. Days to Onboard</div></div>
      <div class="stat reveal"><div class="num" data-count="35" data-suffix="%">0</div><div class="lbl">Freight Savings Up To</div></div>
      <div class="stat reveal"><div class="num" data-count="97" data-suffix="%">0</div><div class="lbl">On-Time Delivery</div></div>
      <div class="stat reveal"><div class="num" data-count="5.0">0</div><div class="lbl">Avg. Client Rating</div></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">How It Works</span>
      <h2>Making logistics simple, secure, and efficient</h2>
    </div>
    <div class="steps">
      <div class="step reveal">
        <div class="no">01</div>
        <div><h3>Tell us about your freight</h3><p>Lanes, volumes, commodities, and pain points. A dedicated logistics expert — not a call center — scopes your needs within one business day.</p></div>
      </div>
      <div class="step reveal">
        <div class="no">02</div>
        <div><h3>We match vetted capacity</h3><p>Only FMCSA-compliant, fully insured carriers in our 200-strong network are matched to your load. Our multi-point verification runs on every carrier, every time.</p></div>
      </div>
      <div class="step reveal">
        <div class="no">03</div>
        <div><h3>Track it in real time</h3><p>Live visibility through MercuryGate TMS from pickup through delivery — with proactive check calls so surprises stay off your dock.</p></div>
      </div>
      <div class="step reveal">
        <div class="no">04</div>
        <div><h3>Settle clean, scale up</h3><p>Accurate invoicing, freight audit, and quarterly business reviews that turn shipping data into savings on the next quarter's lanes.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="block alt-gold">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Questions? We Have You Covered</span>
      <h2>Frequently asked questions</h2>
    </div>
    <div class="faq">
      <div class="faq-item reveal">
        <button class="faq-q">What does "non-asset-based 3PL" actually mean for me?</button>
        <div class="faq-a"><p>We don't own trucks, so we're never tempted to put your freight on equipment that doesn't fit. Instead, we match each load to the best vetted carrier in our network — which keeps rates competitive and service honest.</p></div>
      </div>
      <div class="faq-item reveal">
        <button class="faq-q">How do you vet your carriers?</button>
        <div class="faq-a"><p>Every carrier passes a multi-point verification covering FMCSA safety scores, operating authority, and active insurance before they ever touch a J&A load. We re-verify continuously — a carrier that lapses is pulled from the network automatically.</p></div>
      </div>
      <div class="faq-item reveal">
        <button class="faq-q">Can you handle temperature-controlled or specialized freight?</button>
        <div class="faq-a"><p>Yes. Refrigerated, flatbed, drayage, intermodal, and high-value freight are all core lanes for us. Tell us the commodity and we'll build the right program around it.</p></div>
      </div>
      <div class="faq-item reveal">
        <button class="faq-q">How fast can we start shipping?</button>
        <div class="faq-a"><p>Most new clients are onboarded and moving freight within two business days. Spot quotes turn around the same day.</p></div>
      </div>
      <div class="faq-item reveal">
        <button class="faq-q">Do you work with small shippers, or only large accounts?</button>
        <div class="faq-a"><p>Our sweet spot is mid-market manufacturers, distributors, and retailers — but if you ship regularly, we want the conversation. Many decade-long clients started with a single lane.</p></div>
      </div>
    </div>
  </div>
</section>
"""
)

# ============================================================ SHIPPERS
PAGES['shippers.html'] = dict(
 title="For Shippers | J&A Freight Systems",
 desc="Move freight with confidence, visibility, and control. FTL, LTL, refrigerated, drayage, intermodal, and managed transportation from a 40-year 3PL.",
 cta=dict(cta_h="Your freight deserves a strategist.",
          cta_p="Send us one lane that's been overpriced or underperforming. We'll quote it, explain the market behind the number, and let the work speak.",
          cta_href="contact.html#quote", cta_btn="Get a Quote"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">For Shippers</span>
        <h1>Move freight with <span class="gold-text">confidence, visibility, and control</span></h1>
        <p class="lead">Your freight. Our mission. Forty years of putting mid-market shippers first — with vetted capacity, honest rates, and a team that answers the phone.</p>
        <div class="hero-actions">
          <a href="contact.html#quote" class="btn btn-gold">Request a Quote <span class="arrow">&rarr;</span></a>
          <a href="technology.html" class="btn btn-ghost">See Our TMS</a>
        </div>
      </div>
      <div>
        <div class="visual" style="aspect-ratio:5/4">
          <svg viewBox="0 0 480 384" aria-hidden="true">
            <g fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1.5">
              <rect x="60" y="120" width="360" height="170" rx="10"/>
              <path d="M60 165h360M150 120v170M270 120v170"/>
            </g>
            <g fill="#FFC20D" font-family="Barlow Condensed" font-weight="700">
              <text x="105" y="150" text-anchor="middle" font-size="17" fill="rgba(255,255,255,.85)">LANE</text>
              <text x="210" y="150" text-anchor="middle" font-size="17" fill="rgba(255,255,255,.85)">STATUS</text>
              <text x="345" y="150" text-anchor="middle" font-size="17" fill="rgba(255,255,255,.85)">ETA</text>
              <text x="105" y="205" text-anchor="middle" font-size="16">CHI&rarr;DAL</text>
              <text x="105" y="250" text-anchor="middle" font-size="16">ORD&rarr;ATL</text>
              <circle cx="195" cy="199" r="5" fill="#5BE38A"/><text x="225" y="205" font-size="14" fill="rgba(255,255,255,.8)" text-anchor="middle">In Transit</text>
              <circle cx="195" cy="244" r="5" fill="#5BE38A"/><text x="225" y="250" font-size="14" fill="rgba(255,255,255,.8)" text-anchor="middle">Delivered</text>
              <text x="345" y="205" text-anchor="middle" font-size="16" fill="rgba(255,255,255,.85)">06:40</text>
              <text x="345" y="250" text-anchor="middle" font-size="16" fill="rgba(255,255,255,.85)">&#10003; POD</text>
            </g>
            {brand_lockup(265, 70, 0.85)}
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Tailored Freight Solutions</span>
      <h2>Every mode. One accountable partner.</h2>
    </div>
    <div class="grid-3">
      {card('truck','Full Truckload','Dedicated dry van, flatbed, and specialized equipment. Spot or contract — priced from real market data, not wishful thinking.')}
      {card('box','Less-Than-Truckload','Smart consolidation and carrier selection that protects transit times while trimming 10–35% off partial-load spend.')}
      {card('snow','Refrigerated Freight','Reefer capacity with continuous temperature monitoring for food, beverage, and pharmaceutical shippers.')}
      {card('anchor','Drayage','Port and ramp drayage timed to vessel and rail schedules, keeping containers moving and demurrage at zero.')}
      {card('route','Intermodal','Rail economics on long lanes without losing door-to-door accountability — we manage every handoff.')}
      {card('chart','Managed Transportation','Outsource the whole function: routing guides, RFPs, carrier scorecards, freight audit, and quarterly reviews.')}
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">What We Offer</span>
        <h2>Why partner with J&A Freight</h2>
        <ul class="checks">
          <li><strong>Vetted capacity, guaranteed.</strong> 200 carrier partners, every one FMCSA-compliant and fully insured before the first load.</li>
          <li><strong>Real-time visibility.</strong> MercuryGate TMS tracking and a shipper portal you can log into anytime.</li>
          <li><strong>One owner per load.</strong> A named logistics expert manages your freight — nights, weekends, and holidays included.</li>
          <li><strong>Data you can use.</strong> Lane-level reporting that turns your freight spend into a negotiating asset.</li>
          <li><strong>Decade-long relationships.</strong> Our average enterprise client tenure says more than any pitch deck.</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="form-card">
          <h3 style="margin-bottom:6px">Quick lane check</h3>
          <p style="color:var(--muted);font-size:.95rem;margin-bottom:22px">Drop in one lane — we'll respond with a real quote and the market context behind it.</p>
          <form data-demo>
            <div class="form-grid">
              <div><label for="s-origin">Origin</label><input id="s-origin" placeholder="Chicago, IL" required></div>
              <div><label for="s-dest">Destination</label><input id="s-dest" placeholder="Dallas, TX" required></div>
              <div><label for="s-mode">Mode</label>
                <select id="s-mode"><option>Full Truckload</option><option>LTL</option><option>Refrigerated</option><option>Drayage</option><option>Intermodal</option></select>
              </div>
              <div><label for="s-email">Work Email</label><input id="s-email" type="email" placeholder="you@company.com" required></div>
            </div>
            <div style="margin-top:18px"><button class="btn btn-gold" type="submit">Check This Lane <span class="arrow">&rarr;</span></button></div>
            <div class="form-success">Lane received. A logistics expert will reply with pricing within one business day.</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block dark">
  <div class="wrap">
    <div class="split">
      <div class="reveal on-dark">
        <span class="eyebrow">Shipper Portal</span>
        <h2>Log in to TMS — your freight, on demand</h2>
        <p class="lead">Quote, book, track, and pull PODs from the same MercuryGate platform our team runs on. Total transparency, zero phone tag.</p>
        <div class="hero-actions">
          <a href="technology.html" class="btn btn-gold">Explore the Platform <span class="arrow">&rarr;</span></a>
          <a href="contact.html" class="btn btn-ghost">Request Portal Access</a>
        </div>
      </div>
      <div class="grid-2 reveal">
        {card('eye','Live Tracking','GPS and ELD-fed location updates on every active shipment.')}
        {card('dollar','Instant Rating','Spot-market rates on demand across your saved lanes.')}
        {card('clock','Document Center','BOLs, PODs, and invoices — searchable, downloadable, audit-ready.')}
        {card('chart','Spend Analytics','Lane, carrier, and accessorial reporting refreshed daily.')}
      </div>
    </div>
  </div>
</section>
"""
)

# ============================================================ CARRIERS
PAGES['carriers.html'] = dict(
 title="For Carriers | J&A Freight Systems",
 desc="Consistent loads, fast pay, and real partnership. Join the J&A carrier network — quick pay options, 24/7 dispatch support, and freight that keeps your trucks moving.",
 cta=dict(cta_h="Good freight. Fast pay. No games.",
          cta_p="Set up takes minutes if your authority and insurance are current. Join 200 carriers who keep their trucks loaded with J&A.",
          cta_href="contact.html", cta_btn="Start Carrier Setup"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">For Carriers</span>
        <h1>Consistent loads. Fast pay. <span class="gold-text">Real partnership.</span></h1>
        <p class="lead">We move better, together. J&A treats carriers the way we'd want to be treated — accurate rate cons, no double-brokering, detention paid when it's owed, and a dispatcher who picks up at 2 a.m.</p>
        <div class="hero-actions">
          <a href="#setup" class="btn btn-gold">Drive With J&A <span class="arrow">&rarr;</span></a>
          <a href="#portal" class="btn btn-ghost">Carrier Portal Login</a>
        </div>
      </div>
      <div>
        <img class="hero-40" src="assets/logo-40years.png" alt="40 Years of J&A Freight Systems">
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Why Partner With J&A Freight</span>
      <h2>We keep trucks loaded and drivers respected</h2>
    </div>
    <div class="grid-3">
      {card('dollar','Quick Pay Options','Standard 30-day terms, or quick pay in as little as 2 business days. Clean paperwork, clean payments — every time.')}
      {card('route','Consistent Freight','Steady contract lanes out of the Midwest plus daily spot opportunities across 32+ states. Backhauls included.')}
      {card('phone','24/7 Dispatch Support','A real J&A dispatcher around the clock. Problems get solved at 2 a.m., not logged for Monday.')}
      {card('shield','No Double-Brokering','Your rate con is your rate con. We book direct with our shippers and never re-broker your load.')}
      {card('clock','Fast Check-In','Pre-built load packets, e-signatures, and digital PODs so your drivers spend hours driving, not waiting.')}
      {card('hand','Detention & Accessorials','Documented detention and accessorials are honored without a fight. Fair is fair.')}
    </div>
  </div>
</section>

<section class="block alt" id="setup">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Carrier Onboarding</span>
        <h2>From packet to first load in 24 hours</h2>
        <div class="steps">
          <div class="step"><div class="no">01</div><div><h3>Submit your info</h3><p>MC number, W-9, and certificate of insurance. Five minutes, tops.</p></div></div>
          <div class="step"><div class="no">02</div><div><h3>We verify</h3><p>Our multi-point check confirms FMCSA safety record, active authority, and insurance coverage. It protects you as much as our shippers.</p></div></div>
          <div class="step"><div class="no">03</div><div><h3>Start hauling</h3><p>Get matched to lanes that fit your equipment and home time. Most carriers see their first J&A load within a day of approval.</p></div></div>
        </div>
      </div>
      <div class="reveal">
        <div class="form-card">
          <h3 style="margin-bottom:6px">Carrier setup request</h3>
          <p style="color:var(--muted);font-size:.95rem;margin-bottom:22px">Our carrier relations team will send your full packet today.</p>
          <form data-demo>
            <div class="form-grid">
              <div><label for="c-company">Company Name</label><input id="c-company" required></div>
              <div><label for="c-mc">MC Number</label><input id="c-mc" placeholder="MC-000000" required></div>
              <div><label for="c-equip">Equipment Type</label>
                <select id="c-equip"><option>Dry Van</option><option>Reefer</option><option>Flatbed</option><option>Power Only</option><option>Drayage / Container</option></select>
              </div>
              <div><label for="c-trucks"># of Trucks</label><input id="c-trucks" type="number" min="1" placeholder="5"></div>
              <div><label for="c-email">Email</label><input id="c-email" type="email" required></div>
              <div><label for="c-phone">Phone</label><input id="c-phone" type="tel" required></div>
            </div>
            <div style="margin-top:18px"><button class="btn btn-gold" type="submit">Request Setup Packet <span class="arrow">&rarr;</span></button></div>
            <div class="form-success">Got it. Watch your inbox for the J&A carrier packet within one business day.</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block dark" id="portal">
  <div class="wrap">
    <div class="split">
      <div class="reveal on-dark">
        <span class="eyebrow">Carrier Portal</span>
        <h2>Log in to TMS — access your carrier portal</h2>
        <p class="lead">Available loads, rate confirmations, document upload, and payment status — all in one place, on any device.</p>
        <div class="hero-actions">
          <a href="contact.html" class="btn btn-gold">Request Login <span class="arrow">&rarr;</span></a>
        </div>
      </div>
      <div class="grid-2 reveal">
        {card('truck','Load Board','See and book J&A freight matched to your lanes and equipment.')}
        {card('dollar','Payment Status','Track every invoice from POD upload to payment — no phone calls needed.')}
        {card('box','Document Upload','Snap and submit PODs from the cab. Faster paperwork means faster pay.')}
        {card('chart','Performance Score','Your on-time record with us, transparent — top performers get first call on premium lanes.')}
      </div>
    </div>
  </div>
</section>
"""
)

# ============================================================ TECHNOLOGY
PAGES['technology.html'] = dict(
 title="Technology | J&A Freight Systems",
 desc="Technology-driven solutions for reliable deliveries — MercuryGate TMS, real-time tracking, EDI/API integrations, and analytics from a 40-year 3PL.",
 cta=dict(cta_h="See the platform on your own freight.",
          cta_p="Book a 20-minute walkthrough of MercuryGate TMS configured around your lanes — no slides, just the live system.",
          cta_href="contact.html", cta_btn="Book a Demo"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Technology</span>
        <h1>Forty years of instinct, <span class="gold-text">backed by enterprise software</span></h1>
        <p class="lead">Technology-driven solutions for reliable deliveries. We pair veteran logistics judgment with MercuryGate TMS — the same platform Fortune 500 freight departments run — so mid-market shippers get enterprise power without enterprise overhead.</p>
        <div class="hero-actions">
          <a href="contact.html" class="btn btn-gold">Request a Demo <span class="arrow">&rarr;</span></a>
        </div>
      </div>
      <div>
        <div class="visual" style="aspect-ratio:5/4">
          <svg viewBox="0 0 480 384" aria-hidden="true">
            <g fill="none" stroke="rgba(255,255,255,.18)" stroke-width="1.5">
              <rect x="50" y="60" width="380" height="240" rx="12"/>
              <path d="M50 100h380"/>
            </g>
            <circle cx="74" cy="80" r="5" fill="#FFC20D"/><circle cx="92" cy="80" r="5" fill="rgba(255,255,255,.4)"/><circle cx="110" cy="80" r="5" fill="rgba(255,255,255,.4)"/>
            <g fill="none" stroke="#FFC20D" stroke-width="2.5" stroke-linecap="round">
              <path d="M85 250 L150 200 L210 225 L280 160 L350 185 L400 130"/>
            </g>
            <g fill="#FFC20D"><circle cx="150" cy="200" r="4"/><circle cx="280" cy="160" r="4"/><circle cx="400" cy="130" r="4"/></g>
            {brand_lockup(262, 340, 0.62)}
            <text x="240" y="46" text-anchor="middle" font-family="Barlow Condensed" font-size="17" font-weight="700" fill="rgba(255,255,255,.7)" letter-spacing="4">MERCURYGATE TMS</text>
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">The Stack</span>
      <h2>Logistics with next-generation technologies</h2>
    </div>
    <div class="grid-3">
      {card('chart','MercuryGate TMS','Rating, booking, tendering, and settlement on a single enterprise platform — configured for your routing guide, not a generic template.', True)}
      {card('eye','Real-Time Tracking','ELD and GPS-fed location data on every load, with automated milestone alerts to you and your customers.', True)}
      {card('route','EDI & API Integrations','204/214/210 EDI or modern REST APIs into your ERP, WMS, or e-commerce stack. Your systems stay the source of truth.', True)}
      {card('dollar','Freight Audit & Pay','Automated invoice matching catches accessorial errors before they hit your AP — most clients recover 2–4% of spend.', True)}
      {card('shield','Continuous Carrier Monitoring','Authority, insurance, and safety scores re-verified automatically. A lapsed carrier is removed before the next tender.', True)}
      {card('box','Analytics & Reporting','Lane benchmarks, carrier scorecards, and spend trends delivered in quarterly business reviews — and on demand in the portal.', True)}
    </div>
  </div>
</section>

<section class="block alt-gold">
  <div class="wrap">
    <div class="split flip">
      <div class="reveal">
        <span class="eyebrow">Stay Ahead of the Curve</span>
        <h2>Tech is the tool. Accountability is the product.</h2>
        <p class="lead">Software doesn't answer the phone when a truck breaks down in a snowstorm. Our platform exists to make our people faster — every alert, exception, and data point routes to a named expert who owns the outcome.</p>
        <ul class="checks">
          <li>Exception alerts trigger human action within minutes, not the next business day</li>
          <li>Every client gets portal access plus a direct line — choose your channel</li>
          <li>Ongoing logistics education workshops keep our team sharper than the software</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="grid-2" style="gap:18px">
          <div class="card"><div class="stat" style="text-align:left"><div class="num" data-count="99.4" data-suffix="%" style="color:var(--navy)">0</div><div class="lbl" style="color:var(--muted)">Tracking Uptime</div></div></div>
          <div class="card"><div class="stat" style="text-align:left"><div class="num" data-count="15" data-suffix=" min" style="color:var(--navy)">0</div><div class="lbl" style="color:var(--muted)">Avg. Exception Response</div></div></div>
          <div class="card"><div class="stat" style="text-align:left"><div class="num" data-count="4" data-suffix="%" style="color:var(--navy)">0</div><div class="lbl" style="color:var(--muted)">Spend Recovered via Audit</div></div></div>
          <div class="card"><div class="stat" style="text-align:left"><div class="num" data-count="100" data-suffix="%" style="color:var(--navy)">0</div><div class="lbl" style="color:var(--muted)">Loads with Live Visibility</div></div></div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
)

# ============================================================ ABOUT
PAGES['about.html'] = dict(
 title="About Us | J&A Freight Systems",
 desc="Founded in 1986 in Chicago, J&A Freight Systems is a family-built, non-asset-based 3PL serving mid-market shippers across North America for 40 years.",
 cta=DEFAULT_CTA,
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">About Us</span>
        <h1>A family-built 3PL with <span class="gold-text">enterprise power</span></h1>
        <p class="lead">Founded in 1986 in Chicago, Illinois, J&A Freight Systems is a non-asset-based third-party logistics provider built on integrity, accountability, and relentless service.</p>
      </div>
      <div>
        <img class="hero-40" src="assets/logo-40years.png" alt="J&A Freight Systems — 40 Years">
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Our Story</span>
        <h2>Pioneering global logistics with a commitment to service</h2>
        <p class="lead">For nearly four decades, we've been the logistics backbone for mid-market manufacturers, distributors, and retailers shipping across North America. The names on the door still answer the phones — and our standards haven't moved an inch.</p>
        <p style="margin-top:16px;color:var(--muted)">We believe knowledge-driven logistics is the difference between a broker and a true strategic partner. Every member of our team pairs ongoing logistics education workshops with mentorship from seasoned transportation experts. Our client relationships — many lasting over a decade — are the proof.</p>
      </div>
      <div class="reveal">
        <div class="timeline">
          <div class="tl-item"><div class="yr">1986</div><p>J&A Freight Systems founded in Chicago with two desks, one phone line, and a promise: every load gets an owner.</p></div>
          <div class="tl-item"><div class="yr">1990s</div><p>Network expands across the Midwest; first decade-long client relationships take root.</p></div>
          <div class="tl-item"><div class="yr">2000s</div><p>Coverage grows to 32+ states; refrigerated and intermodal divisions launch.</p></div>
          <div class="tl-item"><div class="yr">2010s</div><p>MercuryGate TMS adopted, bringing enterprise visibility to every mid-market client.</p></div>
          <div class="tl-item"><div class="yr">2026</div><p>Celebrating 40 years — 200 vetted carrier partners, 1.5M+ miles coordinated annually, and the same family standards.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="stats">
  <div class="route-line" aria-hidden="true"></div>
  <div class="wrap">
    <div class="stats-grid">
      <div class="stat reveal"><div class="num" data-count="40">0</div><div class="lbl">Years in Business</div></div>
      <div class="stat reveal"><div class="num" data-count="32" data-suffix="+">0</div><div class="lbl">States Served</div></div>
      <div class="stat reveal"><div class="num" data-count="200">0</div><div class="lbl">Vetted Carrier Partners</div></div>
      <div class="stat reveal"><div class="num" data-count="1.5" data-suffix="M+">0</div><div class="lbl">Miles Coordinated / Year</div></div>
    </div>
  </div>
</section>

<section class="block alt-gold">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Our Values</span>
      <h2>What four decades taught us</h2>
    </div>
    <div class="grid-3">
      {card('shield','Integrity','We quote what the market bears and pay what we owe. The carrier vetting we run protects shippers and drivers alike — no exceptions, no shortcuts.')}
      {card('hand','Accountability',"Every load has a named owner. When something goes sideways at 2 a.m., you know exactly who's fixing it.")}
      {card('grad','Relentless Service','Ongoing logistics education for every team member, because a smarter team moves your freight better. Knowledge is the product.')}
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Leadership</span>
      <h2>Meet the experts behind every seamless shipment</h2>
    </div>
    <div class="team">
      <div class="member reveal"><div class="avatar">JS</div><h3>John Spencer</h3><div class="role">President</div></div>
      <div class="member reveal"><div class="avatar">MC</div><h3>Michael Chen</h3><div class="role">VP, Operations</div></div>
      <div class="member reveal"><div class="avatar">SM</div><h3>Sophia Martinez</h3><div class="role">Director, Carrier Relations</div></div>
      <div class="member reveal"><div class="avatar">RC</div><h3>Robert Clemens</h3><div class="role">Director, Client Services</div></div>
      <div class="member reveal"><div class="avatar">LW</div><h3>Liam Wright</h3><div class="role">Technology Lead</div></div>
      <div class="member reveal"><div class="avatar">ER</div><h3>Emily Robinson</h3><div class="role">Pricing & Analytics</div></div>
      <div class="member reveal"><div class="avatar">MC</div><h3>Mason Carter</h3><div class="role">Refrigerated Division</div></div>
      <div class="member reveal"><div class="avatar">AT</div><h3>Ava Thompson</h3><div class="role">Drayage & Intermodal</div></div>
    </div>
  </div>
</section>

<section class="block dark">
  <div class="wrap center">
    <div class="sec-head center reveal on-dark">
      <span class="eyebrow">Compliance</span>
      <h2>Credentials that travel with every load</h2>
      <p class="lead">Before any carrier touches your freight, they pass our rigorous multi-point safety, authority, and insurance verification process.</p>
    </div>
    <div class="hero-badges reveal" style="justify-content:center">
      <span class="badge">FMCSA Registered</span>
      <span class="badge">Surety Bonded</span>
      <span class="badge">Fully Insured Network</span>
      <span class="badge">MercuryGate TMS Certified</span>
    </div>
  </div>
</section>
"""
)

# ============================================================ CAREERS
PAGES['careers.html'] = dict(
 title="Careers — Join J&A | J&A Freight Systems",
 desc="Unlock endless opportunities in logistics. Build your career at J&A Freight Systems — a 40-year family-built 3PL in Chicago with ongoing logistics education for every team member.",
 cta=dict(cta_h="Ready to take your career to new heights?",
          cta_p="Seventeen open seats and a 40-year track record of promoting from within. Your move.",
          cta_href="positions.html", cta_btn="See Open Positions"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Join J&A</span>
        <h1>Unlock endless opportunities <span class="gold-text">& shape your career</span></h1>
        <p class="lead">Logistics is the industry that moves every other industry. Start your journey at a company where every team member trains alongside seasoned transportation experts — and where 40 years of growth means real room to climb.</p>
        <div class="hero-actions">
          <a href="positions.html" class="btn btn-gold">View Open Positions <span class="arrow">&rarr;</span></a>
          <a href="#apply" class="btn btn-ghost">Apply Now</a>
        </div>
      </div>
      <div>
        <div class="visual" style="aspect-ratio:5/4">
          <svg viewBox="0 0 480 384" aria-hidden="true">
            <g fill="none" stroke="rgba(255,255,255,.18)" stroke-width="1.5">
              <path d="M70 320 L150 250 L230 270 L310 180 L410 80" stroke-width="2.5" stroke="#FFC20D"/>
            </g>
            <g fill="#fff">
              <circle cx="70" cy="320" r="6"/><circle cx="150" cy="250" r="6"/><circle cx="230" cy="270" r="6"/><circle cx="310" cy="180" r="6"/>
            </g>
            <path d="M410 50 l8 22 22 8 -22 8 -8 22 -8 -22 -22 -8 22 -8z" fill="#FFC20D"/>
            <text x="240" y="332" text-anchor="middle" font-family="Barlow Condensed" font-size="20" font-weight="700" fill="rgba(255,255,255,.85)" letter-spacing="3">YOUR NEXT MOVE</text>
            {brand_lockup(262, 366, 0.5)}
          </svg>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Why Work Here</span>
      <h2>Discover your next career move</h2>
    </div>
    <div class="grid-3">
      {card('grad','Paid Logistics Education',"Ongoing workshops, industry certifications, and one-on-one mentorship with veterans who've seen every freight market since 1986.")}
      {card('chart','Promote-From-Within Culture','Most of our leadership started on the dispatch floor. Performance gets noticed fast in a family-built company.')}
      {card('dollar','Competitive Comp + Commission','Base salary, uncapped commission tracks for sales roles, 401(k) match, and full health coverage.')}
      {card('hand','Real Responsibility, Day One',"You'll own loads, clients, and outcomes early — with experienced backup one desk away.")}
      {card('clock','Chicago HQ, Hybrid Options','Modern office near the city, with hybrid flexibility for established team members.')}
      {card('shield',"Stability That's Rare","Forty years, zero layoff rounds. We grow steadily and hire deliberately.")}
    </div>
  </div>
</section>

<section class="block alt-gold" id="apply">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Apply Today</span>
        <h2>Ready to take your career to new heights?</h2>
        <p class="lead">Don't see your exact role on the <a href="positions.html" style="color:var(--navy);font-weight:600;text-decoration:underline">open positions</a> board? Send a general application — we hire great people first and find the seat second.</p>
        <ul class="checks">
          <li>Applications reviewed within 3 business days</li>
          <li>Two-round process: phone screen, then an in-person with your future team</li>
          <li>No ghosting — every applicant gets an answer</li>
        </ul>
      </div>
      <div class="reveal">
        <div class="form-card">
          <h3 style="margin-bottom:22px">General application</h3>
          <form data-demo>
            <div class="form-grid">
              <div><label for="a-first">First Name</label><input id="a-first" required></div>
              <div><label for="a-last">Last Name</label><input id="a-last" required></div>
              <div><label for="a-email">Email</label><input id="a-email" type="email" required></div>
              <div><label for="a-phone">Phone</label><input id="a-phone" type="tel"></div>
              <div class="full"><label for="a-role">Area of Interest</label>
                <select id="a-role"><option>Operations / Dispatch</option><option>Sales & Account Management</option><option>Pricing & Analytics</option><option>Compliance</option><option>Technology</option><option>Other</option></select>
              </div>
              <div class="full"><label for="a-msg">Tell us about yourself</label><textarea id="a-msg" placeholder="Experience, what you're looking for, and why logistics."></textarea></div>
            </div>
            <div style="margin-top:18px"><button class="btn btn-gold" type="submit">Submit Application <span class="arrow">&rarr;</span></button></div>
            <p class="form-note">Attach your resume in the follow-up email you'll receive after submitting.</p>
            <div class="form-success">Application received. Expect a response within 3 business days.</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>
"""
)

# ============================================================ POSITIONS
POSITIONS = [
 ("Logistics Coordinator","ops","Full-Time","Chicago, IL (Hybrid)","Own a book of daily loads end-to-end: tender, track, troubleshoot, and deliver. The classic launchpad role — most of our leadership started here."),
 ("Senior Logistics Coordinator","ops","Full-Time","Chicago, IL (Hybrid)","Run high-volume accounts and mentor new coordinators while managing escalations across modes."),
 ("Night Dispatch Specialist","ops","Full-Time","Remote (US)","Keep freight moving overnight — track-and-trace, carrier check calls, and exception management for active loads."),
 ("Track & Trace Associate","ops","Full-Time","Chicago, IL","Monitor in-transit shipments in MercuryGate TMS and trigger proactive alerts before issues reach the customer."),
 ("Freight Sales Executive","sales","Full-Time · Commission","Chicago, IL (Hybrid)","Hunt and close mid-market shipper accounts. Uncapped commission, warm brand recognition, and 40 years of references behind you."),
 ("Account Manager, Enterprise","sales","Full-Time","Chicago, IL","Grow and retain decade-long client relationships through QBRs, lane expansion, and white-glove service."),
 ("Inside Sales Representative","sales","Full-Time · Commission","Chicago, IL","Qualify inbound leads and book first lanes. Clear promotion track to Freight Sales Executive within 12–18 months."),
 ("Carrier Sales Representative","sales","Full-Time · Commission","Chicago, IL (Hybrid)","Build carrier relationships and cover freight at market-smart rates. Negotiators thrive here."),
 ("Warehouse Operations Manager","ops","Full-Time","Chicago, IL (On-site)","Oversee cross-dock and consolidation operations, staffing, and safety for our Chicago facility."),
 ("Customs Compliance Specialist","compliance","Full-Time","Chicago, IL (Hybrid)","Manage cross-border documentation, HTS classification support, and broker coordination for US–Canada–Mexico lanes."),
 ("Carrier Compliance Analyst","compliance","Full-Time","Remote (US)","Run our multi-point carrier vetting program: FMCSA scores, authority, insurance monitoring, and network audits."),
 ("Freight Pricing Analyst","analytics","Full-Time","Chicago, IL (Hybrid)","Build lane pricing models from market data and win-rate analytics. Excel/SQL fluency required; Python a plus."),
 ("Senior Pricing Analyst, RFP","analytics","Full-Time","Chicago, IL (Hybrid)","Lead annual RFP season — bid strategy, routing guide design, and margin modeling on enterprise accounts."),
 ("Business Intelligence Analyst","analytics","Full-Time","Remote (US)","Turn TMS data into carrier scorecards, client dashboards, and quarterly business review decks."),
 ("TMS Administrator","tech","Full-Time","Chicago, IL (Hybrid)","Configure and optimize MercuryGate: workflows, rating engines, user management, and integration health."),
 ("Integrations Engineer, EDI/API","tech","Full-Time","Remote (US)","Build and maintain EDI 204/214/210 and REST integrations between client ERPs and our TMS."),
 ("Marketing & Content Specialist","sales","Full-Time","Chicago, IL (Hybrid)","Own the J&A brand: market briefs, case studies, web content, and our 40th-anniversary campaign."),
]
pin_svg = IC['pin']; clock_svg = IC['clock']
pos_html = "\n".join(f"""
<article class="pos reveal" data-dept="{d}">
  <div>
    <h3>{t}</h3>
    <div class="meta"><span>{clock_svg}{typ}</span><span>{pin_svg}{loc}</span></div>
    <p class="desc">{desc}</p>
  </div>
  <a class="btn btn-ghost-navy" href="careers.html#apply">Apply <span class="arrow">&rarr;</span></a>
</article>""" for t,d,typ,loc,desc in POSITIONS)

PAGES['positions.html'] = dict(
 title="Open Positions | J&A Freight Systems",
 desc="We currently have 17 open positions across operations, sales, compliance, analytics, and technology at J&A Freight Systems in Chicago.",
 cta=dict(cta_h="Don't see your seat?",
          cta_p="We hire great people first and find the role second. Send a general application and tell us what you'd bring.",
          cta_href="careers.html#apply", cta_btn="General Application"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <span class="eyebrow">Careers</span>
    <h1>We currently have <span class="gold-text" id="pos-count">17</span> open positions</h1>
    <p class="lead">Join our growing team. Every role comes with paid logistics education, veteran mentorship, and a 40-year company behind you.</p>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <div class="pos-filters reveal" role="tablist" aria-label="Filter positions by department">
      <button class="chip active" data-filter="all">All Departments</button>
      <button class="chip" data-filter="ops">Operations</button>
      <button class="chip" data-filter="sales">Sales & Marketing</button>
      <button class="chip" data-filter="compliance">Compliance</button>
      <button class="chip" data-filter="analytics">Pricing & Analytics</button>
      <button class="chip" data-filter="tech">Technology</button>
    </div>
    {pos_html}
  </div>
</section>
"""
)

# ============================================================ CONTACT
PAGES['contact.html'] = dict(
 title="Contact Us | J&A Freight Systems",
 desc="Reach out to our experts for tailored logistics solutions. Quotes, carrier setup, portal access, and general inquiries — answered within one business day.",
 cta=dict(cta_h="Prefer to just call?",
          cta_p="A logistics expert — not a phone tree — picks up Monday through Friday, 7:00 to 19:00 Central. After hours, dispatch has you covered.",
          cta_href="tel:+17735550140", cta_btn="(773) 555-0140"),
 body=f"""
<section class="hero sub">
  {routemap()}
  <div class="wrap">
    <span class="eyebrow">Contact Us</span>
    <h1>Reach out to our experts for <span class="gold-text">tailored solutions</span></h1>
    <p class="lead">Let's chat. Quotes come back same day; everything else within one business day. No phone trees, no ticket queues.</p>
  </div>
</section>

<section class="block" id="quote">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <div class="card" style="padding:34px">
          <div class="c-line">
            <div class="icon">{IC['phone']}</div>
            <div><strong>Phone</strong><span><a href="tel:+17735550140">(773) 555-0140</a> &middot; Mon–Fri 7:00–19:00 CT<br>24/7 dispatch for active loads</span></div>
          </div>
          <div class="c-line">
            <div class="icon">{IC['mail']}</div>
            <div><strong>Email</strong><span><a href="mailto:quotes@jafreightsystems.com">quotes@jafreightsystems.com</a> — pricing<br><a href="mailto:carriers@jafreightsystems.com">carriers@jafreightsystems.com</a> — carrier setup<br><a href="mailto:dispatch@jafreightsystems.com">dispatch@jafreightsystems.com</a> — active loads</span></div>
          </div>
          <div class="c-line">
            <div class="icon">{IC['pin']}</div>
            <div><strong>Headquarters</strong><span>J&A Freight Systems, Inc.<br>4400 W. Logistics Parkway, Suite 200<br>Chicago, IL 60632</span></div>
          </div>
          <div class="c-line">
            <div class="icon">{IC['shield']}</div>
            <div><strong>Credentials</strong><span>FMCSA Registered &middot; Surety Bonded<br>MC# 123456 &middot; DOT# 7891011</span></div>
          </div>
        </div>
      </div>
      <div class="reveal">
        <div class="form-card">
          <h3 style="margin-bottom:6px">Send us a message</h3>
          <p style="color:var(--muted);font-size:.95rem;margin-bottom:22px">Quote requests include lane and commodity details for fastest turnaround.</p>
          <form data-demo>
            <div class="form-grid">
              <div><label for="ct-name">Full Name</label><input id="ct-name" required></div>
              <div><label for="ct-company">Company</label><input id="ct-company"></div>
              <div><label for="ct-email">Email</label><input id="ct-email" type="email" required></div>
              <div><label for="ct-phone">Phone</label><input id="ct-phone" type="tel"></div>
              <div class="full"><label for="ct-topic">I'm reaching out about</label>
                <select id="ct-topic"><option>Freight quote</option><option>Managed transportation</option><option>Carrier setup</option><option>Portal access</option><option>Careers</option><option>Something else</option></select>
              </div>
              <div class="full"><label for="ct-msg">Message</label><textarea id="ct-msg" placeholder="Origin/destination, commodity, frequency — or just say hello." required></textarea></div>
            </div>
            <div style="margin-top:18px"><button class="btn btn-gold" type="submit">Send Message <span class="arrow">&rarr;</span></button></div>
            <div class="form-success">Message sent. A J&A expert will reply within one business day.</div>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block alt tight">
  <div class="wrap">
    <div class="visual reveal" style="aspect-ratio:21/7">
      <svg viewBox="0 0 1050 350" aria-hidden="true">
        <g fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1">
          <path d="M0 70h1050M0 140h1050M0 210h1050M0 280h1050M150 0v350M300 0v350M450 0v350M600 0v350M750 0v350M900 0v350"/>
        </g>
        <g fill="none" stroke="rgba(255,255,255,.25)" stroke-width="2">
          <path d="M200 300 Q400 180 525 175 T880 90" stroke-dasharray="6 8"/>
        </g>
        {compass(525, 150, 0.5)}
        <text x="525" y="248" text-anchor="middle" font-family="Barlow Condensed" font-size="24" font-weight="700" fill="rgba(255,255,255,.9)" letter-spacing="4">CHICAGO, ILLINOIS — HQ</text>
        <text x="525" y="278" text-anchor="middle" font-family="Barlow Condensed" font-size="16" font-weight="600" fill="#FFC20D" letter-spacing="5">J&amp;A LOGISTICS &middot; SINCE 1986</text>
      </svg>
    </div>
  </div>
</section>
"""
)

# ============================================================ write files
OUT = '/home/claude/ja-freight'
for fname, page in PAGES.items():
    html = HEAD.format(title=page['title'], desc=page['desc']) + page['body'] + FOOTER.format(**page['cta'])
    with open(os.path.join(OUT, fname), 'w') as f:
        f.write(html)
    print(f"wrote {fname} ({len(html)} bytes)")
