"""Starts the drive scene after its intro: every animation delay moves 5 s earlier
(negative delays = already in progress), and the contribution-graph disguise
and its empty squares are removed. Usage: skip_intro.py in.svg out.svg"""
import re
import sys

SHIFT = 5.0
s = open(sys.argv[1], encoding="utf-8").read()

# drop the disguise text block and the empty (never-lit) graph squares
s = re.sub(r'<g class="disguise gh".*?</g>\s*</g>', "", s, count=1, flags=re.S) if False else s
start = s.index('<g class="disguise gh"')
depth, i = 0, start
while True:
    o, c = s.find("<g", i), s.find("</g>", i)
    if o != -1 and o < c:
        depth += 1
        i = o + 2
    else:
        depth -= 1
        i = c + 4
        if depth == 0:
            break
s = s[:start] + s[i:]
s = re.sub(r'<rect [^>]*class="empty"/>', "", s)


def shift_decl(m):
    parts = re.split(r",(?![^()]*\))", m.group(1))
    out = []
    for p in parts:
        toks = p.split()
        times = [k for k, t in enumerate(toks) if re.fullmatch(r"-?(\d*\.)?\d+s", t)]
        if len(times) >= 2:
            k = times[1]
            toks[k] = f"{float(toks[k][:-1]) - SHIFT:.3f}s"
        else:
            toks.insert(times[0] + 2 if times else len(toks), f"{-SHIFT:.3f}s")
        out.append(" ".join(toks))
    return "animation:" + ",".join(out)


s = re.sub(r"animation:([^;}]+)", shift_decl, s)
s = re.sub(r"animation-delay:(-?\d+(?:\.\d+)?)s", lambda m: f"animation-delay:{float(m.group(1)) - SHIFT:.3f}s", s)
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("ok")
