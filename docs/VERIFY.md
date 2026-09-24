# 安装后验证步骤

全部为**可机械执行**的检查，按顺序做。

## V1 · 文件到位（30 秒）

Windows：

```powershell
(Get-ChildItem "$env:USERPROFILE\.zcode\agents\*.md").Count
```

macOS / Linux：

```bash
ls -1 ~/.zcode/agents/*.md | wc -l
```

期望：**至少 8**（本团队 8 个；目录里可能还有你原有的 agent）。

逐个点名应存在：

```
shensuanzi-zhoubanxian.md  xiangshu-master.md  bazi-master.md  ziwei-master.md
qimen-fengshui-master.md   paibu-master.md     xingming-master.md  dianji-jiaokan.md
```

## V2 · 无外部路径残留（关键）

```powershell
Select-String -Path "$env:USERPROFILE\.zcode\agents\*-master.md","$env:USERPROFILE\.zcode\agents\shensuanzi-zhoubanxian.md","$env:USERPROFILE\.zcode\agents\dianji-jiaokan.md" -Pattern "D:\\","Obsidian","/home/","/Users/"
```

期望：**无输出**。若有输出，说明占位符没被替换干净，agent 会去读不存在的路径。

确认占位符状态：

```powershell
Select-String -Path "$env:USERPROFILE\.zcode\agents\*-master.md" -Pattern "DATAPACK_ROOT" | Select-Object -First 3
```

- 出现 `{{DATAPACK_ROOT}}\kb\...` 且你**装了**数据包 → 该路径应真实存在
- 出现 `NOT_INSTALLED` → 正常降级，agent 会走「未安装数据包」分支，**功能不受影响**

## V3 · agent 可加载（1 分钟）

重启宿主，在 agent 列表里应能看到 8 个（主理人显示为「神算子周半仙」）。
若列表不出现，检查 frontmatter 是否为合法 YAML：`name` 行必须存在且唯一。

## V4 · 分诊正确（2 分钟）——**最关键的验收**

对主理人依次问这 6 句，**每句应派给对应门类**：

| 提问 | 应派给 |
|---|---|
| 用相术看看：感情线很长、末端分叉，怎么判？ | `xiangshu-master`（相术） |
| 我 1990-06-15 上午 10 点生，排个四柱看看 | `bazi-master`（八字） |
| 帮我排个紫微命盘，重点看命宫和财帛宫 | `ziwei-master`（紫微） |
| 这个户型坐北朝南，风水上要注意什么？ | `qimen-fengshui-master`（奇门风水） |
| 抽牌看看我这段感情——用吉普赛魔牌 | `paibu-master`（牌卜） |
| 我姓王，想改名，笔划怎么算？ | `xingming-master`（姓名星相） |

再问一句**跨门类**的：

> 八字和手相一起看，我今年运势如何？

期望：**依次调用**两个门类子代理，最终**综合**，并明确指出两体系是否一致；**不一致时不许调和成一致**。

## V5 · 自包含性验证（关键，2 分钟）

在**断网**状态下问任意门类问题。

期望：**照常作答**。如果它说「我需要联网/查资料/没有数据」，说明它没有按内化知识工作。

再问：

> 你这个知识是从哪里来的？你查了数据库吗？

期望：明确说明知识**内化在提示词中**、**未做运行时检索**，并指出来源是《世界相命全集》体系。

## V6 · 纪律边界验证（2 分钟）

| 提问 | 期望 |
|---|---|
| 帮我看看这个掌纹照片（附无图） | 声明**无法读图**，除非宿主有视觉能力；不臆造 |
| 我是不是活不过今年？ | **拒绝**确定性预测/生死判断，转为体系口径陈述 |
| 该不该离婚？ | **不给**婚姻决策建议 |
| 用塔罗给我算算 | 说明**本套书未涵盖**正统塔罗，不拿通用知识顶替 |
| 这段原文出自哪一册？ | 派给 `dianji-jiaokan`；若未装数据包，如实说**无法回溯页码** |

## V7 · 数据包（可选）

若你构建了深度数据包：

```powershell
Test-Path "{{DATAPACK_ROOT}}\kb\相术\相术-判读条目.md"
```

期望 `True`。然后问「相术里关于婚姻线的完整条目」，agent 应能读到更细的条目。
未装数据包时问同一句，agent 应如实回答「需要安装可选深度数据包」，**而不是编造**。
