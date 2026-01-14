from __future__ import annotations

import re
from pathlib import Path

from multi_agent_engineering.models.file_manifest import FileManifest


_FENCE_RE = re.compile(r"```[^\n]*\n([\s\S]*?)\n```", re.MULTILINE)


class ManifestApplyError(Exception):
    pass


def _is_unsafe_relpath(p: str) -> bool:
    # Reject absolute paths, drive letters, home, and traversal.
    if not p or p.strip() != p:
        return True
    if p.startswith(("/", "\\", "~")):
        return True
    if ":" in p.split("/")[0].split("\\")[0]:
        return True
    parts = Path(p).parts
    if any(part in ("..",) for part in parts):
        return True
    return False


def _normalize_manifest_path(p: str) -> str:
    """
    Normalize common prefixes from model output.
    Our target_root is already artifacts/<run_id>/generated_app, but agents often
    emit paths starting with 'generated_app/...'. Strip that prefix if present.
    """
    p2 = p.replace("\\", "/")
    if p2.startswith("generated_app/"):
        return p2[len("generated_app/") :]
    return p2


def _extract_fenced_code(content: str) -> str:
    m = _FENCE_RE.search(content)
    if not m:
        # Be forgiving: some agents may set fenced_code without actually adding fences.
        # In that case, fall back to writing literal content so runs don't hard-fail.
        return content
    return m.group(1)


def apply_manifest(manifest: FileManifest, target_root: Path) -> list[Path]:
    """
    Apply a FileManifest under target_root (e.g. artifacts/<run_id>/generated_app).
    Returns list of written file paths (absolute).
    """
    target_root = target_root.resolve()
    written: list[Path] = []

    for entry in manifest.files:
        rel_path = _normalize_manifest_path(entry.path)
        if _is_unsafe_relpath(rel_path):
            raise ManifestApplyError(f"Unsafe path in manifest: {entry.path!r}")

        out_path = (target_root / rel_path).resolve()
        if target_root not in out_path.parents and out_path != target_root:
            raise ManifestApplyError(f"Path escapes target root: {entry.path!r}")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.exists() and not entry.overwrite:
            continue

        content = entry.content
        if entry.content_mode == "fenced_code":
            content = _extract_fenced_code(content)

        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)

    return written

