"""'Thanks for stopping by': golden hour at El Médano. Montaña Roja on its
flat spit across a calm sea, boats moored in front, the low sun to the left,
and a paraglider gliding smoothly across towing a rippling banner, mirrored
softly in the water.
"""
import math
import random

W, H = 1280, 460
HZ = 288                       # horizon
LOOP = 28.0
rng = random.Random(3)
css = []


def kf(name, frames, dur=LOOP, ease="linear", extra=""):
    body = "".join(f"{t / dur * 100:.2f}%{{{d}}}" for t, d in frames)
    css.append(f".{name}{{animation:{name} {dur}s {ease} infinite;{extra}}}@keyframes {name}{{{body}}}")


SUNX, SUNY = 250, HZ - 58
clouds = "".join(f'<path d="M{x} {y} q{w * .2:.0f} -{h} {w * .45:.0f} -{h * .4:.0f} q{w * .2:.0f} -{h * .8:.0f} {w * .4:.0f} 0 q{w * .15:.0f} 0 {w * .15:.0f} {h * .4:.0f}Z" fill="#FFE2B0" opacity="{o}" class="cloud"/>'
                 for x, y, w, h, o in ((80, 96, 180, 14, .45), (900, 70, 240, 18, .5), (1100, 130, 150, 12, .4)))

# ── Montaña Roja on its spit; the low sun (left) lights the west flank ────────
ROJA_PATH = (f"M330 {HZ} C340 {HZ - 12} 356 {HZ - 26} 380 {HZ - 30} C404 {HZ - 32} 424 {HZ - 20} 440 {HZ - 10} L560 {HZ - 8} "
             f"C600 {HZ - 30} 650 {HZ - 72} 700 {HZ - 104} C716 {HZ - 114} 728 {HZ - 118} 740 {HZ - 118} C756 {HZ - 116} 776 {HZ - 104} 810 {HZ - 82} "
             f"C860 {HZ - 52} 930 {HZ - 24} 1010 {HZ - 12} L1150 {HZ - 6} C1190 {HZ - 4} 1230 {HZ - 2} {W} {HZ} Z")
roja = (f'<path d="{ROJA_PATH}" fill="url(#rojaG)"/>'
        f'<path d="M330 {HZ} C340 {HZ - 12} 356 {HZ - 26} 380 {HZ - 30} C404 {HZ - 32} 424 {HZ - 20} 440 {HZ - 10}" fill="none" stroke="#FFC48A" stroke-width="2" opacity=".55"/>'
        f'<path d="M560 {HZ - 8} C600 {HZ - 30} 650 {HZ - 72} 700 {HZ - 104} C716 {HZ - 114} 728 {HZ - 118} 740 {HZ - 118}" fill="none" stroke="#FFB27A" stroke-width="2.5" opacity=".75"/>'
        f'<path d="M600 {HZ - 34} C640 {HZ - 40} 676 {HZ - 52} 700 {HZ - 64} C716 {HZ - 76} 724 {HZ - 96} 732 {HZ - 112}" fill="none" stroke="#E6A47E" stroke-width="1.2" opacity=".6" stroke-dasharray="3 3"/>'
        f'<path d="M440 {HZ - 10} L1150 {HZ - 6} C1190 {HZ - 4} 1230 {HZ - 2} {W} {HZ} H330Z" fill="#D8A878" opacity=".85"/>'
        f'<path d="M330 {HZ} H{W}" stroke="#FFE2B8" stroke-width="1.2" opacity=".6"/>')

# ── sea: sun path, sparkles, moored boats (each with its own reflection) ──────
sunpath = "".join(f'<rect x="{SUNX - w / 2 + rng.randint(-10, 10)}" y="{y}" width="{w}" height="2.4" rx="1.2" fill="#FFE29A" opacity="{o}" class="glint" style="animation-delay:{rng.random() * 2.4:.2f}s"/>'
                  for y, w, o in ((294, 130, .85), (302, 96, .75), (311, 150, .65), (321, 86, .6), (332, 120, .5), (345, 76, .45), (360, 104, .4), (377, 64, .32), (396, 90, .28), (418, 58, .22), (442, 80, .2)))
sparkle = "".join(f'<circle cx="{rng.randint(10, W - 10)}" cy="{rng.randint(HZ + 8, H - 6)}" r="{rng.choice([.8, 1, 1.2])}" fill="#FFF4D6" class="spark" style="animation-delay:{rng.random() * 3:.2f}s"/>' for _ in range(46))
waves = "".join(f'<rect x="{rng.randint(0, W - 80)}" y="{rng.randint(HZ + 14, H - 8)}" width="{rng.randint(24, 80)}" height="1.4" rx=".7" fill="#1E5266" opacity=".35"/>' for _ in range(34))


def mboat(x, y, s, cover):
    body = ('<path d="M-16 0 L16 0 L12 5 L-12 5Z" fill="#F4F1EA"/><path d="M-16 0 H16" stroke="#3A4A55" stroke-width="1"/>'
            + ('<path d="M-10 0 Q0 -9 10 0Z" fill="#C9C2B4"/>' if cover else '<rect x="-4" y="-5" width="8" height="5" rx="1" fill="#F4F1EA"/><rect x="-2" y="-4" width="4" height="2" fill="#3A4A55"/>'))
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="moor" style="animation-delay:{rng.random() * 3:.2f}s">{body}'
            f'<g transform="translate(0 10) scale(1 -1)" opacity=".25">{body}</g></g></g>')


boats = "".join(mboat(x, y, s, c) for x, y, s, c in ((300, HZ + 20, .7, 0), (420, HZ + 26, .85, 1), (540, HZ + 18, .6, 0), (610, HZ + 30, .9, 0), (720, HZ + 22, .65, 1), (790, HZ + 34, .8, 0)))
buoys = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#E8513F" class="moor"/>' for x, y in ((360, HZ + 30), (500, HZ + 36), (680, HZ + 40), (860, HZ + 28)))
sailboat = f'''<g class="boat"><g transform="translate(980 {HZ + 16})"><g class="moor">
  <path d="M-22 0 L22 0 L17 6 L-17 6Z" fill="#F4F1EA"/><path d="M0 0 V-40" stroke="#3A3036" stroke-width="1.4"/>
  <path d="M1 -38 L18 -4 H1Z" fill="#FFF7EC"/><path d="M-1 -32 L-14 -4 H-1Z" fill="#FFE6C8"/>
  <g transform="translate(0 12) scale(1 -1)" opacity=".22"><path d="M-22 0 L22 0 L17 6 L-17 6Z" fill="#F4F1EA"/><path d="M1 -38 L18 -4 H1Z" fill="#FFF7EC"/></g>
</g></g></g>'''
kf("boat", [(0, "transform:translateX(0)"), (14, "transform:translateX(-90px)"), (28, "transform:translateX(0)")], ease="ease-in-out")

# ── the paraglider ────────────────────────────────────────────────────────────
cells = ["#E8513F", "#F2B232", "#FFFFFF", "#E8513F", "#F2B232", "#FFFFFF", "#E8513F"]
canopy = []
n = len(cells)
for i, c in enumerate(cells):
    a0, a1 = 200 + i * (140 / n), 200 + (i + 1) * (140 / n)
    p = lambda a, r: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)) * .42)
    (x0, y0), (x1, y1) = p(a0, 70), p(a1, 70)
    (x2, y2), (x3, y3) = p(a1, 58), p(a0, 58)
    canopy.append(f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f}Z" fill="{c}"/>')
lines_ = "".join(f'<path d="M{x:.1f} {y:.1f} L0 56" stroke="#3A2A3E" stroke-width=".6" opacity=".8"/>' for x, y in ((-84, -36), (-54, -42), (-19, -44), (19, -44), (54, -42), (84, -36)))
BANNER = "Thanks for stopping by!"


def cloth(phase):
    """Banner outline whose edges ripple; the trailing (left) end moves most."""
    top, bot = [], []
    for i in range(13):
        x = -300 + i * 25
        a = (i / 12) * 2 * math.pi * 1.2 + phase
        dy = (0.8 + 3.2 * (1 - i / 12)) * math.sin(a)
        top.append((x, -20 + dy))
        bot.append((x, 20 + dy))
    pts = top + bot[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


phases = [k * math.pi / 2 for k in range(5)]
cloth_d = ";".join(cloth(ph) for ph in phases)
tail_d = ";".join(f"M-300 {-20 + (4 * math.sin(ph)):.1f} l-14 6 l14 6Z M-300 {8 + 4 * math.sin(ph):.1f} l-14 6 l14 6Z" for ph in phases)
glider_body = f'''
  <g class="sway">
    <g transform="translate(0 -6) scale(1.35)">{"".join(canopy)}
    <path d="M{-70 * math.cos(math.radians(20)):.1f} {-70 * math.sin(math.radians(20)) * .42:.1f} Q0 -42 {70 * math.cos(math.radians(20)):.1f} {-70 * math.sin(math.radians(20)) * .42:.1f}" fill="none" stroke="#FFF" stroke-width="1" opacity=".5"/></g>
    {lines_}
    <g transform="translate(0 56)">
      <path d="M-6 0 h12 l-2 12 h-8Z" fill="#2A3A55"/>
      <circle cx="0" cy="-5" r="4" fill="#E9B48A"/><path d="M-4 -7 a4 4 0 0 1 8 0Z" fill="#E8513F"/>
      <path d="M-3 12 l-5 8 M3 12 l6 7" stroke="#2A3A55" stroke-width="2.4" stroke-linecap="round"/>
    </g>
    <path d="M-4 66 C-40 70 -70 72 -96 70" fill="none" stroke="#3A2A3E" stroke-width="1"/>
    <g transform="translate(-96 70)">
      <path fill="#FFF7EC" d="{cloth(0)}"><animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="{cloth_d}"/></path>
      <path fill="url(#bannerShade)" d="{cloth(0)}"><animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="{cloth_d}"/></path>
      <path fill="#FFF7EC"><animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="{tail_d}"/></path>
      <rect x="-4" y="-21" width="5" height="42" fill="#E8513F"/>
      <g class="ride"><text x="-150" y="7" text-anchor="middle" class="disp" font-size="21" font-weight="800" fill="#2A1830">{BANNER}</text></g>
    </g>
  </g>'''
glider = f'<g class="fly"><g class="bob">{glider_body}</g></g>'
kf("fly", [(0, "transform:translate(-60px,150px)"), (26, "transform:translate(1700px,170px)"), (28, "transform:translate(1700px,170px)")])
kf("bob", [(0, "transform:translateY(0)"), (2.5, "transform:translateY(-5px)"), (5, "transform:translateY(0)")], dur=5, ease="ease-in-out")
kf("sway", [(0, "transform:rotate(-1.4deg)"), (4, "transform:rotate(1.4deg)"), (8, "transform:rotate(-1.4deg)")], dur=8, ease="ease-in-out", extra="transform-box:view-box;transform-origin:0 56px")
kf("ride", [(0, "transform:translateY(-1.4px)"), (1.2, "transform:translateY(1.4px)"), (2.4, "transform:translateY(-1.4px)")], dur=2.4, ease="ease-in-out")

gulls = "".join(f'<g class="gull" style="animation-delay:{d}s"><path d="M{x} {y} q6 -6 12 0 q6 -6 12 0" fill="none" stroke="#5A3A2E" stroke-width="2"/></g>' for x, y, d in ((420, 120, 0), (460, 138, -3), (1000, 110, -7)))
kf("gull", [(0, "transform:translate(0,0)"), (14, "transform:translate(120px,-10px)"), (28, "transform:translate(0,0)")], ease="ease-in-out")

css.append("""
  .disp{font-family:'Segoe UI Variable Display','Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif}
  .glint{animation:glint 2.6s ease-in-out infinite alternate}@keyframes glint{from{opacity:.3;transform:translateX(-4px)}to{opacity:.95;transform:translateX(4px)}}
  .spark{animation:spark 3s ease-in-out infinite}@keyframes spark{0%,100%{opacity:0}50%{opacity:.9}}
  .moor{animation:moor 3.2s ease-in-out infinite alternate}@keyframes moor{to{transform:translateY(1.5px)}}
  .cloud{animation:cloud 40s ease-in-out infinite alternate}@keyframes cloud{to{transform:translateX(50px)}}
  .refl{animation:refl 3s ease-in-out infinite alternate}@keyframes refl{to{transform:translateX(-5px)}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.fly{transform:translate(800px,160px)}}
""")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Thanks for stopping by: golden hour at El Medano, Tenerife. Montana Roja rises on its flat spit across a calm sea with small boats moored in front and the low sun to the left. A paraglider glides across the sky towing a banner that says Thanks for stopping by, mirrored softly in the water.">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5E6FA6"/><stop offset=".35" stop-color="#C98A8A"/><stop offset=".7" stop-color="#F2AE6A"/><stop offset="1" stop-color="#FFD89A"/></linearGradient>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9B47A"/><stop offset=".18" stop-color="#7FA59A"/><stop offset=".55" stop-color="#2F6E80"/><stop offset="1" stop-color="#1A4558"/></linearGradient>
    <linearGradient id="rojaG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B8604A"/><stop offset=".45" stop-color="#9A4A3E"/><stop offset="1" stop-color="#5E3036"/></linearGradient>
    <linearGradient id="sunG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6CC"/><stop offset="1" stop-color="#FFC266"/></linearGradient>
    <radialGradient id="sunGlow"><stop offset="0" stop-color="#FFD58A" stop-opacity=".75"/><stop offset="1" stop-color="#FFD58A" stop-opacity="0"/></radialGradient>
    <linearGradient id="bannerShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity="0"/><stop offset="1" stop-color="#C9A88A" stop-opacity=".35"/></linearGradient>
    <filter id="ripple" x="-5%" y="-10%" width="110%" height="120%"><feGaussianBlur stdDeviation="2.4 .9"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <clipPath id="seaC"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>
    <style>{"".join(css)}</style>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{HZ}" fill="url(#sky)"/>
    {clouds}
    <circle cx="{SUNX}" cy="{SUNY}" r="170" fill="url(#sunGlow)"/>
    <circle cx="{SUNX}" cy="{SUNY}" r="40" fill="url(#sunG)"/>
    {roja}
    <rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea)"/>
    <g clip-path="url(#seaC)" opacity=".28" filter="url(#ripple)"><g class="refl">
      <g transform="translate(0 {2 * HZ}) scale(1 -1)"><path d="{ROJA_PATH}" fill="#7A3A36"/>{glider}</g></g></g>
    {sunpath}{waves}{sparkle}
    {buoys}{boats}{sailboat}
    {gulls}
    {glider}
  </g>
</svg>
'''
with open("thanks.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("ok", len(svg) // 1024, "KB")
