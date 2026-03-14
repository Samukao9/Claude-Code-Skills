#!/usr/bin/env python3
"""Generate comprehensive PDF study guide for all installed Claude Code skills."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from datetime import datetime

# ─── Colors ────────────────────────────────────────────────────────────
PRIMARY = HexColor("#1a1a2e")
SECONDARY = HexColor("#16213e")
ACCENT = HexColor("#e94560")
ACCENT2 = HexColor("#0f3460")
LIGHT_BG = HexColor("#f8f9fa")
MEDIUM_BG = HexColor("#e9ecef")
DARK_TEXT = HexColor("#212529")
MUTED = HexColor("#6c757d")
SUCCESS = HexColor("#28a745")
WARNING = HexColor("#ffc107")
INFO = HexColor("#17a2b8")
WHITE = white

# ─── Custom Flowables ──────────────────────────────────────────────────
class ColoredBox(Flowable):
    def __init__(self, width, height, color, text="", text_color=white, font_size=10):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont("Helvetica-Bold", self.font_size)
            self.canv.drawCentredString(self.width/2, self.height/2 - self.font_size/3, self.text)

class SectionDivider(Flowable):
    def __init__(self, width=170*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = 2

    def draw(self):
        self.canv.setStrokeColor(ACCENT)
        self.canv.setLineWidth(2)
        self.canv.line(0, 0, self.width, 0)

# ─── Styles ────────────────────────────────────────────────────────────
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontSize=36, textColor=PRIMARY, spaceAfter=8*mm,
        alignment=TA_CENTER, fontName='Helvetica-Bold', leading=42
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontSize=16, textColor=ACCENT, spaceAfter=4*mm,
        alignment=TA_CENTER, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'ChapterTitle', parent=styles['Heading1'],
        fontSize=26, textColor=PRIMARY, spaceBefore=10*mm,
        spaceAfter=6*mm, fontName='Helvetica-Bold', leading=32
    ))
    styles.add(ParagraphStyle(
        'SectionTitle', parent=styles['Heading2'],
        fontSize=18, textColor=ACCENT2, spaceBefore=6*mm,
        spaceAfter=3*mm, fontName='Helvetica-Bold', leading=22
    ))
    styles.add(ParagraphStyle(
        'SubSection', parent=styles['Heading3'],
        fontSize=14, textColor=SECONDARY, spaceBefore=4*mm,
        spaceAfter=2*mm, fontName='Helvetica-Bold', leading=18
    ))
    styles.add(ParagraphStyle(
        'BodyText2', parent=styles['Normal'],
        fontSize=10, textColor=DARK_TEXT, spaceAfter=2*mm,
        alignment=TA_JUSTIFY, leading=14, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        'CodeBlock', parent=styles['Normal'],
        fontSize=9, textColor=HexColor("#c7254e"), spaceAfter=2*mm,
        fontName='Courier', backColor=LIGHT_BG, leading=12,
        leftIndent=10, rightIndent=10, spaceBefore=2*mm,
        borderColor=MEDIUM_BG, borderWidth=1, borderPadding=6
    ))
    styles.add(ParagraphStyle(
        'Tip', parent=styles['Normal'],
        fontSize=10, textColor=HexColor("#155724"), spaceAfter=3*mm,
        fontName='Helvetica', backColor=HexColor("#d4edda"), leading=13,
        leftIndent=10, rightIndent=10, spaceBefore=2*mm,
        borderColor=SUCCESS, borderWidth=1, borderPadding=8
    ))
    styles.add(ParagraphStyle(
        'Warning', parent=styles['Normal'],
        fontSize=10, textColor=HexColor("#856404"), spaceAfter=3*mm,
        fontName='Helvetica', backColor=HexColor("#fff3cd"), leading=13,
        leftIndent=10, rightIndent=10, spaceBefore=2*mm,
        borderColor=WARNING, borderWidth=1, borderPadding=8
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontSize=10, textColor=WHITE, fontName='Helvetica-Bold',
        alignment=TA_CENTER, leading=13
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontSize=9, textColor=DARK_TEXT, fontName='Helvetica',
        leading=12, alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=8, textColor=MUTED, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TOCEntry', parent=styles['Normal'],
        fontSize=12, textColor=ACCENT2, spaceAfter=2*mm,
        fontName='Helvetica', leading=16, leftIndent=5*mm
    ))
    styles.add(ParagraphStyle(
        'TOCChapter', parent=styles['Normal'],
        fontSize=14, textColor=PRIMARY, spaceAfter=3*mm,
        spaceBefore=3*mm, fontName='Helvetica-Bold', leading=18
    ))
    return styles

# ─── Helper Functions ──────────────────────────────────────────────────
def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    s = get_styles()
    header_row = [Paragraph(f"<b>{h}</b>", s['TableHeader']) for h in headers]
    data_rows = []
    for row in rows:
        data_rows.append([Paragraph(str(cell), s['TableCell']) for cell in row])

    table_data = [header_row] + data_rows
    if not col_widths:
        col_widths = [170*mm / len(headers)] * len(headers)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_TEXT),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_BG),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=1, color=MEDIUM_BG, spaceAfter=3*mm, spaceBefore=3*mm)

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0]/2, 15*mm,
        f"Guia Completo de Skills do Claude Code — Página {doc.page}")
    canvas.restoreState()

# ─── Content Builder ───────────────────────────────────────────────────
def build_pdf():
    s = get_styles()
    doc = SimpleDocTemplate(
        "/home/user/Claude-Code-Skills/Guia_Completo_Skills_Claude_Code.pdf",
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=25*mm
    )

    story = []

    # ══════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("GUIA COMPLETO", s['CoverTitle']))
    story.append(Paragraph("Skills &amp; Plugins do Claude Code", s['CoverSubtitle']))
    story.append(Spacer(1, 5*mm))
    story.append(SectionDivider())
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Material de Estudo e Referência Rápida", ParagraphStyle(
        'CoverDesc', parent=s['Normal'], fontSize=14, textColor=MUTED,
        alignment=TA_CENTER, fontName='Helvetica', leading=18
    )))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("12 Repositórios · 35 Skills · 55+ Comandos · 90+ Agents · 3 MCP Servers", ParagraphStyle(
        'CoverStats', parent=s['Normal'], fontSize=11, textColor=ACCENT,
        alignment=TA_CENTER, fontName='Helvetica-Bold'
    )))
    story.append(Spacer(1, 20*mm))

    cover_data = [
        ["Componente", "Quantidade", "Local"],
        ["Skills de Projeto", "35", ".claude/skills/"],
        ["Plugins Marketplace", "5", "~/.claude/plugins/marketplaces/"],
        ["Comandos Globais", "55+", "~/.claude/commands/"],
        ["Agents Globais", "12+", "~/.claude/agents/"],
        ["MCP Servers", "3", "~/.mcp.json"],
        ["CLIs Instalados", "3", "ctx7, notebooklm, bun"],
    ]
    ct = Table(cover_data, colWidths=[60*mm, 35*mm, 75*mm])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, MEDIUM_BG),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    story.append(ct)

    story.append(Spacer(1, 15*mm))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ParagraphStyle(
        'Date', parent=s['Normal'], fontSize=10, textColor=MUTED, alignment=TA_CENTER
    )))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("Sumário", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Spacer(1, 5*mm))

    toc_items = [
        ("1", "Visão Geral e Arquitetura"),
        ("2", "claude-mem — Sistema de Memória Persistente"),
        ("3", "n8n-mcp — Automação de Workflows"),
        ("4", "obsidian-skills — Formatos do Obsidian"),
        ("5", "get-shit-done — Desenvolvimento Guiado por Specs"),
        ("6", "superpowers — Biblioteca de Padrões de Desenvolvimento"),
        ("7", "awesome-claude-code — Comandos da Comunidade"),
        ("8", "ui-ux-pro-max — Inteligência de Design UI/UX"),
        ("9", "notebooklm-py — Google NotebookLM"),
        ("10", "Anthropic Skills — Coleção Oficial"),
        ("11", "Context7 — Documentação em Tempo Real"),
        ("12", "Ralph — PRDs e Execução Autônoma"),
        ("13", "ruflo/claude-flow — Orquestração Enterprise"),
        ("14", "Base de Dados — Referência Rápida de Todos os Comandos"),
        ("15", "Compatibilidade por Plataforma"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(f"<b>{num}.</b> {title}", s['TOCEntry']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 1: OVERVIEW
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Visão Geral e Arquitetura", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que são Skills, Plugins e MCP Servers?", s['SectionTitle']))
    story.append(Paragraph(
        "O Claude Code possui um ecossistema extensível com três tipos principais de extensões:",
        s['BodyText2']))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("<b>Skills</b> (.claude/skills/)", s['SubSection']))
    story.append(Paragraph(
        "Arquivos SKILL.md que ensinam ao Claude novas capacidades. São ativadas automaticamente quando o contexto da conversa corresponde à descrição da skill, ou manualmente via /nome-da-skill. Cada skill contém instruções, referências e opcionalmente scripts auxiliares.",
        s['BodyText2']))

    story.append(Paragraph("<b>Plugins Marketplace</b> (~/.claude/plugins/marketplaces/)", s['SubSection']))
    story.append(Paragraph(
        "Pacotes completos que incluem skills, comandos, agents, hooks e configurações MCP. São instalados globalmente e ficam disponíveis em todos os projetos. Podem incluir hooks de lifecycle que injetam contexto automaticamente.",
        s['BodyText2']))

    story.append(Paragraph("<b>MCP Servers</b> (~/.mcp.json)", s['SubSection']))
    story.append(Paragraph(
        "Servidores que implementam o Model Context Protocol, fornecendo ferramentas (tools) que o Claude pode chamar. Rodam como processos separados e são configurados em ~/.mcp.json. Permitem integração com serviços externos.",
        s['BodyText2']))

    story.append(Paragraph("<b>Comandos Slash</b> (~/.claude/commands/)", s['SubSection']))
    story.append(Paragraph(
        "Arquivos .md que definem prompts reutilizáveis. Invocados com /categoria:nome. Podem estar no nível global (~/.claude/commands/) ou do projeto (.claude/commands/).",
        s['BodyText2']))

    story.append(Paragraph("<b>Agents Customizados</b> (~/.claude/agents/)", s['SubSection']))
    story.append(Paragraph(
        "Definições de subagentes especializados em .md. Podem ser invocados pelo Claude para delegar tarefas específicas a agentes com instruções e modelos customizados.",
        s['BodyText2']))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Onde cada coisa fica instalada:", s['SubSection']))
    story.append(make_table(
        ["Tipo", "Local", "Escopo"],
        [
            ["Skills de Projeto", ".claude/skills/", "Apenas este projeto"],
            ["Skills Globais", "~/.claude/skills/", "Todos os projetos"],
            ["Plugins", "~/.claude/plugins/marketplaces/", "Global"],
            ["Comandos Globais", "~/.claude/commands/", "Global"],
            ["Comandos de Projeto", ".claude/commands/", "Apenas este projeto"],
            ["Agents Globais", "~/.claude/agents/", "Global"],
            ["MCP Servers", "~/.mcp.json", "Global"],
            ["Hooks", "~/.claude/settings.json ou plugin hooks.json", "Global"],
        ],
        [55*mm, 70*mm, 45*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 2: claude-mem
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("2. claude-mem — Sistema de Memória Persistente", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> thedotmack/claude-mem | <b>Versão:</b> 10.5.5", s['BodyText2']))
    story.append(Paragraph("<b>Local:</b> ~/.claude/plugins/marketplaces/thedotmack/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "O claude-mem é um sistema de memória persistente que captura automaticamente tudo que o Claude faz durante sessões de codificação, comprime com IA, e injeta contexto relevante em sessões futuras. Ele resolve o problema fundamental de que cada sessão do Claude Code começa \"do zero\" — com o claude-mem, o Claude lembra do que foi feito antes.",
        s['BodyText2']))

    story.append(Paragraph("Quando usar", s['SectionTitle']))
    story.append(Paragraph(
        "• Quando precisa que o Claude lembre de decisões anteriores<br/>"
        "• Quando quer buscar como algo foi resolvido em sessões passadas<br/>"
        "• Para projetos de longo prazo com múltiplas sessões<br/>"
        "• O sistema funciona automaticamente via hooks — não precisa ativar manualmente",
        s['BodyText2']))

    story.append(Paragraph("Skills e Comandos", s['SectionTitle']))
    story.append(make_table(
        ["Skill/Comando", "Trigger", "Descrição", "Quando Usar"],
        [
            ["/mem-search", "Automático ou manual", "Busca nas memórias de sessões passadas usando workflow de 3 camadas: search → timeline → get_observations", "\"Como resolvemos X da última vez?\", \"O que fizemos na semana passada?\""],
            ["/make-plan", "Manual", "Cria planos de implementação detalhados em fases usando subagentes para pesquisa de documentação e validação", "Antes de iniciar uma feature complexa que precisa de planejamento"],
            ["/do", "Manual", "Executa planos criados pelo make-plan usando subagentes para cada fase, com verificação e anti-patterns", "Após ter um plano pronto, para executar fase por fase"],
            ["/smart-explore", "Manual", "Exploração de código via AST (tree-sitter) — 4-8x mais eficiente que ler arquivos inteiros", "Quando precisa entender código sem gastar muitos tokens"],
        ],
        [30*mm, 25*mm, 60*mm, 55*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Hooks (automáticos)", s['SubSection']))
    story.append(make_table(
        ["Hook", "Quando Dispara", "O que Faz"],
        [
            ["SessionStart", "Ao abrir sessão", "Instala dependências, inicia worker, injeta contexto de sessões anteriores"],
            ["UserPromptSubmit", "A cada prompt do usuário", "Inicializa sessão no sistema de memória"],
            ["PostToolUse", "Após cada uso de ferramenta", "Captura observações sobre o que o Claude fez"],
            ["Stop", "Quando Claude para de responder", "Gera resumo comprimido da atividade"],
            ["SessionEnd", "Ao fechar sessão", "Marca sessão como completa no banco de dados"],
        ],
        [35*mm, 40*mm, 95*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Arquitetura Técnica", s['SubSection']))
    story.append(Paragraph(
        "• <b>Worker Service:</b> API HTTP na porta 37777 com interface web<br/>"
        "• <b>SQLite:</b> Armazena sessões, observações, resumos<br/>"
        "• <b>Chroma Vector DB:</b> Busca semântica + keyword search híbrida<br/>"
        "• <b>MCP Tools:</b> search, timeline, get_observations<br/>"
        "• <b>Tree-sitter:</b> Parsers para C, C++, Go, Java, JS, Python, Ruby, Rust, TypeScript",
        s['BodyText2']))

    story.append(Paragraph("Exemplo de Uso", s['SubSection']))
    story.append(Paragraph(
        "# Buscar como autenticação foi implementada antes<br/>"
        "/mem-search<br/>"
        "search(query=\"authentication\", limit=20, project=\"meu-projeto\")<br/>"
        "# → Retorna tabela com IDs, timestamps, títulos<br/><br/>"
        "# Ver contexto ao redor de um resultado<br/>"
        "timeline(anchor=11131, depth_before=5, depth_after=5)<br/><br/>"
        "# Buscar detalhes completos<br/>"
        "get_observations(ids=[11131, 10942])",
        s['CodeBlock']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 3: n8n-mcp
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("3. n8n-mcp — Automação de Workflows", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> czlonkowski/n8n-mcp | <b>Versão:</b> 2.37.1", s['BodyText2']))
    story.append(Paragraph("<b>Local:</b> MCP Server via npx n8n-mcp (configurado em ~/.mcp.json)", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Servidor MCP que conecta o Claude ao n8n, plataforma de automação de workflows. Fornece acesso a documentação de 1.239+ nodes de automação, permite buscar, validar e gerenciar workflows do n8n diretamente via Claude.",
        s['BodyText2']))

    story.append(Paragraph("Quando usar", s['SectionTitle']))
    story.append(Paragraph(
        "• Quando precisa criar ou editar workflows no n8n<br/>"
        "• Para buscar documentação de nodes específicos do n8n<br/>"
        "• Para validar configurações de workflow antes de deploy<br/>"
        "• Para acessar templates de workflow prontos",
        s['BodyText2']))

    story.append(Paragraph("Ferramentas MCP Disponíveis", s['SectionTitle']))
    story.append(make_table(
        ["Categoria", "Ferramentas", "Descrição"],
        [
            ["Discovery", "search_nodes, get_node_info", "Buscar e explorar 809 core + 430 community nodes"],
            ["Configuration", "get_node_essentials, get_examples", "Detalhes de configuração, exemplos de uso"],
            ["Validation", "validate_config, validate_workflow", "Validar configurações antes do deploy"],
            ["Management", "create_workflow, update_workflow", "Criar e atualizar workflows (requer API key)"],
            ["Templates", "search_templates", "Buscar entre 2.709+ templates de workflow"],
        ],
        [30*mm, 50*mm, 90*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("IMPORTANTE: Nunca edite workflows de produção diretamente. Sempre teste em ambiente de desenvolvimento primeiro.", s['Warning']))

    story.append(Paragraph("Configuração", s['SubSection']))
    story.append(Paragraph(
        "# Variáveis de ambiente necessárias para management:<br/>"
        "export N8N_API_URL=\"https://seu-n8n.com/api/v1\"<br/>"
        "export N8N_API_KEY=\"sua-api-key\"<br/><br/>"
        "# O servidor MCP já está configurado em ~/.mcp.json<br/>"
        "# Reinicie o Claude Code para ativar",
        s['CodeBlock']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 4: obsidian-skills
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("4. obsidian-skills — Formatos do Obsidian", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> kepano/obsidian-skills | <b>Local:</b> .claude/skills/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Coleção de skills que ensinam o Claude a trabalhar nativamente com os formatos de arquivo do Obsidian — o popular app de notas. Cobre Markdown especial do Obsidian, Bases, JSON Canvas e CLI.",
        s['BodyText2']))

    story.append(make_table(
        ["Skill", "Ativação", "Descrição", "Quando Usar"],
        [
            ["obsidian-markdown", "Automática ao editar .md do Obsidian", "Cria/edita Obsidian Flavored Markdown com wikilinks [[link]], callouts, properties YAML, embeds", "Criar notas, documentação, wikis no formato Obsidian"],
            ["obsidian-bases", "Ao trabalhar com .base files", "Trabalha com Obsidian Bases — views, filters, formulas sobre dados estruturados", "Criar databases/views no Obsidian"],
            ["json-canvas", "Ao trabalhar com .canvas files", "Gerencia JSON Canvas — nodes (text, file, link, group) e edges (connections)", "Criar mapas mentais, diagramas de fluxo no Obsidian"],
            ["obsidian-cli", "Manual", "Operações via CLI no vault — listar, buscar, modificar notas", "Automação em batch no vault Obsidian"],
            ["defuddle", "Ao extrair conteúdo web", "Extrai markdown limpo de páginas web, removendo navegação, ads, etc. Reduz uso de tokens", "Salvar conteúdo web como notas limpas"],
        ],
        [28*mm, 28*mm, 62*mm, 52*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 5: get-shit-done
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("5. get-shit-done — Desenvolvimento Guiado por Specs", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> gsd-build/get-shit-done | <b>Versão:</b> 1.22.4", s['BodyText2']))
    story.append(Paragraph("<b>Local:</b> ~/.claude/ (global — commands, agents, hooks)", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Sistema completo de meta-prompting e context engineering para desenvolvimento guiado por specs. Organiza o trabalho em projetos → milestones → fases, com pesquisa, planejamento, execução e verificação estruturados.",
        s['BodyText2']))

    story.append(Paragraph("Fluxo de Trabalho Típico", s['SubSection']))
    story.append(Paragraph(
        "1. /gsd:new-project → Criar projeto com especificação<br/>"
        "2. /gsd:new-milestone → Definir milestone do projeto<br/>"
        "3. /gsd:plan-phase → Planejar fase de implementação<br/>"
        "4. /gsd:research-phase → Pesquisar antes de executar<br/>"
        "5. /gsd:execute-phase → Executar a fase planejada<br/>"
        "6. /gsd:verify-work → Verificar que tudo funciona<br/>"
        "7. /gsd:complete-milestone → Marcar milestone como completo",
        s['CodeBlock']))

    story.append(Paragraph("Comandos Principais (/gsd:*)", s['SectionTitle']))
    story.append(make_table(
        ["Comando", "Categoria", "Descrição"],
        [
            ["/gsd:new-project", "Projeto", "Criar novo projeto com especificação inicial"],
            ["/gsd:new-milestone", "Projeto", "Criar milestone dentro do projeto"],
            ["/gsd:complete-milestone", "Projeto", "Marcar milestone como concluído"],
            ["/gsd:plan-phase", "Fases", "Planejar uma fase de implementação"],
            ["/gsd:execute-phase", "Fases", "Executar uma fase planejada"],
            ["/gsd:research-phase", "Fases", "Pesquisar antes de implementar"],
            ["/gsd:validate-phase", "Fases", "Validar resultados de uma fase"],
            ["/gsd:discuss-phase", "Fases", "Discutir uma fase com o Claude"],
            ["/gsd:add-phase", "Fases", "Adicionar nova fase ao milestone"],
            ["/gsd:debug", "Execução", "Debugging estruturado com metodologia"],
            ["/gsd:quick", "Execução", "Task rápida sem planejamento completo"],
            ["/gsd:progress", "Status", "Ver progresso geral do projeto"],
            ["/gsd:health", "Status", "Verificar saúde do projeto"],
            ["/gsd:add-todo", "Tasks", "Adicionar TODO ao projeto"],
            ["/gsd:check-todos", "Tasks", "Verificar TODOs pendentes"],
            ["/gsd:add-tests", "Quality", "Adicionar testes para uma feature"],
            ["/gsd:verify-work", "Quality", "Verificar trabalho realizado"],
            ["/gsd:map-codebase", "Análise", "Mapear estrutura do codebase"],
            ["/gsd:cleanup", "Manutenção", "Limpar e organizar código"],
            ["/gsd:pause-work", "Sessão", "Pausar trabalho (salvar contexto)"],
            ["/gsd:resume-work", "Sessão", "Retomar trabalho pausado"],
        ],
        [35*mm, 22*mm, 113*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Agents Especializados (12 agents)", s['SubSection']))
    story.append(make_table(
        ["Agent", "Função"],
        [
            ["gsd-planner", "Cria planos de implementação detalhados"],
            ["gsd-executor", "Executa implementações seguindo o plano"],
            ["gsd-verifier", "Verifica que a implementação está correta"],
            ["gsd-debugger", "Debugging estruturado e análise de erros"],
            ["gsd-phase-researcher", "Pesquisa documentação para uma fase específica"],
            ["gsd-project-researcher", "Pesquisa geral sobre o projeto"],
            ["gsd-research-synthesizer", "Sintetiza resultados de pesquisa"],
            ["gsd-codebase-mapper", "Mapeia e analisa estrutura do código"],
            ["gsd-roadmapper", "Cria roadmaps de desenvolvimento"],
            ["gsd-plan-checker", "Valida qualidade dos planos (read-only)"],
            ["gsd-integration-checker", "Verifica integrações entre componentes (read-only)"],
            ["gsd-nyquist-auditor", "Audita cobertura e qualidade do trabalho"],
        ],
        [45*mm, 125*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 6: superpowers
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("6. superpowers — Biblioteca de Padrões de Desenvolvimento", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> obra/superpowers | <b>Versão:</b> 5.0.2", s['BodyText2']))
    story.append(Paragraph("<b>Local:</b> ~/.claude/plugins/marketplaces/obra/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Biblioteca core de skills que ensinam ao Claude padrões comprovados de desenvolvimento: TDD, debugging sistemático, code review, uso de git worktrees, brainstorming, e mais. As skills são injetadas automaticamente no início de cada sessão via hook de SessionStart.",
        s['BodyText2']))

    story.append(Paragraph("Skills (14 skills)", s['SectionTitle']))
    story.append(make_table(
        ["Skill", "Descrição", "Quando Usar"],
        [
            ["test-driven-development", "Escrever testes primeiro, depois implementar. Red → Green → Refactor", "Sempre que for implementar nova funcionalidade"],
            ["systematic-debugging", "Metodologia estruturada para encontrar e corrigir bugs", "Quando encontrar um bug — ao invés de tentativa e erro"],
            ["subagent-driven-development", "Delegar tarefas para subagentes especializados em paralelo", "Tasks complexas que podem ser divididas"],
            ["dispatching-parallel-agents", "Lançar múltiplos agentes em paralelo para máxima eficiência", "Pesquisa, testes, refatoração em múltiplos arquivos"],
            ["writing-plans", "Criar planos de implementação detalhados antes de codificar", "Features complexas que precisam de planejamento"],
            ["executing-plans", "Executar planos fase por fase com verificação", "Após criar um plano com write-plan"],
            ["brainstorming", "Técnicas estruturadas de brainstorming para ideação", "Explorar soluções alternativas para um problema"],
            ["requesting-code-review", "Solicitar review de código de outro agente", "Antes de fazer merge de código importante"],
            ["receiving-code-review", "Processar e aplicar feedback de code review", "Ao receber review — aplicar melhorias sugeridas"],
            ["verification-before-completion", "Verificar que tudo funciona antes de finalizar", "Sempre, antes de marcar uma task como completa"],
            ["finishing-a-development-branch", "Processo completo para finalizar uma branch", "Ao concluir trabalho em uma feature branch"],
            ["using-git-worktrees", "Usar git worktrees para trabalhar em múltiplas branches", "Quando precisa alternar entre branches frequentemente"],
            ["writing-skills", "Criar novas skills para o Claude Code", "Quando quiser ensinar algo novo ao Claude"],
            ["using-superpowers", "Meta-skill: como usar o sistema de superpowers", "Referência sobre como invocar outras skills"],
        ],
        [38*mm, 65*mm, 67*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Comandos", s['SubSection']))
    story.append(Paragraph(
        "• <b>/brainstorm</b> — Inicia sessão de brainstorming estruturado<br/>"
        "• <b>/write-plan</b> — Cria plano de implementação detalhado<br/>"
        "• <b>/execute-plan</b> — Executa plano existente fase por fase",
        s['BodyText2']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 7: awesome-claude-code
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("7. awesome-claude-code — Comandos da Comunidade", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> hesreallyhim/awesome-claude-code", s['BodyText2']))
    story.append(Paragraph("<b>Local:</b> ~/.claude/commands/awesome/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Coleção curada de 23 slash commands criados pela comunidade para tarefas comuns de desenvolvimento. Cada comando é um prompt otimizado para uma tarefa específica.",
        s['BodyText2']))

    story.append(Paragraph("Comandos (/awesome:*)", s['SectionTitle']))
    story.append(make_table(
        ["Comando", "Categoria", "Descrição"],
        [
            ["/awesome:commit", "Git", "Criar commits bem formatados com mensagens descritivas"],
            ["/awesome:create-pr", "Git", "Criar Pull Requests com título, descrição e test plan"],
            ["/awesome:create-pull-request", "Git", "Variação alternativa de criação de PR"],
            ["/awesome:pr-review", "Git", "Revisar um Pull Request com feedback estruturado"],
            ["/awesome:fix-github-issue", "Git", "Resolver uma issue do GitHub com implementação"],
            ["/awesome:update-branch-name", "Git", "Renomear branch seguindo convenções"],
            ["/awesome:act", "Código", "Agir como um especialista específico"],
            ["/awesome:clean", "Código", "Limpar e organizar código existente"],
            ["/awesome:optimize", "Código", "Otimizar código para performance"],
            ["/awesome:todo", "Código", "Gerenciar TODOs no código"],
            ["/awesome:create-prd", "Projeto", "Criar Product Requirements Document"],
            ["/awesome:create-prp", "Projeto", "Criar Product Requirements Plan"],
            ["/awesome:create-jtbd", "Projeto", "Criar Jobs-To-Be-Done framework"],
            ["/awesome:create-hook", "Projeto", "Criar hook do Claude Code"],
            ["/awesome:release", "Projeto", "Preparar release com changelog"],
            ["/awesome:context-prime", "Contexto", "Preparar contexto antes de uma tarefa"],
            ["/awesome:initref", "Contexto", "Inicializar referências do projeto"],
            ["/awesome:load-llms-txt", "Contexto", "Carregar llms.txt para contexto"],
            ["/awesome:add-to-changelog", "Docs", "Adicionar entrada ao changelog"],
            ["/awesome:update-docs", "Docs", "Atualizar documentação do projeto"],
            ["/awesome:create-worktrees", "Infra", "Configurar git worktrees"],
            ["/awesome:husky", "Infra", "Configurar husky para git hooks"],
            ["/awesome:testing_plan_integration", "Quality", "Criar plano de testes de integração"],
        ],
        [42*mm, 18*mm, 110*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 8: ui-ux-pro-max
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("8. ui-ux-pro-max — Inteligência de Design UI/UX", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> nextlevelbuilder/ui-ux-pro-max-skill | <b>Versão:</b> 2.2.1", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Sistema completo de inteligência de design UI/UX com databases pesquisáveis de estilos, paletas de cores, tipografia, charts e guidelines para 13+ stacks tecnológicos. Ativado automaticamente quando o Claude detecta contexto de UI/design.",
        s['BodyText2']))

    story.append(Paragraph("Skills (7 skills)", s['SectionTitle']))
    story.append(make_table(
        ["Skill", "Recursos", "Descrição", "Quando Usar"],
        [
            ["ui-ux-pro-max", "67 estilos, 96 paletas, 57 fontes, 25 charts", "Core de design — database pesquisável de estilos, cores, tipografia, charts, UX guidelines", "Ao criar qualquer interface: website, dashboard, app, landing page"],
            ["ui-styling", "Tailwind, shadcn/ui, 30+ fontes canvas", "Estilização com Tailwind CSS, shadcn/ui components, responsive design, canvas design system", "Estilizar componentes com Tailwind/shadcn"],
            ["design", "Logo, icon, CIP design", "Design de logos, ícones e Corporate Identity Packages com scripts de geração e busca", "Criar identidade visual, logos, ícones"],
            ["design-system", "Tokens, components, slides", "Design tokens, component specs, geração de slides com layout patterns e dados CSV", "Criar/manter design system, gerar apresentações"],
            ["brand", "Guidelines, voice, messaging", "Brand guidelines completas: identidade visual, paleta de cores, tipografia, voz da marca", "Criar ou aplicar brand guidelines"],
            ["slides", "Copywriting, layouts, estratégias", "Criação de apresentações com fórmulas de copywriting, layout patterns e template HTML", "Criar apresentações profissionais"],
            ["banner-design", "Tamanhos e estilos", "Referência de tamanhos padrão de banners (social media, ads, web) e estilos", "Criar banners para diferentes plataformas"],
        ],
        [25*mm, 28*mm, 60*mm, 57*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Estilos Suportados", s['SubSection']))
    story.append(Paragraph(
        "Glassmorphism · Claymorphism · Minimalism · Brutalism · Neumorphism · Bento Grid · "
        "Dark Mode · Skeuomorphism · Flat Design · Material Design · e 57+ mais",
        s['BodyText2']))

    story.append(Paragraph("Stacks Suportados", s['SubSection']))
    story.append(Paragraph(
        "React · Next.js · Astro · Vue · Nuxt.js · Nuxt UI · Svelte · SwiftUI · "
        "React Native · Flutter · Tailwind CSS · shadcn/ui · Jetpack Compose",
        s['BodyText2']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 9: notebooklm-py
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("9. notebooklm-py — Google NotebookLM", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> teng-lin/notebooklm-py | <b>Versão:</b> 0.3.4", s['BodyText2']))
    story.append(Paragraph("<b>CLI:</b> notebooklm | <b>Skill:</b> .claude/skills/notebooklm/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Acesso programático completo ao Google NotebookLM — incluindo funcionalidades não disponíveis na interface web. Permite criar notebooks, adicionar fontes, gerar podcasts, vídeos, reports, quizzes e mais, tudo via CLI.",
        s['BodyText2']))

    story.append(Paragraph("Comandos Principais", s['SectionTitle']))
    story.append(make_table(
        ["Comando", "Descrição"],
        [
            ["notebooklm login", "Autenticar com Google OAuth (abre browser)"],
            ["notebooklm create \"Título\"", "Criar novo notebook"],
            ["notebooklm source add \"URL\"", "Adicionar fonte (URL, YouTube, PDF, áudio, vídeo, imagem)"],
            ["notebooklm source add-research \"query\"", "Web research automático"],
            ["notebooklm ask \"pergunta\"", "Chat com as fontes do notebook"],
            ["notebooklm generate audio \"instrução\"", "Gerar podcast (deep-dive, brief, critique, debate)"],
            ["notebooklm generate video \"instrução\"", "Gerar vídeo (explainer, brief, múltiplos estilos)"],
            ["notebooklm generate report --format study-guide", "Gerar relatório (briefing-doc, study-guide, blog-post)"],
            ["notebooklm generate quiz", "Gerar quiz (easy/medium/hard)"],
            ["notebooklm generate flashcards", "Gerar flashcards para estudo"],
            ["notebooklm generate slide-deck", "Gerar apresentação de slides"],
            ["notebooklm generate mind-map", "Gerar mapa mental (instantâneo)"],
            ["notebooklm download audio ./podcast.mp3", "Baixar podcast como MP3"],
            ["notebooklm download video ./video.mp4", "Baixar vídeo como MP4"],
            ["notebooklm download slide-deck ./slides.pptx --format pptx", "Baixar slides como PPTX"],
            ["notebooklm download quiz --format markdown quiz.md", "Baixar quiz como Markdown"],
            ["notebooklm language set pt_BR", "Definir idioma dos artefatos"],
        ],
        [75*mm, 95*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Pré-requisito: Execute 'notebooklm login' antes de qualquer outro comando. Re-execute se comandos falharem com erro de autenticação.", s['Warning']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 10: Anthropic Skills
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("10. Anthropic Skills — Coleção Oficial", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> anthropics/skills | <b>Local:</b> .claude/skills/", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Coleção oficial de skills criadas pela Anthropic. São as skills mais bem testadas e otimizadas, cobrindo geração de documentos, design, desenvolvimento e produtividade.",
        s['BodyText2']))

    story.append(Paragraph("Skills (17 skills)", s['SectionTitle']))
    story.append(make_table(
        ["Skill", "Categoria", "Descrição", "Quando Usar"],
        [
            ["pdf", "Documentos", "Gerar PDFs profissionais com layouts, tabelas, gráficos e formulários", "Relatórios, guias, documentação formal"],
            ["docx", "Documentos", "Criar e editar documentos Word (.docx) com formatação completa", "Documentos para compartilhar com equipe"],
            ["xlsx", "Documentos", "Criar e editar planilhas Excel (.xlsx) com fórmulas e gráficos", "Planilhas de dados, análises, relatórios"],
            ["pptx", "Documentos", "Criar e editar apresentações PowerPoint (.pptx)", "Apresentações, pitch decks, treinamentos"],
            ["claude-api", "Desenvolvimento", "Construir apps com Claude API em 7 linguagens (Python, TS, Go, Java, PHP, Ruby, C#)", "Integrar Claude em aplicações"],
            ["mcp-builder", "Desenvolvimento", "Construir servidores MCP com docs de referência e scripts", "Criar novos MCP servers"],
            ["skill-creator", "Desenvolvimento", "Criar novas skills com agents, eval viewer e templates", "Desenvolver suas próprias skills"],
            ["web-artifacts-builder", "Desenvolvimento", "Construir artefatos web interativos (HTML/CSS/JS self-contained)", "Criar demos, protótipos, tools web"],
            ["webapp-testing", "Quality", "Testar web applications com exemplos e scripts de automação", "Testes end-to-end, smoke tests"],
            ["frontend-design", "Design", "Padrões de design frontend — layouts, componentes, responsividade", "Criar interfaces de qualidade"],
            ["canvas-design", "Design", "Design baseado em canvas HTML5 com 30+ fontes bundled", "Criar gráficos, infográficos, visual content"],
            ["brand-guidelines", "Design", "Criar e aplicar brand guidelines consistentes", "Padronizar identidade visual"],
            ["theme-factory", "Design", "Gerar temas customizados com showcase PDF e templates", "Criar temas para apps/sites"],
            ["algorithmic-art", "Criativo", "Criar arte algorítmica/generativa com templates JS", "Arte digital, backgrounds, visual effects"],
            ["doc-coauthoring", "Produtividade", "Co-autoria de documentos — edição colaborativa estruturada", "Escrever documentos longos iterativamente"],
            ["internal-comms", "Produtividade", "Comunicações internas — emails, anúncios, newsletters", "Escrever comunicações profissionais"],
            ["slack-gif-creator", "Produtividade", "Criar GIFs animados para Slack com Python", "Criar GIFs customizados para equipe"],
        ],
        [28*mm, 22*mm, 62*mm, 58*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 11: Context7
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("11. Context7 — Documentação em Tempo Real", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> upstash/context7 | <b>CLI:</b> ctx7 v0.3.5", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Busca documentação atualizada de qualquer biblioteca/framework em tempo real. Ao invés de depender do conhecimento de treinamento (que pode estar desatualizado), o Context7 consulta a documentação mais recente diretamente.",
        s['BodyText2']))

    story.append(Paragraph("Quando usar", s['SectionTitle']))
    story.append(Paragraph(
        "• Sempre que perguntar sobre APIs, configurações ou código de bibliotecas externas<br/>"
        "• Quando a versão da biblioteca importa (ex: \"React 19\", \"Next.js 15\")<br/>"
        "• Para verificar breaking changes ou APIs deprecated<br/>"
        "• Quando o Claude não tem certeza sobre uma API ou configuração",
        s['BodyText2']))

    story.append(Paragraph("Componentes", s['SectionTitle']))
    story.append(make_table(
        ["Componente", "Como Usar", "Descrição"],
        [
            ["CLI ctx7", "ctx7 library react \"hooks\" → ctx7 docs /facebook/react \"useEffect\"", "Busca via linha de comando — 2 passos: resolver ID + buscar docs"],
            ["MCP Server", "Automático via tools resolve-library-id e query-docs", "Integração direta via MCP — Claude usa automaticamente"],
            ["Skill find-docs", "Ativação automática ao perguntar sobre libs", "Instrui o Claude a usar ctx7 CLI para buscar docs"],
            ["Skill context7-mcp", "Ativação automática", "Instrui o Claude a usar MCP tools para buscar docs"],
            ["/docs", "Manual: /docs react hooks", "Comando rápido para buscar documentação"],
            ["Agent docs-researcher", "Delegação automática", "Subagente leve que busca docs sem poluir contexto principal"],
        ],
        [30*mm, 60*mm, 80*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Exemplo de Uso", s['SubSection']))
    story.append(Paragraph(
        "# Passo 1: Resolver biblioteca<br/>"
        "ctx7 library nextjs \"app router middleware\"<br/>"
        "# → /vercel/next.js (Score: 95, Snippets: 2847)<br/><br/>"
        "# Passo 2: Buscar documentação<br/>"
        "ctx7 docs /vercel/next.js \"How to add auth middleware to app router\"<br/>"
        "# → Retorna code snippets + info snippets atualizados",
        s['CodeBlock']))

    story.append(Paragraph("Funciona sem autenticação. Para limites maiores: ctx7 login ou defina CONTEXT7_API_KEY.", s['Tip']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 12: Ralph
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("12. Ralph — PRDs e Execução Autônoma", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> snarktank/ralph | <b>Versão:</b> 1.0.0", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Sistema para gerar PRDs (Product Requirements Documents) e convertê-los em formato JSON executável pelo loop autônomo do Ralph. O Ralph trabalha em um ciclo: PRD → prd.json → execução autônoma → verificação.",
        s['BodyText2']))

    story.append(Paragraph("Skills", s['SectionTitle']))
    story.append(make_table(
        ["Skill", "Trigger", "Fluxo", "Quando Usar"],
        [
            ["/prd", "\"crie um PRD\", \"planeje feature\"", "1. Recebe descrição da feature<br/>2. Faz 3-5 perguntas de clarificação<br/>3. Gera PRD estruturado<br/>4. Salva em tasks/prd-[nome].md", "Ao iniciar uma nova feature — antes de codificar"],
            ["/ralph", "\"converta este PRD\", \"ralph json\"", "1. Recebe PRD (markdown ou texto)<br/>2. Extrai user stories, tasks, critérios de aceitação<br/>3. Gera prd.json com formato executável<br/>4. Salva no diretório ralph", "Quando tem um PRD pronto e quer execução autônoma"],
        ],
        [18*mm, 32*mm, 65*mm, 55*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 13: ruflo/claude-flow
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("13. ruflo/claude-flow — Orquestração Enterprise", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Paragraph("<b>Repositório:</b> ruvnet/ruflo | <b>Versão:</b> 2.5.0", s['BodyText2']))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("O que faz", s['SectionTitle']))
    story.append(Paragraph(
        "Plataforma enterprise de orquestração de agentes IA com 150+ comandos, 74+ agents, SPARC methodology, coordenação de swarms, GitHub automation e neural training. É o sistema mais completo e complexo instalado.",
        s['BodyText2']))

    story.append(Paragraph("Categorias de Skills (38 skills)", s['SectionTitle']))
    story.append(make_table(
        ["Categoria", "Skills", "Descrição"],
        [
            ["Swarm", "swarm-orchestration, swarm-advanced", "Coordenação de múltiplos agentes (Hierarchical, Mesh, Ring, Star)"],
            ["GitHub", "github-code-review, github-multi-repo, github-project-management, github-release-management, github-workflow-automation", "Automação completa de GitHub — PRs, reviews, releases, projetos"],
            ["SPARC", "sparc-methodology", "Specification, Pseudocode, Architecture, Refinement, Completion — 18 modos"],
            ["Pair Programming", "pair-programming", "Programação em par com agente IA"],
            ["AgentDB", "agentdb-advanced, agentdb-learning, agentdb-memory-patterns, agentdb-optimization, agentdb-vector-search", "Database de agentes com aprendizado e busca vetorial"],
            ["Hive Mind", "hive-mind-advanced", "Inteligência coletiva de agentes"],
            ["Flow Nexus", "flow-nexus-neural, flow-nexus-platform, flow-nexus-swarm", "Plataforma cloud de orquestração (70+ tools)"],
            ["Performance", "performance-analysis, worker-benchmarks", "Análise de performance e benchmarking"],
            ["Hooks", "hooks-automation", "Automação de hooks do Claude Code"],
            ["Reasoning", "reasoningbank-agentdb, reasoningbank-intelligence", "Banco de raciocínio e inteligência artificial"],
            ["Quality", "verification-quality, worker-integration", "Verificação de qualidade e integração"],
            ["v3", "v3-cli-modernization, v3-core-implementation, v3-ddd-architecture, + 6 mais", "Modernização, DDD, MCP optimization, security, memory"],
        ],
        [28*mm, 55*mm, 87*mm]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("MCP Server — claude-flow", s['SubSection']))
    story.append(Paragraph(
        "O MCP server claude-flow fornece 40+ tools para coordenação de swarm. Configurado em ~/.mcp.json com comando: npx -y claude-flow@alpha mcp start",
        s['BodyText2']))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 14: DATABASE
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("14. Base de Dados — Referência Rápida", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Todas as 35 Skills do Projeto", s['SectionTitle']))
    story.append(make_table(
        ["#", "Skill", "Origem", "Tipo"],
        [
            ["1", "algorithmic-art", "Anthropic", "Arte generativa"],
            ["2", "banner-design", "UI/UX Pro Max", "Design de banners"],
            ["3", "brand", "UI/UX Pro Max", "Brand guidelines"],
            ["4", "brand-guidelines", "Anthropic", "Brand guidelines"],
            ["5", "canvas-design", "Anthropic", "Design canvas"],
            ["6", "claude-api", "Anthropic", "Desenvolvimento API"],
            ["7", "context7-cli", "Context7", "Docs lookup CLI"],
            ["8", "context7-mcp", "Context7", "Docs lookup MCP"],
            ["9", "defuddle", "Obsidian", "Web scraping limpo"],
            ["10", "design", "UI/UX Pro Max", "Logo/icon design"],
            ["11", "design-system", "UI/UX Pro Max", "Design tokens"],
            ["12", "doc-coauthoring", "Anthropic", "Co-autoria"],
            ["13", "docx", "Anthropic", "Documentos Word"],
            ["14", "find-docs", "Context7", "Docs lookup"],
            ["15", "frontend-design", "Anthropic", "Frontend patterns"],
            ["16", "internal-comms", "Anthropic", "Comunicação interna"],
            ["17", "json-canvas", "Obsidian", "JSON Canvas files"],
            ["18", "mcp-builder", "Anthropic", "Criar MCP servers"],
            ["19", "notebooklm", "NotebookLM", "Google NotebookLM"],
            ["20", "obsidian-bases", "Obsidian", "Obsidian Bases"],
            ["21", "obsidian-cli", "Obsidian", "Obsidian CLI"],
            ["22", "obsidian-markdown", "Obsidian", "Obsidian Markdown"],
            ["23", "pdf", "Anthropic", "Geração de PDFs"],
            ["24", "pptx", "Anthropic", "Apresentações PPT"],
            ["25", "prd", "Ralph", "Product Requirements"],
            ["26", "ralph", "Ralph", "PRD → JSON executável"],
            ["27", "skill-creator", "Anthropic", "Criar skills"],
            ["28", "slack-gif-creator", "Anthropic", "GIFs para Slack"],
            ["29", "slides", "UI/UX Pro Max", "Criação de slides"],
            ["30", "theme-factory", "Anthropic", "Gerar temas"],
            ["31", "ui-styling", "UI/UX Pro Max", "Tailwind/shadcn"],
            ["32", "ui-ux-pro-max", "UI/UX Pro Max", "Core design DB"],
            ["33", "web-artifacts-builder", "Anthropic", "Artefatos web"],
            ["34", "webapp-testing", "Anthropic", "Testes web apps"],
            ["35", "xlsx", "Anthropic", "Planilhas Excel"],
        ],
        [8*mm, 38*mm, 32*mm, 92*mm]
    ))

    story.append(PageBreak())

    story.append(Paragraph("Todos os MCP Servers", s['SectionTitle']))
    story.append(make_table(
        ["Server", "Comando", "Ferramentas", "Propósito"],
        [
            ["n8n-mcp", "npx -y n8n-mcp", "search, validate, create workflows", "Automação de workflows n8n"],
            ["context7", "npx -y @upstash/context7-mcp", "resolve-library-id, query-docs", "Documentação em tempo real"],
            ["claude-flow", "npx -y claude-flow@alpha mcp start", "40+ tools de swarm", "Orquestração de agentes"],
        ],
        [25*mm, 55*mm, 45*mm, 45*mm]
    ))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Todos os CLIs Instalados", s['SectionTitle']))
    story.append(make_table(
        ["CLI", "Versão", "Comando de Verificação", "Propósito"],
        [
            ["ctx7", "0.3.5", "ctx7 --version", "Busca de documentação Context7"],
            ["notebooklm", "0.3.4", "notebooklm --version", "Google NotebookLM CLI"],
            ["bun", "1.3.9", "bun --version", "Runtime JavaScript (usado pelo claude-mem)"],
        ],
        [25*mm, 20*mm, 55*mm, 70*mm]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════
    # CHAPTER 15: COMPATIBILITY
    # ══════════════════════════════════════════════════════════════
    story.append(Paragraph("15. Compatibilidade por Plataforma", s['ChapterTitle']))
    story.append(SectionDivider())
    story.append(Spacer(1, 3*mm))

    story.append(make_table(
        ["Plugin/Skill", "Claude Code", "Claude AI (web)", "Claude Cowork"],
        [
            ["claude-mem", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver ~/.claude/"],
            ["n8n-mcp", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver MCP"],
            ["obsidian-skills", "✅ Completo", "❌ Não compatível", "✅ Via .claude/skills/"],
            ["get-shit-done", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver ~/.claude/"],
            ["superpowers", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver plugins/"],
            ["awesome-claude-code", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver commands/"],
            ["ui-ux-pro-max", "✅ Completo", "❌ Não compatível", "✅ Via .claude/skills/"],
            ["notebooklm-py", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver pip install"],
            ["Anthropic Skills", "✅ Completo", "⚠️ Algumas built-in", "✅ Via .claude/skills/"],
            ["Context7", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver MCP + CLI"],
            ["Ralph", "✅ Completo", "❌ Não compatível", "✅ Via .claude/skills/"],
            ["ruflo/claude-flow", "✅ Completo", "❌ Não compatível", "⚠️ Se tiver plugins/"],
        ],
        [35*mm, 30*mm, 35*mm, 35*mm]
    ))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Como instalar no Claude Cowork", s['SectionTitle']))
    story.append(Paragraph(
        "O Claude Cowork roda sobre o Claude Code. Para que os plugins funcionem no Cowork:<br/><br/>"
        "1. <b>Skills de projeto</b> (.claude/skills/) — já estão no repositório, funcionam automaticamente<br/>"
        "2. <b>Plugins globais</b> (~/.claude/plugins/) — precisam estar no filesystem do ambiente<br/>"
        "3. <b>MCP Servers</b> (~/.mcp.json) — precisam ser configurados no ambiente<br/>"
        "4. <b>CLIs</b> (ctx7, notebooklm) — precisam ser instalados: npm i -g ctx7@latest; pip install notebooklm-py<br/>"
        "5. <b>Comandos globais</b> (~/.claude/commands/) — copiar os .md para o diretório correto",
        s['BodyText2']))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("O Claude AI (web — claude.ai) NÃO suporta skills, plugins, hooks, MCP servers ou comandos customizados. Essas funcionalidades são exclusivas do Claude Code.", s['Warning']))

    story.append(Spacer(1, 10*mm))
    story.append(SectionDivider())
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        f"Documento gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}.<br/>"
        "Total: 12 repositórios · 35 skills · 55+ comandos · 90+ agents · 3 MCP servers",
        ParagraphStyle('FinalNote', parent=s['Normal'], fontSize=10, textColor=MUTED,
                       alignment=TA_CENTER, leading=14)
    ))

    # Build PDF
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print("PDF gerado com sucesso!")

if __name__ == "__main__":
    build_pdf()
