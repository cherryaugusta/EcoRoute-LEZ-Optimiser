import re
import subprocess
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "Possible AWS Access Key ID"),
    (re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----"), "Private key material"),
    (re.compile(r"(?i)\bpassword\s*=\s*['\"][^'\"]+['\"]"), "Hardcoded password assignment"),
    (re.compile(r"(?i)\bapi[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]"), "Hardcoded API key"),
    (re.compile(r"(?i)\bsecret\s*[:=]\s*['\"][^'\"]+['\"]"), "Hardcoded secret"),
]


def staged_files() -> list[Path]:
    r = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    if r.returncode != 0:
        return []
    files: list[Path] = []
    for line in r.stdout.splitlines():
        p = Path(line.strip())
        if not p.as_posix():
            continue
        if any(part in {"node_modules", ".venv", "dist", ".angular"} for part in p.parts):
            continue
        if p.exists() and p.is_file():
            files.append(p)
    return files


def main() -> int:
    hits: list[str] = []
    for f in staged_files():
        try:
            data = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for rx, label in PATTERNS:
            if rx.search(data):
                hits.append(f"{f.as_posix()}: {label}")

    if hits:
        print("mock_gitleaks: potential secrets detected (demo hook).")
        for h in hits:
            print(f"  - {h}")
        print("Fix before commit, or remove the offending material.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
