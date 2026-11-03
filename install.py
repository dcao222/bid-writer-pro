#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bid-writer-pro 一键安装脚本。

用法:
    python install.py --auto        # 自动安装 requirements.txt 中的依赖
    python install.py               # 显示帮助（交互式提示省略，直接安装）
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQ_FILE = HERE / "requirements.txt"


def install_requirements() -> int:
    if not REQ_FILE.exists():
        print(f"[错误] 未找到依赖文件: {REQ_FILE}")
        return 1
    print(f"[信息] 正在从 {REQ_FILE} 安装依赖 ...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)]
        )
    except subprocess.CalledProcessError as exc:
        print(f"[错误] 依赖安装失败: {exc}")
        return exc.returncode
    print("[完成] 依赖安装成功。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="bid-writer-pro 安装脚本")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="无需交互，直接安装依赖",
    )
    args = parser.parse_args()
    # 无论是否带 --auto，当前均执行依赖安装（保留参数以兼容原命令）
    _ = args.auto
    return install_requirements()


if __name__ == "__main__":
    raise SystemExit(main())
