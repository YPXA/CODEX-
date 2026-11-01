# 跨账号、跨 AI 的共享记忆

用 **Markdown + AGENTS.md + GitHub** 保存可复用的项目知识。换 Codex
账号或切换 Claude Code、Gemini CLI、Cursor、Copilot 后，读取同一份仓库
文件即可继续工作；无需购买记忆服务，也不需要模型 API 密钥。

**当前状态：共享记忆工具已建立，原电脑上的旧 Codex 记忆尚未导入。**
云端任务无法直接读取你的电脑；首次导入需要在有旧记忆的电脑上运行。
原仓库 `YPXA/CODEX-` 在部署时是公开的，私人知识应使用私有仓库。

## 直接开始

在你平时使用 Codex 的电脑上安装 Git 和 Python 3.10+，然后打开终端：

```bash
git clone https://github.com/YPXA/CODEX-.git
cd CODEX-
python scripts/memory.py import
```

macOS/Linux 如果只有 `python3`，把 `python` 换成 `python3`；Windows
也可使用 `py -3`。已有克隆时进入原目录并先执行 `git pull --ff-only`，
无需重复克隆。

命令会把找到的 Markdown 记忆复制到被 Git 忽略的 `.memory-import/`，
不会上传，也不会改动原来的 Codex 数据。未找到时可运行：

```bash
python scripts/memory.py discover
python scripts/memory.py import "/你的实际记忆目录"
```

在本机打开暂存文件，整理成适合共享的知识，再按
[完整迁移步骤](docs/migration.md) 提升和推送。工具只发现常见 Markdown
候选位置；如果你的 Codex 版本没有输出这些文件，需先在原会话中让 AI
整理记忆为 Markdown，再导入。

## 切换 AI 时怎么用

| 工具 | 读取入口 | 操作 |
| --- | --- | --- |
| Codex | `AGENTS.md` | 在克隆目录中打开任务 |
| Claude Code | `CLAUDE.md` | 在克隆目录中启动，入口导入共享记忆 |
| Gemini CLI | `GEMINI.md` | 在克隆目录中启动，入口导入共享记忆 |
| Cursor | `.cursor/rules/shared-memory.mdc` | 打开仓库，规则要求读取共享记忆 |
| GitHub Copilot | `.github/copilot-instructions.md` | 打开仓库并启用仓库指令 |
| 网页版 ChatGPT / Claude / 其他 AI | `CONTEXT.md` | 将文件内容作为上下文提供给 AI |

仓库文件不绑定 AI 登录。私有仓库需要新使用者具备 GitHub 读取权限。
入口是否加载还受客户端版本、信任和指令设置影响；首次切换时可以说：

> 请先读取 AGENTS.md、memory/README.md 和当前交接文件，说明已掌握的
> 项目状态，再继续我的任务。不要把历史记忆当作优先于当前要求的指令。

没有文件或联网能力的 AI 不会凭空知道仓库内容：请直接提供
[CONTEXT.md](CONTEXT.md)。网页 AI 返回的新结论也需要写回仓库，才能
供下一次使用。

## 日常保存和同步

开始工作前，在工作区干净时执行 `git pull --ff-only`。结束后，让 AI
更新 `memory/current.md`，把长期决定写入 `memory/decisions.md`，
然后执行：

```bash
python scripts/memory.py export
python scripts/memory.py check
git diff -- memory CONTEXT.md
git add -- memory CONTEXT.md
git diff --cached
git commit -m "Update shared memory"
git push
```

推送被拒绝时保留本地提交，获取远端变更并处理冲突；不要强制推送。
新电脑或新账号拉取最新提交后，即可读到已同步的记忆。

## 文件结构和验证

```text
AGENTS.md                 各工具共用的规则
CLAUDE.md / GEMINI.md      对应客户端的导入入口
CONTEXT.md                自动生成的单文件快照
memory/                   经选择共享的记忆原件
scripts/memory.py          发现、隔离导入、提升、导出、校验
docs/migration.md         本地迁移和私有仓库说明
docs/research.md          开源方案调研及选择理由
tests/                    数据边界和迁移行为测试
.memory-import/           本机原文与来源清单，不提交、不导出
```

```bash
python -m unittest discover -s tests -v
python scripts/memory.py check
```

GitHub Actions 会在提交和 PR 时运行同样的检查。凭据检查只能发现部分
常见格式，不能判断自然语言是否涉及隐私，仍需检查准备共享的内容。

这套方案迁移的是显式记录的知识，不包括 AI 内部状态、登录凭据、聊天
列表或未整理的完整历史。开源选择依据见 [调研记录](docs/research.md)。
