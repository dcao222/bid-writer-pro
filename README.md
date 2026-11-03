# bid-writer-pro · 投标/标书写作助手

一个面向招投标场景的标书写作辅助工具：内置常用标书模板（投标函、法定代表人授权书、商务报价表、技术方案大纲等），
通过结构化数据一键生成规范化的 Word（.docx）标书文档，减少重复排版与手工套模板的工作量。

## 功能特性

- 📄 基于 `python-docx` 生成规范 Word 标书
- 🧩 内置多套常用模板，支持自定义扩展
- 🛠 命令行（CLI）交互：`list-templates` / `generate`
- 🔌 结构化输入（YAML / JSON），便于和现有业务系统对接
- ⚙️ 自带 `install.py --auto` 一键安装依赖

## 目录结构

```
bid-writer-pro/
├── README.md
├── requirements.txt        # 运行依赖
├── install.py              # 一键安装脚本（--auto）
├── src/
│   └── bid_writer_pro/
│       ├── __init__.py     # 版本号
│       ├── cli.py          # 命令行入口
│       ├── templates.py    # 内置标书模板
│       └── generator.py    # 文档生成核心
└── tests/
    └── test_basic.py       # 基础冒烟测试
```

## 安装

```bash
pip install -r requirements.txt
# 或一键安装
python install.py --auto
```

## 使用

列出所有可用模板：

```bash
python -m bid_writer_pro.cli list-templates
```

生成一份投标函（示例数据）：

```bash
python -m bid_writer_pro.cli generate \
  --template 投标函 \
  --output 投标函.docx \
  --set bidder="某某科技有限公司" \
  --set project="智慧林业平台建设项目" \
  --set amount="壹佰贰拾万元整" \
  --set owner="大理州林业和草原局" \
  --set date="2026-11-03"
```

也可从 YAML 文件读取结构化数据：

```bash
python -m bid_writer_pro.cli generate --template 投标函 --output 投标函.docx --file spec.yaml
```

`spec.yaml` 示例：

```yaml
bidder: 某某科技有限公司
project: 智慧林业平台建设项目
amount: 壹佰贰拾万元整
owner: 大理州林业和草原局
date: 2026-11-03
```

## 开发

```bash
pip install -r requirements.txt
python -m pytest tests/ -q
```

## 许可证

内部工具，许可证待定。
