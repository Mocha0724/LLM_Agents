#!/usr/bin/env python3
"""Generate a literature progress report PDF from structured JSON data.

Usage:
    python generate_report.py \
        --topic "世界模型" \
        --timeframe "2026-04-21 ~ 2026-04-28" \
        --input research_data.json \
        --output "文献进展报告.pdf"
"""

import argparse
import json
import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, BaseDocTemplate,
    Frame, PageTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Register Chinese Fonts ──────────────────────────────────────────
# STHeiti Medium is used for regular Chinese text
# STHeiti Light is used for lighter-weight Chinese text
pdfmetrics.registerFont(TTFont('STHeitiMedium', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('STHeitiLight', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=0))
CN_FONT = 'STHeitiMedium'
CN_FONT_LIGHT = 'STHeitiLight'

# ── Color Palette ──────────────────────────────────────────────────────

PRIMARY = HexColor("#1a1a2e")
ACCENT = "#16213e"
ACCENT_COLOR = HexColor("#16213e")
HIGHLIGHT = HexColor("#0f3460")
LIGHT_BG = HexColor("#f0f4f8")
DIVIDER = "#e0e6ed"
TEXT_DARK = "#2d3748"
TEXT_MEDIUM = "#4a5568"
TEXT_LIGHT = "#718096"
PAPER_TITLE = "#1a365d"
CHIP_BG = HexColor("#ebf4ff")
CHIP_TEXT = "#2b6cb0"


# ── Styles ─────────────────────────────────────────────────────────────

def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverTitle", fontName=CN_FONT, fontSize=26,
        leading=34, textColor=white, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle", fontName=CN_FONT_LIGHT, fontSize=14,
        leading=20, textColor=HexColor("#cbd5e1"), alignment=TA_CENTER, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "SectionTitle", fontName=CN_FONT, fontSize=18,
        leading=24, textColor=PRIMARY, spaceBefore=20, spaceAfter=12,
        borderPadding=(0, 0, 4, 0)
    ))
    styles.add(ParagraphStyle(
        "SubSectionTitle", fontName=CN_FONT, fontSize=14,
        leading=18, textColor=ACCENT_COLOR, spaceBefore=14, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "PaperTitle", fontName=CN_FONT, fontSize=12,
        leading=16, textColor=PAPER_TITLE, spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "PaperMeta", fontName=CN_FONT_LIGHT, fontSize=9,
        leading=12, textColor=TEXT_LIGHT, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "BodyCN", fontName=CN_FONT, fontSize=10,
        leading=16, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=6,
        wordWrap="CJK"
    ))
    styles.add(ParagraphStyle(
        "BodyEN", fontName="Helvetica", fontSize=9,
        leading=13, textColor=TEXT_MEDIUM, alignment=TA_JUSTIFY, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "Label", fontName=CN_FONT, fontSize=9,
        leading=13, textColor=TEXT_MEDIUM
    ))
    styles.add(ParagraphStyle(
        "TrendItem", fontName=CN_FONT, fontSize=10,
        leading=16, textColor=TEXT_DARK, leftIndent=16, spaceAfter=4,
        bulletIndent=0
    ))
    styles.add(ParagraphStyle(
        "OutlookText", fontName=CN_FONT, fontSize=10,
        leading=16, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=6,
        wordWrap="CJK"
    ))
    styles.add(ParagraphStyle(
        "FooterStyle", fontName=CN_FONT_LIGHT, fontSize=8,
        leading=10, textColor=TEXT_LIGHT, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        "SummaryText", fontName=CN_FONT, fontSize=10.5,
        leading=17, textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceAfter=8,
        wordWrap="CJK"
    ))
    return styles


# ── Page Template ──────────────────────────────────────────────────────

class LiteratureReport(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        self._cover_drawn = False
        super().__init__(filename, **kwargs)
        frame = Frame(
            2.2*cm, 2.2*cm, self.width - 4.4*cm, self.height - 4.4*cm,
            id="normal"
        )
        self.addPageTemplates([
            PageTemplate(id="main", frames=frame)
        ])

    def handle_pageBegin(self):
        super().handle_pageBegin()
        if not self._cover_drawn:
            self._cover_drawn = True
            self._draw_cover(self.canv)
        else:
            self._draw_footer(self.canv)

    def _draw_cover(self, c):
        c.saveState()
        w, h = A4
        c.setFillColor(PRIMARY)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(HIGHLIGHT)
        c.rect(0, h * 0.35, w, 4, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#ffffff"))
        c.setLineWidth(0.5)
        c.setDash(4, 4)
        c.line(3*cm, h*0.55, w - 3*cm, h*0.55)
        c.restoreState()

    def _draw_footer(self, c):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor(TEXT_LIGHT))
        c.drawCentredString(
            A4[0] / 2, 1.2*cm,
            f"— {self.page} —"
        )
        c.restoreState()


# ── Helpers ────────────────────────────────────────────────────────────

def make_chip(text, styles):
    """Render a small tag/badge element."""
    return Paragraph(f'<font color="{CHIP_TEXT}"><b>{text}</b></font>',
                     ParagraphStyle("chip", fontSize=8, leading=12,
                                    backColor=CHIP_BG,
                                    borderPadding=(2, 6, 2, 6),
                                    spaceAfter=4))


def safe_para(text, style):
    """Create a Paragraph, handling None properly."""
    return Paragraph(text or "", style)


def build_cover_story(data, styles):
    """Build cover page elements."""
    story = []

    story.append(Spacer(1, 6*cm))
    story.append(Paragraph("📄 文献进展报告", styles["CoverTitle"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(data.get("topic", ""), styles["CoverSubtitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f'<font color="#94a3b8" size=11>{data.get("topic_en", "")}</font>',
        styles["CoverSubtitle"]
    ))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(
        f'<font color="#94a3b8" size=11>时间范围：{data.get("timeframe", "")}</font>',
        styles["CoverSubtitle"]
    ))
    story.append(Paragraph(
        f'<font color="#94a3b8" size=11>报告日期：{data.get("report_date", datetime.now().strftime("%Y-%m-%d"))}</font>',
        styles["CoverSubtitle"]
    ))

    story.append(PageBreak())
    return story


# ── Section Builders ───────────────────────────────────────────────────

def build_executive_summary(data, styles):
    story = []
    story.append(Paragraph("1  执行摘要", styles["SectionTitle"]))
    story.append(Spacer(1, 4))
    # Divider line
    story.append(Paragraph(
        f'<hr color="{DIVIDER}" width="100%" />',
        ParagraphStyle("hr", fontSize=1, leading=1, spaceAfter=8)
    ))
    summary = data.get("summary_zh", "暂无摘要信息。")
    story.append(safe_para(summary, styles["SummaryText"]))
    story.append(Spacer(1, 6))

    # Stats summary
    papers = data.get("papers", [])
    stats_text = (
        f'<font color="{TEXT_MEDIUM}">'
        f'本期共收录 <b>{len(papers)}</b> 篇相关论文，涵盖 '
        f'<b>{len(data.get("trends", {}).get("hot_directions", []))}</b> 个热点方向。'
        f'</font>'
    )
    story.append(Paragraph(stats_text, styles["BodyCN"]))
    story.append(Spacer(1, 4))
    return story


def build_trend_analysis(data, styles):
    story = []
    story.append(Paragraph("2  趋势洞察", styles["SectionTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f'<hr color="{DIVIDER}" width="100%" />',
        ParagraphStyle("hr", fontSize=1, leading=1, spaceAfter=8)
    ))

    trends = data.get("trends", {})

    if trends.get("hot_directions"):
        story.append(Paragraph("热点方向", styles["SubSectionTitle"]))
        for d in trends["hot_directions"]:
            story.append(Paragraph(f"•  {d}", styles["TrendItem"]))
        story.append(Spacer(1, 6))

    if trends.get("method_trends"):
        story.append(Paragraph("方法趋势", styles["SubSectionTitle"]))
        for t in trends["method_trends"]:
            story.append(Paragraph(f"•  {t}", styles["TrendItem"]))
        story.append(Spacer(1, 6))

    if trends.get("key_breakthroughs"):
        story.append(Paragraph("关键突破", styles["SubSectionTitle"]))
        for b in trends["key_breakthroughs"]:
            story.append(Paragraph(f"•  {b}", styles["TrendItem"]))
        story.append(Spacer(1, 6))

    if trends.get("open_questions"):
        story.append(Paragraph("开放问题", styles["SubSectionTitle"]))
        for q in trends["open_questions"]:
            story.append(Paragraph(f"•  {q}", styles["TrendItem"]))

    return story


def build_paper_detail(paper, styles):
    """Build a single paper entry."""
    story = []

    # Paper number badge
    chip = make_chip(f"论文 #{paper['id']}", styles)
    story.append(chip)

    # Title
    story.append(Paragraph(paper.get("title", ""), styles["PaperTitle"]))
    story.append(Spacer(1, 2))

    # Meta info
    meta_parts = []
    if paper.get("authors"):
        meta_parts.append(f"作者：{paper['authors']}")
    if paper.get("venue"):
        meta_parts.append(f"来源：{paper['venue']}")
    if paper.get("date"):
        meta_parts.append(f"日期：{paper['date']}")
    story.append(Paragraph(" | ".join(meta_parts), styles["PaperMeta"]))
    story.append(Spacer(1, 4))

    # Core contribution (Chinese)
    story.append(Paragraph(
        f'<font color="{ACCENT}"><b>核心贡献</b></font>',
        styles["Label"]
    ))
    story.append(safe_para(paper.get("contribution_zh", ""), styles["BodyCN"]))

    # Method highlight (Chinese)
    if paper.get("method_zh"):
        story.append(Paragraph(
            f'<font color="{ACCENT}"><b>方法亮点</b></font>',
            styles["Label"]
        ))
        story.append(safe_para(paper["method_zh"], styles["BodyCN"]))

    # Relevance (Chinese)
    if paper.get("relevance_zh"):
        story.append(Paragraph(
            f'<font color="{ACCENT}"><b>意义评价</b></font>',
            styles["Label"]
        ))
        story.append(safe_para(paper["relevance_zh"], styles["BodyCN"]))

    # Abstract (English)
    if paper.get("abstract"):
        story.append(Spacer(1, 2))
        story.append(Paragraph(
            f'<font color="{TEXT_LIGHT}">'
            f'<i>Abstract: {paper["abstract"][:300]}'
            f'{"..." if len(paper["abstract"]) > 300 else ""}</i></font>',
            styles["BodyEN"]
        ))

    return story


def build_papers_section(data, styles):
    story = []
    story.append(Paragraph("3  论文详情", styles["SectionTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f'<hr color="{DIVIDER}" width="100%" />',
        ParagraphStyle("hr", fontSize=1, leading=1, spaceAfter=8)
    ))

    papers = data.get("papers", [])
    if not papers:
        story.append(Paragraph("本期未收录相关论文。", styles["BodyCN"]))
        return story

    for i, paper in enumerate(papers):
        entry = build_paper_detail(paper, styles)
        story.extend(entry)
        if i < len(papers) - 1:
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                f'<hr color="{DIVIDER}" width="60%" align="left" />',
                ParagraphStyle("hr-light", fontSize=1, leading=1, spaceAfter=4)
            ))
        story.append(Spacer(1, 6))

    return story


def build_outlook(data, styles):
    story = []
    story.append(Paragraph("4  总结与展望", styles["SectionTitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f'<hr color="{DIVIDER}" width="100%" />',
        ParagraphStyle("hr", fontSize=1, leading=1, spaceAfter=8)
    ))
    outlook = data.get("outlook_zh", "暂无总结信息。")
    story.append(safe_para(outlook, styles["OutlookText"]))
    story.append(Spacer(1, 2*cm))

    # Footer note
    story.append(Paragraph(
        f'<font color="{TEXT_LIGHT}" size=8>'
        f'本报告由 AI 自动生成，论文信息来源于公开的 arXiv/会议论文库。'
        f'建议在引用前核实原始论文。</font>',
        styles["FooterStyle"]
    ))
    return story


# ── Main Builder ───────────────────────────────────────────────────────

def generate_report(data, output_path):
    """Generate the full PDF report."""
    doc = LiteratureReport(
        output_path, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title=f"文献进展报告 - {data.get('topic', '')}",
        author="AI Literature Tracker",
    )

    styles = build_styles()

    # Build content
    story = []

    # Cover page (handled by onFirstPage)
    story.extend(build_cover_story(data, styles))

    # Section 1: Executive Summary
    story.extend(build_executive_summary(data, styles))

    # Section 2: Trend Analysis
    story.extend(build_trend_analysis(data, styles))

    # Section 3: Papers
    story.extend(build_papers_section(data, styles))

    # Section 4: Outlook
    story.extend(build_outlook(data, styles))

    # Build with cover page callback
    doc.build(story)
    return output_path


# ── CLI ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="生成文献进展报告 PDF"
    )
    parser.add_argument("--topic", required=True, help="研究主题（中文）")
    parser.add_argument("--timeframe", required=True, help="时间范围")
    parser.add_argument("--input", required=True, help="输入 JSON 数据文件路径")
    parser.add_argument("--output", default=None, help="输出 PDF 文件路径")
    args = parser.parse_args()

    # Load data
    if not os.path.exists(args.input):
        print(f"错误：输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Override topic/timeframe from CLI if provided
    if args.topic:
        data["topic"] = args.topic
    if args.timeframe:
        data["timeframe"] = args.timeframe

    # Default output path
    output = args.output
    if not output:
        date_str = datetime.now().strftime("%Y%m%d")
        safe_topic = args.topic.replace(" ", "_")
        output = f"文献进展报告_{safe_topic}_{date_str}.pdf"

    # Generate
    print(f"正在生成文献报告：{output}")
    result = generate_report(data, output)
    print(f"✓ 报告已生成：{result}")


if __name__ == "__main__":
    main()
