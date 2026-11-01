# 已导入的记忆

目前尚无从原电脑迁入的旧记忆。

检查 `.memory-import/` 中的文件并整理出适合共享的内容后，执行：

```bash
python scripts/memory.py promote .memory-import/BATCH/note.md --name note --reviewed
python scripts/memory.py export
python scripts/memory.py check
```

`promote` 只复制指定文件，不执行 Git 提交或上传。新笔记会自动进入
下一次单文件导出。导入完成后请更新本说明与 `memory/current.md`。
