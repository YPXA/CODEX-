# 开源方案调研

调研日期：2026-11-01。目标是让同一个仓库的知识可跨账号、跨 AI 使用，
先满足可迁移、可审阅和低维护成本。

| 方案 | 原始资料 | 适用范围 | 本次选择 |
| --- | --- | --- | --- |
| AGENTS.md + Git | [AGENTS.md 官方项目](https://github.com/agentsmd/agents.md)、[格式说明](https://agents.md/) | 用项目文件向编码 AI 提供上下文；Git 提供云端版本同步 | 采用，作为记忆原件和入口 |
| Basic Memory | [官方开源仓库](https://github.com/basicmachines-co/basic-memory) | 将 Markdown 作为知识文件，经 MCP 提供读写、检索和知识图谱能力 | 后续需要检索时可接入；本次未安装或部署其服务 |
| Mem0 | [官方开源仓库](https://github.com/mem0ai/mem0) | 面向应用的记忆层，提供 SDK 和自托管选项，涉及模型及嵌入配置 | 当前需求不需要该运行栈；本次未部署 |

本次实现参考文件优先和开放入口的做法，迁移工具为本仓库的 Python
标准库代码。没有复制上述项目源码，也没有连接它们的托管付费服务。

## 为什么先选择仓库文件

用户需要把项目知识带到另一个账号或 AI。直接把可共享知识存成文件，
克隆后即可读取，无需让新 AI 兼容旧客户端的数据库。Git 可以展示改动
并保留历史。局限是记忆必须显式维护；它不会自动提炼所有旧会话，
也不提供语义搜索或随时在线的远程 MCP 接口。

如果后续需要大量笔记的搜索，可以在相同 Markdown 文件上接入 Basic
Memory。届时需单独验证版本、运行配置、鉴权和云端访问。GitHub 中
存放记忆与远程 MCP 服务是不同的部署方式。

## 各 AI 入口的依据

- [AGENTS.md 官方说明](https://agents.md/)：项目级 Markdown 指令入口。
- [Claude Code 记忆文档](https://code.claude.com/docs/en/memory)：
  `CLAUDE.md` 支持 `@path` 导入；本仓库显式导入共享规则和核心记忆。
- [Gemini CLI 上下文文档](https://geminicli.com/docs/cli/gemini-md/)：
  `GEMINI.md` 支持分文件导入。
- [Cursor 规则文档](https://cursor.com/docs/rules)：
  `.cursor/rules/*.mdc` 支持 `alwaysApply`，入口要求读取共享文件。
- [GitHub Copilot 仓库指令文档](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)：
  使用 `.github/copilot-instructions.md`。

这些是客户端的上下文入口，不保证在所有产品版本、设置或网页聊天中
自动生效。因此同时提供普通 Markdown 的 `CONTEXT.md` 作为手动交接。
