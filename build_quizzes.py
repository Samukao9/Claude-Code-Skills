#!/usr/bin/env python3
"""
Build QUIZZES_3_e_4_Samuel.xlsx — Solver-ready spreadsheet.
Decision variables are filled with PuLP optimal values.
All formulas are real Excel formulas so Solver (LP Simplex) works directly.
"""

import pulp
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter
import os, shutil

# ============================================================
# STYLES
# ============================================================
F = Font(name='Arial', size=10)
FB = Font(name='Arial', size=10, bold=True)
FT = Font(name='Arial', size=14, bold=True)
FS = Font(name='Arial', size=12, bold=True)
FBLUE = Font(name='Arial', size=10, color='0000FF')
FBLUEB = Font(name='Arial', size=10, color='0000FF', bold=True)
FWHITEB = Font(name='Arial', size=10, color='FFFFFF', bold=True)
FRED = Font(name='Arial', size=10, color='FF0000', bold=True)
FYELLOW = PatternFill('solid', fgColor='FFFF00')
FGRAY = PatternFill('solid', fgColor='D9D9D9')
FDARK = PatternFill('solid', fgColor='4472C4')
FLTBLUE = PatternFill('solid', fgColor='D6E4F0')
FLTGREEN = PatternFill('solid', fgColor='E2EFDA')
FLTYELLOW = PatternFill('solid', fgColor='FFFFCC')
BB = Border(left=Side('medium',color='0000FF'), right=Side('medium',color='0000FF'),
            top=Side('medium',color='0000FF'), bottom=Side('medium',color='0000FF'))
BT = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
AC = Alignment(horizontal='center', vertical='center')
AL = Alignment(horizontal='left', vertical='center', wrap_text=True)
ALT = Alignment(horizontal='left', vertical='top', wrap_text=True)
MF = '$#,##0'
IF_ = '#,##0'

def cr(row, col):
    return f"{get_column_letter(col)}{row}"

def sc(ws, r, c, v, font=F, fill=None, border=None, align=None, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    if font: cell.font = font
    if fill: cell.fill = fill
    if border: cell.border = border
    if align: cell.alignment = align
    if fmt: cell.number_format = fmt
    return cell

def hdr(ws, r, c0, labels, fill=FGRAY, font=FB):
    for i, l in enumerate(labels):
        sc(ws, r, c0+i, l, font=font, fill=fill, border=BT, align=AC)

def stitle(ws, r, c, text, end=None):
    sc(ws, r, c, text, font=FWHITEB, fill=FDARK)
    if end:
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=end)
        for c2 in range(c, end+1):
            ws.cell(row=r, column=c2).fill = FDARK

# ============================================================
# QUIZ 3 — Solve with PuLP
# ============================================================
WH = ['NY', 'LA', 'Chicago', 'Atlanta']
REG = ['Região 1', 'Região 2', 'Região 3']
FC = {'NY':60000, 'LA':50000, 'Chicago':40000, 'Atlanta':35000}
DEM = {'Região 1':8000, 'Região 2':9000, 'Região 3':7000}
CAP = 15000
UC = {('NY','Região 1'):26,('NY','Região 2'):41,('NY','Região 3'):39,
      ('LA','Região 1'):59,('LA','Região 2'):27,('LA','Região 3'):27,
      ('Chicago','Região 1'):28,('Chicago','Região 2'):32,('Chicago','Região 3'):43,
      ('Atlanta','Região 1'):28,('Atlanta','Região 2'):40,('Atlanta','Região 3'):38}

m3 = pulp.LpProblem("Q3", pulp.LpMinimize)
y = {w: pulp.LpVariable(f"y_{w}", cat='Binary') for w in WH}
x = {(w,r): pulp.LpVariable(f"x_{w}_{r}", lowBound=0) for w in WH for r in REG}
m3 += pulp.lpSum(FC[w]*y[w] for w in WH) + pulp.lpSum(UC[w,r]*x[w,r] for w in WH for r in REG)
for r in REG: m3 += pulp.lpSum(x[w,r] for w in WH) >= DEM[r]
for w in WH: m3 += pulp.lpSum(x[w,r] for r in REG) <= CAP * y[w]
m3 += y['NY'] <= y['LA']
m3 += pulp.lpSum(y[w] for w in WH) <= 2
m3 += y['Atlanta'] + y['LA'] >= 1
m3.solve(pulp.PULP_CBC_CMD(msg=0))
print(f"Q3: {pulp.LpStatus[m3.status]}, Z* = {pulp.value(m3.objective)}")
q3y = {w: int(y[w].varValue) for w in WH}
q3x = {(w,r): x[w,r].varValue for w in WH for r in REG}
q3z = pulp.value(m3.objective)

# ============================================================
# QUIZ 4 — Solve with PuLP
# ============================================================
ARCS = [('Porto 1','Distrib. 1',100),('Porto 1','Revenda 3',300),('Porto 1','Distrib. 2',130),
        ('Porto 2','Distrib. 1',150),('Porto 2','Revenda 2',300),('Porto 2','Distrib. 2',120),
        ('Distrib. 1','Revenda 3',160),('Distrib. 1','Revenda 2',170),('Distrib. 1','Distrib. 2',280),
        ('Distrib. 2','Revenda 3',140),('Distrib. 2','Revenda 2',160),
        ('Revenda 3','Revenda 2',150)]
VMULT = {'Minivan':1.15, 'Esportivo':0.90}
SUP = {('Porto 1','Minivan'):325,('Porto 1','Esportivo'):450,
       ('Porto 2','Minivan'):430,('Porto 2','Esportivo'):300}
DEM4 = {('Revenda 3','Minivan'):477,('Revenda 3','Esportivo'):227,
        ('Revenda 2','Minivan'):278,('Revenda 2','Esportivo'):523}
ORIG = ['Porto 1','Porto 2']
INTER = ['Distrib. 1','Distrib. 2']
DEST = ['Revenda 3','Revenda 2']

def solve_q4(cap=None):
    prob = pulp.LpProblem("Q4", pulp.LpMinimize)
    fl = {}
    for (i,j,c) in ARCS:
        for v in VMULT:
            fl[i,j,v] = pulp.LpVariable(f"f_{i}_{j}_{v}", lowBound=0)
    prob += pulp.lpSum(c*VMULT[v]*fl[i,j,v] for (i,j,c) in ARCS for v in VMULT)
    for nd in INTER:
        for v in VMULT:
            prob += (pulp.lpSum(fl[i,j,v] for (i,j,c) in ARCS if j==nd) ==
                     pulp.lpSum(fl[i,j,v] for (i,j,c) in ARCS if i==nd))
    for p in ORIG:
        for v in VMULT:
            prob += pulp.lpSum(fl[p,j,v] for (i,j,c) in ARCS if i==p) <= SUP[p,v]
    for d in DEST:
        for v in VMULT:
            prob += (pulp.lpSum(fl[i,d,v] for (i,j,c) in ARCS if j==d) -
                     pulp.lpSum(fl[d,j,v] for (i,j,c) in ARCS if i==d) >= DEM4[d,v])
    if cap is not None:
        for (i,j,c) in ARCS:
            prob += pulp.lpSum(fl[i,j,v] for v in VMULT) <= cap
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return prob, fl

m4, fb = solve_q4()
q4z = pulp.value(m4.objective)
q4f = {}
for (i,j,c) in ARCS:
    for v in VMULT:
        val = fb[i,j,v].varValue or 0
        q4f[i,j,v] = val
print(f"Q4: {pulp.LpStatus[m4.status]}, Z* = {q4z}")

# Sensitivity
CAPS = list(range(500,1600,100))
SENS = {}
for cv in CAPS:
    ms, _ = solve_q4(cap=cv)
    SENS[cv] = pulp.value(ms.objective) if ms.status == 1 else None

# ============================================================
# BUILD EXCEL WORKBOOK
# ============================================================
wb = Workbook()

# ################################################################
# QUIZ 3 SHEET
# ################################################################
ws = wb.active
ws.title = "Quiz 3 - Armazéns"
for c in range(1,10): ws.column_dimensions[get_column_letter(c)].width = 20

R = 1
sc(ws, R, 1, "QUIZ 3 — Localização de Armazéns (Programação Linear Inteira Mista)", font=FT)
ws.merge_cells('A1:H1')

# === 1. DADOS ===
R = 3; stitle(ws, R, 1, "1. DADOS DO PROBLEMA", end=8)

R = 5; sc(ws, R, 1, "Custos Unitários de Produção + Transporte ($/unidade)", font=FB)
R = 6; hdr(ws, R, 1, ['Armazém','Região 1','Região 2','Região 3'])
UC_R0 = 7  # rows 7-10
for wi,w in enumerate(WH):
    rr = UC_R0+wi
    sc(ws, rr, 1, w, font=FBLUE, border=BT, align=AC)
    for ri,reg in enumerate(REG):
        sc(ws, rr, 2+ri, UC[w,reg], font=FBLUE, border=BT, align=AC, fmt=MF)

R = 12; sc(ws, R, 1, "Custos Fixos Semanais", font=FB)
R = 13; hdr(ws, R, 1, ['Armazém','Custo Fixo'])
FC_R0 = 14  # rows 14-17
for wi,w in enumerate(WH):
    rr = FC_R0+wi
    sc(ws, rr, 1, w, font=FBLUE, border=BT, align=AC)
    sc(ws, rr, 2, FC[w], font=FBLUE, border=BT, align=AC, fmt=MF)

R = 19; sc(ws, R, 1, "Demandas Semanais por Região", font=FB)
R = 20; hdr(ws, R, 1, ['Região','Demanda'])
DM_R0 = 21  # rows 21-23
for ri,reg in enumerate(REG):
    rr = DM_R0+ri
    sc(ws, rr, 1, reg, font=FBLUE, border=BT, align=AC)
    sc(ws, rr, 2, DEM[reg], font=FBLUE, border=BT, align=AC, fmt=IF_)

R = 25; sc(ws, R, 1, "Capacidade máx. por armazém:", font=FB)
sc(ws, R, 2, CAP, font=FBLUE, fmt=IF_)

# === 2. VARIÁVEIS DE DECISÃO ===
R = 27; stitle(ws, R, 1, "2. VARIÁVEIS DE DECISÃO (células que o Solver altera)", end=8)

# y_i binaries
R = 29; sc(ws, R, 1, "y_i — Abrir armazém? (0 ou 1) → VARIÁVEIS BINÁRIAS", font=FB)
R = 30; hdr(ws, R, 1, ['y_NY','y_LA','y_Chicago','y_Atlanta'])
YR = 31  # <<< Y variables row
for wi,w in enumerate(WH):
    sc(ws, YR, 1+wi, q3y[w], font=FBLUEB, border=BB, align=AC, fmt='0')

# x_ij continuous
R = 33; sc(ws, R, 1, "x_ij — Unidades enviadas de armazém i → região j → VARIÁVEIS CONTÍNUAS", font=FB)
R = 34; hdr(ws, R, 1, ['x_ij','Região 1','Região 2','Região 3','Total Enviado (LHS cap.)'])
XR0 = 35  # rows 35-38
for wi,w in enumerate(WH):
    rr = XR0+wi
    sc(ws, rr, 1, w, font=FB, border=BT, align=AC, fill=FGRAY)
    for ri in range(3):
        sc(ws, rr, 2+ri, q3x[w,REG[ri]], font=FBLUEB, border=BB, align=AC, fmt=IF_)
    # col E = SUM(B:D) for this row → LHS of capacity constraint
    sc(ws, rr, 5, f"=SUM({cr(rr,2)}:{cr(rr,4)})", font=F, border=BT, align=AC, fmt=IF_)

# Total received per region row → LHS of demand constraints
R = 39; sc(ws, R, 1, "Total Recebido (LHS dem.)", font=FB, border=BT, align=AC, fill=FGRAY)
for ri in range(3):
    sc(ws, R, 2+ri, f"=SUM({cr(XR0,2+ri)}:{cr(XR0+3,2+ri)})", font=F, border=BT, align=AC, fmt=IF_)

# === 3. FUNÇÃO OBJETIVO ===
R = 41; stitle(ws, R, 1, "3. FUNÇÃO OBJETIVO — Minimizar Custo Total", end=8)

R = 43; sc(ws, R, 1, "Custo Fixo:", font=FB)
# =B14*A31 + B15*B31 + B16*C31 + B17*D31
fc_f = "=" + "+".join([f"{cr(FC_R0+i,2)}*{cr(YR,1+i)}" for i in range(4)])
sc(ws, R, 2, fc_f, font=F, border=BT, fmt=MF)

R = 44; sc(ws, R, 1, "Custo Variável:", font=FB)
sc(ws, R, 2, f"=SUMPRODUCT({cr(UC_R0,2)}:{cr(UC_R0+3,4)},{cr(XR0,2)}:{cr(XR0+3,4)})", font=F, border=BT, fmt=MF)

R = 45; sc(ws, R, 1, "▶ CUSTO TOTAL (Célula Objetivo):", font=FS)
FO3 = cr(45,2)
sc(ws, 45, 2, f"={cr(43,2)}+{cr(44,2)}", font=Font(name='Arial',size=12,bold=True,color='000000'),
   fill=FYELLOW, border=BB, fmt=MF)

# === 4. RESTRIÇÕES (com LHS fórmula | sinal | RHS) ===
R = 47; stitle(ws, R, 1, "4. RESTRIÇÕES (LHS e RHS para o Solver)", end=8)
R = 49; hdr(ws, R, 1, ['Descrição','Célula LHS','Fórmula LHS','Sinal','Célula RHS','Valor RHS','Status'])

# Track constraint rows for Solver config
constr_rows = []

def add_constr(ws, row, desc, lhs_formula, sign, rhs_val_or_formula, is_rhs_formula=False):
    """Add a constraint row. Returns (lhs_cell, sign, rhs_cell) strings."""
    sc(ws, row, 1, desc, font=F, border=BT, align=AL)
    lhs_cell = cr(row, 3)
    rhs_cell = cr(row, 6)
    sc(ws, row, 2, lhs_cell, font=FBLUE, border=BT, align=AC)  # shows cell ref
    sc(ws, row, 3, lhs_formula, font=F, border=BT, align=AC, fmt=IF_)
    sc(ws, row, 4, sign, font=FB, border=BT, align=AC)
    sc(ws, row, 5, rhs_cell, font=FBLUE, border=BT, align=AC)
    if is_rhs_formula:
        sc(ws, row, 6, rhs_val_or_formula, font=F, border=BT, align=AC, fmt=IF_)
    else:
        sc(ws, row, 6, rhs_val_or_formula, font=FBLUE, border=BT, align=AC, fmt=IF_)
    # Status
    if sign == ">=":
        sc(ws, row, 7, f'=IF({lhs_cell}>={rhs_cell},"OK","VIOLA")', font=F, border=BT, align=AC)
    elif sign == "<=":
        sc(ws, row, 7, f'=IF({lhs_cell}<={rhs_cell},"OK","VIOLA")', font=F, border=BT, align=AC)
    else:
        sc(ws, row, 7, f'=IF({lhs_cell}={rhs_cell},"OK","VIOLA")', font=F, border=BT, align=AC)
    constr_rows.append((desc, lhs_cell, sign, rhs_cell))

rr = 50
# Demand constraints
for ri, reg in enumerate(REG):
    add_constr(ws, rr, f"Demanda {reg}: Σx_ij ≥ {DEM[reg]}",
               f"={cr(39,2+ri)}", ">=", DEM[reg])
    rr += 1

# Capacity constraints
for wi, w in enumerate(WH):
    add_constr(ws, rr, f"Capacidade {w}: Σx_{w}j ≤ 15000·y_{w}",
               f"={cr(XR0+wi,5)}", "<=", f"={cr(25,2)}*{cr(YR,1+wi)}", is_rhs_formula=True)
    rr += 1

# Logical constraints
add_constr(ws, rr, "NY→LA: y_NY ≤ y_LA", f"={cr(YR,1)}", "<=", f"={cr(YR,2)}", is_rhs_formula=True)
rr += 1
add_constr(ws, rr, "Máx 2 armazéns: Σy_i ≤ 2", f"=SUM({cr(YR,1)}:{cr(YR,4)})", "<=", 2)
rr += 1
add_constr(ws, rr, "ATL ou LA: y_ATL + y_LA ≥ 1", f"={cr(YR,4)}+{cr(YR,2)}", ">=", 1)
rr += 1

# Binaries note
sc(ws, rr, 1, "y_i ∈ {0,1} — Binário", font=FB, border=BT)
sc(ws, rr, 2, f"{cr(YR,1)}:{cr(YR,4)}", font=FBLUE, border=BT, align=AC)
sc(ws, rr, 4, "bin", font=FB, border=BT, align=AC)
rr += 1

# Non-negativity
sc(ws, rr, 1, "x_ij ≥ 0 — Não-negatividade", font=FB, border=BT)
sc(ws, rr, 2, f"{cr(XR0,2)}:{cr(XR0+3,4)}", font=FBLUE, border=BT, align=AC)
sc(ws, rr, 4, ">=", font=FB, border=BT, align=AC)
sc(ws, rr, 6, 0, font=FBLUE, border=BT, align=AC)
CONSTR3_END = rr + 1

# === 5. CONFIGURAÇÃO DO SOLVER — PASSO A PASSO ===
R = CONSTR3_END + 1
stitle(ws, R, 1, "5. CONFIGURAÇÃO DO SOLVER — PASSO A PASSO", end=8)
R += 2

steps = [
    ("PASSO 1:", "Abra a aba 'Dados' → clique em 'Solver' (canto superior direito)"),
    ("PASSO 2:", f"Definir Objetivo: selecione a célula {FO3} (custo total, fundo amarelo)"),
    ("PASSO 3:", "Para: selecione 'Mín' (minimizar)"),
    ("PASSO 4:", f"Alterando Células Variáveis: {cr(YR,1)}:{cr(YR,4)},{cr(XR0,2)}:{cr(XR0+3,4)}"),
    ("PASSO 5:", "Sujeito às Restrições — clique 'Adicionar' para cada uma:"),
]
for si, (lbl, txt) in enumerate(steps):
    sc(ws, R+si, 1, lbl, font=FB, fill=FLTYELLOW)
    sc(ws, R+si, 2, txt, font=F)
    ws.merge_cells(start_row=R+si, start_column=2, end_row=R+si, end_column=8)

R += len(steps) + 1
sc(ws, R, 1, "Restrições a adicionar no Solver:", font=FB)
R += 1
hdr(ws, R, 1, ['#','Referência da Célula (LHS)','Operador','Restrição (RHS)','Descrição'])
R += 1

# Re-list all constraints in Solver format
solver_constrs = [
    (f"{cr(50,3)}", ">=", f"{cr(50,6)}", "Demanda Região 1"),
    (f"{cr(51,3)}", ">=", f"{cr(51,6)}", "Demanda Região 2"),
    (f"{cr(52,3)}", ">=", f"{cr(52,6)}", "Demanda Região 3"),
    (f"{cr(53,3)}", "<=", f"{cr(53,6)}", "Capacidade NY"),
    (f"{cr(54,3)}", "<=", f"{cr(54,6)}", "Capacidade LA"),
    (f"{cr(55,3)}", "<=", f"{cr(55,6)}", "Capacidade Chicago"),
    (f"{cr(56,3)}", "<=", f"{cr(56,6)}", "Capacidade Atlanta"),
    (f"{cr(57,3)}", "<=", f"{cr(57,6)}", "NY implica LA"),
    (f"{cr(58,3)}", "<=", f"{cr(58,6)}", "Máx 2 armazéns"),
    (f"{cr(59,3)}", ">=", f"{cr(59,6)}", "ATL ou LA"),
    (f"{cr(YR,1)}:{cr(YR,4)}", "bin", "—", "Variáveis binárias"),
    (f"{cr(XR0,2)}:{cr(XR0+3,4)}", ">=", "0", "Não-negatividade"),
]
for ci, (lhs, op, rhs, desc) in enumerate(solver_constrs):
    sc(ws, R+ci, 1, ci+1, font=F, border=BT, align=AC)
    sc(ws, R+ci, 2, lhs, font=FBLUEB, border=BT, align=AC)
    sc(ws, R+ci, 3, op, font=FB, border=BT, align=AC)
    sc(ws, R+ci, 4, rhs, font=FBLUEB, border=BT, align=AC)
    sc(ws, R+ci, 5, desc, font=F, border=BT, align=AL)
R += len(solver_constrs) + 1

sc(ws, R, 1, "PASSO 6:", font=FB, fill=FLTYELLOW)
sc(ws, R, 2, "Selecionar Método de Resolução: 'Simplex LP'", font=FB)
ws.merge_cells(start_row=R, start_column=2, end_row=R, end_column=8)
R += 1
sc(ws, R, 1, "PASSO 7:", font=FB, fill=FLTYELLOW)
sc(ws, R, 2, "Marcar 'Tornar Variáveis Irrestritas Não Negativas' ✓", font=F)
ws.merge_cells(start_row=R, start_column=2, end_row=R, end_column=8)
R += 1
sc(ws, R, 1, "PASSO 8:", font=FB, fill=FLTYELLOW)
sc(ws, R, 2, "Clicar 'Resolver' → 'Manter Solução do Solver' → OK", font=F)
ws.merge_cells(start_row=R, start_column=2, end_row=R, end_column=8)
R += 2

sc(ws, R, 1, "NOTA:", font=FRED)
sc(ws, R, 2, "O Excel usa Simplex LP com Branch & Bound interno para variáveis binárias (inteiras). "
             "Não é necessário selecionar outro método — o Simplex LP do Solver trata binárias automaticamente.", font=F)
ws.merge_cells(start_row=R, start_column=2, end_row=R+1, end_column=8)
ws.cell(row=R, column=2).alignment = ALT

# === 6. RESPOSTA POR EXTENSO ===
R += 3
stitle(ws, R, 1, "6. RESPOSTA POR EXTENSO", end=8)
R += 2

q3_open = [w for w in WH if q3y[w]==1]
lines = [f"SOLUÇÃO ÓTIMA — Custo Total Mínimo: ${q3z:,.0f}",
         "",
         f"Armazéns abertos: {', '.join(q3_open)}",
         f"Armazéns fechados: {', '.join(w for w in WH if q3y[w]==0)}",
         "",
         "Distribuição ótima (armazém → região → quantidade):"]
for w in WH:
    for reg in REG:
        v = q3x[w,reg]
        if v and v > 0.001:
            lines.append(f"  • {w} → {reg}: {v:,.0f} unidades (custo unit.: ${UC[w,reg]})")
lines.append("")
lines.append("Verificação das restrições lógicas:")
lines.append(f"  • NY aberto? {'Sim' if q3y['NY'] else 'Não'}, LA aberto? {'Sim' if q3y['LA'] else 'Não'} → NY→LA: OK")
lines.append(f"  • Total armazéns abertos: {sum(q3y.values())} ≤ 2 → OK")
lines.append(f"  • ATL ou LA aberto? y_ATL+y_LA = {q3y['Atlanta']+q3y['LA']} ≥ 1 → OK")

sc(ws, R, 1, "\n".join(lines), font=Font(name='Arial', size=11), align=ALT)
ws.merge_cells(start_row=R, start_column=1, end_row=R+14, end_column=8)
ws.cell(row=R, column=1).fill = FLTGREEN

# ################################################################
# QUIZ 4 SHEET
# ################################################################
ws4 = wb.create_sheet("Quiz 4 - Distribuição")
for c in range(1,13): ws4.column_dimensions[get_column_letter(c)].width = 18

R = 1
sc(ws4, R, 1, "QUIZ 4 — Distribuição de Veículos (PL - Fluxo em Rede)", font=FT)
ws4.merge_cells('A1:K1')

# === 1. DADOS ===
R = 3; stitle(ws4, R, 1, "1. DADOS DO PROBLEMA", end=11)

R = 5; sc(ws4, R, 1, "Arcos da Rede — Custos Padrão e Ajustados por Tipo de Veículo", font=FB)
R = 6; hdr(ws4, R, 1, ['#','De','Para','Custo Padrão ($)','Custo Minivan (×1.15)','Custo Esportivo (×0.90)'])
A_R0 = 7  # arc data rows 7-18
for ai,(fr,to,cost) in enumerate(ARCS):
    rr = A_R0+ai
    sc(ws4, rr, 1, ai+1, font=F, border=BT, align=AC)
    sc(ws4, rr, 2, fr, font=FBLUE, border=BT)
    sc(ws4, rr, 3, to, font=FBLUE, border=BT)
    sc(ws4, rr, 4, cost, font=FBLUE, border=BT, fmt=MF)
    sc(ws4, rr, 5, f"={cr(rr,4)}*1.15", font=F, border=BT, fmt='$#,##0.00')
    sc(ws4, rr, 6, f"={cr(rr,4)}*0.9", font=F, border=BT, fmt='$#,##0.00')
A_REND = A_R0 + len(ARCS) - 1  # 18

# Supply
R = A_REND + 2
sc(ws4, R, 1, "Oferta (Portos)", font=FB)
R += 1; hdr(ws4, R, 1, ['Porto','Minivan','Esportivo'])
S_R0 = R + 1
for pi,p in enumerate(ORIG):
    rr = S_R0+pi
    sc(ws4, rr, 1, p, font=FBLUE, border=BT)
    sc(ws4, rr, 2, SUP[p,'Minivan'], font=FBLUE, border=BT, fmt=IF_)
    sc(ws4, rr, 3, SUP[p,'Esportivo'], font=FBLUE, border=BT, fmt=IF_)

# Demand
R = S_R0 + 3
sc(ws4, R, 1, "Demanda (Revendas)", font=FB)
R += 1; hdr(ws4, R, 1, ['Revenda','Minivan','Esportivo'])
D4_R0 = R + 1
for di,d in enumerate(DEST):
    rr = D4_R0+di
    sc(ws4, rr, 1, d, font=FBLUE, border=BT)
    sc(ws4, rr, 2, DEM4[d,'Minivan'], font=FBLUE, border=BT, fmt=IF_)
    sc(ws4, rr, 3, DEM4[d,'Esportivo'], font=FBLUE, border=BT, fmt=IF_)

# === 2. VARIÁVEIS DE DECISÃO ===
R = D4_R0 + 4
stitle(ws4, R, 1, "2. VARIÁVEIS DE DECISÃO — Fluxo por Arco (células que o Solver altera)", end=11)
R += 2
sc(ws4, R, 1, "Arco / Tipo de Veículo → Quantidades de Fluxo (variáveis) e Custos (fórmulas)", font=FB)
R += 1
hdr(ws4, R, 1, ['#','De','Para','Fluxo Minivan','Fluxo Esportivo','Fluxo Total',
                  'Custo Minivan ($)','Custo Esportivo ($)','Custo Total Arco ($)'])
FH = R  # flow header row
F_R0 = R + 1  # flow data start
for ai,(fr,to,cost) in enumerate(ARCS):
    rr = F_R0+ai
    sc(ws4, rr, 1, ai+1, font=F, border=BT, align=AC)
    sc(ws4, rr, 2, fr, font=F, border=BT)
    sc(ws4, rr, 3, to, font=F, border=BT)
    # Decision variable cells — filled with PuLP solution
    sc(ws4, rr, 4, q4f.get((fr,to,'Minivan'),0), font=FBLUEB, border=BB, align=AC, fmt=IF_)
    sc(ws4, rr, 5, q4f.get((fr,to,'Esportivo'),0), font=FBLUEB, border=BB, align=AC, fmt=IF_)
    # Formulas
    sc(ws4, rr, 6, f"={cr(rr,4)}+{cr(rr,5)}", font=F, border=BT, align=AC, fmt=IF_)
    ac = cr(A_R0+ai, 4)  # arc std cost cell
    sc(ws4, rr, 7, f"={cr(rr,4)}*{ac}*1.15", font=F, border=BT, fmt=MF)
    sc(ws4, rr, 8, f"={cr(rr,5)}*{ac}*0.9", font=F, border=BT, fmt=MF)
    sc(ws4, rr, 9, f"={cr(rr,7)}+{cr(rr,8)}", font=F, border=BT, fmt=MF)
F_REND = F_R0 + len(ARCS) - 1  # last flow row

# === 3. FUNÇÃO OBJETIVO ===
R = F_REND + 2
stitle(ws4, R, 1, "3. FUNÇÃO OBJETIVO — Minimizar Custo Total de Transporte", end=11)
R += 2
sc(ws4, R, 1, "▶ CUSTO TOTAL (Célula Objetivo):", font=FS)
FO4 = cr(R, 2)
sc(ws4, R, 2, f"=SUM({cr(F_R0,9)}:{cr(F_REND,9)})", font=Font(name='Arial',size=12,bold=True),
   fill=FYELLOW, border=BB, fmt=MF)
FO4_ROW = R

# === 4. RESTRIÇÕES ===
R = FO4_ROW + 2
stitle(ws4, R, 1, "4. RESTRIÇÕES (LHS e RHS para o Solver)", end=11)
R += 2
hdr(ws4, R, 1, ['Descrição','Célula LHS','Fórmula LHS','Sinal','Célula RHS','Valor RHS','Status'])
R += 1

def aidx_from(node):
    return [ai for ai,(fr,to,c) in enumerate(ARCS) if fr==node]
def aidx_to(node):
    return [ai for ai,(fr,to,c) in enumerate(ARCS) if to==node]

q4_constrs = []  # for solver config

def add_c4(ws4, row, desc, lhs_f, sign, rhs_v, is_rhs_f=False):
    lhs_c = cr(row, 3)
    rhs_c = cr(row, 6)
    sc(ws4, row, 1, desc, font=F, border=BT, align=AL)
    sc(ws4, row, 2, lhs_c, font=FBLUE, border=BT, align=AC)
    sc(ws4, row, 3, lhs_f, font=F, border=BT, align=AC, fmt=IF_)
    sc(ws4, row, 4, sign, font=FB, border=BT, align=AC)
    sc(ws4, row, 5, rhs_c, font=FBLUE, border=BT, align=AC)
    sc(ws4, row, 6, rhs_v, font=FBLUE if not is_rhs_f else F, border=BT, align=AC, fmt=IF_)
    if sign == ">=":
        sc(ws4, row, 7, f'=IF({lhs_c}>={rhs_c},"OK","VIOLA")', font=F, border=BT, align=AC)
    elif sign == "<=":
        sc(ws4, row, 7, f'=IF({lhs_c}<={rhs_c},"OK","VIOLA")', font=F, border=BT, align=AC)
    else:
        sc(ws4, row, 7, f'=IF(ABS({lhs_c}-{rhs_c})<0.01,"OK","VIOLA")', font=F, border=BT, align=AC)
    q4_constrs.append((desc, lhs_c, sign, rhs_c))

# Flow conservation
for nd in INTER:
    for vi, vt in enumerate(['Minivan','Esportivo']):
        col = 4+vi
        ins = "+".join([cr(F_R0+ai, col) for ai in aidx_to(nd)]) or "0"
        outs = "+".join([cr(F_R0+ai, col) for ai in aidx_from(nd)]) or "0"
        add_c4(ws4, R, f"Conservação {nd} ({vt})", f"={ins}-({outs})", "=", 0)
        R += 1

# Supply
for p in ORIG:
    for vi, vt in enumerate(['Minivan','Esportivo']):
        col = 4+vi
        outs = "+".join([cr(F_R0+ai, col) for ai in aidx_from(p)])
        add_c4(ws4, R, f"Oferta {p} ({vt})", f"={outs}", "<=", SUP[p,vt])
        R += 1

# Demand
for d in DEST:
    for vi, vt in enumerate(['Minivan','Esportivo']):
        col = 4+vi
        ins = "+".join([cr(F_R0+ai, col) for ai in aidx_to(d)]) or "0"
        outs = "+".join([cr(F_R0+ai, col) for ai in aidx_from(d)]) or "0"
        add_c4(ws4, R, f"Demanda {d} ({vt})", f"={ins}-({outs})", ">=", DEM4[d,vt])
        R += 1

# Non-negativity note
sc(ws4, R, 1, "f_ij_v ≥ 0 — Não-negatividade (todas variáveis)", font=FB, border=BT)
sc(ws4, R, 2, f"{cr(F_R0,4)}:{cr(F_REND,5)}", font=FBLUE, border=BT, align=AC)
sc(ws4, R, 4, ">=", font=FB, border=BT, align=AC)
sc(ws4, R, 6, 0, font=FBLUE, border=BT, align=AC)
R += 2

# === 5. CONFIGURAÇÃO DO SOLVER — PASSO A PASSO ===
stitle(ws4, R, 1, "5. CONFIGURAÇÃO DO SOLVER — PASSO A PASSO", end=11)
R += 2

steps4 = [
    ("PASSO 1:", "Abra a aba 'Dados' → clique em 'Solver' (canto superior direito)"),
    ("PASSO 2:", f"Definir Objetivo: selecione a célula {FO4} (custo total, fundo amarelo)"),
    ("PASSO 3:", "Para: selecione 'Mín' (minimizar)"),
    ("PASSO 4:", f"Alterando Células Variáveis: {cr(F_R0,4)}:{cr(F_R0,5)},{cr(F_R0+1,4)}:{cr(F_R0+1,5)},...,{cr(F_REND,4)}:{cr(F_REND,5)}"
                f"\n  → Ou simplesmente: {cr(F_R0,4)}:{cr(F_REND,5)}"),
    ("PASSO 5:", "Sujeito às Restrições — clique 'Adicionar' para cada uma (ver tabela abaixo):"),
]
for si, (lbl, txt) in enumerate(steps4):
    sc(ws4, R+si, 1, lbl, font=FB, fill=FLTYELLOW)
    sc(ws4, R+si, 2, txt, font=F, align=ALT)
    ws4.merge_cells(start_row=R+si, start_column=2, end_row=R+si, end_column=11)
R += len(steps4) + 1

sc(ws4, R, 1, "Restrições a adicionar no Solver:", font=FB)
R += 1
hdr(ws4, R, 1, ['#','Referência da Célula (LHS)','Operador','Restrição (RHS)','Descrição'])
R += 1

for ci, (desc, lhs_c, sign, rhs_c) in enumerate(q4_constrs):
    sc(ws4, R+ci, 1, ci+1, font=F, border=BT, align=AC)
    sc(ws4, R+ci, 2, lhs_c, font=FBLUEB, border=BT, align=AC)
    sc(ws4, R+ci, 3, sign, font=FB, border=BT, align=AC)
    sc(ws4, R+ci, 4, rhs_c, font=FBLUEB, border=BT, align=AC)
    short_desc = desc.split(":")[0] if ":" in desc else desc
    sc(ws4, R+ci, 5, short_desc, font=F, border=BT, align=AL)
R += len(q4_constrs)

# Add non-neg row
sc(ws4, R, 1, len(q4_constrs)+1, font=F, border=BT, align=AC)
sc(ws4, R, 2, f"{cr(F_R0,4)}:{cr(F_REND,5)}", font=FBLUEB, border=BT, align=AC)
sc(ws4, R, 3, ">=", font=FB, border=BT, align=AC)
sc(ws4, R, 4, "0", font=FBLUEB, border=BT, align=AC)
sc(ws4, R, 5, "Não-negatividade", font=F, border=BT, align=AL)
R += 2

sc(ws4, R, 1, "PASSO 6:", font=FB, fill=FLTYELLOW)
sc(ws4, R, 2, "Selecionar Método de Resolução: 'Simplex LP'", font=Font(name='Arial',size=10,bold=True))
ws4.merge_cells(start_row=R, start_column=2, end_row=R, end_column=11)
R += 1
sc(ws4, R, 1, "PASSO 7:", font=FB, fill=FLTYELLOW)
sc(ws4, R, 2, "Marcar 'Tornar Variáveis Irrestritas Não Negativas' ✓", font=F)
ws4.merge_cells(start_row=R, start_column=2, end_row=R, end_column=11)
R += 1
sc(ws4, R, 1, "PASSO 8:", font=FB, fill=FLTYELLOW)
sc(ws4, R, 2, "Clicar 'Resolver' → 'Manter Solução do Solver' → OK", font=F)
ws4.merge_cells(start_row=R, start_column=2, end_row=R, end_column=11)
R += 2

# === 6. RESPOSTAS POR EXTENSO (c, d) ===
stitle(ws4, R, 1, "6. RESPOSTAS POR EXTENSO — Itens c) e d)", end=11)
R += 2

# Item c
clines = ["ITEM c) Fluxo ótimo (De → Para) e quantidades por tipo de veículo:", ""]
for vt in ['Minivan', 'Esportivo']:
    clines.append(f"=== {vt} (multiplicador de custo: ×{VMULT[vt]:.2f}) ===")
    for (fr,to,cost) in ARCS:
        val = q4f.get((fr,to,vt), 0)
        if val > 0.001:
            clines.append(f"  • {fr} → {to}: {val:.0f} veículos  (custo unit. ajustado: ${cost*VMULT[vt]:.2f}, custo total arco: ${val*cost*VMULT[vt]:,.2f})")
    clines.append("")
sc(ws4, R, 1, "\n".join(clines), font=Font(name='Arial', size=11), align=ALT)
ws4.merge_cells(start_row=R, start_column=1, end_row=R+16, end_column=11)
ws4.cell(row=R, column=1).fill = FLTGREEN
R += 18

# Item d
sc(ws4, R, 1, f"ITEM d) O custo mínimo total dessa operação é: ${q4z:,.2f}", font=Font(name='Arial',size=12,bold=True), align=AL)
ws4.merge_cells(start_row=R, start_column=1, end_row=R+1, end_column=11)
ws4.cell(row=R, column=1).fill = FLTGREEN
R += 3

# === 7. ANÁLISE DE SENSIBILIDADE — Item e ===
stitle(ws4, R, 1, "7. ANÁLISE DE SENSIBILIDADE — Item e)", end=11)
R += 2

sc(ws4, R, 1, "Como o custo total varia quando a capacidade máxima de cada arco vai de 500 a 1500 veículos:", font=FB)
ws4.merge_cells(start_row=R, start_column=1, end_row=R, end_column=6)
R += 1
hdr(ws4, R, 1, ['Capacidade Máx/Arco','Custo Total ($)','Status','Variação vs Sem Limite'])
SH = R  # sensitivity header
SR0 = R + 1
for si, cv in enumerate(CAPS):
    rr = SR0+si
    sc(ws4, rr, 1, cv, font=FBLUE, border=BT, fmt=IF_, align=AC)
    sv = SENS[cv]
    if sv is not None:
        sc(ws4, rr, 2, round(sv,2), font=F, border=BT, fmt=MF, align=AC)
        sc(ws4, rr, 3, "Viável", font=F, border=BT, align=AC)
        sc(ws4, rr, 4, f"=({cr(rr,2)}-{q4z})/{q4z}", font=F, border=BT, fmt='0.00%', align=AC)
    else:
        sc(ws4, rr, 2, "N/A", font=F, border=BT, align=AC)
        sc(ws4, rr, 3, "Inviável", font=FRED, border=BT, align=AC)
SREND = SR0 + len(CAPS) - 1
R = SREND + 2

# Sensitivity text
slines = ["ITEM e) Análise de Sensibilidade — Resposta por extenso:", ""]
slines.append("Capacidade Máx/Arco  →  Custo Total")
for cv in CAPS:
    sv = SENS[cv]
    if sv is not None:
        diff = sv - q4z
        slines.append(f"  {cv:>5} veículos  →  ${sv:>12,.2f}  (diferença: ${diff:>+10,.2f})")
    else:
        slines.append(f"  {cv:>5} veículos  →  INVIÁVEL")

viable = [(c,v) for c,v in SENS.items() if v is not None]
if viable:
    minv = min(v for _,v in viable)
    stab = min(c for c,v in viable if abs(v-minv)<0.01)
    slines.append("")
    slines.append(f"Conclusão: O custo mínimo de ${minv:,.2f} (igual ao caso sem restrição de capacidade)")
    slines.append(f"é atingido a partir de {stab} veículos/arco. Abaixo desse valor, as restrições de")
    slines.append(f"capacidade forçam o uso de rotas mais caras, elevando o custo total.")

sc(ws4, R, 1, "\n".join(slines), font=Font(name='Arial', size=11), align=ALT)
ws4.merge_cells(start_row=R, start_column=1, end_row=R+16, end_column=11)
ws4.cell(row=R, column=1).fill = FLTGREEN

# Chart
chart = LineChart()
chart.title = "Análise de Sensibilidade: Capacidade Máxima por Arco vs Custo Total"
chart.style = 10
chart.y_axis.title = "Custo Total ($)"
chart.x_axis.title = "Capacidade Máxima por Arco (veículos)"
chart.width = 28
chart.height = 16
data_ref = Reference(ws4, min_col=2, min_row=SH, max_row=SREND)
cats_ref = Reference(ws4, min_col=1, min_row=SR0, max_row=SREND)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
chart.series[0].graphicalProperties.line.width = 25000
ws4.add_chart(chart, f"A{R+18}")

# ============================================================
# SAVE & COPY
# ============================================================
out = "/home/user/Claude-Code-Skills/QUIZZES_3_e_4_Samuel.xlsx"
wb.save(out)
print(f"\nSaved: {out}")
os.makedirs("/mnt/user-data/outputs", exist_ok=True)
shutil.copy(out, "/mnt/user-data/outputs/QUIZZES_3_e_4_Samuel.xlsx")
print("Copied to /mnt/user-data/outputs/")

print(f"\n{'='*60}")
print(f"QUIZ 3: Z* = ${q3z:,.0f}")
print(f"  Abertos: {q3_open}")
for w in WH:
    for reg in REG:
        v = q3x[w,reg]
        if v and v>0.001: print(f"    {w} → {reg}: {v:,.0f}")
print(f"\nQUIZ 4: Z* = ${q4z:,.2f}")
for vt in ['Minivan','Esportivo']:
    print(f"  --- {vt} ---")
    for (fr,to,c) in ARCS:
        v = q4f.get((fr,to,vt),0)
        if v>0.001: print(f"    {fr} → {to}: {v:.0f}")
print(f"\nSensibilidade:")
for cv in CAPS:
    sv = SENS[cv]
    print(f"  Cap={cv}: {'${:,.2f}'.format(sv) if sv else 'INFEASIBLE'}")
