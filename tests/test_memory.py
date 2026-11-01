"""Test migration boundaries and handoff behavior without network access."""

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/memory.py"
SPEC = importlib.util.spec_from_file_location("memory", MODULE_PATH)
memory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(memory)


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.source = self.base / "old-computer"
        self.source.mkdir()
        for relative in memory.CORE:
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {relative}\n\n已核实的共享知识。\n", encoding="utf-8")
        for relative in memory.ADAPTERS:
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Read AGENTS.md\n", encoding="utf-8")

    def note(self, name="MEMORY.md", text="# Memory\n\n使用中文交接。\n"):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def imported_note(self, text="# Reviewed\n\nA project fact.\n"):
        self.note(text=text)
        batch, _ = memory.stage_import(self.repo, [self.source])
        return batch / "source-01/MEMORY.md"

    def test_import_only_markdown_and_skip_transcripts_and_credentials(self):
        self.note()
        self.note("nested/项目.md")
        self.note("sessions/transcript.md", "private transcript")
        self.note("plugins/plugin.md", "unrelated plugin")
        self.note("AUTH.md", "private auth")
        (self.source / "auth.json").write_text('{"token": "not-a-note"}')
        (self.source / "history.jsonl").write_text("private transcript")
        (self.source / "config.toml").write_text("not a note")
        batch, count = memory.stage_import(self.repo, [self.source])
        self.assertEqual(count, 2)
        names = sorted(p.relative_to(batch).as_posix() for p in batch.rglob("*.md"))
        self.assertEqual(names, ["source-01/MEMORY.md", "source-01/nested/项目.md"])
        self.assertFalse((self.repo / "memory/imported").exists())

    def test_source_bytes_are_never_changed(self):
        original = self.note(text="\ufeff# 记忆\r\n原始内容\r\n")
        before = original.read_bytes()
        batch, _ = memory.stage_import(self.repo, [original])
        self.assertEqual(original.read_bytes(), before)
        self.assertIn("原始内容", (batch / "source-01/MEMORY.md").read_text(encoding="utf-8"))

    def test_duplicate_import_preserves_review_edits(self):
        original = self.note()
        batch, _ = memory.stage_import(self.repo, [original])
        staged = batch / "source-01/MEMORY.md"
        staged.write_text("Reviewed and shortened", encoding="utf-8")
        again, count = memory.stage_import(self.repo, [original])
        self.assertEqual(again, batch)
        self.assertEqual(count, 1)
        self.assertEqual(staged.read_text(), "Reviewed and shortened")

    def test_changed_source_gets_new_batch(self):
        original = self.note()
        first, _ = memory.stage_import(self.repo, [original])
        original.write_text("A new fact", encoding="utf-8")
        second, _ = memory.stage_import(self.repo, [original])
        self.assertNotEqual(first, second)
        self.assertTrue(first.is_dir())

    def test_empty_import_is_an_error_and_writes_nothing(self):
        with self.assertRaises(memory.MemoryError):
            memory.stage_import(self.repo, [])
        self.assertFalse((self.repo / ".memory-import").exists())

    def test_invalid_input_fails_before_any_copy(self):
        self.note("a-valid.md")
        (self.source / "z-bad.md").write_bytes(b"\xff\xfe")
        with self.assertRaises(memory.MemoryError):
            memory.stage_import(self.repo, [self.source])
        self.assertFalse((self.repo / ".memory-import").exists())

    def test_oversized_note_fails_before_copy(self):
        path = self.note(text="x" * (memory.MAX_NOTE_BYTES + 1))
        with self.assertRaises(memory.MemoryError):
            memory.stage_import(self.repo, [path])
        self.assertFalse((self.repo / ".memory-import").exists())

    def test_explicit_non_markdown_input_is_refused(self):
        path = self.source / "auth.json"
        path.write_text("private")
        with self.assertRaises(memory.MemoryError):
            memory.stage_import(self.repo, [path])

    @unittest.skipIf(os.name == "nt", "Windows symlink creation may need privileges")
    def test_source_scan_does_not_follow_symlinks(self):
        self.note()
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "private.md").write_text("private")
        (self.source / "linked-dir").symlink_to(outside, target_is_directory=True)
        (self.source / "linked.md").symlink_to(outside / "private.md")
        _, count = memory.stage_import(self.repo, [self.source])
        self.assertEqual(count, 1)

    @unittest.skipIf(os.name == "nt", "Windows symlink creation may need privileges")
    def test_staging_symlink_cannot_write_outside_repository(self):
        self.note()
        outside = self.base / "outside"
        outside.mkdir()
        (self.repo / ".memory-import").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(memory.MemoryError):
            memory.stage_import(self.repo, [self.source])
        self.assertEqual(list(outside.iterdir()), [])

    def test_promote_requires_review_and_valid_name(self):
        staged = self.imported_note()
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, staged, "note", False)
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, staged, "../../escape", True)
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, staged, "config", True)
        self.assertFalse((self.repo / "memory/imported").exists())

    def test_promote_refuses_external_source_and_path_traversal(self):
        external = self.note()
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, external, "note", True)
        staged = self.imported_note()
        traversal = staged.parent / ".." / "source-01" / staged.name
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, traversal, "note", True)

    def test_secret_is_blocked_without_exposing_its_value(self):
        fake_token = "sk-" + "A" * 32
        staged = self.imported_note(f"# Credentials\n{fake_token}\n")
        with self.assertRaises(memory.MemoryError) as raised:
            memory.promote(self.repo, staged, "note", True)
        self.assertNotIn(fake_token, str(raised.exception))
        self.assertIn("第 2 行", str(raised.exception))
        manifest = staged.parents[1] / "manifest.json"
        self.assertIn('"possible_credentials": true', manifest.read_text())

    def test_promote_preserves_existing_shared_note(self):
        staged = self.imported_note()
        target = memory.promote(self.repo, staged, "note", True)
        before = target.read_bytes()
        staged.write_text("Changed draft", encoding="utf-8")
        with self.assertRaises(memory.MemoryError):
            memory.promote(self.repo, staged, "note", True)
        self.assertEqual(target.read_bytes(), before)

    def test_export_excludes_quarantine_and_local_source_paths(self):
        marker = "PRIVATE_QUARANTINED_CONTENT"
        self.imported_note(marker)
        output = memory.export_context(self.repo).read_text(encoding="utf-8")
        self.assertNotIn(marker, output)
        self.assertNotIn(str(self.source), output)
        self.assertIn("已核实的共享知识", output)

    def test_promoted_note_is_automatically_included_in_handoff(self):
        staged = self.imported_note("# 原记忆\n\n项目下一步是更新文档。\n")
        memory.promote(self.repo, staged, "codex-memory", True)
        output = memory.export_context(self.repo).read_text(encoding="utf-8")
        self.assertIn("memory/imported/codex-memory.md", output)
        self.assertIn("项目下一步是更新文档", output)
        memory.check_repository(self.repo)

    def test_stale_export_is_detected(self):
        memory.export_context(self.repo)
        memory.check_repository(self.repo)
        (self.repo / "memory/current.md").write_text("New handoff", encoding="utf-8")
        with self.assertRaises(memory.MemoryError):
            memory.check_repository(self.repo)
        memory.export_context(self.repo)
        memory.check_repository(self.repo)

    def test_direct_edit_with_credential_is_blocked_from_export(self):
        private = self.repo / "memory/private.md"
        private.write_text("password=" + "A" * 32, encoding="utf-8")
        with self.assertRaises(memory.MemoryError):
            memory.export_context(self.repo)
        self.assertFalse((self.repo / "CONTEXT.md").exists())

    @unittest.skipIf(os.name == "nt", "Windows symlink creation may need privileges")
    def test_export_refuses_symlinks_in_shared_memory(self):
        (self.repo / "memory/private.md").symlink_to(self.note())
        with self.assertRaises(memory.MemoryError):
            memory.export_context(self.repo)

    @unittest.skipUnless(shutil.which("git"), "Git is needed for the ignore integration check")
    def test_raw_batches_are_ignored_by_git(self):
        shutil.copyfile(MODULE_PATH.parents[1] / ".gitignore", self.repo / ".gitignore")
        subprocess.run(["git", "init", "--quiet", str(self.repo)], check=True)
        staged = self.imported_note("Private local material")
        result = subprocess.run(
            ["git", "check-ignore", str(staged)], cwd=self.repo,
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(".memory-import", result.stdout)

    def test_discovery_obeys_custom_codex_home_without_opening_config(self):
        custom = self.base / "custom-codex"
        with patch.dict(os.environ, {"CODEX_HOME": str(custom)}):
            paths = memory.candidate_sources(self.base)
        self.assertIn(custom / "memories", paths)
        self.assertIn(self.base / ".codex/AGENTS.md", paths)
        self.assertNotIn(custom / "auth.json", paths)
        self.assertNotIn(custom / "config.toml", paths)


if __name__ == "__main__":
    unittest.main()
