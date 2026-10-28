"""Neon-sign section titles. Letters are converted to outlines (no font file is
shipped), drawn as glowing tubes on a dark backplate: each tube draws itself on,
powers up, then flickers now and then.

Usage: neon_titles.py <out-dir> <style>=<font-file> [...]
Writes <out-dir>/title-<style>-<slug>.svg
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

W, H = 1280, 150
TITLES = {"daily-life": "day to day", "my-city": "a ride through my life", "thanks": "see you"}
# tube colour, outer glow colour, per style (all golden-hour neon)
PALETTE = {
    "kangu": ("#FFE3F1", "#FF4FA3"),
    "seabox": ("#FFF1D6", "#FF9A2E"),
    "kregan": ("#FFE6D8", "#FF6A4D"),
    "ogelo": ("#FFF6CC", "#FFC233"),
}


def outline(font, text, size):
    """Glyph outlines laid out with the font's own advances; returns (paths, width, ascent)."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    k = size / upm
    x, paths = 0.0, []
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord(ch.upper()))
        if g is None:
            x += size * 0.3
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        d = pen.getCommands()
        if d:
            paths.append(d)
        x += gs[g].width * k
    asc = font["hhea"].ascent * k
    return paths, x, asc


def neon_svg(font, style, text):
    tube, glow = PALETTE[style]
    size = 86 if len(text) < 14 else 66
    paths, width, asc = outline(font, text, size)
    if width > W - 160:
        size *= (W - 160) / width
        paths, width, asc = outline(font, text, size)
    x0 = (W - width) / 2
    base = H / 2 + asc * 0.36
    plate_w = width + 90
    letters = []
    for i, d in enumerate(paths):
        t = 0.3 + i * 0.11
        letters.append(f'<path d="{d}" pathLength="1" class="tube" style="animation-delay:{t:.2f}s,{t + .55:.2f}s,{t + 3 + (i % 5) * .7:.2f}s"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(text)}">
  <defs>
    <filter id="glow" x="-10%" y="-60%" width="120%" height="220%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="wide"/>
      <feColorMatrix in="wide" type="matrix" values="0 0 0 0 {int(glow[1:3], 16) / 255:.3f}  0 0 0 0 {int(glow[3:5], 16) / 255:.3f}  0 0 0 0 {int(glow[5:7], 16) / 255:.3f}  0 0 0 1.1 0" result="wideC"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="2.4" result="near"/>
      <feColorMatrix in="near" type="matrix" values="0 0 0 0 {int(glow[1:3], 16) / 255:.3f}  0 0 0 0 {int(glow[3:5], 16) / 255:.3f}  0 0 0 0 {int(glow[5:7], 16) / 255:.3f}  0 0 0 1.6 0" result="nearC"/>
      <feMerge><feMergeNode in="wideC"/><feMergeNode in="nearC"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="haze"><stop offset="0" stop-color="{glow}" stop-opacity=".28"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
    <linearGradient id="plate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A1520"/><stop offset="1" stop-color="#0E0B12"/></linearGradient>
    <style>
      .tube{{fill:none;stroke:{tube};stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round;
             stroke-dasharray:1;stroke-dashoffset:1;opacity:.35;
             animation:draw .55s ease-out forwards,power .4s steps(3,end) forwards,flick 8s steps(1) infinite}}
      @keyframes draw{{to{{stroke-dashoffset:0}}}}
      @keyframes power{{0%{{opacity:.35}}40%{{opacity:1}}60%{{opacity:.5}}100%{{opacity:1}}}}
      @keyframes flick{{0%,94%,100%{{opacity:1}}95%{{opacity:.4}}96.5%{{opacity:1}}97.5%{{opacity:.55}}}}
      .halo{{opacity:0;animation:halo 1.2s ease-out {0.3 + len(paths) * 0.11:.2f}s forwards}}
      @keyframes halo{{to{{opacity:1}}}}
      @media (prefers-reduced-motion:reduce){{.tube{{animation:none;stroke-dashoffset:0;opacity:1}}.halo{{animation:none;opacity:1}}}}
    </style>
  </defs>
  <rect x="{(W - plate_w) / 2:.1f}" y="14" width="{plate_w:.1f}" height="{H - 28}" rx="16" fill="url(#plate)" stroke="#2C2433" stroke-width="1.5"/>
  {"".join(f'<circle cx="{cx:.1f}" cy="{cy}" r="3" fill="#3A3240"/>' for cx in ((W - plate_w) / 2 + 14, (W + plate_w) / 2 - 14) for cy in (28, H - 28))}
  <ellipse class="halo" cx="{W / 2}" cy="{H / 2}" rx="{width / 2 + 30:.1f}" ry="46" fill="url(#haze)"/>
  <g transform="translate({x0:.1f} {base:.1f})" filter="url(#glow)">{"".join(letters)}</g>
</svg>
'''


out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for arg in sys.argv[2:]:
    style, file = arg.split("=", 1)
    font = TTFont(file)
    for slug, text in TITLES.items():
        (out / f"title-{style}-{slug}.svg").write_text(neon_svg(font, style, text), encoding="utf-8")
print("ok")
