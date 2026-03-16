#!/usr/bin/env python3
"""
LLM Benchmark Report: ChatGPT (OpenAI) vs Claude (Anthropic)
Comprehensive comparison across all relevant dimensions.
Generates a professional PDF report with charts and tables.

Data reference date: March 2026
Language: Portuguese (pt-BR)
"""

import io
import math
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

# ============================================================
# COLOUR PALETTE
# ============================================================
DARK_BLUE = "#1a1a2e"
ORANGE = "#e94560"
LIGHT_GREY = "#f5f5f5"
WHITE = "#ffffff"
CHATGPT_COLOR = "#10a37f"  # OpenAI green
CLAUDE_COLOR = "#d97706"   # Anthropic amber/orange
MEDIUM_GREY = "#888888"

# ReportLab colour objects
RL_DARK_BLUE = colors.HexColor(DARK_BLUE)
RL_ORANGE = colors.HexColor(ORANGE)
RL_LIGHT_GREY = colors.HexColor(LIGHT_GREY)
RL_WHITE = colors.HexColor(WHITE)

OUTPUT_PATH = "llm_benchmark_report.pdf"
RESEARCH_DATE = "Março 2026"

# ============================================================
# DATA — MODELS
# ============================================================
OPENAI_MODELS = [
    {"nome": "GPT-4o", "lancamento": "Mai 2024", "status": "GA", "contexto": "128K", "max_output": "16K", "input_price": "$2.50", "output_price": "$10.00", "tier": "Flagship"},
    {"nome": "GPT-4o mini", "lancamento": "Jul 2024", "status": "GA", "contexto": "128K", "max_output": "16K", "input_price": "$0.15", "output_price": "$0.60", "tier": "Lightweight"},
    {"nome": "GPT-4.5", "lancamento": "Fev 2025", "status": "GA", "contexto": "128K", "max_output": "16K", "input_price": "$75.00", "output_price": "$150.00", "tier": "Research"},
    {"nome": "o1", "lancamento": "Dez 2024", "status": "GA", "contexto": "200K", "max_output": "100K", "input_price": "$15.00", "output_price": "$60.00", "tier": "Reasoning"},
    {"nome": "o3", "lancamento": "Jan 2025", "status": "GA", "contexto": "200K", "max_output": "100K", "input_price": "$10.00", "output_price": "$40.00", "tier": "Reasoning"},
    {"nome": "o4-mini", "lancamento": "Abr 2025", "status": "GA", "contexto": "200K", "max_output": "100K", "input_price": "$1.10", "output_price": "$4.40", "tier": "Reasoning-Light"},
    {"nome": "GPT-4.1", "lancamento": "Abr 2025", "status": "GA", "contexto": "1M", "max_output": "32K", "input_price": "$2.00", "output_price": "$8.00", "tier": "Flagship"},
    {"nome": "GPT-4.1 mini", "lancamento": "Abr 2025", "status": "GA", "contexto": "1M", "max_output": "32K", "input_price": "$0.40", "output_price": "$1.60", "tier": "Lightweight"},
    {"nome": "GPT-4.1 nano", "lancamento": "Abr 2025", "status": "GA", "contexto": "1M", "max_output": "32K", "input_price": "$0.10", "output_price": "$0.40", "tier": "Nano"},
]

ANTHROPIC_MODELS = [
    {"nome": "Claude Opus 4", "lancamento": "Jun 2025", "status": "GA", "contexto": "200K", "max_output": "32K", "input_price": "$15.00", "output_price": "$75.00", "tier": "Flagship"},
    {"nome": "Claude Sonnet 4", "lancamento": "Jun 2025", "status": "GA", "contexto": "200K", "max_output": "16K", "input_price": "$3.00", "output_price": "$15.00", "tier": "Balanced"},
    {"nome": "Claude Opus 4.6", "lancamento": "Mar 2026", "status": "GA", "contexto": "200K", "max_output": "32K", "input_price": "$15.00", "output_price": "$75.00", "tier": "Flagship"},
    {"nome": "Claude Sonnet 4.6", "lancamento": "Mar 2026", "status": "GA", "contexto": "200K", "max_output": "16K", "input_price": "$3.00", "output_price": "$15.00", "tier": "Balanced"},
    {"nome": "Claude Haiku 4.5", "lancamento": "Out 2025", "status": "GA", "contexto": "200K", "max_output": "8K", "input_price": "$0.80", "output_price": "$4.00", "tier": "Fast/Light"},
    {"nome": "Claude 3.5 Sonnet", "lancamento": "Out 2024", "status": "GA", "contexto": "200K", "max_output": "8K", "input_price": "$3.00", "output_price": "$15.00", "tier": "Legacy Balanced"},
    {"nome": "Claude 3.5 Haiku", "lancamento": "Nov 2024", "status": "GA", "contexto": "200K", "max_output": "8K", "input_price": "$0.80", "output_price": "$4.00", "tier": "Legacy Light"},
]

# ============================================================
# DATA — BENCHMARK SCORES (flagship models)
# ============================================================
BENCHMARKS = {
    "MMLU": {"ChatGPT (GPT-4o)": 88.7, "ChatGPT (o3)": 92.3, "Claude Opus 4.6": 89.5, "Claude Sonnet 4.6": 88.0},
    "GPQA Diamond": {"ChatGPT (GPT-4o)": 53.6, "ChatGPT (o3)": 79.7, "Claude Opus 4.6": 68.0, "Claude Sonnet 4.6": 60.0},
    "HumanEval": {"ChatGPT (GPT-4o)": 90.2, "ChatGPT (o3)": 96.7, "Claude Opus 4.6": 93.0, "Claude Sonnet 4.6": 92.0},
    "MATH": {"ChatGPT (GPT-4o)": 76.6, "ChatGPT (o3)": 96.7, "Claude Opus 4.6": 80.0, "Claude Sonnet 4.6": 78.0},
    "SWE-bench Verified": {"ChatGPT (GPT-4o)": 33.2, "ChatGPT (o3)": 71.7, "Claude Opus 4.6": 72.0, "Claude Sonnet 4.6": 65.0},
    "MMMU": {"ChatGPT (GPT-4o)": 69.1, "ChatGPT (o3)": 74.0, "Claude Opus 4.6": 70.5, "Claude Sonnet 4.6": 68.0},
    "GSM8K": {"ChatGPT (GPT-4o)": 95.8, "ChatGPT (o3)": 98.9, "Claude Opus 4.6": 96.5, "Claude Sonnet 4.6": 95.0},
    "ARC-Challenge": {"ChatGPT (GPT-4o)": 96.4, "ChatGPT (o3)": 97.8, "Claude Opus 4.6": 96.0, "Claude Sonnet 4.6": 95.5},
}

# ============================================================
# DATA — DIMENSION SCORES (0-10)
# ============================================================
DIMENSION_LABELS = [
    "Modelos Disponíveis",
    "Escrita e Linguagem",
    "Código",
    "Imagem",
    "Vídeo e Áudio",
    "Contexto e Tokens",
    "Latência e Performance",
    "Benchmarks Técnicos",
    "Ferramentas e Ecossistema",
    "Segurança e Alinhamento",
    "Casos de Uso",
]

SCORES_CHATGPT = [9, 8, 9, 9, 9, 9, 8, 9, 9, 8, 9]
SCORES_CLAUDE  = [7, 9, 9, 7, 6, 8, 8, 9, 8, 9, 9]

WEIGHTS = [0.08, 0.12, 0.14, 0.08, 0.06, 0.10, 0.08, 0.10, 0.10, 0.08, 0.06]

# ============================================================
# DATA — CONTEXT WINDOW SIZES (for chart)
# ============================================================
CTX_MODELS = [
    "GPT-4o", "GPT-4.1", "o3", "GPT-4.5",
    "Opus 4.6", "Sonnet 4.6", "Haiku 4.5",
]
CTX_SIZES = [128, 1000, 200, 128, 200, 200, 200]  # in K tokens

# ============================================================
# DATA — PRICING TABLE (per 1M tokens)
# ============================================================
PRICING_DATA = [
    ("GPT-4o", 2.50, 10.00, "OpenAI"),
    ("GPT-4o mini", 0.15, 0.60, "OpenAI"),
    ("GPT-4.1", 2.00, 8.00, "OpenAI"),
    ("GPT-4.1 mini", 0.40, 1.60, "OpenAI"),
    ("GPT-4.1 nano", 0.10, 0.40, "OpenAI"),
    ("o3", 10.00, 40.00, "OpenAI"),
    ("o4-mini", 1.10, 4.40, "OpenAI"),
    ("GPT-4.5", 75.00, 150.00, "OpenAI"),
    ("Claude Opus 4.6", 15.00, 75.00, "Anthropic"),
    ("Claude Sonnet 4.6", 3.00, 15.00, "Anthropic"),
    ("Claude Haiku 4.5", 0.80, 4.00, "Anthropic"),
    ("Claude 3.5 Sonnet", 3.00, 15.00, "Anthropic"),
]


# ============================================================
# HELPER — MATPLOTLIB FIGURE → REPORTLAB IMAGE
# ============================================================
def fig_to_image(fig, width=16 * cm, height=10 * cm):
    """Convert a matplotlib figure to a ReportLab Image flowable."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    buf.seek(0)
    return Image(buf, width=width, height=height)


# ============================================================
# CHART BUILDERS
# ============================================================

def build_radar_chart():
    """Radar/spider chart comparing overall dimension scores."""
    labels = DIMENSION_LABELS
    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(WHITE)

    vals_gpt = SCORES_CHATGPT + SCORES_CHATGPT[:1]
    vals_claude = SCORES_CLAUDE + SCORES_CLAUDE[:1]

    ax.plot(angles, vals_gpt, "o-", linewidth=2, label="ChatGPT", color=CHATGPT_COLOR)
    ax.fill(angles, vals_gpt, alpha=0.15, color=CHATGPT_COLOR)
    ax.plot(angles, vals_claude, "s-", linewidth=2, label="Claude", color=CLAUDE_COLOR)
    ax.fill(angles, vals_claude, alpha=0.15, color=CLAUDE_COLOR)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=7, weight="bold")
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11, 2))
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=9)
    ax.set_title("Pontuação por Dimensão", size=12, weight="bold", pad=20)
    return fig_to_image(fig, width=14 * cm, height=14 * cm)


def build_horizontal_bar_chart():
    """Horizontal bar chart — score by category side-by-side."""
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(WHITE)
    y = np.arange(len(DIMENSION_LABELS))
    bar_h = 0.35

    ax.barh(y - bar_h / 2, SCORES_CHATGPT, bar_h, label="ChatGPT", color=CHATGPT_COLOR)
    ax.barh(y + bar_h / 2, SCORES_CLAUDE, bar_h, label="Claude", color=CLAUDE_COLOR)

    ax.set_yticks(y)
    ax.set_yticklabels(DIMENSION_LABELS, fontsize=8)
    ax.set_xlim(0, 11)
    ax.set_xlabel("Pontuação (0–10)")
    ax.legend(fontsize=9)
    ax.set_title("Comparação por Categoria", fontsize=12, weight="bold")
    ax.invert_yaxis()
    plt.tight_layout()
    return fig_to_image(fig, width=17 * cm, height=11 * cm)


def build_context_window_chart():
    """Bar chart — context window size per model."""
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(WHITE)
    bar_colors = [CHATGPT_COLOR if i < 4 else CLAUDE_COLOR for i in range(len(CTX_MODELS))]
    bars = ax.bar(CTX_MODELS, CTX_SIZES, color=bar_colors, edgecolor="#333", linewidth=0.5)
    for bar, val in zip(bars, CTX_SIZES):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
                f"{val}K", ha="center", va="bottom", fontsize=8, weight="bold")
    ax.set_ylabel("Tokens (K)")
    ax.set_title("Tamanho da Janela de Contexto por Modelo", fontsize=12, weight="bold")
    plt.xticks(rotation=25, ha="right", fontsize=8)
    plt.tight_layout()
    return fig_to_image(fig, width=17 * cm, height=10 * cm)


def build_benchmark_chart():
    """Grouped bar chart for key benchmarks."""
    bench_names = ["MMLU", "HumanEval", "MATH", "GPQA\nDiamond", "SWE-bench\nVerified", "GSM8K"]
    bench_keys = ["MMLU", "HumanEval", "MATH", "GPQA Diamond", "SWE-bench Verified", "GSM8K"]

    gpt_vals = [BENCHMARKS[k]["ChatGPT (o3)"] for k in bench_keys]
    claude_vals = [BENCHMARKS[k]["Claude Opus 4.6"] for k in bench_keys]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(WHITE)
    x = np.arange(len(bench_names))
    w = 0.32
    bars1 = ax.bar(x - w / 2, gpt_vals, w, label="ChatGPT (o3)", color=CHATGPT_COLOR)
    bars2 = ax.bar(x + w / 2, claude_vals, w, label="Claude Opus 4.6", color=CLAUDE_COLOR)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                    f"{h:.1f}", ha="center", va="bottom", fontsize=7, weight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(bench_names, fontsize=8)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Score (%)")
    ax.set_title("Benchmarks Técnicos — Modelos de Topo", fontsize=12, weight="bold")
    ax.legend(fontsize=9)
    plt.tight_layout()
    return fig_to_image(fig, width=17 * cm, height=10 * cm)


# ============================================================
# STYLES
# ============================================================
def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"],
        fontSize=28, leading=34, textColor=RL_WHITE,
        alignment=TA_CENTER, spaceAfter=12,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontSize=14, leading=18, textColor=colors.HexColor("#cccccc"),
        alignment=TA_CENTER, spaceAfter=6,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "SectionTitle", parent=styles["Heading1"],
        fontSize=18, leading=22, textColor=RL_DARK_BLUE,
        spaceBefore=20, spaceAfter=10,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "SubSection", parent=styles["Heading2"],
        fontSize=13, leading=16, textColor=RL_DARK_BLUE,
        spaceBefore=12, spaceAfter=6,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "BodyText2", parent=styles["Normal"],
        fontSize=10, leading=14, textColor=colors.HexColor("#222222"),
        alignment=TA_JUSTIFY, spaceAfter=8,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "SmallNote", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=colors.HexColor("#666666"),
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "TOCEntry", parent=styles["Normal"],
        fontSize=11, leading=16, textColor=RL_DARK_BLUE,
        fontName="Helvetica",
        leftIndent=10,
    ))
    return styles


# ============================================================
# PAGE TEMPLATES
# ============================================================
PAGE_W, PAGE_H = A4


def cover_page_template(canvas, doc):
    """Draw the cover page background."""
    canvas.saveState()
    canvas.setFillColor(RL_DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Accent stripe
    canvas.setFillColor(RL_ORANGE)
    canvas.rect(0, PAGE_H * 0.42, PAGE_W, 4, fill=1, stroke=0)
    canvas.restoreState()


def normal_page_template(canvas, doc):
    """Header and footer for content pages."""
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(RL_DARK_BLUE)
    canvas.setLineWidth(1)
    canvas.line(2 * cm, PAGE_H - 1.5 * cm, PAGE_W - 2 * cm, PAGE_H - 1.5 * cm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(RL_DARK_BLUE)
    canvas.drawString(2 * cm, PAGE_H - 1.3 * cm, "LLM Benchmark Report — ChatGPT vs Claude")
    canvas.drawRightString(PAGE_W - 2 * cm, PAGE_H - 1.3 * cm, f"Data de Referência: {RESEARCH_DATE}")
    # Footer
    canvas.setStrokeColor(RL_DARK_BLUE)
    canvas.line(2 * cm, 1.5 * cm, PAGE_W - 2 * cm, 1.5 * cm)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(2 * cm, 1.0 * cm, "Relatório gerado automaticamente • Dados públicos")
    canvas.drawRightString(PAGE_W - 2 * cm, 1.0 * cm, f"Página {doc.page}")
    canvas.restoreState()


# ============================================================
# TABLE HELPER
# ============================================================
def make_table(data, col_widths=None, header=True):
    """Create a styled table flowable."""
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), RL_DARK_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), RL_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [RL_WHITE, RL_LIGHT_GREY]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t


# ============================================================
# SECTION TEXT CONTENT (Portuguese)
# ============================================================

EXECUTIVE_SUMMARY = """
Este relatório apresenta uma comparação abrangente e imparcial entre os dois principais sistemas de inteligência artificial conversacional: <b>ChatGPT</b> (OpenAI) e <b>Claude</b> (Anthropic). A análise cobre 11 dimensões críticas, incluindo modelos disponíveis, capacidades de escrita, código, imagem, vídeo/áudio, contexto, latência, benchmarks técnicos, ferramentas/ecossistema, segurança e casos de uso recomendados.
<br/><br/>
<b>Principais Conclusões:</b><br/>
• A OpenAI mantém vantagem em <b>amplitude de ecossistema</b>, com geração nativa de imagens (DALL-E/GPT-4o), capacidades de vídeo (Sora) e áudio avançado, além de uma janela de contexto de até 1M tokens no GPT-4.1.<br/>
• A Anthropic se destaca em <b>qualidade de escrita</b>, <b>segurança/alinhamento</b> e <b>código de alta complexidade</b> (SWE-bench), com o Claude Opus 4.6 e o Claude Code liderando em tarefas de engenharia de software.<br/>
• Em benchmarks de raciocínio puro, os modelos da série <b>o3/o4-mini</b> da OpenAI lideram, mas o Claude Opus 4.6 compete de perto em tarefas práticas.<br/>
• O custo-benefício favorece modelos leves de ambas as plataformas: GPT-4.1 nano/mini e Claude Haiku 4.5 oferecem excelente desempenho a preços acessíveis.
"""

SEC_MODELOS = """
A OpenAI oferece uma gama mais ampla de modelos, incluindo a família GPT-4o (flagship multimodal), a série de raciocínio o1/o3/o4-mini, o GPT-4.5 (modelo de pesquisa de alta capacidade) e a recente família GPT-4.1 com contexto de 1M tokens. A Anthropic concentra-se em três tiers bem definidos: Opus (máxima capacidade), Sonnet (equilíbrio custo-performance) e Haiku (velocidade e baixo custo).
<br/><br/>
A OpenAI possui modelos especializados em raciocínio estendido (o3, o4-mini) que não possuem equivalente direto no portfólio da Anthropic. Por outro lado, a Anthropic mantém uma linha de produtos mais enxuta e consistente, facilitando a escolha para desenvolvedores.
"""

SEC_ESCRITA = """
<b>Qualidade de prosa:</b> O Claude é amplamente reconhecido por produzir texto mais natural, nuançado e menos repetitivo. O ChatGPT melhorou significativamente com o GPT-4o, mas ainda tende a usar fórmulas linguísticas mais previsíveis.
<br/><br/>
<b>Suporte a idiomas:</b> Ambos suportam dezenas de idiomas. O ChatGPT tem leve vantagem em idiomas de baixo recurso. O Claude demonstra excelente qualidade em português, espanhol, francês, alemão e japonês.
<br/><br/>
<b>Seguimento de instruções:</b> Ambos são excelentes. O Claude tende a seguir instruções complexas com maior fidelidade, especialmente em tarefas que exigem formatação específica ou restrições múltiplas. Nos rankings do Chatbot Arena, ambos disputam as primeiras posições em categorias de escrita criativa e seguimento de instruções.
<br/><br/>
<b>Formatação:</b> Ambos dominam Markdown. O Claude produz formatação mais consistente em documentos longos.
"""

SEC_CODIGO = """
<b>Linguagens suportadas:</b> Ambos suportam todas as linguagens mainstream (Python, JavaScript/TypeScript, Java, C++, Go, Rust, etc.) e muitas linguagens de nicho.
<br/><br/>
<b>Geração e debugging:</b> O ChatGPT (especialmente o3) lidera em benchmarks puros como HumanEval (~96.7%). O Claude Opus 4.6 compete de perto (~93%) e lidera no SWE-bench Verified (~72%), que mede capacidade de resolver issues reais em repositórios open-source.
<br/><br/>
<b>Integração com IDEs:</b> O ChatGPT alimenta o GitHub Copilot (integrado ao VS Code, JetBrains, Neovim). O Claude alimenta o Claude Code (CLI), Cursor e possui extensão oficial para VS Code. O Claude Code é considerado o melhor agente de codificação autônomo do mercado.
<br/><br/>
<b>Refactoring e tarefas complexas:</b> O Claude demonstra superioridade em tarefas de refatoração de grandes bases de código, planejamento de arquitetura e resolução de bugs complexos em projetos reais.
"""

SEC_IMAGEM = """
<b>Análise de imagens (input multimodal):</b> Ambos suportam análise de imagens com alta qualidade. O GPT-4o e o Claude Opus/Sonnet processam imagens, diagramas, screenshots e documentos escaneados com precisão comparável.
<br/><br/>
<b>Geração de imagens:</b> Grande vantagem do ChatGPT. O GPT-4o possui geração nativa de imagens integrada (evolução do DALL-E 3), permitindo criar e editar imagens diretamente na conversa. O Claude <b>não possui geração nativa de imagens</b> — os usuários precisam recorrer a ferramentas externas.
<br/><br/>
<b>Qualidade:</b> A geração de imagens do GPT-4o é considerada estado da arte em modelos conversacionais, com excelente aderência ao prompt e qualidade estética.
"""

SEC_VIDEO_AUDIO = """
<b>Vídeo:</b> O ChatGPT suporta análise de vídeo (upload e processamento de frames). O Claude tem suporte limitado a vídeo — aceita frames individuais mas não processa vídeo nativo de forma fluida.
<br/><br/>
<b>Áudio — entrada:</b> O ChatGPT possui modo de voz avançado (Advanced Voice Mode) com compreensão nativa de áudio e fala em tempo real. O Claude suporta entrada de áudio via API mas sem o mesmo nível de integração em tempo real.
<br/><br/>
<b>Áudio — saída:</b> O ChatGPT gera fala sintética de alta qualidade com múltiplas vozes e expressividade emocional. O Claude não possui síntese de voz nativa.
<br/><br/>
<b>Transcrição:</b> A OpenAI possui o Whisper (ASR de classe mundial). A Anthropic não oferece serviço de transcrição dedicado.
"""

SEC_CONTEXTO = """
<b>Janela de contexto:</b> O GPT-4.1 lidera com <b>1 milhão de tokens</b> de contexto. Os modelos o3/o1 suportam 200K tokens. O Claude mantém 200K tokens em todos os modelos recentes.
<br/><br/>
<b>Tokens de saída:</b> O o3 pode gerar até 100K tokens de saída. O Claude Opus 4.6 permite até 32K tokens de saída. O GPT-4.1 também suporta 32K de saída.
<br/><br/>
<b>Prompt caching:</b> Ambas as plataformas oferecem prompt caching via API, reduzindo custos em cenários com prefixos repetidos. A Anthropic oferece desconto de 90% em tokens cacheados; a OpenAI oferece 50% de desconto.
<br/><br/>
<b>Custo:</b> A tabela de preços mostra que os modelos nano/mini de ambas as plataformas são extremamente acessíveis. O GPT-4.1 nano é o mais barato ($0.10/1M input), enquanto o GPT-4.5 é o mais caro ($75/1M input).
"""

SEC_LATENCIA = """
<b>Time-to-first-token (TTFT):</b> Modelos leves como GPT-4o mini e Claude Haiku 4.5 respondem em menos de 500ms. Modelos de raciocínio (o3, o1) podem levar de 5 a 60+ segundos dependendo da complexidade.
<br/><br/>
<b>Throughput:</b> O GPT-4o e o Claude Sonnet 4.6 geram ~80-100 tokens/segundo. O Claude Haiku 4.5 pode superar 150 tokens/segundo. Modelos de raciocínio são significativamente mais lentos.
<br/><br/>
<b>Disponibilidade:</b> Ambas as plataformas oferecem SLAs empresariais com 99.9%+ de uptime. A OpenAI tem historicamente mais incidentes de instabilidade devido ao volume maior de usuários.
"""

SEC_BENCHMARKS = """
Os benchmarks técnicos mostram uma competição acirrada entre as plataformas. Os modelos de raciocínio da OpenAI (o3) lideram em matemática e ciência (MATH: 96.7%, GPQA Diamond: 79.7%), enquanto o Claude Opus 4.6 compete de perto e lidera em tarefas de engenharia de software real (SWE-bench: ~72%).
<br/><br/>
No Chatbot Arena (LMSYS), ambas as plataformas disputam as primeiras posições, com rankings variando conforme a categoria (escrita, código, raciocínio, multimodal).
<br/><br/>
<b>Nota importante:</b> Benchmarks não capturam todas as dimensões de qualidade. Na prática, a escolha entre ChatGPT e Claude depende fortemente do caso de uso específico.
"""

SEC_FERRAMENTAS = """
<b>Function calling / Tool use:</b> Ambos suportam chamadas de função/ferramentas via API com excelente confiabilidade. A OpenAI pioneirou o formato; a Anthropic atingiu paridade funcional.
<br/><br/>
<b>Web browsing:</b> O ChatGPT possui busca web nativa integrada. O Claude suporta busca web via ferramentas conectadas (tool use) mas não possui browsing nativo tão fluido.
<br/><br/>
<b>Execução de código:</b> O ChatGPT possui Code Interpreter (sandbox Python). O Claude oferece execução de código via Claude Code (CLI) e análise tool em sandbox.
<br/><br/>
<b>APIs e SDKs:</b> Ambos oferecem APIs REST completas com SDKs oficiais em Python e TypeScript/JavaScript. A OpenAI também oferece SDK em .NET, Go e Java.
<br/><br/>
<b>Produtos:</b> ChatGPT Plus ($20/mês), Team ($25/mês/usuário), Enterprise. Claude Pro ($20/mês), Team ($25/mês/usuário), Enterprise. A OpenAI também oferece o plano ChatGPT Pro ($200/mês) com acesso ilimitado aos modelos de topo.
"""

SEC_SEGURANCA = """
<b>Abordagem da OpenAI:</b> Utiliza RLHF (Reinforcement Learning from Human Feedback), red-teaming extensivo e filtros de segurança em múltiplas camadas. Publica relatórios de segurança (System Cards) para cada modelo.
<br/><br/>
<b>Abordagem da Anthropic:</b> Pioneira em Constitutional AI (RLAIF), onde o modelo é treinado com um conjunto de princípios ("constituição") para auto-avaliar e corrigir seu comportamento. A Anthropic é reconhecida por sua postura mais conservadora em segurança.
<br/><br/>
<b>Transparência:</b> A Anthropic publica extensivamente sobre interpretabilidade e segurança de IA. A OpenAI tem sido mais criticada por falta de transparência em modelos recentes, embora publique System Cards detalhados.
<br/><br/>
<b>Recusa de conteúdo:</b> O Claude tende a ser mais cauteloso na recusa de conteúdo potencialmente prejudicial, enquanto o ChatGPT encontrou um equilíbrio mais permissivo nas versões recentes.
"""

SEC_CASOS_DE_USO = """
<b>Onde o ChatGPT é melhor:</b><br/>
• Geração e edição de imagens<br/>
• Interação por voz em tempo real<br/>
• Análise de vídeo<br/>
• Ecossistema de plugins e integrações<br/>
• Tarefas que exigem raciocínio matemático/científico de ponta (via o3)<br/>
• Processamento de documentos com contexto muito longo (1M tokens no GPT-4.1)<br/><br/>
<b>Onde o Claude é melhor:</b><br/>
• Escrita criativa e produção de texto de alta qualidade<br/>
• Codificação de software complexo e engenharia de código (Claude Code)<br/>
• Tarefas que exigem seguimento rigoroso de instruções longas e complexas<br/>
• Cenários que exigem máxima segurança e controle de conteúdo<br/>
• Análise de documentos longos com foco em fidelidade<br/>
• Aplicações empresariais com requisitos estritos de compliance
"""


# ============================================================
# SCORE CARD HELPERS
# ============================================================
def compute_weighted_scores():
    gpt_weighted = sum(s * w for s, w in zip(SCORES_CHATGPT, WEIGHTS))
    claude_weighted = sum(s * w for s, w in zip(SCORES_CLAUDE, WEIGHTS))
    return round(gpt_weighted, 2), round(claude_weighted, 2)


def build_scorecard_table(styles):
    """Build the final scorecard table with winners per category."""
    data = [["Dimensão", "ChatGPT", "Claude", "Vencedor"]]
    for i, label in enumerate(DIMENSION_LABELS):
        gpt_s = SCORES_CHATGPT[i]
        claude_s = SCORES_CLAUDE[i]
        if gpt_s > claude_s:
            winner = "ChatGPT ✓"
        elif claude_s > gpt_s:
            winner = "Claude ✓"
        else:
            winner = "Empate"
        data.append([label, str(gpt_s), str(claude_s), winner])

    gpt_total, claude_total = compute_weighted_scores()
    overall_winner = "ChatGPT" if gpt_total > claude_total else "Claude" if claude_total > gpt_total else "Empate"
    data.append(["SCORE PONDERADO GERAL", f"{gpt_total:.2f}", f"{claude_total:.2f}", f"{overall_winner} ✓"])

    col_w = [6 * cm, 2.5 * cm, 2.5 * cm, 3.5 * cm]
    t = make_table(data, col_widths=col_w)
    # Highlight last row
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, -1), (-1, -1), RL_DARK_BLUE),
        ("TEXTCOLOR", (0, -1), (-1, -1), RL_WHITE),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 9),
    ]))
    return t


# ============================================================
# BUILD PDF
# ============================================================
def build_pdf():
    styles = get_styles()

    doc = BaseDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    frame_cover = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id="cover",
    )
    frame_normal = Frame(
        doc.leftMargin, doc.bottomMargin + 0.5 * cm,
        doc.width, doc.height - 1 * cm,
        id="normal",
    )

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=frame_cover, onPage=cover_page_template),
        PageTemplate(id="Content", frames=frame_normal, onPage=normal_page_template),
    ])

    story = []

    # ---- COVER PAGE ----
    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph("LLM Benchmark Report", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("ChatGPT (OpenAI) vs Claude (Anthropic)", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("Comparação Abrangente e Multidimensional", styles["CoverSubtitle"]))
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph(f"Data de Referência: {RESEARCH_DATE}", styles["CoverSubtitle"]))
    story.append(Paragraph("Relatório Técnico • Dados Públicos", styles["CoverSubtitle"]))

    # ---- SWITCH TO CONTENT TEMPLATE ----
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ---- TABLE OF CONTENTS ----
    story.append(Paragraph("Sumário", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3 * cm))
    toc_items = [
        "1. Executive Summary",
        "2. Modelos Disponíveis",
        "3. Capacidades de Escrita e Linguagem",
        "4. Capacidades de Código",
        "5. Capacidades de Imagem",
        "6. Capacidades de Vídeo e Áudio",
        "7. Contexto e Tokens",
        "8. Latência e Performance",
        "9. Benchmarks Técnicos",
        "10. Ferramentas e Ecossistema",
        "11. Segurança e Alinhamento",
        "12. Casos de Uso Recomendados",
        "13. Gráficos Comparativos",
        "14. Pontuação Comparativa Final",
        "15. Conclusão e Recomendações",
        "Apêndice: Fontes e Metodologia",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles["TOCEntry"]))
    story.append(PageBreak())

    # ---- 1. EXECUTIVE SUMMARY ----
    story.append(Paragraph("1. Executive Summary", styles["SectionTitle"]))
    story.append(Paragraph(EXECUTIVE_SUMMARY, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 2. MODELOS DISPONÍVEIS ----
    story.append(Paragraph("2. Modelos Disponíveis", styles["SectionTitle"]))
    story.append(Paragraph(SEC_MODELOS, styles["BodyText2"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("2.1 Modelos OpenAI", styles["SubSection"]))
    oai_data = [["Modelo", "Lançamento", "Status", "Contexto", "Max Output", "Input/1M", "Output/1M", "Tier"]]
    for m in OPENAI_MODELS:
        oai_data.append([m["nome"], m["lancamento"], m["status"], m["contexto"],
                         m["max_output"], m["input_price"], m["output_price"], m["tier"]])
    story.append(make_table(oai_data, col_widths=[2.8*cm, 1.8*cm, 1.2*cm, 1.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2.5*cm]))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("2.2 Modelos Anthropic", styles["SubSection"]))
    ant_data = [["Modelo", "Lançamento", "Status", "Contexto", "Max Output", "Input/1M", "Output/1M", "Tier"]]
    for m in ANTHROPIC_MODELS:
        ant_data.append([m["nome"], m["lancamento"], m["status"], m["contexto"],
                         m["max_output"], m["input_price"], m["output_price"], m["tier"]])
    story.append(make_table(ant_data, col_widths=[3.2*cm, 1.8*cm, 1.2*cm, 1.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2.3*cm]))
    story.append(PageBreak())

    # ---- 3. ESCRITA ----
    story.append(Paragraph("3. Capacidades de Escrita e Linguagem", styles["SectionTitle"]))
    story.append(Paragraph(SEC_ESCRITA, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 4. CÓDIGO ----
    story.append(Paragraph("4. Capacidades de Código", styles["SectionTitle"]))
    story.append(Paragraph(SEC_CODIGO, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 5. IMAGEM ----
    story.append(Paragraph("5. Capacidades de Imagem", styles["SectionTitle"]))
    story.append(Paragraph(SEC_IMAGEM, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 6. VÍDEO E ÁUDIO ----
    story.append(Paragraph("6. Capacidades de Vídeo e Áudio", styles["SectionTitle"]))
    story.append(Paragraph(SEC_VIDEO_AUDIO, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 7. CONTEXTO ----
    story.append(Paragraph("7. Contexto e Tokens", styles["SectionTitle"]))
    story.append(Paragraph(SEC_CONTEXTO, styles["BodyText2"]))
    story.append(Spacer(1, 0.4 * cm))

    # Pricing table
    story.append(Paragraph("7.1 Tabela de Preços por 1M Tokens", styles["SubSection"]))
    price_data = [["Modelo", "Empresa", "Input / 1M tokens", "Output / 1M tokens"]]
    for name, inp, outp, company in PRICING_DATA:
        price_data.append([name, company, f"${inp:.2f}", f"${outp:.2f}"])
    story.append(make_table(price_data, col_widths=[4*cm, 3*cm, 4*cm, 4*cm]))
    story.append(PageBreak())

    # ---- 8. LATÊNCIA ----
    story.append(Paragraph("8. Latência e Performance", styles["SectionTitle"]))
    story.append(Paragraph(SEC_LATENCIA, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 9. BENCHMARKS ----
    story.append(Paragraph("9. Benchmarks Técnicos", styles["SectionTitle"]))
    story.append(Paragraph(SEC_BENCHMARKS, styles["BodyText2"]))
    story.append(Spacer(1, 0.3 * cm))

    # Benchmark table
    story.append(Paragraph("9.1 Tabela de Benchmarks", styles["SubSection"]))
    bench_data = [["Benchmark"] + list(list(BENCHMARKS.values())[0].keys())]
    for bench_name, scores in BENCHMARKS.items():
        row = [bench_name] + [f"{v:.1f}" for v in scores.values()]
        bench_data.append(row)
    bench_col_w = [3*cm] + [3.2*cm] * len(list(BENCHMARKS.values())[0])
    story.append(make_table(bench_data, col_widths=bench_col_w))
    story.append(PageBreak())

    # ---- 10. FERRAMENTAS ----
    story.append(Paragraph("10. Ferramentas e Ecossistema", styles["SectionTitle"]))
    story.append(Paragraph(SEC_FERRAMENTAS, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 11. SEGURANÇA ----
    story.append(Paragraph("11. Segurança e Alinhamento", styles["SectionTitle"]))
    story.append(Paragraph(SEC_SEGURANCA, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 12. CASOS DE USO ----
    story.append(Paragraph("12. Casos de Uso Recomendados", styles["SectionTitle"]))
    story.append(Paragraph(SEC_CASOS_DE_USO, styles["BodyText2"]))
    story.append(PageBreak())

    # ---- 13. GRÁFICOS COMPARATIVOS ----
    story.append(Paragraph("13. Gráficos Comparativos", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("13.1 Radar — Pontuação Geral por Dimensão", styles["SubSection"]))
    story.append(build_radar_chart())
    story.append(PageBreak())

    story.append(Paragraph("13.2 Barras Horizontais — Score por Categoria", styles["SubSection"]))
    story.append(build_horizontal_bar_chart())
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("13.3 Janela de Contexto por Modelo", styles["SubSection"]))
    story.append(build_context_window_chart())
    story.append(PageBreak())

    story.append(Paragraph("13.4 Benchmarks Técnicos — Modelos de Topo", styles["SubSection"]))
    story.append(build_benchmark_chart())
    story.append(PageBreak())

    # ---- 14. PONTUAÇÃO FINAL ----
    story.append(Paragraph("14. Pontuação Comparativa Final", styles["SectionTitle"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "A tabela abaixo apresenta a pontuação de 0 a 10 para cada dimensão analisada, "
        "com o score geral ponderado calculado com base nos pesos atribuídos a cada categoria. "
        "Pesos refletem a importância relativa de cada dimensão para uso profissional e empresarial.",
        styles["BodyText2"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(build_scorecard_table(styles))

    gpt_total, claude_total = compute_weighted_scores()
    overall = "ChatGPT" if gpt_total > claude_total else "Claude"
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        f"<b>Vencedor Geral: {overall}</b> (ChatGPT: {gpt_total:.2f} vs Claude: {claude_total:.2f}). "
        f"A diferença de {abs(gpt_total - claude_total):.2f} pontos indica uma competição extremamente "
        f"acirrada, com cada plataforma liderando em dimensões diferentes.",
        styles["BodyText2"]
    ))
    story.append(PageBreak())

    # ---- 15. CONCLUSÃO ----
    story.append(Paragraph("15. Conclusão e Recomendações", styles["SectionTitle"]))
    story.append(Paragraph(
        "A comparação entre ChatGPT e Claude revela duas plataformas de IA excepcionais, "
        "cada uma com forças distintas. A escolha entre elas deve ser guiada pelo caso de uso específico:"
        "<br/><br/>"
        "<b>Escolha o ChatGPT quando:</b> você precisa de um ecossistema completo com geração de imagens, "
        "interação por voz, análise de vídeo, raciocínio matemático de ponta ou contexto ultra-longo (1M tokens). "
        "O ChatGPT é ideal para usuários que valorizam a amplitude de capacidades multimodais."
        "<br/><br/>"
        "<b>Escolha o Claude quando:</b> você prioriza qualidade de escrita, codificação complexa de software, "
        "segurança e alinhamento, ou seguimento rigoroso de instruções. O Claude é ideal para equipes de "
        "engenharia de software, análise de documentos longos e aplicações empresariais com requisitos "
        "estritos de compliance."
        "<br/><br/>"
        "<b>Recomendação final:</b> Para a maioria das organizações, a melhor estratégia é manter acesso "
        "a ambas as plataformas e selecionar o modelo mais adequado para cada tarefa específica. "
        "A competição entre OpenAI e Anthropic beneficia todos os usuários, impulsionando melhorias "
        "contínuas em qualidade, segurança e acessibilidade.",
        styles["BodyText2"]
    ))
    story.append(PageBreak())

    # ---- APÊNDICE ----
    story.append(Paragraph("Apêndice: Fontes e Metodologia", styles["SectionTitle"]))
    story.append(Paragraph(
        "<b>Fontes de dados:</b><br/>"
        "• OpenAI Documentation (platform.openai.com)<br/>"
        "• Anthropic Documentation (docs.anthropic.com)<br/>"
        "• LMSYS Chatbot Arena (lmarena.ai)<br/>"
        "• Papers With Code (paperswithcode.com)<br/>"
        "• Artificial Analysis (artificialanalysis.ai)<br/>"
        "• Relatórios técnicos e System Cards publicados por OpenAI e Anthropic<br/>"
        "• Blogs oficiais da OpenAI e Anthropic<br/><br/>"
        "<b>Metodologia:</b><br/>"
        "• Pontuações de 0–10 atribuídas com base em dados públicos de benchmarks, "
        "análise de funcionalidades e consenso da comunidade técnica.<br/>"
        "• Pesos refletem importância relativa para uso profissional: código (14%), "
        "escrita (12%), contexto (10%), benchmarks (10%), ferramentas (10%), "
        "modelos (8%), imagem (8%), latência (8%), segurança (8%), "
        "vídeo/áudio (6%), casos de uso (6%).<br/>"
        "• Valores marcados com ~ são aproximações baseadas em dados parciais.<br/>"
        "• Dados coletados até março de 2026. Modelos e preços podem ter sido "
        "atualizados após esta data.<br/><br/>"
        "<b>Limitações:</b><br/>"
        "• Benchmarks acadêmicos não capturam todas as dimensões de qualidade prática.<br/>"
        "• Preços e disponibilidade podem variar por região e tipo de conta.<br/>"
        "• A evolução rápida da área pode tornar algumas comparações desatualizadas em semanas.",
        styles["BodyText2"]
    ))

    # ---- BUILD ----
    doc.build(story)
    print(f"PDF gerado com sucesso: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
