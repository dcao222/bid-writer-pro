"""标书文档生成核心：将结构化数据渲染为 Word(.docx)。"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from .templates import get_template


def _add_title(doc: Document, text: str) -> None:
    p = doc.add_heading(text, level=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def _render_block(doc: Document, block: Dict[str, Any], data: Dict[str, Any]) -> None:
    btype = block.get("type")
    if btype == "heading":
        doc.add_heading(block["text"].format(**data), level=block.get("level", 1))
    elif btype == "paragraph":
        p = doc.add_paragraph(block["text"].format(**data))
        if block.get("bold"):
            for run in p.runs:
                run.bold = True
    elif btype == "spacer":
        doc.add_paragraph("")
    elif btype == "table":
        headers = [h.format(**data) for h in block["headers"]]
        rows = block["rows"]
        table = doc.add_table(rows=1, cols=len(headers))
        try:
            table.style = "Light Grid Accent 1"
        except KeyError:
            pass
        hdr_cells = table.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
        for row in rows:
            cells = table.add_row().cells
            for i, val in enumerate(row):
                cells[i].text = str(val).format(**data)
    else:
        raise ValueError(f"不支持的 block 类型: {btype!r}")


def generate(
    spec: Dict[str, Any],
    template_name: str,
    output_path: str | Path,
) -> Path:
    """根据模板与数据生成 .docx 标书。

    Args:
        spec: 字段键值（会覆盖模板默认值）。
        template_name: 模板名称，见 templates.list_templates()。
        output_path: 输出 .docx 路径。

    Returns:
        实际写入的文件路径。
    """
    template = get_template(template_name)
    data: Dict[str, Any] = {**template.get("defaults", {}), **spec}

    doc = Document()
    _add_title(doc, template["title"].format(**data))
    for block in template["blocks"]:
        _render_block(doc, block, data)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    return out
