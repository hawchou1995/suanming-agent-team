# 算命 agent 团队 · 神算子周半仙

一支**完全自包含**的中式命理术数 agent 团队：1 位主理人 + 6 个门类子代理 + 1 个典籍校勘代理。

按术数门类分工，主理人根据你的问题**自动分诊派单**——问手相派相术，问八字派八字，问风水派奇门风水，
跨门类问题（如「八字和手相一起看」）依次派单后综合，并如实呈现不同体系之间的分歧。

> **每一个 agent 的知识都已内化在其自身提示词里，运行时不检索任何外部资源。**
> 装完即可用，不需要联网、不需要 API key、不需要数据库、不需要 MCP。

---

## 一、30 秒装好

### 方式 A：装到支持的 agent 宿主（推荐）

```bash
git clone https://github.com/hawchou1995/suanming-agent-team.git
cd suanming-agent-team
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File install\install.ps1
```

macOS / Linux：

```bash
bash install/install.sh
```

装完**重启宿主**，即可看到 8 个 agent。默认装到 `~/.zcode/agents/`，可用参数改到别处：

```powershell
.\install\install.ps1 -TargetDir "D:\my\agents"
```

```bash
bash install/install.sh --target-dir ~/.claude/agents
```

### 方式 B：不想装、只想马上用（任意 LLM，零安装）

把 `install/prompt-template.md` 合并出的单文件提示词，**整段粘进任何大模型对话的系统提示词**即可。
主理人会把门类知识当作自己的知识作答。

---

## 二、装了什么

```
agents/                     8 个 agent 定义（每个都自带本门类内核知识）
  shensuanzi-zhoubanxian.md 主理人「神算子周半仙」——分诊、派单、综合
  xiangshu-master.md        相术：手相 / 面相·血型 / 指纹
  bazi-master.md            八字：四柱、五行、通变星、十二运星
  ziwei-master.md           紫微斗数：排盘、十二宫、星曜
  qimen-fengshui-master.md  奇门遁甲 · 堪舆风水
  paibu-master.md           牌卜：吉普赛魔牌 / 扑克牌
  xingming-master.md        姓名学 · 星相 · 十二支 · 灵数
  dianji-jiaokan.md         典籍校勘：出处回溯、OCR 可靠性判定
spec/SPEC-蒸馏规范.md        知识蒸馏与三层标注规范
docs/                       环境支持范围、验证步骤、可选数据包说明
install/                    安装脚本（Windows / macOS / Linux）+ 通用提示词模板
tools/build_datapack.py     可选：用你自己的底稿构建深度数据包
```

---

## 三、能做什么 / 不能做什么

**能做**：按门类做体系内判读（手相线纹、四柱排盘、紫微命盘、奇门局数、牌阵、姓名笔划、生肖、卦象…），
跨门类综合，说明各体系的边界与分歧，回答「这句出自哪一册」。

**不能做，且会如实告诉你**：
- **不臆造**。知识来自扫描件 OCR（实测字符错误率约 **5–10%**），凡可疑处标 `^[ambiguous]`，不假装读得懂。
- **不读插图**。原书插图在文本模型视角下不可见；若宿主没有视觉能力，agent 会明说「无法读图」。
- **不当事实**。所有输出都是**命理术数体系的主张**，不是经科学验证的结论。
- **不给确定性预测**，不判断生死、不诊断疾病、不预测灾祸，不提供医疗/投资/法律/婚姻决策建议。
- **不覆盖本套书以外的术数**（如西洋占星本命盘、正统塔罗牌义）——会说「本套书未涵盖」。

---

## 四、可选深度数据包（默认不装）

agent 自带的**内核**已足够完成门类判读。若你要更细的逐条目、逐表格深度资料，
可用**你自己**的底稿构建深度数据包：

```bash
python tools/build_datapack.py --help
```

详见 `docs/DATAPACK.md`。

> 本仓库**不附带任何原书正文、OCR 底稿或插图**——版权归原作者与出版方所有，见 `NOTICE.md`。

---

## 五、装完怎么确认能用

见 `docs/VERIFY.md`。最快的一条：装上后问

> 「用相术看看：感情线很长、末端分叉，怎么判？」

正确表现：主理人**分诊到相术**，子代理**引用内核里的判读规则**作答，并以体系口径表述（「手相學主張…」），
结尾带免责声明。若它反而去联网搜索或说「我需要查资料」，说明装错了。

---

## 六、支持环境

| 层级 | 环境 | 状态 |
|---|---|---|
| A | zcode / WorkBuddy 桌面（`~/.zcode/agents/`） | **已实测** |
| B | 任何接受 markdown+YAML agent 定义的宿主（Claude Code 等） | 格式兼容，需按宿主调整 frontmatter 键名 |
| C | 任意 LLM 对话（粘贴 `install/prompt-template.md`） | 通用，零安装 |

详见 `docs/ENVIRONMENTS.md`。

---

## 七、许可

本仓库的**提示词、规范、脚本、文档**采用 MIT（见 `LICENSE`）。
《世界相命全集》原书内容版权归原作者与出版方，本仓库不包含其正文（见 `NOTICE.md`）。
