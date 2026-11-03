"""内置标书模板定义。

每个模板包含:
    title:  文档标题
    defaults: 字段默认值（缺省占位文本）
    blocks: 文档段落/表格的有序定义列表

block 支持的 type:
    heading   标题 (text, level)
    paragraph  段落 (text, bold?)
    table      表格 (headers, rows)
    spacer     空行
字段通过 Python str.format 注入，键来自 defaults 与运行时传入的 spec。
"""
from __future__ import annotations

from typing import Any, Dict

TEMPLATES: Dict[str, Dict[str, Any]] = {
    "投标函": {
        "title": "投 标 函",
        "defaults": {
            "bidder": "（投标人名称）",
            "project": "（项目名称）",
            "amount": "（投标总报价）",
            "owner": "（招标人）",
            "date": "（日期）",
        },
        "blocks": [
            {"type": "paragraph", "text": "致：{owner}", "bold": True},
            {"type": "spacer"},
            {"type": "paragraph", "text": "1. 我方已仔细研究了 {project} 招标文件的全部内容，愿意以人民币（大写）{amount} 的投标总报价，按合同约定实施和完成本项目，修补其任何缺陷。"},
            {"type": "paragraph", "text": "2. 我方承诺在投标有效期内不撤销投标文件，并随时准备接受贵方可能提出的澄清要求。"},
            {"type": "paragraph", "text": "3. 如我方中标，将严格按照招标文件及投标文件的承诺履约。"},
            {"type": "spacer"},
            {"type": "paragraph", "text": "投标人：{bidder}（盖章）"},
            {"type": "paragraph", "text": "法定代表人或其委托代理人：（签字）"},
            {"type": "paragraph", "text": "日期：{date}"},
        ],
    },
    "法定代表人授权书": {
        "title": "法定代表人授权书",
        "defaults": {
            "principal": "（法定代表人姓名）",
            "bidder": "（投标人名称）",
            "agent": "（被授权人姓名）",
            "idno": "（身份证号）",
            "date": "（日期）",
        },
        "blocks": [
            {"type": "paragraph", "text": "本人 {principal} 系 {bidder} 的法定代表人，现授权 {agent}（身份证号：{idno}）为我方代理人，以本公司名义办理招投标相关事宜。", "bold": False},
            {"type": "spacer"},
            {"type": "paragraph", "text": "代理人在授权范围内签署的一切文件和处理与之有关的一切事务，我公司均予以承认。"},
            {"type": "paragraph", "text": "委托期限：自本授权书签署之日起至本项目招投标活动结束止。"},
            {"type": "spacer"},
            {"type": "paragraph", "text": "法定代表人（签字或盖章）：{principal}"},
            {"type": "paragraph", "text": "投标人（盖章）：{bidder}"},
            {"type": "paragraph", "text": "日期：{date}"},
        ],
    },
    "商务报价表": {
        "title": "商务报价一览表",
        "defaults": {
            "project": "（项目名称）",
            "currency": "人民币（元）",
        },
        "blocks": [
            {"type": "paragraph", "text": "项目名称：{project}", "bold": True},
            {"type": "spacer"},
            {
                "type": "table",
                "headers": ["序号", "分项名称", "单位", "数量", "单价({currency})".format(currency="{currency}"), "合价({currency})".format(currency="{currency}"), "备注"],
                "rows": [
                    ["1", "（分项一）", "项", "1", "0.00", "0.00", "—"],
                    ["2", "（分项二）", "项", "1", "0.00", "0.00", "—"],
                    ["3", "（分项三）", "项", "1", "0.00", "0.00", "—"],
                ],
            },
            {"type": "spacer"},
            {"type": "paragraph", "text": "投标总报价（大写）：（金额）"},
        ],
    },
    "技术方案大纲": {
        "title": "技术方案",
        "defaults": {
            "project": "（项目名称）",
        },
        "blocks": [
            {"type": "heading", "text": "一、项目理解", "level": 1},
            {"type": "paragraph", "text": "结合 {project} 的建设目标，阐述对本项目的理解与总体思路。"},
            {"type": "heading", "text": "二、总体架构", "level": 1},
            {"type": "paragraph", "text": "描述系统总体技术架构、网络拓扑与部署方案。"},
            {"type": "heading", "text": "三、实施计划", "level": 1},
            {"type": "paragraph", "text": "列出里程碑、交付物与进度安排。"},
            {"type": "heading", "text": "四、质量与安全保障", "level": 1},
            {"type": "paragraph", "text": "说明质量控制措施、数据安全与运维保障方案。"},
        ],
    },
}


def get_template(name: str) -> Dict[str, Any]:
    if name not in TEMPLATES:
        raise KeyError(
            f"未知模板: {name!r}，可用模板: {list_templates()}"
        )
    return TEMPLATES[name]


def list_templates() -> list:
    return list(TEMPLATES.keys())
