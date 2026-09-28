import math, random, os
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"parts","figs")
os.makedirs(OUT, exist_ok=True)
def f(v): return f"{v:.1f}".rstrip('0').rstrip('.') if abs(v-round(v))>1e-9 else str(int(round(v)))
def br(v, d=2):
    s=f"{v:.{d}f}".replace('.',',')
    return s
def save(name, s):
    open(f"{OUT}/{name}.svg","w").write(s)

class Plot:
    def __init__(s, W,H, L,R,T,B, xmin,xmax,ymin,ymax):
        s.W,s.H,s.L,s.R,s.T,s.B=W,H,L,R,T,B; s.xmin,s.xmax,s.ymin,s.ymax=xmin,xmax,ymin,ymax
    def X(s,x): return s.L+(x-s.xmin)/(s.xmax-s.xmin)*(s.R-s.L)
    def Y(s,y): return s.B-(y-s.ymin)/(s.ymax-s.ymin)*(s.B-s.T)
    def axes(s, xt, yt, xlab, ylab, xfmt=str, yfmt=str, grid=True):
        o=[]
        if grid:
            for v in yt: o.append(f'<line class="g" x1="{f(s.L)}" y1="{f(s.Y(v))}" x2="{f(s.R)}" y2="{f(s.Y(v))}"/>')
            for v in xt: o.append(f'<line class="g" x1="{f(s.X(v))}" y1="{f(s.T)}" x2="{f(s.X(v))}" y2="{f(s.B)}"/>')
        o.append(f'<line class="ax" x1="{f(s.L)}" y1="{f(s.B)}" x2="{f(s.R)}" y2="{f(s.B)}"/>')
        o.append(f'<line class="ax" x1="{f(s.L)}" y1="{f(s.T)}" x2="{f(s.L)}" y2="{f(s.B)}"/>')
        for v in xt: o.append(f'<text class="tk" x="{f(s.X(v))}" y="{f(s.B+16)}" text-anchor="middle">{xfmt(v)}</text>')
        for v in yt: o.append(f'<text class="tk" x="{f(s.L-7)}" y="{f(s.Y(v)+4)}" text-anchor="end">{yfmt(v)}</text>')
        o.append(f'<text class="lb" x="{f((s.L+s.R)/2)}" y="{f(s.H-6)}" text-anchor="middle">{xlab}</text>')
        o.append(f'<text class="lb" x="12" y="{f((s.T+s.B)/2)}" text-anchor="middle" transform="rotate(-90 12 {f((s.T+s.B)/2)})">{ylab}</text>')
        return '\n'.join(o)

def svg(W,H,body,label):
    return f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>'

# ---------- A: Aula 3 exemplo (5 indivíduos) ----------
P=Plot(520,320, 58,500,18,270, 6,18,6,22)
xs=[8,10,12,14,16]; ys=[10,12,15,15,20]
b=[P.axes([6,8,10,12,14,16,18],[6,10,14,18,22],"Anos de estudo (x)","Salário/hora, R$ (y)")]
x0,x1=6.5,17.5
b.append(f'<line class="fit" x1="{f(P.X(x0))}" y1="{f(P.Y(0.6+1.15*x0))}" x2="{f(P.X(x1))}" y2="{f(P.Y(0.6+1.15*x1))}"/>')
for x,y in zip(xs,ys):
    yh=0.6+1.15*x
    b.append(f'<line class="res" x1="{f(P.X(x))}" y1="{f(P.Y(y))}" x2="{f(P.X(x))}" y2="{f(P.Y(yh))}"/>')
for x,y in zip(xs,ys):
    b.append(f'<circle class="pt" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="5"/>')
# mean point
b.append(f'<line class="mean" x1="{f(P.X(12))}" y1="{f(P.B)}" x2="{f(P.X(12))}" y2="{f(P.Y(14.4))}"/>')
b.append(f'<line class="mean" x1="{f(P.L)}" y1="{f(P.Y(14.4))}" x2="{f(P.X(12))}" y2="{f(P.Y(14.4))}"/>')
b.append(f'<rect class="meanpt" x="{f(P.X(12)-6)}" y="{f(P.Y(14.4)-6)}" width="12" height="12" transform="rotate(45 {f(P.X(12))} {f(P.Y(14.4))})"/>')
b.append(f'<text class="an" x="{f(P.X(12)+12)}" y="{f(P.Y(14.4)+18)}">(x̄, ȳ) = (12; 14,4)</text>')
b.append(f'<text class="an fitc" x="{f(P.X(13.2))}" y="{f(P.Y(19.9))}">ŷ = 0,6 + 1,15x</text>')
b.append(f'<text class="an resc" x="{f(P.X(14)+8)}" y="{f(P.Y(15.9))}">û₄ = −1,7</text>')
save("a3_exemplo", svg(520,320,'\n'.join(b),"Gráfico de dispersão dos 5 indivíduos com a reta de MQO"))

# ---------- B: aluguel x área (esboço da lousa) ----------
P=Plot(520,320, 64,500,18,270, 0,100,0,3200)
b=[P.axes([0,20,40,60,80,100],[0,800,1600,2400,3200],"Área (m²)","Aluguel (R$)",yfmt=lambda v: f"{v:,}".replace(',','.'))]
b.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(560))}" x2="{f(P.X(100))}" y2="{f(P.Y(560+2400))}"/>')
b.append(f'<line class="mean" x1="{f(P.X(60))}" y1="{f(P.B)}" x2="{f(P.X(60))}" y2="{f(P.Y(2000))}"/>')
b.append(f'<line class="mean" x1="{f(P.L)}" y1="{f(P.Y(2000))}" x2="{f(P.X(60))}" y2="{f(P.Y(2000))}"/>')
b.append(f'<rect class="meanpt" x="{f(P.X(60)-6)}" y="{f(P.Y(2000)-6)}" width="12" height="12" transform="rotate(45 {f(P.X(60))} {f(P.Y(2000))})"/>')
b.append(f'<text class="an" x="{f(P.X(60)-8)}" y="{f(P.Y(2000)-12)}" text-anchor="end">(x̄, ȳ) = (60; 2.000)</text>')
b.append(f'<circle class="icpt" cx="{f(P.X(0))}" cy="{f(P.Y(560))}" r="5"/>')
b.append(f'<text class="an" x="{f(P.X(0)+10)}" y="{f(P.Y(560)+18)}">β̂₀ = 560 (altura quando área = 0)</text>')
# slope triangle between 70 and 80
x1,x2=78,88
b.append(f'<path class="tri" d="M{f(P.X(x1))} {f(P.Y(560+24*x1))} H{f(P.X(x2))} V{f(P.Y(560+24*x2))}"/>')
b.append(f'<text class="an" x="{f(P.X(83))}" y="{f(P.Y(560+24*x1)+16)}" text-anchor="middle">+10 m²</text>')
b.append(f'<text class="an" x="{f(P.X(x2)+6)}" y="{f(P.Y(560+24*85))}">+R$ 240</text>')
b.append(f'<circle class="pt" cx="{f(P.X(70))}" cy="{f(P.Y(2300))}" r="5"/>')
b.append(f'<circle class="fitpt" cx="{f(P.X(70))}" cy="{f(P.Y(2240))}" r="4"/>')
b.append(f'<text class="an" x="{f(P.X(70)-8)}" y="{f(P.Y(2300)-10)}" text-anchor="end">70 m²: observado 2.300; ajustado 2.240</text>')
b.append(f'<text class="an fitc" x="{f(P.X(22))}" y="{f(P.Y(1350))}">alugûel = 560 + 24·área</text>')
save("aluguel", svg(520,320,'\n'.join(b),"Reta estimada do aluguel contra a área passando pelo ponto das médias"))

# ---------- C: parábola Ex 4 ----------
P=Plot(520,330, 58,500,18,280, 0,12,30,80)
b=[P.axes([0,2,4,6,8,10,12],[30,40,50,60,70,80],"Q (centenas de unidades)","Lucro ajustado (R$ mil)")]
pts=[]
for i in range(0,241):
    q=i*12/240; pts.append(f"{f(P.X(q))},{f(P.Y(40+12*q-q*q))}")
b.append(f'<polyline class="fit" points="{" ".join(pts)}"/>')
for q,sl,cls in [(2,8,"tg"),(6,0,"tg0"),(8,-4,"tgn")]:
    L=40+12*q-q*q; d=0.9
    b.append(f'<line class="{cls}" x1="{f(P.X(q-d))}" y1="{f(P.Y(L-sl*d))}" x2="{f(P.X(q+d))}" y2="{f(P.Y(L+sl*d))}"/>')
    b.append(f'<circle class="pt" cx="{f(P.X(q))}" cy="{f(P.Y(L))}" r="5"/>')
b.append(f'<line class="mean" x1="{f(P.X(6))}" y1="{f(P.B)}" x2="{f(P.X(6))}" y2="{f(P.Y(76))}"/>')
b.append(f'<text class="an" x="{f(P.X(2)+10)}" y="{f(P.Y(60)+16)}">Q=2: inclinação +8</text>')
b.append(f'<text class="an" x="{f(P.X(6))}" y="{f(P.Y(76)-12)}" text-anchor="middle">Q*=6: inclinação 0 → lucro máx. 76</text>')
b.append(f'<text class="an" x="{f(P.X(8)+10)}" y="{f(P.Y(72)+4)}">Q=8: inclinação −4</text>')
b.append(f'<text class="an fitc" x="{f(P.X(9.2))}" y="{f(P.Y(47))}">lucro = 40 + 12Q − Q²</text>')
save("parabola", svg(520,330,'\n'.join(b),"Parábola do lucro com retas tangentes em Q igual a 2, 6 e 8"))

# ---------- D: 4 alvos ----------
random.seed(7)
def target(cx,cy,off,spread,title):
    o=[]
    for r,cls in [(62,"t1"),(44,"t2"),(26,"t3"),(9,"t4")]:
        o.append(f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
    for k in range(10):
        a=random.random()*2*math.pi; rr=abs(random.gauss(0,spread))
        o.append(f'<circle class="shot" cx="{f(cx+off[0]+rr*math.cos(a))}" cy="{f(cy+off[1]+rr*math.sin(a))}" r="3.6"/>')
    o.append(f'<text class="an" x="{cx}" y="{cy+84}" text-anchor="middle">{title}</text>')
    return '\n'.join(o)
b=[target(80,80,(0,0),7,"Não viesado, baixa variância"),target(260,80,(0,0),26,"Não viesado, alta variância"),
   target(440,80,(26,-20),7,"Viesado, baixa variância"),target(620,80,(26,-20),26,"Viesado, alta variância")]
save("alvos", svg(700,180,'\n'.join(b),"Quatro alvos combinando viés e variância"))

# ---------- E: distribuições amostrais ----------
def npdf(x,m,s): return math.exp(-0.5*((x-m)/s)**2)/(s*math.sqrt(2*math.pi))
P=Plot(560,300, 40,540,20,250, 0.2,2.2,0,4.2)
b=[P.axes([0.4,0.8,1.2,1.64,2.0],[],"valores possíveis do estimador",""," ".join, xfmt=lambda v: br(v,2).rstrip('0').rstrip(','))] if False else []
b.append(P.axes([0.4,0.8,1.2,1.64,2.0],[],"valores possíveis da estimativa de β₁","",xfmt=lambda v: (f"{v:.2f}".rstrip('0').rstrip('.')).replace('.',','),grid=False))
for m,sd,cls,lab,lx in [(0.8,0.1,"cA","precisa (SQTₓ grande)",0.95),(0.8,0.25,"cB","imprecisa (SQTₓ pequeno)",0.2),(1.64,0.1,"cC","viesada (variável omitida)",1.78)]:
    pts=[f"{f(P.X(x/200))},{f(P.Y(npdf(x/200,m,sd)))}" for x in range(40,441)]
    b.append(f'<polyline class="{cls}" points="{" ".join(pts)}"/>')
b.append(f'<line class="true" x1="{f(P.X(0.8))}" y1="{f(P.T-4)}" x2="{f(P.X(0.8))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an" x="{f(P.X(0.8)+6)}" y="{f(P.T+8)}">β₁ = 0,8 (verdadeiro)</text>')
b.append(f'<text class="an cAt" x="{f(P.X(0.93))}" y="{f(P.Y(3.2))}">precisa: SQTₓ grande</text>')
b.append(f'<text class="an cBt" x="{f(P.X(0.25))}" y="{f(P.Y(1.1))}">imprecisa: SQTₓ pequeno</text>')
b.append(f'<text class="an cCt" x="{f(P.X(1.76))}" y="{f(P.Y(3.2))}">viesada: centro em 1,64</text>')
save("distribuicoes", svg(560,300,'\n'.join(b),"Três distribuições amostrais: precisa, imprecisa e viesada"))

# ---------- F: homo x hetero ----------
def band(x0,title,het):
    P=Plot(0,0, x0+20,x0+250,20,190, 0,10,0,10)
    o=[f'<line class="ax" x1="{P.L}" y1="{P.B}" x2="{P.R}" y2="{P.B}"/>',f'<line class="ax" x1="{P.L}" y1="{P.T}" x2="{P.L}" y2="{P.B}"/>']
    up=[];dn=[]
    for i in range(0,51):
        x=i/5; m=1.5+0.7*x; w=(0.4+0.28*x) if het else 1.4
        up.append(f"{f(P.X(x))},{f(P.Y(m+w))}"); dn.append(f"{f(P.X(x))},{f(P.Y(m-w))}")
    o.append(f'<polygon class="bandf" points="{" ".join(up+dn[::-1])}"/>')
    o.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(1.5))}" x2="{f(P.X(10))}" y2="{f(P.Y(8.5))}"/>')
    random.seed(3 if het else 4)
    for k in range(40):
        x=random.uniform(0.3,9.7); m=1.5+0.7*x; w=(0.4+0.28*x) if het else 1.4
        y=m+random.uniform(-1,1)*w*0.9
        o.append(f'<circle class="pt sm" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="2.6"/>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="212" text-anchor="middle">{title}</text>')
    o.append(f'<text class="tk" x="{P.R}" y="{P.B+14}" text-anchor="end">x</text><text class="tk" x="{P.L-6}" y="{P.T+8}" text-anchor="end">y</text>')
    return '\n'.join(o)
save("homohetero", svg(560,222, band(0,"Homocedasticidade: faixa constante",False)+band(290,"Heterocedasticidade: faixa cresce com x",True),"Comparação entre homocedasticidade e heterocedasticidade"))

# ---------- G: distribuição t (3 g.l.) ----------
def t3(t): return (1/(math.sqrt(3)*math.pi/2))*(1+t*t/3)**-2  # Gamma(2)/(sqrt(3pi)Gamma(1.5)) = 1/(sqrt3 * pi/2)
# check normalization factor: Gamma(2)=1, Gamma(1.5)=sqrt(pi)/2 -> 1/(sqrt(3pi)*sqrt(pi)/2) = 2/(sqrt3*pi)
def t3(t): return 2/(math.sqrt(3)*math.pi)*(1+t*t/3)**-2
P=Plot(560,280, 30,540,20,230, -7.5,7.5,0,0.4)
b=[P.axes([-6,-3.182,0,3.182,6],[],"estatística t (n − 2 = 3 graus de liberdade)","",xfmt=lambda v: (f"{v:g}").replace('.',','),grid=False)]
for side in (-1,1):
    xs_=[side*(3.182+i*(7.5-3.182)/80) for i in range(81)]
    pts=[f"{f(P.X(x))},{f(P.Y(t3(x)))}" for x in xs_]
    pts=[f"{f(P.X(side*3.182))},{f(P.B)}"]+pts+[f"{f(P.X(side*7.5))},{f(P.B)}"]
    b.append(f'<polygon class="rej" points="{" ".join(pts)}"/>')
pts=[f"{f(P.X(x/20))},{f(P.Y(t3(x/20)))}" for x in range(-150,151)]
b.append(f'<polyline class="fit" points="{" ".join(pts)}"/>')
b.append(f'<line class="obs" x1="{f(P.X(6.08))}" y1="{f(P.Y(0.2))}" x2="{f(P.X(6.08))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(6.08))}" y="{f(P.Y(0.2)-8)}" text-anchor="middle">t = 6,08</text>')
b.append(f'<text class="an" x="{f(P.X(0))}" y="{f(P.Y(0.2))}" text-anchor="middle">não rejeita H₀ (95%)</text>')
b.append(f'<text class="an resc" x="{f(P.X(-5.3))}" y="{f(P.Y(0.06))}" text-anchor="middle">rejeita (2,5%)</text>')
b.append(f'<text class="an resc" x="{f(P.X(4.6))}" y="{f(P.Y(0.06))}" text-anchor="middle">rejeita (2,5%)</text>')
save("tdist", svg(560,280,'\n'.join(b),"Distribuição t com 3 graus de liberdade e regiões de rejeição"))

# ---------- H: poder (Lista 3 Q8) ----------
P=Plot(560,280, 30,540,20,230, -0.8,1.4,0,2.2)
b=[P.axes([-0.392,0,0.392,0.6,1.0],[],"valores de β̂₁ (erro-padrão 0,20)","",xfmt=lambda v: (f"{v:g}").replace('.',','),grid=False)]
# type II area under H1 between -0.392 and 0.392
xs_=[-0.392+i*(0.784)/80 for i in range(81)]
pts=[f"{f(P.X(-0.392))},{f(P.B)}"]+[f"{f(P.X(x))},{f(P.Y(npdf(x,0.6,0.2)))}" for x in xs_]+[f"{f(P.X(0.392))},{f(P.B)}"]
b.append(f'<polygon class="bandf" points="{" ".join(pts)}"/>')
for m,cls in [(0,"cB"),(0.6,"cA")]:
    pts=[f"{f(P.X(x/200))},{f(P.Y(npdf(x/200,m,0.2)))}" for x in range(-160,281)]
    b.append(f'<polyline class="{cls}" points="{" ".join(pts)}"/>')
for v in (-0.392,0.392):
    b.append(f'<line class="true" x1="{f(P.X(v))}" y1="{f(P.T)}" x2="{f(P.X(v))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an cBt" x="{f(P.X(-0.05))}" y="{f(P.Y(2.05))}" text-anchor="end">sob H₀: β₁ = 0</text>')
b.append(f'<text class="an cAt" x="{f(P.X(0.66))}" y="{f(P.Y(2.05))}">se β₁ = 0,6</text>')
b.append(f'<text class="an" x="{f(P.X(0.02))}" y="{f(P.B-8)}" text-anchor="middle">erro tipo II ≈ 0,149</text>')
save("poder", svg(560,280,'\n'.join(b),"Região de não rejeição e probabilidade de erro tipo II"))

# ---------- I: formas funcionais ----------
def mini(x0,title,fn,xmin=0.2):
    P=Plot(0,0, x0+10,x0+120,10,110, 0,10,0,10)
    o=[f'<line class="ax" x1="{P.L}" y1="{P.B}" x2="{P.R}" y2="{P.B}"/>',f'<line class="ax" x1="{P.L}" y1="{P.T}" x2="{P.L}" y2="{P.B}"/>']
    pts=[f"{f(P.X(x/10))},{f(P.Y(fn(x/10)))}" for x in range(int(xmin*10),101)]
    o.append(f'<polyline class="fit" points="{" ".join(pts)}"/>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="132" text-anchor="middle">{title}</text>')
    return '\n'.join(o)
body=mini(0,"Nível–nível",lambda x:1+0.8*x)+mini(145,"Log–nível",lambda x:0.8*math.exp(0.25*x))+mini(290,"Nível–log",lambda x:2+3.2*math.log(x),xmin=0.55)+mini(435,"Log–log (β₁<1)",lambda x:3*x**0.5)
save("formas", svg(575,142,body,"Formato das quatro formas funcionais"))
print(sorted(os.listdir(OUT)))

# ================= v2: matemática de apoio e lacunas =================
# ---------- tangente x secante: f(x)=x² ----------
P=Plot(520,320, 58,500,18,270, 0,5,0,20)
b=[P.axes([0,1,2,3,4,5],[0,5,10,15,20],"x","f(x) = x²")]
pts=[f"{f(P.X(i/50))},{f(P.Y((i/50)**2))}" for i in range(0,224)]
b.append(f'<polyline class="fit" points="{" ".join(pts)}"/>')
# secant through (3,9),(4,16): slope 7
x1,x2=1.9,4.4
b.append(f'<line class="tgn" x1="{f(P.X(x1))}" y1="{f(P.Y(9+7*(x1-3)))}" x2="{f(P.X(x2))}" y2="{f(P.Y(9+7*(x2-3)))}"/>')
# tangent at 3: slope 6
b.append(f'<line class="tg" x1="{f(P.X(1.8))}" y1="{f(P.Y(9+6*(1.8-3)))}" x2="{f(P.X(4.6))}" y2="{f(P.Y(9+6*(4.6-3)))}"/>')
for x in (3,4): b.append(f'<circle class="pt" cx="{f(P.X(x))}" cy="{f(P.Y(x*x))}" r="5"/>')
b.append(f'<text class="an resc" x="{f(P.X(4.05))}" y="{f(P.Y(17.5))}">secante (3→4): inclinação 7</text>')
b.append(f'<text class="an" x="{f(P.X(3.2))}" y="{f(P.Y(8.2))}" style="fill:var(--green)">tangente em x = 3: inclinação 6</text>')
save("tangente", svg(520,320,'\n'.join(b),"Reta secante e reta tangente à parábola x ao quadrado"))

# ---------- exponencial e ln ----------
P=Plot(520,320, 58,500,18,270, -2,5,-2,5)
b=[P.axes([-2,-1,0,1,2,3,4,5],[-2,-1,0,1,2,3,4,5],"x","y")]
b.append(f'<line class="mean" x1="{f(P.X(-2))}" y1="{f(P.Y(-2))}" x2="{f(P.X(5))}" y2="{f(P.Y(5))}"/>')
pts=[f"{f(P.X(x/100))},{f(P.Y(math.exp(x/100)))}" for x in range(-200,161)]
b.append(f'<polyline class="fit" points="{" ".join(pts)}"/>')
pts=[f"{f(P.X(x/100))},{f(P.Y(math.log(x/100)))}" for x in range(14,501)]
b.append(f'<polyline class="cC" points="{" ".join(pts)}"/>')
b.append(f'<circle class="pt" cx="{f(P.X(0))}" cy="{f(P.Y(1))}" r="4"/><circle class="pt" cx="{f(P.X(1))}" cy="{f(P.Y(0))}" r="4"/>')
b.append(f'<text class="an fitc" x="{f(P.X(1.7))}" y="{f(P.Y(4.6))}">y = eˣ</text>')
b.append(f'<text class="an resc" x="{f(P.X(3.6))}" y="{f(P.Y(1.7))}">y = ln x</text>')
b.append(f'<text class="an" x="{f(P.X(3.3))}" y="{f(P.Y(3.9))}">y = x (espelho)</text>')
b.append(f'<text class="an" x="{f(P.X(0.12))}" y="{f(P.Y(1.25))}">(0, 1)</text><text class="an" x="{f(P.X(1.1))}" y="{f(P.Y(-0.35))}">(1, 0)</text>')
save("explog", svg(520,320,'\n'.join(b),"Gráficos da exponencial e do logaritmo natural, espelhados na reta y igual a x"))

# ---------- soma de retângulos: ∫0^2 x dx ----------
P=Plot(520,300, 58,500,18,250, 0,2.2,0,2.4)
b=[P.axes([0,0.5,1,1.5,2],[0,0.5,1,1.5,2],"x","f(x) = x",xfmt=lambda v:(f"{v:g}").replace('.',','),yfmt=lambda v:(f"{v:g}").replace('.',','))]
for k in range(4):
    x0=k*0.5; h=x0+0.5
    b.append(f'<rect class="bandf" x="{f(P.X(x0))}" y="{f(P.Y(h))}" width="{f(P.X(0.5)-P.X(0))}" height="{f(P.Y(0)-P.Y(h))}" style="stroke:var(--marker);stroke-width:1"/>')
b.append(f'<polygon class="rej" points="{f(P.X(0))},{f(P.Y(0))} {f(P.X(2))},{f(P.Y(2))} {f(P.X(2))},{f(P.Y(0))}"/>')
b.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(0))}" x2="{f(P.X(2.2))}" y2="{f(P.Y(2.2))}"/>')
b.append(f'<text class="an" x="{f(P.X(0.1))}" y="{f(P.Y(2.15))}">4 retângulos pela direita: 2,5 · área exata (triângulo): 2</text>')
save("riemann", svg(520,300,'\n'.join(b),"Área sob f de x igual a x aproximada por retângulos"))

# ---------- Uniforme U(0,10) ----------
P=Plot(520,260, 58,500,18,210, -1,11,0,0.14)
b=[P.axes([0,2,5,10],[0,0.1],"x","f(x)",yfmt=lambda v:(f"{v:g}").replace('.',','),grid=False)]
b.append(f'<rect class="rej" x="{f(P.X(2))}" y="{f(P.Y(0.1))}" width="{f(P.X(5)-P.X(2))}" height="{f(P.Y(0)-P.Y(0.1))}"/>')
b.append(f'<polyline class="fit" points="{f(P.X(-1))},{f(P.Y(0))} {f(P.X(0))},{f(P.Y(0))} {f(P.X(0))},{f(P.Y(0.1))} {f(P.X(10))},{f(P.Y(0.1))} {f(P.X(10))},{f(P.Y(0))} {f(P.X(11))},{f(P.Y(0))}"/>')
b.append(f'<text class="an" x="{f(P.X(3.5))}" y="{f(P.Y(0.05))}" text-anchor="middle">área = 3 × 0,1 = 0,3</text>')
b.append(f'<text class="an fitc" x="{f(P.X(7.5))}" y="{f(P.Y(0.115))}" text-anchor="middle">f(x) = 1/10</text>')
save("uniforme", svg(520,260,'\n'.join(b),"Densidade uniforme entre 0 e 10 com a área entre 2 e 5 destacada"))

# ---------- R² alto x baixo ----------
def r2panel(x0,title,spread,seed):
    P=Plot(0,0, x0+20,x0+250,20,190, 0,10,0,12)
    o=[f'<line class="ax" x1="{P.L}" y1="{P.B}" x2="{P.R}" y2="{P.B}"/>',f'<line class="ax" x1="{P.L}" y1="{P.T}" x2="{P.L}" y2="{P.B}"/>']
    o.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(1.5))}" x2="{f(P.X(10))}" y2="{f(P.Y(9.5))}"/>')
    random.seed(seed)
    for k in range(30):
        x=random.uniform(0.4,9.6); y=1.5+0.8*x+random.gauss(0,spread)
        y=max(0.2,min(11.8,y))
        o.append(f'<circle class="pt sm" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="2.8"/>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="212" text-anchor="middle">{title}</text>')
    return '\n'.join(o)
save("r2", svg(560,222, r2panel(0,"R² ≈ 0,96: pontos colados na reta",0.45,11)+r2panel(290,"R² ≈ 0,20: pontos espalhados",3.2,12),"Mesma reta com R quadrado alto e baixo"))

# ---------- Lagrange: max xy s.a. 2x+4y=40 ----------
P=Plot(520,320, 58,500,18,270, 0,22,0,12)
b=[P.axes([0,5,10,15,20],[0,2,4,6,8,10,12],"x","y")]
b.append(f'<line class="tgn" x1="{f(P.X(0))}" y1="{f(P.Y(10))}" x2="{f(P.X(20))}" y2="{f(P.Y(0))}"/>')
for U,cls in [(50,"fit"),(30,"cB"),(80,"cB")]:
    pts=[f"{f(P.X(x/10))},{f(P.Y(U/(x/10)))}" for x in range(int(U/12*10)+1,221)]
    b.append(f'<polyline class="{cls}" points="{" ".join(pts)}"/>')
b.append(f'<circle class="pt" cx="{f(P.X(10))}" cy="{f(P.Y(5))}" r="5"/>')
b.append(f'<text class="an" x="{f(P.X(10.6))}" y="{f(P.Y(5.6))}">ótimo (10, 5): xy = 50, λ = 2,5</text>')
b.append(f'<text class="an resc" x="{f(P.X(13.2))}" y="{f(P.Y(1.1))}">restrição 2x + 4y = 40</text>')
b.append(f'<text class="an fitc" x="{f(P.X(15.5))}" y="{f(P.Y(3.8))}">xy = 50</text>')
save("lagrange", svg(520,320,'\n'.join(b),"Curva xy igual a 50 tangente à restrição 2x mais 4y igual a 40"))
print("v2 figs ok")

# ======================= v3: Aula 5, Aula 6 e Lista 3 =======================
def tpdf(t,v): return math.exp(math.lgamma((v+1)/2)-math.lgamma(v/2))/math.sqrt(v*math.pi)*(1+t*t/v)**(-(v+1)/2)
def nb(v,d=3):
    s=f"{v:.{d}f}".rstrip('0').rstrip('.'); return s.replace('.',',')

# ---------- enumeração: distribuição amostral exata de β̂1 ----------
P=Plot(560,300, 58,540,24,250, 1.4,5.1,0,0.6)
b=[P.axes([2,2.5,3,3.5,4,4.5],[0,0.25,0.5],"valores possíveis de β̂₁ nas 8 amostras","probabilidade",xfmt=lambda v: nb(v,1),yfmt=lambda v: nb(v,2))]
for v,p in [(2,.25),(3,.5),(4,.25)]:
    b.append(f'<rect class="barA" x="{f(P.X(v-0.17))}" y="{f(P.Y(p))}" width="{f(P.X(0.34)-P.X(0))}" height="{f(P.Y(0)-P.Y(p))}"/>')
for v,p in [(2.5,.25),(3.5,.5),(4.5,.25)]:
    b.append(f'<rect class="barB" x="{f(P.X(v-0.17))}" y="{f(P.Y(p))}" width="{f(P.X(0.34)-P.X(0))}" height="{f(P.Y(0)-P.Y(p))}"/>')
b.append(f'<line class="true" x1="{f(P.X(3))}" y1="{f(P.T-6)}" x2="{f(P.X(3))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an fitc" x="{f(P.X(3)-6)}" y="{f(P.T+4)}" text-anchor="end">E(β̂₁) = 3 = β₁ (sem viés)</text>')
b.append(f'<text class="an resc" x="{f(P.X(3.5)-8)}" y="{f(P.T+4)}">com E(u|x) ≠ 0: centro 3,5</text>')
b.append(f'<line class="true" x1="{f(P.X(3.5))}" y1="{f(P.T+10)}" x2="{f(P.X(3.5))}" y2="{f(P.Y(0.5))}"/>')
save("enum", svg(560,300,'\n'.join(b),"Distribuição amostral exata do estimador nas 8 amostras possíveis"))

# ---------- Lista 3 Q5: t com 16 g.l. ----------
P=Plot(560,330, 30,540,26,200, -4.2,4.2,0,0.42)
b=[P.axes([-2.667,0,2.667],[],"","",xfmt=lambda v: nb(v,3),grid=False)]
for side in (-1,1):
    xs_=[side*(2.667+i*(4.2-2.667)/60) for i in range(61)]
    pts=[f"{f(P.X(side*2.667))},{f(P.B)}"]+[f"{f(P.X(x))},{f(P.Y(tpdf(x,16)))}" for x in xs_]+[f"{f(P.X(side*4.2))},{f(P.B)}"]
    b.append(f'<polygon class="rej" points="{" ".join(pts)}"/>')
b.append(f'<polyline class="fit" points="{" ".join(f"{f(P.X(x/50))},{f(P.Y(tpdf(x/50,16)))}" for x in range(-210,211))}"/>')
b.append(f'<line class="obs" x1="{f(P.X(2.667))}" y1="{f(P.Y(0.2))}" x2="{f(P.X(2.667))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(2.667))}" y="{f(P.Y(0.2)-8)}" text-anchor="middle">t = 2,67</text>')
b.append(f'<text class="an" x="{f(P.X(-1.9))}" y="{f(P.Y(0.3))}" text-anchor="middle">p-valor = soma das</text>')
b.append(f'<text class="an" x="{f(P.X(-1.9))}" y="{f(P.Y(0.3)+17)}" text-anchor="middle">duas caudas vermelhas</text>')
# régua de zoom entre 2,0 e 3,0
Z=Plot(0,0, 60,520,0,0, 2.0,3.0,0,1); yz=280
b.append(f'<text class="lb" x="30" y="{yz-26}">zoom da cauda direita (16 g.l.):</text>')
b.append(f'<line class="ax" x1="{f(Z.X(2.0))}" y1="{yz}" x2="{f(Z.X(3.0))}" y2="{yz}"/>')
for v,lab,area,up in [(2.12,"2,120","2,5%",True),(2.583,"2,583","1%",False),(2.921,"2,921","0,5%",True)]:
    b.append(f'<line class="ax" x1="{f(Z.X(v))}" y1="{yz-7}" x2="{f(Z.X(v))}" y2="{yz+7}"/>')
    b.append(f'<text class="tk" x="{f(Z.X(v))}" y="{yz+22}" text-anchor="middle">{lab}</text>')
    b.append(f'<text class="an" x="{f(Z.X(v))}" y="{yz-12}" text-anchor="middle">{area}</text>')
b.append(f'<circle class="shot" cx="{f(Z.X(2.667))}" cy="{yz}" r="6"/>')
b.append(f'<text class="an resc" x="{f(Z.X(2.667))}" y="{yz+22}" text-anchor="middle">2,67</text>')
b.append(f'<text class="tk" x="{f(Z.X(3.0))}" y="{yz+40}" text-anchor="end">(% = área numa cauda além do valor)</text>')
save("tq5", svg(560,330,'\n'.join(b),"Distribuição t com 16 graus de liberdade, estatística 2,67 e valores críticos"))

# ---------- Lista 3 Q6: unilateral × bilateral (28 g.l.) ----------
def tpanel(x0,title,crit,two):
    P=Plot(0,0, x0+14,x0+266,34,190, -4,4,0,0.42)
    o=[f'<line class="ax" x1="{f(P.L)}" y1="{f(P.B)}" x2="{f(P.R)}" y2="{f(P.B)}"/>']
    sides=(-1,1) if two else (1,)
    for sd in sides:
        xs_=[sd*(crit+i*(4-crit)/50) for i in range(51)]
        pts=[f"{f(P.X(sd*crit))},{f(P.B)}"]+[f"{f(P.X(x))},{f(P.Y(tpdf(x,28)))}" for x in xs_]+[f"{f(P.X(sd*4))},{f(P.B)}"]
        o.append(f'<polygon class="rej" points="{" ".join(pts)}"/>')
        o.append(f'<text class="tk" x="{f(P.X(sd*crit))}" y="{f(P.B+15)}" text-anchor="middle">{nb(sd*crit,3)}</text>')
    o.append(f'<polyline class="fit" points="{" ".join(f"{f(P.X(x/40))},{f(P.Y(tpdf(x/40,28)))}" for x in range(-160,161))}"/>')
    o.append(f'<line class="obs" x1="{f(P.X(1.85))}" y1="{f(P.Y(0.3))}" x2="{f(P.X(1.85))}" y2="{f(P.B)}"/>')
    o.append(f'<text class="an resc" x="{f(P.X(1.85))}" y="{f(P.Y(0.3)-6)}" text-anchor="middle">t = 1,85</text>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="20" text-anchor="middle">{title}</text>')
    o.append(f'<text class="tk" x="{f(P.X(0))}" y="{f(P.B+15)}" text-anchor="middle">0</text>')
    return '\n'.join(o)
save("unibi", svg(580,212, tpanel(0,"Unilateral: 5% na cauda direita → rejeita",1.701,False)+tpanel(300,"Bilateral: 2,5% em cada cauda → não rejeita",2.048,True),"Comparação entre regiões de rejeição unilateral e bilateral"))

# ---------- intervalos de confiança (Q7 e Q10) ----------
def ciline(P,y,lo,hi,c,lab,cls="fit"):
    o=[f'<line class="{cls}" x1="{f(P.X(lo))}" y1="{y}" x2="{f(P.X(hi))}" y2="{y}"/>']
    for v in (lo,hi): o.append(f'<line class="{cls}" x1="{f(P.X(v))}" y1="{y-7}" x2="{f(P.X(v))}" y2="{y+7}"/>')
    o.append(f'<circle class="pt" cx="{f(P.X(c))}" cy="{y}" r="5"/>')
    o.append(f'<text class="an" x="{f(P.X(lo))}" y="{y-12}">{lab}</text>')
    return '\n'.join(o)
P=Plot(560,170, 30,540,20,130, -0.3,1.5,0,1)
b=[P.axes([0,0.203,0.72,1,1.237],[],"valores de β₁","",xfmt=lambda v: nb(v,3),grid=False)]
b.append(ciline(P,78,0.203,1.237,0.72,"IC 95% = [0,203; 1,237], centro β̂₁ = 0,72"))
for v,txt,cls in [(0,"0 está fora → rejeita H₀: β₁ = 0","resc"),(1,"1 está dentro → não rejeita H₀: β₁ = 1","fitc")]:
    b.append(f'<line class="true" x1="{f(P.X(v))}" y1="74" x2="{f(P.X(v))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(0)-4)}" y="112" text-anchor="end">rejeita β₁ = 0</text>')
b.append(f'<text class="an fitc" x="{f(P.X(1)+6)}" y="112">não rejeita β₁ = 1</text>')
save("icq7", svg(560,170,'\n'.join(b),"Intervalo de confiança da Questão 7 com os valores 0 e 1"))

P=Plot(560,190, 30,540,20,150, -0.6,1.8,0,1)
b=[P.axes([-0.4,0,0.2,0.6,1,1.6],[],"valores de β₁","",xfmt=lambda v: nb(v,2),grid=False)]
b.append(ciline(P,60,-0.4,1.6,0.6,"Estudo A: SQTₓ = 16, ep = 0,50 → [−0,40; 1,60]","cB"))
b.append(ciline(P,118,0.2,1.0,0.6,"Estudo B: SQTₓ = 100, ep = 0,20 → [0,20; 1,00]"))
b.append(f'<line class="obs" x1="{f(P.X(0))}" y1="30" x2="{f(P.X(0))}" y2="{f(P.B)}"/>')
save("icq10", svg(560,190,'\n'.join(b),"Intervalos de confiança dos estudos A e B da Questão 10"))
print("v3 figs ok")

# ======================= v4: estatística do zero, conceitos, LGN, P2 =======================
# ---------- 1 dado × média de 2 dados ----------
def bars(x0,title,vals,probs,ymax,xt):
    P=Plot(0,0, x0+40,x0+270,26,180, 0.5,6.5,0,ymax)
    o=[f'<line class="ax" x1="{f(P.L)}" y1="{f(P.B)}" x2="{f(P.R)}" y2="{f(P.B)}"/>',f'<line class="ax" x1="{f(P.L)}" y1="{f(P.T)}" x2="{f(P.L)}" y2="{f(P.B)}"/>']
    w=(P.X(1)-P.X(0))*(0.4 if len(vals)>6 else 0.7)
    for v,p in zip(vals,probs):
        o.append(f'<rect class="barA" x="{f(P.X(v)-w/2)}" y="{f(P.Y(p))}" width="{f(w)}" height="{f(P.Y(0)-P.Y(p))}"/>')
    for v in xt: o.append(f'<text class="tk" x="{f(P.X(v))}" y="{f(P.B+15)}" text-anchor="middle">{nb(v,1)}</text>')
    for v in (0.1,0.2): o.append(f'<text class="tk" x="{f(P.L-6)}" y="{f(P.Y(v)+4)}" text-anchor="end">{nb(v,1)}</text>')
    o.append(f'<line class="true" x1="{f(P.X(3.5))}" y1="{f(P.T)}" x2="{f(P.X(3.5))}" y2="{f(P.B)}"/>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="16" text-anchor="middle">{title}</text>')
    return '\n'.join(o)
v2=[1+i/2 for i in range(11)]; p2=[c/36 for c in (1,2,3,4,5,6,5,4,3,2,1)]
save("dados", svg(600,210, bars(0,"1 dado: todos com 1/6",[1,2,3,4,5,6],[1/6]*6,0.2,[1,2,3,4,5,6])+bars(300,"Média de 2 dados: o meio fica mais provável",v2,p2,0.2,[1,2,3,4,5,6]),"Distribuição de um dado e da média de dois dados"))

# ---------- normal 68-95-99,7 ----------
P=Plot(560,260, 30,540,20,210, -3.6,3.6,0,0.42)
b=[P.axes([-3,-2,-1,0,1,2,3],[],"desvios-padrão a partir da média (z)","",xfmt=lambda v: (f"{v:+g}" if v else "0").replace('+',''),grid=False)]
for k,cls in [(3,"t1"),(2,"t3"),(1,"t4")]:
    xs_=[-k+i*(2*k)/120 for i in range(121)]
    pts=[f"{f(P.X(-k))},{f(P.B)}"]+[f"{f(P.X(x))},{f(P.Y(npdf(x,0,1)))}" for x in xs_]+[f"{f(P.X(k))},{f(P.B)}"]
    b.append(f'<polygon class="{cls}" points="{" ".join(pts)}"/>')
b.append(f'<polyline class="fit" points="{" ".join(f"{f(P.X(x/40))},{f(P.Y(npdf(x/40,0,1)))}" for x in range(-144,145))}"/>')
b.append(f'<text class="an" x="{f(P.X(0))}" y="{f(P.Y(0.2))}" text-anchor="middle">68%</text>')
b.append(f'<text class="an" x="{f(P.X(1.5))}" y="{f(P.Y(0.06))}" text-anchor="middle">95%</text>')
b.append(f'<text class="an" x="{f(P.X(2.55))}" y="{f(P.Y(0.035))}" text-anchor="middle">99,7%</text>')
save("normal68", svg(560,260,'\n'.join(b),"Curva normal com as faixas de 68, 95 e 99,7 por cento"))

# ---------- boxplot ----------
P=Plot(560,170, 30,540,20,120, 0,28,0,1)
b=[P.axes([0,2,3,4,6,10.5,26],[],"salário (R$ mil)","",xfmt=lambda v: nb(v,1),grid=False)]
yc=P.Y(0.55)
b.append(f'<rect class="t3" x="{f(P.X(3))}" y="{f(yc-18)}" width="{f(P.X(6)-P.X(3))}" height="36"/>')
b.append(f'<line class="fit" x1="{f(P.X(4))}" y1="{f(yc-18)}" x2="{f(P.X(4))}" y2="{f(yc+18)}"/>')
for a_,c_ in [(2,3),(6,6)]: pass
b.append(f'<line class="ax" x1="{f(P.X(2))}" y1="{f(yc)}" x2="{f(P.X(3))}" y2="{f(yc)}"/><line class="ax" x1="{f(P.X(6))}" y1="{f(yc)}" x2="{f(P.X(6))}" y2="{f(yc)}"/>')
b.append(f'<line class="ax" x1="{f(P.X(2))}" y1="{f(yc-10)}" x2="{f(P.X(2))}" y2="{f(yc+10)}"/>')
b.append(f'<line class="true" x1="{f(P.X(10.5))}" y1="{f(yc-26)}" x2="{f(P.X(10.5))}" y2="{f(yc+26)}"/>')
b.append(f'<circle class="shot" cx="{f(P.X(26))}" cy="{f(yc)}" r="6"/>')
b.append(f'<text class="an resc" x="{f(P.X(26))}" y="{f(yc-14)}" text-anchor="middle">outlier (26)</text>')
b.append(f'<text class="an" x="{f(P.X(4.5))}" y="{f(yc-26)}" text-anchor="middle">Q1 = 3 · mediana = 4 · Q3 = 6</text>')
b.append(f'<text class="an" x="{f(P.X(10.5)+6)}" y="{f(yc+26)}">limite Q3 + 1,5·AIQ = 10,5</text>')
b.append(f'<polygon class="meanpt" points="{f(P.X(7))},{f(yc+12)} {f(P.X(7)-6)},{f(yc+22)} {f(P.X(7)+6)},{f(yc+22)}"/>')
b.append(f'<text class="an" x="{f(P.X(7))}" y="{f(yc+36)}" text-anchor="middle">média = 7</text>')
save("boxplot", svg(560,170,'\n'.join(b),"Boxplot dos salários com um outlier"))

# ---------- MQO: quadrados dos resíduos ----------
def sqpanel(x0,title,b0,b1,lab):
    P=Plot(0,0, x0+40,x0+270,30,200, 0.5,4.5,1,9.5)
    o=[f'<line class="ax" x1="{f(P.L)}" y1="{f(P.B)}" x2="{f(P.R)}" y2="{f(P.B)}"/>',f'<line class="ax" x1="{f(P.L)}" y1="{f(P.T)}" x2="{f(P.L)}" y2="{f(P.B)}"/>']
    xs=[1,2,3,4]; ys=[8,4,5,3]; tot=0
    for x,y in zip(xs,ys):
        yh=b0+b1*x; r=y-yh; tot+=r*r; side=abs(P.Y(y)-P.Y(yh))
        top=min(P.Y(y),P.Y(yh))
        o.append(f'<rect class="sqr" x="{f(P.X(x))}" y="{f(top)}" width="{f(side)}" height="{f(side)}"/>')
    o.append(f'<line class="fit" x1="{f(P.X(0.6))}" y1="{f(P.Y(b0+b1*0.6))}" x2="{f(P.X(4.4))}" y2="{f(P.Y(b0+b1*4.4))}"/>')
    for x,y in zip(xs,ys): o.append(f'<circle class="pt" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="4.5"/>')
    for v in xs: o.append(f'<text class="tk" x="{f(P.X(v))}" y="{f(P.B+15)}" text-anchor="middle">{v}</text>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="16" text-anchor="middle">{title}</text>')
    o.append(f'<text class="an resc" x="{f((P.L+P.R)/2)}" y="{f(P.B+34)}" text-anchor="middle">{lab}</text>')
    return '\n'.join(o)
save("mqo_quadrados", svg(600,250, sqpanel(0,"Reta do MQO: ŷ = 8,5 − 1,4x",8.5,-1.4,"soma das áreas = SQR = 4,2 (a menor possível)")+sqpanel(300,"Linha na média: ŷ = 5",5,0,"soma das áreas = 14"),"Quadrados dos resíduos para a reta de MQO e para a linha horizontal na média"))

# ---------- LGN: média corrente de lançamentos de dado ----------
random.seed(37); rolls=[random.randint(1,6) for _ in range(1000)]; acc=0; rm=[]
for i,r in enumerate(rolls,1): acc+=r; rm.append(acc/i)
P=Plot(560,260, 50,540,20,210, 0,1000,1.5,5.5)
b=[P.axes([0,200,400,600,800,1000],[2,3,3.5,4,5],"número de lançamentos (n)","média até ali",yfmt=lambda v: nb(v,1))]
b.append(f'<line class="true" x1="{f(P.L)}" y1="{f(P.Y(3.5))}" x2="{f(P.R)}" y2="{f(P.Y(3.5))}"/>')
b.append(f'<polyline class="fit" points="{" ".join(f"{f(P.X(i+1))},{f(P.Y(v))}" for i,v in enumerate(rm))}"/>')
b.append(f'<text class="an" x="{f(P.X(620))}" y="{f(P.Y(3.5)-10)}">E(X) = 3,5</text>')
b.append(f'<text class="an resc" x="{f(P.X(40))}" y="{f(P.Y(5.2))}">no começo, a média oscila muito</text>')
save("lgn", svg(560,260,'\n'.join(b),"Média corrente de mil lançamentos de um dado convergindo para 3,5"))
print("LGN final mean", rm[9], rm[99], rm[-1])

# ---------- resíduos independentes × AR(1) ----------
random.seed(7); e=[random.gauss(0,1) for _ in range(60)]; u=[e[0]]
for t in range(1,60): u.append(0.8*u[-1]+e[t])
def tspanel(x0,title,s):
    P=Plot(0,0, x0+20,x0+270,28,190, 0,60,-4.2,4.2)
    o=[f'<line class="ax" x1="{f(P.L)}" y1="{f(P.Y(0))}" x2="{f(P.R)}" y2="{f(P.Y(0))}"/>',f'<line class="ax" x1="{f(P.L)}" y1="{f(P.T)}" x2="{f(P.L)}" y2="{f(P.B)}"/>']
    o.append(f'<polyline class="cB" points="{" ".join(f"{f(P.X(i))},{f(P.Y(v))}" for i,v in enumerate(s))}"/>')
    for i,v in enumerate(s): o.append(f'<circle class="pt sm" cx="{f(P.X(i))}" cy="{f(P.Y(v))}" r="2.4"/>')
    o.append(f'<text class="an" x="{f((P.L+P.R)/2)}" y="16" text-anchor="middle">{title}</text>')
    o.append(f'<text class="tk" x="{f(P.R)}" y="{f(P.B+14)}" text-anchor="end">tempo t</text>')
    return '\n'.join(o)
save("ar1", svg(580,212, tspanel(0,"Sem autocorrelação: sobe e desce ao acaso",e)+tspanel(300,"AR(1) com ρ = 0,8: ondas longas",u),"Resíduos independentes comparados com resíduos autocorrelacionados"))
print("v4 figs ok")

# ======================= v5: Lista em sala =======================
# ---------- Ex. 1: distribuição de T (média δ+1, dp 2) ----------
P=Plot(560,250, 30,540,26,200, -6,8,0,0.22)
b=[P.axes([-4,-2,0,1,2,4,6],[],"valores de T (em torno de δ)","",xfmt=lambda v: {0:"δ",1:"δ+1"}.get(v,("δ"+("+" if v>0 else "−")+str(abs(v)))),grid=False)]
b.append(f'<polyline class="fit" points="{" ".join(f"{f(P.X(x/20))},{f(P.Y(npdf(x/20,1,2)))}" for x in range(-120,161))}"/>')
b.append(f'<line class="true" x1="{f(P.X(0))}" y1="{f(P.T)}" x2="{f(P.X(0))}" y2="{f(P.B)}"/>')
b.append(f'<line class="obs" x1="{f(P.X(1))}" y1="{f(P.Y(0.2))}" x2="{f(P.X(1))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an" x="{f(P.X(0)-6)}" y="{f(P.T+10)}" text-anchor="end">alvo δ</text>')
b.append(f'<text class="an resc" x="{f(P.X(1)+6)}" y="{f(P.Y(0.2)+4)}">centro de T: δ + 1 (viés +1)</text>')
b.append(f'<text class="an fitc" x="{f(P.X(4.6))}" y="{f(P.Y(0.07))}">dp(T) = 2</text>')
save("sala1", svg(560,250,'\n'.join(b),"Distribuição de T centrada em delta mais 1, com desvio-padrão 2"))

# ---------- Ex. 2: A × B ----------
P=Plot(560,250, 30,540,26,200, -3.5,4.5,0,0.45)
b=[P.axes([-2,-1,0,1,2,3],[],"valores da estimativa (em torno de θ)","",xfmt=lambda v: {0:"θ",1:"θ+1"}.get(v,("θ"+("+" if v>0 else "−")+str(abs(v)))),grid=False)]
for m,cls in [(0,"cA"),(1,"cC")]:
    b.append(f'<polyline class="{cls}" points="{" ".join(f"{f(P.X(x/20))},{f(P.Y(npdf(x/20,m,1)))}" for x in range(-70,91))}"/>')
b.append(f'<line class="true" x1="{f(P.X(0))}" y1="{f(P.T)}" x2="{f(P.X(0))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an cAt" x="{f(P.X(-0.2))}" y="{f(P.Y(0.42))}" text-anchor="end">B: centro θ, Var 1, EQM 1</text>')
b.append(f'<text class="an cCt" x="{f(P.X(1.25))}" y="{f(P.Y(0.42))}">A: centro θ + 1, Var 1, EQM 2</text>')
save("sala2", svg(560,250,'\n'.join(b),"Distribuições dos procedimentos A e B, com mesma variância e centros diferentes"))

# ---------- Ex. 3 e 4: intervalos ----------
P=Plot(560,160, 30,540,20,122, -0.6,2.4,0,1)
b=[P.axes([0,0.2,0.4,1.2,2.0],[],"valores de β₁ (experiência)","",xfmt=lambda v: nb(v,1),grid=False)]
b.append(ciline(P,74,0.4,2.0,1.2,"IC 95% = [0,4; 2,0]: centro 1,2, margem 0,8, EP 0,4"))
b.append(f'<line class="obs" x1="{f(P.X(0.2))}" y1="40" x2="{f(P.X(0.2))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(0.2)+6)}" y="108">teoria: 0,2 (fora → rejeita)</text>')
save("sala3", svg(560,160,'\n'.join(b),"Intervalo de confiança do Exercício 3 e o valor teórico 0,2"))

P=Plot(560,160, 30,540,20,122, -1.8,0.2,0,1)
b=[P.axes([-1.5,-0.9,-0.3,-0.2,0],[],"valores de β₁ (preço)","",xfmt=lambda v: nb(v,1),grid=False)]
b.append(ciline(P,74,-1.5,-0.3,-0.9,"não rejeitados: −0,9 ± 2(0,3) = [−1,5; −0,3]"))
b.append(f'<line class="obs" x1="{f(P.X(-0.2))}" y1="40" x2="{f(P.X(-0.2))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(-0.2)-6)}" y="108" text-anchor="end">teoria: −0,2 (fora → rejeita)</text>')
save("sala4", svg(560,160,'\n'.join(b),"Conjunto de valores não rejeitados do Exercício 4 e o valor teórico"))

# ---------- Ex. 5: reta estimada e extrapolação ----------
P=Plot(560,280, 50,540,20,230, -0.5,5,0,9)
b=[P.axes([0,1,2,3,4],[0,3,4,5,6,7],"X","Ŷ")]
b.append(f'<rect class="bandf" x="{f(P.X(0))}" y="{f(P.T)}" width="{f(P.X(3)-P.X(0))}" height="{f(P.B-P.T)}"/>')
b.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(3))}" x2="{f(P.X(3))}" y2="{f(P.Y(6))}"/>')
b.append(f'<line class="res" x1="{f(P.X(3))}" y1="{f(P.Y(6))}" x2="{f(P.X(4.6))}" y2="{f(P.Y(7.6))}"/>')
for x in (1,4): b.append(f'<circle class="fitpt" cx="{f(P.X(x))}" cy="{f(P.Y(3+x))}" r="5"/>')
b.append(f'<rect class="meanpt" x="{f(P.X(2)-6)}" y="{f(P.Y(5)-6)}" width="12" height="12" transform="rotate(45 {f(P.X(2))} {f(P.Y(5))})"/>')
b.append(f'<text class="an" x="{f(P.X(2)+12)}" y="{f(P.Y(5)+18)}">(x̄, ȳ) = (2; 5)</text>')
b.append(f'<text class="an fitc" x="{f(P.X(0.15))}" y="{f(P.Y(8.3))}">faixa observada: X de 0 a 3</text>')
b.append(f'<text class="an resc" x="{f(P.X(3.3))}" y="{f(P.Y(8.3))}">X = 4: extrapolação</text>')
b.append(f'<text class="an" x="{f(P.X(1)+8)}" y="{f(P.Y(4)+18)}">Ŷ(1) = 4</text>')
b.append(f'<text class="an" x="{f(P.X(4)+8)}" y="{f(P.Y(7)+18)}">Ŷ(4) = 7</text>')
save("sala5", svg(560,280,'\n'.join(b),"Reta estimada Y chapéu igual a 3 mais X, com a faixa observada e a extrapolação em X igual a 4"))
print("v5 figs ok")

# ======================= v7: Os betas, visualmente =======================
def arrow(x1,y1,x2,y2,cls="arw",hcls="arwh",h=9):
    a=math.atan2(y2-y1,x2-x1); bx=x2-h*math.cos(a); by=y2-h*math.sin(a)
    p1=(bx+h*0.45*math.sin(a), by-h*0.45*math.cos(a)); p2=(bx-h*0.45*math.sin(a), by+h*0.45*math.cos(a))
    return (f'<line class="{cls}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(bx)}" y2="{f(by)}"/>'
            f'<polygon class="{hcls}" points="{f(x2)},{f(y2)} {f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])}"/>')
def ols(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    b1=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs); return my-b1*mx,b1

# ---------- anatomia da equação ----------
cols=[(68,"y","nb","",["y: o que queremos","explicar","(ex.: salário-hora)"]),
      (204,"β₀","nr","resc",["β₀: intercepto","(coeficiente linear)","valor de y se x = 0"]),
      (340,"β₁","nm","fitc",["β₁: inclinação","(coeficiente angular)","Δy médio se x sobe 1"]),
      (476,"x","nb","",["x: variável","explicativa","(ex.: anos de estudo)"]),
      (612,"u","ng","posc",["u: erro","tudo o mais","que afeta y"])]
b=[]
b.append(f'<path class="brk" d="M164 44 V36 H516 V44"/><text class="an" x="340" y="28" text-anchor="middle">a reta (parte explicada por x): E(y | x) = β₀ + β₁x</text>')
b.append(f'<path class="brk" d="M572 44 V36 H652 V44"/><text class="an" x="612" y="28" text-anchor="middle">o que a reta não vê</text>')
for cx,t,box,tc,lab in cols:
    b.append(f'<rect class="{box}" x="{cx-40}" y="52" width="80" height="54" rx="10"/>')
    b.append(f'<text class="big {tc}" x="{cx}" y="90" text-anchor="middle">{t}</text>')
    for i,l in enumerate(lab): b.append(f'<text class="an sm" x="{cx}" y="{128+i*16}" text-anchor="middle">{l}</text>')
for cx,t in [(136,"="),(272,"+"),(408,"·"),(544,"+")]:
    b.append(f'<text class="big" x="{cx}" y="90" text-anchor="middle">{t}</text>')
save("b_anatomia", svg(680,184,'\n'.join(b),"Anatomia da equação y igual a beta zero mais beta um vezes x mais u, com o significado de cada parte"))

# ---------- β verdadeiro × β̂ de várias amostras ----------
P=Plot(560,300, 50,540,24,250, 0,10,0,12)
b=[P.axes([0,2,4,6,8,10],[0,2,4,6,8,10,12],"x","y")]
random.seed(11); est=[]
for k in range(3):
    xs=[random.uniform(0.5,9.5) for _ in range(12)]; ys=[2+0.8*x+random.gauss(0,1.6) for x in xs]
    b0,b1=ols(xs,ys); est.append((b0,b1,xs,ys))
for b0,b1,_,_ in est:
    b.append(f'<line class="samp" x1="{f(P.X(0))}" y1="{f(P.Y(b0))}" x2="{f(P.X(10))}" y2="{f(P.Y(b0+10*b1))}"/>')
for x,y in zip(est[0][2],est[0][3]): b.append(f'<circle class="pt sm" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="3"/>')
b.append(f'<line class="truel" x1="{f(P.X(0))}" y1="{f(P.Y(2))}" x2="{f(P.X(10))}" y2="{f(P.Y(10))}"/>')
b.append(f'<text class="an" x="{f(P.X(9.9))}" y="{f(P.Y(3.4))}" text-anchor="end">tracejada: reta verdadeira, β₁ = 0,8 (fixa)</text>')
b.append(f'<text class="an fitc" x="{f(P.X(9.9))}" y="{f(P.Y(2.3))}" text-anchor="end">azuis: retas de 3 amostras diferentes</text>')
_bt='; '.join(f'{e[1]:.2f}'.replace('.',',') for e in est)
b.append(f'<text class="an fitc" x="{f(P.X(9.9))}" y="{f(P.Y(1.2))}" text-anchor="end">β̂₁ = {_bt}</text>')
save("b_popamostra", svg(560,300,'\n'.join(b),"Reta verdadeira fixa e três retas estimadas em amostras diferentes"))
BETA_EST=[nb(e[1],2) for e in est]

# ---------- β₀: onde a reta corta o eixo ----------
P=Plot(560,280, 50,540,24,236, 0,10,0,11)
b=[P.axes([0,2,4,6,8,10],[0,2,4,6,8,10],"x","y")]
b.append(f'<line class="samp" x1="{f(P.X(0))}" y1="{f(P.Y(4.5))}" x2="{f(P.X(10))}" y2="{f(P.Y(10.5))}"/>')
b.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(2))}" x2="{f(P.X(10))}" y2="{f(P.Y(8))}"/>')
b.append(f'<line class="brk" x1="{f(P.X(0)+10)}" y1="{f(P.Y(0))}" x2="{f(P.X(0)+10)}" y2="{f(P.Y(2))}"/>')
b.append(f'<text class="an posc" x="{f(P.X(0)+16)}" y="{f(P.Y(1)+4)}">β₀ = 2</text>')
for y0 in (2,4.5): b.append(f'<circle class="icpt" cx="{f(P.X(0))}" cy="{f(P.Y(y0))}" r="5.5"/>')
b.append(f'<text class="an fitc" x="{f(P.X(6.2))}" y="{f(P.Y(5.2))}">y = 2 + 0,6x</text>')
b.append(f'<text class="an" x="{f(P.X(4.2))}" y="{f(P.Y(9.6))}">y = 4,5 + 0,6x: mesma inclinação, β₀ maior</text>')
b.append(f'<text class="an resc" x="{f(P.X(2.2))}" y="{f(P.Y(0.8))}">β₀ é a altura onde a reta cruza x = 0</text>')
save("b_beta0", svg(560,280,'\n'.join(b),"Intercepto como a altura em que a reta cruza o eixo vertical; mudar o intercepto desloca a reta sem girar"))

# ---------- β₁: a escada ----------
P=Plot(560,300, 58,540,20,250, 7,17,6,22)
b=[P.axes([8,10,12,14,16],[6,10,14,18,22],"Anos de estudo (x)","Salário-hora ajustado, R$")]
b.append(f'<line class="fit" x1="{f(P.X(7.5))}" y1="{f(P.Y(0.6+1.15*7.5))}" x2="{f(P.X(16.5))}" y2="{f(P.Y(0.6+1.15*16.5))}"/>')
for x in (10,11,12,13):
    y=0.6+1.15*x
    b.append(f'<path class="tri" d="M{f(P.X(x))} {f(P.Y(y))} H{f(P.X(x+1))} V{f(P.Y(y+1.15))}"/>')
b.append(f'<text class="an posc" x="{f(P.X(10.5))}" y="{f(P.Y(0.6+11.5)+16)}" text-anchor="middle">+1 ano</text>')
b.append(f'<text class="an posc" x="{f(P.X(11)+6)}" y="{f(P.Y(0.6+1.15*10.5)+4)}">+R$ 1,15</text>')
b.append(f'<text class="an" x="{f(P.X(7.6))}" y="{f(P.Y(18.8))}">cada degrau: +1 em x ⇒ +β̂₁ em ŷ</text>')
b.append(f'<text class="an" x="{f(P.X(7.6))}" y="{f(P.Y(17.5))}">4 anos a mais ⇒ 4 × 1,15 = R$ 4,60</text>')
b.append(f'<text class="an fitc" x="{f(P.X(7.6))}" y="{f(P.Y(20.5))}">ŷ = 0,6 + 1,15x</text>')
save("b_beta1", svg(560,300,'\n'.join(b),"A inclinação como uma escada: cada ano a mais de estudo sobe o salário ajustado em 1,15"))

# ---------- sinais de β₁ ----------
def sgn(x0,slope,title):
    P=Plot(0,0, x0+14,x0+184,16,146, 0,10,0,10)
    o=[f'<line class="ax" x1="{P.L}" y1="{P.B}" x2="{P.R}" y2="{P.B}"/>',f'<line class="ax" x1="{P.L}" y1="{P.T}" x2="{P.L}" y2="{P.B}"/>']
    a=5-slope*5; random.seed(int(20+slope*10))
    for k in range(14):
        x=random.uniform(0.6,9.4); y=min(9.4,max(0.6,a+slope*x+random.gauss(0,0.9)))
        o.append(f'<circle class="pt sm" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="2.6"/>')
    cls="tg" if slope>0 else ("tgn" if slope<0 else "tg0")
    o.append(f'<line class="{cls}" x1="{f(P.X(0.3))}" y1="{f(P.Y(a+slope*0.3))}" x2="{f(P.X(9.7))}" y2="{f(P.Y(a+slope*9.7))}"/>')
    for i,l in enumerate(title): o.append(f'<text class="an sm" x="{f((P.L+P.R)/2)}" y="{166+i*15}" text-anchor="middle">{l}</text>')
    return '\n'.join(o)
save("b_sinais", svg(600,200, sgn(0,0.7,["β₁ > 0: x e y sobem juntos","(educação × salário)"])+sgn(200,0,["β₁ = 0: sem relação linear","(y não muda com x)"])+sgn(400,-0.7,["β₁ < 0: x sobe, y desce","(preço × quantidade)"]),"Três painéis: inclinação positiva, nula e negativa"))

# ---------- de onde vem β̂₁: áreas (x − x̄)(y − ȳ) ----------
P=Plot(560,330, 58,540,20,280, 6,18,8,22)
b=[P.axes([6,8,10,12,14,16,18],[8,10,12,14,16,18,20,22],"Anos de estudo (x)","Salário-hora, R$ (y)")]
xs=[8,10,12,14,16]; ys=[10,12,15,15,20]; mx,my=12,14.4
for x,y in zip(xs,ys):
    pr=(x-mx)*(y-my)
    if abs(x-mx)<1e-9: continue
    x1,x2=sorted([P.X(mx),P.X(x)]); y1,y2=sorted([P.Y(my),P.Y(y)])
    b.append(f'<rect class="{"pos" if pr>0 else "sqr"}" x="{f(x1)}" y="{f(y1)}" width="{f(x2-x1)}" height="{f(y2-y1)}"/>')
b.append(f'<line class="mean" x1="{f(P.X(mx))}" y1="{f(P.T)}" x2="{f(P.X(mx))}" y2="{f(P.B)}"/>')
b.append(f'<line class="mean" x1="{f(P.L)}" y1="{f(P.Y(my))}" x2="{f(P.R)}" y2="{f(P.Y(my))}"/>')
for x,y in zip(xs,ys): b.append(f'<circle class="pt" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="5"/>')
labs={8:("+17,6",-1),10:("+4,8",-1),12:("0",1),14:("+1,2",1),16:("+22,4",1)}
for x,y in zip(xs,ys):
    t,s=labs[x]
    b.append(f'<text class="an posc" x="{f(P.X(x)+(8 if s>0 else -8))}" y="{f(P.Y(y)-8)}" text-anchor="{"start" if s>0 else "end"}">{t}</text>')
b.append(f'<text class="an posc" x="{f(P.X(17.8))}" y="{f(P.Y(21.3))}" text-anchor="end">quadrante I: (+)·(+) = +</text>')
b.append(f'<text class="an posc" x="{f(P.X(6.3))}" y="{f(P.Y(8.6))}">quadrante III: (−)·(−) = +</text>')
b.append(f'<text class="an resc" x="{f(P.X(6.3))}" y="{f(P.Y(21.3))}">II: (−)·(+) = −</text>')
b.append(f'<text class="an resc" x="{f(P.X(17.8))}" y="{f(P.Y(8.6))}" text-anchor="end">IV: (+)·(−) = −</text>')
b.append(f'<text class="an" x="{f(P.X(12)+6)}" y="{f(P.T+12)}">x̄ = 12</text><text class="an" x="{f(P.R-4)}" y="{f(P.Y(my)-6)}" text-anchor="end">ȳ = 14,4</text>')
save("b_quadrantes", svg(560,330,'\n'.join(b),"Retângulos entre o ponto das médias e cada observação; a soma das áreas com sinal é o numerador de beta um chapéu"))

# ---------- β̂₀ a partir do ponto das médias ----------
P=Plot(560,300, 50,540,20,250, 0,17,0,22)
b=[P.axes([0,4,8,12,16],[0,4,8,12,16,20],"Anos de estudo (x)","Salário-hora ajustado, R$")]
b.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(0.6))}" x2="{f(P.X(17))}" y2="{f(P.Y(0.6+1.15*17))}"/>')
b.append(f'<path class="tri" d="M{f(P.X(12))} {f(P.Y(14.4))} H{f(P.X(0))} V{f(P.Y(0.6))}"/>')
b.append(f'<rect class="meanpt" x="{f(P.X(12)-6)}" y="{f(P.Y(14.4)-6)}" width="12" height="12" transform="rotate(45 {f(P.X(12))} {f(P.Y(14.4))})"/>')
b.append(f'<circle class="icpt" cx="{f(P.X(0))}" cy="{f(P.Y(0.6))}" r="5.5"/>')
b.append(f'<text class="an" x="{f(P.X(12.4))}" y="{f(P.Y(12.3))}">1. comece em (x̄, ȳ)</text><text class="an" x="{f(P.X(12.4))}" y="{f(P.Y(10.9))}">= (12; 14,4)</text>')
b.append(f'<text class="an posc" x="{f(P.X(6))}" y="{f(P.Y(14.4)-8)}" text-anchor="middle">2. volte x̄ = 12 anos até x = 0</text>')
b.append(f'<text class="an posc" x="{f(P.X(0)+10)}" y="{f(P.Y(9.2))}">3. desça β̂₁·x̄</text><text class="an posc" x="{f(P.X(0)+10)}" y="{f(P.Y(7.8))}">= 1,15 × 12 = 13,8</text>')
b.append(f'<text class="an resc" x="{f(P.X(2.0))}" y="{f(P.Y(1.1))}">4. chegou em β̂₀ = 14,4 − 13,8 = 0,6</text>')
save("b_pivo", svg(560,300,'\n'.join(b),"Como achar beta zero chapéu: partir do ponto das médias, voltar até x igual a zero e descer beta um vezes x barra"))

# ---------- tradutor das formas funcionais ----------
rows=[("Nível–nível","y = β₀ + β₁x","+1 unidade em x","+β₁ unidades em y","área +1 m² ⇒ aluguel +R$ 24 (β̂₁ = 24)"),
      ("Log–nível","ln y = β₀ + β₁x","+1 unidade em x","≈ +100·β₁ % em y","estudo +1 ano ⇒ salário ≈ +8% (β̂₁ = 0,080)"),
      ("Nível–log","y = β₀ + β₁ ln x","+1% em x","≈ +β₁/100 unidades em y","β̂₁ = 50: x +1% ⇒ y +0,5 unidade"),
      ("Log–log","ln y = β₀ + β₁ ln x","+1% em x","≈ +β₁ % em y (elasticidade)","β̂₁ = 1,5: x +10% ⇒ y ≈ +15%")]
b=[]
for i,(nm,eq,cx,cy,ex) in enumerate(rows):
    y0=8+i*66
    b.append(f'<text class="an" x="0" y="{y0+20}" font-weight="700">{nm}</text><text class="an sm" x="0" y="{y0+37}">{eq}</text>')
    b.append(f'<rect class="nb" x="150" y="{y0+4}" width="170" height="38" rx="8"/><text class="an" x="235" y="{y0+28}" text-anchor="middle">{cx}</text>')
    b.append(arrow(326,y0+23,382,y0+23))
    b.append(f'<rect class="nm" x="388" y="{y0+4}" width="252" height="38" rx="8"/><text class="an fitc" x="514" y="{y0+28}" text-anchor="middle">{cy}</text>')
    b.append(f'<text class="an sm cBt" x="150" y="{y0+58}">exemplo: {ex}</text>')
save("b_tradutor", svg(640,272,'\n'.join(b),"Tradutor dos betas nas quatro formas funcionais: o que muda em x e o que muda em y"))

# ---------- dummy: diferença de médias ----------
P=Plot(560,300, 58,540,20,240, 0,4.3,6,16)
b=[P.axes([],[6,8,10,12,14,16],"","Salário-hora, R$",grid=True)]
for x,t in [(1,"D = 0: não sindicalizados"),(3,"D = 1: sindicalizados")]:
    b.append(f'<text class="tk" x="{f(P.X(x))}" y="{f(P.B+18)}" text-anchor="middle">{t}</text>')
g0=[8,9,10,9,9]; g1=[13,14,12,14,12]
def jit(v):
    seen={}; out=[]
    for y in v:
        k=seen.get(y,0); seen[y]=k+1; out.append((k-(v.count(y)-1)/2)*0.13)
    return out
for grp,xc,cls in [(g0,1,"pt"),(g1,3,"ptB")]:
    for y,j in zip(grp,jit(grp)): b.append(f'<circle class="{cls}" cx="{f(P.X(xc+j))}" cy="{f(P.Y(y))}" r="5"/>')
b.append(f'<line class="fit" x1="{f(P.X(1))}" y1="{f(P.Y(9))}" x2="{f(P.X(3))}" y2="{f(P.Y(13))}"/>')
b.append(f'<line class="mean" x1="{f(P.X(1))}" y1="{f(P.Y(9))}" x2="{f(P.X(3.45))}" y2="{f(P.Y(9))}"/>')
for x,y in [(1,9),(3,13)]:
    b.append(f'<rect class="meanpt" x="{f(P.X(x)-6)}" y="{f(P.Y(y)-6)}" width="12" height="12" transform="rotate(45 {f(P.X(x))} {f(P.Y(y))})"/>')
b.append(f'<line class="brk" x1="{f(P.X(3.45))}" y1="{f(P.Y(9))}" x2="{f(P.X(3.45))}" y2="{f(P.Y(13))}"/>')
b.append(f'<text class="an posc" x="{f(P.X(3.45)+8)}" y="{f(P.Y(11.4))}">β̂₁ = 13 − 9</text><text class="an posc" x="{f(P.X(3.45)+8)}" y="{f(P.Y(10.6))}">= 4</text>')
b.append(f'<text class="an resc" x="{f(P.X(1))}" y="{f(P.Y(7.1))}" text-anchor="middle">β̂₀ = 9 (média do grupo base)</text>')
b.append(f'<text class="an" x="{f(P.X(3))}" y="{f(P.Y(15.1))}" text-anchor="middle">média do grupo D = 1: β̂₀ + β̂₁ = 13</text>')
save("b_dummy", svg(560,300,'\n'.join(b),"Regressão numa dummy: beta zero é a média do grupo base e beta um é a diferença de médias"))

# ---------- dummy sozinha × com interação ----------
def ipanel(x0,title,b0,b1,g,gs):
    P=Plot(0,0, x0+16,x0+286,16,170, 0,10,0,12)
    o=[f'<line class="ax" x1="{P.L}" y1="{P.B}" x2="{P.R}" y2="{P.B}"/>',f'<line class="ax" x1="{P.L}" y1="{P.T}" x2="{P.L}" y2="{P.B}"/>']
    o.append(f'<line class="fit" x1="{f(P.X(0))}" y1="{f(P.Y(b0))}" x2="{f(P.X(10))}" y2="{f(P.Y(b0+10*b1))}"/>')
    o.append(f'<line class="tgn" x1="{f(P.X(0))}" y1="{f(P.Y(b0+g))}" x2="{f(P.X(10))}" y2="{f(P.Y(b0+g+10*(b1+gs)))}"/>')
    for xx in (2,8):
        o.append(f'<line class="brk" x1="{f(P.X(xx))}" y1="{f(P.Y(b0+b1*xx))}" x2="{f(P.X(xx))}" y2="{f(P.Y(b0+g+(b1+gs)*xx))}"/>')
    o.append(f'<text class="an sm fitc" x="{f(P.X(10))}" y="{f(P.Y(b0+b1*5)+22)}" text-anchor="end">grupo base (D = 0)</text>')
    o.append(f'<text class="an sm resc" x="{f(P.X(10))}" y="{f(P.Y(b0+g+(b1+gs)*10)-8)}" text-anchor="end">grupo D = 1</text>')
    for i,l in enumerate(title): o.append(f'<text class="an sm" x="{f((P.L+P.R)/2)}" y="{190+i*15}" text-anchor="middle">{l}</text>')
    return '\n'.join(o)
save("b_interacao", svg(620,226, ipanel(0,["Só a dummy: retas paralelas","diferença constante = β₂"],2,0.5,1.5,0)+ipanel(320,["Dummy + interação D·x: inclinações diferentes","diferença = β₂ + β₃·x (cresce com x)"],2,0.5,1,0.3),"Dummy sozinha desloca a reta; com interação, a inclinação também muda"))

# ---------- regressão múltipla: β₁ com o resto constante ----------
P=Plot(560,320, 58,540,20,270, 7,17,8,36)
b=[P.axes([8,10,12,14,16],[8,12,16,20,24,28,32,36],"Anos de estudo (educ)","Salário-hora, R$")]
E=[8,10,12,12,14,16]; H=[1,2,4,3,6,8]; S=[12,15,23,20,29,33]
b.append(f'<line class="cC" x1="{f(P.X(7.5))}" y1="{f(P.Y(-11.6+2.8*7.5))}" x2="{f(P.X(16.5))}" y2="{f(P.Y(-11.6+2.8*16.5))}"/>')
for hb in (2,6):
    b.append(f'<line class="samp" x1="{f(P.X(7.5))}" y1="{f(P.Y(2+2*hb+7.5))}" x2="{f(P.X(16.5))}" y2="{f(P.Y(2+2*hb+16.5))}"/>')
    b.append(f'<text class="an sm fitc" x="{f(P.X(16.6))}" y="{f(P.Y(2+2*hb+16.5)+4)}">hab = {hb}</text>')
for e,h,s in zip(E,H,S):
    b.append(f'<circle class="pt" cx="{f(P.X(e))}" cy="{f(P.Y(s))}" r="5"/>')
    side={(8,12):"L",(10,15):"R",(12,23):"L",(12,20):"R",(14,29):"L",(16,33):"B"}[(e,s)]
    if side=="L": b.append(f'<text class="an sm" x="{f(P.X(e)-9)}" y="{f(P.Y(s)+4)}" text-anchor="end">h={h}</text>')
    elif side=="R": b.append(f'<text class="an sm" x="{f(P.X(e)+9)}" y="{f(P.Y(s)+4)}">h={h}</text>')
    else: b.append(f'<text class="an sm" x="{f(P.X(e)+6)}" y="{f(P.Y(s)+18)}">h={h}</text>')
b.append(f'<text class="an resc" x="{f(P.X(16.6))}" y="{f(P.Y(13.6))}" text-anchor="end">vermelha: simples, inclinação 2,8</text>')
b.append(f'<text class="an resc" x="{f(P.X(16.6))}" y="{f(P.Y(11.9))}" text-anchor="end">(educação + habilidade juntas)</text>')
b.append(f'<text class="an fitc" x="{f(P.X(16.6))}" y="{f(P.Y(9.6))}" text-anchor="end">azuis: hab fixa, inclinação β̂₁ = 1</text>')
save("b_multipla", svg(600,320,'\n'.join(b),"Na regressão múltipla, beta um é a inclinação com habilidade fixa; na simples, a inclinação mistura educação e habilidade"))

# ---------- diagrama de caminhos (viés de variável omitida) ----------
b=[]
for cx,cy,t,box in [(90,150,"educ","nb"),(510,150,"salário","nb"),(300,50,"hab","ng")]:
    b.append(f'<rect class="{box}" x="{cx-58}" y="{cy-22}" width="116" height="44" rx="10"/><text class="an" x="{cx}" y="{cy+5}" text-anchor="middle" font-weight="700">{t}</text>')
b.append(arrow(150,150,450,150))
b.append(arrow(140,130,242,68))
b.append(arrow(358,68,460,130))
b.append(f'<text class="an fitc" x="300" y="170" text-anchor="middle">β₁ = 1 (efeito direto, com hab fixa)</text>')
b.append(f'<text class="an" x="170" y="92" text-anchor="end">δ₁ = 0,9</text>')
b.append(f'<text class="an" x="428" y="92">β₂ = 2</text>')
b.append(f'<text class="an resc" x="300" y="206" text-anchor="middle">a regressão simples mede os dois caminhos juntos: 1 + 2 × 0,9 = 2,8</text>')
save("b_caminhos", svg(600,218,'\n'.join(b),"Diagrama de caminhos: efeito direto da educação e caminho indireto pela habilidade"))

# ---------- régua de erros-padrão: t e IC ----------
P=Plot(600,178, 30,580,20,120, -0.15,1.85,0,1)
b=[P.axes([0,0.55,1.15,1.75],[],"valores de β₁","",xfmt=lambda v: nb(v,2),grid=False)]
ep=0.189
for k in range(0,7):
    x=k*ep
    b.append(f'<line class="mean" x1="{f(P.X(x))}" y1="30" x2="{f(P.X(x))}" y2="{f(P.B)}"/>')
    b.append(f'<text class="tk" x="{f(P.X(x))}" y="26" text-anchor="middle">{k} EP</text>')
b.append(ciline(P,86,0.549,1.751,1.15,"IC 95%: 1,15 ± 3,182 × 0,189 = [0,55; 1,75]"))
b.append(f'<line class="obs" x1="{f(P.X(0))}" y1="34" x2="{f(P.X(0))}" y2="{f(P.B)}"/>')
b.append(f'<text class="an resc" x="{f(P.X(0)+6)}" y="112">H₀: β₁ = 0</text>')
b.append(f'<text class="an fitc" x="{f(P.R)}" y="112" text-anchor="end">β̂₁ = 1,15 está a t = 1,15 / 0,189 ≈ 6,08 EPs do zero</text>')
save("b_regua", svg(600,178,'\n'.join(b),"Régua de erros-padrão: a estimativa está a cerca de seis erros-padrão do zero e o intervalo não contém o zero"))
print("v7 figs ok", BETA_EST)

# ---------- SQT = SQE + SQR: desvios de cada ponto ----------
P=Plot(560,330, 58,540,20,280, 6,18,8,22)
b=[P.axes([6,8,10,12,14,16,18],[8,10,12,14,16,18,20,22],"Anos de estudo (x)","Salário-hora, R$ (y)")]
xs=[8,10,12,14,16]; ys=[10,12,15,15,20]; my=14.4
b.append(f'<line class="mean" x1="{f(P.L)}" y1="{f(P.Y(my))}" x2="{f(P.R)}" y2="{f(P.Y(my))}"/>')
b.append(f'<line class="fit" x1="{f(P.X(7))}" y1="{f(P.Y(0.6+1.15*7))}" x2="{f(P.X(17))}" y2="{f(P.Y(0.6+1.15*17))}"/>')
for x,y in zip(xs,ys):
    yh=0.6+1.15*x
    b.append(f'<line class="tot" x1="{f(P.X(x)-9)}" y1="{f(P.Y(my))}" x2="{f(P.X(x)-9)}" y2="{f(P.Y(y))}"/>')
    b.append(f'<line class="expl" x1="{f(P.X(x))}" y1="{f(P.Y(my))}" x2="{f(P.X(x))}" y2="{f(P.Y(yh))}"/>')
    b.append(f'<line class="res" x1="{f(P.X(x)+9)}" y1="{f(P.Y(yh))}" x2="{f(P.X(x)+9)}" y2="{f(P.Y(y))}"/>')
for x,y in zip(xs,ys): b.append(f'<circle class="pt" cx="{f(P.X(x))}" cy="{f(P.Y(y))}" r="4.5"/>')
b.append(f'<text class="an" x="{f(P.X(17.9))}" y="{f(P.Y(9.9))}" text-anchor="end">em x = 16: total 5,6 =</text><text class="an" x="{f(P.X(17.9))}" y="{f(P.Y(8.8))}" text-anchor="end">explicado 4,6 + resíduo 1,0</text>')
b.append(f'<text class="an" x="{f(P.R-4)}" y="{f(P.Y(my)+16)}" text-anchor="end">ȳ = 14,4</text>')
lx=P.X(6.3); ly=P.Y(21.2)
for i,(cls,t) in enumerate([("tot","preta: total, y − ȳ"),("expl","azul: explicado, ŷ − ȳ"),("res","vermelha: resíduo, y − ŷ")]):
    yy=ly+i*18
    b.append(f'<line class="{cls}" x1="{f(lx)}" y1="{f(yy-4)}" x2="{f(lx+22)}" y2="{f(yy-4)}"/><text class="an sm" x="{f(lx+28)}" y="{f(yy)}">{t}</text>')
save("sq_desvios", svg(560,330,'\n'.join(b),"Para cada ponto, o desvio total em relação à média se divide em parte explicada pela reta e resíduo"))

# ---------- barra SQT = SQE + SQR ----------
b=[]
x0,x1=20,540; W=x1-x0; sqt,sqe,sqr=57.2,52.9,4.3
xe=x0+W*sqe/sqt
b.append(f'<text class="an" x="{x0}" y="22" font-weight="700">SQT = 57,2: toda a variação de y em torno de ȳ</text>')
b.append(f'<rect class="barA" x="{x0}" y="34" width="{f(xe-x0)}" height="44" rx="4"/>')
b.append(f'<rect class="sqr" x="{f(xe)}" y="34" width="{f(x1-xe)}" height="44" rx="4"/>')
b.append(f'<text class="an" x="{f((x0+xe)/2)}" y="61" text-anchor="middle" font-weight="700">SQE = 52,9 (explicada pela reta)</text>')
b.append(f'<text class="an resc" x="{x1}" y="98" text-anchor="end">SQR = 4,3 (resíduos) ↑</text>')
b.append(f'<text class="an fitc" x="{x0}" y="124">R² = SQE / SQT = 52,9 / 57,2 = 0,925: 92,5% da barra é azul</text>')
b.append(f'<text class="an resc" x="{x0}" y="144">1 − R² = SQR / SQT = 4,3 / 57,2 = 0,075: o que a reta não explica</text>')
save("sq_barra", svg(560,156,'\n'.join(b),"Barra da SQT dividida em SQE e SQR, com o R-quadrado como a fração explicada"))
print("sq figs ok")
