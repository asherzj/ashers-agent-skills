#!/usr/bin/env python3
"""Deterministic HTML-to-PDF resume pipeline for the write-resume skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Sequence
from unicodedata import normalize


SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parent.parent
TEMPLATE_PATH = SKILL_DIR / "references" / "anonymized-growth-product-manager-resume.html"
PROVENANCE_RE = re.compile(
    r"<!--\s*resume-pipeline:\s*template-sha256=([0-9a-f]{64})\s*-->"
)

DEFAULT_FORBIDDEN_TERMS = (
    "候选人姓名",
    "手机号占位",
    "YYYY.MM",
    "大型互联网公司 A",
    "互联网平台公司 B",
    "企业服务公司 C",
    "运营分层策略引擎重构",
    "ROI 从 0.92",
    "沉默商家激活率",
    "某理工类高校",
)

STRUCTURAL_TOKENS = (
    '<main class="resume">',
    "@media print",
    "@page",
    "size: A4",
    "section-title",
    "--blue-light",
)

COMMON_CHROME_PATHS = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
)

COMMON_ATS_FONT_PATHS = (
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
)

PINGFANG_SEARCH_ROOTS = (
    Path("/System/Library/AssetsV2/com_apple_MobileAsset_Font8"),
    Path("/System/Library/AssetsV2/PreinstalledAssetsV2/InstallWithOs/com_apple_MobileAsset_Font7"),
)

PINGFANG_OUTPUTS = {
    "Regular": ("PingFangSC-Regular.ttf", 400),
    "Medium": ("PingFangSC-Medium.ttf", 500),
    "Semibold": ("PingFangSC-Semibold.ttf", 600),
}

# These are hard quality gates, not tuning knobs. A wrapped prose block, title,
# contact line, or bullet with a tiny final fragment is difficult to scan even
# when the PDF is otherwise valid.
MIN_BLOCK_LAST_LINE_CHARS = 8
MIN_BLOCK_LAST_LINE_FILL = 0.15
DEFAULT_MIN_NONFINAL_FILL = 0.82
BULLET_PREFIX_CHARS = "•●▪◦·‣⁃-–—"
MONITORED_DIV_CLASSES = {"contact", "target", "item-subtitle", "mock-banner"}


class PipelineError(RuntimeError):
    pass


class ResumeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_body = False
        self.skip_depth = 0
        self.current_h2: list[str] | None = None
        self.current_li: list[str] | None = None
        self.current_layout_tag: str | None = None
        self.current_layout_kind: str | None = None
        self.current_layout_chunks: list[str] | None = None
        self.body_chunks: list[str] = []
        self.section_titles: list[str] = []
        self.list_items: list[str] = []
        self.layout_blocks: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        classes = set((dict(attrs).get("class") or "").split())
        if tag == "body":
            self.in_body = True
        if tag in {"script", "style"}:
            self.skip_depth += 1
        if self.in_body and self.skip_depth == 0 and tag == "h2":
            self.current_h2 = []
        if self.in_body and self.skip_depth == 0 and tag == "li":
            if self.current_li is not None:
                fail("Nested list items are not supported by the resume layout validator.")
            self.current_li = []
        block_kind: str | None = None
        if self.in_body and self.skip_depth == 0:
            if tag == "li":
                block_kind = "bullet"
            elif tag == "p":
                block_kind = next(
                    (f"paragraph.{name}" for name in sorted(classes) if name),
                    "paragraph",
                )
            elif tag == "h3" and "project-title" in classes:
                block_kind = "project-title"
            elif tag == "div":
                monitored = sorted(classes & MONITORED_DIV_CLASSES)
                if monitored:
                    block_kind = monitored[0]
        if block_kind is not None:
            if self.current_layout_chunks is not None:
                fail("Nested monitored text blocks are not supported by the layout validator.")
            self.current_layout_tag = tag
            self.current_layout_kind = block_kind
            self.current_layout_chunks = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "h2" and self.current_h2 is not None:
            title = clean_text("".join(self.current_h2))
            if title:
                self.section_titles.append(title)
            self.current_h2 = None
        if tag == "li" and self.current_li is not None:
            item = clean_text("".join(self.current_li))
            if item:
                self.list_items.append(item)
            self.current_li = None
        if tag == self.current_layout_tag and self.current_layout_chunks is not None:
            block_text = clean_text("".join(self.current_layout_chunks))
            if block_text:
                self.layout_blocks.append(
                    {
                        "kind": self.current_layout_kind or tag,
                        "text": block_text,
                    }
                )
            self.current_layout_tag = None
            self.current_layout_kind = None
            self.current_layout_chunks = None
        if tag == "body":
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if not self.in_body or self.skip_depth:
            return
        value = clean_text(data)
        if not value:
            return
        self.body_chunks.append(value)
        if self.current_h2 is not None:
            self.current_h2.append(value)
        if self.current_li is not None:
            self.current_li.append(value)
        if self.current_layout_chunks is not None:
            self.current_layout_chunks.append(data)


def fail(message: str) -> None:
    raise PipelineError(message)


def clean_text(value: str) -> str:
    return " ".join(normalize("NFKC", value).split())


def compact_text(value: str) -> str:
    return re.sub(r"\s+", "", clean_text(value)).casefold()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_pdf_runtime() -> None:
    try:
        import fontTools  # noqa: F401
        import pdfplumber  # noqa: F401
        import pypdf  # noqa: F401

        return
    except ImportError:
        pass

    bundled_python = (
        Path.home()
        / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
    )
    if (
        bundled_python.exists()
        and Path(sys.executable).resolve() != bundled_python.resolve()
        and os.environ.get("RESUME_PIPELINE_REEXEC") != "1"
    ):
        new_env = os.environ.copy()
        new_env["RESUME_PIPELINE_REEXEC"] = "1"
        os.execve(
            bundled_python,
            [str(bundled_python), str(SCRIPT_PATH), *sys.argv[1:]],
            new_env,
        )

    fail(
        "Python packages 'fonttools', 'pypdf', and 'pdfplumber' are required. Run with "
        "the Codex bundled Python or install them in the active runtime."
    )


def first_existing(paths: Iterable[Path]) -> Path | None:
    for path in paths:
        if path.is_file() and os.access(path, os.X_OK):
            return path
    return None


def find_pingfang_ttc() -> Path:
    for root in PINGFANG_SEARCH_ROOTS:
        if not root.is_dir():
            continue
        matches = sorted(root.glob("*.asset/AssetData/PingFang.ttc"))
        if matches:
            return matches[0].resolve()
    fail(
        "PingFang.ttc was not found in the macOS system font assets. The resume skill "
        "requires PingFang SC for Chinese text; do not silently substitute another font."
    )


def prepare_pingfang_fonts(html_path: Path, html_parser: ResumeHTMLParser) -> dict[str, object]:
    from fontTools.subset import Options, Subsetter
    from fontTools.ttLib import TTCollection

    source_path = find_pingfang_ttc()
    visible_text = " ".join(html_parser.body_chunks)
    unicode_points = {ord(char) for char in visible_text if not char.isspace()}
    if not unicode_points:
        fail("Cannot prepare PingFang SC subsets because the HTML body has no visible text.")

    collection = TTCollection(str(source_path))
    selected: dict[str, object] = {}
    for font in collection.fonts:
        family = font["name"].getDebugName(1)
        style = font["name"].getDebugName(2)
        if family == "PingFang SC" and style in PINGFANG_OUTPUTS:
            selected[style] = font

    missing = sorted(set(PINGFANG_OUTPUTS) - set(selected))
    if missing:
        collection.close()
        fail(f"PingFang SC collection is missing required faces: {missing}")

    output_dir = html_path.parent / "resume-fonts"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, dict[str, object]] = {}
    for style, (filename, css_weight) in PINGFANG_OUTPUTS.items():
        target = output_dir / filename
        temporary = output_dir / f".{filename}.tmp"
        font = selected[style]
        subsetter = Subsetter(options=Options())
        subsetter.populate(unicodes=unicode_points)
        subsetter.subset(font)
        font.save(temporary)
        os.replace(temporary, target)
        outputs[style] = {
            "path": str(target),
            "css_weight": css_weight,
            "size_bytes": target.stat().st_size,
        }
    collection.close()
    return {
        "source": str(source_path),
        "visible_unicode_count": len(unicode_points),
        "outputs": outputs,
    }


def find_chrome(explicit: str | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("CHROME_PATH"):
        candidates.append(Path(os.environ["CHROME_PATH"]).expanduser())
    candidates.extend(COMMON_CHROME_PATHS)
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        located = shutil.which(name)
        if located:
            candidates.append(Path(located))
    found = first_existing(candidates)
    if not found:
        fail("Chrome/Chromium not found. Set CHROME_PATH or pass --chrome.")
    return found.resolve()


def find_pdftoppm(explicit: str | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("PDFTOPPM_PATH"):
        candidates.append(Path(os.environ["PDFTOPPM_PATH"]).expanduser())
    located = shutil.which("pdftoppm")
    if located:
        candidates.append(Path(located))
    runtime_root = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin"
    candidates.extend(
        (
            runtime_root / "override" / "pdftoppm",
            runtime_root / "fallback" / "pdftoppm",
        )
    )
    found = first_existing(candidates)
    if not found:
        fail("pdftoppm not found. Set PDFTOPPM_PATH or install Poppler.")
    return found.resolve()


def parse_html(html_text: str) -> ResumeHTMLParser:
    parser = ResumeHTMLParser()
    parser.feed(html_text)
    parser.close()
    if not parser.body_chunks:
        fail("HTML body has no visible text.")
    return parser


def validate_html_source(
    html_path: Path,
    *,
    allow_stale_template: bool,
    extra_forbidden_terms: Sequence[str],
) -> tuple[str, ResumeHTMLParser, str]:
    if not html_path.is_file():
        fail(f"HTML source not found: {html_path}")
    if html_path.resolve() == TEMPLATE_PATH.resolve():
        fail("Refusing to build the canonical template. Run 'init' and edit the copied file.")

    html_text = html_path.read_text(encoding="utf-8")
    marker = PROVENANCE_RE.search(html_text)
    if not marker:
        fail("Missing template fingerprint. Create this file with 'resume_pipeline.py init'.")

    current_template_sha = sha256_file(TEMPLATE_PATH)
    copied_template_sha = marker.group(1)
    if copied_template_sha != current_template_sha and not allow_stale_template:
        fail(
            "The copied HTML was created from an older template. Re-run 'init', or pass "
            "--allow-stale-template only when the difference has been reviewed."
        )

    missing_structure = [token for token in STRUCTURAL_TOKENS if token not in html_text]
    if missing_structure:
        fail(f"Template structure was removed: {missing_structure}")

    parser = parse_html(html_text)
    compact_html = compact_text(" ".join(parser.body_chunks))
    forbidden = [*DEFAULT_FORBIDDEN_TERMS, *extra_forbidden_terms]
    leftovers = [term for term in forbidden if compact_text(term) in compact_html]
    if leftovers:
        fail(f"Template/sample text still present: {leftovers}")

    has_cjk = bool(re.search(r"[\u3400-\u9fff]", " ".join(parser.body_chunks)))
    if has_cjk and "ResumeArialUnicode" not in html_text:
        fail(
            "ATS-safe CJK font declaration is missing. Re-copy the current template or "
            "restore the ResumeArialUnicode @font-face block."
        )

    return html_text, parser, current_template_sha


def render_pdf(chrome: Path, html_path: Path, candidate_pdf: Path, timeout: int) -> None:
    chrome_log = candidate_pdf.parent / "chrome.log"
    pdf_ready = False
    timed_out = False
    with tempfile.TemporaryDirectory(prefix="resume-chrome-profile-") as profile_dir:
        command = [
            str(chrome),
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-extensions",
            "--no-first-run",
            "--no-default-browser-check",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--user-data-dir={profile_dir}",
            f"--print-to-pdf={candidate_pdf}",
            html_path.resolve().as_uri(),
        ]
        started = time.monotonic()
        last_size = -1
        unchanged_since = started
        with chrome_log.open("w", encoding="utf-8") as log_stream:
            process = subprocess.Popen(
                command,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

            while True:
                now = time.monotonic()
                return_code = process.poll()
                size = candidate_pdf.stat().st_size if candidate_pdf.is_file() else 0
                if size != last_size:
                    last_size = size
                    unchanged_since = now
                elif size >= 10_000 and now - unchanged_since >= 1.5:
                    pdf_ready = True
                    break

                if return_code is not None:
                    pdf_ready = size >= 10_000
                    break
                if now - started >= timeout:
                    timed_out = True
                    break
                time.sleep(0.25)

            if process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=5)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        pass
            return_code = process.poll()

    if not pdf_ready:
        log_tail = chrome_log.read_text(encoding="utf-8", errors="replace")[-2000:]
        if timed_out:
            fail(f"Chrome timed out after {timeout}s before producing a stable PDF:\n{log_tail}")
        fail(f"Chrome exited with code {return_code} without a usable PDF:\n{log_tail}")
    if not candidate_pdf.is_file() or candidate_pdf.stat().st_size < 10_000:
        fail(
            "Chrome returned without a usable PDF. In Codex, rerun the same build command "
            "with the required GUI/sandbox approval; do not bypass the pipeline."
        )


def has_cjk_radical_leak(text: str) -> list[str]:
    leaked = {
        char
        for char in text
        if "\u2e80" <= char <= "\u2eff" or "\u2f00" <= char <= "\u2fdf"
    }
    return sorted(leaked)


def is_cjk_ideograph(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x20000 <= codepoint <= 0x2FA1F
    )


def inspect_pdf_fonts(
    pdf_path: Path, html_parser: ResumeHTMLParser
) -> dict[str, object]:
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    import pdfplumber

    cjk_fonts: set[str] = set()
    latin_fonts: set[str] = set()
    with pdfplumber.open(pdf_path) as document:
        for page in document.pages:
            for glyph in page.chars:
                font_name = str(glyph.get("fontname") or "")
                for char in str(glyph.get("text") or ""):
                    if is_cjk_ideograph(char):
                        cjk_fonts.add(font_name)
                    elif char.isascii() and char.isalnum():
                        latin_fonts.add(font_name)

    unexpected_cjk = sorted(name for name in cjk_fonts if "PingFangSC" not in name)
    if unexpected_cjk:
        fail(f"Chinese text is not fully rendered with PingFang SC: {unexpected_cjk}")
    unexpected_latin = sorted(
        name for name in latin_fonts if ".SFNS" not in name and "SFPro" not in name
    )
    if unexpected_latin:
        fail(f"Latin text or numerals are not fully rendered with SF Pro: {unexpected_latin}")
    html_text = " ".join(html_parser.body_chunks)
    expects_cjk = any(is_cjk_ideograph(char) for char in html_text)
    expects_latin = any(char.isascii() and char.isalnum() for char in html_text)
    if expects_cjk and not cjk_fonts:
        fail("No PingFang SC Chinese glyphs were found in the generated PDF.")
    if expects_latin and not latin_fonts:
        fail("No SF Pro Latin or numeric glyphs were found in the generated PDF.")
    return {
        "status": "passed",
        "cjk_fonts": sorted(cjk_fonts),
        "latin_fonts": sorted(latin_fonts),
    }


def meaningful_char_count(value: str) -> int:
    return sum(1 for char in normalize("NFKC", value) if char.isalnum())


def compact_pdf_line(value: str) -> str:
    return compact_text(value).lstrip(BULLET_PREFIX_CHARS)


def extract_pdf_visual_lines(pdf_path: Path) -> list[dict[str, object]]:
    # pdfminer logs one FontBBox warning per affected glyph for some otherwise
    # valid embedded fonts. The ATS checks below remain authoritative.
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    import pdfplumber

    visual_lines: list[dict[str, object]] = []
    with pdfplumber.open(pdf_path) as document:
        for page_number, page in enumerate(document.pages, start=1):
            page_lines: list[dict[str, object]] = []
            for extracted in page.extract_text_lines(
                layout=False,
                strip=True,
                return_chars=True,
            ):
                text = clean_text(str(extracted.get("text", "")))
                if not text:
                    continue
                page_lines.append(
                    {
                        "page": page_number,
                        "text": text,
                        "compact": compact_pdf_line(text),
                        "x0": float(extracted["x0"]),
                        "x1": float(extracted["x1"]),
                        "top": float(extracted["top"]),
                    }
                )

            body_right = max(
                (float(line["x1"]) for line in page_lines),
                default=float(page.width),
            )
            for line in page_lines:
                line["body_right"] = body_right
                visual_lines.append(line)
    return visual_lines


def match_text_block_lines(
    block_text: str,
    visual_lines: Sequence[dict[str, object]],
    cursor: int,
) -> tuple[list[dict[str, object]], int] | None:
    target = compact_text(block_text)
    for start in range(cursor, len(visual_lines)):
        remaining = target
        matched: list[dict[str, object]] = []
        position = start
        while remaining and position < len(visual_lines):
            line = visual_lines[position]
            fragment = str(line["compact"])
            if not fragment or not remaining.startswith(fragment):
                break
            matched.append(line)
            remaining = remaining[len(fragment) :]
            position += 1
        if matched and not remaining:
            return matched, position
    return None


def match_list_item_lines(
    item: str,
    visual_lines: Sequence[dict[str, object]],
    cursor: int,
) -> tuple[list[dict[str, object]], int] | None:
    """Backward-compatible alias used by older diagnostic harnesses."""
    return match_text_block_lines(item, visual_lines, cursor)


def inspect_wrapped_text_blocks(
    pdf_path: Path,
    html_parser: ResumeHTMLParser,
) -> dict[str, object]:
    visual_lines = extract_pdf_visual_lines(pdf_path)
    cursor = 0
    wrapped_count = 0
    checked: list[dict[str, object]] = []
    violations: list[dict[str, object]] = []

    kinds_checked: dict[str, int] = {}
    for block_number, block in enumerate(html_parser.layout_blocks, start=1):
        kind = block["kind"]
        block_text = block["text"]
        kinds_checked[kind] = kinds_checked.get(kind, 0) + 1
        match = match_text_block_lines(block_text, visual_lines, cursor)
        if match is None:
            preview = block_text if len(block_text) <= 80 else f"{block_text[:77]}..."
            fail(
                "Could not map an HTML text block to PDF visual lines; orphan-line "
                f"validation cannot be trusted. Block {block_number} ({kind}): {preview}"
            )
        matched_lines, cursor = match
        if len(matched_lines) < 2:
            continue

        wrapped_count += 1
        last_line = matched_lines[-1]
        last_text = str(last_line["text"])
        char_count = meaningful_char_count(last_text)
        available_width = max(
            max(float(line["x1"]) - float(line["x0"]) for line in matched_lines[:-1]),
            1.0,
        )
        fill_ratio = (float(last_line["x1"]) - float(last_line["x0"])) / available_width
        record = {
            "block_number": block_number,
            "block_kind": kind,
            "page": int(last_line["page"]),
            "line_count": len(matched_lines),
            "last_line": last_text,
            "last_line_meaningful_chars": char_count,
            "last_line_fill_ratio": round(fill_ratio, 4),
            "block": block_text,
        }
        checked.append(record)
        if char_count < MIN_BLOCK_LAST_LINE_CHARS or fill_ratio < MIN_BLOCK_LAST_LINE_FILL:
            violations.append(record)

    if violations:
        details = []
        for issue in violations:
            block_text = str(issue["block"])
            preview = block_text if len(block_text) <= 90 else f"{block_text[:87]}..."
            details.append(
                "- page {page}, block {block_number} ({block_kind}): last line {last_line!r} "
                "({last_line_meaningful_chars} meaningful chars, {fill:.1%} width); "
                "block={block_preview!r}".format(
                    page=issue["page"],
                    block_number=issue["block_number"],
                    block_kind=issue["block_kind"],
                    last_line=issue["last_line"],
                    last_line_meaningful_chars=issue[
                        "last_line_meaningful_chars"
                    ],
                    fill=float(issue["last_line_fill_ratio"]),
                    block_preview=preview,
                )
            )
        fail(
            "Wrapped text-block orphan lines detected. Every monitored block's final line "
            f"must contain at least {MIN_BLOCK_LAST_LINE_CHARS} meaningful characters and "
            f"fill at least {MIN_BLOCK_LAST_LINE_FILL:.0%} of the block's reference line "
            "width. Rewrite or shorten the text; do not shrink the global font or page "
            "margins to bypass "
            "this check.\n" + "\n".join(details)
        )

    return {
        "status": "passed",
        "blocks_checked": len(html_parser.layout_blocks),
        "blocks_checked_by_kind": kinds_checked,
        "wrapped_blocks_checked": wrapped_count,
        "minimum_last_line_meaningful_chars": MIN_BLOCK_LAST_LINE_CHARS,
        "minimum_last_line_fill_ratio": MIN_BLOCK_LAST_LINE_FILL,
        "wrapped_blocks": checked,
    }


def inspect_pdf(
    pdf_path: Path,
    html_parser: ResumeHTMLParser,
    *,
    expected_pages: int | None,
    required_terms: Sequence[str],
    min_text_chars: int,
) -> dict[str, object]:
    ensure_pdf_runtime()
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        fail("Generated PDF is unexpectedly encrypted.")
    page_count = len(reader.pages)
    if page_count == 0:
        fail("Generated PDF has no pages.")
    if expected_pages is not None and page_count != expected_pages:
        fail(f"Expected {expected_pages} pages, generated {page_count}.")

    page_sizes: list[list[float]] = []
    raw_pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        page_sizes.append([round(width, 2), round(height, 2)])
        if abs(width - 595.0) > 4.0 or abs(height - 842.0) > 4.0:
            fail(f"Page {index} is not portrait A4: {width:.2f} x {height:.2f} pt")
        raw_text = page.extract_text() or ""
        if len(compact_text(raw_text)) < min_text_chars:
            fail(f"Page {index} has too little extractable text; it may be blank or image-only.")
        raw_pages.append(raw_text)

    raw_text = "\n".join(raw_pages)
    leaked = has_cjk_radical_leak(raw_text)
    if leaked:
        preview = " ".join(leaked[:12])
        fail(
            "ATS text mapping contains CJK radical code points "
            f"({preview}). Rebuild the per-resume PingFang SC subsets and try again."
        )

    font_check = inspect_pdf_fonts(pdf_path, html_parser)

    normalized_pdf = clean_text(raw_text)
    compact_pdf = compact_text(raw_text)
    first_body = compact_text(html_parser.body_chunks[0])
    if first_body and not compact_pdf.startswith(first_body):
        fail(
            "PDF text starts before the first HTML body item. Browser headers/footers or "
            "reading-order corruption may be present."
        )
    if "file:///" in raw_text.casefold():
        fail("Browser file URL/header text detected.")

    section_positions: list[int] = []
    section_anchors: list[dict[str, object]] = []
    cursor = 0
    for section in html_parser.section_titles:
        needle = compact_text(section)
        position = compact_pdf.find(needle, cursor)
        if position < 0:
            fail(f"Section missing or out of reading order in PDF: {section}")
        section_positions.append(position)
        cursor = position + len(needle)

        body_index = next(
            (
                index
                for index, chunk in enumerate(html_parser.body_chunks)
                if compact_text(chunk) == needle
            ),
            -1,
        )
        anchor = next(
            (
                chunk
                for chunk in html_parser.body_chunks[body_index + 1 :]
                if compact_text(chunk) and compact_text(chunk) != needle
            ),
            None,
        )
        if anchor:
            anchor_position = compact_pdf.find(compact_text(anchor))
            if anchor_position < 0:
                fail(f"First content after section is missing from PDF: {section} -> {anchor}")
            if position >= anchor_position:
                fail(
                    "PDF reading order places a section heading after its content: "
                    f"{section}. Avoid positioned heading elements or pseudo-element bars."
                )
            section_anchors.append(
                {
                    "section": section,
                    "heading_position": position,
                    "first_content": anchor,
                    "first_content_position": anchor_position,
                }
            )

    missing_terms = [term for term in required_terms if compact_text(term) not in compact_pdf]
    if missing_terms:
        fail(f"Required PDF terms missing: {missing_terms}")

    wrapped_text_block_check = inspect_wrapped_text_blocks(pdf_path, html_parser)

    return {
        "page_count": page_count,
        "page_sizes_points": page_sizes,
        "text_lengths": [len(clean_text(text)) for text in raw_pages],
        "section_titles": html_parser.section_titles,
        "section_positions": section_positions,
        "section_anchors": section_anchors,
        "required_terms": list(required_terms),
        "cjk_radical_leak_count": 0,
        "font_check": font_check,
        "header_footer_check": "passed",
        "wrapped_text_block_check": wrapped_text_block_check,
    }


def render_pngs(
    pdftoppm: Path,
    pdf_path: Path,
    run_dir: Path,
    dpi: int,
    expected_count: int,
) -> list[Path]:
    prefix = run_dir / "page"
    command = [str(pdftoppm), "-png", "-r", str(dpi), str(pdf_path), str(prefix)]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"pdftoppm failed:\n{result.stderr[-2000:]}")

    def page_number(path: Path) -> int:
        match = re.search(r"-(\d+)\.png$", path.name)
        return int(match.group(1)) if match else 0

    images = sorted(run_dir.glob("page-*.png"), key=page_number)
    if len(images) != expected_count:
        fail(f"Expected {expected_count} rendered page images, found {len(images)}.")
    return images


def create_contact_sheet(images: Sequence[Path], destination: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False

    opened = [Image.open(path).convert("RGB") for path in images]
    try:
        target_width = min(1100, max(image.width for image in opened))
        resized = []
        for image in opened:
            if image.width == target_width:
                resized.append(image.copy())
                continue
            height = round(image.height * target_width / image.width)
            resized.append(image.resize((target_width, height)))
        gap = 24
        canvas = Image.new(
            "RGB",
            (target_width, sum(image.height for image in resized) + gap * (len(resized) - 1)),
            "white",
        )
        top = 0
        for image in resized:
            canvas.paste(image, (0, top))
            top += image.height + gap
        canvas.save(destination)
        return True
    finally:
        for image in opened:
            image.close()


def analyze_page_fill(images: Sequence[Path], min_nonfinal_fill: float) -> list[float]:
    try:
        from PIL import Image
    except ImportError:
        fail("Pillow is required for non-final page fill checks.")

    ratios: list[float] = []
    for path in images:
        with Image.open(path) as image:
            grayscale = image.convert("L")
            ink_mask = grayscale.point(lambda value: 255 if value < 250 else 0)
            bounds = ink_mask.getbbox()
            ratio = 0.0 if bounds is None else bounds[3] / image.height
            ratios.append(round(ratio, 4))

    if min_nonfinal_fill > 0:
        sparse_pages = [
            index + 1
            for index, ratio in enumerate(ratios[:-1])
            if ratio < min_nonfinal_fill
        ]
        if sparse_pages:
            fail(
                "Non-final pages have excessive bottom whitespace: "
                f"pages {sparse_pages}, fill ratios {ratios}, required minimum "
                f"{min_nonfinal_fill:.2f}. Remove unnecessary explicit page breaks, avoid "
                "protecting whole long projects from splitting, or rebalance complete content "
                "blocks. Do not lower this gate merely to make the build pass."
            )
    return ratios


def command_doctor(args: argparse.Namespace) -> int:
    ensure_pdf_runtime()
    chrome = find_chrome(args.chrome)
    pdftoppm = find_pdftoppm(args.pdftoppm)
    pingfang = find_pingfang_ttc()
    fonts = [str(path) for path in COMMON_ATS_FONT_PATHS if path.is_file()]
    result = {
        "status": "ok",
        "template": str(TEMPLATE_PATH),
        "template_sha256": sha256_file(TEMPLATE_PATH),
        "python": sys.executable,
        "chrome": str(chrome),
        "pdftoppm": str(pdftoppm),
        "pingfang_source": str(pingfang),
        "ats_fonts": fonts,
        "pdf_packages": ["fonttools", "pypdf", "pdfplumber"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not fonts:
        print(
            "Warning: the preferred Arial Unicode font file was not found; the build-time "
            "ATS mapping check will determine whether the platform fallback is safe.",
            file=sys.stderr,
        )
    return 0


def command_init(args: argparse.Namespace) -> int:
    destination = Path(args.output).expanduser().resolve()
    if destination.suffix.lower() not in {".html", ".htm"}:
        fail("The initialized resume source must use an .html or .htm extension.")
    if destination.exists():
        fail(f"Refusing to overwrite existing HTML: {destination}")
    if destination == TEMPLATE_PATH.resolve():
        fail("Refusing to overwrite the canonical template.")

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    template_sha = sha256_file(TEMPLATE_PATH)
    marker = f"<!-- resume-pipeline: template-sha256={template_sha} -->"
    first_newline = template_text.find("\n")
    if first_newline < 0:
        fail("Template has no newline after the doctype.")
    copied_text = template_text[: first_newline + 1] + marker + "\n" + template_text[first_newline + 1 :]

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(copied_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "initialized",
                "template": str(TEMPLATE_PATH),
                "template_sha256": template_sha,
                "editable_html": str(destination),
                "next": "Edit only editable_html, then run the build subcommand.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_build(args: argparse.Namespace) -> int:
    ensure_pdf_runtime()
    if args.expected_pages is not None and args.expected_pages < 1:
        fail("--expected-pages must be at least 1.")
    if not 0.0 <= args.min_nonfinal_fill <= 1.0:
        fail("--min-nonfinal-fill must be between 0 and 1.")
    if args.dpi < 72:
        fail("--dpi must be at least 72.")
    if args.timeout < 10:
        fail("--timeout must be at least 10 seconds.")
    html_path = Path(args.html).expanduser().resolve()
    pdf_path = Path(args.pdf).expanduser().resolve()
    qa_root = Path(args.qa_dir).expanduser().resolve()
    if pdf_path.suffix.lower() != ".pdf":
        fail("--pdf must end in .pdf")
    if pdf_path.exists() and not args.overwrite:
        fail(f"Refusing to overwrite existing PDF without --overwrite: {pdf_path}")

    html_text, html_parser, template_sha = validate_html_source(
        html_path,
        allow_stale_template=args.allow_stale_template,
        extra_forbidden_terms=args.forbid_term,
    )
    chrome = find_chrome(args.chrome)
    pdftoppm = find_pdftoppm(args.pdftoppm)
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = qa_root / f"run-{run_stamp}-{os.getpid()}"
    run_dir.mkdir(parents=True, exist_ok=False)
    render_html = run_dir / html_path.name
    render_html.write_text(html_text, encoding="utf-8")
    font_preparation = prepare_pingfang_fonts(render_html, html_parser)
    candidate_pdf = run_dir / "candidate.pdf"

    render_pdf(chrome, render_html, candidate_pdf, args.timeout)
    inspection = inspect_pdf(
        candidate_pdf,
        html_parser,
        expected_pages=args.expected_pages,
        required_terms=args.required_term,
        min_text_chars=args.min_text_chars,
    )
    page_images = render_pngs(
        pdftoppm,
        candidate_pdf,
        run_dir,
        args.dpi,
        int(inspection["page_count"]),
    )
    page_fill_ratios = analyze_page_fill(page_images, args.min_nonfinal_fill)
    contact_sheet = run_dir / "contact-sheet.png"
    has_contact_sheet = create_contact_sheet(page_images, contact_sheet)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    os.replace(candidate_pdf, pdf_path)

    report = {
        "status": "passed_automated_checks",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "template": str(TEMPLATE_PATH),
        "template_sha256": template_sha,
        "html": str(html_path),
        "render_html": str(render_html),
        "pdf": str(pdf_path),
        "pdf_sha256": sha256_file(pdf_path),
        "pdf_size_bytes": pdf_path.stat().st_size,
        "chrome": str(chrome),
        "pdftoppm": str(pdftoppm),
        "font_preparation": font_preparation,
        "inspection": inspection,
        "page_images": [str(path) for path in page_images],
        "page_fill_ratios": page_fill_ratios,
        "contact_sheet": str(contact_sheet) if has_contact_sheet else None,
        "visual_review_required": True,
        "visual_review_instruction": (
            "Inspect every page image (or the contact sheet) for clipping, overlap, bad page "
            "breaks, large bottom whitespace on non-final pages, font size, contact readability, "
            "balanced bullet wrapping, and template visual consistency."
        ),
    }
    report_path = run_dir / "qa-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**report, "qa_report": str(report_path)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Copy the canonical resume HTML template, build an A4 PDF with Chrome, render "
            "page PNGs, and run deterministic ATS/layout preflight checks, including hard "
            "wrapped text-block orphan-line and non-final page-fill gates."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check required runtime dependencies.")
    doctor.add_argument("--chrome", help="Explicit Chrome/Chromium executable path.")
    doctor.add_argument("--pdftoppm", help="Explicit pdftoppm executable path.")
    doctor.set_defaults(handler=command_doctor)

    initialize = subparsers.add_parser(
        "init", help="Copy and fingerprint the canonical HTML template."
    )
    initialize.add_argument("--output", required=True, help="New editable HTML file.")
    initialize.set_defaults(handler=command_init)

    build = subparsers.add_parser(
        "build", help="Generate, inspect, and render a PDF from an initialized HTML copy."
    )
    build.add_argument("--html", required=True, help="Initialized and edited HTML source.")
    build.add_argument("--pdf", required=True, help="Final PDF output path.")
    build.add_argument("--qa-dir", required=True, help="Base directory for run-specific QA files.")
    build.add_argument("--expected-pages", type=int, help="Require an exact page count.")
    build.add_argument(
        "--required-term",
        action="append",
        default=[],
        help="Term that must be extractable from the PDF; may be repeated.",
    )
    build.add_argument(
        "--forbid-term",
        action="append",
        default=[],
        help="Additional term that must not remain in HTML; may be repeated.",
    )
    build.add_argument("--chrome", help="Explicit Chrome/Chromium executable path.")
    build.add_argument("--pdftoppm", help="Explicit pdftoppm executable path.")
    build.add_argument("--dpi", type=int, default=144, help="PNG render DPI (default: 144).")
    build.add_argument(
        "--min-nonfinal-fill",
        type=float,
        default=DEFAULT_MIN_NONFINAL_FILL,
        help=(
            "Minimum bottom-most visible-content ratio for every non-final page "
            f"(default: {DEFAULT_MIN_NONFINAL_FILL:.2f}; lower only for intentional whitespace "
            "after visual review)."
        ),
    )
    build.add_argument(
        "--min-text-chars",
        type=int,
        default=80,
        help="Minimum extractable characters per page (default: 80).",
    )
    build.add_argument(
        "--timeout", type=int, default=120, help="Chrome timeout in seconds (default: 120)."
    )
    build.add_argument(
        "--overwrite", action="store_true", help="Atomically replace an existing final PDF."
    )
    build.add_argument(
        "--allow-stale-template",
        action="store_true",
        help="Allow a copy created from an older template after manual review.",
    )
    build.set_defaults(handler=command_build)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.handler(args))
    except PipelineError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
