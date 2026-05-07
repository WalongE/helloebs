from pathlib import Path
from datetime import datetime, timedelta

RECORDINGS_DIR = Path("recordings")
RETENTION_DAYS = 30


def cleanup():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)

    deleted_count = 0

    for file_path in RECORDINGS_DIR.glob("*.mp3"):
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

        if modified_time < cutoff:
            print(f"Deleting old file: {file_path}")
            file_path.unlink()
            deleted_count += 1

    print(f"Cleanup complete. Deleted {deleted_count} file(s).")


if __name__ == "__main__":
    cleanup()
