# 共享记忆索引

这是可随 Git 同步的记忆原件，不依赖某个 Codex 账号或某家模型。

| 文件 | 用途 |
| --- | --- |
| [project.md](project.md) | 仓库目标、已核实事实 |
| [current.md](current.md) | 最近进展、验证结果、下一步 |
| [decisions.md](decisions.md) | 长期决定及原因 |
| [imported/](imported/) | 从本地导入、经检查后保留的记忆 |
| [../CONTEXT.md](../CONTEXT.md) | 给无法读取仓库的 AI 使用的单文件版本 |

每次开始任务先读前三个文件，并按需读取 `imported/`。任务结束更新当前
进展，长期决定单独记录。记忆应简明、注明来源或依据，不把推测写成事实。
发生矛盾时以用户当前指示和已核实的仓库状态为准，保留必要的变更原因。

本地导入的原文位于 Git 忽略的 `.memory-import/`；它不属于共享记忆，
也不会进入单文件导出。只有显式整理、检查并提升到 `memory/imported/`
的内容会随 Git 同步。公开仓库的所有历史提交都可能被任何人读取。

本次新增：[LaTeX PDF偏好](imported/latex-pdf-preferences.md)，实现见 [LaTeX工作流](../docs/latex-workflow.md)。
