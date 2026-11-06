import random, math, sys

random.seed(11)

def j(a):
    return random.uniform(-a, a)

def seg(x1, y1, x2, y2, a=0.7):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    over = random.uniform(0.2, 1.6)
    sx, sy = x1 + j(a) - dx / L * over * 0.4, y1 + j(a) - dy / L * over * 0.4
    ex, ey = x2 + j(a) + dx / L * over, y2 + j(a) + dy / L * over
    c1 = (x1 + dx * 0.33 + j(a * 1.6), y1 + dy * 0.33 + j(a * 1.6))
    c2 = (x1 + dx * 0.66 + j(a * 1.6), y1 + dy * 0.66 + j(a * 1.6))
    return f"M{sx:.1f} {sy:.1f}C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {ex:.1f} {ey:.1f}"

def line(x1, y1, x2, y2, a=0.7, step=140):
    """Long lines get broken into slightly wobbly pieces, like a pen lifted now and then."""
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(1, int(L // step))
    out = []
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        out.append(seg(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                       x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1, a))
    return " ".join(out)

main, light, pil, pil_l = [], [], [], []

# deck
for y in (78, 86):
    main.append(line(30, y, 985, y, 0.6))
    light.append(line(30, y + 1.2, 985, y + 1.2, 0.9))
main.append(seg(30, 78, 30, 86, 0.3)); main.append(seg(985, 78, 985, 86, 0.3))
# planks hint
for x in range(46, 980, 17):
    light.append(seg(x, 79.5, x - 2, 85, 0.3))
# railing
main.append(line(30, 62, 818, 62, 0.6))
light.append(line(30, 70, 818, 70, 0.8))
for x in range(34, 816, 26):
    light.append(seg(x, 62, x, 78, 0.4))
# end-platform railing
main.append(line(968, 62, 985, 62, 0.4)); light.append(seg(984, 62, 984, 78, 0.3))
# pilings + bracing
xs = list(range(48, 985, 44))
for i, x in enumerate(xs):
    pil.append(seg(x, 87, x + j(1.5), 190, 0.8))
    pil_l.append(seg(x + 4, 87, x + 4 + j(1.5), 190, 0.8))
    if i < len(xs) - 1 and i % 2 == 0:
        pil_l.append(seg(x + 4, 92, x + 44, 118, 0.6))
        pil_l.append(seg(x + 44, 92, x + 4, 118, 0.6))
# lamp posts
lamps = []
for x in (190, 400, 610):
    main.append(seg(x, 62, x, 30, 0.4))
    main.append(f"M{x-7} 31Q{x} 23 {x+7} 31")
    lamps.append(x)
# shop building
main.append(seg(832, 78, 832, 42, 0.4)); main.append(seg(958, 78, 958, 42, 0.4))
main.append(line(822, 42, 968, 42, 0.5))
main.append(seg(822, 42, 895, 15, 0.5)); main.append(seg(895, 15, 968, 42, 0.5))
light.append(seg(824, 43.5, 895, 17.5, 0.8)); light.append(seg(895, 17.5, 966, 43.5, 0.8))
for k in range(1, 7):  # roof hatching
    x = 830 + k * 18
    yy = 42 - (26 * (1 - abs(x - 895) / 73))
    light.append(seg(x, 41, x + 6, yy + 3, 0.4))
for wx in (840, 862, 912, 934):
    main.append(seg(wx, 50, wx + 14, 50, 0.3)); main.append(seg(wx + 14, 50, wx + 14, 62, 0.3))
    main.append(seg(wx + 14, 62, wx, 62, 0.3)); main.append(seg(wx, 62, wx, 50, 0.3))
    light.append(seg(wx + 7, 50, wx + 7, 62, 0.3))
main.append(seg(886, 78, 886, 52, 0.3)); main.append(seg(886, 52, 904, 52, 0.3)); main.append(seg(904, 52, 904, 78, 0.3))
main.append(seg(895, 15, 895, 1, 0.3))
# runners
def runner(x, flip=1):
    p = [f"M{x+2*flip} 63L{x} 71", f"M{x} 71L{x-4*flip} 78", f"M{x} 71L{x+5*flip} 76.5",
         f"M{x+1.5*flip} 65L{x-3.5*flip} 68.5", f"M{x+1.5*flip} 65L{x+6*flip} 63"]
    return p
for r in runner(300) + runner(318) + runner(522, -1):
    main.append(r)
heads = [(302.5, 59.6), (320.5, 59.6), (519.5, 59.6)]
# birds
for (bx, by, s) in ((110, 22, 1), (128, 15, .8), (690, 12, .9)):
    light.append(f"M{bx-6*s} {by}Q{bx-3*s} {by-4*s} {bx} {by}Q{bx+3*s} {by-4*s} {bx+6*s} {by}")

def path(d, cls):
    return f'<path class="{cls}" d="{" ".join(d)}"/>'

svg = f'''<svg id="pier" viewBox="0 0 1000 190" role="img" aria-label="Sketch of the Huntington Beach pier with the merch shop at the end">
<defs><linearGradient id="sub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".22" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity=".12"/></linearGradient>
<mask id="pilMask" maskUnits="userSpaceOnUse" x="0" y="80" width="1000" height="110"><rect x="0" y="80" width="1000" height="110" fill="url(#sub)"/></mask></defs>
<g mask="url(#pilMask)">{path(pil, "ink")}{path(pil_l, "ink-l")}</g>
{path(main, "ink")}{path(light, "ink-l")}
{"".join(f'<circle cx="{x}" cy="31.5" r="2" class="acc-fill"/>' for x in lamps)}
{"".join(f'<circle cx="{x}" cy="{y}" r="3" class="ink paper-fill"/>' for x, y in heads)}
<path d="M895 2L909 5.5L895 9Z" class="acc-fill"/>
<text x="895" y="38" text-anchor="middle" class="pier-sign">SHOP</text>
<g transform="rotate(-5 812 112)"><path class="ink-l" d="M806 70L810 104"/><rect x="779" y="104" width="64" height="16" rx="1.5" class="stamp-rect"/><text x="811" y="115" text-anchor="middle" class="stamp-text">DROP 02 · OPEN</text></g>
</svg>'''

tpl = open(sys.argv[1]).read()
open(sys.argv[2], "w").write(tpl.replace("<!--PIER-->", svg))
print("ok", len(svg))
