import subprocess
from datetime import datetime
from pathlib import Path

STREAM_URL = "https://ebsonair.ebs.co.kr/fmradiofamilypc/familypc1m/playlist.m3u8"

RECORD_SECONDS = 19 * 60
OUTPUT_DIR = Path("recordings")
PROGRAM_NAME = "ibtyoung"


def make_output_path() -> Path:
    today = datetime.now().strftime("%Y%m%d")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / f"{today}_{PROGRAM_NAME}.mp3"


def record():
    output_path = make_output_path()

    cmd = [
        "ffmpeg",
        "-y",
        "-i", STREAM_URL,
        "-t", str(RECORD_SECONDS),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "128k",
        str(output_path),
    ]

    print(f"Recording start: {output_path}")
    subprocess.run(cmd, check=True)
    print(f"Recording done: {output_path}")


if __name__ == "__main__":
    record()
