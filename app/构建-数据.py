# -*- coding: utf-8 -*-
"""从 资源/古诗词-全库.json 生成 app/data.js（应用内置数据，勿手改 data.js）。"""
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
SRC = BASE.parent / "资源" / "古诗词-全库.json"
OUT = BASE / "data.js"

data = json.loads(SRC.read_text(encoding="utf-8"))
poems = data["poems"]

out = "/* 自动生成：由 资源/古诗词-全库.json 生成，重新运行 构建-数据.py 可更新 */\n"
out += "var POEM_LIB = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
OUT.write_text(out, encoding="utf-8")

print(f"data.js 已生成：{len(poems)} 首，{OUT.stat().st_size // 1024} KB")
