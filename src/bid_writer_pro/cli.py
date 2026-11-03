"""bid-writer-pro 命令行入口。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    from rich.console import Console
    from rich.table import Table
    _console = Console()
    _rich = True
except ImportError:  # 未安装 rich 时降级为普通输出
    _rich = False

from .generator import generate
from .templates import list_templates


def _print_info(msg: str) -> None:
    if _rich:
        _console.print(f"[cyan]{msg}[/cyan]")
    else:
        print(msg)


def _print_ok(msg: str) -> None:
    if _rich:
        _console.print(f"[green]✔ {msg}[/green]")
    else:
        print(f"OK: {msg}")


def _print_err(msg: str) -> None:
    if _rich:
        _console.print(f"[red]✘ {msg}[/red]")
    else:
        print(f"ERROR: {msg}", file=sys.stderr)


def _parse_set(items: List[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"--set 参数格式应为 key=value，收到: {item!r}")
        key, val = item.split("=", 1)
        result[key.strip()] = val
    return result


def _load_file(path: str) -> Dict[str, Any]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            raise RuntimeError("读取 YAML 需要 PyYAML，请先 pip install PyYAML")
        return yaml.safe_load(text) or {}
    if p.suffix.lower() == ".json":
        import json
        return json.loads(text)
    raise ValueError(f"不支持的规格文件类型: {p.suffix}")


def cmd_list(args: argparse.Namespace) -> int:
    names = list_templates()
    if _rich:
        table = Table(title="可用标书模板")
        table.add_column("模板名称", style="bold")
        for n in names:
            table.add_row(n)
        _console.print(table)
    else:
        print("可用模板：")
        for n in names:
            print(f"  - {n}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    try:
        spec: Dict[str, Any] = {}
        if args.file:
            spec.update(_load_file(args.file))
        spec.update(_parse_set(args.set))

        out = generate(spec, args.template, args.output)
        _print_ok(f"已生成: {out}")
        return 0
    except Exception as exc:  # noqa: BLE001
        _print_err(str(exc))
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bid-writer-pro",
        description="投标/标书写作助手：基于模板生成 Word 标书",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-templates", help="列出所有可用模板")
    p_list.set_defaults(func=cmd_list)

    p_gen = sub.add_parser("generate", help="根据模板生成标书")
    p_gen.add_argument("--template", required=True, help="模板名称")
    p_gen.add_argument("--output", required=True, help="输出 .docx 路径")
    p_gen.add_argument("--set", action="append", default=[], help="字段赋值 key=value，可多次")
    p_gen.add_argument("--file", default=None, help="YAML/JSON 规格文件")
    p_gen.set_defaults(func=cmd_generate)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
