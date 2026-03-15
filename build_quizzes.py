#!/usr/bin/env python3
"""Build QUIZZES_3_e_4_Samuel.xlsx with PuLP optimization and openpyxl formatting."""

import pulp
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, numbers
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter
import os, copy

# ============================================================
# STYLES
# ============================================================
FONT_DEFAULT = Font(name='Arial', size=10)
FONT_HEADER = Font(name='Arial', size=10, bold=True)
FONT_TITLE = Font(name='Arial', size=14, bold=True)
FONT_SUBTITLE = Font(name='Arial', size=12, bold=True)
FONT_BLUE = Font(name='Arial', size=10, color='0000FF')
FONT_BLUE_BOLD = Font(name='Arial', size=10, color='0000FF', bold=True)
FONT_WHITE_BOLD = Font(name='Arial', size=10, color='FFFFFF', bold=True)
FILL_YELLOW = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
FILL_GRAY = PatternFill(start_color='D9D9D9', end_color='D9D9D9', fill_type='solid')
FILL_DARK = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
FILL_LIGHT_BLUE = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
FILL_LIGHT_GREEN = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
BORDER_BLUE = Border(
    left=Side(style='medium', color='0000FF'),
    right=Side(style='medium', color='0000FF'),
    top=Side(style='medium', color='0000FF'),
    bottom=Side(style='medium', color='0000FF')
)
BORDER_THIN = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_LEFT = Alignment(horizontal='left', vertical='center', wrap_text=True)
MONEY_FMT = '$#,##0'
INT_FMT = '#,##0'

def cell_ref(row, col):
    return f"{get_column_letter(col)}{row}"

def set_cell(ws, row, col, value, font=None, fill=None, border=None, align=None, fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    if font: c.font = font
    if fill: c.fill = fill
    if border: c.border = border
    if align: c.alignment = align
    if fmt: c.number_format = fmt
    return c

def header_row(ws, row, col_start, labels, fill=FILL_GRAY, font=FONT_HEADER):
    for i, lbl in enumerate(labels):
        set_cell(ws, row, col_start+i, lbl, font=font, fill=fill, border=BORDER_THIN, align=ALIGN_CENTER)

def section_title(ws, row, col, text, merge_end=None):
    set_cell(ws, row, col, text, font=FONT_SUBTITLE, fill=FILL_DARK)
    ws.cell(row=row, column=col).font = FONT_WHITE_BOLD
    if merge_end:
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=merge_end)
        for c2 in range(col, merge_end+1):
            ws.cell(row=row, column=c2).fill = FILL_DARK

# ============================================================
# QUIZ 3 — Warehouse Location (MILP)
# ============================================================
warehouses = ['NY', 'LA', 'Chicago', 'Atlanta']
regions = ['Região 1', 'Região 2', 'Região 3']
fixed_costs = {'NY': 60000, 'LA': 50000, 'Chicago': 40000, 'Atlanta': 35000}
demands = {'Região 1': 8000, 'Região 2': 9000, 'Região 3': 7000}
capacity = 15000
unit_costs = {
    ('NY','Região 1'):26, ('NY','Região 2'):41, ('NY','Região 3'):39,
    ('LA','Região 1'):59, ('LA','Região 2'):27, ('LA','Região 3'):27,
    ('Chicago','Região 1'):28, ('Chicago','Região 2'):32, ('Chicago','Região 3'):43,
    ('Atlanta','Região 1'):28, ('Atlanta','Região 2'):40, ('Atlanta','Região 3'):38,
}

# Solve Quiz 3
m3 = pulp.LpProblem("Quiz3_Warehouse", pulp.LpMinimize)
y = {w: pulp.LpVariable(f"y_{w}", cat='Binary') for w in warehouses}
x = {(w,r): pulp.LpVariable(f"x_{w}_{r}", lowBound=0) for w in warehouses for r in regions}

m3 += (pulp.lpSum(fixed_costs[w]*y[w] for w in warehouses) +
       pulp.lpSum(unit_costs[w,r]*x[w,r] for w in warehouses for r in regions))

for r in regions:
    m3 += pulp.lpSum(x[w,r] for w in warehouses) >= demands[r], f"Demand_{r}"
for w in warehouses:
    m3 += pulp.lpSum(x[w,r] for r in regions) <= capacity * y[w], f"Cap_{w}"
m3 += y['NY'] <= y['LA'], "NY_implies_LA"
m3 += pulp.lpSum(y[w] for w in warehouses) <= 2, "Max2"
m3 += y['Atlanta'] + y['LA'] >= 1, "ATL_or_LA"

m3.solve(pulp.PULP_CBC_CMD(msg=0))
print(f"Quiz 3 Status: {pulp.LpStatus[m3.status]}, Obj = {pulp.value(m3.objective)}")

q3_y = {w: int(y[w].varValue) for w in warehouses}
q3_x = {(w,r): x[w,r].varValue for w in warehouses for r in regions}
q3_obj = pulp.value(m3.objective)

# ============================================================
# QUIZ 4 — Vehicle Distribution (LP)
# ============================================================
arcs = [
    ('Porto 1','Distrib. 1',100), ('Porto 1','Revenda 3',300), ('Porto 1','Distrib. 2',130),
    ('Porto 2','Distrib. 1',150), ('Porto 2','Revenda 2',300), ('Porto 2','Distrib. 2',120),
    ('Distrib. 1','Revenda 3',160), ('Distrib. 1','Revenda 2',170), ('Distrib. 1','Distrib. 2',280),
    ('Distrib. 2','Revenda 3',140), ('Distrib. 2','Revenda 2',160),
    ('Revenda 3','Revenda 2',150),
]
vtypes = {'Minivan': 1.15, 'Esportivo': 0.90}
supply = {('Porto 1','Minivan'):325, ('Porto 1','Esportivo'):450,
          ('Porto 2','Minivan'):430, ('Porto 2','Esportivo'):300}
demand_q4 = {('Revenda 2','Minivan'):278, ('Revenda 2','Esportivo'):523,
             ('Revenda 3','Minivan'):477, ('Revenda 3','Esportivo'):227}
nodes = ['Porto 1','Porto 2','Distrib. 1','Distrib. 2','Revenda 3','Revenda 2']
intermediaries = ['Distrib. 1','Distrib. 2']
origins = ['Porto 1','Porto 2']
destinations = ['Revenda 3','Revenda 2']

def solve_q4(cap=None):
    m4 = pulp.LpProblem("Quiz4_Distribution", pulp.LpMinimize)
    f = {}
    for (i,j,c) in arcs:
        for v, mult in vtypes.items():
            f[i,j,v] = pulp.LpVariable(f"f_{i}_{j}_{v}", lowBound=0)
    # Objective
    m4 += pulp.lpSum(c*vtypes[v]*f[i,j,v] for (i,j,c) in arcs for v in vtypes)
    # Flow conservation at intermediaries
    for node in intermediaries:
        for v in vtypes:
            inflow = pulp.lpSum(f[i,j,v] for (i,j,c) in arcs if j == node)
            outflow = pulp.lpSum(f[i,j,v] for (i,j,c) in arcs if i == node)
            m4 += inflow == outflow, f"FlowCons_{node}_{v}"
    # Supply
    for port in origins:
        for v in vtypes:
            m4 += pulp.lpSum(f[port,j,v] for (i,j,c) in arcs if i == port) <= supply[port,v], f"Supply_{port}_{v}"
    # Demand
    for dest in destinations:
        for v in vtypes:
            inflow = pulp.lpSum(f[i,dest,v] for (i,j,c) in arcs if j == dest)
            outflow = pulp.lpSum(f[dest,j,v] for (i,j,c) in arcs if i == dest)
            m4 += inflow - outflow >= demand_q4[dest,v], f"Demand_{dest}_{v}"
    # Capacity constraints (if specified)
    if cap is not None:
        for (i,j,c) in arcs:
            m4 += pulp.lpSum(f[i,j,v] for v in vtypes) <= cap, f"ArcCap_{i}_{j}"
    m4.solve(pulp.PULP_CBC_CMD(msg=0))
    return m4, f

# Solve base (no capacity)
m4_base, f_base = solve_q4(cap=None)
q4_obj = pulp.value(m4_base.objective)
q4_flows = {}
for (i,j,c) in arcs:
    for v in vtypes:
        val = f_base[i,j,v].varValue
        if val and val > 0.001:
            q4_flows[i,j,v] = val
print(f"Quiz 4 Status: {pulp.LpStatus[m4_base.status]}, Obj = {q4_obj}")

# Sensitivity analysis (item e)
caps_range = list(range(500, 1600, 100))
sensitivity = {}
for cap_val in caps_range:
    m4s, _ = solve_q4(cap=cap_val)
    if m4s.status == 1:
        sensitivity[cap_val] = pulp.value(m4s.objective)
    else:
        sensitivity[cap_val] = None
        print(f"  Cap={cap_val}: Infeasible")

# Build answer texts
# Item c - flow description
flow_text_lines = ["ITEM c) Fluxo ótimo por tipo de veículo:\n"]
for v in ['Minivan', 'Esportivo']:
    flow_text_lines.append(f"--- {v} ---")
    for (i,j,c) in arcs:
        val = f_base[i,j,v].varValue
        if val and val > 0.001:
            custo_unit = c * vtypes[v]
            flow_text_lines.append(f"  {i} → {j}: {val:.0f} veículos (custo unitário: ${custo_unit:.2f})")
    flow_text_lines.append("")
flow_text = "\n".join(flow_text_lines)

# Item d
cost_text = f"ITEM d) O valor do custo mínimo total dessa operação é: ${q4_obj:,.2f}"

# Quiz 3 answer text
q3_open = [w for w in warehouses if q3_y[w]==1]
q3_text_lines = [f"SOLUÇÃO ÓTIMA — Custo Total Mínimo: ${q3_obj:,.0f}\n",
    f"Armazéns abertos: {', '.join(q3_open)}\n",
    "Envios (armazém → região):"]
for w in warehouses:
    for r in regions:
        val = q3_x[w,r]
        if val and val > 0.001:
            q3_text_lines.append(f"  {w} → {r}: {val:,.0f} unidades")
q3_answer_text = "\n".join(q3_text_lines)

# ============================================================
# BUILD EXCEL
# ============================================================
wb = Workbook()

# ======================== QUIZ 3 SHEET ========================
ws3 = wb.active
ws3.title = "Quiz 3 - Armazéns"

# -- TITLE --
r = 1
set_cell(ws3, r, 1, "QUIZ 3 — Localização de Armazéns (MILP)", font=FONT_TITLE)
ws3.merge_cells('A1:H1')

# -- DATA SECTION --
r = 3
section_title(ws3, r, 1, "1. DADOS DO PROBLEMA", merge_end=8)

r = 5
set_cell(ws3, r, 1, "Custos Unitários (Produção + Transporte)", font=FONT_HEADER)
r = 6
header_row(ws3, r, 1, ['Armazém', 'Região 1', 'Região 2', 'Região 3'])
for wi, w in enumerate(warehouses):
    row = r + 1 + wi
    set_cell(ws3, row, 1, w, font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER)
    for ri, reg in enumerate(regions):
        set_cell(ws3, row, 2+ri, unit_costs[w,reg], font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER, fmt=MONEY_FMT)
# Store unit cost cell refs: row 7-10, cols B-D
UC_START_ROW = 7
UC_END_ROW = 10

r = 12
set_cell(ws3, r, 1, "Custos Fixos Semanais", font=FONT_HEADER)
r = 13
header_row(ws3, r, 1, ['Armazém', 'Custo Fixo'])
FC_START_ROW = 14
for wi, w in enumerate(warehouses):
    row = FC_START_ROW + wi
    set_cell(ws3, row, 1, w, font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER)
    set_cell(ws3, row, 2, fixed_costs[w], font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER, fmt=MONEY_FMT)

r = 19
set_cell(ws3, r, 1, "Demandas Semanais", font=FONT_HEADER)
r = 20
header_row(ws3, r, 1, ['Região', 'Demanda'])
DEM_START_ROW = 21
for ri, reg in enumerate(regions):
    row = DEM_START_ROW + ri
    set_cell(ws3, row, 1, reg, font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER)
    set_cell(ws3, row, 2, demands[reg], font=FONT_BLUE, border=BORDER_THIN, align=ALIGN_CENTER, fmt=INT_FMT)

set_cell(ws3, 25, 1, "Capacidade por armazém:", font=FONT_HEADER)
set_cell(ws3, 25, 2, capacity, font=FONT_BLUE, fmt=INT_FMT)

# -- DECISION VARIABLES --
r = 27
section_title(ws3, r, 1, "2. VARIÁVEIS DE DECISÃO", merge_end=8)

r = 29
set_cell(ws3, r, 1, "Variáveis Binárias (y_i = 1 se armazém i é aberto)", font=FONT_HEADER)
r = 30
header_row(ws3, r, 1, ['NY', 'LA', 'Chicago', 'Atlanta'])
Y_ROW = 31
for wi, w in enumerate(warehouses):
    set_cell(ws3, Y_ROW, 1+wi, q3_y[w], font=FONT_BLUE_BOLD, border=BORDER_BLUE, align=ALIGN_CENTER, fmt='0')

r = 33
set_cell(ws3, r, 1, "Variáveis de Envio x_ij (unidades armazém → região)", font=FONT_HEADER)
r = 34
header_row(ws3, r, 1, ['Armazém', 'Região 1', 'Região 2', 'Região 3', 'Total Enviado'])
X_START_ROW = 35
for wi, w in enumerate(warehouses):
    row = X_START_ROW + wi
    set_cell(ws3, row, 1, w, font=FONT_HEADER, border=BORDER_THIN, align=ALIGN_CENTER)
    for ri, reg in enumerate(regions):
        set_cell(ws3, row, 2+ri, q3_x[w,reg], font=FONT_BLUE_BOLD, border=BORDER_BLUE, align=ALIGN_CENTER, fmt=INT_FMT)
    # Total sent from this warehouse
    cols = ','.join([cell_ref(row, 2+ri) for ri in range(3)])
    set_cell(ws3, row, 5, None, font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER, fmt=INT_FMT)
    ws3.cell(row=row, column=5).value = f"=SUM({cell_ref(row,2)}:{cell_ref(row,4)})"

# Demand totals row
r = X_START_ROW + 4  # row 39
set_cell(ws3, r, 1, "Total Recebido", font=FONT_HEADER, border=BORDER_THIN, align=ALIGN_CENTER)
for ri in range(3):
    col = 2 + ri
    formula = f"=SUM({cell_ref(X_START_ROW, col)}:{cell_ref(X_START_ROW+3, col)})"
    set_cell(ws3, r, col, formula, font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER, fmt=INT_FMT)

# -- OBJECTIVE FUNCTION --
r = 41
section_title(ws3, r, 1, "3. FUNÇÃO OBJETIVO (Minimizar Custo Total)", merge_end=8)

r = 43
set_cell(ws3, r, 1, "Custo Fixo Total:", font=FONT_HEADER)
# =SUMPRODUCT(B14:B17, A31:D31) — but need to map correctly
# Fixed costs are in B14:B17, y values in A31:D31
# We do it component by component: =B14*A31 + B15*B31 + B16*C31 + B17*D31
fc_formula = "=" + "+".join([f"{cell_ref(FC_START_ROW+wi,2)}*{cell_ref(Y_ROW,1+wi)}" for wi in range(4)])
set_cell(ws3, r, 2, fc_formula, font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT)

r = 44
set_cell(ws3, r, 1, "Custo Variável Total:", font=FONT_HEADER)
# =SUMPRODUCT(unit_costs_range, x_range)
vc_formula = "=SUMPRODUCT(" + cell_ref(UC_START_ROW,2) + ":" + cell_ref(UC_END_ROW,4) + "," + cell_ref(X_START_ROW,2) + ":" + cell_ref(X_START_ROW+3,4) + ")"
set_cell(ws3, r, 2, vc_formula, font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT)

r = 45
set_cell(ws3, r, 1, "CUSTO TOTAL (FO):", font=Font(name='Arial', size=12, bold=True))
fo_formula = f"={cell_ref(43,2)}+{cell_ref(44,2)}"
c_fo = set_cell(ws3, r, 2, fo_formula, font=Font(name='Arial', size=12, bold=True), fill=FILL_YELLOW, border=BORDER_BLUE, fmt=MONEY_FMT)
FO3_CELL = cell_ref(45, 2)

# -- CONSTRAINTS --
r = 47
section_title(ws3, r, 1, "4. RESTRIÇÕES", merge_end=8)

r = 49
header_row(ws3, r, 1, ['Restrição', 'LHS', 'Sinal', 'RHS', 'Atendida?'])

# Demand constraints
for ri, reg in enumerate(regions):
    row = 50 + ri
    set_cell(ws3, row, 1, f"Demanda {reg}", font=FONT_DEFAULT, border=BORDER_THIN)
    lhs_ref = cell_ref(39, 2+ri)  # total received
    set_cell(ws3, row, 2, f"={lhs_ref}", font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws3, row, 3, ">=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
    set_cell(ws3, row, 4, demands[reg], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws3, row, 5, f'=IF({cell_ref(row,2)}>={cell_ref(row,4)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)

# Capacity constraints
for wi, w in enumerate(warehouses):
    row = 53 + wi
    set_cell(ws3, row, 1, f"Capacidade {w}", font=FONT_DEFAULT, border=BORDER_THIN)
    lhs_ref = cell_ref(X_START_ROW+wi, 5)  # total sent
    set_cell(ws3, row, 2, f"={lhs_ref}", font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws3, row, 3, "<=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
    rhs_formula = f"={cell_ref(25,2)}*{cell_ref(Y_ROW,1+wi)}"
    set_cell(ws3, row, 4, rhs_formula, font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws3, row, 5, f'=IF({cell_ref(row,2)}<={cell_ref(row,4)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)

# Logical constraints
row = 57
set_cell(ws3, row, 1, "NY → LA (y_NY ≤ y_LA)", font=FONT_DEFAULT, border=BORDER_THIN)
set_cell(ws3, row, 2, f"={cell_ref(Y_ROW,1)}", font=FONT_DEFAULT, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 3, "<=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
set_cell(ws3, row, 4, f"={cell_ref(Y_ROW,2)}", font=FONT_DEFAULT, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 5, f'=IF({cell_ref(row,2)}<={cell_ref(row,4)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)

row = 58
set_cell(ws3, row, 1, "Máx 2 armazéns (Σy ≤ 2)", font=FONT_DEFAULT, border=BORDER_THIN)
set_cell(ws3, row, 2, f"=SUM({cell_ref(Y_ROW,1)}:{cell_ref(Y_ROW,4)})", font=FONT_DEFAULT, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 3, "<=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
set_cell(ws3, row, 4, 2, font=FONT_BLUE, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 5, f'=IF({cell_ref(row,2)}<={cell_ref(row,4)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)

row = 59
set_cell(ws3, row, 1, "ATL ou LA (y_ATL + y_LA ≥ 1)", font=FONT_DEFAULT, border=BORDER_THIN)
set_cell(ws3, row, 2, f"={cell_ref(Y_ROW,4)}+{cell_ref(Y_ROW,2)}", font=FONT_DEFAULT, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 3, ">=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
set_cell(ws3, row, 4, 1, font=FONT_BLUE, border=BORDER_THIN, fmt='0')
set_cell(ws3, row, 5, f'=IF({cell_ref(row,2)}>={cell_ref(row,4)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)

row = 60
set_cell(ws3, row, 1, "y_i ∈ {0,1} (binário)", font=FONT_DEFAULT, border=BORDER_THIN)
set_cell(ws3, row, 2, "Restrição de tipo", font=FONT_DEFAULT, border=BORDER_THIN)
set_cell(ws3, row, 3, "=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
set_cell(ws3, row, 4, "Binário", font=FONT_BLUE, border=BORDER_THIN)

# -- SOLVER CONFIG --
r = 62
section_title(ws3, r, 1, "5. CONFIGURAÇÃO DO SOLVER", merge_end=8)

solver_info = [
    ("Célula Objetivo:", f"{FO3_CELL} (Minimizar)"),
    ("Variáveis de Decisão:", f"{cell_ref(Y_ROW,1)}:{cell_ref(Y_ROW,4)} (binárias), {cell_ref(X_START_ROW,2)}:{cell_ref(X_START_ROW+3,4)} (contínuas)"),
    ("Método:", "Simplex LP (Branch & Bound para variáveis binárias)"),
    ("Restrições:", ""),
]
for si, (label, val) in enumerate(solver_info):
    set_cell(ws3, r+2+si, 1, label, font=FONT_HEADER)
    set_cell(ws3, r+2+si, 2, val, font=FONT_DEFAULT)
    if si == 3:
        ws3.merge_cells(start_row=r+2+si, start_column=2, end_row=r+2+si, end_column=8)

# List constraints for solver
constr_list = [
    f"{cell_ref(50,2)} >= {cell_ref(50,4)}  (Demanda Região 1)",
    f"{cell_ref(51,2)} >= {cell_ref(51,4)}  (Demanda Região 2)",
    f"{cell_ref(52,2)} >= {cell_ref(52,4)}  (Demanda Região 3)",
    f"{cell_ref(53,2)} <= {cell_ref(53,4)}  (Capacidade NY)",
    f"{cell_ref(54,2)} <= {cell_ref(54,4)}  (Capacidade LA)",
    f"{cell_ref(55,2)} <= {cell_ref(55,4)}  (Capacidade Chicago)",
    f"{cell_ref(56,2)} <= {cell_ref(56,4)}  (Capacidade Atlanta)",
    f"{cell_ref(57,2)} <= {cell_ref(57,4)}  (NY→LA)",
    f"{cell_ref(58,2)} <= {cell_ref(58,4)}  (Máx 2 armazéns)",
    f"{cell_ref(59,2)} >= {cell_ref(59,4)}  (ATL ou LA)",
    f"{cell_ref(Y_ROW,1)}:{cell_ref(Y_ROW,4)} = Binário",
    f"{cell_ref(X_START_ROW,2)}:{cell_ref(X_START_ROW+3,4)} >= 0",
]
for ci, ctext in enumerate(constr_list):
    set_cell(ws3, 68+ci, 2, ctext, font=FONT_DEFAULT)

# -- ANSWER SECTION --
r = 82
section_title(ws3, r, 1, "6. RESPOSTA POR EXTENSO", merge_end=8)
r = 84
set_cell(ws3, r, 1, q3_answer_text, font=Font(name='Arial', size=11), align=ALIGN_LEFT)
ws3.merge_cells(start_row=r, start_column=1, end_row=r+8, end_column=8)
ws3.cell(row=r, column=1).fill = FILL_LIGHT_GREEN

# Column widths
for col_idx in range(1, 9):
    ws3.column_dimensions[get_column_letter(col_idx)].width = 18

# ======================== QUIZ 4 SHEET ========================
ws4 = wb.create_sheet("Quiz 4 - Distribuição")

r = 1
set_cell(ws4, r, 1, "QUIZ 4 — Distribuição de Veículos (PL - Fluxo em Rede)", font=FONT_TITLE)
ws4.merge_cells('A1:K1')

# -- DATA SECTION --
r = 3
section_title(ws4, r, 1, "1. DADOS DO PROBLEMA", merge_end=11)

# Arcs table
r = 5
set_cell(ws4, r, 1, "Arcos da Rede e Custos Padrão", font=FONT_HEADER)
r = 6
header_row(ws4, r, 1, ['#', 'De', 'Para', 'Custo Padrão', 'Custo Minivan (×1.15)', 'Custo Esportivo (×0.90)'])
ARC_DATA_ROW = 7
for ai, (fr, to, cost) in enumerate(arcs):
    row = ARC_DATA_ROW + ai
    set_cell(ws4, row, 1, ai+1, font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
    set_cell(ws4, row, 2, fr, font=FONT_BLUE, border=BORDER_THIN)
    set_cell(ws4, row, 3, to, font=FONT_BLUE, border=BORDER_THIN)
    set_cell(ws4, row, 4, cost, font=FONT_BLUE, border=BORDER_THIN, fmt=MONEY_FMT)
    set_cell(ws4, row, 5, f"={cell_ref(row,4)}*1.15", font=FONT_DEFAULT, border=BORDER_THIN, fmt='$#,##0.00')
    set_cell(ws4, row, 6, f"={cell_ref(row,4)}*0.9", font=FONT_DEFAULT, border=BORDER_THIN, fmt='$#,##0.00')

# Supply table
r = ARC_DATA_ROW + len(arcs) + 1  # 19
SUP_ROW = r + 1
set_cell(ws4, r, 1, "Oferta (Portos)", font=FONT_HEADER)
r += 1
header_row(ws4, r, 1, ['Porto', 'Minivan', 'Esportivo'])
for pi, port in enumerate(origins):
    row = r + 1 + pi
    set_cell(ws4, row, 1, port, font=FONT_BLUE, border=BORDER_THIN)
    set_cell(ws4, row, 2, supply[port,'Minivan'], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws4, row, 3, supply[port,'Esportivo'], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
SUP_DATA_ROW = r + 1  # first data row of supply

# Demand table
r = SUP_DATA_ROW + 3
DEM4_ROW = r
set_cell(ws4, r, 1, "Demanda (Revendas)", font=FONT_HEADER)
r += 1
header_row(ws4, r, 1, ['Revenda', 'Minivan', 'Esportivo'])
for di, dest in enumerate(destinations):
    row = r + 1 + di
    set_cell(ws4, row, 1, dest, font=FONT_BLUE, border=BORDER_THIN)
    set_cell(ws4, row, 2, demand_q4[dest,'Minivan'], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
    set_cell(ws4, row, 3, demand_q4[dest,'Esportivo'], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)

# -- DECISION VARIABLES --
r = DEM4_ROW + 6
VAR4_SECTION = r
section_title(ws4, r, 1, "2. VARIÁVEIS DE DECISÃO (Fluxo por Arco e Tipo)", merge_end=11)

r += 2
set_cell(ws4, r, 1, "Fluxo de Veículos por Arco", font=FONT_HEADER)
r += 1
header_row(ws4, r, 1, ['#', 'De', 'Para', 'Fluxo Minivan', 'Fluxo Esportivo', 'Fluxo Total', 'Custo Minivan', 'Custo Esportivo', 'Custo Total Arco'])
FLOW_HDR_ROW = r
FLOW_START_ROW = r + 1
for ai, (fr, to, cost) in enumerate(arcs):
    row = FLOW_START_ROW + ai
    set_cell(ws4, row, 1, ai+1, font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
    set_cell(ws4, row, 2, fr, font=FONT_DEFAULT, border=BORDER_THIN)
    set_cell(ws4, row, 3, to, font=FONT_DEFAULT, border=BORDER_THIN)
    # Flow values (decision variables)
    fmin = q4_flows.get((fr,to,'Minivan'), 0)
    fesp = q4_flows.get((fr,to,'Esportivo'), 0)
    set_cell(ws4, row, 4, fmin, font=FONT_BLUE_BOLD, border=BORDER_BLUE, align=ALIGN_CENTER, fmt=INT_FMT)
    set_cell(ws4, row, 5, fesp, font=FONT_BLUE_BOLD, border=BORDER_BLUE, align=ALIGN_CENTER, fmt=INT_FMT)
    # Total flow
    set_cell(ws4, row, 6, f"={cell_ref(row,4)}+{cell_ref(row,5)}", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER, fmt=INT_FMT)
    # Cost per type — reference arc cost from data section
    arc_cost_cell = cell_ref(ARC_DATA_ROW + ai, 4)
    set_cell(ws4, row, 7, f"={cell_ref(row,4)}*{arc_cost_cell}*1.15", font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT)
    set_cell(ws4, row, 8, f"={cell_ref(row,5)}*{arc_cost_cell}*0.9", font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT)
    set_cell(ws4, row, 9, f"={cell_ref(row,7)}+{cell_ref(row,8)}", font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT)

FLOW_END_ROW = FLOW_START_ROW + len(arcs) - 1

# -- OBJECTIVE FUNCTION --
r = FLOW_END_ROW + 2
section_title(ws4, r, 1, "3. FUNÇÃO OBJETIVO (Minimizar Custo Total de Transporte)", merge_end=11)
r += 2
set_cell(ws4, r, 1, "CUSTO TOTAL (FO):", font=Font(name='Arial', size=12, bold=True))
fo4_formula = f"=SUM({cell_ref(FLOW_START_ROW,9)}:{cell_ref(FLOW_END_ROW,9)})"
set_cell(ws4, r, 2, fo4_formula, font=Font(name='Arial', size=12, bold=True), fill=FILL_YELLOW, border=BORDER_BLUE, fmt=MONEY_FMT)
FO4_ROW = r
FO4_CELL = cell_ref(r, 2)

# -- CONSTRAINTS SECTION --
r = FO4_ROW + 2
CONSTR4_SECTION = r
section_title(ws4, r, 1, "4. RESTRIÇÕES", merge_end=11)

r += 2
header_row(ws4, r, 1, ['Restrição', 'Tipo', 'LHS', 'Sinal', 'RHS', 'Atendida?'])
CONSTR4_HDR = r
cr = r + 1

# Helper: build LHS formula for flow constraints
def arc_indices_from(node):
    return [ai for ai, (fr,to,c) in enumerate(arcs) if fr == node]
def arc_indices_to(node):
    return [ai for ai, (fr,to,c) in enumerate(arcs) if to == node]

# Flow conservation constraints
for node in intermediaries:
    for vi, v in enumerate(['Minivan', 'Esportivo']):
        col_flow = 4 + vi  # 4=Minivan, 5=Esportivo
        in_refs = [cell_ref(FLOW_START_ROW+ai, col_flow) for ai in arc_indices_to(node)]
        out_refs = [cell_ref(FLOW_START_ROW+ai, col_flow) for ai in arc_indices_from(node)]
        lhs_in = "+".join(in_refs) if in_refs else "0"
        lhs_out = "+".join(out_refs) if out_refs else "0"
        set_cell(ws4, cr, 1, f"Conservação {node} ({v})", font=FONT_DEFAULT, border=BORDER_THIN)
        set_cell(ws4, cr, 2, "Fluxo", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 3, f"={lhs_in}-({lhs_out})", font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 4, "=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 5, 0, font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 6, f'=IF({cell_ref(cr,3)}={cell_ref(cr,5)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        cr += 1

# Supply constraints
for port in origins:
    for vi, v in enumerate(['Minivan', 'Esportivo']):
        col_flow = 4 + vi
        out_refs = [cell_ref(FLOW_START_ROW+ai, col_flow) for ai in arc_indices_from(port)]
        lhs = "+".join(out_refs)
        set_cell(ws4, cr, 1, f"Oferta {port} ({v})", font=FONT_DEFAULT, border=BORDER_THIN)
        set_cell(ws4, cr, 2, "Oferta", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 3, f"={lhs}", font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 4, "<=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 5, supply[port,v], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 6, f'=IF({cell_ref(cr,3)}<={cell_ref(cr,5)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        cr += 1

# Demand constraints
for dest in destinations:
    for vi, v in enumerate(['Minivan', 'Esportivo']):
        col_flow = 4 + vi
        in_refs = [cell_ref(FLOW_START_ROW+ai, col_flow) for ai in arc_indices_to(dest)]
        out_refs = [cell_ref(FLOW_START_ROW+ai, col_flow) for ai in arc_indices_from(dest)]
        lhs_in = "+".join(in_refs) if in_refs else "0"
        lhs_out = "+".join(out_refs) if out_refs else "0"
        set_cell(ws4, cr, 1, f"Demanda {dest} ({v})", font=FONT_DEFAULT, border=BORDER_THIN)
        set_cell(ws4, cr, 2, "Demanda", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 3, f"={lhs_in}-({lhs_out})", font=FONT_DEFAULT, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 4, ">=", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, cr, 5, demand_q4[dest,v], font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT)
        set_cell(ws4, cr, 6, f'=IF({cell_ref(cr,3)}>={cell_ref(cr,5)},"OK","VIOLA")', font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        cr += 1

CONSTR4_END = cr

# -- SOLVER CONFIG --
cr += 1
section_title(ws4, cr, 1, "5. CONFIGURAÇÃO DO SOLVER", merge_end=11)
cr += 2
solver4_info = [
    ("Célula Objetivo:", f"{FO4_CELL} (Minimizar)"),
    ("Variáveis de Decisão:", f"{cell_ref(FLOW_START_ROW,4)}:{cell_ref(FLOW_END_ROW,5)} (fluxos contínuos ≥ 0)"),
    ("Método:", "Simplex LP"),
    ("Restrições:", "Ver seção 4 acima — conservação de fluxo, oferta e demanda"),
]
for si, (label, val) in enumerate(solver4_info):
    set_cell(ws4, cr+si, 1, label, font=FONT_HEADER)
    set_cell(ws4, cr+si, 2, val, font=FONT_DEFAULT)
cr += len(solver4_info) + 1

# -- ITEM c) and d) ANSWERS --
cr += 1
section_title(ws4, cr, 1, "6. RESPOSTAS POR EXTENSO (Itens c e d)", merge_end=11)
cr += 2
ANSWER_C_ROW = cr
set_cell(ws4, cr, 1, flow_text, font=Font(name='Arial', size=11), align=ALIGN_LEFT)
ws4.merge_cells(start_row=cr, start_column=1, end_row=cr+15, end_column=11)
ws4.cell(row=cr, column=1).fill = FILL_LIGHT_GREEN

cr = ANSWER_C_ROW + 17
set_cell(ws4, cr, 1, cost_text, font=Font(name='Arial', size=12, bold=True), align=ALIGN_LEFT)
ws4.merge_cells(start_row=cr, start_column=1, end_row=cr+1, end_column=11)
ws4.cell(row=cr, column=1).fill = FILL_LIGHT_GREEN
ANSWER_D_ROW = cr

# -- ITEM e) SENSITIVITY ANALYSIS --
cr = ANSWER_D_ROW + 3
section_title(ws4, cr, 1, "7. ANÁLISE DE SENSIBILIDADE — Item e)", merge_end=11)
cr += 2
set_cell(ws4, cr, 1, "Variação do custo total conforme capacidade máxima por arco (500 a 1500, intervalos de 100)", font=FONT_HEADER)
ws4.merge_cells(start_row=cr, start_column=1, end_row=cr, end_column=6)
cr += 1
header_row(ws4, cr, 1, ['Capacidade Máx/Arco', 'Custo Total', 'Status'])
SENS_HDR_ROW = cr
SENS_START_ROW = cr + 1
for si, cap_val in enumerate(caps_range):
    row = SENS_START_ROW + si
    set_cell(ws4, row, 1, cap_val, font=FONT_BLUE, border=BORDER_THIN, fmt=INT_FMT, align=ALIGN_CENTER)
    cost_val = sensitivity[cap_val]
    if cost_val is not None:
        set_cell(ws4, row, 2, round(cost_val, 2), font=FONT_DEFAULT, border=BORDER_THIN, fmt=MONEY_FMT, align=ALIGN_CENTER)
        set_cell(ws4, row, 3, "Viável", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
    else:
        set_cell(ws4, row, 2, "N/A", font=FONT_DEFAULT, border=BORDER_THIN, align=ALIGN_CENTER)
        set_cell(ws4, row, 3, "Inviável", font=Font(name='Arial', size=10, color='FF0000'), border=BORDER_THIN, align=ALIGN_CENTER)
SENS_END_ROW = SENS_START_ROW + len(caps_range) - 1

# Sensitivity text
cr = SENS_END_ROW + 2
sens_text_lines = ["ITEM e) Análise de Sensibilidade:\n"]
sens_text_lines.append("Capacidade Máx/Arco → Custo Total:")
for cap_val in caps_range:
    cost_val = sensitivity[cap_val]
    if cost_val is not None:
        sens_text_lines.append(f"  {cap_val:>5} veículos → ${cost_val:>12,.2f}")
    else:
        sens_text_lines.append(f"  {cap_val:>5} veículos → INVIÁVEL (demanda não pode ser atendida)")

# Find where cost stabilizes
viable_costs = [(c, v) for c, v in sensitivity.items() if v is not None]
if len(viable_costs) > 1:
    min_cost = min(v for _, v in viable_costs)
    stabilize_cap = min(c for c, v in viable_costs if abs(v - min_cost) < 0.01)
    sens_text_lines.append(f"\nO custo mínimo de ${min_cost:,.2f} é atingido a partir da capacidade de {stabilize_cap} veículos/arco.")
    sens_text_lines.append("Abaixo desse valor, as restrições de capacidade forçam rotas mais caras ou tornam o problema inviável.")

sens_text = "\n".join(sens_text_lines)
set_cell(ws4, cr, 1, sens_text, font=Font(name='Arial', size=11), align=ALIGN_LEFT)
ws4.merge_cells(start_row=cr, start_column=1, end_row=cr+14, end_column=11)
ws4.cell(row=cr, column=1).fill = FILL_LIGHT_GREEN

# -- CHART --
# Only chart viable values
viable_indices = [si for si, cap_val in enumerate(caps_range) if sensitivity[cap_val] is not None]
if len(viable_indices) >= 2:
    chart = LineChart()
    chart.title = "Análise de Sensibilidade: Capacidade vs Custo Total"
    chart.style = 10
    chart.y_axis.title = "Custo Total ($)"
    chart.x_axis.title = "Capacidade Máxima por Arco"
    chart.width = 25
    chart.height = 15

    data_ref = Reference(ws4, min_col=2, min_row=SENS_HDR_ROW, max_row=SENS_END_ROW)
    cats_ref = Reference(ws4, min_col=1, min_row=SENS_START_ROW, max_row=SENS_END_ROW)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.series[0].graphicalProperties.line.width = 25000

    chart_row = cr + 16
    ws4.add_chart(chart, f"A{chart_row}")

# Column widths for Quiz 4
for col_idx in range(1, 12):
    ws4.column_dimensions[get_column_letter(col_idx)].width = 18

# ============================================================
# SAVE
# ============================================================
output_path = "/home/user/Claude-Code-Skills/QUIZZES_3_e_4_Samuel.xlsx"
wb.save(output_path)
print(f"\nSaved to {output_path}")

# Copy to outputs
os.makedirs("/mnt/user-data/outputs", exist_ok=True)
import shutil
shutil.copy(output_path, "/mnt/user-data/outputs/QUIZZES_3_e_4_Samuel.xlsx")
print("Copied to /mnt/user-data/outputs/QUIZZES_3_e_4_Samuel.xlsx")

# Print solutions summary
print("\n" + "="*60)
print("QUIZ 3 SOLUTION SUMMARY")
print("="*60)
print(q3_answer_text)
print(f"\n{'='*60}")
print("QUIZ 4 SOLUTION SUMMARY")
print("="*60)
print(flow_text)
print(cost_text)
print("\nSensitivity:")
for cap_val in caps_range:
    cost_val = sensitivity[cap_val]
    status = f"${cost_val:,.2f}" if cost_val else "INFEASIBLE"
    print(f"  Cap={cap_val}: {status}")
