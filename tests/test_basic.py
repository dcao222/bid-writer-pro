"""bid-writer-pro 基础冒烟测试。"""
from pathlib import Path

from bid_writer_pro import generate, list_templates, get_template
from bid_writer_pro.cli import build_parser, _parse_set


def test_list_templates():
    names = list_templates()
    assert isinstance(names, list) and len(names) > 0
    assert "投标函" in names


def test_get_template_unknown():
    try:
        get_template("不存在的模板")
        assert False, "应当抛出 KeyError"
    except KeyError:
        pass


def test_generate_docx(tmp_path):
    out = tmp_path / "投标函.docx"
    path = generate(
        {"bidder": "测试公司", "project": "测试项目", "owner": "测试招标人"},
        "投标函",
        out,
    )
    assert path.exists() and path.suffix == ".docx"
    assert path.stat().st_size > 0


def test_parse_set():
    parsed = _parse_set(["a=1", "b=hello"])
    assert parsed == {"a": "1", "b": "hello"}


def test_cli_parser_build():
    parser = build_parser()
    args = parser.parse_args(["generate", "--template", "投标函", "--output", "x.docx"])
    assert args.template == "投标函"
    assert args.output == "x.docx"
