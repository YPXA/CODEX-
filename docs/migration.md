# 从原电脑导入 Codex 记忆

## 1. 选择合适的存储位置

`YPXA/CODEX-` 部署时是公开仓库。公开仓库适合工具和可公开的项目知识；
个人偏好、内部项目资料和其他私人记忆请放进私有仓库。

可在 GitHub 创建一个私有仓库，把这套文件复制进去，并把本地 Git
remote 指向该私有仓库。不要用复制整个 `.codex` 目录的方式迁移。
私有仓库需要为新账号授权访问；AI 账号与 GitHub 仓库权限是两回事。
已有公开历史的资料不会因为删除文件而从历史中消失。

## 2. 在有记忆的电脑上定位和导入

```bash
python scripts/memory.py discover
python scripts/memory.py import
```

工具检查 `CODEX_HOME`（若设置）及 `~/.codex` 下的 `memories/`、
`memory/`、`MEMORY.md`、`memory.md`、`AGENTS.md`、`AGENTS.override.md`。
这些只是候选位置，不保证每个 Codex 版本都存在。也可以明确指定：

```bash
python scripts/memory.py import "/path/to/memories" "/path/to/project/AGENTS.md"
```

Windows 示例（在 PowerShell 中运行）：

```powershell
py -3 scripts/memory.py discover
py -3 scripts/memory.py import "$env:USERPROFILE\.codex\memories"
```

只接受 UTF-8 的 `.md` / `.markdown`；单文件最多 1 MiB，过大时请先整理
摘要。目录扫描跳过符号链接、会话、日志、插件、技能和临时目录，不读
`auth.json`、`config.toml`、JSONL 或数据库。原文件保持不变。

没有 Markdown 时，在原来的 Codex 会话里提出：

> 请将本项目已确认的目标、长期偏好、关键决定、运行方法、已完成工作和
> 未完成事项整理为一个 UTF-8 Markdown 交接文件。区分事实与推测，
> 省略密钥、账号登录、私人资料和完整聊天原文，注明需要核实的旧信息。

然后将该文件作为显式来源导入。不支持直接解码 Codex 内部数据库。

## 3. 在本机检查暂存内容

导入命令会返回类似：

```text
.memory-import/0123456789abcdef/source-01/MEMORY.md
```

每个批次的 `manifest.json` 记录本机来源和校验值；它只保留在本机。
相同来源和内容重复导入会复用同一批次，不覆盖检查过程中修改的文件；
原文件变化后会产生新批次。导入结果不是已发布的记忆。

在暂存区直接修改副本，删除不应共享的内容，并精简过时或矛盾的记录。
确认使用者范围后，逐个选择要同步的笔记：

```bash
python scripts/memory.py promote .memory-import/0123456789abcdef/source-01/MEMORY.md --name codex-memory --reviewed
```

`--reviewed` 表示你已经检查这份文件可以被目标仓库的读者看到。
它会复制到 `memory/imported/codex-memory.md`，不会覆盖同名共享文件。
命令只复制文件，不会自动提交、推送或更改仓库可见性。常见凭据格式
会阻止提升，错误只显示类型和行号，不显示凭据值；此检查并不完备。

## 4. 生成上下文并同步到 GitHub

导入成功后，更新 `memory/current.md` 和 `memory/imported/README.md`
中的状态，说明导入来源、保留的知识和未完成事项。不要把本机绝对路径
或原始清单直接贴进共享目录。

```bash
python scripts/memory.py export
python scripts/memory.py check
python -m unittest discover -s tests -v
git status --short
git add -- memory CONTEXT.md
git diff --cached
git commit -m "Import reviewed Codex memories"
git push
```

如仓库进展同时发生变化，先处理 Git 冲突，再重新生成 `CONTEXT.md`。
不要使用 `git add -f` 把 `.memory-import/` 加进版本控制。

## 5. 在新账号或其他 AI 验证

在新环境克隆或拉取相同仓库，打开 AI 并要求它读共享记忆，复述最近
进展和下一步。核对其依据是否来自实际笔记。客户端不能读文件时提供
`CONTEXT.md`；无法访问私有仓库时先解决仓库授权。

在其他业务仓库使用这些记忆时，可把本仓库克隆到旁边，并在那个仓库的
`AGENTS.md` 中写明相对位置，要求 AI 读取共享目录。该位置必须在 AI
可访问的范围内；本方案不会偷偷更改电脑全局指令或客户端配置。
