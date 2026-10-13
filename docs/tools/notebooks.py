"""Execute derham notebooks in ``guides/`` and convert them into Starlight MDX pages.

``execute``
    Runs each notebook with nbclient into ``docs/.cache/notebooks/<slug>.ipynb``. A notebook is
    rerun only when the hash of its cells changes (``--force`` reruns all of them).
``convert``
    Writes ``docs/src/content/docs/guides/<slug>.mdx`` from the executed copy, the images into
    ``docs/public/guides/<slug>/`` and a downloadable copy of the notebook next to them.
    Notebooks that have not been executed are converted without outputs (``--strict`` fails on
    them, and on notebooks whose run raised).
``clean``
    Removes the cache, the generated pages and the public assets.

Usage: python docs/tools/notebooks.py <execute|convert|clean> [options]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

DOCS = Path(__file__).resolve().parents[1]
REPO = DOCS.parent
NOTEBOOKS = REPO / "guides"
CACHE = DOCS / ".cache" / "notebooks"
CONTENT = DOCS / "src" / "content" / "docs" / "guides"
PUBLIC = DOCS / "public" / "guides"
COMPONENTS = "../../../components"


def slug_of(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")


def notebooks() -> list[Path]:
    return sorted(NOTEBOOKS.glob("*.ipynb"))


# Execution ------------------------------------------------------------------------------- #


def cell_hash(path: Path) -> str:
    nb = json.loads(path.read_text())
    cells = [
        {
            "type": c["cell_type"],
            "source": c["source"],
            "tags": c.get("metadata", {}).get("tags", []),
        }
        for c in nb["cells"]
    ]
    return hashlib.sha256(json.dumps(cells, sort_keys=True).encode()).hexdigest()[:16]


def execute_notebook(path: Path, target: Path, timeout: int) -> None:
    import nbformat
    from nbclient import NotebookClient

    from jupyter_client.kernelspec import KernelSpec
    from jupyter_client.manager import KernelManager

    nb = nbformat.read(path, as_version=4)
    km = KernelManager(kernel_name="python3")
    km._kernel_spec = KernelSpec(
        argv=[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        language="python", display_name="Python 3 (docs)",
    )
    client = NotebookClient(
        nb,
        km=km,
        timeout=timeout,
        resources={"metadata": {"path": str(path.parent)}},
    )
    error = None
    try:
        client.execute()
    except Exception as exc:  # the partial outputs are still written for the page
        error = f"{type(exc).__name__}: {exc}"
    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, target)
    error_file = target.with_suffix(".error")
    if error:
        error_file.write_text(error)
    else:
        error_file.unlink(missing_ok=True)


def cmd_execute(args: argparse.Namespace) -> None:
    failed = []
    for path in notebooks():
        slug = slug_of(path)
        target = CACHE / f"{slug}.ipynb"
        key_file = CACHE / f"{slug}.key"
        key = cell_hash(path)
        if (
            not args.force
            and target.exists()
            and key_file.exists()
            and key_file.read_text() == key
            and not target.with_suffix(".error").exists()
        ):
            print(f"[notebooks] {slug}: up to date")
            continue
        print(f"[notebooks] {slug}: executing", flush=True)
        execute_notebook(path, target, args.timeout)
        key_file.write_text(key)
        error_file = target.with_suffix(".error")
        if error_file.exists():
            failed.append(slug)
            print(f"[notebooks] {slug}: FAILED: {error_file.read_text()}")
    if failed:
        print(f"[notebooks] {len(failed)} failed: {', '.join(failed)}")
        sys.exit(1)


# Conversion: markdown ---------------------------------------------------------------------- #

# Regions whose contents MDX must not touch: code fences, inline code and math.
_PROTECTED = re.compile(
    r"(?P<fence>^(?P<ticks>`{3,}|~{3,})[^\n]*\n.*?^(?P=ticks)[ \t]*$)"
    r"|(?P<display>\$\$.+?\$\$)"
    r"|(?P<bracket>\\\[.+?\\\])"
    r"|(?P<code>(?P<bt>`+).+?(?P=bt))"
    r"|(?P<inline>(?<![\\$])\$(?!\s)(?:[^$\n\\]|\\.)+?(?<!\s)\$(?!\d))"
    r"|(?P<paren>\\\(.+?\\\))",
    re.DOTALL | re.MULTILINE,
)
_VOID_TAGS = re.compile(
    r"<(br|hr|img|input|meta|link|source)\b([^>]*?)\s*/?>", re.IGNORECASE
)
_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(\s[^<>]*)?/?>")
_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _escape_plain(text: str) -> str:
    return (
        text.replace("{", "\\{")
        .replace("}", "\\}")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _escape_text(text: str) -> str:
    """Escape what MDX would parse in plain markdown text: braces, stray <, comments."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = _VOID_TAGS.sub(lambda m: f"<{m.group(1)}{m.group(2)} />", text)
    out = []
    position = 0
    for match in _TAG.finditer(text):
        out.append(_escape_plain(text[position : match.start()]))
        out.append(
            re.sub(r'\sstyle="[^"]*"', "", match.group(0))
        )  # JSX wants style objects
        position = match.end()
    out.append(_escape_plain(text[position:]))
    return "".join(out)


def sanitize_markdown(text: str) -> str:
    """Make notebook markdown valid MDX, keeping code and math as they are."""
    out = []
    position = 0
    for match in _PROTECTED.finditer(text):
        out.append(_escape_text(text[position : match.start()]))
        chunk = match.group(0)
        if match.group("bracket"):
            out.append("\n$$\n" + chunk[2:-2].strip() + "\n$$\n")
        elif match.group("paren"):
            out.append("$" + chunk[2:-2].strip() + "$")
        else:
            out.append(chunk)
        position = match.end()
    out.append(_escape_text(text[position:]))
    return "".join(out)


def _first_heading(markdown: str) -> tuple[str | None, str]:
    """Split off the first ``# Title`` line; return (title, the rest)."""
    lines = markdown.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            return line.strip()[2:].strip(), "\n".join(lines[:i] + lines[i + 1 :])
        if line.strip():
            break
    return None, markdown


def _plain(text: str) -> str:
    """Markdown to plain text for a title or description."""
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\$([^$]+)\$", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_#>{}]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _description(markdown: str) -> str:
    for paragraph in re.split(r"\n\s*\n", markdown):
        stripped = paragraph.strip()
        if not stripped or stripped.startswith(("#", "|", "-", "*", "```", "$$", "<")):
            continue
        plain = _plain(stripped)
        if len(plain) > 20:
            return plain[:200].rsplit(" ", 1)[0] + "…" if len(plain) > 200 else plain
    return ""


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


# Conversion: outputs ----------------------------------------------------------------------- #


class Page:
    def __init__(self, slug: str) -> None:
        self.slug = slug
        self.public = PUBLIC / slug
        self.components: set[str] = set()
        self.errors: list[str] = []
        self.assets = 0

    def asset(self, suffix: str) -> tuple[Path, str]:
        self.assets += 1
        self.public.mkdir(parents=True, exist_ok=True)
        name = f"{self.assets}{suffix}"
        return self.public / name, f"/guides/{self.slug}/{name}"


def _fence(text: str, language: str = "text") -> str:
    text = _ANSI.sub("", text).rstrip("\n")
    if not text.strip():
        return ""
    lines = text.splitlines()
    if len(lines) > 200:
        lines = (
            lines[:100] + [f"... ({len(lines) - 200} lines skipped) ..."] + lines[-100:]
        )
        text = "\n".join(lines)
    ticks = "```"
    while ticks in text:
        ticks += "`"
    return f"{ticks}{language}\n{text}\n{ticks}"


def _text(value: Any) -> str:
    return "".join(value) if isinstance(value, list) else str(value)


def merge_streams(outputs: list[dict]) -> list[dict]:
    """Join consecutive stream outputs of the same stream (one print per line otherwise)."""
    merged: list[dict] = []
    for output in outputs:
        previous = merged[-1] if merged else None
        if (
            output.get("output_type") == "stream"
            and previous is not None
            and previous.get("output_type") == "stream"
            and previous.get("name") == output.get("name")
        ):
            previous["text"] = _text(previous["text"]) + _text(output.get("text", ""))
        else:
            merged.append(dict(output))
    return merged


def convert_output(output: dict, page: Page, tags: list[str], index: int) -> str:
    kind = output.get("output_type")
    if kind == "stream":
        return _fence(_text(output.get("text", "")))
    if kind == "error":
        if "raises-exception" not in tags:
            page.errors.append(
                f"cell {index}: {output.get('ename')}: {output.get('evalue')}"
            )
        return _fence(_ANSI.sub("", "\n".join(output.get("traceback", []))))
    data = output.get("data", {})
    if "image/png" in data or "image/jpeg" in data:
        mime = "image/png" if "image/png" in data else "image/jpeg"
        path, url = page.asset(".png" if mime == "image/png" else ".jpg")
        path.write_bytes(base64.b64decode(_text(data[mime])))
        page.components.add("NotebookImage")
        return f'<NotebookImage src="{url}" />'
    if "image/svg+xml" in data:
        page.components.add("RawHtml")
        return f"<RawHtml html={{{json.dumps(_text(data['image/svg+xml']))}}} />"
    if "text/html" in data:
        page.components.add("RawHtml")
        return f"<RawHtml html={{{json.dumps(_text(data['text/html']))}}} />"
    if "text/markdown" in data:
        return sanitize_markdown(_text(data["text/markdown"]))
    if "text/latex" in data:
        return "\n$$\n" + _text(data["text/latex"]).strip().strip("$") + "\n$$\n"
    if "text/plain" in data:
        return _fence(_text(data["text/plain"]))
    return ""


# Conversion: pages ------------------------------------------------------------------------- #


def convert_notebook(source: Path, executed: Path | None, order: int) -> Page:
    import nbformat

    slug = slug_of(source)
    nb = nbformat.read(executed or source, as_version=4)
    page = Page(slug)
    shutil.rmtree(page.public, ignore_errors=True)
    title = None
    description = ""
    body = []
    for index, cell in enumerate(nb.cells):
        tags = list(cell.metadata.get("tags", []))
        if "remove-cell" in tags:
            continue
        if cell.cell_type == "markdown":
            text = cell.source
            if title is None:
                heading, text = _first_heading(text)
                if heading:
                    title = _plain(heading)
            if not description:
                description = _description(text)
            for name, bundle in cell.get("attachments", {}).items():
                for mime, payload in bundle.items():
                    if mime.startswith("image/"):
                        path, url = page.asset(Path(name).suffix or ".png")
                        path.write_bytes(base64.b64decode(_text(payload)))
                        text = text.replace(f"attachment:{name}", url)
            body.append(sanitize_markdown(text).strip())
        elif cell.cell_type == "code":
            if cell.source.strip() and "hide-input" not in tags:
                code = _fence(cell.source, "python")
                if "fold-input" in tags:
                    code = (
                        "<details>\n<summary>Show code</summary>\n\n"
                        + code
                        + "\n\n</details>"
                    )
                body.append(code)
            if "remove-output" in tags:
                continue
            for output in merge_streams(cell.get("outputs", [])):
                converted = convert_output(output, page, tags, index)
                if converted:
                    body.append(converted)
    title = title or source.stem.replace("_", " ").capitalize()
    imports = [f"import NotebookHeader from '{COMPONENTS}/NotebookHeader.astro';"]
    imports += [
        f"import {name} from '{COMPONENTS}/{name}.astro';"
        for name in sorted(page.components)
    ]
    page.public.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, page.public / source.name)
    status = "executed" if executed else "not run"
    frontmatter = [
        "---",
        f"title: {_yaml_string(title)}",
        f"description: {_yaml_string(description or title)}",
        "sidebar:",
        f"  order: {nb.metadata.get('guide', {}).get('order', order)}",
        "---",
    ]
    header = (
        f'<NotebookHeader download="/guides/{slug}/{source.name}" '
        f'source="guides/{source.name}" status="{status}" />'
    )
    text = (
        "\n".join(frontmatter) + "\n\n" + "\n".join(imports) + "\n\n" + header + "\n\n"
    )
    text += "\n\n".join(part for part in body if part) + "\n"
    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / f"{slug}.mdx").write_text(text)
    return page


def cmd_convert(args: argparse.Namespace) -> None:
    expected = {f"{slug_of(path)}.mdx" for path in notebooks()}
    for stale in CONTENT.glob("*.mdx"):
        if stale.name not in expected:
            stale.unlink()
    problems = []
    for order, source in enumerate(notebooks(), start=1):
        slug = slug_of(source)
        executed = CACHE / f"{slug}.ipynb"
        error_file = executed.with_suffix(".error")
        fresh = executed.exists() and cell_hash(executed) == cell_hash(source)
        page = convert_notebook(source, executed if fresh else None, order)
        state = "executed" if fresh else "not run"
        if error_file.exists():
            problems.append(f"{slug}: run failed: {error_file.read_text().strip()}")
        elif not fresh:
            problems.append(f"{slug}: not executed or source changed")
        problems += [f"{slug}: {error}" for error in page.errors]
        print(
            f"[notebooks] {slug}: {state}, {page.assets} assets -> {CONTENT / slug}.mdx"
        )
    for problem in problems:
        print(f"[notebooks] warning: {problem}")
    if args.strict and problems:
        sys.exit(1)


def cmd_clean(args: argparse.Namespace) -> None:
    shutil.rmtree(CACHE, ignore_errors=True)
    shutil.rmtree(PUBLIC, ignore_errors=True)
    for page in CONTENT.glob("*.mdx"):
        page.unlink()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    execute = sub.add_parser("execute", help="run the notebooks whose cells changed")
    execute.add_argument("--force", action="store_true", help="rerun every notebook")
    execute.add_argument("--timeout", type=int, default=600, help="seconds per cell")
    execute.set_defaults(func=cmd_execute)
    convert = sub.add_parser("convert", help="write the MDX pages and assets")
    convert.add_argument(
        "--strict", action="store_true", help="fail on missing or failed runs"
    )
    convert.set_defaults(func=cmd_convert)
    clean = sub.add_parser("clean", help="remove the cache and generated files")
    clean.set_defaults(func=cmd_clean)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
