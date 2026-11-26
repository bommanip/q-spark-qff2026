"""Generate Q-Spark MP3s from the localized captions."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
LESSON = ROOT / "frontend" / "fundamentals"
STEPS = ("classical", "qubit", "interference", "tilt", "entanglement")
PAGES = (*("module" + str(n) for n in range(1, 6)), "coin-lab", "linked-dice", "treasure-hunt")
PAGE_NARRATION = ROOT / "frontend" / "narration"
LANGUAGES = ("en", "kn", "te", "hi")


def read_narration(path, name):
    prefix = f"const {name} = "
    source = path.read_text(encoding="utf-8").strip()
    if not source.startswith(prefix) or not source.endswith(";"):
        raise ValueError(f"{path.name} must assign a JSON object to {name}")
    return json.loads(source[len(prefix):-1])


def load_scripts(scope):
    if scope == "concepts":
        scripts = read_narration(PAGE_NARRATION / "concepts.js", "conceptNarration")
    else:
        trail = scope == "trail"
        path = LESSON / "narration.js" if trail else PAGE_NARRATION / "scripts.js"
        steps = STEPS if trail else PAGES
        source = read_narration(path, "coinNarration" if trail else "pageNarration")
        if set(source) != set(LANGUAGES) or any(
            not isinstance(lines, list) or len(lines) != len(steps) for lines in source.values()
        ):
            raise ValueError(f"Expected {len(steps)} clips per language in {path.name}")
        scripts = {step: {lang: source[lang][index] for lang in LANGUAGES}
                   for index, step in enumerate(steps)}

    if not scripts or any(
        set(lines) != set(LANGUAGES)
        or any(not isinstance(line, str) or not line.strip() for line in lines.values())
        for lines in scripts.values()
    ):
        raise ValueError("Each clip needs nonempty text in en, kn, te, and hi")
    return scripts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, required=True, help="Local Mithi v2 Flash checkout")
    parser.add_argument("--language", action="append", choices=LANGUAGES, help="Language to regenerate. Repeat as needed.")
    parser.add_argument("--scope", choices=("trail", "pages", "concepts"), default="trail", help="Trail steps, page guides, or module concepts")
    parser.add_argument("--step", action="append", help="Step, page, or concept key to regenerate. Repeat as needed.")
    parser.add_argument("--output-dir", type=Path, help="Override the scope’s MP3 output directory")
    args = parser.parse_args()
    model_dir = args.model_dir.resolve()
    if not (model_dir / "run.py").is_file():
        parser.error(f"Mithi run.py is missing from {model_dir}")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        parser.error("FFmpeg must be installed and on PATH")

    trail = args.scope == "trail"
    scripts = load_scripts(args.scope)
    steps = tuple(scripts)
    if args.step and any(step not in scripts for step in args.step):
        parser.error(f"--step must be one of {', '.join(steps)} for --scope {args.scope}")
    output_dir = args.output_dir or (LESSON if trail else PAGE_NARRATION) / "audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    import torch

    sys.path.insert(0, str(model_dir))
    from run import Mithi

    torch.set_num_threads(4)
    model = Mithi(model_dir=str(model_dir), device="cpu")
    with TemporaryDirectory(dir=output_dir) as directory:
        temporary = Path(directory)
        for language in args.language or LANGUAGES:
            for step in args.step or steps:
                index = steps.index(step)
                suffix = index + 1 if trail else step
                target = output_dir / f"{language}-{suffix}.mp3"
                wav = temporary / "narration.wav"
                mp3 = temporary / target.name
                clip = model.synthesize(scripts[step][language], lang=language, voice="vaidehi")
                model.save(clip, str(wav))
                subprocess.run(
                    [ffmpeg, "-v", "error", "-y", "-i", str(wav), "-af",
                     "volume=7dB,alimiter=limit=0.9:level=false", "-codec:a", "libmp3lame",
                     "-b:a", "64k", str(mp3)],
                    check=True,
                )
                mp3.replace(target)
                print(target, flush=True)


if __name__ == "__main__":
    main()
