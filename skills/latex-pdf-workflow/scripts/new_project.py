import argparse
import json
import os
from pathlib import Path
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--directory", type=Path)
args = parser.parse_args()
if Path(args.name).name != args.name or args.name in {".", ".."}:
    parser.error("--name must be one directory name")
parent = args.directory or (Path("D:/LaTeX工作区") if os.name == "nt" else Path.home()/"latex-projects")
destination = parent.expanduser().resolve()/args.name
if destination.exists():
    parser.error(f"project already exists: {destination}")
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT/"assets/project", destination)
print(json.dumps({"project": str(destination), "main": str(destination/"main.tex")}, ensure_ascii=False))
