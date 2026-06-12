#!/usr/bin/env python3
"""Patch v2: brand every visual with the J&A compass + 'J&A LOGISTICS', vary section backgrounds."""
import re

src = open('build.py').read()

# ---------- 1. Helpers: compass logo + branded truck + container ----------
helpers = '''
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
'''
src = src.replace('def card(icon, h, p, gold=False):', helpers + '\ndef card(icon, h, p, gold=False):')

# ---------- 2. Home: replace split visual with branded truck ----------
src = re.sub(
    r'<div class="visual reveal">\s*<svg viewBox="0 0 480 360".*?</svg>\s*</div>',
    '<div class="visual reveal">{TRUCK}</div>'.replace('{TRUCK}', '{truck_svg()}'),
    src, count=1, flags=re.S)

# ---------- 3. Home: replace stats band with container + stats (original style) ----------
old_stats_home = '''<section class="stats">
  <div class="route-line" aria-hidden="true"></div>
  <div class="wrap">
    <div class="stats-grid">
      <div class="stat reveal"><div class="num" data-count="2">0</div><div class="lbl">Avg. Days to Onboard</div></div>'''
new_stats_home = '''<section class="stats">
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
      <div class="stat reveal"><div class="num" data-count="2">0</div><div class="lbl">Avg. Days to Onboard</div></div>'''
src = src.replace(old_stats_home, new_stats_home)

# ---------- 4. Background variety ----------
# Home: FAQ section gets warm gold tint instead of repeating gray
src = src.replace('''<section class="block alt">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Questions? We Have You Covered</span>''',
'''<section class="block alt-gold">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Questions? We Have You Covered</span>''')

# Careers: apply section warm tint (was gray right after white)
src = src.replace('<section class="block alt" id="apply">', '<section class="block alt-gold" id="apply">')

# Shippers: services white -> why/form section navy-tint stays alt; portal dark; ok.
# Technology: alt section -> alt-gold for variety
src = src.replace('''<section class="block alt">
  <div class="wrap">
    <div class="split flip">''',
'''<section class="block alt-gold">
  <div class="wrap">
    <div class="split flip">''')

# About: values section gold tint (sits between stats-dark and white team)
src = src.replace('''<section class="block alt">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Our Values</span>''',
'''<section class="block alt-gold">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Our Values</span>''')

# ---------- 5. Brand the shippers hero visual ----------
src = src.replace(
'''            <path d="M240 40 l7 20 20 7 -20 7 -7 20 -7 -20 -20 -7 20 -7z" fill="#fff" opacity=".9"/>''',
'''            {brand_lockup(265, 70, 0.85)}''')

# ---------- 6. Brand the technology dashboard visual ----------
src = src.replace(
'''            <text x="240" y="340" text-anchor="middle" font-family="Barlow Condensed" font-size="20" font-weight="700" fill="rgba(255,255,255,.85)" letter-spacing="3">MERCURYGATE TMS</text>''',
'''            {brand_lockup(262, 340, 0.62)}
            <text x="240" y="46" text-anchor="middle" font-family="Barlow Condensed" font-size="17" font-weight="700" fill="rgba(255,255,255,.7)" letter-spacing="4">MERCURYGATE TMS</text>''')

# ---------- 7. Brand the careers visual ----------
src = src.replace(
'''            <text x="240" y="360" text-anchor="middle" font-family="Barlow Condensed" font-size="20" font-weight="700" fill="rgba(255,255,255,.85)" letter-spacing="3">YOUR NEXT MOVE</text>''',
'''            <text x="240" y="332" text-anchor="middle" font-family="Barlow Condensed" font-size="20" font-weight="700" fill="rgba(255,255,255,.85)" letter-spacing="3">YOUR NEXT MOVE</text>
            {brand_lockup(262, 366, 0.5)}''')

# ---------- 8. Brand the contact map ----------
src = src.replace(
'''        <path d="M525 130 l9 26 26 9 -26 9 -9 26 -9 -26 -26 -9 26 -9z" fill="#FFC20D"/>
        <text x="525" y="240" text-anchor="middle" font-family="Barlow Condensed" font-size="24" font-weight="700" fill="rgba(255,255,255,.9)" letter-spacing="4">CHICAGO, ILLINOIS — HQ</text>''',
'''        {compass(525, 150, 0.5)}
        <text x="525" y="248" text-anchor="middle" font-family="Barlow Condensed" font-size="24" font-weight="700" fill="rgba(255,255,255,.9)" letter-spacing="4">CHICAGO, ILLINOIS — HQ</text>
        <text x="525" y="278" text-anchor="middle" font-family="Barlow Condensed" font-size="16" font-weight="600" fill="#FFC20D" letter-spacing="5">J&amp;A LOGISTICS &middot; SINCE 1986</text>''')

# ---------- 9. Brand the home why-section visual already replaced by truck; also brand carriers grid? portal fine.
open('build.py','w').write(src)
print("build.py patched")

# ---------- 10. CSS additions ----------
css = open('css/styles.css').read()
css = css.replace('section.alt{background:var(--paper)}',
'''section.alt{background:#F1F5FA}
section.alt-gold{background:linear-gradient(180deg,#FFF9E8,#FFF4D6)}
section.alt-gold .card,section.alt-gold .faq-item,section.alt-gold .form-card{border-color:#F0E3B8}
.container-visual svg{width:100%;max-width:540px;margin:0 auto;display:block}''')
# distinct paper tone tweak + faq on gold bg
css += '''
/* v2: stronger section rhythm */
section.block + section.block:not(.alt):not(.alt-gold):not(.dark){border-top:1px solid var(--line)}
.stats .split h2{font-size:clamp(1.8rem,3.4vw,2.6rem)}
.stats .container-visual{filter:drop-shadow(0 24px 40px rgba(0,0,0,.35))}
'''
open('css/styles.css','w').write(css)
print("css patched")
