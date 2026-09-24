# 支持的运行环境

## 层级 A — 已实测

| 项 | 值 |
|---|---|
| 宿主 | **zcode / WorkBuddy 桌面版** |
| agent 目录 | `~/.zcode/agents/`（Windows：`C:\Users\<你>\.zcode\agents\`） |
| 文件格式 | 单个 `.md`，YAML frontmatter + 正文即系统提示词 |
| 必需 frontmatter 键 | `name` `description` `displayName` `profession` `maxTurns` `skills` |
| 实测版本 | agent 文件在本仓库 `agents/` 下按上述格式产出，已在本机加载运行 |

安装后需**重启宿主**才会加载新 agent。

## 层级 B — 格式兼容（未逐一实测）

任何**接受 markdown + YAML frontmatter 作为 agent 定义**的宿主都可以用，例如 Claude Code 的
subagent、Cursor rules、Continue 配置等。差异只在 frontmatter 键名，正文（提示词 + 内核知识）
是通用的。

迁移做法：

1. 把 `agents/*.md` 里的 frontmatter 换成目标宿主的键名；
2. 正文**整段照搬**（正文才是知识本体）；
3. 确保 `{{DATAPACK_ROOT}}` 被替换成真实路径，或保留占位符（agent 会走降级路径）。

## 层级 C — 通用（零安装）

任何 LLM 对话都能用：把 `install/prompt-template.md` 里的合成提示词粘进系统提示词位置。
没有工具调用、没有文件读取，纯提示词自包含，**这是最稳的「所有设备直接可用」路径**。

## 不支持的场景

| 场景 | 说明 |
|---|---|
| 无 LLM 的纯脚本环境 | agent 是提示词，不是可执行程序，必须有模型驱动 |
| 期望 agent 自己联网查资料 | 设计上**禁止**运行时检索；它凭内化知识作答 |
| 期望读原书插图 | 需宿主具备视觉能力且可选数据包含图片；否则明确声明读不了图 |
| 需要他人底稿内容的离线包 | 本仓库不含原书正文，须按 `docs/DATAPACK.md` 用你自己的底稿构建 |
