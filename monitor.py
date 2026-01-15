import argparse
import random
import string
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.config import Config
from src.detector import BehaviorDetector
from src.event_bus import push_event
from src.utils.logger import now_iso


class Handler(FileSystemEventHandler):
    def __init__(self, detector: BehaviorDetector, cfg: Config):
        self.detector = detector
        self.cfg = cfg

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle("created", event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._handle("modified", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._handle("deleted", event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        # moved includes rename
        self._handle("moved", event.src_path, event.dest_path)

    def _handle(self, ev_type: str, src: str, dest: str = ""):
        ev = {
            "ts": now_iso(),
            "type": ev_type,
            "src_path": src,
            "dest_path": dest,
        }
        push_event(self.cfg.STATE_JSON, ev)
        self.detector.record_event(ev_type, src, dest or None)


def safe_test_generator(folder: Path, seconds: int = 15):
    """Creates benign activity to test rules (NOT encryption, NOT malware)."""
    folder.mkdir(parents=True, exist_ok=True)
    start = time.time()
    files: list[Path] = []

    # Seed some files
    for i in range(10):
        p = folder / f"doc_{i}.txt"
        try:
            p.write_text("hello world\n" * 10, encoding="utf-8")
            files.append(p)
        except Exception:
            pass

    while time.time() - start < seconds:
        # Clean list from missing files (renamed/deleted)
        files = [x for x in files if x.exists()]

        # If list got empty for any reason, recreate a seed file
        if not files:
            p = folder / f"doc_reseed_{int(time.time())}.txt"
            try:
                p.write_text("reseed\n", encoding="utf-8")
                files.append(p)
            except Exception:
                time.sleep(0.1)
                continue

        # ✅ Modify random file safely
        p = random.choice(files)
        if p.exists():
            try:
                old_text = p.read_text(encoding="utf-8")
                new_text = old_text + "update-" + "".join(
                    random.choices(string.ascii_lowercase, k=20)
                ) + "\n"
                p.write_text(new_text, encoding="utf-8")
            except Exception:
                # ignore file access issues (race conditions)
                pass

        # ✅ Occasionally rename (simulate extension spike) safely
        if random.random() < 0.25 and files:
            old = random.choice(files)
            if old.exists():
                new = old.with_suffix(".locked")  # label only (no encryption)
                try:
                    old.rename(new)
                    # update list
                    if old in files:
                        files.remove(old)
                    files.append(new)
                except Exception:
                    pass

        # ✅ Occasionally create new file
        if random.random() < 0.2:
            p2 = folder / f"new_{int(time.time())}.txt"
            try:
                p2.write_text("new file\n", encoding="utf-8")
                files.append(p2)
            except Exception:
                pass

        time.sleep(0.2)


def main():
    parser = argparse.ArgumentParser(
        description="RansomWatch — defensive folder behavior monitor"
    )
    parser.add_argument(
        "--path", default=Config().WATCH_PATH,
        help="Folder to watch (default: data/watch_folder)"
    )
    parser.add_argument(
        "--safe-test", action="store_true",
        help="Generate benign activity for testing (no malware)"
    )
    args = parser.parse_args()

    cfg = Config(WATCH_PATH=args.path)
    watch_path = Path(cfg.WATCH_PATH)
    watch_path.mkdir(parents=True, exist_ok=True)

    detector = BehaviorDetector(cfg)

    if args.safe_test:
        print("✅ Running SAFE test generator (benign activity)...")
        safe_test_generator(watch_path, seconds=18)
        print("✅ Safe test done. Check Streamlit dashboard and logs/alerts.csv")
        return

    event_handler = Handler(detector, cfg)
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=True)
    observer.start()

    print(f"🛡️ RansomWatch monitoring: {watch_path.resolve()}")
    print("Press CTRL+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
