import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("main", type=Path)
parser.add_argument("--engine", choices=["xelatex", "lualatex"], default="xelatex")
parser.add_argument("--profile", choices=["native", "portable"])
parser.add_argument("--tex-bin", type=Path)
parser.add_argument("--output-directory", type=Path)
args = parser.parse_args()
main = args.main.expanduser().resolve()
if not main.is_file() or main.suffix.lower() != ".tex":
    parser.error("main must be an existing .tex file")
config_path = ROOT/"local-environment.json"
config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
tex_bin = args.tex_bin or (Path(os.environ["LATEX_TEX_BIN"]) if os.environ.get("LATEX_TEX_BIN") else None)
if tex_bin is None and config.get("tex_bin"):
    tex_bin = Path(config["tex_bin"])
env = os.environ.copy()
if tex_bin:
    env["PATH"] = str(tex_bin) + os.pathsep + env.get("PATH", "")
if os.name == "nt":
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
compiler = shutil.which(args.engine, path=env["PATH"])
latexmk = shutil.which("latexmk", path=env["PATH"])
if not compiler:
    parser.error(f"{args.engine} not found; inspect the existing TeX installation")
if args.profile:
    if not (main.parent/"report-style.sty").is_file():
        parser.error("--profile is only for this skill's report template")
    (main.parent/"font-profile.tex").write_text(
        "\\portablefontstrue\n" if args.profile == "portable" else "\\portablefontsfalse\n", encoding="utf-8")
outdir = (args.output_directory or main.parent/"build").resolve()
outdir.mkdir(parents=True, exist_ok=True)
flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
if latexmk:
    command = [latexmk, "-"+args.engine, "-no-shell-escape", "-file-line-error",
               "-halt-on-error", "-interaction=nonstopmode", "-synctex=1",
               "-outdir="+os.path.relpath(outdir, main.parent), main.name]
    passes = 1
else:
    command = [compiler, "-no-shell-escape", "-file-line-error", "-halt-on-error",
               "-interaction=nonstopmode", "-synctex=1", "-output-directory="+str(outdir), main.name]
    passes = 2
started = time.monotonic()
outputs = []
result_code = 0
try:
    for _ in range(passes):
        proc = subprocess.run(command, cwd=main.parent, env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=240,
                              creationflags=flags)
        outputs.append(proc.stdout + proc.stderr)
        result_code = proc.returncode
        if result_code:
            break
except subprocess.TimeoutExpired as error:
    outputs.append(str(error))
    result_code = 124
pdf = outdir/(main.stem+".pdf")
combined = "\n".join(outputs)
(outdir/"compile-console.txt").write_text(combined, encoding="utf-8")
record = {"success": result_code == 0 and pdf.is_file(), "exit_code": result_code,
          "pdf": str(pdf), "engine": args.engine, "font_profile": args.profile or "project-defined",
          "compiler": compiler, "driver": latexmk or compiler, "command": command,
          "elapsed_seconds": round(time.monotonic()-started, 2),
          "log": str(outdir/(main.stem+".log")), "console": str(outdir/"compile-console.txt")}
(outdir/"build-result.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
if not record["success"]:
    print("\n".join(combined.splitlines()[-24:]), file=sys.stderr)
    sys.exit(result_code or 1)
