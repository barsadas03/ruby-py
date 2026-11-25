#!/usr/bin/env python3
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "Custom CPython Extension Specification")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, footer_text)
        self.drawString(54, 32, "CPython Core Extension • Technical Brief")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    primary = colors.HexColor("#1E3A8A")
    secondary = colors.HexColor("#0284C7")
    text_dark = colors.HexColor("#0F172A")
    bg_box = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=secondary,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=text_dark,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=text_dark
    )

    meta_lbl = ParagraphStyle('ML', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=primary)
    meta_val = ParagraphStyle('MV', fontName='Helvetica', fontSize=8.5, leading=11, textColor=text_dark)

    story = []

    # Title & Metadata
    story.append(Paragraph("Custom CPython Engine: Core Built-ins", title_style))
    story.append(Paragraph("Native C Extensions & Dual-Access Architecture", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary, spaceAfter=8))

    meta_data = [
        [Paragraph("<b>Target Runtime:</b>", meta_lbl), Paragraph("CPython 3.16 dev (Core C layer)", meta_val),
         Paragraph("<b>Author:</b>", meta_lbl), Paragraph("Sanjoy Deb (Sanjoy-ui)", meta_val)],
        [Paragraph("<b>Upstream Source:</b>", meta_lbl), Paragraph("https://github.com/python/cpython", meta_val),
         Paragraph("<b>Custom Repo:</b>", meta_lbl), Paragraph("https://github.com/Sanjoy-ui/cpython", meta_val)]
    ]
    meta_t = Table(meta_data, colWidths=[90, 180, 80, 162])
    meta_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_box),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 6))

    # 1. Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "This project extends CPython at the core C implementation level. "
        "Unlike Python-level libraries, operations execute natively in C without bytecode overhead, "
        "interpreter frame allocation, or import latency. All capabilities support a <b>Dual-Access Model</b>: "
        "callable globally with zero imports (like <code>len()</code>), as native object methods (<code>'abc'.reverse()</code>), "
        "or via standard modules (<code>math.clamp()</code>, <code>string.reverse_str()</code>).",
        body_style
    ))

    # 2. Use Cases
    story.append(Paragraph("2. Capabilities & Use Cases", h1_style))
    use_cases_data = [
        [Paragraph("<b>Function</b>", meta_lbl), Paragraph("<b>Syntax</b>", meta_lbl), Paragraph("<b>Primary Use Case</b>", meta_lbl)],
        [Paragraph("<b>clamp</b>", code_style), Paragraph("<code>clamp(v, lo, hi)</code><br/><code>math.clamp(...)</code>", code_style), Paragraph("Bounding physics velocities, UI layout bounds, audio/sensor signals [0, 1], and RGB color ranges [0, 255].", body_style)],
        [Paragraph("<b>is_prime</b>", code_style), Paragraph("<code>is_prime(n)</code><br/><code>math.is_prime(...)</code>", code_style), Paragraph("Cryptographic key checks and hash table sizing via an optimized C 6k ± 1 primality algorithm.", body_style)],
        [Paragraph("<b>reverse_str</b>", code_style), Paragraph("<code>reverse_str(s)</code><br/><code>s.reverse()</code><br/><code>string.reverse_str(s)</code>", code_style), Paragraph("Bioinformatics (reverse complement sequences), NLP parsing, and palindrome verification with full Unicode/emoji support.", body_style)],
        [Paragraph("<b>inspect_obj</b>", code_style), Paragraph("<code>inspect_obj(obj)</code>", code_style), Paragraph("Low-level memory debugging: returns type, reference count (<code>Py_REFCNT</code>), size in bytes, and memory address.", body_style)],
        [Paragraph("<b>stats</b>", code_style), Paragraph("<code>stats(iterable)</code>", code_style), Paragraph("Streaming ETL: computes count, sum, min, max, and mean in a single pass without buffering collections.", body_style)]
    ]
    uc_t = Table(use_cases_data, colWidths=[75, 140, 297])
    uc_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0F2FE")),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(uc_t)
    story.append(Spacer(1, 6))

    # 3. How It Works
    story.append(Paragraph("3. How It Works", h1_style))
    story.append(Paragraph(
        "• <b>Python/bltinmodule.c:</b> Implemented C functions (<code>builtin_clamp</code>, <code>builtin_is_prime</code>, "
        "<code>builtin_reverse_str</code>, <code>builtin_inspect_obj</code>, <code>builtin_stats</code>) and registered them in "
        "<code>builtin_methods[]</code> to expose them globally in the root namespace.<br/>"
        "• <b>Objects/unicodeobject.c:</b> Implemented <code>unicode_reverse()</code> using direct C buffer operations "
        "(<code>PyUnicode_New</code>, <code>PyUnicode_WRITE</code>) and registered in <code>unicode_methods[]</code> as <code>.reverse()</code>.<br/>"
        "• <b>Modules/mathmodule.c:</b> Added <code>clamp</code> and <code>is_prime</code> into <code>math_methods[]</code> for standard modular access.<br/>"
        "• <b>Lib/string/__init__.py:</b> Added <code>reverse_str</code> to <code>__all__</code> for standard library parity.",
        body_style
    ))

    # Example block
    code_text = (
        "&gt;&gt;&gt; clamp(150, 0, 100), math.clamp(150, 0, 100)        # (100, 100)<br/>"
        "&gt;&gt;&gt; is_prime(997), math.is_prime(997)                    # (True, True)<br/>"
        "&gt;&gt;&gt; 'Python 🚀'.reverse(), string.reverse_str('CPython')   # ('🚀 nohtyP', 'nohtyPC')<br/>"
        "&gt;&gt;&gt; inspect_obj([1, 2])                                   # {'type': 'list', 'refcount': 1, ...}<br/>"
        "&gt;&gt;&gt; stats([10, 20, 30, 40])                               # {'count': 4, 'sum': 100.0, 'mean': 25.0, ...}"
    )
    code_t = Table([[Paragraph(code_text, code_style)]], colWidths=[512])
    code_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(code_t)
    story.append(Spacer(1, 6))

    # 4. Repository Links
    story.append(Paragraph("4. Repository Links", h1_style))
    repo_data = [
        [Paragraph("<b>Resource</b>", meta_lbl), Paragraph("<b>GitHub URL</b>", meta_lbl)],
        [Paragraph("<b>Main CPython Source Code</b>", meta_val), Paragraph("https://github.com/python/cpython", code_style)],
        [Paragraph("<b>Custom Implementation Repository</b>", meta_val), Paragraph("https://github.com/Sanjoy-ui/cpython", code_style)]
    ]
    repo_t = Table(repo_data, colWidths=[160, 352])
    repo_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(repo_t)
    story.append(Spacer(1, 6))

    # 5. Conclusion
    story.append(Paragraph("5. Conclusion", h1_style))
    story.append(Paragraph(
        "Extending CPython directly at the C core delivers maximum runtime execution speed while maintaining full language stability. "
        "The dual-access architecture combines developer convenience (zero-import global built-ins) with clean object-oriented semantics (<code>str.reverse()</code>) "
        "and modular standard library patterns (<code>math.clamp()</code>).",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated concise PDF: {filename}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "CPython_Custom_Builtins_Documentation.pdf"
    build_pdf(out_path)
