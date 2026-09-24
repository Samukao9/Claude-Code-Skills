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

# ---------- H: poder (Lista 02 Q8) ----------
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
