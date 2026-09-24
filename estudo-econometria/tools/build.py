import os, re, glob
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parts=sorted(glob.glob(base+"/parts/*.html"))
html="\n".join(open(p).read() for p in parts)
def fig(m):
    name=m.group(1)
    return open(f"{base}/parts/figs/{name}.svg").read()
html=re.sub(r"FIG:([a-z0-9_]+)", fig, html)
out=base+"/guia_econometria_P1.html"
open(out,"w").write(html)
print("parts:", [os.path.basename(p) for p in parts]); print("bytes:", len(html.encode()))
