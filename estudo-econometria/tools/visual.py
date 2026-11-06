"""Mapa visual: um mini desenho + explicação fácil para cada conceito do curso.
Gera parts/figs/v_*.svg, parts/01b_visual.html (módulo) e parts/strips/*.html (faixas por aula)."""
import math, random, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(BASE, "parts", "figs"); STRIPS = os.path.join(BASE, "parts", "strips")
os.makedirs(FIGS, exist_ok=True); os.makedirs(STRIPS, exist_ok=True)

def f(v): return f"{v:.1f}".rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-9 else str(int(round(v)))
def npdf(x, m=0, s=1): return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
class P:
    def __init__(s, L, R, T, B, x0, x1, y0, y1): s.L, s.R, s.T, s.B, s.x0, s.x1, s.y0, s.y1 = L, R, T, B, x0, x1, y0, y1
    def X(s, x): return s.L + (x - s.x0) / (s.x1 - s.x0) * (s.R - s.L)
    def Y(s, y): return s.B - (y - s.y0) / (s.y1 - s.y0) * (s.B - s.T)
    def axes(s): return (f'<line class="ax" x1="{f(s.L)}" y1="{f(s.B)}" x2="{f(s.R)}" y2="{f(s.B)}"/>'
                         f'<line class="ax" x1="{f(s.L)}" y1="{f(s.T)}" x2="{f(s.L)}" y2="{f(s.B)}"/>')
    def base(s): return f'<line class="ax" x1="{f(s.L)}" y1="{f(s.B)}" x2="{f(s.R)}" y2="{f(s.B)}"/>'
    def line(s, x1, y1, x2, y2, c="fit"): return f'<line class="{c}" x1="{f(s.X(x1))}" y1="{f(s.Y(y1))}" x2="{f(s.X(x2))}" y2="{f(s.Y(y2))}"/>'
    def dot(s, x, y, r=3.2, c="pt"): return f'<circle class="{c}" cx="{f(s.X(x))}" cy="{f(s.Y(y))}" r="{r}"/>'
    def curve(s, fn, a, b, c="fit", n=120): return f'<polyline class="{c}" points="{" ".join(f"{f(s.X(a+(b-a)*i/n))},{f(s.Y(fn(a+(b-a)*i/n)))}" for i in range(n+1))}"/>'
    def area(s, fn, a, b, c="rej", n=60):
        pts = [f"{f(s.X(a))},{f(s.Y(s.y0))}"] + [f"{f(s.X(a+(b-a)*i/n))},{f(s.Y(fn(a+(b-a)*i/n)))}" for i in range(n+1)] + [f"{f(s.X(b))},{f(s.Y(s.y0))}"]
        return f'<polygon class="{c}" points="{" ".join(pts)}"/>'
def T(x, y, s, c="an sm", a="start", w=""): return f'<text class="{c}" x="{f(x)}" y="{f(y)}" text-anchor="{a}"{w}>{s}</text>'
def arrow(x1, y1, x2, y2, c="arw", h=7):
    a = math.atan2(y2 - y1, x2 - x1); bx, by = x2 - h * math.cos(a), y2 - h * math.sin(a)
    p1 = (bx + h * .45 * math.sin(a), by - h * .45 * math.cos(a)); p2 = (bx - h * .45 * math.sin(a), by + h * .45 * math.cos(a))
    return (f'<line class="{c}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(bx)}" y2="{f(by)}"/>'
            f'<polygon class="arwh" points="{f(x2)},{f(y2)} {f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])}"/>')
def diamond(x, y, r=5): return f'<rect class="meanpt" x="{f(x-r)}" y="{f(y-r)}" width="{2*r}" height="{2*r}" transform="rotate(45 {f(x)} {f(y)})"/>'
def save(name, body, label, W=240, H=140):
    open(f"{FIGS}/{name}.svg", "w").write(f'<svg class="fig mini" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')
def target(cx, cy, shots, r0=44):
    o = [f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}"/>' for r, c in [(r0, "t1"), (r0*.7, "t2"), (r0*.42, "t3"), (r0*.14, "t4")]]
    o += [f'<circle class="shot" cx="{f(cx+dx)}" cy="{f(cy+dy)}" r="3.2"/>' for dx, dy in shots]
    return ''.join(o)
def shots(seed, n, sd, off=(0, 0)):
    random.seed(seed); return [(off[0] + random.gauss(0, sd), off[1] + random.gauss(0, sd)) for _ in range(n)]
def scatter(p, seed, n, fn, sd, x0, x1, c="pt sm", r=2.6):
    random.seed(seed); o = []
    for _ in range(n):
        x = random.uniform(x0, x1); o.append(p.dot(x, fn(x) + random.gauss(0, sd), r, c))
    return ''.join(o)

# ============================ A. Estatística do zero ============================
b = []
cols = ["id", "salário", "educ", "idade"]; rows = [["1", "12", "8", "25"], ["2", "15", "10", "31"], ["3", "23", "12", "28"], ["4", "20", "12", "40"]]
x0, y0, cw, rh = 18, 10, 52, 20
b.append(f'<rect class="nm" x="{x0+2*cw}" y="{y0}" width="{cw}" height="{rh*5}" rx="3"/>')
b.append(f'<rect class="ng" x="{x0}" y="{y0+3*rh}" width="{cw*4}" height="{rh}" rx="3" opacity=".85"/>')
for j, c in enumerate(cols): b.append(T(x0 + cw*j + cw/2, y0 + 14, c, "an sm", "middle", ' font-weight="700"'))
for i, r in enumerate(rows):
    for j, c in enumerate(r): b.append(T(x0 + cw*j + cw/2, y0 + rh*(i+1) + 14, c, "an sm", "middle"))
b.append(T(x0 + 2*cw, 128, "coluna azul = uma variável", "an sm fitc", "middle"))
b.append(T(x0 + 2*cw, 146, "linha verde = uma observação", "an sm posc", "middle"))
save("v_variavel", ''.join(b), "Tabela de dados: a coluna é uma variável e a linha é uma observação", 240, 154)

p = P(16, 226, 20, 96, 0, 10, 0, 1)
b = [p.line(0.5, 0.5, 9.5, 0.5, "tg0")]
b += [p.dot(2, 0.62, 4), p.dot(3, 0.62, 4), p.dot(3, 0.8, 4), p.dot(4, 0.62, 4), p.dot(8, 0.62, 4)]
b.append(f'<polygon class="nm" points="{f(p.X(4))},{f(p.Y(0.5)+2)} {f(p.X(4)-10)},{f(p.Y(0.5)+20)} {f(p.X(4)+10)},{f(p.Y(0.5)+20)}"/>')
b += [T(p.X(4), p.Y(0.5) + 34, "x̄ = 4: o ponto de equilíbrio", "an sm fitc", "middle"), T(120, 14, "2, 3, 3, 4, 8 → soma 20 ÷ 5 = 4", "an sm", "middle")]
for x in [2, 3, 4, 8]: b.append(T(p.X(x), p.Y(0.5) + 12, str(x), "tk", "middle"))
save("v_media", ''.join(b), "Pontos sobre uma gangorra equilibrada no ponto da média")

p = P(14, 230, 30, 84, 0, 28, 0, 1)
b = [p.base()]
for i, x in enumerate([2, 3, 3, 4, 5, 6, 26]): b.append(p.dot(x, 0.25 + (0.3 if (x == 3 and i == 2) else 0), 4, "ptB" if x == 26 else "pt"))
b += [p.line(4, 0, 4, 1.15, "tg"), p.line(7, 0, 7, 1.15, "fit")]
b += [T(p.X(4) + 3, 14, "mediana 4", "an sm posc"), T(p.X(7) + 3, 28, "média 7", "an sm fitc")]
b += [T(p.X(26), p.Y(0.25) - 10, "26", "an sm resc", "middle"), T(120, 104, "um valor extremo puxa a média,", "an sm", "middle"), T(120, 120, "mas quase não mexe na mediana", "an sm", "middle")]
save("v_mediana", ''.join(b), "Valor extremo puxa a média para a direita, mas a mediana fica no meio")

p = P(14, 230, 10, 120, 0, 10, 0, 2)
b = []
for yy, xs, lab, cls in [(1.55, [4, 4.5, 5, 5.5, 6], "s = 0,79 (pouco espalhado)", "fit"), (0.55, [1, 3, 5, 7, 9], "s = 3,16 (muito espalhado)", "tgn")]:
    b.append(p.line(0.3, yy, 9.7, yy, "g"))
    for x in xs:
        b.append(p.line(5, yy, x, yy, cls)); b.append(p.dot(x, yy, 3.6))
    b.append(p.line(5, yy - .18, 5, yy + .18, "tg0")); b.append(T(p.X(5), p.Y(yy) - 12, lab, "an sm", "middle"))
b.append(T(120, 136, "mesma média; muda o espalhamento", "an sm", "middle"))
save("v_variancia", ''.join(b), "Duas amostras com a mesma média: uma concentrada e outra espalhada", 240, 142)

b = []
for k, (slope, lab) in enumerate([(0.9, "r ≈ +0,9"), (0, "r ≈ 0"), (-0.9, "r ≈ −0,9")]):
    p = P(8 + k*78, 76 + k*78, 12, 96, 0, 10, 0, 10)
    b.append(p.axes()); b.append(scatter(p, 40 + k, 14, lambda x, s=slope: 5 + s*(x - 5), 1.0 if slope else 2.2, 0.8, 9.2, "pt sm", 2.3))
    b.append(T((p.L + p.R)/2, 112, lab, "an sm", "middle"))
b.append(T(120, 132, "sinal = direção; ±1 = bem alinhado", "an sm", "middle"))
save("v_correlacao", ''.join(b), "Três nuvens de pontos: correlação positiva, nula e negativa")

p = P(10, 230, 12, 108, -3.4, 3.4, 0, 0.42)
b = [p.area(npdf, -2, 2, "bandf"), p.area(npdf, -1, 1, "bandf"), p.curve(npdf, -3.4, 3.4), p.base()]
b += [T(p.X(0), p.Y(0.2), "68%", "an sm", "middle"), T(p.X(-1.55), p.Y(0.012), "≈95%", "an sm", "middle")]
for v, t in [(-2, "μ−2σ"), (-1, "μ−σ"), (0, "μ"), (1, "μ+σ"), (2, "μ+2σ")]: b.append(T(p.X(v), 122, t, "tk", "middle"))
b.append(T(120, 136, "a maioria fica perto da média", "an sm", "middle"))
save("v_normal", ''.join(b), "Curva normal com 68% dos valores a um desvio-padrão e cerca de 95% a dois", 240, 140)

p = P(18, 226, 18, 104, 0.4, 6.6, 0, 0.25)
b = [p.base()]
for k in range(1, 7): b.append(f'<rect class="barA" x="{f(p.X(k-0.32))}" y="{f(p.Y(1/6))}" width="{f(p.X(0.64)-p.X(0))}" height="{f(p.Y(0)-p.Y(1/6))}"/>'); b.append(T(p.X(k), 118, str(k), "tk", "middle"))
b += [p.line(3.5, 0, 3.5, 0.235, "obs"), T(p.X(3.5) + 4, 14, "E(X) = 3,5", "an sm resc")]
b.append(T(120, 134, "cada face 1/6; média de longo prazo 3,5", "an sm", "middle"))
save("v_esperanca", ''.join(b), "Distribuição de um dado com as seis faces igualmente prováveis e esperança 3,5")

b = [f'<circle class="t1" cx="70" cy="66" r="54"/>']
random.seed(5); pts = [(random.uniform(-40, 40), random.uniform(-40, 40)) for _ in range(60)]
pts = [(x, y) for x, y in pts if x*x + y*y < 46*46]
for i, (x, y) in enumerate(pts): b.append(f'<circle class="{"ptB" if i % 7 == 0 else "pt sm"}" cx="{f(70+x)}" cy="{f(66+y)}" r="{3 if i % 7 == 0 else 2.2}"/>')
b.append(f'<circle class="nr" cx="190" cy="66" r="30"/>')
for i, (x, y) in enumerate([p for k, p in enumerate(pts) if k % 7 == 0][:7]): b.append(f'<circle class="ptB" cx="{f(190+x*0.5)}" cy="{f(66+y*0.5)}" r="3"/>')
b.append(arrow(128, 66, 156, 66))
b += [T(70, 134, "população: β, μ (fixos)", "an sm", "middle"), T(190, 112, "amostra: β̂, x̄", "an sm resc", "middle"), T(190, 126, "(calculados)", "an sm resc", "middle")]
save("v_amostra", ''.join(b), "Da população sorteamos uma amostra; dela calculamos as estimativas")

# ============================ B. Estimadores ============================
b = [target(52, 64, [(8, -6)], 40), f'<circle class="shot" cx="60" cy="58" r="4"/>']
b += [arrow(104, 34, 64, 55), T(108, 32, "estimativa β̂ = 1,15"), T(108, 46, "(uma flecha)")]
b += [arrow(104, 92, 56, 68), T(108, 90, "parâmetro β: o centro"), T(108, 104, "(fixo e invisível)")]
b.append(T(120, 134, "estimador = a regra de mira (MQO)", "an sm fitc", "middle"))
save("v_param", ''.join(b), "Alvo: o centro é o parâmetro e cada flecha é uma estimativa")

b = [target(56, 64, shots(3, 9, 5, (16, -13)), 42), arrow(56, 64, 72, 51, "obs"), T(110, 44, "flechas juntas,"), T(110, 58, "mas fora do centro"), T(110, 84, "viés = E(β̂) − β", "an sm resc")]
b.append(T(120, 134, "erra sempre para o mesmo lado", "an sm", "middle"))
save("v_vies", ''.join(b), "Alvo com flechas agrupadas fora do centro: viés")

b = [target(56, 64, shots(8, 11, 15), 42), T(112, 40, "flechas em volta"), T(112, 54, "do centro, mas"), T(112, 68, "espalhadas"), T(112, 92, "Var(β̂) grande", "an sm fitc")]
b.append(T(120, 134, "acerta na média, erra muito em cada tiro", "an sm", "middle"))
save("v_varest", ''.join(b), "Alvo com flechas espalhadas em volta do centro: sem viés, alta variância")

b = []
x0, sc = 10, 17
for k, (lab, var, vi) in enumerate([("T (viesado)", 4, 1), ("Z₂ (sem viés)", 8, 0)]):
    y = 40 + k*46
    b.append(T(x0, y - 4, lab, "an sm"))
    b.append(f'<rect class="barA" x="{x0}" y="{y}" width="{var*sc}" height="22" rx="2"/>')
    if vi: b.append(f'<rect class="sqr" x="{x0+var*sc}" y="{y}" width="{vi*sc}" height="22" rx="2"/>')
    b.append(T(x0 + (var + vi)*sc + 4, y + 15, f"EQM = {var+vi}", "an sm", "start", ' font-weight="700"'))
b += [T(x0, 16, "azul: variância · vermelho: viés²", "an sm", "start", ' font-weight="700"'), T(120, 132, "o viesado pode errar menos no total", "an sm", "middle")]
save("v_eqm", ''.join(b), "Barras do erro quadrático médio: variância mais viés ao quadrado")

p = P(14, 230, 16, 104, 0.2, 1.4, 0, 1)
b = [p.base()]
for i in range(-5, 6):
    c = 0.8 + i*0.09; h = math.exp(-0.5*(i/2.2)**2)
    b.append(f'<rect class="barA" x="{f(p.X(c-0.04))}" y="{f(p.Y(h*0.9))}" width="{f(p.X(0.08)-p.X(0))}" height="{f(p.Y(0)-p.Y(h*0.9))}"/>')
b += [p.line(0.8, 0, 0.8, 1, "obs"), T(p.X(0.8) + 4, 14, "β verdadeiro", "an sm resc"), T(120, 118, "cada barra: quantas amostras", "an sm", "middle"), T(120, 132, "deram aquele valor de β̂", "an sm", "middle")]
save("v_amostral", ''.join(b), "Histograma de muitas estimativas em torno do valor verdadeiro")

p = P(12, 230, 12, 110, -3, 3, 0, 1.35)
b = [p.base()]
for s, lab, c in [(1.0, "n = 10", "cB"), (0.55, "n = 100", "samp"), (0.3, "n = 1.000", "fit")]:
    b.append(p.curve(lambda x, s=s: npdf(x, 0, s), -3, 3, c, 150))
b += [p.line(0, 0, 0, 1.35, "true"), T(p.X(0) + 4, 16, "θ", "an sm"), T(p.X(0.55), p.Y(1.1), "n = 1.000", "an sm fitc"), T(p.X(1.2), p.Y(0.45), "n = 100", "an sm fitc"), T(p.X(1.9), p.Y(0.16), "n = 10", "an sm cBt")]
b.append(T(120, 128, "com mais dados, gruda no alvo", "an sm", "middle"))
save("v_consistencia", ''.join(b), "Distribuições do estimador cada vez mais estreitas em volta do parâmetro quando n cresce")

p = P(12, 230, 12, 110, -3.5, 3.5, 0, 0.85)
b = [p.base(), p.curve(lambda x: npdf(x, 0, 1.4), -3.5, 3.5, "cB"), p.curve(lambda x: npdf(x, 0, 0.5), -2, 2, "fit")]
b += [p.line(0, 0, 0, 0.85, "true"), T(236, 30, "azul: MQO", "an sm fitc", "end"), T(236, 44, "tracejada: outro", "an sm cBt", "end")]
b.append(T(120, 128, "mesmo centro; ganha o mais estreito", "an sm", "middle"))
save("v_eficiencia", ''.join(b), "Dois estimadores sem viés: o MQO tem a distribuição mais estreita")

p = P(20, 230, 12, 106, 0, 300, 1, 6)
random.seed(37); s = 0; pts = []
for n in range(1, 301):
    s += random.randint(1, 6); pts.append((n, s/n))
b = [p.axes(), p.line(0, 3.5, 300, 3.5, "true"), f'<polyline class="fit" points="{" ".join(f"{f(p.X(n))},{f(p.Y(m))}" for n, m in pts)}"/>']
b += [T(p.R, p.Y(3.5) - 6, "μ = 3,5", "an sm", "end"), T(120, 120, "lançamentos de um dado →", "tk", "middle"), T(120, 134, "a média acumulada se aproxima de μ", "an sm", "middle")]
save("v_lgn", ''.join(b), "Média acumulada de lançamentos de um dado se aproximando de 3,5")

b = []
p = P(10, 100, 20, 96, 0, 7, 0, 0.45)
b.append(p.base())
for k, h in enumerate([0.40, 0.24, 0.15, 0.09, 0.06, 0.04]): b.append(f'<rect class="barB" x="{f(p.X(k+0.6))}" y="{f(p.Y(h))}" width="{f(p.X(0.8)-p.X(0))}" height="{f(p.Y(0)-p.Y(h))}"/>')
b.append(T(55, 112, "dados: tortos", "an sm", "middle"))
b.append(arrow(106, 60, 132, 60))
p = P(138, 230, 20, 96, -3, 3, 0, 0.45)
b.append(p.base())
for i in range(-3, 4):
    h = npdf(i*0.85)*0.95; b.append(f'<rect class="barA" x="{f(p.X(i*0.85-0.35))}" y="{f(p.Y(h))}" width="{f(p.X(0.7)-p.X(0))}" height="{f(p.Y(0)-p.Y(h))}"/>')
b.append(p.curve(npdf, -3, 3, "fit"))
b += [T(184, 112, "médias: sino", "an sm", "middle"), T(120, 132, "médias de muitas amostras viram normal", "an sm", "middle")]
save("v_tcl", ''.join(b), "Dados assimétricos à esquerda; a distribuição das médias amostrais tem forma de sino à direita")

# ============================ C. Regressão e MQO ============================
p = P(16, 228, 12, 112, 0, 10, 0, 10)
b = [p.axes(), scatter(p, 12, 16, lambda x: 1.5 + 0.7*x, 1.0, 0.5, 9.5), p.line(0, 1.5, 10, 8.5)]
b += [T(p.X(0.4), p.Y(9.2), "ŷ = β̂₀ + β̂₁x", "an sm fitc"), T(120, 130, "a reta que resume a nuvem", "an sm", "middle")]
save("v_regressao", ''.join(b), "Nuvem de pontos com a reta de regressão")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
xs, ys = [1.5, 3, 4.5, 6.5, 8.5], [3.6, 2.9, 5.2, 5.3, 8.1]
b0, b1 = 1.6, 0.65
b = [p.axes()]
for x, y in zip(xs, ys):
    yh = b0 + b1*x; d = y - yh; w = abs(p.Y(y) - p.Y(yh))
    x1 = p.X(x); b.append(f'<rect class="sqr" x="{f(x1)}" y="{f(min(p.Y(y), p.Y(yh)))}" width="{f(w)}" height="{f(w)}"/>')
b.append(p.line(0, b0, 10, b0 + 10*b1))
for x, y in zip(xs, ys): b.append(p.dot(x, y))
b.append(T(120, 130, "MQO: menor soma das áreas", "an sm", "middle"))
save("v_mqo", ''.join(b), "Quadrados dos resíduos: o MQO escolhe a reta com a menor soma das áreas")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), p.line(0, 1, 10, 8, "truel"), p.line(0, 2, 10, 7.6, "fit"), p.line(6, 5.2, 6, 8.2, "tot"), p.line(6.25, 5.36, 6.25, 8.2, "res"), p.dot(6.12, 8.2, 3.6)]
b += [T(p.X(6) - 5, p.Y(6.6), "u", "an", "end"), T(p.X(6.25) + 5, p.Y(6.8), "û", "an resc")]
b += [T(p.X(0.3), p.Y(9.5), "tracejada: reta verdadeira", "an sm"), T(p.X(0.3), p.Y(8.0), "azul: reta estimada", "an sm fitc")]
b.append(T(120, 130, "u: até a verdadeira; û: até a estimada", "an sm", "middle"))
save("v_erro_residuo", ''.join(b), "O erro vai do ponto até a reta verdadeira; o resíduo, até a reta estimada")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), p.line(0, 1.5, 10, 8.5), p.line(7, 0, 7, 6.4, "mean"), p.dot(7, 8.3, 3.6), p.dot(7, 6.4, 4, "fitpt"), diamond(p.X(4.5), p.Y(4.65))]
b += [T(p.X(7) - 7, p.Y(8.3) + 4, "y (ponto real)", "an sm", "end"), T(p.X(7) + 7, p.Y(6.4) + 12, "ŷ", "an fitc"), T(p.X(7), p.B + 12, "x = 7", "tk", "middle"), T(p.X(4.5) - 8, p.Y(4.65) - 8, "(x̄, ȳ)", "an sm", "end")]
b.append(T(120, 134, "a reta passa sempre por (x̄, ȳ)", "an sm", "middle"))
save("v_ajustado", ''.join(b), "Valor ajustado é a altura da reta; a reta passa pelo ponto das médias")

b = [T(12, 22, "SQT = toda a variação de y", "an sm", "start", ' font-weight="700"')]
b.append(f'<rect class="barA" x="12" y="32" width="{f(216*0.925)}" height="34" rx="3"/>')
b.append(f'<rect class="sqr" x="{f(12+216*0.925)}" y="32" width="{f(216*0.075)}" height="34" rx="3"/>')
b += [T(110, 54, "SQE (explicada)", "an sm", "middle"), T(228, 82, "SQR (resíduos) ↑", "an sm resc", "end")]
b += [T(12, 106, "R² = SQE / SQT = parte azul", "an sm fitc"), T(12, 124, "ex.: 52,9 / 57,2 = 0,925", "an sm")]
save("v_r2", ''.join(b), "Barra da variação total dividida em parte explicada e resíduos; o R-quadrado é a parte azul")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
up = [f"{f(p.X(x/10))},{f(p.Y(1.5+0.7*x/10+1.3))}" for x in range(0, 101)]; dn = [f"{f(p.X(x/10))},{f(p.Y(1.5+0.7*x/10-1.3))}" for x in range(100, -1, -1)]
b = [p.axes(), f'<polygon class="bandf" points="{" ".join(up+dn)}"/>', p.line(0, 1.5, 10, 8.5), scatter(p, 21, 18, lambda x: 1.5 + 0.7*x, 0.8, 0.5, 9.5)]
b += [T(p.X(0.3), p.Y(9.3), "faixa ≈ ±σ̂ em volta da reta", "an sm fitc"), T(120, 130, "σ̂² = SQR/(n − 2): o tremor típico", "an sm", "middle")]
save("v_sigma", ''.join(b), "Faixa em torno da reta mostrando o espalhamento típico dos pontos")

b = []
for k, (x0, x1, lab) in enumerate([(4.3, 5.7, "x concentrado"), (1, 9, "x espalhado")]):
    p = P(10 + k*118, 112 + k*118, 12, 96, 0, 10, 0, 10)
    b.append(p.axes())
    for sl in ([0.2, 0.7, 1.2] if k == 0 else [0.62, 0.7, 0.78]):
        b.append(p.line(0.3, 5 + sl*(0.3 - 5), 9.7, 5 + sl*(9.7 - 5), "samp"))
    b.append(scatter(p, 31 + k, 9, lambda x: 5 + 0.7*(x - 5), 0.6, x0, x1, "pt sm", 2.4))
    b.append(T((p.L + p.R)/2, 112, lab, "an sm", "middle"))
b.append(T(120, 132, "x espalhado (SQTₓ grande) → reta firme", "an sm", "middle"))
save("v_sqtx", ''.join(b), "Com x concentrado, várias retas servem; com x espalhado, a inclinação fica bem determinada")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), f'<rect class="bandf" x="{f(p.X(2))}" y="{f(p.T)}" width="{f(p.X(6)-p.X(2))}" height="{f(p.B-p.T)}"/>', scatter(p, 44, 10, lambda x: 2 + 0.6*x, 0.5, 2.1, 5.9)]
b += [p.line(2, 3.2, 6, 5.6), p.line(6, 5.6, 9.6, 7.76, "res"), p.line(0, 2, 2, 3.2, "res"), T(p.X(8.2), p.Y(8.9), "?", "an resc", "middle"), T(p.X(4), p.Y(9.2), "dados", "an sm fitc", "middle")]
b.append(T(120, 130, "fora da faixa dos dados: extrapolação", "an sm", "middle"))
save("v_extrapolacao", ''.join(b), "A reta só é confiável dentro da faixa de x observada")

# ============================ D. Hipóteses RLS ============================
p = P(16, 228, 10, 112, 0.2, 10, 0, 10)
b = [p.axes(), p.curve(lambda x: 1 + 3*math.log(x), 0.75, 10), scatter(p, 51, 12, lambda x: 1 + 3*math.log(x), 0.5, 1.2, 9.6)]
b += [T(p.X(3.5), p.Y(2.2), "y = β₀ + β₁·ln x", "an sm fitc"), T(120, 130, "x pode entrar curvo; β entra linear", "an sm", "middle")]
save("v_rls1", ''.join(b), "Relação curva em x que ainda é linear nos parâmetros")

b = []
random.seed(9); pick = set(random.sample(range(48), 8))
for i in range(48):
    cx, cy = 22 + (i % 12)*18, 20 + (i // 12)*22
    b.append(f'<circle class="{"ptB" if i in pick else "pt sm"}" cx="{cx}" cy="{cy}" r="{4 if i in pick else 3}"/>')
b += [T(120, 116, "vermelhos: sorteados ao acaso", "an sm resc", "middle"), T(120, 132, "mesma chance para todos", "an sm", "middle")]
save("v_rls2", ''.join(b), "População em grade com alguns indivíduos sorteados ao acaso")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes()]
for sl in [-0.6, 0, 0.6, 1.2]: b.append(p.line(1, 5 + sl*(1 - 5), 9, 5 + sl*(9 - 5), "samp"))
for y in [3.2, 4.1, 5, 5.6, 6.5, 7.2]: b.append(p.dot(5, y, 3.4))
b += [T(p.X(0.3), p.Y(9.4), "todos com o mesmo x", "an sm"), T(120, 130, "SQTₓ = 0: qualquer inclinação serve", "an sm resc", "middle")]
save("v_rls3", ''.join(b), "Se todos os x são iguais, não dá para estimar a inclinação")

b = []
for k, (tilt, lab, cls) in enumerate([(0, "E(u | x) = 0 ✓", "posc"), (0.55, "u cresce com x ✗", "resc")]):
    p = P(10 + k*118, 112 + k*118, 12, 96, 0, 10, -4, 4)
    b.append(p.axes()); b.append(p.line(0, 0, 10, 0, "mean"))
    b.append(scatter(p, 61 + k, 16, lambda x, t=tilt: t*(x - 5), 1.0, 0.5, 9.5, "pt sm", 2.4))
    b.append(T((p.L + p.R)/2, 112, lab, f"an sm {cls}", "middle"))
b.append(T(120, 132, "u tem média 0 em todo x → sem viés", "an sm", "middle"))
save("v_rls4", ''.join(b), "Resíduos centrados em zero para todo x, comparados com resíduos que crescem com x")

b = []
for k, (het, lab) in enumerate([(False, "faixa constante ✓"), (True, "funil (hetero)")]):
    p = P(10 + k*118, 112 + k*118, 12, 96, 0, 10, 0, 10)
    up = [f"{f(p.X(x/10))},{f(p.Y(2+0.6*x/10+((0.3+0.28*x/10) if het else 1.4)))}" for x in range(0, 101, 5)]
    dn = [f"{f(p.X(x/10))},{f(p.Y(2+0.6*x/10-((0.3+0.28*x/10) if het else 1.4)))}" for x in range(100, -1, -5)]
    b += [p.axes(), f'<polygon class="bandf" points="{" ".join(up+dn)}"/>', p.line(0, 2, 10, 8)]
    b.append(T((p.L + p.R)/2, 112, lab, "an sm", "middle"))
b.append(T(120, 132, "RLS.5: Var(u | x) = σ² igual para todo x", "an sm", "middle"))
save("v_rls5", ''.join(b), "Faixa de espalhamento constante comparada com um funil")

p = P(12, 230, 12, 106, -3.4, 3.4, 0, 0.42)
b = [p.base(), p.curve(npdf, -3.4, 3.4), p.line(0, 0, 0, 0.42, "true"), T(p.X(0) + 4, 18, "0", "an sm")]
b += [T(236, 40, "u ~ Normal", "an sm fitc", "end"), T(236, 54, "(0, σ²)", "an sm fitc", "end"), T(120, 122, "com isso, o t é exato", "an sm", "middle"), T(120, 136, "mesmo com amostra pequena", "an sm", "middle")]
save("v_rls6", ''.join(b), "O erro segue uma distribuição normal centrada em zero", 240, 142)

# ============================ E. Inferência ============================
p = P(12, 230, 14, 104, -3.4, 3.4, 0, 0.45)
b = [p.base(), p.curve(npdf, -3.4, 3.4), p.line(0, 0, 0, 0.42, "true"), f'<path class="brk" d="M{f(p.X(0))} {f(p.Y(0.24))} H{f(p.X(1))}"/>']
b += [T(p.X(0.5), p.Y(0.24) + 14, "1 EP", "an sm posc", "middle"), T(p.X(0) - 4, 24, "β", "an sm", "end")]
b += [T(120, 120, "EP: o tamanho típico do erro de β̂", "an sm", "middle"), T(120, 134, "(desvio-padrão estimado de β̂)", "an sm", "middle")]
save("v_ep", ''.join(b), "Distribuição de beta chapéu com a largura de um erro-padrão marcada")

p = P(12, 230, 14, 104, -4, 4, 0, 0.45)
b = [p.base(), p.curve(npdf, -4, 4), p.line(0, 0, 0, 0.42, "true"), p.line(2.5, 0, 2.5, 0.2, "obs")]
b += [T(p.X(0) - 4, 24, "H₀", "an sm", "end"), T(p.X(2.5) + 4, p.Y(0.2), "t = 2,5", "an sm resc"), f'<path class="brk" d="M{f(p.X(0))} {f(p.Y(0.1))} H{f(p.X(2.5))}"/>']
b += [T(p.X(0.9), p.Y(0.1) + 13, "2,5 EPs", "an sm posc", "middle"), T(120, 122, "t = (β̂ − valor de H₀) / EP", "an sm", "middle"), T(120, 136, "quantos EPs longe de H₀", "an sm", "middle")]
save("v_t", ''.join(b), "Estatística t como a distância, em erros-padrão, entre a estimativa e o valor da hipótese nula", 240, 142)

p = P(12, 230, 14, 104, -4, 4, 0, 0.45)
b = [p.area(npdf, 2.5, 4), p.area(npdf, -4, -2.5), p.base(), p.curve(npdf, -4, 4), p.line(2.5, 0, 2.5, 0.2, "obs"), p.line(-2.5, 0, -2.5, 0.2, "obs")]
b += [T(p.X(2.5) + 4, p.Y(0.2), "+2,5", "an sm resc"), T(p.X(-2.5) - 4, p.Y(0.2), "−2,5", "an sm resc", "end"), T(120, 122, "área vermelha = p-valor = 0,012", "an sm resc", "middle"), T(120, 136, "(0,006 em cada cauda)", "an sm", "middle")]
save("v_pvalor", ''.join(b), "p-valor como a área nas caudas além do valor observado", 240, 142)

p = P(12, 230, 14, 104, -4, 4, 0, 0.45)
b = [p.area(npdf, 1.96, 4), p.area(npdf, -4, -1.96), p.base(), p.curve(npdf, -4, 4)]
b += [T(p.X(0), p.Y(0.07), "não rejeita", "an sm", "middle"), T(p.X(3.1), p.Y(0.1), "rejeita", "an sm resc", "middle"), T(p.X(-3.1), p.Y(0.1), "rejeita", "an sm resc", "middle")]
b += [T(p.X(1.96), 118, "+1,96", "tk", "middle"), T(p.X(-1.96), 118, "−1,96", "tk", "middle"), T(120, 134, "α = 5%: 2,5% em cada cauda", "an sm", "middle")]
save("v_alfa", ''.join(b), "Regiões de rejeição de 2,5 por cento em cada cauda para alfa de 5 por cento")

b = []
offs = [0.3, -0.5, 0.8, -0.2, 0.1, -0.9, 0.4, 1.7, -0.4, 0.6]
p = P(12, 230, 10, 112, -3, 3, 0, 11)
b.append(p.line(0, 0, 0, 11, "true"))
for i, o in enumerate(offs):
    y = 10.3 - i; miss = abs(o) > 1.2; c = "obs" if miss else "fit"
    b += [p.line(o - 1.2, y, o + 1.2, y, c), p.dot(o, y, 2.6, "ptB" if miss else "pt")]
b += [T(p.X(0) + 4, 122, "β verdadeiro", "an sm"), T(120, 136, "95% dos ICs cobrem β (aqui, 9 de 10)", "an sm", "middle")]
save("v_ic", ''.join(b), "Dez intervalos de confiança de amostras diferentes; nove cobrem o valor verdadeiro", 240, 142)

p = P(12, 230, 14, 104, -3.2, 6, 0, 0.45)
b = [p.area(npdf, 1.96, 4.2, "rej"), p.area(lambda x: npdf(x, 2.8), -1, 1.96, "bandf"), p.base(), p.curve(npdf, -3.2, 3.6, "cB"), p.curve(lambda x: npdf(x, 2.8), -0.5, 6), p.line(1.96, 0, 1.96, 0.44, "obs")]
b += [T(p.X(-1.9), p.Y(0.2), "H₀", "an sm"), T(p.X(3.9), p.Y(0.36), "H₁", "an sm fitc"), T(p.X(2.25), p.Y(0.03), "α", "an resc"), T(p.X(1.4), p.Y(0.06), "β", "an fitc")]
b += [T(120, 120, "α = P(tipo I); área β = P(tipo II)", "an sm", "middle"), T(120, 134, "poder = 1 − P(tipo II)", "an sm", "middle")]
save("v_erros", ''.join(b), "Duas distribuições, sob a hipótese nula e sob a alternativa, com as áreas dos erros tipo I e tipo II")

b = []
for k, (lab, tails) in enumerate([("bilateral: ±1,96", 2), ("unilateral: +1,645", 1)]):
    p = P(8 + k*118, 112 + k*118, 16, 96, -3.5, 3.5, 0, 0.45)
    if tails == 2: b += [p.area(npdf, 1.96, 3.5), p.area(npdf, -3.5, -1.96)]
    else: b.append(p.area(npdf, 1.645, 3.5))
    b += [p.base(), p.curve(npdf, -3.5, 3.5), T((p.L + p.R)/2, 112, lab, "an sm", "middle")]
b.append(T(120, 132, "≠: duas caudas; > ou <: uma", "an sm", "middle"))
save("v_unibi", ''.join(b), "Teste bilateral com duas caudas e teste unilateral com uma cauda")

# ============================ F. Problemas ============================
b = []
for cx, cy, t, c in [(40, 96, "x", "nb"), (200, 96, "y", "nb"), (120, 28, "z (omitida)", "nr")]:
    w = 84 if len(t) > 2 else 44
    b += [f'<rect class="{c}" x="{cx-w/2}" y="{cy-15}" width="{w}" height="30" rx="8"/>', T(cx, cy + 5, t, "an", "middle", ' font-weight="700"')]
b += [arrow(64, 96, 176, 96), arrow(150, 42, 186, 80), arrow(90, 42, 54, 80, "arw")]
b += [T(120, 90, "β₁", "an sm fitc", "middle"), T(176, 56, "β₂", "an sm"), T(80, 66, "anda junto", "an sm")]
b.append(T(120, 132, "z fica no u e “empresta” efeito a x", "an sm resc", "middle"))
save("v_omitida", ''.join(b), "Diagrama: a variável omitida afeta y e anda junto com x, contaminando a inclinação")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
random.seed(71); b = [p.axes()]
for _ in range(14):
    x = random.uniform(1.5, 8.5); y = 1 + 0.9*x + random.gauss(0, 0.4); xm = min(9.7, max(0.3, x + random.gauss(0, 1.8)))
    b += [p.dot(xm, y, 2.6, "ptB")]
b += [p.line(0, 1, 10, 10, "truel"), p.line(0, 2.8, 10, 7.8, "fit")]
b += [T(p.X(9.8), p.Y(2.2), "tracejada: verdadeira", "an sm", "end"), T(p.X(9.8), p.Y(0.9), "azul: estimada, mais plana", "an sm fitc", "end")]
b.append(T(120, 130, "erro de medida em x achata a reta", "an sm", "middle"))
save("v_medida", ''.join(b), "Com erro de medida em x, a reta estimada fica mais plana que a verdadeira")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
up = [f"{f(p.X(x/10))},{f(p.Y(2+0.6*x/10+0.25+0.3*x/10))}" for x in range(0, 101, 5)]; dn = [f"{f(p.X(x/10))},{f(p.Y(2+0.6*x/10-0.25-0.3*x/10))}" for x in range(100, -1, -5)]
b = [p.axes(), f'<polygon class="bandf" points="{" ".join(up+dn)}"/>', p.line(0, 2, 10, 8)]
b += [T(120, 126, "β̂ continua sem viés ✓", "an sm posc", "middle"), T(120, 141, "EP usual erra ✗ → use EP robusto", "an sm resc", "middle")]
save("v_hetero", ''.join(b), "Funil de heterocedasticidade: o estimador continua sem viés, mas o erro-padrão usual fica errado", 240, 146)

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), scatter(p, 81, 16, lambda x: 0.5 + 0.9*x, 0.35, 0.8, 9.4), T(p.R - 2, p.B - 6, "x₁", "an sm", "end"), T(p.L + 4, p.T + 10, "x₂", "an sm")]
b += [T(p.X(1.2), p.Y(8.6), "quase uma reta:", "an sm"), T(p.X(1.2), p.Y(7.3), "VIF alto", "an sm resc")]
b.append(T(120, 130, "x₁ e x₂ juntos: difícil separar efeitos", "an sm", "middle"))
save("v_multicol", ''.join(b), "Duas variáveis explicativas quase perfeitamente alinhadas: multicolinearidade")

p = P(16, 228, 14, 104, 0, 40, -3, 3)
random.seed(7); u = [0]; pts = []
for t in range(40): u.append(0.8*u[-1] + random.gauss(0, 0.6))
b = [p.base(), p.line(0, 0, 40, 0, "mean"), f'<polyline class="fit" points="{" ".join(f"{f(p.X(t))},{f(p.Y(max(-2.9,min(2.9,v))))}" for t, v in enumerate(u[1:]))}"/>']
b += [T(p.R, 118, "tempo →", "tk", "end"), T(120, 134, "resíduos em ondas: hoje parece ontem", "an sm", "middle")]
save("v_autocorr", ''.join(b), "Resíduos ao longo do tempo formando ondas longas: autocorrelação")

# ============================ G. Formas funcionais e grupos ============================
p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), p.curve(lambda x: 1.2*math.exp(0.2*x), 0, 10)]
for x in (3, 6): b += [p.dot(x, 1.2*math.exp(0.2*x), 3), p.line(x, 1.2*math.exp(0.2*x), x + 1, 1.2*math.exp(0.2*x), "tri"), p.line(x + 1, 1.2*math.exp(0.2*x), x + 1, 1.2*math.exp(0.2*(x+1)), "tri")]
b += [T(p.X(0.3), p.Y(9.2), "ln y = β₀ + β₁x", "an sm fitc"), T(120, 130, "+1 em x ⇒ ≈ 100·β₁ % em y", "an sm", "middle")]
save("v_lognivel", ''.join(b), "Curva exponencial: cada unidade a mais de x aumenta y na mesma porcentagem")

p = P(16, 228, 10, 112, 0.2, 10, 0, 10)
b = [p.axes(), p.curve(lambda x: 2 + 3*math.log(x), 0.6, 10)]
b += [T(p.X(3.5), p.Y(3.0), "y = β₀ + β₁·ln x", "an sm fitc"), T(p.X(3.5), p.Y(1.5), "ganhos cada vez menores", "an sm")]
b.append(T(120, 130, "+1% em x ⇒ β₁/100 unidades de y", "an sm", "middle"))
save("v_nivellog", ''.join(b), "Curva logarítmica: nível-log, com ganhos decrescentes")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
b = [p.axes(), p.curve(lambda x: 1.8*x**0.6, 0, 10)]
for x0 in (2, 6): b += [p.dot(x0, 1.8*x0**0.6, 3), p.dot(x0*1.3, 1.8*(x0*1.3)**0.6, 3)]
b += [T(p.X(0.3), p.Y(9.2), "ln y = β₀ + β₁·ln x", "an sm fitc"), T(120, 130, "+1% em x ⇒ β₁ % em y (elasticidade)", "an sm", "middle")]
save("v_loglog", ''.join(b), "Curva de elasticidade constante do modelo log-log")

p = P(16, 228, 10, 112, 0, 12, 30, 80)
b = [p.axes(), p.curve(lambda q: 40 + 12*q - q*q, 0, 12), p.line(6, 30, 6, 76, "mean"), p.dot(6, 76, 3.6), p.line(4.6, 76, 7.4, 76, "tg0")]
b += [T(p.X(6), p.Y(76) - 8, "topo: x* = −β₁/(2β₂) = 6", "an sm", "middle"), T(120, 130, "inclinação = β₁ + 2β₂x (muda com x)", "an sm", "middle")]
save("v_quadratico", ''.join(b), "Parábola com o ponto de virada onde a inclinação é zero")

p = P(16, 228, 10, 112, 0, 4.4, 6, 16)
b = [p.axes()]
for grp, xc, c in [([8, 9, 10, 9, 9], 1, "pt"), ([13, 14, 12, 14, 12], 3, "ptB")]:
    seen = {}
    for y in grp:
        k = seen.get(y, 0); seen[y] = k + 1; b.append(p.dot(xc + (k - (grp.count(y) - 1)/2)*0.16, y, 3.2, c))
b += [p.line(1, 9, 3, 13), diamond(p.X(1), p.Y(9)), diamond(p.X(3), p.Y(13)), p.line(3.5, 9, 3.5, 13, "brk"), p.line(1, 9, 3.5, 9, "mean")]
b += [T(p.X(3.5) + 4, p.Y(11) + 4, "β₁ = 4", "an sm posc"), T(p.X(1.2), p.Y(6.6), "β₀ = 9 (D = 0)", "an sm resc", "middle"), T(p.X(3), p.Y(15.2), "D = 1: 13", "an sm", "middle")]
b.append(T(120, 130, "dummy: β₁ = diferença de médias", "an sm", "middle"))
save("v_dummy", ''.join(b), "Dois grupos: o intercepto é a média do grupo base e o coeficiente da dummy é a diferença de médias")

p = P(16, 228, 10, 112, 0, 10, 0, 12)
b = [p.axes(), p.line(0, 2, 10, 7), p.line(0, 3, 10, 11, "tgn")]
for x in (2, 8): b.append(p.line(x, 2 + 0.5*x, x, 3 + 0.8*x, "brk"))
b += [T(p.X(9.8), p.Y(7) + 22, "D = 0", "an sm fitc", "end"), T(p.X(9.8), p.Y(11) - 6, "D = 1", "an sm resc", "end")]
b.append(T(120, 130, "interação D·x: inclinações diferentes", "an sm", "middle"))
save("v_interacao", ''.join(b), "Duas retas com inclinações diferentes: interação entre a dummy e x")

p = P(16, 228, 10, 112, 0, 10, 0, 10)
xs = [3, 4, 5, 6, 7, 8]; ys = [5.1, 5.4, 6.3, 6.4, 7.2, 7.6]
b0, b1 = 3.0, 0.57
b1o = sum(x*y for x, y in zip(xs, ys))/sum(x*x for x in xs)
b = [p.axes()] + [p.dot(x, y) for x, y in zip(xs, ys)] + [p.line(0, b0, 10, b0 + 10*b1), p.line(0, 0, 10, 10*b1o, "tgn"), p.dot(0, 0, 4, "icpt")]
b += [T(p.X(0.3), p.Y(9.3), "vermelha: passa em (0, 0)", "an sm resc"), T(p.X(9.8), p.Y(1.2), "azul: com intercepto", "an sm fitc", "end")]
b.append(T(120, 130, "sem β₀: se o β₀ real ≠ 0, dá viés", "an sm", "middle"))
save("v_origem", ''.join(b), "Regressão pela origem forçada a passar em zero comparada com a reta com intercepto")

p = P(16, 228, 10, 112, 7, 17, 8, 36)
E = [8, 10, 12, 12, 14, 16]; H = [1, 2, 4, 3, 6, 8]; S = [12, 15, 23, 20, 29, 33]
b = [p.axes(), p.line(7.5, -11.6 + 2.8*7.5, 16.5, -11.6 + 2.8*16.5, "cC")]
for hb in (2, 6): b.append(p.line(7.5, 2 + 2*hb + 7.5, 16.5, 2 + 2*hb + 16.5, "samp"))
b += [p.dot(e, s) for e, s in zip(E, S)]
b += [T(p.X(7.2), p.Y(34.5), "vermelha: simples (2,8)", "an sm resc"), T(p.X(12.2), p.Y(12), "azuis: hab fixa (1)", "an sm fitc")]
b.append(T(120, 130, "múltipla: efeito com o resto constante", "an sm", "middle"))
save("v_multipla", ''.join(b), "Regressão múltipla: com habilidade fixa a inclinação é menor que na simples")
print("mini figs ok")

# ============================ Cartões (texto) ============================
# (slug, título, em uma frase, imagine, na prova, (link, rótulo), tag)
G = [
("v-estat", "A. Estatística do zero", [
 ("variavel", "Variável e observação", "Variável é uma característica medida (salário, educação); observação é cada unidade medida (uma pessoa, uma empresa, um ano).", "Uma planilha: cada coluna é uma variável e cada linha é uma observação.", "n = número de observações (linhas da tabela).", ("#zero", "Módulo 0"), ""),
 ("media", "Média (x̄)", "Soma tudo e divide pela quantidade: é o valor típico do grupo.", "Uma gangorra com os valores como pesos: a média é o ponto onde ela fica equilibrada.", r"\(\bar x=\frac1n\sum x_i\)", ("#estat", "Estatística do zero"), ""),
 ("mediana", "Mediana", "O valor do meio depois de ordenar os dados.", "Um milionário entra na sala: a média dos salários dispara, mas a mediana quase não muda.", "2, 3, 3, 4, 5, 6, 26: mediana 4, média 7.", ("#estat", "Estatística do zero"), ""),
 ("variancia", "Variância e desvio-padrão", "Medem o quanto os valores se espalham em torno da média. O desvio-padrão é a raiz da variância e volta à unidade original.", "Duas turmas com média 5: numa todos tiram quase 5; na outra, as notas vão de 1 a 9.", r"\(s^2=\frac{\sum(x_i-\bar x)^2}{n-1}\), \(s=\sqrt{s^2}\)", ("#estat", "Estatística do zero"), ""),
 ("correlacao", "Covariância e correlação", "Dizem se duas variáveis andam juntas. A correlação vai de −1 a +1: o sinal dá a direção; o tamanho, o quanto os pontos se alinham numa reta.", "Altura e peso: quem é mais alto tende a pesar mais (correlação positiva).", r"\(Corr=\dfrac{Cov(x,y)}{s_x\,s_y}\); mede só relação linear.", ("#estat", "Estatística do zero"), ""),
 ("normal", "Distribuição normal", "A curva em forma de sino: a maioria dos valores fica perto da média e poucos ficam nos extremos.", "Alturas de adultos: muita gente perto da média, pouquíssima gente muito alta ou muito baixa.", "≈ 68% a 1 desvio-padrão da média; ≈ 95% a 2 (exato: 1,96).", ("#estat", "Estatística do zero"), ""),
 ("esperanca", "Esperança E(X)", "A média de longo prazo de uma variável aleatória: o que se obtém, em média, repetindo muitas vezes.", "Nenhuma jogada de dado dá 3,5, mas a média de mil jogadas fica perto de 3,5.", r"\(E(X)=\sum x\,P(x)\); \(E(aX+b)=aE(X)+b\)", ("#estat", "Estatística do zero"), ""),
 ("amostra", "População × amostra", "População é o grupo todo que interessa; amostra é a parte que você de fato observa.", "Provar uma colher (amostra) para saber o gosto da panela inteira (população).", "Parâmetros (β, μ) são da população; estimativas (β̂, x̄) vêm da amostra.", ("#conceitos", "Conceitos-chave"), ""),
]),
("v-estim", "B. Estimadores e suas propriedades", [
 ("param", "Parâmetro, estimador e estimativa", "Parâmetro é o valor verdadeiro e fixo (β). Estimador é a regra de cálculo (a fórmula do MQO). Estimativa é o número que a regra deu na sua amostra (1,15).", "O centro do alvo é o parâmetro; o jeito de mirar é o estimador; cada flecha é uma estimativa.", "“As propriedades pertencem ao estimador; a estimativa é uma realização dele.”", ("#conceitos", "Conceitos-chave"), ""),
 ("vies", "Viés", "O erro sistemático: quanto, em média, o estimador fica longe do valor verdadeiro.", "Uma balança que sempre marca 1 kg a mais: pesar mil vezes não faz o erro sumir.", r"\(\text{Viés}=E(\hat\beta)-\beta\); não viesado quando \(E(\hat\beta)=\beta\).", ("#aula5", "Aula 5"), ""),
 ("varest", "Variância do estimador", "O quanto a estimativa muda de uma amostra para outra. Variância pequena = estimador preciso.", "Um arqueiro que acerta o centro na média, mas com as flechas espalhadas.", r"\(Var(\hat\beta_1\mid X)=\sigma^2/SQT_x\)", ("#aula5", "Aula 5"), ""),
 ("eqm", "Erro quadrático médio (EQM)", "O erro total médio: junta a variância e o viés ao quadrado num número só.", "Um relógio sempre 1 minuto adiantado pode ser mais útil que um que erra 5 minutos para qualquer lado.", "EQM = Var + viés² (Lista em sala: 4 + 1 = 5, contra 8 da fonte sem viés).", ("#listasala", "Lista em sala"), ""),
 ("amostral", "Distribuição amostral", "Repetindo a amostragem muitas vezes, cada amostra daria um β̂; o histograma desses valores é a distribuição amostral.", "Mil pesquisas eleitorais diferentes: cada uma dá um número um pouco diferente.", "O centro dela mostra se há viés; a largura mostra a precisão.", ("#aula5", "Aula 5"), ""),
 ("consistencia", "Consistência", "Com cada vez mais dados, o estimador chega tão perto quanto se queira do valor verdadeiro.", "Uma foto que fica mais nítida à medida que aumenta a resolução.", r"\(\text{plim}\,\hat\beta_1=\beta_1\); o MQO é consistente se \(Cov(x,u)=0\).", ("#aula5", "Aula 5"), ""),
 ("eficiencia", "Eficiência e Gauss–Markov (BLUE)", "Entre os estimadores sem viés, o eficiente é o de menor variância. Gauss–Markov: sob RLS.1–RLS.5, o MQO é o melhor entre os lineares não viesados.", "Dois arqueiros que acertam o centro na média: o melhor é o que espalha menos.", "BLUE = Best Linear Unbiased Estimator.", ("#aula5", "Aula 5"), ""),
 ("lgn", "Lei dos Grandes Números", "A média de uma amostra grande fica perto da média da população.", "Jogue um dado muitas vezes: a média das jogadas se aproxima de 3,5.", r"\(\bar X\xrightarrow{p}\mu\) quando n → ∞.", ("#lgn", "Leis dos Grandes Números"), ""),
 ("tcl", "Teorema Central do Limite", "A média de muitas observações tem distribuição aproximadamente normal, mesmo que os dados não sejam.", "Rendas individuais são muito tortas, mas as médias de muitas amostras formam um sino.", r"\(\bar X\approx N(\mu,\sigma^2/n)\) para n grande.", ("#lgn", "Leis dos Grandes Números"), ""),
]),
("v-mqo", "C. Regressão e MQO", [
 ("regressao", "Regressão linear simples", "Uma reta que resume como y muda, em média, quando x muda.", "Traçar com a régua a linha que melhor passa pelo meio da nuvem de pontos.", r"\(y=\beta_0+\beta_1x+u\); estimada: \(\hat y=\hat\beta_0+\hat\beta_1x\)", ("#aula3", "Aula 3"), ""),
 ("mqo", "MQO / OLS", "O método que escolhe, entre todas as retas, a de menor soma dos resíduos ao quadrado.", "Cada ponto erra a reta um pouco; o MQO fica com a reta que erra menos no total, contando cada erro ao quadrado.", r"\(\min\sum(y_i-b_0-b_1x_i)^2\Rightarrow\hat\beta_1=\frac{Cov}{Var},\ \hat\beta_0=\bar y-\hat\beta_1\bar x\)", ("#aula3", "Aula 3"), ""),
 ("erro_residuo", "Erro (u) × resíduo (û)", "O erro é a distância até a reta verdadeira, que ninguém vê; o resíduo é a distância até a reta estimada, que dá para calcular.", "O erro é a distância até o tesouro de verdade; o resíduo, até onde o seu mapa diz que ele está.", r"\(\hat u_i=y_i-\hat y_i\); com intercepto, \(\sum\hat u_i=0\) e \(\sum x_i\hat u_i=0\).", ("#aula3", "Aula 3"), ""),
 ("ajustado", "Valor ajustado e ponto das médias", "ŷ é a altura da reta num certo x: a previsão da média de y. A reta do MQO sempre passa por (x̄, ȳ).", "Ler na régua (a reta) o valor que corresponde a um x.", r"\(\hat y_i=\hat\beta_0+\hat\beta_1x_i\); \(\bar y=\hat\beta_0+\hat\beta_1\bar x\)", ("#betas", "Os betas, visualmente"), ""),
 ("r2", "SQT, SQE, SQR e R²", "SQT é a variação total de y; SQE, a parte que a reta explica; SQR, o que sobra nos resíduos. O R² é a fração explicada.", "Uma pizza inteira (SQT) dividida no pedaço explicado (SQE) e no pedaço que sobrou (SQR).", "SQT = SQE + SQR; R² = SQE/SQT = 1 − SQR/SQT. E de Explicada, R de Resíduos.", ("#betas-sq", "Os betas, seção 12"), ""),
 ("sigma", "Variância do erro (σ² e σ̂²)", "O quanto os pontos se espalham em torno da reta verdadeira. Como é desconhecida, é estimada a partir dos resíduos.", "A espessura da nuvem de pontos em volta da reta.", r"\(\hat\sigma^2=SQR/(n-2)\): divide por n − 2 porque estimamos 2 parâmetros.", ("#aula3", "Aula 3"), ""),
 ("sqtx", "Variação de x (SQTₓ) e precisão", "Quanto mais espalhados os valores de x, mais firme fica a inclinação estimada.", "Para medir a inclinação de uma rampa, dois pontos distantes funcionam melhor que dois pontos colados.", r"\(Var(\hat\beta_1)=\sigma^2/SQT_x\): mais variação em x (ou mais n) ⇒ menos variância.", ("#aula5", "Aula 5"), ""),
 ("extrapolacao", "Extrapolação", "Usar a reta para x fora da faixa observada. Nada garante que a relação continue igual lá fora.", "Uma criança cresce 6 cm por ano; isso não quer dizer que terá 3 metros aos 50 anos.", "Lista em sala, Ex. 5: prever em X = 4 com dados de 0 a 3 é extrapolação.", ("#listasala", "Lista em sala"), ""),
]),
("v-hip", "D. As hipóteses RLS.1 a RLS.6", [
 ("rls1", "RLS.1 · Linear nos parâmetros", "O modelo é uma soma de parâmetros vezes variáveis. As variáveis podem ser transformadas (log, quadrado); os β entram lineares.", "A receita pode usar ingredientes processados (ln x, x²), mas cada um entra numa quantidade fixa (β).", r"\(\ln y=\beta_0+\beta_1\ln x+u\) também satisfaz RLS.1.", ("#aula5", "Aula 5"), ""),
 ("rls2", "RLS.2 · Amostragem aleatória", "As observações são sorteadas ao acaso da mesma população, independentes umas das outras.", "Sortear nomes de uma urna, em vez de entrevistar só os amigos.", "Garante que a amostra represente a população.", ("#aula5", "Aula 5"), ""),
 ("rls3", "RLS.3 · Variação em x", "Os valores de x na amostra não podem ser todos iguais.", "Se todos estudaram 12 anos, não há como ver o efeito de estudar mais.", r"\(SQT_x>0\); sem isso, a fórmula de \(\hat\beta_1\) divide por zero.", ("#aula5", "Aula 5"), ""),
 ("rls4", "RLS.4 · Média condicional zero", "O que ficou no erro u não tem relação com x: para cada x, u tem média zero. É a hipótese que garante a ausência de viés.", "Se a habilidade (que está no u) cresce junto com o estudo (x), o efeito do estudo sai inflado.", r"\(E(u\mid x)=0\ \Rightarrow\ E(\hat\beta_1)=\beta_1\)", ("#aula5", "Aula 5"), ""),
 ("rls5", "RLS.5 · Homocedasticidade", "O espalhamento dos pontos em torno da reta é o mesmo para todo x.", "A faixa em volta da reta tem largura constante, sem virar funil.", r"\(Var(u\mid x)=\sigma^2\) ⇒ vale \(Var(\hat\beta_1)=\sigma^2/SQT_x\) e Gauss–Markov.", ("#aula5", "Aula 5"), ""),
 ("rls6", "RLS.6 · Normalidade do erro", "O erro segue uma normal de média zero, independente de x. Com isso, o teste t é exato mesmo com poucos dados.", "Os desvios em relação à reta seguem o formato de sino.", r"\(u\sim N(0,\sigma^2)\Rightarrow t\sim t_{n-2}\); em amostras grandes, o TCL dispensa.", ("#aula6", "Aula 6"), ""),
]),
("v-inf", "E. Inferência: EP, t, p-valor e IC", [
 ("ep", "Erro-padrão (EP)", "O tamanho típico do erro da estimativa: o desvio-padrão estimado de β̂.", "O tremor do seu número: quanto ele mudaria com outra amostra.", r"\(EP(\hat\beta_1)=\hat\sigma/\sqrt{SQT_x}\)", ("#aula6", "Aula 6"), ""),
 ("t", "Estatística t", "Quantos erros-padrão a estimativa está do valor da hipótese nula.", "Medir uma distância em passos do tamanho do EP.", r"\(t=\dfrac{\hat\beta_1-\beta_{1,0}}{EP(\hat\beta_1)}\); rejeita se |t| > crítico.", ("#h0-h1-pvalor", "H₀, H₁ e p-valor do zero"), ""),
 ("pvalor", "p-valor", "Se H₀ fosse verdadeira, a chance de obter um resultado tão ou mais extremo que o seu.", "O quanto o seu resultado seria surpreendente num mundo onde H₀ vale.", "p < α ⇒ rejeita H₀. Não é a probabilidade de H₀ ser verdadeira.", ("#h0-h1-pvalor", "H₀, H₁ e p-valor do zero"), ""),
 ("alfa", "Nível de significância (α) e valor crítico", "α é o risco, escolhido antes, de rejeitar H₀ quando ela é verdadeira. Ele define a região de rejeição.", "O rigor de um juiz: α baixo exige mais provas para condenar.", r"α = 5% bilateral: rejeita se |t| > 1,96 (normal) ou \(t_{0{,}025;\,n-2}\).", ("#aula6", "Aula 6"), ""),
 ("ic", "Intervalo de confiança", "A faixa de valores compatíveis com os dados. O procedimento cobre o β verdadeiro em 95% das amostras.", "Jogar uma rede em vez de uma lança: a rede pega o peixe em 95% das vezes.", r"\(\hat\beta_1\pm t_c\cdot EP\); contém exatamente os valores que o teste não rejeita.", ("#aula6", "Aula 6"), ""),
 ("erros", "Erro tipo I, tipo II e poder", "Tipo I: rejeitar H₀ verdadeira (chance α). Tipo II: não rejeitar H₀ falsa. Poder: chance de rejeitar uma H₀ falsa.", "Tipo I é condenar um inocente; tipo II é soltar um culpado.", "Poder = 1 − P(tipo II); cresce com n e com efeitos maiores.", ("#aula6", "Aula 6"), ""),
 ("unibi", "Teste bilateral × unilateral", "Bilateral testa “diferente” (duas caudas); unilateral testa “maior” ou “menor” (uma cauda).", "Procurar o erro dos dois lados da estrada ou só de um lado.", "5%: bilateral ±1,96; unilateral 1,645 (normal).", ("#aula6", "Aula 6"), ""),
]),
("v-prob", "F. Problemas do modelo", [
 ("omitida", "Viés de variável omitida", "Se algo que afeta y fica de fora e anda junto com x, a inclinação de x leva parte do efeito do que foi omitido.", "Creditar ao estudo um salário maior que, em parte, vem da habilidade.", r"\(E(\tilde\beta_1)=\beta_1+\beta_2\delta_1\) (ex.: 1 + 2 × 0,9 = 2,8).", ("#aula5", "Aula 5"), ""),
 ("medida", "Erro de medida em x (atenuação)", "Se x é medido com erro aleatório, a inclinação estimada fica mais perto de zero que a verdadeira.", "Olhar a relação através de um vidro embaçado: a tendência parece mais fraca do que é.", r"\(\text{plim}\,\hat\beta_1=\beta_1\dfrac{Var(x^*)}{Var(x^*)+Var(r)}\)", ("#aula5", "Aula 5"), ""),
 ("hetero", "Heterocedasticidade e EP robusto", "O espalhamento muda com x (funil). O MQO continua sem viés, mas o EP usual fica errado e o MQO deixa de ser o mais eficiente.", "Os gastos de famílias ricas variam muito mais que os de famílias pobres.", "Use EP robusto (HC); detecte com Breusch–Pagan.", ("#aula6", "Aula 6"), ""),
 ("multicol", "Multicolinearidade", "Quando as explicativas andam muito juntas, fica difícil separar o efeito de cada uma. Não causa viés; aumenta os EPs.", "Dois cantores que só cantam em dueto: não dá para saber quem canta melhor.", "VIF = 1/(1 − R²ⱼ); VIF alto ⇒ EP grande.", ("#p2", "Prévia da P2"), "P2"),
 ("autocorr", "Autocorrelação", "Em séries de tempo, o erro de hoje se parece com o de ontem.", "Um dia chuvoso costuma vir depois de outro dia chuvoso.", r"AR(1): \(u_t=\rho u_{t-1}+e_t\); Durbin–Watson ≈ 2(1 − ρ̂).", ("#p2", "Prévia da P2"), "P2"),
]),
("v-formas", "G. Formas funcionais, dummies e múltipla", [
 ("lognivel", "Log–nível (ln y)", "Com log em y, o β vira variação percentual de y para +1 em x.", "Um salário que cresce 8% a cada ano de estudo, como juros compostos.", r"+1 em x ⇒ ≈ 100·β₁ % em y; exato: \(100(e^{\beta_1}-1)\%\).", ("#aula4", "Aula 4"), ""),
 ("nivellog", "Nível–log (ln x)", "Com log em x, +1% em x muda y em β₁/100 unidades: ganhos decrescentes.", "Os primeiros R$ 1.000 de propaganda rendem mais vendas que os décimos R$ 1.000.", "+1% em x ⇒ β₁/100 unidades de y.", ("#aula4", "Aula 4"), ""),
 ("loglog", "Log–log e elasticidade", "Com log nos dois lados, β₁ é a elasticidade: a variação percentual de y para +1% em x.", "O preço sobe 1% e a quantidade cai β₁%.", "+1% em x ⇒ β₁ % em y.", ("#aula4", "Aula 4"), ""),
 ("quadratico", "Modelo quadrático", "Com x e x², a inclinação muda ao longo da curva: pode subir e depois cair.", "Adubo ajuda a colheita até certo ponto; depois, atrapalha.", "Inclinação β₁ + 2β₂x; virada em x* = −β₁/(2β₂).", ("#aula4", "Aula 4"), ""),
 ("dummy", "Variável dummy", "Uma variável 0/1 que marca um grupo. Seu β é a diferença média entre os grupos.", "Um interruptor: ligado (D = 1), a reta sobe β₁.", r"\(y=\beta_0+\beta_1D\): β₀ = média do grupo D = 0; β₁ = diferença de médias.", ("#dummies", "Aula de dummies"), ""),
 ("interacao", "Interação D·x", "Permite que a inclinação de x seja diferente em cada grupo.", "Um ano de estudo pode valer mais para um grupo do que para outro.", "Diferença entre os grupos: β₂ + β₃x (muda com x).", ("#dummies", "Aula de dummies"), ""),
 ("origem", "Regressão pela origem", "Reta sem intercepto, obrigada a passar em (0, 0).", "Obrigar a régua a encostar no canto do gráfico, mesmo que os pontos não peçam.", r"\(\hat\beta_1=\sum x_iy_i/\sum x_i^2\); se o β₀ verdadeiro ≠ 0, há viés.", ("#dummies", "Aula de dummies"), ""),
 ("multipla", "Regressão múltipla (ceteris paribus)", "Com várias explicativas, cada β mede o efeito da sua variável mantendo as outras fixas.", "Comparar só pessoas com a mesma habilidade para ver o efeito de estudar mais.", r"\(y=\beta_0+\beta_1x_1+\beta_2x_2+u\); β₁: efeito de x₁ com x₂ constante.", ("#p2", "Prévia da P2"), "P2"),
]),
]
CARD = {c[0]: c for g in G for c in g[2]}
assert len(CARD) == 51 and all(os.path.exists(f"{FIGS}/v_{k}.svg") for k in CARD), "falta figura"

def full(c):
    slug, t, fr, im, pr, (href, lab), tag = c
    tg = f' <span class="tag warn">{tag}</span>' if tag else ""
    return (f'<article class="vcard" id="c-{slug}"><div class="vfig">FIG:v_{slug}</div><h4>{t}{tg}</h4>'
            f'<p><span class="k">Em uma frase:</span> {fr}</p><p><span class="k">Imagine:</span> {im}</p>'
            f'<p class="vprova"><span class="k">Na prova:</span> {pr}</p><a class="vlink" href="{href}">Aprofundar: {lab} →</a></article>')
def small(slug):
    _, t, fr, _, _, _, _ = CARD[slug]
    return (f'<a class="vcard vsmall" href="#c-{slug}"><div class="vfig">FIG:v_{slug}</div><h4>{t}</h4>'
            f'<p>{fr}</p><span class="vlink">cartão completo no Mapa visual →</span></a>')

out = ['', '<!-- ================= MAPA VISUAL (gerado por tools/visual.py) ================= -->',
       '<section class="mod" id="mapa" data-title="Mapa visual">',
       '  <div class="eyebrow"><span class="tag hot">Visual</span> Todos os conceitos do curso, um desenho para cada</div>',
       '  <h2>Mapa visual: todos os conceitos em desenho</h2>',
       '  <p>Cada cartão explica <strong>um conceito</strong> com um mini desenho e três linhas: <strong>em uma frase</strong> (o que é, sem jargão), <strong>imagine</strong> (uma comparação do dia a dia) e <strong>na prova</strong> (a fórmula ou a frase que vale ponto). O link no pé do cartão leva à explicação completa. Use o mapa para revisar rápido ou quando um conceito “não entrar”.</p>',
       '  <div class="vtools"><label for="vsearch" class="small">Procurar conceito</label><input id="vsearch" type="search" placeholder="ex.: viés, p-valor, dummy" autocomplete="off"><span class="small" id="vcount"></span></div>',
       '  <nav class="vnav" aria-label="Grupos do mapa">' + ''.join(f'<a href="#{gid}">{gt.split(". ",1)[0]}. {gt.split(". ",1)[1]}</a>' for gid, gt, _ in G) + '</nav>']
for gid, gt, cards in G:
    out.append(f'  <h3 id="{gid}" class="vgh">{gt}</h3>')
    out.append('  <div class="vgrid">' + '\n'.join(full(c) for c in cards) + '</div>')
out.append('''  <h3>Teste rápido</h3>
  <div class="quiz" data-answer="b"><div class="qh">Alvos</div>
    <p>Num alvo, as flechas estão todas juntas, mas longe do centro. Isso descreve um estimador:</p>
    <div class="opts"><button data-k="a">a) sem viés e com variância alta</button><button data-k="b">b) viesado e com variância baixa</button><button data-k="c">c) sem viés e com variância baixa</button><button data-k="d">d) consistente</button></div>
    <div class="fb" hidden>b. Flechas juntas = pouca variância; longe do centro = erro sistemático (viés).</div></div>
  <div class="quiz" data-answer="c"><div class="qh">Funil</div>
    <p>Os pontos formam um funil em volta da reta (espalhamento cresce com x). O que acontece com o MQO?</p>
    <div class="opts"><button data-k="a">a) fica viesado</button><button data-k="b">b) deixa de ser consistente</button><button data-k="c">c) continua sem viés, mas o EP usual fica errado</button><button data-k="d">d) nada muda</button></div>
    <div class="fb" hidden>c. Heterocedasticidade viola RLS.5, não RLS.4: o centro continua certo, mas a fórmula usual da variância (e do EP) não vale. Use EP robusto.</div></div>
  <div class="quiz" data-answer="a"><div class="qh">Erro × resíduo</div>
    <p>A distância de um ponto até a reta <strong>estimada</strong> é:</p>
    <div class="opts"><button data-k="a">a) o resíduo û</button><button data-k="b">b) o erro u</button><button data-k="c">c) o viés</button><button data-k="d">d) o erro-padrão</button></div>
    <div class="fb" hidden>a. O erro u é a distância até a reta verdadeira, que não observamos.</div></div>
  <div class="quiz" data-answer="d"><div class="qh">p-valor</div>
    <p>Um p-valor de 0,012 significa que:</p>
    <div class="opts"><button data-k="a">a) H₀ tem 1,2% de chance de ser verdadeira</button><button data-k="b">b) o efeito é pequeno</button><button data-k="c">c) há 98,8% de chance de H₁ ser verdadeira</button><button data-k="d">d) se H₀ fosse verdadeira, resultados tão extremos quanto o observado ocorreriam em cerca de 1,2% das amostras</button></div>
    <div class="fb" hidden>d. O p-valor é calculado supondo H₀ verdadeira; não é a probabilidade de H₀ nem de H₁.</div></div>
  <div class="done-row"><button class="btn done-btn" data-done="mapa" aria-pressed="false">Marcar como concluído</button></div>
</section>
''')
open(os.path.join(BASE, "parts", "01b_visual.html"), "w").write('\n'.join(out))

STR = {"zero": ["variavel", "media", "variancia"],
       "estat": ["media", "mediana", "variancia", "correlacao", "normal", "esperanca", "amostra"],
       "conceitos": ["param", "vies", "varest", "mqo", "erro_residuo", "rls5", "multicol", "dummy"],
       "aula1": ["variavel", "amostra", "param", "omitida"],
       "aula2": ["esperanca", "variancia", "correlacao", "normal", "lgn", "tcl", "pvalor", "ic"],
       "lgn": ["lgn", "tcl", "consistencia"],
       "aula3": ["regressao", "mqo", "erro_residuo", "ajustado", "r2", "sigma"],
       "aula4": ["lognivel", "nivellog", "loglog", "quadratico"],
       "aula5": ["amostral", "vies", "varest", "sqtx", "eficiencia", "consistencia", "rls4", "rls5", "omitida", "medida"],
       "aula6": ["ep", "t", "pvalor", "alfa", "ic", "erros", "unibi", "hetero"],
       "dummies": ["dummy", "interacao", "origem"],
       "p2": ["multipla", "multicol", "autocorr"]}
for k, slugs in STR.items():
    open(f"{STRIPS}/{k}.html", "w").write(
        f'<details class="vstrip" open><summary>Este conteúdo em desenhos ({len(slugs)} cartões)</summary>'
        f'<div class="vgrid">' + '\n'.join(small(s) for s in slugs) + '</div>'
        f'<p class="small vmore"><a href="#mapa">Ver todos os conceitos no Mapa visual →</a></p></details>')
print("cards ok:", len(CARD), "strips:", len(STR))
