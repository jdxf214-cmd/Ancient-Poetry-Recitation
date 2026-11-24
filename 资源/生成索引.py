# -*- coding: utf-8 -*-
"""校验各年级古诗词 JSON，并生成合订库、索引与 CSV 清单。"""
import json
import csv
import pathlib
from datetime import date

BASE = pathlib.Path(__file__).resolve().parent
GRADE_FILES = [BASE / f"古诗词-{g}年级.json" for g in ["一", "二", "三", "四", "五", "六"]]

poems = []
for path in GRADE_FILES:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["count"] != len(data["poems"]):
        raise SystemExit(f"{path.name} 声明数量 {data['count']} 与实际 {len(data['poems'])} 不符")
    poems.extend(data["poems"])

poems.sort(key=lambda p: p["id"])

ids = [p["id"] for p in poems]
if len(ids) != len(set(ids)):
    raise SystemExit("存在重复 id")
if ids != list(range(1, len(poems) + 1)):
    raise SystemExit("id 不是从 1 开始的连续编号")

required = ["id", "title", "dynasty", "author", "grade", "semester", "genre", "tags", "lines", "notes", "translation"]
for p in poems:
    missing = [k for k in required if k not in p]
    if missing:
        raise SystemExit(f"id={p.get('id')} 缺少字段：{missing}")
    if not p["lines"] or not p["notes"] or not p["translation"]:
        raise SystemExit(f"id={p['id']} 存在空内容")
    if p["semester"] not in ("上", "下"):
        raise SystemExit(f"id={p['id']} 册次异常：{p['semester']}")

grades = []
for g in range(1, 7):
    for sem in ("上", "下"):
        subset = [p for p in poems if p["grade"] == g and p["semester"] == sem]
        grades.append({"grade": g, "semester": sem, "count": len(subset)})

meta = {
    "name": "小学古诗词资源（统编版·人教部编版）",
    "version": "1.1",
    "updated": date.today().isoformat(),
    "scope": "小学语文 1-6 年级，共 112 首古诗词，按教材册次编排",
    "total": len(poems),
    "grades": grades,
    "fields": {
        "id": "全库唯一编号，1-112，按册次顺序",
        "title": "篇目名称，同名篇目括注首句",
        "dynasty": "朝代",
        "author": "作者，乐府或民歌注明出处",
        "grade": "年级 1-6",
        "semester": "册次：上 / 下",
        "genre": "体裁（五言绝句、七言绝句、词、乐府诗等）",
        "tags": "主题标签，用于筛选与推荐",
        "lines": "原文，按句拆分，保留标点",
        "notes": "注释，{w: 词语, t: 释义}，按教材课文注释点整理，含易错读音",
        "translation": "译文，按句拆分，参照人教社教师教学用书通行表述"
    },
    "pending": [
        "逐字拼音（拼音开关需要）",
        "范读音频与时长",
        "诗词配图 / 插画素材",
        "AI 评测用标准音频与评分维度",
        "教师端布置任务所需的分册单元信息"
    ],
    "review": "册次与原文依据统编版教材目录整理，注释按课文注释点整理，译文参照人教社教师教学用书通行表述；上线前请教研人员逐首复核。",
    "source": "参考人民教育出版社课程教材研究所电子教材（jc.pep.com.cn）语文各年级古诗词篇目；学生用书无逐首译文，译文按教师教学用书口径整理。",
    "files": {
        "全库": "古诗词-全库.json",
        "分年级": "古诗词-一年级.json ~ 古诗词-六年级.json",
        "索引": "古诗词-索引.json",
        "清单": "古诗词-清单.csv"
    }
}

(BASE / "古诗词-全库.json").write_text(
    json.dumps({"meta": meta, "poems": poems}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
(BASE / "古诗词-索引.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
)

with (BASE / "古诗词-清单.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["编号", "年级", "册次", "篇目", "朝代", "作者", "体裁", "主题", "首句", "注释数", "译文句数", "原文"])
    for p in poems:
        writer.writerow([
            p["id"], p["grade"], p["semester"], p["title"], p["dynasty"], p["author"],
            p["genre"], "、".join(p["tags"]), p["lines"][0],
            len(p["notes"]), len(p["translation"]), "".join(p["lines"]),
        ])

print(f"校验通过：{len(poems)} 首")
for item in grades:
    print(f"  {item['grade']}年级{item['semester']}册：{item['count']} 首")
