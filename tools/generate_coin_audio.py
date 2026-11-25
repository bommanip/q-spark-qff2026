"""Generate Quantum Coin Trail MP3s from its localized captions."""

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
LANGUAGES = ("en", "kn", "te", "hi")


def read_narration():
    path = LESSON / "narration.js"
    prefix = "const coinNarration = "
    source = path.read_text(encoding="utf-8").strip()
    if not source.startswith(prefix) or not source.endswith(";"):
        raise ValueError(f"{path.name} must assign a JSON object to coinNarration")
    scripts = json.loads(source[len(prefix):-1])
    if set(scripts) != set(LANGUAGES) or any(
        not isinstance(lines, list)
        or len(lines) != len(STEPS)
        or any(not isinstance(line, str) or not line.strip() for line in lines)
        for lines in scripts.values()
    ):
        raise ValueError("Expected five nonempty narration lines for each of en, kn, te, hi")
    return scripts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, required=True, help="Local Mithi v2 Flash checkout")
    parser.add_argument("--language", action="append", choices=LANGUAGES, help="Language to regenerate. Repeat as needed.")
    parser.add_argument("--step", action="append", choices=STEPS, help="Step to regenerate. Repeat as needed.")
    parser.add_argument("--output-dir", type=Path, default=LESSON / "audio", help="MP3 output directory")
    args = parser.parse_args()
    model_dir = args.model_dir.resolve()
    if not (model_dir / "run.py").is_file():
        parser.error(f"Mithi run.py is missing from {model_dir}")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        parser.error("FFmpeg must be installed and on PATH")

    scripts = read_narration()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    import torch

    sys.path.insert(0, str(model_dir))
    from run import Mithi

    torch.set_num_threads(4)
    model = Mithi(model_dir=str(model_dir), device="cpu")
    with TemporaryDirectory(dir=args.output_dir) as directory:
        temporary = Path(directory)
        for language in args.language or LANGUAGES:
            for step in args.step or STEPS:
                index = STEPS.index(step)
                target = args.output_dir / f"{language}-{index + 1}.mp3"
                wav = temporary / "narration.wav"
                mp3 = temporary / target.name
                clip = model.synthesize(scripts[language][index], lang=language, voice="vaidehi")
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
