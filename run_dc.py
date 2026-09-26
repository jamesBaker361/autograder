"""For each student, run their most recent dc.py through dcsolve.py and save results.

Usage: python run_dc.py
Writes one <First Last>.txt per student into ./results/
"""

import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKELETON = ROOT / "code_skeleton"
RESULTS = ROOT / "results"
CSV_FILE = ROOT / "students_f2026.csv"
TIMEOUT = 120  # seconds per command

COMMANDS = [
    "python dcsolve.py dog cat",
    "python dcsolve.py why ask",
    "python dcsolve.py test bush",
    "python dcsolve.py love hate",
    "python dcsolve.py bear duck steps",
    "python dcsolve.py bear duck scrabble",
    "python dcsolve.py bear duck frequency",
]

PATTERN = re.compile(r"^PA1_(.+)_attempt_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})(?:_.*)?_dc\.py$")


def load_names():
    names = {}
    with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            names[row["Username"].strip()] = f"{row['First Name'].strip()} {row['Last Name'].strip()}"
    return names


def latest_submissions():
    latest = {}
    for p in ROOT.glob("PA1_*_attempt_*dc.py"):
        m = PATTERN.match(p.name)
        if not m:
            continue
        sid, date = m.groups()
        # dates are YYYY-MM-DD-HH-MM-SS, so string comparison orders them correctly
        if sid not in latest or date > latest[sid][0]:
            latest[sid] = (date, p)
    return latest


def run(cmd):
    args = cmd.split()
    args[0] = sys.executable
    try:
        r = subprocess.run(args, cwd=SKELETON, capture_output=True, text=True, timeout=TIMEOUT)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return out + f"TIMEOUT after {TIMEOUT}s\n"


def main():
    names = load_names()
    RESULTS.mkdir(exist_ok=True)
    dc_path = SKELETON / "dc.py"
    backup = SKELETON / "dc.py.orig"
    shutil.copy(dc_path, backup)
    try:
        for sid, (date, src) in sorted(latest_submissions().items()):
            name = names.get(sid)
            if name is None:
                print(f"WARNING: no CSV entry for {sid}; using id as name")
                name = sid
            print(f"{name} ({sid}) <- {src.name}")
            shutil.copy(src, dc_path)
            with open(RESULTS / f"{name}.txt", "w") as out:
                out.write(f"Student: {name} ({sid})\nSubmission: {src.name}\n\n")
                for cmd in COMMANDS:
                    out.write(f"$ {cmd}\n{run(cmd)}\n")
    finally:
        shutil.move(backup, dc_path)


if __name__ == "__main__":
    main()
