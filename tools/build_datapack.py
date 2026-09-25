#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_datapack.py - 用你合法持有的底稿，在本地构建可选深度数据包。

本工具**不下载任何内容**，也不包含任何原书正文：它只把你自己的 OCR 底稿
整理成数据包骨架，并按 spec/SPEC-蒸馏规范.md 生成待蒸馏清单。

依赖：仅 Python 3.8+ 标准库。

用法:
  python tools/build_datapack.py --sources <你的底稿目录> --out <数据包目录>
  python tools/build_datapack.py --sources ./my_ocr --out ./datapack --assets ./my_images \
      --bufyuan ./my_kb --tushuo ./my_tushuo
"""
import argparse, json, os, re, shutil, sys

MENLEI = {
    "相术":     ["01", "02", "03"],
    "八字":     ["09"],
    "紫微":     ["08"],
    "奇门风水": ["10"],
    "牌卜":     ["06", "07"],
    "姓名星相": ["04", "05"],
}
ALL_VOLS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
VOL_NAME = {
    "01": "手相", "02": "面相·血型", "03": "指纹占卜", "04": "十二支·姓名学·星相",
    "05": "易经与八卦·灵数占卜", "06": "吉普赛魔牌", "07": "扑克牌占卜",
    "08": "紫微斗数", "09": "四柱与八字", "10": "奇门遁甲·堪舆风水",
}


def main():
    ap = argparse.ArgumentParser(description="构建可选深度数据包骨架（不含任何原书正文）")
    ap.add_argument("--sources", required=True, help="你自己的 OCR 底稿目录（每册一个 .md）")
    ap.add_argument("--out", required=True, help="输出数据包目录")
    ap.add_argument("--assets", default="", help="可选：插图目录，将复制为 assets/")
    ap.add_argument("--bufyuan", default="", help="可选：补源档目录（形如 <门类>/补源-*.md），复制为 kb/ 下对应文件")
    ap.add_argument("--tushuo", default="", help="可选：图说档目录（图说-*.md），复制为 图说/")
    args = ap.parse_args()

    src, out = os.path.abspath(args.sources), os.path.abspath(args.out)
    if not os.path.isdir(src):
        print("错误：底稿目录不存在：%s" % src); return 2
    os.makedirs(out, exist_ok=True)

    found = {}
    for fn in sorted(os.listdir(src)):
        if not fn.endswith((".md", ".txt", ".markdown")):
            continue
        m = re.search(r"(\d{2})", fn)
        if m and m.group(1) in ALL_VOLS:
            found.setdefault(m.group(1), os.path.join(src, fn))
    print("在底稿目录中识别到 %d/%d 册：" % (len(found), len(ALL_VOLS)))
    for v in ALL_VOLS:
        print("   %s %-22s %s" % (v, VOL_NAME[v], "OK  " + os.path.basename(found[v]) if v in found else "** 缺失 **"))

    # 1) sources/
    sdst = os.path.join(out, "sources")
    os.makedirs(sdst, exist_ok=True)
    for v, p in found.items():
        shutil.copy2(p, os.path.join(sdst, "《世界相命全集》%s %s.md" % (v, VOL_NAME[v])))
    print("\nsources/ 已写入 %d 个底稿（仅本地，勿再分发）" % len(found))

    # 2) kb/<门类>/ 骨架
    for ml, vols in MENLEI.items():
        d = os.path.join(out, "kb", ml)
        os.makedirs(d, exist_ok=True)
        todo = ["# %s — 待蒸馏" % ml, "",
                "> 源册：%s" % "、".join("%s %s" % (v, VOL_NAME[v]) for v in vols), "",
                "按 `spec/SPEC-蒸馏规范.md` 产出两个文件：", "",
                "1. `_kernel.md` — 门类内核，**≤12,000 字符**，五节结构：",
                "   一、本门类是什么（判定范围）／二、判读规则表／三、查表／四、决策流程／五、常见问法→结论映射",
                "2. `%s-判读条目.md` — 无上限的逐条目深度资料，每条带 `（源：<册名> p.N）`" % ml, "",
                "标注纪律：三层（典籍记载／术数主张／推断 `^[inferred]`／存疑 `^[ambiguous]`），",
                "并把 OCR 可疑处登记到 `## 待核验`。**不得编造原书没有的规则或数值。**", "",
                "## 待处理源册", ""]
        for v in vols:
            todo.append("- [%s] %s %s" % ("x" if v in found else " ", v, VOL_NAME[v]))
        with open(os.path.join(d, "_TODO.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(todo) + "\n")

    # 3) spec / docs
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    for rel in ("spec/SPEC-蒸馏规范.md", "docs/OVERVIEW.md", "docs/PROVENANCE.md"):
        s = os.path.join(repo, rel.replace("/", os.sep))
        if os.path.isfile(s):
            d = os.path.join(out, *rel.split("/"))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
    print("kb/<门类>/_TODO.md 已为 %d 个门类生成" % len(MENLEI))
    print("spec/ 与 docs/ 已复制")

    # 4) assets (optional)
    if args.assets and os.path.isdir(args.assets):
        shutil.copytree(args.assets, os.path.join(out, "assets"), dirs_exist_ok=True)
        print("assets/ 已复制")

    # 5) kb/ 补源档（可选，由使用者提供）
    if args.bufyuan and os.path.isdir(args.bufyuan):
        n = 0
        for r, _d, ff in os.walk(args.bufyuan):
            for fn in ff:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(r, fn), args.bufyuan)
                dst = os.path.join(out, "kb", rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(r, fn), dst)
                n += 1
        print("kb/ 补源档已复制 %d 个" % n)

    # 6) 图说档（可选，由使用者提供）
    if args.tushuo and os.path.isdir(args.tushuo):
        shutil.copytree(args.tushuo, os.path.join(out, "图说"), dirs_exist_ok=True)
        print("图说/ 已复制")

    print("""
完成。接下来需要 **LLM 参与蒸馏**（本工具不联网、不含模型）：
  1. 打开 kb/<门类>/_TODO.md，按清单逐门类蒸馏
  2. 以各源册底稿为输入，按 spec/SPEC-蒸馏规范.md 产出 _kernel.md 与 <门类>-判读条目.md
  3. 蒸馏完成后，用 install 脚本带 --datapack-root 重新安装 agent，占位符即指向本数据包

数据包只是**加深**层：即使不产出，agent 也能仅凭自带内核完成门类判读。""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
