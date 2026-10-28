"""'Daily life' v2: Moe's room at dusk, seen from behind his chair (24 s loop).

Composition and lighting after a lit night-room illustration: textured wall, a
steel window onto Teide and the sea, four monitors 2x2 on one arm with Moe in
front of them, desk lamp light cone, LED strip under the desk, shelves with a
small TV. Everything stands on a surface and casts a shadow.
"""
W, H = 1280, 640
SHELF = 300
LOOP = 24.0
DESK = 468            # desk top surface
FLOOR = 588
css = []


def pct(t, dur=LOOP):
    return f"{t / dur * 100:.2f}%"


def kf(name, frames, dur=LOOP, ease="linear", extra=""):
    body = "".join(f"{pct(t, dur)}{{{d}}}" for t, d in frames)
    css.append(f".{name}{{animation:{name} {dur}s {ease} infinite;{extra}}}@keyframes {name}{{{body}}}")


def shadow(cx, y, rx, op=.45):
    return f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{max(2, rx * .14):.1f}" fill="#000" opacity="{op}"/>'


# ── wall texture: stone courses, very subtle ──────────────────────────────────
stones = []
for r, y in enumerate(range(0, DESK, 26)):
    off = 0 if r % 2 else 38
    for x in range(-off, W, 76):
        stones.append(f'<rect x="{x + 2}" y="{y + 2}" width="72" height="22" rx="3"/>')
wall = (f'<rect width="{W}" height="{DESK}" fill="url(#wallG)"/>'
        f'<g fill="#FFFFFF" opacity=".025">{"".join(stones)}</g>'
        f'<rect width="{W}" height="{DESK}" fill="url(#vignette)"/>')
# wooden ceiling beams (Canarian "tea" wood)
beams = "".join(f'<rect x="0" y="{y}" width="{W}" height="10" fill="#2A1A14"/><rect x="0" y="{y + 10}" width="{W}" height="3" fill="#000" opacity=".35"/>' for y in (0,))

# ── window: a Playa Jardín-style view (Puerto de la Cruz), drawn ──
WX, WY, WW, WH = 34, 44, 360, 286
SILL = WY + WH + 8
HZ = WY + 66                        # sea horizon, high: the sea fills the view
houses_w = []
hx = WX - 4
for i, (w, h, c) in enumerate(((26, 30, "#F4EFE6"), (20, 40, "#EFC27A"), (24, 26, "#F08A4B"), (18, 34, "#F4EFE6"), (22, 22, "#D9534F"),
                               (20, 30, "#F4EFE6"), (16, 24, "#6FA8DC"), (22, 28, "#F7D9A8"))):
    top = HZ + 10 - h + (i % 3) * 4
    houses_w.append(f'<rect x="{hx}" y="{top}" width="{w}" height="{h + 30}" fill="{c}"/>'
                    f'<rect x="{hx + w - 4}" y="{top}" width="4" height="{h + 30}" fill="#000" opacity=".12"/>'
                    + "".join(f'<rect x="{hx + 4 + k * 7}" y="{top + 6 + r * 9}" width="3.5" height="4" fill="#3A4A5A" opacity=".6"/>' for k in range(max(1, w // 8)) for r in range(2)))
    hx += w + 1
people = "".join(f'<rect x="{WX + x}" y="{WY + y}" width="{w}" height="2.4" rx="1" fill="{c}"/>'
                 for x, y, w, c in ((70, 170, 8, "#F25C54"), (96, 186, 7, "#4FC3F7"), (124, 176, 9, "#FFD54F"), (150, 196, 7, "#F4EFE6"), (60, 206, 8, "#81C784"),
                                    (110, 214, 7, "#F25C54"), (176, 212, 8, "#4FC3F7"), (88, 232, 9, "#FFD54F"), (140, 240, 7, "#F4EFE6"), (200, 236, 8, "#F48FB1")))
umbrellas = "".join(f'<g transform="translate({WX + x} {WY + y})"><path d="M-6 0 Q0 -6 6 0Z" fill="{c}"/><rect x="-.5" y="0" width="1" height="5" fill="#2A2A2A"/></g>'
                    for x, y, c in ((84, 178, "#F25C54"), (132, 168, "#FFD54F"), (164, 204, "#4FC3F7"), (102, 226, "#F48FB1"), (60, 196, "#81C784")))
window = f"""
  <clipPath id="winC"><rect x="{WX}" y="{WY}" width="{WW}" height="{WH}"/></clipPath>
  <g clip-path="url(#winC)">
    <rect x="{WX}" y="{WY}" width="{WW}" height="{HZ - WY + 2}" fill="url(#daySky)"/>
    <path d="M{WX + 40} {WY + 26} q10 -8 22 -2 q8 -6 18 0 q10 0 10 6 h-56Z" fill="#FFF" opacity=".8" class="cloudDrift"/>
    <path d="M{WX + 220} {WY + 16} q8 -6 18 -2 q6 -5 14 0 q8 0 8 5 h-46Z" fill="#FFF" opacity=".7" class="cloudDrift"/>
    <rect x="{WX}" y="{HZ}" width="{WW}" height="{WH}" fill="url(#atlantic)"/>
    <path d="M{WX + 300} {HZ} q14 -6 30 -4 q20 -2 34 4Z" fill="#3D4A55" opacity=".6"/>
    <!-- coastline: the black-sand beach sweeps from the cliff (left) round to the bottom right -->
    <path d="M{WX - 6} {HZ + 34} C{WX + 70} {HZ + 40} {WX + 150} {HZ + 76} {WX + 210} {HZ + 120} C{WX + 260} {HZ + 156} {WX + 320} {HZ + 186} {WX + WW + 6} {HZ + 196} L{WX + WW + 6} {WY + WH} L{WX - 6} {WY + WH}Z" fill="url(#blackSand)"/>
    <g fill="none" stroke="#FFF" stroke-linecap="round" class="surf">
      <path d="M{WX + 40} {HZ + 34} C{WX + 110} {HZ + 44} {WX + 170} {HZ + 80} {WX + 220} {HZ + 116} C{WX + 266} {HZ + 148} {WX + 320} {HZ + 176} {WX + WW + 6} {HZ + 186}" stroke-width="4" opacity=".9"/>
      <path d="M{WX + 70} {HZ + 26} C{WX + 130} {HZ + 36} {WX + 186} {HZ + 66} {WX + 232} {HZ + 98} C{WX + 276} {HZ + 128} {WX + 326} {HZ + 160} {WX + WW + 6} {HZ + 168}" stroke-width="2" opacity=".6"/>
      <path d="M{WX + 120} {HZ + 22} C{WX + 170} {HZ + 34} {WX + 210} {HZ + 54} {WX + 250} {HZ + 80}" stroke-width="1.4" opacity=".45"/>
    </g>
    <path d="M{WX + 40} {HZ + 38} C{WX + 110} {HZ + 48} {WX + 170} {HZ + 84} {WX + 220} {HZ + 120} C{WX + 266} {HZ + 152} {WX + 320} {HZ + 180} {WX + WW + 6} {HZ + 190}" fill="none" stroke="#7FD6D9" stroke-width="5" opacity=".35"/>
    {people}{umbrellas}
    <!-- the cliff with its colourful houses (left) -->
    <path d="M{WX - 6} {HZ - 4} L{WX + 150} {HZ - 4} C{WX + 158} {HZ + 6} {WX + 152} {HZ + 18} {WX + 138} {HZ + 22} C{WX + 100} {HZ + 30} {WX + 50} {HZ + 34} {WX - 6} {HZ + 40}Z" fill="#3A3230"/>
    <g>{"".join(houses_w)}</g>
    <!-- palms and agave right in front of the window -->
    <g fill="#2F5A2E">
      <path d="M{WX + 290} {WY + WH} C{WX + 296} {WY + 230} {WX + 304} {WY + 190} {WX + 316} {WY + 150}" stroke="#5A4630" stroke-width="7" fill="none"/>
      {"".join(f'<path d="M{WX + 316} {WY + 150} q{dx * .5:.0f} {dy * .6:.0f} {dx} {dy} q{-dx * .4:.0f} {-dy * .2:.0f} {-dx} {-dy + 4}Z" fill="{c}"/>' for dx, dy, c in ((-60, -18, "#2F5A2E"), (-50, 14, "#3B6E36"), (54, -26, "#2F5A2E"), (58, 10, "#3B6E36"), (-20, -46, "#3B6E36"), (24, -44, "#2F5A2E"), (-36, 34, "#2F5A2E")))}
      {"".join(f'<path d="M{WX + 340 + ox} {WY + WH} q{lx * .3:.0f} {-ly * .6:.0f} {lx} {-ly} q{-lx * .2:.0f} {ly * .5:.0f} {-lx + (6 if lx > 0 else -6)} {ly}Z" fill="{c}"/>' for ox, lx, ly, c in ((0, -40, 56, "#4E7F3C"), (0, -10, 70, "#5E9446"), (0, 22, 62, "#4E7F3C"), (0, 44, 40, "#3E6A30"), (-14, -30, 36, "#3E6A30")))}
    </g>
  </g>
  <rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" fill="url(#glassTint)"/>
  <rect x="{WX - 10}" y="{WY - 10}" width="{WW + 20}" height="{WH + 20}" fill="none" stroke="#141118" stroke-width="12"/>
  <g stroke="#141118" stroke-width="6"><path d="M{WX + WW / 3} {WY} V{WY + WH} M{WX + 2 * WW / 3} {WY} V{WY + WH} M{WX} {WY + WH * .42} H{WX + WW}"/></g>
  <rect x="{WX - 22}" y="{SILL}" width="{WW + 44}" height="12" fill="#3A2A24"/><rect x="{WX - 22}" y="{SILL + 12}" width="{WW + 44}" height="4" fill="#000" opacity=".4"/>
  <path d="M{WX + WW} {WY + 40} L{WX + WW + 260} {DESK} L{WX + WW + 120} {DESK} L{WX + WW - 40} {WY + WH}Z" fill="#CFEFFF" opacity=".035"/>
"""
css.append(".surf{animation:surf 3.2s ease-in-out infinite alternate}@keyframes surf{to{transform:translate(-4px,3px);opacity:.7}}")
css.append(".cloudDrift{animation:cd 24s linear infinite alternate}@keyframes cd{to{transform:translateX(30px)}}")


# ── two vertical posters on the left wall (mirror the TV/game column around x = 640) ──
PW, PH, PY = 128, 214, 60
P1X, P2X = 202 - 11 - PW, 202 + 11        # the pair is centred on x = 202 (= 640 - 438)
JP = "'Yu Gothic','Hiragino Sans','Noto Sans JP','Meiryo',sans-serif"
CASTLE_ROOF = "#0B0A12"
def roof(cx, y, w, h, flare=10):
    return (f'<path d="M{cx - w / 2 - flare} {y + h} Q{cx - w / 2} {y + h - 2} {cx - w / 2 + 6} {y + 2} L{cx + w / 2 - 6} {y + 2} '
            f'Q{cx + w / 2} {y + h - 2} {cx + w / 2 + flare} {y + h}Z" fill="{CASTLE_ROOF}"/>'
            f'<path d="M{cx - w / 2 - flare} {y + h} Q{cx - w / 2} {y + h - 2} {cx - w / 2 + 6} {y + 2}" fill="none" stroke="#6E7FB8" stroke-width="1" opacity=".5"/>')
def wall_(cx, y, w, h):
    win = "".join(f'<rect x="{cx - w / 2 + 5 + i * ((w - 14) / 3):.1f}" y="{y + 4}" width="4" height="5" fill="#F2B45A"/>' for i in range(4))
    return f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" fill="#1C2236"/>{win}'
petals = "".join(f'<path d="M{x} {y} q2 -3 4 0 q-2 3 -4 0Z" fill="#E8A0B8" opacity="{o}"/>' for x, y, o in ((22, 40, .7), (96, 58, .6), (40, 120, .5), (108, 96, .6), (70, 30, .5), (16, 160, .45), (112, 150, .5)))
# the hidden leaf: a small leaf with a swirl, low contrast, carved into the gate
hidden_leaf = ('<g transform="translate(64 176) scale(.55)" opacity=".55"><path d="M0 -10 C8 -10 12 -2 10 6 C8 12 0 14 -6 10 C-12 6 -10 -6 0 -10Z" fill="none" stroke="#6E7FB8" stroke-width="1.6"/>'
               '<path d="M0 -2 C4 -2 4 4 0 4 C-3 4 -3 0 0 0" fill="none" stroke="#6E7FB8" stroke-width="1.4"/><path d="M-6 10 L-10 15" stroke="#6E7FB8" stroke-width="1.6"/></g>')
poster1 = f"""<g transform="translate({P1X} {PY})">
  <rect x="4" y="6" width="{PW}" height="{PH}" fill="#000" opacity=".45"/>
  <rect width="{PW}" height="{PH}" fill="url(#nightPoster)"/>
  <circle cx="96" cy="40" r="15" fill="#E9E4D4"/><circle cx="96" cy="40" r="26" fill="#E9E4D4" opacity=".08"/>
  {"".join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#FFF" opacity=".6"/>' for x, y in ((18, 22), (40, 14), (60, 34), (112, 70), (28, 64)))}
  <path d="M0 196 C30 186 60 190 {PW} 184 V{PH} H0Z" fill="#0A0C16"/>
  <rect x="26" y="168" width="76" height="22" fill="#151A2A"/>{"".join(f'<rect x="{26 + i * 8}" y="{168 + (i % 2) * 6}" width="7" height="5" fill="#1B2134"/>' for i in range(10))}
  {wall_(64, 148, 58, 20)}{roof(64, 136, 66, 14, 9)}
  {wall_(64, 120, 46, 18)}{roof(64, 108, 54, 14, 8)}
  {wall_(64, 94, 34, 16)}{roof(64, 82, 42, 14, 7)}
  {roof(64, 68, 26, 16, 6)}
  <path d="M60 68 l4 -6 l4 6Z" fill="#C9A44A"/>
  <path d="M56 190 v-12 a8 8 0 0 1 16 0 v12Z" fill="#0A0C16"/>{hidden_leaf}
  {petals}
  <text x="14" y="34" style="font-family:{JP}" font-size="18" font-weight="800" fill="#E9E4D4">夜</text>
  <text x="14" y="56" style="font-family:{JP}" font-size="18" font-weight="800" fill="#E9E4D4">の</text>
  <text x="14" y="78" style="font-family:{JP}" font-size="18" font-weight="800" fill="#C0392B">城</text>
  <text x="{PW / 2}" y="206" text-anchor="middle" class="mono" font-size="7" font-weight="700" fill="#8A93B8" letter-spacing="2">CASTLE · NIGHT</text>
  <rect width="{PW}" height="{PH}" fill="url(#paperShade)"/>
  <rect x="{PW / 2 - 14}" y="-5" width="28" height="10" fill="#E8DCC8" opacity=".45" transform="rotate(-4 {PW / 2} 0)"/>
</g>"""
# a comic-book "heroes" poster: four original emblems in a 2x2 panel grid, dark paper
import math as _m
def _burst(n, r1, r2, rot=0):
    pts = []
    for k in range(2 * n):
        r = r1 if k % 2 == 0 else r2
        a = _m.pi * k / n + rot
        pts.append(f"{r * _m.sin(a):.1f},{-r * _m.cos(a):.1f}")
    return " ".join(pts)
HERO_LINE = "#F4EFE6"
emb_shield = ('<path d="M0 -20 L17 -14 C17 4 10 14 0 21 C-10 14 -17 4 -17 -14Z" fill="#C8343A" stroke="#F4EFE6" stroke-width="1.2"/>'
              '<path d="M0 -16 L13 -11.5 C13 2 8 10 0 16" fill="none" stroke="#7E1E28" stroke-width="1.4"/>'
              '<path d="M4 -15 L-7 2 L-1 2 L-4 15 L8 -3 L2 -3 L5 -15Z" fill="#FFD23F" stroke="#14101A" stroke-width=".7" stroke-linejoin="round"/>')
emb_star = (f'<circle r="19" fill="#E8A72E" stroke="#F4EFE6" stroke-width="1.2"/><circle r="14.5" fill="#123A4A"/>'
            f'<circle r="14.5" fill="none" stroke="#E8A72E" stroke-width=".8" stroke-dasharray="1.5 1.8" opacity=".8"/>'
            f'<polygon points="{_burst(5, 11, 4.4)}" fill="#F4EFE6" stroke="#14101A" stroke-width=".6"/>'
            f'<polygon points="{_burst(5, 4.4, 1.8, _m.pi / 5)}" fill="#3FC1C9"/>')
_wing = '<path d="M-10 -5 C-16 -15 -24 -16 -27 -11 C-23 -10 -21 -8 -20 -6 C-25 -6 -27 -2 -26 1 C-22 -1 -19 -1 -17 0 C-20 2 -21 5 -20 7 C-16 4 -12 2 -9 2Z" fill="#E8E4F0" stroke="#14101A" stroke-width=".6"/>'
emb_mask = (f'{_wing}<g transform="scale(-1 1)">{_wing}</g>'
            '<path d="M-13 -7 C-6 -10 6 -10 13 -7 C14 1 10 7 4 7 C2 7 1 4 0 4 C-1 4 -2 7 -4 7 C-10 7 -14 1 -13 -7Z" fill="#7B4FD6" stroke="#F4EFE6" stroke-width="1.2"/>'
            '<path d="M-8.5 -1.5 C-6 -4 -3 -4 -2 -1 C-4 1 -7 1 -8.5 -1.5Z M8.5 -1.5 C6 -4 3 -4 2 -1 C4 1 7 1 8.5 -1.5Z" fill="#F4EFE6"/>')
emb_crest = ('<path d="M0 -21 L19 0 L0 21 L-19 0Z" fill="#2E9E62" stroke="#F4EFE6" stroke-width="1.2" stroke-linejoin="round"/>'
             '<path d="M0 -16 L14 0 L0 16 L-14 0Z" fill="none" stroke="#165C38" stroke-width="1.2"/>'
             '<path d="M-8 2 L0 -6 L8 2 M-8 9 L0 1 L8 9" fill="none" stroke="#FFD23F" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
hero_cells = []
for cx, cy, bg, glow, emb, rot in ((36, 78, "#2A1222", "#C8343A", emb_shield, 0), (92, 78, "#0F2533", "#3FC1C9", emb_star, .2),
                                  (36, 146, "#1D1536", "#7B4FD6", emb_mask, .1), (92, 146, "#0F2620", "#2E9E62", emb_crest, .3)):
    hero_cells.append(
        f'<rect x="{cx - 26}" y="{cy - 31}" width="52" height="62" fill="{bg}"/>'
        f'<rect x="{cx - 26}" y="{cy - 31}" width="52" height="62" fill="url(#heroDots)"/>'
        f'<polygon points="{_burst(12, 27, 17, rot)}" transform="translate({cx} {cy})" fill="{glow}" opacity=".22"/>'
        f'<g transform="translate({cx} {cy})">{emb}</g>'
        f'<rect x="{cx - 26}" y="{cy - 31}" width="52" height="62" fill="none" stroke="#E9E4D4" stroke-width="1.2" opacity=".55"/>')
poster2 = f"""<g transform="translate({P2X} {PY})">
  <rect x="4" y="6" width="{PW}" height="{PH}" fill="#000" opacity=".45"/>
  <rect width="{PW}" height="{PH}" fill="url(#heroPoster)"/>
  <g transform="translate({PW / 2} 35) skewX(-8)" class="disp" font-size="25" font-weight="900" text-anchor="middle" letter-spacing="1.5">
    <text x="2" y="2" fill="#C8343A">HEROES</text>
    <text x="0" y="0" fill="#FFD23F" stroke="#14101A" stroke-width=".8" paint-order="stroke">HEROES</text>
  </g>
  <path d="M14 41 H{PW - 14}" stroke="#E9E4D4" stroke-width=".6" opacity=".35"/>
  {"".join(hero_cells)}
  <text x="{PW / 2}" y="194" text-anchor="middle" style="font-family:{JP}" font-size="11" font-weight="800" fill="#E9E4D4" letter-spacing="1">ヒーロー</text>
  <text x="{PW / 2}" y="206" text-anchor="middle" class="mono" font-size="7" font-weight="700" fill="#8A93B8" letter-spacing="2">ISSUE #01</text>
  <rect width="{PW}" height="{PH}" fill="url(#paperShade)"/>
  <rect x="{PW / 2 - 14}" y="-5" width="28" height="10" fill="#E8DCC8" opacity=".45" transform="rotate(3 {PW / 2} 0)"/>
</g>"""
posters = poster1 + poster2

# ── the cat: curled up asleep on the desk in the lamp light (tortoiseshell) ──
TB, TO, TC, TR = "#191414", "#D9772E", "#F0C08A", "#8A3E1A"
import random as _r
_rng = _r.Random(5)
patches = "".join(f'<ellipse cx="{_rng.randint(18, 118)}" cy="{_rng.randint(-50, -6)}" rx="{_rng.randint(5, 13)}" ry="{_rng.randint(2, 5)}" '
                  f'fill="{_rng.choice([TO, TO, TO, TR, TR, TC])}" transform="rotate({_rng.randint(-40, 40)} 60 -28)" opacity="{_rng.choice([.75, .85, .95])}"/>'
                  for _ in range(46))
cat = f"""<g transform="translate(176 {DESK})">
  {shadow(64, 0, 70, .6)}
  <path d="M10 -4 C26 6 92 8 118 -4 C122 -8 120 -12 112 -12" fill="none" stroke="{TB}" stroke-width="11" stroke-linecap="round"/>
  <path d="M100 -9 C108 -10 114 -10 118 -6" fill="none" stroke="{TO}" stroke-width="11" stroke-linecap="round"/>
  <path d="M14 -6 C10 -30 34 -54 66 -54 C98 -54 122 -36 122 -14 C122 -6 116 -2 108 -2 L22 -2 C16 -2 14 -4 14 -6Z" fill="{TB}"/>
  <clipPath id="catBody"><path d="M14 -6 C10 -30 34 -54 66 -54 C98 -54 122 -36 122 -14 C122 -6 116 -2 108 -2 L22 -2 C16 -2 14 -4 14 -6Z"/></clipPath>
  <g clip-path="url(#catBody)"><g filter="url(#mottle)">{patches}</g></g>
  <g class="breath"><path d="M14 -6 C10 -30 34 -54 66 -54 C98 -54 122 -36 122 -14" fill="none" stroke="#FFD9A8" stroke-width="2" opacity=".35"/></g>
  <path d="M10 -4 C26 6 92 8 118 -4" fill="none" stroke="#FFD9A8" stroke-width="1.6" opacity=".45"/>
  <g transform="translate(20 -26)">
    <ellipse cx="0" cy="0" rx="21.5" ry="18.5" fill="#000" opacity=".55"/>
    <ellipse cx="0" cy="0" rx="20" ry="17" fill="{TB}"/>
    <path d="M-18 -6 C-14 -16 -4 -18 4 -17" fill="none" stroke="#FFD9A8" stroke-width="1.8" opacity=".6"/>
    <path d="M-1 -16 C8 -16 18 -10 19 0 C12 -4 4 -8 -1 -16Z" fill="{TO}"/>
    <path d="M-16 -9 L-20 -28 L-6 -15Z" fill="{TB}"/><path d="M-15 -12 L-17 -23 L-9 -15Z" fill="#E7A2A0" opacity=".75"/>
    <g class="ear"><path d="M4 -16 L10 -32 L16 -12Z" fill="{TO}"/><path d="M6 -16 L10 -27 L13 -14Z" fill="#E7A2A0" opacity=".7"/></g>
    <path d="M-12 -2 q4 3 8 0" fill="none" stroke="#000" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M2 -2 q4 3 8 0" fill="none" stroke="#000" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M-3 5 l2 2 l2 -2Z" fill="#E7A2A0"/>
    <path d="M-14 7 l-10 -1 M-14 9 l-10 2 M8 7 l10 -1 M8 9 l10 2" stroke="#E8DCC8" stroke-width=".7" opacity=".7"/>
    <path d="M-16 -9 L-20 -28 L-6 -15 M4 -16 L10 -32 L16 -12" fill="none" stroke="#FFD9A8" stroke-width="1.2" opacity=".55"/>
  </g>
  <g>
    <ellipse cx="40" cy="-5" rx="9" ry="5" fill="#000" opacity=".55"/><ellipse cx="40" cy="-5" rx="8" ry="4.4" fill="{TO}"/>
    <path d="M35 -3 v-2 M39 -2.6 v-2 M43 -3 v-2" stroke="#7A3A16" stroke-width=".9" stroke-linecap="round"/>
    <ellipse cx="54" cy="-4" rx="9" ry="5" fill="#000" opacity=".55"/><ellipse cx="54" cy="-4" rx="8" ry="4.4" fill="{TB}"/>
    <path d="M49 -2 v-2 M53 -1.6 v-2 M57 -2 v-2" stroke="{TC}" stroke-width=".9" stroke-linecap="round" opacity=".8"/>
  </g>
  <g class="zz"><text x="2" y="-60" class="disp" font-size="13" font-weight="700" fill="#FFE9C8">z</text><text x="12" y="-72" class="disp" font-size="10" font-weight="700" fill="#FFE9C8">z</text></g>
</g>"""
kf("ear", [(0, "transform:none"), (9, "transform:none"), (9.15, "transform:rotate(14deg)"), (9.3, "transform:none"), (24, "transform:none")], extra="transform-box:fill-box;transform-origin:0% 100%")
kf("breath", [(0, "transform:none"), (2, "transform:translateY(-1.5px)"), (4, "transform:none")], dur=4)
kf("zz", [(0, "opacity:0;transform:translateY(4px)"), (1.2, "opacity:1"), (3, "opacity:0;transform:translateY(-10px)")], dur=3)

# ── monitors 2x2 on one arm ───────────────────────────────────────────────────
MW, MH = 232, 136
MON = {"tl": (394, 46), "tr": (654, 46), "bl": (394, 212), "br": (654, 212)}   # 28 px gaps, centred on x=640


def frame(x, y, title, inner):
    return (f'<rect x="{x - 5}" y="{y - 5}" width="{MW + 10}" height="{MH + 10}" rx="5" fill="#0B0A0E"/>'
            f'<clipPath id="c{x}{y}"><rect x="{x}" y="{y}" width="{MW}" height="{MH}"/></clipPath>'
            f'<g clip-path="url(#c{x}{y})">{inner}'
            + (f'<rect x="{x}" y="{y}" width="{MW}" height="13" fill="#1A1820"/>'
               f'<circle cx="{x + 8}" cy="{y + 6.5}" r="2.2" fill="#FF5F57"/><circle cx="{x + 15}" cy="{y + 6.5}" r="2.2" fill="#FEBC2E"/><circle cx="{x + 22}" cy="{y + 6.5}" r="2.2" fill="#28C840"/>'
               f'<text x="{x + MW / 2}" y="{y + 9.5}" text-anchor="middle" class="mono" font-size="7" fill="#8A8496">{title}</text>' if title else "")
            + f'</g><rect x="{x}" y="{y}" width="{MW}" height="{MH}" fill="url(#glare)"/>')


# TL — Sasuke Lens: desktop with the notch
x, y = MON["tl"]
pills = "".join(f'<g><circle cx="{x + MW / 2 - 40 + i * 16}" cy="{y + 40}" r="5" fill="{c}"/></g>' for i, c in enumerate(["#9B6BFF", "#6EE7B7", "#FF2E88", "#FBBF24", "#A3E635", "#D4D7DD"]))
snow = "".join(f'<path d="M{x + sx} {y + sy} l{dx} {dy}" stroke="#F4F1F6" stroke-width="{w}" stroke-linecap="round" opacity=".85"/>'
               for sx, sy, dx, dy, w in ((86, 34, -14, 30, 2.4), (92, 36, -6, 34, 1.6), (100, 34, 8, 30, 2), (108, 38, 18, 30, 1.6), (116, 44, 26, 28, 2.2),
                                         (78, 44, -18, 22, 1.4), (124, 52, 30, 24, 1.4), (96, 42, 2, 26, 1.2), (70, 56, -16, 14, 1.2)))
taskbar_icons = "".join(f'<rect x="{x + MW / 2 - 46 + i * 13}" y="{y + MH - 15}" width="9" height="9" rx="2.5" fill="{c}"/>'
                        for i, c in enumerate(["#4F8BF9", "#F4F1F6", "#FBBF24", "#28C840", "#9B6BFF", "#FF5F57"]))
tl = (f'<rect x="{x}" y="{y}" width="{MW}" height="{MH}" fill="url(#alpenglow)"/>'
      f'<path d="M{x - 4} {y + 92} L{x + 40} {y + 64} C{x + 60} {y + 52} {x + 76} {y + 40} {x + 90} {y + 26} L{x + 96} {y + 22} L{x + 102} {y + 26}'
      f' C{x + 126} {y + 48} {x + 160} {y + 70} {x + 196} {y + 84} L{x + MW + 4} {y + 90} V{y + MH} H{x - 4}Z" fill="#7A6A7E"/>'
      f'<path d="M{x + 96} {y + 22} C{x + 120} {y + 46} {x + 160} {y + 70} {x + 196} {y + 84} L{x + MW + 4} {y + 90} V{y + 100} L{x + 96} {y + 100}Z" fill="#55485E" opacity=".75"/>'
      f'{snow}<path d="M{x + 90} {y + 26} L{x + 96} {y + 22} L{x + 102} {y + 26} L{x + 98} {y + 30} L{x + 94} {y + 28}Z" fill="#F7B3A0"/>'
      f'<path d="M{x - 4} {y + 100} C{x + 40} {y + 92} {x + 90} {y + 96} {x + 140} {y + 94} C{x + 180} {y + 92} {x + 210} {y + 98} {x + MW + 4} {y + 96} V{y + MH} H{x - 4}Z" fill="#1E2C36"/>'
      f'<path d="M{x + 180} {y + MH - 16} q12 -8 26 -4 q14 -6 26 2 v6 h-52Z" fill="#F4F1F6" opacity=".85"/>'
      f'<rect x="{x + MW / 2 - 52}" y="{y + MH - 18}" width="104" height="15" rx="7.5" fill="#000"/>{taskbar_icons}'
      f'<text x="{x + MW / 2 + 46}" y="{y + MH - 8}" text-anchor="end" class="mono" font-size="5.5" fill="#CFC9DB">19:42</text>'

      f'<g class="notchOpen"><rect x="{x + MW / 2 - 62}" y="{y}" width="124" height="56" rx="14" fill="#000"/>{pills}'
      f'</g>'
      f'<rect x="{x + MW / 2 - 30}" y="{y}" width="60" height="18" rx="9" fill="#000"/>'
      f'<g transform="translate({x + MW / 2 - 16} {y + 9})"><ellipse rx="6" ry="5" fill="#9B6BFF" class="mochi"/><circle cx="-2" cy="-1" r="1" fill="#1A1028"/><circle cx="2" cy="-1" r="1" fill="#1A1028"/></g>'
      f'<g class="wave" fill="#9B6BFF">{"".join(f'<rect x="{x + MW / 2 - 4 + i * 4}" y="{y + 6}" width="2" height="6" rx="1" class="wb{i % 3}"/>' for i in range(6))}</g>'
      '')
kf("notchOpen", [(0, "opacity:0;transform:scale(.48,.32)"), (13, "opacity:0;transform:scale(.48,.32)"), (13.4, "opacity:1;transform:none"), (18, "opacity:1;transform:none"), (18.4, "opacity:0;transform:scale(.48,.32)"), (24, "opacity:0")],
   extra="transform-box:fill-box;transform-origin:50% 0")
for i in range(3):
    kf(f"wb{i}", [(0, "transform:scaleY(.4)"), (.2, "transform:scaleY(1)"), (.4, "transform:scaleY(.5)"), (.6, "transform:scaleY(.4)")], dur=0.6 + i * .15, extra="transform-box:fill-box;transform-origin:center")

# BR — systems support: L2 queue
x, y = MON["br"]
rows = [("P3", "#60A5FA", "INC0412 · Printer offline", "Resolved"), ("P2", "#FBBF24", "INC0409 · MFA reset", "Resolved"), ("P3", "#60A5FA", "INC0405 · Teams audio", "Resolved"), ("P4", "#94A3B8", "REQ0398 · New laptop", "In progress")]
rr = []
for i, (p, pc, t_, st) in enumerate(rows):
    ry = y + 62 + i * 17
    rr.append(f'<rect x="{x + 8}" y="{ry}" width="{MW - 16}" height="14" rx="3" fill="#1E1B27"/>'
              f'<rect x="{x + 12}" y="{ry + 3}" width="16" height="8" rx="2" fill="{pc}"/><text x="{x + 15}" y="{ry + 10}" class="mono" font-size="6" font-weight="700" fill="#0E0B12">{p}</text>'
              f'<text x="{x + 34}" y="{ry + 10}" class="mono" font-size="6.6" fill="#CFC9DB">{t_}</text>'
              f'<text x="{x + MW - 12}" y="{ry + 10}" text-anchor="end" class="mono" font-size="6.6" fill="{"#4ADE80" if st == "Resolved" else "#FBBF24"}">{st}</text>')
tr = (f'<rect x="{x}" y="{y}" width="{MW}" height="{MH}" fill="#121019"/>'
      f'<text x="{x + 10}" y="{y + 26}" class="mono" font-size="7.5" font-weight="700" fill="#A9A3B8">SERVICE DESK · L2 QUEUE</text>'
      f'<text x="{x + MW - 10}" y="{y + 26}" text-anchor="end" class="mono" font-size="7" fill="#4ADE80">SLA 98%</text>'
      f'<g class="newT"><rect x="{x + 8}" y="{y + 34}" width="{MW - 16}" height="22" rx="4" fill="#24182A" stroke="#F87171" stroke-width="1"/>'
      f'<rect x="{x + 12}" y="{y + 41}" width="16" height="8" rx="2" fill="#F87171"/><text x="{x + 15}" y="{y + 48}" class="mono" font-size="6" font-weight="700" fill="#0E0B12">P2</text>'
      f'<text x="{x + 34}" y="{y + 44}" class="mono" font-size="7" fill="#FFF">INC0417 · VPN not connecting</text>'
      f'<text x="{x + 34}" y="{y + 52}" class="mono" font-size="6" fill="#8A8496">Ivanti · user remote</text>'
      f'<text x="{x + MW - 12}" y="{y + 48}" text-anchor="end" class="mono stOpen" font-size="7" fill="#F87171">Open</text>'
      f'<text x="{x + MW - 12}" y="{y + 48}" text-anchor="end" class="mono stWork" font-size="7" fill="#FBBF24">Working</text>'
      f'<text x="{x + MW - 12}" y="{y + 48}" text-anchor="end" class="mono stDone" font-size="7" fill="#4ADE80">Resolved ✓</text></g>'
      + "".join(rr))
frame_tr_title = "ServiceNow · my work"
kf("newT", [(0, "opacity:0;transform:translateY(-8px)"), (2, "opacity:0;transform:translateY(-8px)"), (2.4, "opacity:1;transform:none"), (23.3, "opacity:1;transform:none"), (23.7, "opacity:0"), (24, "opacity:0")])
kf("stOpen", [(0, "opacity:1"), (5, "opacity:1"), (5.05, "opacity:0"), (23.9, "opacity:0"), (24, "opacity:1")])
kf("stWork", [(0, "opacity:0"), (5, "opacity:0"), (5.05, "opacity:1"), (9, "opacity:1"), (9.05, "opacity:0"), (24, "opacity:0")])
kf("stDone", [(0, "opacity:0"), (9, "opacity:0"), (9.05, "opacity:1"), (23.9, "opacity:1"), (24, "opacity:0")])

# BL — systems: an admin PowerShell session + server health
x, y = MON["bl"]
ps_lines = [
    ("PS> ", "Unlock-ADAccount -Identity jgarcia", "#E5E5E5"),
    ("", "  account unlocked", "#4ADE80"),
    ("PS> ", "Reset-MgUserAuthMethods jgarcia", "#E5E5E5"),
    ("", "  MFA re-registration required", "#4ADE80"),
    ("PS> ", "Test-NetConnection SRV-FS01", "#E5E5E5"),
    ("", "  TcpTestSucceeded : True", "#93C5FD"),
]
pl = []
for i, (pr, cmd, col) in enumerate(ps_lines):
    ly = y + 28 + i * 11
    pl.append(f'<g class="ln{i}"><text x="{x + 6}" y="{ly}" class="mono" font-size="6.4" xml:space="preserve"><tspan fill="#FBBF24">{pr}</tspan><tspan fill="{col}">{cmd}</tspan></text></g>')
    t0 = .6 + i * 1.3
    kf(f"ln{i}", [(0, "clip-path:inset(0 100% 0 0)"), (t0, "clip-path:inset(0 100% 0 0)"), (t0 + 1, "clip-path:inset(0 0 0 0)"), (23, "clip-path:inset(0 0 0 0)"), (23.4, "clip-path:inset(0 100% 0 0)"), (24, "clip-path:inset(0 100% 0 0)")])
servers = [("SRV-DC01", "#4ADE80"), ("SRV-FS01", "#4ADE80"), ("SRV-APP02", "amber"), ("M365", "#4ADE80"), ("VPN-GW", "#4ADE80")]
sv = []
for i, (n, c) in enumerate(servers):
    sy = y + 34 + i * 18
    if c == "amber":
        dot = (f'<circle cx="{x + 166}" cy="{sy - 2.5}" r="3" fill="#FBBF24" class="warnDot"/>'
               f'<circle cx="{x + 166}" cy="{sy - 2.5}" r="3" fill="#4ADE80" class="okDot"/>')
    else:
        dot = f'<circle cx="{x + 166}" cy="{sy - 2.5}" r="3" fill="{c}"/>'
    sv.append(f'{dot}<text x="{x + 173}" y="{sy}" class="mono" font-size="6.2" fill="#CFC9DB">{n}</text>'
              f'<rect x="{x + 173}" y="{sy + 3}" width="48" height="2" rx="1" fill="#1E2A3E"/><rect x="{x + 173}" y="{sy + 3}" width="{[30, 22, 40, 18, 26][i]}" height="2" rx="1" fill="#60A5FA"/>')
bl = (f'<rect x="{x}" y="{y}" width="{MW}" height="{MH}" fill="#0C1A2E"/>'
      + "".join(pl) +
      f'<text x="{x + 6}" y="{y + 28 + 6 * 11}" class="mono blink" font-size="6.4" fill="#FBBF24">PS&gt; ▍</text>'
      f'<rect x="{x + 156}" y="{y + 18}" width="{MW - 160}" height="{MH - 22}" rx="4" fill="#0A1424"/>'
      f'<text x="{x + 162}" y="{y + 27}" class="mono" font-size="6" font-weight="700" fill="#8EA3C0">HEALTH</text>' + "".join(sv))
kf("warnDot", [(0, "opacity:1"), (12, "opacity:1"), (12.1, "opacity:0"), (23.9, "opacity:0"), (24, "opacity:1")])
kf("okDot", [(0, "opacity:0"), (12, "opacity:0"), (12.1, "opacity:1"), (23.9, "opacity:1"), (24, "opacity:0")])

# TR — watching something: night anime-style scene, subtitles, player bar
x, y = MON["tr"]
subs = ["“You knew all along?”", "“I never saw that twist coming.”", "“Then it was you…”"]
br = (f'<rect x="{x}" y="{y}" width="{MW}" height="{MH}" fill="url(#animeSky)"/>'
      f'<circle cx="{x + 172}" cy="{y + 40}" r="18" fill="#FFF3C4"/><circle cx="{x + 172}" cy="{y + 40}" r="30" fill="#FFF3C4" opacity=".12"/>'
      + "".join(f'<circle cx="{x + sx}" cy="{y + sy}" r=".9" fill="#fff" class="tl" style="animation-delay:{d}s"/>' for sx, sy, d in ((20, 18, 0), (60, 30, .7), (100, 14, 1.3), (210, 80, .4), (40, 60, 1.9), (130, 50, 1)))
      + f'<path d="M{x} {y + MH} V{y + 98} C{x + 60} {y + 84} {x + 150} {y + 88} {x + MW} {y + 104} V{y + MH}Z" fill="#0D0F2A"/>'
      f'<g fill="#07081A"><circle cx="{x + 92}" cy="{y + 74}" r="7"/><path d="M{x + 82} {y + 100} q10 -26 20 0Z"/><path d="M{x + 84} {y + 70} l-5 -9 l7 4 l2 -9 l4 8 l5 -7 l-1 10Z"/>'
      f'<circle cx="{x + 118}" cy="{y + 76}" r="7"/><path d="M{x + 108} {y + 100} q10 -24 20 0Z"/><path d="M{x + 110} {y + 74} q8 -14 16 0Z"/></g>'
      f'<rect x="{x + 34}" y="{y + 106}" width="{MW - 68}" height="13" rx="3" fill="#000" opacity=".6"/>'
      + "".join(f'<text x="{x + MW / 2}" y="{y + 115.5}" text-anchor="middle" class="disp sub{i}" font-size="7.5" fill="#FFF">{s}</text>' for i, s in enumerate(subs))
      + f'<rect x="{x}" y="{y + MH - 9}" width="{MW}" height="9" fill="#000" opacity=".55"/>'
      f'<rect x="{x + 22}" y="{y + MH - 5}" width="{MW - 60}" height="2" fill="#3A3D55"/><rect x="{x + 22}" y="{y + MH - 5}" width="{MW - 60}" height="2" fill="#FF3B5C" class="prog"/>'
      f'<path d="M{x + 8} {y + MH - 7} v5 l4 -2.5Z" fill="#FFF"/><text x="{x + MW - 34}" y="{y + MH - 2.5}" class="mono" font-size="5.5" fill="#CFC9DB">18:42 / 23:40</text>')
SUB_FRAMES = [
    [(0, "opacity:1"), (7.7, "opacity:1"), (8, "opacity:0"), (23.9, "opacity:0"), (24, "opacity:1")],
    [(0, "opacity:0"), (7.99, "opacity:0"), (8, "opacity:1"), (15.7, "opacity:1"), (16, "opacity:0"), (24, "opacity:0")],
    [(0, "opacity:0"), (15.99, "opacity:0"), (16, "opacity:1"), (23.7, "opacity:1"), (24, "opacity:0")],
]
for i in range(3):
    kf(f"sub{i}", SUB_FRAMES[i])
kf("prog", [(0, "transform:scaleX(.78)"), (24, "transform:scaleX(.84)")], extra="transform-box:fill-box;transform-origin:left")

monitors = (frame(*MON["tl"], "", tl) + frame(*MON["tr"], "", br) + frame(*MON["bl"], "Administrator: Windows PowerShell", bl) + frame(*MON["br"], frame_tr_title, tr))
arm = (f'<rect x="{640 - 3}" y="40" width="6" height="{DESK - 40}" fill="#2A2730"/>'
       f'<rect x="{640 - 40}" y="{DESK - 6}" width="80" height="6" rx="2" fill="#2A2730"/>{shadow(640, DESK, 44, .5)}')

# ── Moe, from behind ──────────────────────────────────────────────────────────
person = f'''<g class="typing">
  <path d="M560 {H} C556 470 572 418 600 402 C618 392 662 392 680 402 C708 418 724 470 720 {H}Z" fill="#2B2A36"/>
  <path d="M600 402 C618 392 662 392 680 402 C668 410 612 410 600 402Z" fill="#3A3946"/>
  <rect x="628" y="372" width="24" height="30" rx="8" fill="#B07A5A"/>
  <ellipse cx="603" cy="342" rx="5" ry="9" fill="#B07A5A"/><ellipse cx="677" cy="342" rx="5" ry="9" fill="#B07A5A"/>
  <ellipse cx="640" cy="336" rx="37" ry="44" fill="#1A1416"/>
  <path d="M606 352 C606 368 618 380 640 382 C662 380 674 368 674 352 C668 364 656 370 640 370 C624 370 612 364 606 352Z" fill="#1A1416"/>
  <g stroke="#2E2428" stroke-width="2" fill="none" stroke-linecap="round" opacity=".9">
    <path d="M618 306 q6 -6 12 -2"/><path d="M640 300 q6 -5 12 0"/><path d="M626 322 q6 -6 12 -2"/><path d="M648 318 q6 -5 12 0"/><path d="M616 340 q6 -6 12 -2"/><path d="M636 344 q6 -5 12 0"/><path d="M656 338 q5 -5 10 0"/></g>
  <path d="M600 334 C598 300 616 286 640 286 C664 286 682 300 680 334 C676 338 668 340 664 338 L616 338 C612 340 604 338 600 334Z" fill="#22304F"/>
  <path d="M640 286 V336 M622 290 C614 306 610 320 608 334 M658 290 C666 306 670 320 672 334" fill="none" stroke="#2E3E63" stroke-width="1.5"/>
  <path d="M616 338 C620 326 630 320 640 320 C650 320 660 326 664 338Z" fill="#1A1416"/>
  <rect x="624" y="328" width="32" height="5" rx="2.5" fill="#2E3E63"/><rect x="637" y="327" width="6" height="7" rx="1" fill="#C9CED8"/>
  <circle cx="640" cy="287" r="3" fill="#2E3E63"/>
  <path d="M598 340 C596 300 614 280 640 280 C666 280 684 300 682 340" fill="none" stroke="#141218" stroke-width="7" stroke-linecap="round"/>
  <path d="M600 330 C600 300 616 284 640 284 C664 284 680 300 680 330" fill="none" stroke="#7FB8FF" stroke-width="1.2" opacity=".35"/>
  <rect x="588" y="326" width="16" height="28" rx="7" fill="#141218"/><rect x="676" y="326" width="16" height="28" rx="7" fill="#141218"/>
  <rect x="590" y="330" width="4" height="20" rx="2" fill="#2A2731"/><rect x="686" y="330" width="4" height="20" rx="2" fill="#2A2731"/>
  <path d="M594 354 C590 380 586 404 572 424 C562 438 556 452 552 468" fill="none" stroke="#141218" stroke-width="2.4" stroke-linecap="round"/>
</g>'''
kf("typing", [(0, "transform:none"), (.35, "transform:translateY(1px)"), (.7, "transform:none")], dur=0.7)
chair = f'''<g>
  <path d="M520 {H} C514 520 520 452 540 430 C560 412 720 412 740 430 C760 452 766 520 760 {H}Z" fill="#17151D"/>
  <path d="M540 {H} C536 524 540 466 556 448 C572 432 708 432 724 448 C740 466 744 524 740 {H}Z" fill="#221F2A"/>
  <path d="M556 448 C572 432 708 432 724 448" fill="none" stroke="#FF8A3D" stroke-width="2.5" opacity=".75"/>
  <g fill="#2B2733" opacity=".7">{"".join(f'<rect x="{564 + c * 16}" y="{470 + r * 16}" width="10" height="10" rx="2"/>' for r in range(10) for c in range(10))}</g>
</g>'''

# ── left of the desk: lamp, dragon tree, music ────────────────────────────────
lamp = f'''<g>
  <path d="M232 {DESK} L262 {DESK - 6} L300 {DESK - 6} L330 {DESK}Z" fill="#FFC78A" opacity=".0"/>
  <path d="M196 288 L132 {DESK} L308 {DESK}Z" fill="url(#cone)" class="lampLight"/>
  {shadow(150, DESK, 30, .55)}
  <rect x="128" y="{DESK - 6}" width="44" height="6" rx="2" fill="#2A2730"/>
  <path d="M150 {DESK - 6} L176 352 L204 296" fill="none" stroke="#2A2730" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M188 282 L222 296 L208 312 L176 300Z" fill="#2E2A34"/>
  <ellipse cx="200" cy="304" rx="12" ry="4" fill="#FFE7B8" transform="rotate(22 200 304)"/>
</g>'''
drago = f'''<g transform="translate(796 {DESK}) scale(.8)">
  {shadow(0, 0, 24, .55)}
  <path d="M-18 -30 L18 -30 L14 0 L-14 0Z" fill="#B25E3A"/><rect x="-20" y="-34" width="40" height="6" rx="2" fill="#C9714A"/>
  <path d="M-2 -34 C-4 -54 -2 -70 0 -78 M0 -66 C8 -76 14 -84 18 -92 M-1 -58 C-10 -70 -16 -78 -18 -86" fill="none" stroke="#7A5A42" stroke-width="5" stroke-linecap="round"/>
  {"".join(f'<g transform="translate({cx} {cy})">' + "".join(f'<path d="M0 0 l{17 * __import__("math").cos(a / 57.3):.1f} {17 * __import__("math").sin(a / 57.3):.1f}" stroke="#5E8C4A" stroke-width="3.2" stroke-linecap="round"/>' for a in range(-180, 1, 22)) + '</g>' for cx, cy in ((0, -80), (18, -94), (-18, -88)))}
</g>'''
speaker = f'''<g transform="translate(332 {DESK})">
  {shadow(0, 0, 30, .55)}
  <rect x="-26" y="-92" width="52" height="92" rx="7" fill="#1A1820"/>
  <rect x="-26" y="-92" width="52" height="92" rx="7" fill="url(#sideLight)"/>
  <circle cx="0" cy="-66" r="9" fill="#26232D"/><circle cx="0" cy="-66" r="3.5" fill="#33303B"/>
  <g class="cone"><circle cx="0" cy="-30" r="17" fill="#26232D"/><circle cx="0" cy="-30" r="7" fill="#3A3644"/></g>
  {"".join(f'<text x="{dx}" y="-100" class="disp note" font-size="{fs}" fill="{c}" style="animation-delay:{d}s">{n}</text>' for dx, fs, c, d, n in ((-14, 18, "#FFD27A", 0, "♪"), (4, 15, "#FF8ACB", 1.3, "♫"), (-6, 16, "#9B6BFF", 2.6, "♪")))}
</g>'''
speaker2 = speaker.replace('translate(332 {DESK})'.replace("{DESK}", str(DESK)), f'translate({640 + (640 - 332)} {DESK})').replace('animation-delay:0s', 'animation-delay:2s').replace('animation-delay:1.3s', 'animation-delay:3.3s').replace('animation-delay:2.6s', 'animation-delay:.6s')
kf("cone", [(0, "transform:scale(1)"), (.25, "transform:scale(1.1)"), (.5, "transform:scale(1)")], dur=0.5, extra="transform-box:fill-box;transform-origin:center")
kf("note", [(0, "opacity:0;transform:none"), (.6, "opacity:1"), (3.4, "opacity:0;transform:translate(12px,-44px)"), (4, "opacity:0")], dur=4)

# ── right of the desk: NAS (middle), coffee, controller, PC, side screen ──────
nas = f'''<g transform="translate(1190 {SHELF}) scale(.78)">
  {shadow(0, 0, 40, .55)}
  <rect x="-36" y="-66" width="72" height="66" rx="6" fill="#141218"/>
  <rect x="-36" y="-66" width="72" height="66" rx="6" fill="url(#sideLight)"/>
  {"".join(f'<rect x="-28" y="{-58 + i * 14}" width="44" height="10" rx="2" fill="#1F1C25"/><circle cx="24" cy="{-53 + i * 14}" r="2" fill="#4ADE80" class="led" style="animation-delay:{i * .37:.2f}s"/>' for i in range(4))}
  <text x="0" y="-70" text-anchor="middle" class="mono" font-size="6.5" fill="#8A8496" letter-spacing="1">CHIQUITO</text>
</g>'''
kf("led", [(0, "opacity:1"), (.3, "opacity:.2"), (.5, "opacity:1"), (1.1, "opacity:.3"), (1.4, "opacity:1")], dur=1.4)
coffee = f'''<g transform="translate(870 {DESK})">
  {shadow(0, 0, 20, .55)}
  <rect x="-15" y="-28" width="30" height="28" rx="4" fill="#ECE3D6"/><path d="M15 -22 a8 8 0 0 1 0 15" fill="none" stroke="#ECE3D6" stroke-width="4"/>
  <rect x="-15" y="-28" width="30" height="5" rx="2" fill="#4A2E20"/>
  {"".join(f'<path d="M{dx} -34 c-6 -8 6 -14 0 -22" fill="none" stroke="#F4E6D6" stroke-width="2.2" stroke-linecap="round" class="steam" style="animation-delay:{d}s"/>' for dx, d in ((-5, 0), (4, 1), (-1, 2)))}
</g>'''
kf("steam", [(0, "opacity:0;transform:translateY(4px)"), (1, "opacity:.7"), (3, "opacity:0;transform:translateY(-14px)")], dur=3)
controller = f'''<g transform="translate(1080 {SHELF})">
  {shadow(0, 0, 34, .5)}
  <path d="M-30 -8 C-36 -8 -38 -18 -32 -22 C-26 -26 -16 -24 -10 -22 L10 -22 C16 -24 26 -26 32 -22 C38 -18 36 -8 30 -8 C24 -8 20 -12 14 -14 L-14 -14 C-20 -12 -24 -8 -30 -8Z" fill="#1B1A22"/>
  <circle cx="-20" cy="-17" r="3.2" fill="#2E2C36"/><circle cx="8" cy="-16" r="2.6" fill="#2E2C36"/>
  <g><circle cx="22" cy="-19" r="1.6" fill="#4ADE80"/><circle cx="26" cy="-16" r="1.6" fill="#F87171"/><circle cx="18" cy="-16" r="1.6" fill="#60A5FA"/><circle cx="22" cy="-13" r="1.6" fill="#FBBF24"/></g>
  <rect x="-4" y="-22" width="8" height="2" rx="1" fill="#9B6BFF" class="ctrlLed"/>
</g>'''
kf("ctrlLed", [(0, "opacity:1"), (1, "opacity:.3"), (2, "opacity:1")], dur=2)
keyboard = f'''<g transform="translate(640 {DESK})">
  {shadow(0, 0, 100, .5)}
  <rect x="-96" y="-12" width="192" height="12" rx="3" fill="#1A1820"/>
  <g class="kb">{"".join(f'<rect x="{-90 + c * 12}" y="{-10 + r * 3.6:.1f}" width="10" height="2.6" rx=".8" fill="url(#rgb)"/>' for r in range(3) for c in range(15))}</g>
  <rect x="110" y="-8" width="14" height="8" rx="4" fill="#1A1820"/>
</g>'''
pc = f'''<g transform="translate(1212 {DESK})">
  {shadow(0, 0, 32, .55)}
  <rect x="-26" y="-118" width="52" height="118" rx="5" fill="#141218"/>
  <rect x="-20" y="-110" width="4" height="102" rx="2" fill="url(#rgbV)" class="rgbPulse"/>
  <circle cx="6" cy="-96" r="8" fill="none" stroke="#2A2731" stroke-width="2"/><circle cx="6" cy="-66" r="8" fill="none" stroke="#2A2731" stroke-width="2"/>
</g>'''
kf("rgbPulse", [(0, "opacity:1"), (2, "opacity:.55"), (4, "opacity:1")], dur=4)

# side screen with the paused game (on its own stand)
SX, SY, SW, SH = 980, 330, 196, 112
game = f'''<g>
  <rect x="{SX + SW / 2 - 4}" y="{SY + SH}" width="8" height="{DESK - SY - SH - 4}" fill="#2A2730"/>
  <rect x="{SX + SW / 2 - 26}" y="{DESK - 5}" width="52" height="5" rx="2" fill="#2A2730"/>{shadow(SX + SW / 2, DESK, 30, .5)}
  <rect x="{SX - 5}" y="{SY - 5}" width="{SW + 10}" height="{SH + 10}" rx="5" fill="#0B0A0E"/>
  <clipPath id="gC"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}"/></clipPath>
  <g clip-path="url(#gC)">
    <rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#7EC4E8"/>
    <path d="M{SX} {SY + 74} q34 -26 68 0 q34 -20 68 0 q30 -14 60 -4 V{SY + SH} H{SX}Z" fill="#3E8E4E"/>
    <rect x="{SX}" y="{SY + 90}" width="{SW}" height="{SH - 90}" fill="#8B5A2B"/>
    <rect x="{SX + 108}" y="{SY + 52}" width="15" height="15" fill="#B4763A"/><rect x="{SX + 123}" y="{SY + 52}" width="15" height="15" fill="#E8B04A"/>
    <rect x="{SX + 36}" y="{SY + 72}" width="12" height="18" fill="#D9372E"/>
    <rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#0B0A0E" opacity=".58"/>
    <text x="{SX + SW / 2}" y="{SY + 44}" text-anchor="middle" class="mono" font-size="20" font-weight="800" fill="#FFF" letter-spacing="4">PAUSED</text>
    <g class="mono" font-size="9" fill="#D9D3E0"><text x="{SX + 74}" y="{SY + 64}">Resume</text><text x="{SX + 74}" y="{SY + 78}">Options</text><text x="{SX + 74}" y="{SY + 92}">Quit</text></g>
    <text x="{SX + 62}" y="{SY + 64}" class="mono blink" font-size="9" fill="#FFD27A">▶</text>
  </g>
  <rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#glare)"/>
</g>'''

# ── ceiling LEDs: round downlights, mirrored around x = 640 ──
downlights = "".join(
    f'<path d="M{x - 14} 14 L{x - 120} {DESK} L{x + 120} {DESK} L{x + 14} 14Z" fill="url(#downlight)"/>'
    f'<ellipse cx="{x}" cy="12" rx="16" ry="4" fill="#3A3036"/><ellipse cx="{x}" cy="12" rx="11" ry="2.6" fill="#FFF3DC"/>'
    f'<ellipse cx="{x}" cy="13" rx="22" ry="6" fill="#FFE2B8" opacity=".25"/>'
    for x in (202, 446, 834, 1078))

# ── right wall: the TV high up; one shelf with the football, the controller and the NAS ──
shelves = f"""
  <rect x="950" y="{SHELF}" width="290" height="8" fill="#4A3226"/><rect x="950" y="{SHELF + 8}" width="290" height="4" fill="#000" opacity=".35"/>
  <g transform="translate(1000 {SHELF})">{shadow(0, 0, 26, .55)}
    <clipPath id="ballC"><circle cx="0" cy="-25" r="25"/></clipPath>
    <circle cx="0" cy="-25" r="25" fill="#F6F4EE"/>
    <g clip-path="url(#ballC)" fill="#1C1A1F">
      <path d="M0 -34 l8.6 6.2 l-3.3 10.1 h-10.6 l-3.3 -10.1Z"/>
      <path d="M0 -50 l8 0 l3 -8 l-11 -6 l-11 6 l3 8Z"/>
      <path d="M0 -41 l6.6 -4.6 l-2.5 -7.8 h-8.2 l-2.5 7.8Z"/>
      <path d="M24 -36 l-4 8 l7 6 l8 -8 l-4 -10Z"/>
      <path d="M-24 -36 l4 8 l-7 6 l-8 -8 l4 -10Z"/>
      <path d="M14 -4 l-8 -4 l2 -9 l11 -1 l4 10Z"/>
      <path d="M-14 -4 l8 -4 l-2 -9 l-11 -1 l-4 10Z"/>
    </g>
    <g fill="none" stroke="#8C8A90" stroke-width="1" clip-path="url(#ballC)">
      <path d="M0 -34 V-41 M6.6 -45.6 L16 -46 M-6.6 -45.6 L-16 -46 M8.6 -27.8 L20 -30 M5.3 -17.7 L10 -8 M-5.3 -17.7 L-10 -8 M-8.6 -27.8 L-20 -30"/></g>
    <circle cx="0" cy="-25" r="25" fill="url(#ballShade)"/>
  </g>
"""
TVX, TVY, TVW, TVH = 968, 60, 220, 126          # a bit bigger than the game screen, centred over it (x = 1078)
sxp, syp = TVW / 170, TVH / 70
players = "".join(f'<circle cx="{TVX + px * sxp:.1f}" cy="{TVY + 6 + py * syp * .92:.1f}" r="3" fill="{c}" class="pl{i % 4}"/>' for i, (px, py, c) in enumerate(
    [(30, 30, "#FFF"), (60, 50, "#FFF"), (90, 26, "#FFF"), (120, 44, "#FFF"), (44, 56, "#C4B5FD"), (80, 40, "#C4B5FD"), (110, 22, "#C4B5FD"), (146, 50, "#C4B5FD")]))
for k in range(4):
    dx, dy = [(9, -5), (-7, 6), (8, 7), (-9, -6)][k]
    kf(f"pl{k}", [(0, "transform:none"), (6, f"transform:translate({dx}px,{dy}px)"), (12, "transform:none"), (18, f"transform:translate({-dx}px,{dy}px)"), (24, "transform:none")], ease="ease-in-out")
tv = f'''<g>
  <rect x="{TVX - 6}" y="{TVY - 6}" width="{TVW + 12}" height="{TVH + 12}" rx="5" fill="#0B0A0E"/>
  <rect x="{TVX + TVW / 2 - 14}" y="{TVY + TVH + 6}" width="28" height="4" fill="#1A1820"/>
  <rect x="{TVX}" y="{TVY}" width="{TVW}" height="{TVH}" fill="#2F7D3A"/>
  <g fill="#3A8C45">{"".join(f'<rect x="{TVX + i * TVW / 6:.1f}" y="{TVY}" width="{TVW / 12:.1f}" height="{TVH}"/>' for i in range(6))}</g>
  <g fill="none" stroke="#E8F5E8" stroke-width="1.2" opacity=".85">
    <rect x="{TVX + 8}" y="{TVY + 16}" width="{TVW - 16}" height="{TVH - 22}"/><path d="M{TVX + TVW / 2} {TVY + 16} V{TVY + TVH - 6}"/>
    <circle cx="{TVX + TVW / 2}" cy="{TVY + TVH / 2 + 5}" r="15"/>
    <rect x="{TVX + 8}" y="{TVY + TVH / 2 - 14}" width="20" height="38"/><rect x="{TVX + TVW - 28}" y="{TVY + TVH / 2 - 14}" width="20" height="38"/></g>
  {players}<circle cx="{TVX + TVW * .52:.1f}" cy="{TVY + TVH * .56:.1f}" r="2.6" fill="#FFF7D6" class="fball"/>
  <rect x="{TVX + 5}" y="{TVY + 3}" width="122" height="14" rx="2" fill="#0B0A0E" opacity=".92"/>
  <text x="{TVX + 10}" y="{TVY + 13.5}" class="mono" font-size="9" font-weight="700" fill="#FFF">RMA <tspan class="sc1">2</tspan><tspan class="sc2" dx="-5.4">3</tspan>-1 <tspan fill="#C4B5FD">ATM</tspan></text>
  <text x="{TVX + 100}" y="{TVY + 13.5}" class="mono" font-size="8.5" fill="#9BE39B">88'</text>
  <g class="goal"><rect x="{TVX + TVW / 2 - 54}" y="{TVY + TVH / 2 - 16}" width="108" height="36" rx="5" fill="#FFD23F"/>
    <text x="{TVX + TVW / 2}" y="{TVY + TVH / 2 + 10}" text-anchor="middle" class="disp" font-size="24" font-weight="900" fill="#14101A">GOAL!</text></g>
</g>'''
kf("fball", [(0, "transform:none"), (6, "transform:translate(34px,-16px)"), (12, "transform:translate(-24px,14px)"), (17.5, "transform:translate(66px,-2px)"), (18.2, "transform:translate(82px,-2px)"), (24, "transform:none")], ease="ease-in-out")
kf("goal", [(0, "opacity:0;transform:scale(.6)"), (18.2, "opacity:0;transform:scale(.6)"), (18.6, "opacity:1;transform:scale(1.06)"), (19, "opacity:1;transform:none"), (21.5, "opacity:1;transform:none"), (22, "opacity:0"), (24, "opacity:0")],
   extra="transform-box:fill-box;transform-origin:center")
kf("sc1", [(0, "opacity:1"), (18.5, "opacity:1"), (18.6, "opacity:0"), (23.9, "opacity:0"), (24, "opacity:1")])
kf("sc2", [(0, "opacity:0"), (18.5, "opacity:0"), (18.6, "opacity:1"), (23.9, "opacity:1"), (24, "opacity:0")])

# ── desk, LED strip, floor, guitar ────────────────────────────────────────────
desk = f'''
  <rect x="96" y="{DESK}" width="{W - 96}" height="16" fill="url(#deskTop)"/>
  <rect x="96" y="{DESK + 16}" width="{W - 96}" height="4" fill="url(#ledStrip)" class="ledStrip"/>
  <rect x="96" y="{DESK + 20}" width="{W - 96}" height="{FLOOR - DESK - 20}" fill="url(#underDesk)"/>
  <rect x="0" y="{FLOOR}" width="{W}" height="{H - FLOOR}" fill="url(#floorG)"/>
  <rect x="96" y="{FLOOR}" width="{W - 96}" height="10" fill="url(#ledFloor)" opacity=".5"/>
'''
kf("ledStrip", [(0, "filter:hue-rotate(0deg)"), (12, "filter:hue-rotate(40deg)"), (24, "filter:hue-rotate(0deg)")])
guitar = f'''<g transform="translate(58 {FLOOR + 22})">
  {shadow(0, 0, 46, .6)}
  <path d="M-34 0 L-6 -46 M34 0 L6 -46 M0 0 L0 -40" stroke="#2A2731" stroke-width="4" stroke-linecap="round"/>
  <path d="M-12 -48 Q0 -40 12 -48" fill="none" stroke="#2A2731" stroke-width="5" stroke-linecap="round"/>
  <g transform="rotate(-6 0 -50)">
    <rect x="-3.5" y="-330" width="9" height="190" rx="3" fill="#5A3A28"/>
    <g fill="#C9B79F">{"".join(f'<rect x="-3.5" y="{-300 + i * 24}" width="9" height="1.2"/>' for i in range(7))}</g>
    <rect x="-9" y="-356" width="20" height="28" rx="4" fill="#3A2418"/>
    <g fill="#D9CDB8">{"".join(f'<circle cx="-12" cy="{-350 + i * 8}" r="2.2"/><circle cx="14" cy="{-350 + i * 8}" r="2.2"/>' for i in range(3))}</g>
    <path d="M1 -152 C-44 -152 -50 -110 -32 -90 C-54 -64 -50 -6 1 -6 C52 -6 56 -64 34 -90 C52 -110 46 -152 1 -152Z" fill="url(#guitarG)"/>
    <path d="M1 -152 C-44 -152 -50 -110 -32 -90 C-54 -64 -50 -6 1 -6" fill="none" stroke="#FFD9A8" stroke-width="1.5" opacity=".35"/>
    <circle cx="1" cy="-96" r="14" fill="#1E120C"/><circle cx="1" cy="-96" r="17" fill="none" stroke="#3A2418" stroke-width="2"/>
    <rect x="-15" y="-42" width="32" height="6" rx="2" fill="#2A1A12"/>
    <g stroke="#EFE6D6" stroke-width=".7" opacity=".85">{"".join(f'<path d="M{-3.2 + i * 1.7:.1f} -350 V-40"/>' for i in range(6))}</g>
  </g>
</g>'''

css.append("""
  .mono{font-family:'Cascadia Code','SF Mono',Consolas,'Liberation Mono',monospace}
  .disp{font-family:'Segoe UI Variable Display','Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif}
  .blink{animation:blinkC 1s steps(1) infinite}@keyframes blinkC{50%{opacity:0}}
  .lampLight{animation:lampL 6s ease-in-out infinite alternate}@keyframes lampL{to{opacity:.85}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}}
""")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Daily life: Moe's room at dusk, seen from behind his chair. Through a steel window, Teide with the town lights at its foot and the moon over the sea; a tortoiseshell cat sleeps on the sill. Four monitors on one arm show the Sasuke Lens notch, an L2 service-desk queue where a VPN ticket gets resolved, code being built with an AI assistant until it deploys, and an anime with subtitles. A small TV on the shelf shows a football match ending in a goal, a side screen has a paused game, and the desk holds a lamp, a dragon tree, a speaker playing music, the home NAS, a coffee, a game controller and the PC. A guitar stands on its floor stand.">
  <defs>
    <linearGradient id="wallG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2128"/><stop offset="1" stop-color="#1A1519"/></linearGradient>
    <radialGradient id="vignette" cx="50%" cy="40%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
    <linearGradient id="duskG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1230"/><stop offset=".55" stop-color="#3A2A62"/><stop offset=".8" stop-color="#B2506E"/><stop offset="1" stop-color="#F08A5A"/></linearGradient>
    <radialGradient id="sunsetGlow"><stop offset="0" stop-color="#FF9A5A" stop-opacity=".75"/><stop offset="1" stop-color="#FF9A5A" stop-opacity="0"/></radialGradient>
    <linearGradient id="hazeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C77A9A" stop-opacity="0"/><stop offset="1" stop-color="#C77A9A" stop-opacity=".45"/></linearGradient>
    <linearGradient id="nightSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2450"/><stop offset="1" stop-color="#0E0C22"/></linearGradient>
    <linearGradient id="deskSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A1E5E"/><stop offset=".6" stop-color="#C2506A"/><stop offset="1" stop-color="#FFB46B"/></linearGradient>
    <linearGradient id="animeSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121640"/><stop offset="1" stop-color="#2E2A6A"/></linearGradient>
    <linearGradient id="glare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".07"/><stop offset=".4" stop-color="#FFF" stop-opacity="0"/></linearGradient>
    <linearGradient id="deskTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E4A34"/><stop offset="1" stop-color="#4A3022"/></linearGradient>
    <linearGradient id="ledStrip" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A3D"/><stop offset=".5" stop-color="#FF4FA8"/><stop offset="1" stop-color="#9B6BFF"/></linearGradient>
    <linearGradient id="underDesk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2030"/><stop offset=".25" stop-color="#1A1219"/><stop offset="1" stop-color="#120E13"/></linearGradient>
    <linearGradient id="ledFloor" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A3D" stop-opacity=".5"/><stop offset=".5" stop-color="#FF4FA8" stop-opacity=".5"/><stop offset="1" stop-color="#9B6BFF" stop-opacity=".5"/></linearGradient>
    <linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E1618"/><stop offset="1" stop-color="#120D0F"/></linearGradient>
    <linearGradient id="guitarG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E8A04A"/><stop offset=".6" stop-color="#B8642A"/><stop offset="1" stop-color="#5A2C14"/></linearGradient>
    <linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD9A0" stop-opacity=".55"/><stop offset="1" stop-color="#FFD9A0" stop-opacity=".04"/></linearGradient>
    <linearGradient id="sideLight" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFB46B" stop-opacity=".18"/><stop offset=".5" stop-color="#FFB46B" stop-opacity="0"/></linearGradient>
    <linearGradient id="rgb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A3D"/><stop offset=".5" stop-color="#FF4FA8"/><stop offset="1" stop-color="#9B6BFF"/></linearGradient>
    <linearGradient id="rgbV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9B6BFF"/><stop offset=".5" stop-color="#FF4FA8"/><stop offset="1" stop-color="#FF8A3D"/></linearGradient>
    <radialGradient id="monGlow" cx="50%" cy="45%" r="50%"><stop offset="0" stop-color="#6B7CFF" stop-opacity=".16"/><stop offset="1" stop-color="#6B7CFF" stop-opacity="0"/></radialGradient>
    <radialGradient id="ballShade" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#FFF" stop-opacity=".35"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
    <linearGradient id="daySky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E86D8"/><stop offset="1" stop-color="#BFE1F4"/></linearGradient>
    <linearGradient id="atlantic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E5FA8"/><stop offset=".5" stop-color="#2A8FC0"/><stop offset="1" stop-color="#4CC3C9"/></linearGradient>
    <linearGradient id="blackSand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4340"/><stop offset="1" stop-color="#2A2524"/></linearGradient>
    <linearGradient id="glassTint" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".08"/><stop offset=".5" stop-color="#FFF" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></linearGradient>
    <linearGradient id="alpenglow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3A27E"/><stop offset=".55" stop-color="#E9A0AE"/><stop offset="1" stop-color="#9FC2DA"/></linearGradient>
    <linearGradient id="synth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B0B3A"/><stop offset=".55" stop-color="#5A1E6E"/><stop offset="1" stop-color="#E8566C"/></linearGradient>
    <linearGradient id="synthSun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE66B"/><stop offset=".6" stop-color="#FF8A5C"/><stop offset="1" stop-color="#FF3D8A"/></linearGradient>
    <linearGradient id="paperShade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF" stop-opacity=".12"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
    <linearGradient id="nightPoster" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1226"/><stop offset=".7" stop-color="#1A1F3C"/><stop offset="1" stop-color="#2A2142"/></linearGradient>
    <linearGradient id="heroPoster" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101428"/><stop offset=".7" stop-color="#171A33"/><stop offset="1" stop-color="#221C3A"/></linearGradient>
    <pattern id="heroDots" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".75" fill="#FFF" opacity=".1"/></pattern>
    <radialGradient id="downlight" cx="50%" cy="0%" r="100%"><stop offset="0" stop-color="#FFE2B8" stop-opacity=".22"/><stop offset="1" stop-color="#FFE2B8" stop-opacity="0"/></radialGradient>
    <filter id="mottle" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <style>{"".join(css)}</style>
  </defs>
  <g clip-path="url(#frame)">
    {wall}{beams}
    {downlights}
    <ellipse cx="640" cy="200" rx="380" ry="230" fill="url(#monGlow)"/>
    {posters}
    {shelves}
    {tv}
    {arm}
    {monitors}
    {game}
    {desk}
    {speaker}{cat}
    {keyboard}{drago}{coffee}{speaker2}{pc}
    {nas}{controller}
    {guitar}
    {person}
    {chair}
  </g>
</svg>
'''
with open("daily-life.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("ok", len(svg) // 1024, "KB")
