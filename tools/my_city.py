"""'My City' hero, v3.

Opens as a GitHub contribution graph + activity list (the disguise). The lit
squares fly down and become the windows of a Canarian town on the hillside,
which ends in a beach cove. A golden-hour sky and a striped sun rise, Teide
appears above the sea of clouds, the coast road slides in above the sea and a
red Clio IV drives in. Then a slow loop of career signs (green), hobby signs
(brown, like Spanish tourist signs), app billboards and a motorway exit sign
for AI that leads into a short tunnel; the route starts over after it.
Five cats live along the way.
"""
import random
from xml.sax.saxutils import escape as esc
from PIL import ImageFont

W, H = 1280, 820
ROAD_TOP, ROAD_BOT = 596, 714
LANE_Y = (ROAD_TOP + ROAD_BOT) // 2     # centre line
CAR_GROUND = 690                        # wheels touch the near lane here
SIDE = 718                              # pavement top (in front of the road)
SEA_Y = 752
INTRO = 5.0
V = 110                                 # road speed, px/s

FONT_B = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 100)
FONT_M = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 100)


def tw(s, fs, mono=False, spacing=0.0):
    f = FONT_M if mono else FONT_B
    return f.getlength(s) * fs / 100 + spacing * len(s)


THEMES = {
    "light": dict(l=["#EFF2F5", "#ACEEBB", "#4AC26B", "#2DA44E", "#116329"], text="#59636E", strong="#1F2328", line="#D1D9E0"),
    "dark": dict(l=["#151B23", "#033A16", "#196C2E", "#2EA043", "#56D364"], text="#9198A1", strong="#F0F6FC", line="#3D444D"),
}
WIN = ["#000", "#F7B25A", "#FFC774", "#FFD893", "#FFE9BC"]

rng = random.Random(23)

# ── the disguise: contribution graph ──────────────────────────────────────────
COLS, ROWS, CELL, PITCH = 36, 7, 26, 33
GX, GY = 96, 120
LEVELS = [[(rng.choice([1, 1, 2, 2, 3, 4]) if rng.random() > 0.55 else 0) for _ in range(ROWS)] for _ in range(COLS)]

# ── the town ──────────────────────────────────────────────────────────────────
FACADES = ["#F4E8D4", "#EDC07A", "#E39A74", "#F7DDB0", "#D9E2CF", "#F1D3C3", "#FAF3E6", "#E7B9A0"]
SHUTTERS = ["#3F6E4C", "#6E4428", "#2F5F78"]
TOWN_RIGHT = 880                         # the beach cove starts here
houses = []


def make_row(y_base, s, x_from, x_to, count, spread=1.0):
    xs, x = [], x_from
    while len(xs) < count and x < x_to:
        xs.append(x)
        x += int(rng.choice([64, 74, 84, 96]) * s * spread) + rng.randint(-6, 10)
    for x in xs:
        w = int(rng.choice([58, 66, 76, 86]) * s)
        floors = rng.choice([1, 2, 2, 3])
        h = int((26 + 22 * floors) * s)
        cols = max(1, int(w / (22 * s)))
        win = []
        for f in range(floors):
            for c in range(cols):
                wx = x + (w - cols * 20 * s) / 2 + c * 20 * s + 4 * s
                wy = y_base - h + 13 * s + f * 22 * s
                win.append((wx, wy, 11 * s))
        roof = rng.choice(["flat", "flat", "tank", "solar", "tiles"])
        houses.append(dict(x=x, y=y_base, w=w, h=h, col=rng.choice(FACADES), win=win, s=s, roof=roof,
                           shutter=rng.choice(SHUTTERS), balcony=floors >= 2 and rng.random() < .45, door=s > .85))


make_row(560, 0.6, 60, 380, 3, spread=2.6)      # scattered under Teide
make_row(590, 0.8, 20, 360, 3, spread=2.4)
make_row(526, 0.62, 440, TOWN_RIGHT - 30, 9)    # the town, in the middle
make_row(558, 0.78, 420, TOWN_RIGHT - 10, 7)
make_row(596, 0.96, 400, TOWN_RIGHT + 10, 5)
houses[:] = [h_ for h_ in houses if h_["x"] + h_["w"] <= 840]
SLOTS = [w for hs in houses for w in hs["win"]]
rng.shuffle(SLOTS)

# ── signs (kind, small, big lines) in driving order ───────────────────────────
SIGNS = [
    ("career", "2015", ["Retail & customer service"]),
    ("hobby", "HOBBY", ["Gym"]),
    ("board", "Kanbate", ["self-hosted kanban board"]),
    ("career", "2023", ["Technical Support L1"]),
    ("hobby", "HOBBY", ["Board games"]),
    ("board", "Kage", ["reminders, by voice"]),
    ("career", "2024", ["L2 Support · Incident manager", "Lead Management"]),
    ("hobby", "HOBBY", ["Series · Films · Anime"]),
    ("board", "PRM", ["never miss a payment"]),
    ("exit", "NEXT EXIT", ["AI"]),
]
GAP = 6.5
SIGN_FROM, SIGN_TO = W + 30, -720
SIGN_T = (SIGN_FROM - SIGN_TO) / V
TUNNEL_L = 700
TUNNEL_AT = len(SIGNS) * GAP + 3.0
CAR_X, CAR_W = 250, 300
EXIT_PASS = (len(SIGNS) - 1) * GAP + (SIGN_FROM - (CAR_X + 150)) / V   # exit sign alongside the car
LEAVE, BACK = 2.4, 2.4
EXIT_GONE = (len(SIGNS) - 1) * GAP + (SIGN_FROM + 360) / V             # exit sign fully off the left edge
EMPTY = EXIT_GONE + 1.0 - (EXIT_PASS + 0.6 + LEAVE)                     # Clio stays away until then (+1 s)
CYCLE = EXIT_PASS + 0.6 + LEAVE + EMPTY + BACK                          # then 2015 comes round again
TUNNEL_T = (SIGN_FROM + TUNNEL_L + 60) / V

# ── cats ──────────────────────────────────────────────────────────────────────
CATS = {   # base, patch, belly
    "ginger": ("#D27A34", "#F2B27A", "#F6D3A8"),
    "grey": ("#7F838F", "#B3B7C2", "#D7DAE0"),
    "tuxedo": ("#1E1B22", "#1E1B22", "#F4F1EC"),
    "calico": ("#F3ECE2", "#D6782F", "#2A2226"),
    "cream": ("#E9D7BC", "#B98D62", "#F7EEDF"),
    "tabby": ("#8A6A4A", "#5A4330", "#D9C3A2"),
    "black": ("#1D1A20", "#2C2830", "#3A353D"),
    "siamese": ("#EDE2D0", "#5A4335", "#F6EEE2"),
    "orangewhite": ("#F4EFE8", "#E0873A", "#F4EFE8"),
}


def sitting_cat(kind):
    base, patch, belly = CATS[kind]
    return f'''
      <g class="swish"><path d="M26 -4 C40 -2 44 -16 36 -26" fill="none" stroke="{base}" stroke-width="5.5" stroke-linecap="round"/></g>
      <path d="M2 0 C-1 -16 4 -32 16 -36 C27 -33 32 -18 29 0 Z" fill="{base}"/>
      <path d="M8 0 C6 -12 10 -22 16 -26 C18 -16 18 -8 18 0Z" fill="{belly}" opacity=".95"/>
      <path d="M20 -28 C26 -24 30 -14 28 -6 C24 -12 21 -20 20 -28Z" fill="{patch}" opacity=".9"/>
      <path d="M4 0 h9 v-4 a4 4 0 0 0 -9 0Z M15 0 h9 v-4 a4 4 0 0 0 -9 0Z" fill="{belly}"/>
      <circle cx="12" cy="-42" r="11" fill="{base}"/>
      <path d="M3 -47 L2 -60 L11 -52Z M14 -52 L22 -60 L22 -46Z" fill="{base}"/>
      <path d="M14 -51 C18 -50 22 -46 22 -40 C18 -43 15 -46 14 -51Z" fill="{patch}" opacity=".9"/>
      <path d="M8 -38 C10 -34 14 -34 16 -38 C14 -36 10 -36 8 -38Z" fill="{belly}"/>
      <path d="M4 -49 L4 -56 L8 -51Z" fill="#E7A2A0" opacity=".8"/>
      <circle cx="7.5" cy="-43" r="1.8" fill="#9BD15A"/><circle cx="15.5" cy="-43" r="1.8" fill="#9BD15A"/>
      <path d="M10 -39 l1.5 1.4 l1.5 -1.4" fill="none" stroke="#2A1A1A" stroke-width="1"/>'''


def sleeping_cat(kind):
    base, patch, belly = CATS[kind]
    return f'''
      <ellipse cx="34" cy="-13" rx="32" ry="14" fill="{base}"/>
      <path d="M30 -24 C40 -28 54 -22 58 -12 C48 -16 38 -18 30 -24Z" fill="{patch}" opacity=".9"/>
      <circle cx="14" cy="-14" r="11" fill="{base}"/>
      <path d="M6 -21 L4 -31 L13 -24Z M15 -25 L22 -33 L23 -20Z" fill="{base}"/>
      <path d="M8 -13 q3 2 6 0" fill="none" stroke="#2A1A1A" stroke-width="1.3" stroke-linecap="round"/>
      <path d="M4 -4 C20 2 40 2 60 -4" fill="none" stroke="{base}" stroke-width="6" stroke-linecap="round"/>
      <path d="M50 -6 C54 -6 58 -8 60 -4" fill="none" stroke="{patch}" stroke-width="6" stroke-linecap="round"/>
      <g class="zzz"><text x="20" y="-34" class="disp" font-size="13" font-weight="700" fill="#FFF1DA">z</text><text x="28" y="-46" class="disp" font-size="10" font-weight="700" fill="#FFF1DA">z</text></g>'''


def football_cat(kind):
    """A crouching cat batting a football back and forth."""
    base, patch, belly = CATS[kind]
    ball = ('<g class="ball"><g class="roll"><circle r="9" fill="#F7F7F2" stroke="#2A2328" stroke-width="1.2"/>'
            '<path d="M0 -3.5 l3.3 2.4 l-1.3 3.9 h-4 l-1.3 -3.9Z" fill="#1E1A1F"/>'
            '<path d="M0 -9 V-3.5 M3.3 -1.1 L8.5 -2.8 M2 2.8 L5.3 7.2 M-2 2.8 L-5.3 7.2 M-3.3 -1.1 L-8.5 -2.8" stroke="#1E1A1F" stroke-width="1.1"/></g></g>')
    return f'''
      <g transform="translate(-30 -9)">{ball}</g>
      <g class="swish"><path d="M48 -10 C62 -12 66 -26 58 -34" fill="none" stroke="{base}" stroke-width="5.5" stroke-linecap="round"/></g>
      <path d="M4 0 C2 -14 14 -26 30 -26 C44 -26 52 -16 50 0Z" fill="{base}"/>
      <path d="M30 -26 C40 -26 48 -20 50 -10 C42 -16 36 -20 30 -26Z" fill="{patch}" opacity=".9"/>
      <g class="paw"><path d="M6 -8 C-2 -10 -10 -10 -16 -6" fill="none" stroke="{base}" stroke-width="6" stroke-linecap="round"/><circle cx="-16" cy="-6" r="3.6" fill="{belly}"/></g>
      <circle cx="6" cy="-26" r="11" fill="{base}"/>
      <path d="M-3 -31 L-5 -43 L4 -35Z M8 -36 L15 -44 L16 -30Z" fill="{base}"/>
      <path d="M0 -21 C2 -18 6 -18 8 -21 C6 -19 2 -19 0 -21Z" fill="{belly}"/>
      <circle cx="1" cy="-27" r="1.9" fill="#F2C94C"/><circle cx="9" cy="-27" r="1.9" fill="#F2C94C"/>
      <circle cx="1.5" cy="-27" r=".9" fill="#1E1A1F"/><circle cx="9.5" cy="-27" r=".9" fill="#1E1A1F"/>'''


# ── signs ─────────────────────────────────────────────────────────────────────
def sign_svg(kind, small, big):
    base = ROAD_TOP - 8
    if kind == "board":
        w = max(tw(small, 34), tw(big[0], 16, mono=True)) + 56
        h, top = 104, base - 220
        nap = f'<g transform="translate({w*0.55:.0f} {top + 1})">{sleeping_cat("black")}</g>' if small == "Kage" else ""
        return (nap +f'<rect x="{w/2-6:.0f}" y="{top+h}" width="12" height="{base-top-h}" fill="#3B2A35"/>'
                f'<rect x="0" y="{top}" width="{w:.0f}" height="{h}" rx="10" fill="#1A0E26" stroke="#FF5CB4" stroke-width="3" filter="url(#neon)"/>'
                f'<text x="{w/2:.0f}" y="{top+52}" text-anchor="middle" class="disp" font-size="34" font-weight="800" fill="#FFE6F5" filter="url(#neon)">{esc(small)}</text>'
                f'<text x="{w/2:.0f}" y="{top+82}" text-anchor="middle" class="mono" font-size="16" fill="#FFA6DA">{esc(big[0])}</text>')
    if kind == "exit":
        ink = "#FFFFFF"
        text_w = max(tw(small, 17, mono=True, spacing=2), tw(big[0], 64))
        w, h = int(118 + text_w + 46), 150
        top = base - 70 - h
        return (f'<rect x="{w*0.22:.0f}" y="{top+h}" width="9" height="{base-top-h}" fill="#5C5560"/>'
                f'<rect x="{w*0.78-9:.0f}" y="{top+h}" width="9" height="{base-top-h}" fill="#5C5560"/>'
                f'<rect x="0" y="{top}" width="{w}" height="{h}" rx="12" fill="#1B5FB4"/>'
                f'<rect x="6" y="{top+6}" width="{w-12}" height="{h-12}" rx="8" fill="none" stroke="{ink}" stroke-width="3"/>'
                f'<g transform="translate(26 {top+28})" fill="none" stroke="{ink}" stroke-width="9" stroke-linecap="round">'
                f'<path d="M26 92 V8"/><path d="M26 66 C26 44 50 40 66 22"/><path d="M52 18 L68 20 L66 36" stroke-width="7" stroke-linejoin="round"/></g>'
                f'<text x="118" y="{top+54}" class="mono" font-size="17" font-weight="700" fill="{ink}" letter-spacing="2">{esc(small)}</text>'
                f'<text x="116" y="{top+118}" class="disp" font-size="64" font-weight="800" fill="{ink}" letter-spacing="-1">{esc(big[0])}</text>'
                f'<g transform="translate({w-70} {top})">{sitting_cat("tuxedo")}</g>')
    fill, ink, sub = {"career": ("#0E7A43", "#FFFFFF", "#CFF5DD"), "hobby": ("#7A4524", "#FFFFFF", "#F7DCC4")}[kind]
    fs, pad = 28, 26
    w = max(max(tw(b, fs) for b in big), tw(small, 15, mono=True, spacing=1.6)) + 2 * pad
    h = 54 + 34 * len(big)
    top = base - 70 - h
    lines = "".join(f'<text x="{pad}" y="{top+60+34*j}" class="disp" font-size="{fs}" font-weight="700" fill="{ink}">{esc(b)}</text>' for j, b in enumerate(big))
    cat = ""
    if big == ["Gym"]:
        cat = f'<g transform="translate({w*0.6:.0f} {top})">{sitting_cat("ginger")}</g>'
    if small == "2023":
        cat = f'<g transform="translate({w*0.14:.0f} {top})">{sitting_cat("tabby")}</g>'

    return (f'<rect x="{w*0.2:.0f}" y="{top+h}" width="8" height="{base-top-h}" fill="#5C5560"/>'
            f'<rect x="{w*0.8-8:.0f}" y="{top+h}" width="8" height="{base-top-h}" fill="#5C5560"/>'
            f'<rect x="0" y="{top}" width="{w:.0f}" height="{h}" rx="10" fill="{fill}"/>'
            f'<rect x="6" y="{top+6}" width="{w-12:.0f}" height="{h-12}" rx="7" fill="none" stroke="{ink}" stroke-width="2.5"/>'
            f'<text x="{pad}" y="{top+32}" class="mono" font-size="15" font-weight="700" fill="{sub}" letter-spacing="1.6">{esc(small)}</text>'
            + lines + f'<rect x="0" y="{top}" width="{w:.0f}" height="{h}" rx="10" fill="url(#signSheen)"/>' + cat)


# ── tunnel: short, in the road's plane (pavement and sea pass in front) ───────
def tunnel_svg():
    L = TUNNEL_L
    top = 420
    rock = (f'M-6 {ROAD_BOT} L-6 {ROAD_TOP-150} C30 {top+70} 110 {top+8} 230 {top} C360 {top-8} 470 {top+22} 560 {top+44} '
            f'C640 {top+62} {L-6} {top+120} {L+6} {ROAD_TOP-150} L{L+6} {ROAD_BOT} Z')
    lights = "".join(f'<circle cx="{x}" cy="{ROAD_TOP-30}" r="3" fill="#FFB347"/>' for x in range(50, L - 30, 60))
    cracks = ''.join(f'<path d="M{x} {top+40+rng.randint(0,40)} l{rng.randint(-14,14)} {rng.randint(30,60)} l{rng.randint(-10,10)} {rng.randint(20,40)}" fill="none" stroke="#24161E" stroke-width="2" opacity=".6"/>' for x in range(60, L - 40, 70))

    def portal(x, flip=False):
        sx = -1 if flip else 1
        return (f'<g transform="translate({x} 0) scale({sx} 1)">'
                f'<rect x="-14" y="{ROAD_TOP-132}" width="36" height="{ROAD_BOT-ROAD_TOP+132}" fill="#BDB3A9"/>'
                f'<rect x="12" y="{ROAD_TOP-132}" width="10" height="{ROAD_BOT-ROAD_TOP+132}" fill="#8F857C"/>'
                f'<rect x="-20" y="{ROAD_TOP-140}" width="48" height="12" rx="3" fill="#D9D0C6"/></g>')
    return (f'<path d="{rock}" fill="url(#rockG)"/>{cracks}'
            f'<path d="M-6 {ROAD_TOP-150} C30 {top+70} 110 {top+8} 230 {top} C360 {top-8} 470 {top+22} 560 {top+44}" fill="none" stroke="#FF9E6B" stroke-width="3" stroke-opacity=".55"/>'
            f'<path d="M22 {ROAD_BOT} V{ROAD_TOP-40} a60 60 0 0 1 60 -60 H22Z M{L-22} {ROAD_BOT} V{ROAD_TOP-40} a60 60 0 0 0 -60 -60 H{L-22}Z" fill="#0C0812" opacity=".55"/>'
            f'<path d="M30 {ROAD_TOP+10} H{L-30}" stroke="#24171F" stroke-width="3" opacity=".6"/>'
            + ''.join(f'<path d="M{x} {ROAD_TOP-60} q14 -18 30 -6 q10 -14 24 -2" fill="none" stroke="#4E6B3A" stroke-width="5" stroke-linecap="round" opacity=".8"/>' for x in range(120, L - 120, 160))
            + portal(0) + portal(L, flip=True) +
            f'<rect x="-14" y="{ROAD_TOP-176}" width="62" height="28" rx="4" fill="#1B5FB4" stroke="#fff" stroke-width="2"/>'
            f'<text x="17" y="{ROAD_TOP-156}" text-anchor="middle" class="disp" font-size="18" font-weight="800" fill="#fff">AI</text>'
            f'<g transform="translate({L*0.45:.0f} {top + 8})">{sitting_cat("tuxedo")}</g>')


# ── the Clio IV (side view, facing right; 300 x 108, ground at y=108) ─────────
def wheel(cx):
    spokes = "".join(f'<path d="M-2.2 -6 L-3.6 -19 L3.6 -19 L2.2 -6Z" fill="#D7DAE0" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return (f'<g transform="translate({cx} 84)"><circle r="24" fill="#121216"/><circle r="17.5" fill="#2A2C33"/>'
            f'<g class="spin">{spokes}<circle r="5" fill="#9AA0AA"/><circle r="2" fill="#2A2C33"/></g>'
            f'<circle r="17.5" fill="none" stroke="#5B606A" stroke-width="1.2"/></g>')


CAR = f'''
  <ellipse cx="150" cy="107" rx="146" ry="7" fill="#0E0816" opacity=".6"/>
  <path d="M292 60 L470 34 L470 98 L294 74Z" fill="url(#beam)" class="beam"/>
  <path d="M10 88 L6 74 C3 62 5 50 12 42 L22 30 C28 22 36 18 46 16
           L70 10 C96 3 132 1 160 4 C176 6 188 12 198 22 L214 40
           C238 44 262 48 278 54 C292 60 298 68 298 78 L296 90
           L270 92 A30 30 0 0 0 210 92 L106 92 A30 30 0 0 0 46 92 Z" fill="url(#paint)"/>
  <path d="M42 92 A34 34 0 0 1 110 92" fill="none" stroke="#9C0C16" stroke-width="5"/>
  <path d="M206 92 A34 34 0 0 1 274 92" fill="none" stroke="#9C0C16" stroke-width="5"/>
  <path d="M30 26 C38 18 46 16 52 15 L70 10 C96 3 132 1 160 4 C176 6 188 12 198 22" fill="none" stroke="#FFC890" stroke-width="2.5" stroke-opacity=".85"/>
  <path d="M60 38 L54 22 C70 13 100 8 130 7 C152 7 170 10 182 18 L202 40 C160 41 104 42 60 38 Z" fill="url(#glass)"/>
  <path d="M132 7 L134 41" stroke="#B80F1B" stroke-width="5"/>
  <path d="M54 22 L60 38 L50 34 Z" fill="#B80F1B"/>
  <rect x="62" y="24" width="3" height="9" rx="1.5" fill="#7A0A12"/>
  <path d="M134 42 C136 60 136 76 132 90 M206 42 C214 58 214 74 208 86" fill="none" stroke="#86101A" stroke-width="1.5"/>
  <rect x="176" y="50" width="14" height="3.2" rx="1.6" fill="#86101A"/>
  <path d="M112 84 C150 76 190 70 232 64" fill="none" stroke="#FF7A66" stroke-width="2" stroke-opacity=".6"/>
  <path d="M112 86 C150 80 190 76 230 70 L230 78 C190 82 150 86 112 90Z" fill="#6E0710" opacity=".35"/>
  <path d="M196 38 l13 -5 l3 8 l-13 2Z" fill="#C2121D"/><path d="M196 38 l13 -5 l1 3 l-13 4Z" fill="#14121A" opacity=".7"/>
  <path d="M296 62 C284 56 266 52 248 52 C254 58 264 64 288 68Z" fill="#FFF6D6"/>
  <path d="M290 66 C274 64 262 60 252 55" fill="none" stroke="#FFFFFF" stroke-width="1.6"/>
  <path d="M8 46 C12 38 18 32 26 28 L30 38 C24 42 18 48 14 56 L8 56Z" fill="#FF2A3A" filter="url(#tailGlow)"/>
  <path d="M276 82 L298 80 L296 90 L272 92Z" fill="#221C1F"/>
  <path d="M8 80 L24 82 L26 90 L10 88Z" fill="#221C1F"/>
  <path d="M284 70 l3 -4 l3 4 l-3 4Z" fill="#E8E8EE"/>
  {wheel(76)}{wheel(240)}
'''


# ── Canary palm (symbol; trunk base at 0,0, about 150 tall) ───────────────────
def palm_symbol():
    rings = "".join(f'<path d="M{-7 + i*0.18:.1f} {-i*9} l7 -5 l7 5" fill="none" stroke="#5A3A2C" stroke-width="2"/>' for i in range(1, 12))
    fronds = []
    for k, ang in enumerate(range(-170, 10, 14)):
        length = 70 - abs(ang + 80) * 0.18
        droop = 14 + abs(ang + 80) * 0.22
        fronds.append(
            f'<g transform="rotate({ang} 4 -112)"><path d="M4 -112 q{length*0.5:.0f} -{droop*0.4:.0f} {length:.0f} {droop*0.5:.0f} q-{length*0.5:.0f} -{droop*0.1:.0f} -{length:.0f} -{droop*0.25:.0f}Z" fill="{"#3F5E36" if k % 2 else "#4F7440"}"/>'
            f'<path d="M4 -112 q{length*0.5:.0f} -{droop*0.4:.0f} {length:.0f} {droop*0.5:.0f}" fill="none" stroke="#7FA05E" stroke-width="1" opacity=".7"/></g>')
    dates = '<g fill="#E08A2E"><circle cx="-2" cy="-104" r="2.5"/><circle cx="3" cy="-102" r="2.5"/><circle cx="8" cy="-105" r="2.5"/><circle cx="1" cy="-98" r="2.2"/></g>'
    return (f'<symbol id="palm" overflow="visible"><path d="M-8 0 C-6 -40 -4 -80 0 -112 L8 -112 C10 -80 10 -40 9 0Z" fill="#6B4632"/>'
            f'<path d="M3 0 C4 -40 5 -80 6 -112 L8 -112 C10 -80 10 -40 9 0Z" fill="#3F281E" opacity=".6"/>{rings}'
            f'{"".join(fronds)}<ellipse cx="4" cy="-112" rx="12" ry="7" fill="#33502C"/>{dates}</symbol>')


def house_svg(hs):
    x, yb, w, h, s = hs["x"], hs["y"], hs["w"], hs["h"], hs["s"]
    side = 9 * s
    out = [f'<rect x="{x}" y="{yb-h}" width="{w}" height="{h+8}" fill="{hs["col"]}"/>',
           f'<rect x="{x+w-side:.1f}" y="{yb-h}" width="{side:.1f}" height="{h+8}" fill="#2E1A33" opacity=".22"/>',
           f'<rect x="{x}" y="{yb-h}" width="{w}" height="{h+8}" fill="url(#houseShade)"/>']
    roof = hs["roof"]
    if roof == "tiles":
        out.append(f'<path d="M{x-4*s:.1f} {yb-h+1} L{x+w*0.5:.1f} {yb-h-14*s:.1f} L{x+w+4*s:.1f} {yb-h+1}Z" fill="#B65A3C"/>'
                   f'<path d="M{x-4*s:.1f} {yb-h+1} L{x+w*0.5:.1f} {yb-h-14*s:.1f}" stroke="#E08A62" stroke-width="{1.5*s:.1f}"/>')
    else:
        out.append(f'<rect x="{x-1.5:.1f}" y="{yb-h-4*s:.1f}" width="{w+3}" height="{4*s:.1f}" fill="#E9DDCB"/>'
                   f'<rect x="{x-1.5:.1f}" y="{yb-h-0.8:.1f}" width="{w+3}" height="1.6" fill="#8A6A5A" opacity=".5"/>')
        if roof == "tank":
            out.append(f'<rect x="{x+w*0.65:.1f}" y="{yb-h-14*s:.1f}" width="{12*s:.1f}" height="{10*s:.1f}" rx="{2*s:.1f}" fill="#F2F0EA"/>'
                       f'<rect x="{x+w*0.65:.1f}" y="{yb-h-14*s:.1f}" width="{4*s:.1f}" height="{10*s:.1f}" fill="#C9C2B8"/>')
        if roof == "solar":
            out.append(f'<path d="M{x+w*0.18:.1f} {yb-h-4*s:.1f} l{16*s:.1f} -{9*s:.1f} l{5*s:.1f} {9*s:.1f}Z" fill="#2E4A78"/>'
                       f'<path d="M{x+w*0.18:.1f} {yb-h-4*s:.1f} l{16*s:.1f} -{9*s:.1f}" stroke="#8FB2E6" stroke-width="1"/>')
    for (wx, wy, ws) in hs["win"]:   # shutters + sill; the glass itself is a flying square
        out.append(f'<rect x="{wx-3*s:.1f}" y="{wy:.1f}" width="{2.6*s:.1f}" height="{ws:.1f}" fill="{hs["shutter"]}"/>'
                   f'<rect x="{wx+ws+0.4*s:.1f}" y="{wy:.1f}" width="{2.6*s:.1f}" height="{ws:.1f}" fill="{hs["shutter"]}"/>'
                   f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ws:.1f}" height="{ws:.1f}" fill="#4A3036"/>'
                   f'<rect x="{wx-1.5*s:.1f}" y="{wy+ws:.1f}" width="{ws+3*s:.1f}" height="{1.6*s:.1f}" fill="#FFFFFF" opacity=".7"/>')
    if hs["balcony"] and len(hs["win"]) > 1:
        wx, wy, ws = hs["win"][-1]
        out.append(f'<rect x="{wx-5*s:.1f}" y="{wy+ws+1:.1f}" width="{ws+10*s:.1f}" height="{6*s:.1f}" fill="#6B3E22"/>'
                   + "".join(f'<rect x="{wx-4*s+i*3.2*s:.1f}" y="{wy+ws+1:.1f}" width="{1.2*s:.1f}" height="{6*s:.1f}" fill="#3E2214"/>' for i in range(int((ws + 9 * s) / (3.2 * s)))))
    if hs["door"]:
        dx = x + w * 0.5 - 6 * s
        out.append(f'<path d="M{dx:.1f} {yb+8} v-{14*s:.1f} a{6*s:.1f} {6*s:.1f} 0 0 1 {12*s:.1f} 0 v{14*s:.1f}Z" fill="{hs["shutter"]}"/>')
    return "".join(out)


def svg(theme):
    t = THEMES[theme]
    css = [f"""
      .mono{{font-family:'Cascadia Code','SF Mono',Consolas,'Liberation Mono',monospace}}
      .disp{{font-family:'Segoe UI Variable Display','Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif}}
      .gh{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif}}
      @keyframes in{{from{{opacity:0}}to{{opacity:1}}}}
      @keyframes out{{to{{opacity:0}}}}
      .disguise{{animation:out .6s ease 2.1s forwards}}
      .empty{{animation:out .4s ease 2.15s forwards}}
      .sky{{transform-box:view-box;transform-origin:640px 470px;animation:sky 1.2s cubic-bezier(.7,0,.2,1) 2.5s both}}
      @keyframes sky{{from{{transform:scaleY(0);opacity:0}}20%{{opacity:1}}to{{transform:none;opacity:1}}}}
      .sun{{animation:rise 1.6s cubic-bezier(.2,.8,.2,1) 3.0s both}}
      .teide{{animation:rise 1.5s cubic-bezier(.2,.8,.2,1) 3.05s both}}
      @keyframes rise{{from{{transform:translateY(160px);opacity:0}}35%{{opacity:1}}to{{transform:none;opacity:1}}}}
      .clouds{{animation:in 1.2s ease 3.3s both}}
      .drift{{animation:drift 60s linear infinite alternate}}
      @keyframes drift{{to{{transform:translateX(-40px)}}}}
      .hill{{animation:in .9s ease 2.9s both}}
      .houses{{animation:in .8s ease 3.25s both}}
      .stars{{animation:in 1.5s ease 3.6s both}}
      .tw{{animation:twk 3.4s ease-in-out infinite}}
      @keyframes twk{{50%{{opacity:.25}}}}
      .road{{animation:road .8s cubic-bezier(.2,.8,.2,1) 3.7s both}}
      @keyframes road{{from{{transform:translateY(240px);opacity:0}}40%{{opacity:1}}to{{transform:none;opacity:1}}}}
      .car{{animation:carIn 1.3s cubic-bezier(.15,.75,.25,1) 4.1s both}}
      @keyframes carIn{{from{{transform:translateX(-640px);opacity:0}}20%{{opacity:1}}to{{transform:none;opacity:1}}}}
      .bob{{animation:bob .5s ease-in-out infinite alternate}}
      @keyframes bob{{to{{transform:translateY(-1.2px)}}}}
      .spin{{animation:spin .55s linear infinite}}
      @keyframes spin{{to{{transform:rotate(360deg)}}}}
      .beam{{animation:beam 3s ease-in-out infinite alternate}}
      @keyframes beam{{from{{opacity:.5}}to{{opacity:.8}}}}
      .dash{{animation:dash {120/V:.3f}s linear {INTRO}s infinite}}
      @keyframes dash{{to{{transform:translateX(-120px)}}}}
      .palms{{animation:palms {1040/(V*.55):.3f}s linear {INTRO}s infinite}}
      @keyframes palms{{to{{transform:translateX(-1040px)}}}}
      .joints{{animation:joints {160/V:.3f}s linear {INTRO}s infinite}}
      @keyframes joints{{to{{transform:translateX(-160px)}}}}
      .swish{{transform-box:fill-box;transform-origin:0% 100%;animation:swish 2.2s ease-in-out infinite alternate}}
      @keyframes swish{{from{{transform:rotate(-10deg)}}to{{transform:rotate(12deg)}}}}
      .zzz{{animation:zzz 2.8s ease-in-out infinite}}
      @keyframes zzz{{0%{{opacity:0;transform:translateY(4px)}}40%{{opacity:1}}100%{{opacity:0;transform:translateY(-8px)}}}}
      .ball{{animation:ball 1.6s ease-in-out infinite alternate}}
      @keyframes ball{{from{{transform:translateX(-14px)}}to{{transform:translateX(10px)}}}}
      .roll{{animation:roll 1.6s ease-in-out infinite alternate}}
      @keyframes roll{{from{{transform:rotate(-120deg)}}to{{transform:rotate(90deg)}}}}
      .paw{{transform-box:fill-box;transform-origin:100% 50%;animation:paw 1.6s ease-in-out infinite alternate}}
      @keyframes paw{{from{{transform:rotate(14deg)}}to{{transform:rotate(-6deg)}}}}
      .glint{{animation:glint 2.4s ease-in-out infinite alternate}}
      @keyframes glint{{from{{opacity:.35;transform:translateX(-6px)}}to{{opacity:.95;transform:translateX(6px)}}}}
      .waves{{animation:waves 4s ease-in-out infinite alternate}}
      @keyframes waves{{to{{transform:translateX(-10px)}}}}
      .roofcat{{animation:roofcat {CYCLE:.2f}s ease {INTRO}s infinite both}}
      @keyframes roofcat{{0%,8%{{opacity:0}}11%,70%{{opacity:1}}73%,100%{{opacity:0}}}}
    """]

    sq, slot = [], 0
    for c in range(COLS):
        for r in range(ROWS):
            x0, y0 = GX + c * PITCH, GY + r * PITCH
            lvl = LEVELS[c][r]
            if lvl == 0 or slot >= len(SLOTS):
                sq.append(f'<rect x="{x0}" y="{y0}" width="{CELL}" height="{CELL}" rx="5" fill="{t["l"][lvl]}" class="empty"/>')
                continue
            wx, wy, ws = SLOTS[slot]
            slot += 1
            name = f"q{c}_{r}"
            delay = 2.25 + c * 0.018 + r * 0.03
            css.append(f".{name}{{transform-box:view-box;transform-origin:0 0;animation:{name} 1.25s cubic-bezier(.65,0,.25,1) {delay:.3f}s both,w{lvl} .8s ease {delay + .45:.3f}s both}}"
                       f"@keyframes {name}{{from{{transform:translate({x0}px,{y0}px)}}to{{transform:translate({wx:.1f}px,{wy:.1f}px) scale({ws / CELL:.3f})}}}}")
            sq.append(f'<rect width="{CELL}" height="{CELL}" rx="5" class="{name}" fill="{t["l"][lvl]}"/>')
    for lvl in range(1, 5):
        css.append(f"@keyframes w{lvl}{{from{{fill:{t['l'][lvl]}}}to{{fill:{WIN[lvl]}}}}}")

    hs = [house_svg(h_) for h_ in houses]
    hs.append('<g transform="translate(626 0)"><rect x="0" y="466" width="32" height="70" fill="#F6EEDF"/><rect x="24" y="466" width="8" height="70" fill="#2E1A33" opacity=".2"/>'
              '<path d="M-4 466 h40 l-20 -28Z" fill="#B5553A"/><rect x="11" y="478" width="10" height="15" rx="5" fill="#3A2630"/>'
              '<rect x="15" y="428" width="2" height="12" fill="#3A2630"/><rect x="11" y="432" width="10" height="2" fill="#3A2630"/></g>')
    front = max((h_ for h_ in houses if h_["s"] > .9), key=lambda h_: h_["w"])
    roofcat = f'<g class="roofcat"><g transform="translate({front["x"] + front["w"]*0.25:.0f} {front["y"]-front["h"]-4*front["s"]:.0f}) scale(.85)">{sitting_cat("grey")}</g></g>'

    signs = []
    for i, (kind, small, big) in enumerate(SIGNS):
        start = INTRO + i * GAP
        css.append(f".s{i}{{animation:s{i} {CYCLE:.2f}s linear {start:.2f}s infinite both}}"
                   f"@keyframes s{i}{{0%{{transform:translateX({SIGN_FROM}px)}}{SIGN_T / CYCLE * 100:.3f}%{{transform:translateX({SIGN_TO}px)}}100%{{transform:translateX({SIGN_TO}px)}}}}")
        signs.append(f'<g class="s{i}">{sign_svg(kind, small, big)}</g>')
    p1 = (EXIT_PASS + 0.6) / CYCLE * 100
    p2 = (EXIT_PASS + 0.6 + LEAVE) / CYCLE * 100
    p3 = (EXIT_PASS + 0.6 + LEAVE + EMPTY) / CYCLE * 100
    css.append(f".carloop{{animation:carloop {CYCLE:.2f}s linear {INTRO}s infinite}}"
               f"@keyframes carloop{{0%{{transform:none}}"
               f"{p1:.3f}%{{transform:none;animation-timing-function:cubic-bezier(.55,0,.9,.55)}}"
               f"{p2:.3f}%{{transform:translateX(1150px)}}"
               f"{p3:.3f}%{{transform:translateX(1150px)}}"
               f"{p3 + 0.01:.3f}%{{transform:translateX(-760px);animation-timing-function:cubic-bezier(.15,.75,.3,1)}}"
               f"100%{{transform:none}}}}")
    walk_t = (W + 300) / V
    for name, start in (("nap", INTRO + 12), ("perch", INTRO + 25), ("kick", INTRO + 38)):
        css.append(f".{name}{{animation:{name} {CYCLE:.2f}s linear {start:.2f}s infinite both}}"
                   f"@keyframes {name}{{0%{{transform:translateX({W + 140}px)}}{walk_t / CYCLE * 100:.3f}%{{transform:translateX(-160px)}}100%{{transform:translateX(-160px)}}}}")

    activity = "".join(
        f'<g transform="translate({GX} {GY + ROWS * PITCH + 92 + k * 54})"><circle cx="9" cy="-6" r="9" fill="{t["line"]}"/>'
        f'<text x="30" y="0" font-size="17" fill="{t["strong"]}">{txt}</text></g>'
        for k, txt in enumerate(["Created commits in kanbate, kage and prm", "Opened pull requests in 2 repositories", "Created a repository"]))
    months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    mlab = "".join(f'<text x="{GX + k * 4.2 * PITCH:.0f}" y="{GY - 16}">{m}</text>' for k, m in enumerate(months))
    dlab = "".join(f'<text x="{GX - 14}" y="{GY + r * PITCH + 20}" text-anchor="end">{d}</text>' for r, d in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    lx = GX + COLS * PITCH - 5 * 20 - 46
    legend = (f'<text x="{lx - 10}" y="{GY + ROWS * PITCH + 34}" text-anchor="end">Less</text>'
              + "".join(f'<rect x="{lx + k * 20}" y="{GY + ROWS * PITCH + 20}" width="16" height="16" rx="3" fill="{t["l"][k]}"/>' for k in range(5))
              + f'<text x="{lx + 5 * 20 + 6}" y="{GY + ROWS * PITCH + 34}">More</text>')

    stars = "".join(f'<circle cx="{rng.randint(20, W - 20)}" cy="{rng.randint(14, 150)}" r="{rng.choice([1, 1.3, 1.7])}" fill="#FFF3E0" class="tw" style="animation-delay:{rng.random() * 3:.2f}s"/>' for _ in range(30))
    stripes = "".join(f'<rect x="-160" y="{y}" width="320" height="{hgt}" fill="#000"/>' for y, hgt in ((20, 6), (42, 8), (64, 10), (86, 12), (108, 14)))
    # roadside palms: two per 1040 px period, sizes repeat with the period (no popping)
    palms = "".join(f'<use href="#palm" transform="translate({x + off} {ROAD_TOP - 6}) scale({sc})"/>'
                    for x in range(0, W + 1100, 1040) for off, sc in ((180, 1.0), (700, .88)))
    dashes = "".join(f'<rect x="{x}" y="{LANE_Y - 2}" width="56" height="5" rx="2.5" fill="#FFE2A8" opacity=".85"/>' for x in range(0, W + 240, 120))
    joints = "".join(f'<rect x="{x}" y="{SIDE + 18}" width="3" height="16" fill="#5E4C5A"/>' for x in range(0, W + 320, 160))
    glints = "".join(
        f'<rect x="{300 - w / 2 + rng.randint(-30, 30):.0f}" y="{y}" width="{w}" height="3" rx="1.5" fill="#FFC77A" class="glint" style="animation-delay:{rng.random() * 2:.2f}s"/>'
        for y, w in ((764, 180), (776, 150), (788, 210), (800, 120), (811, 90)))
    glints += "".join(f'<rect x="{rng.randint(500, W - 60)}" y="{rng.randint(760, 812)}" width="{rng.randint(20, 60)}" height="2" rx="1" fill="#F6A98A" opacity=".35"/>' for _ in range(14))
    parasols = "".join(
        f'<g transform="translate({x} {y})"><rect x="-1" y="-22" width="2" height="22" fill="#4A3440"/>'
        f'<path d="M-15 -20 Q0 -32 15 -20Z" fill="{c1}"/><path d="M-5 -20 Q0 -31 5 -20Z" fill="{c2}"/>'
        f'<rect x="-14" y="-3" width="18" height="4" rx="1" fill="#F2E6D6"/></g>'
        for x, y, c1, c2 in ((930, 590, "#E8513F", "#FFF1E0"), (1010, 594, "#2F8FD1", "#FFF1E0"), (1110, 588, "#F2B232", "#FFF1E0"), (1205, 593, "#E8513F", "#FFF1E0")))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Looks like a GitHub contribution graph, until the squares fly into the windows of a Canarian town under Teide at golden hour, next to a beach cove. A red Renault Clio IV drives the coast road past signs: 2015 retail and customer service, 2023 technical support L1, 2024 L2 support, incident manager and lead management, hobbies gym, board games and series, films and anime, billboards for Kanbate, Kage and PRM, then the next exit, AI, into a tunnel. Five cats nap, sit and play football along the way.">
  <defs>
    <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#22134A"/><stop offset=".34" stop-color="#5E2463"/>
      <stop offset=".62" stop-color="#C9475C"/><stop offset=".82" stop-color="#F38D4E"/><stop offset="1" stop-color="#FFC876"/>
    </linearGradient>
    <linearGradient id="sunG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFF2B4"/><stop offset=".55" stop-color="#FFB257"/><stop offset="1" stop-color="#FF5E78"/>
    </linearGradient>
    <mask id="sunMask"><rect x="-170" y="-170" width="340" height="340" fill="#fff"/>{stripes}</mask>
    <radialGradient id="sunGlow"><stop offset="0" stop-color="#FFB86B" stop-opacity=".6"/><stop offset="1" stop-color="#FFB86B" stop-opacity="0"/></radialGradient>
    <linearGradient id="teideG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8E4468"/><stop offset=".45" stop-color="#6A3263"/><stop offset="1" stop-color="#4A2558"/>
    </linearGradient>
    <linearGradient id="cloudG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFD9B0"/><stop offset=".5" stop-color="#F3A58C"/><stop offset="1" stop-color="#C76E7E"/>
    </linearGradient>
    <linearGradient id="hillG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#9A5B4A"/><stop offset="1" stop-color="#5A3440"/>
    </linearGradient>
    <linearGradient id="bayG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E88A7E"/><stop offset=".5" stop-color="#9A4E78"/><stop offset="1" stop-color="#5C3466"/>
    </linearGradient>
    <linearGradient id="sandG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2C58C"/><stop offset="1" stop-color="#D99A68"/>
    </linearGradient>
    <linearGradient id="houseShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FF9A5A" stop-opacity=".25"/><stop offset=".6" stop-color="#FF9A5A" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="roadG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3A2A3E"/><stop offset="1" stop-color="#1E1424"/>
    </linearGradient>
    <linearGradient id="seaG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7A3A62"/><stop offset=".4" stop-color="#4A2552"/><stop offset="1" stop-color="#22143A"/>
    </linearGradient>
    <linearGradient id="rockG" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6A4448"/><stop offset=".5" stop-color="#3E2832"/><stop offset="1" stop-color="#24171F"/>
    </linearGradient>
    <linearGradient id="paint" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF5A48"/><stop offset=".5" stop-color="#E0151F"/><stop offset="1" stop-color="#900B15"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3E2D58"/><stop offset=".42" stop-color="#1C122A"/><stop offset=".52" stop-color="#FFB27A" stop-opacity=".55"/><stop offset=".6" stop-color="#1C122A"/>
    </linearGradient>
    <linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFF1C4" stop-opacity=".5"/><stop offset="1" stop-color="#FFF1C4" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="signSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFB46B" stop-opacity=".2"/><stop offset=".5" stop-color="#FFB46B" stop-opacity="0"/>
    </linearGradient>
    <filter id="neon" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="tailGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    {palm_symbol()}
    <style>{"".join(css)}
      @media (prefers-reduced-motion:reduce){{
        *{{animation-duration:.001s!important;animation-delay:0s!important;animation-iteration-count:1!important}}
        .disguise,.empty{{opacity:0}}
      }}
    </style>
  </defs>

  <g class="disguise gh" fill="{t["text"]}">
    <text x="{GX - 2}" y="{GY - 50}" font-size="20" font-weight="600" fill="{t["strong"]}">Contribution activity</text>
    <g font-size="15">{mlab}{dlab}{legend}</g>
    <path d="M{GX} {GY + ROWS * PITCH + 58}H{GX + COLS * PITCH}" stroke="{t["line"]}"/>
    {activity}
  </g>

  <g clip-path="url(#frame)">
    <g class="sky"><rect width="{W}" height="{ROAD_TOP}" fill="url(#skyG)"/></g>
    <g class="stars">{stars}</g>
    <g class="teide"><g transform="translate(-480 0)">
      <path d="M330 470 C400 440 450 380 500 330 C530 300 556 284 590 282 C624 280 650 290 672 272
               C700 250 740 200 772 166 C786 150 796 134 806 118 L816 112 L832 112 L842 120
               C858 140 880 170 920 214 C990 290 1080 380 1180 440 C1240 470 1300 486 1360 500 C1400 510 1430 520 1460 530 L1460 600 L330 600 Z" fill="url(#teideG)"/>
      <path d="M500 330 C530 300 556 284 590 282 C624 280 650 290 672 272 C700 250 740 200 772 166 C786 150 796 134 806 118 L816 112"
            fill="none" stroke="#FFB07A" stroke-width="3" stroke-opacity=".7"/>
      <path d="M842 120 C858 140 880 170 920 214 C990 290 1080 380 1180 440" fill="none" stroke="#FFC79A" stroke-width="3" stroke-opacity=".8"/>
      <path d="M806 118 L816 112 L832 112 L842 120 L846 134 L834 128 L826 140 L818 128 L810 138 L800 132Z" fill="#F6E8EE"/>
      <path d="M790 140 L800 132 L796 160 Z M846 134 L856 150 L842 146Z M772 170 L782 158 L776 196Z" fill="#F0DDE6" opacity=".85"/>
      <path d="M842 150 C860 190 880 240 910 300 C890 270 864 230 846 190Z M760 200 C740 240 720 280 712 330 C730 290 748 250 770 214Z" fill="#3A1C40" opacity=".55"/>
      <path d="M590 282 C604 286 618 296 624 312 C610 302 598 294 584 290Z" fill="#3A1C40" opacity=".5"/>
      <path d="M930 330 C1000 360 1060 400 1120 440 C1060 420 990 380 930 330Z" fill="#3A1C40" opacity=".35"/>
    </g></g>
    <!-- a few wisps on Teide's flank (not a sea of clouds under it) -->
    <g class="clouds"><g class="drift" fill="#FFD3B4" opacity=".55">
      <path d="M40 360 C80 346 120 352 150 344 C186 336 214 350 250 346 C230 360 170 366 120 366 C90 366 60 366 40 360Z"/>
      <path d="M380 300 C410 290 440 296 466 290 C490 286 510 296 530 294 C510 306 470 308 440 308 C416 308 396 306 380 300Z"/>
    </g></g>
    <!-- the right: setting sun over the sea, then the beach -->
    <g class="sun"><circle cx="1085" cy="470" r="230" fill="url(#sunGlow)"/>
      <g transform="translate(1085 470)"><circle r="108" fill="url(#sunG)" mask="url(#sunMask)"/></g></g>
    <g class="hill">
      <rect x="860" y="476" width="{W - 840}" height="{ROAD_TOP - 476}" fill="url(#bayG)"/>
      <rect x="860" y="476" width="{W - 840}" height="2" fill="#FFD7A8" opacity=".8"/>
      <g class="waves">
        <rect x="1040" y="486" width="90" height="4" rx="2" fill="#FFD27A" opacity=".85"/><rect x="1050" y="497" width="70" height="3" rx="1.5" fill="#FFD27A" opacity=".75"/>
        <rect x="1030" y="508" width="110" height="3" rx="1.5" fill="#FFC77A" opacity=".65"/><rect x="1058" y="520" width="56" height="3" rx="1.5" fill="#FFC77A" opacity=".6"/>
        <rect x="1040" y="532" width="84" height="2" rx="1" fill="#FFC77A" opacity=".5"/><rect x="1062" y="544" width="44" height="2" rx="1" fill="#FFC77A" opacity=".45"/>
        <g fill="#FFD3A8" opacity=".45"><rect x="900" y="500" width="60" height="2" rx="1"/><rect x="1170" y="512" width="70" height="2" rx="1"/><rect x="930" y="538" width="80" height="2" rx="1"/><rect x="1190" y="546" width="60" height="2" rx="1"/></g>
      </g>
      <path d="M850 {ROAD_TOP} C900 572 980 566 1060 568 C1140 570 1220 566 {W + 10} 570 L{W + 10} {ROAD_TOP}Z" fill="url(#sandG)"/>
      <path d="M860 584 C910 568 990 563 1060 565 C1140 567 1220 563 {W + 10} 567" fill="none" stroke="#FFF3E2" stroke-width="2.5" opacity=".7"/>
      {parasols}
      <g transform="translate(1160 592) scale(.5)">{sitting_cat('orangewhite')}</g>
      <path d="M-10 556 C100 546 220 540 340 546 C430 550 520 530 640 520 C740 512 820 516 864 536 C882 548 890 {ROAD_TOP - 6} 898 {ROAD_TOP} L-10 {ROAD_TOP}Z" fill="url(#hillG)"/>
    </g>
    <g class="houses">{"".join(hs)}{roofcat}</g>
  </g>
  <g>{"".join(sq)}</g>
  <g clip-path="url(#frame)">
    <g class="road">
      <g class="palms">{palms}</g>
      {"".join(signs)}
      <rect x="0" y="{ROAD_TOP - 8}" width="{W}" height="8" fill="#C9C2BC"/>
      <rect x="0" y="{ROAD_TOP}" width="{W}" height="{ROAD_BOT - ROAD_TOP}" fill="url(#roadG)"/>
      <rect x="0" y="{ROAD_TOP + 6}" width="{W}" height="3" fill="#F4EDE4" opacity=".55"/>
      <g class="dash">{dashes}</g>
      <rect x="0" y="{ROAD_BOT - 8}" width="{W}" height="3" fill="#F4EDE4" opacity=".75"/>
    </g>
    <g class="car"><g class="carloop"><g transform="translate({CAR_X} {CAR_GROUND - 108})"><g class="bob">{CAR}</g></g></g></g>
    <g class="road">
      <rect x="0" y="{ROAD_BOT}" width="{W}" height="{SIDE - ROAD_BOT}" fill="#9B8F96"/>
      <rect x="0" y="{SIDE}" width="{W}" height="18" fill="#D8CFC8"/>
      <rect x="0" y="{SIDE + 18}" width="{W}" height="16" fill="#8C7A86"/>
      <g class="joints">{joints}</g>
      <rect x="0" y="{SEA_Y}" width="{W}" height="{H - SEA_Y}" fill="url(#seaG)"/>
      {glints}
    </g>
    <g class="nap"><g transform="translate(0 {SIDE + 4}) scale(1.4)">{sleeping_cat("calico")}</g></g>
    <g class="perch"><g transform="translate(0 {SIDE + 4}) scale(1.15)">{sitting_cat("siamese")}</g></g>
    <g class="kick"><g transform="translate(0 {SIDE + 4}) scale(1.3)">{football_cat("cream")}</g></g>
  </g>
</svg>
'''


for name in THEMES:
    with open(f"hero-road-{name}.svg", "w", encoding="utf-8") as f:
        f.write(svg(name))
print("ok cycle", round(CYCLE, 1), "slots", len(SLOTS), "lit", sum(1 for c in LEVELS for v in c if v))
