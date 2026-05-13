#!/usr/bin/env python3
"""Sync html-anything skill assets from refer/ to skills/."""

import argparse
import shutil
import sys
from pathlib import Path

# Assets to copy, relative to refer/html-anything/
ASSETS = [
    "SKILL.md",
    "prompts/sources",
    "prompts/styles",
]

# Exclude patterns (applied within ASSETS)
EXCLUDE_NAMES = {".git", ".gitignore", ".clawhubignore", "__pycache__"}
EXCLUDE_PATTERNS = {"*.pyc"}


def get_project_root() -> Path:
    """Locate project root from this script's position."""
    return Path(__file__).resolve().parent.parent


def should_copy(path: Path) -> bool:
    """Return True if the file should be copied."""
    if path.is_symlink() or path.name in EXCLUDE_NAMES:
        return False
    return not any(path.match(p) for p in EXCLUDE_PATTERNS)


def _copy_item(rel: Path, src: Path, dst: Path, dry_run: bool) -> bool:
    """Copy a single file. Returns True if copied/skipped, False on error."""
    if dry_run:
        print(f"[DRY-RUN] would copy: {rel}")
        return True
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied: {rel}")
        return True
    except OSError as exc:
        print(f"Error copying {rel}: {exc}", file=sys.stderr)
        return False


def _asset_files(source: Path):
    """Yield (rel_path, src_path, should_copy) for every candidate file."""
    for asset in ASSETS:
        src_path = source / asset
        if not src_path.exists():
            print(f"Warning: missing source asset: {src_path}", file=sys.stderr)
            continue
        if src_path.is_file():
            yield src_path.relative_to(source), src_path, should_copy(src_path)
        elif src_path.is_dir():
            for file_path in sorted(src_path.rglob("*")):
                if file_path.is_file():
                    yield file_path.relative_to(source), file_path, should_copy(file_path)


def sync(dry_run: bool = False) -> int:
    """Perform the sync. Returns exit code (0 for success)."""
    root = get_project_root()
    source = root / "refer" / "html-anything"
    target = root / "skills" / "html-anything"

    if not source.exists():
        print(f"Error: source not found: {source}", file=sys.stderr)
        return 1

    if not dry_run and target.exists():
        print(f"Cleaning: {target}")
        shutil.rmtree(target)

    copied = skipped = errors = 0
    for rel, src, ok in _asset_files(source):
        if not ok:
            skipped += 1
            continue
        if _copy_item(rel, src, target / rel, dry_run):
            copied += 1
        else:
            errors += 1

    action = "Would copy" if dry_run else "Copied"
    print(f"\n{action} {copied} files, skipped {skipped} files.")
    if errors:
        print(f"Errors: {errors} files", file=sys.stderr)

    return 0 if dry_run else verify(target)


def verify(target: Path) -> int:
    """Verify the sync result. Returns 0 if all checks pass."""
    print("\nVerification:")
    all_ok = True

    def check(path: Path, kind: str) -> None:
        nonlocal all_ok
        exists = path.exists() if kind == "file" else path.is_dir()
        rel = path.relative_to(target)
        mark, msg = ("✓", "") if exists else ("✗", " MISSING")
        print(f"  {mark} {rel}{msg}")
        if not exists:
            all_ok = False

    check(target / "SKILL.md", "file")
    check(target / "prompts" / "sources", "dir")
    check(target / "prompts" / "styles", "dir")
    check(target / "prompts" / "styles" / "catalog.json", "file")

    for subdir in ("sources", "styles"):
        md_files = list((target / "prompts" / subdir).glob("*.md"))
        if md_files:
            print(f"  ✓ prompts/{subdir}/ has {len(md_files)} .md files")
        else:
            print(f"  ✗ prompts/{subdir}/ has no .md files")
            all_ok = False

    if all_ok:
        print("All checks passed.")
    return 0 if all_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync html-anything skill assets from refer/ to skills/"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    args = parser.parse_args()
    return sync(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
