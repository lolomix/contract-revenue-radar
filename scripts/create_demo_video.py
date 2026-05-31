#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo_video"
WORK = OUT / "work"
VIDEO = OUT / "contract_revenue_radar_qdrant_demo_final.mp4"
WIDTH = 1280
HEIGHT = 720


@dataclass(frozen=True)
class Slide:
    title: str
    bullets: tuple[str, ...]
    narration: str
    accent: str = "#184d3a"


SLIDES = [
    Slide(
        "Contract Revenue Radar",
        (
            "Vector search for contract clauses that delay cash",
            "Built for the Qdrant Think Outside the Bot hackathon",
            "Not a chatbot: one audit command produces a source-linked report",
        ),
        "Contract Revenue Radar is a vector-search audit tool for contracts. It finds clauses that delay cash, weaken renewals, or create unpaid implementation work. It is built for Qdrant's Think Outside the Bot hackathon, and it is intentionally not another chatbot.",
    ),
    Slide(
        "The Business Problem",
        (
            "Net 60 or Net 90 payment terms hurt cash flow",
            "Payment-after-acceptance language lets buyers delay invoices",
            "Vague support promises create unpaid work",
            "Weak renewal and termination terms leak future revenue",
        ),
        "Small agencies, SaaS implementers, and managed service providers often sign SOWs and MSAs that quietly damage revenue. A single payment-after-acceptance clause or broad support promise can cost more than the audit.",
        "#9e3f31",
    ),
    Slide(
        "How Qdrant Is Used",
        (
            "Split each contract into sections",
            "Embed each section into a deterministic 96-dimensional vector",
            "Upsert sections as Qdrant points with source metadata",
            "Query once per risk class: payment, renewal, scope, credits, security",
        ),
        "The app splits a contract into sections, embeds those sections, and stores them as Qdrant points. Then it runs vector queries for revenue-risk classes like payment delay, renewal loss, scope creep, credits, and security blockers.",
        "#245f8f",
    ),
    Slide(
        "Live Demo Command",
        (
            "./scripts/demo.sh",
            "Backend: qdrant-local-memory",
            "Sections searched: 5",
            "Revenue risk score: 96 out of 100",
        ),
        "The demo command runs the included sample agreement through the installed CLI. In the verified run, the backend is Qdrant local memory, five sections are searched, and the report returns a revenue risk score of ninety six out of one hundred.",
        "#184d3a",
    ),
    Slide(
        "Example Findings",
        (
            "Payment delay: Net 90 after customer acceptance",
            "Renewal loss: month-to-month plus convenience termination",
            "Scope creep: additional support included at no charge",
            "Service credit and data/security blockers also flagged",
        ),
        "The report shows exact excerpts from the source agreement. It flags Net ninety after acceptance, convenience termination, vague additional support, service credits, and data handling blockers.",
        "#b07a25",
    ),
    Slide(
        "Why It Matters",
        (
            "$1,500 quick audit for up to five documents",
            "$2,500 audit plus fallback positions",
            "$5,000 sprint for a clause playbook and intake checklist",
            "Primary buyers: SaaS implementers, RevOps, MSPs, technical agencies",
        ),
        "This project is also commercially useful. The same tool can be sold as a fixed-scope revenue terms audit: fifteen hundred dollars for a quick audit, twenty five hundred with fallback positions, or five thousand for a clause playbook.",
        "#184d3a",
    ),
    Slide(
        "Submission Summary",
        (
            "Runnable Python package",
            "Qdrant local-memory backend with fallback index",
            "Tests, sample contracts, report, landing page, and sales kit",
            "Built to turn vector search into a concrete business workflow",
        ),
        "The submission includes a runnable Python package, Qdrant local memory backend, tests, sample contracts, generated reports, a landing page, and a sales kit. Contract Revenue Radar turns vector search into a concrete business workflow.",
        "#245f8f",
    ),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


TITLE_FONT = font(54, bold=True)
BODY_FONT = font(31)
SMALL_FONT = font(22)
MONO_FONT = font(30)


def wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False)


def draw_slide(slide: Slide, index: int, total: int, path: Path) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f7f8f5")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 96), fill=slide.accent)
    draw.text((58, 28), "Contract Revenue Radar", fill="#ffffff", font=SMALL_FONT)
    draw.text((WIDTH - 120, 28), f"{index}/{total}", fill="#ffffff", font=SMALL_FONT, anchor="ra")

    draw.text((58, 142), slide.title, fill="#151716", font=TITLE_FONT)
    y = 236
    for bullet in slide.bullets:
        draw.rounded_rectangle((58, y - 8, 92, y + 26), radius=6, fill=slide.accent)
        draw.text((75, y + 9), "•", fill="#ffffff", font=SMALL_FONT, anchor="mm")
        for line in wrap(bullet, 58):
            selected_font = MONO_FONT if bullet.startswith("./") or bullet.startswith("Backend:") else BODY_FONT
            draw.text((112, y), line, fill="#151716", font=selected_font)
            y += 42
        y += 18

    draw.line((58, HEIGHT - 72, WIDTH - 58, HEIGHT - 72), fill="#dce2dd", width=2)
    draw.text(
        (58, HEIGHT - 48),
        "Business-risk review, not legal advice. Demo generated locally.",
        fill="#5d665f",
        font=SMALL_FONT,
    )
    image.save(path)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def make_video() -> Path:
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required. Install it with apt-get install ffmpeg.")
    if not shutil.which("espeak-ng"):
        raise SystemExit("espeak-ng is required. Install it with apt-get install espeak-ng.")

    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    concat_file = WORK / "concat.txt"
    concat_lines = []

    for idx, slide in enumerate(SLIDES, start=1):
        image_path = WORK / f"slide_{idx:02d}.png"
        audio_path = WORK / f"slide_{idx:02d}.wav"
        clip_path = WORK / f"clip_{idx:02d}.mp4"
        draw_slide(slide, idx, len(SLIDES), image_path)
        run(["espeak-ng", "-v", "en-us", "-s", "146", "-w", str(audio_path), slide.narration])
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-loop",
                "1",
                "-i",
                str(image_path),
                "-i",
                str(audio_path),
                "-vf",
                "format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-shortest",
                str(clip_path),
            ]
        )
        concat_lines.append(f"file '{clip_path.name}'")

    concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(VIDEO),
        ]
    )
    return VIDEO


def main() -> int:
    video = make_video()
    print(video)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
