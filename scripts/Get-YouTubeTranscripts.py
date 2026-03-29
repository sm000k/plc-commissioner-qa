"""
Pobieranie transkrypcji wszystkich filmów z kanału YouTube.
Kanał: controlbyte automatyka na plc

Użycie:
  1. Skrypt najpierw pobiera listę wszystkich URL z kanału (yt-dlp)
  2. Dla każdego filmiku próbuje pobrać napisy YT (youtube-transcript-api)
  3. Jeśli brak napisów → opcjonalnie transkrybuje przez Gemini (wymaga klucza API)
  4. Zapisuje wyniki do folderu transcripts/

Klucz Gemini API:
  Ustaw zmienną środowiskową GEMINI_API_KEY lub wpisz poniżej.
"""

import os
import re
import json
import time
import subprocess
import sys
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix Windows terminal encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─── KONFIGURACJA ────────────────────────────────────────────────────────────

CHANNEL_URL = "https://www.youtube.com/@controlbytepl"   # URL kanału
OUTPUT_DIR  = Path("transcripts/controlbyte")           # folder wyjściowy
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")   # lub wpisz tutaj

# Jeśli klucz jest ustawiony, Gemini jest używany automatycznie jako fallback
USE_GEMINI_FALLBACK = bool(GEMINI_API_KEY)

# Cookies YouTube (potrzebne do ominięcia blokady 429)
# Opcja 1: plik cookies.txt (Netscape format) - np. wyeksportowany przez rozszerzenie przeglądarki
COOKIES_FILE = Path("cookies.txt")  # umieść w głównym folderze workspace
# Opcja 2: przeglądarka (działa gdy przeglądarka jest ZAMKNIĘTA)
# Opcje: "chrome", "edge", "firefox" | None = wyłączone
BROWSER_FOR_COOKIES = None  # zmień na "chrome" i zamknij przeglądarkę aby użyć

# Języki napisów do próbowania (kolejność priorytetu)
TRANSCRIPT_LANGS = ["pl", "en"]

# Liczba równoległych wątków (Gemini Pro: do 10 równolegle jest bezpieczne)
MAX_WORKERS = 5

# ─── SETUP ───────────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = OUTPUT_DIR / "_log.json"
_log_lock = threading.Lock()
_print_lock = threading.Lock()

def tprint(*args, **kwargs):
    """Thread-safe print."""
    with _print_lock:
        print(*args, **kwargs)

def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return {}

def save_log(log):
    with _log_lock:
        LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

# ─── KROK 1: Pobierz listę filmów z kanału ───────────────────────────────────

def _cookies_args():
    """Zwraca argumenty cookies dla yt-dlp."""
    if COOKIES_FILE.exists():
        return ["--cookies", str(COOKIES_FILE)]
    if BROWSER_FOR_COOKIES:
        return ["--cookies-from-browser", BROWSER_FOR_COOKIES]
    return []

def get_channel_videos(channel_url):
    print(f"\n[1/3] Pobieranie listy filmów z: {channel_url}")
    result = subprocess.run(
        [
            "yt-dlp",
            "--flat-playlist",
            "--print", "%(id)s\t%(title)s\t%(upload_date)s",
        ] + _cookies_args() + [
            channel_url + "/videos"
        ],
        capture_output=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0 and not result.stdout:
        print(f"BŁĄD yt-dlp:\n{result.stderr}")
        return []

    videos = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            vid_id, title, date = parts
            videos.append({"id": vid_id.strip(), "title": title.strip(), "date": date.strip()})

    print(f"  → Znaleziono {len(videos)} filmów.")
    return videos

# ─── KROK 2: Pobierz napisy przez youtube-transcript-api ─────────────────────

# ─── KROK 2: Pobierz napisy przez yt-dlp (bardziej niezawodne niż transcript-api) ──

def get_transcript_yt(video_id, langs=TRANSCRIPT_LANGS):
    """Pobiera napisy przez yt-dlp w formacie json3 (auto-caption)."""
    import json as jsonlib, tempfile, glob

    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub",
                "--sub-lang", ",".join(langs),
                "--sub-format", "json3",
                "--skip-download",
                "--quiet",
                "-o", os.path.join(tmpdir, "sub"),
            ] + _cookies_args() + [
                url
            ],
            capture_output=True, encoding="utf-8", errors="replace"
        )

        json3_files = glob.glob(os.path.join(tmpdir, "*.json3"))
        if not json3_files:
            return None, "NOT_FOUND"

        # Czytaj pierwszy dostępny plik (priorytet pl)
        json3_files.sort(key=lambda f: (0 if ".pl." in f else 1))
        chosen = json3_files[0]
        detected = re.search(r'\.([a-z]{2,10})\.json3$', chosen)
        lang_code = detected.group(1) if detected else "?"

        try:
            data = jsonlib.loads(Path(chosen).read_text(encoding="utf-8", errors="replace"))
            segments = data.get("events", [])
            words = []
            for seg in segments:
                for segs in seg.get("segs", []):
                    w = segs.get("utf8", "").strip()
                    if w and w != "\n":
                        words.append(w)
            text = " ".join(words)
            if len(text) > 50:
                return lang_code, text
        except Exception as e:
            return None, f"PARSE_ERROR: {e}"

    return None, "NOT_FOUND"

# ─── KROK 3 (opcjonalny): Transkrypcja przez Gemini ──────────────────────────

def transcribe_with_gemini(video_id):
    """Transkrybuje film przez Gemini API - bezpośrednio z URL YouTube (bez pobierania audio)."""
    if not GEMINI_API_KEY:
        return None, "NO_API_KEY"

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        yt_url = f"https://www.youtube.com/watch?v={video_id}"

        tprint(f"    [Gemini] Transkrybowanie: {yt_url}")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=types.Content(
                parts=[
                    types.Part(
                        file_data=types.FileData(file_uri=yt_url)
                    ),
                    types.Part(
                        text=(
                            "Proszę dosłownie transkrybuj ten film wideo po polsku. "
                            "Zachowaj terminologię techniczną (PLC, Siemens, TIA Portal, PROFINET). "
                            "Nie dodawaj podsumowań ani komentarzy — tylko czysty tekst wypowiedzi."
                        )
                    )
                ]
            )
        )
        text = response.text.strip()
        if len(text) > 50:
            return "gemini", text
        return None, "GEMINI_EMPTY"
    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            retry_delay = 60
            m = re.search(r'Please retry in ([\d\.]+)s', err)
            if m:
                retry_delay = float(m.group(1)) + 1
            tprint(f"    [Gemini] Limit zapytań (429). Czekam {retry_delay:.0f}s...")
            time.sleep(retry_delay)
            return transcribe_with_gemini(video_id)
        if "google.genai" in err or "cannot import" in err:
            return _transcribe_gemini_legacy(video_id)
        return None, f"GEMINI_ERROR: {err}"


def _transcribe_gemini_legacy(video_id):
    """Fallback: stary SDK google.generativeai z pobieraniem audio."""
    import tempfile
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
    except ImportError:
        return None, "NO_GEMINI_SDK"

    audio_path = Path(tempfile.gettempdir()) / f"{video_id}.mp3"
    try:
        print(f"    [Gemini legacy] Pobieranie audio: {video_id}")
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "--audio-quality", "5",   # niższa jakość = mniejszy plik
            "-o", str(audio_path),
            f"https://www.youtube.com/watch?v={video_id}"
        ], capture_output=True, check=True)

        print(f"    [Gemini] Transkrypcja audio ({audio_path.stat().st_size // 1024} KB)...")
        model = genai.GenerativeModel("gemini-2.5-flash")
        audio_file = genai.upload_file(str(audio_path))
        response = model.generate_content([
            audio_file,
            "Transkrybuj to nagranie po polsku. Zachowaj terminologię techniczną (PLC, Siemens, TIA Portal)."
        ])
        return "gemini", response.text
    except Exception as e:
        return None, f"GEMINI_ERROR: {e}"
    finally:
        if audio_path.exists():
            audio_path.unlink()

# ─── GŁÓWNA PĘTLA ────────────────────────────────────────────────────────────

def slugify(text):
    text = re.sub(r'[<>:"/\\|?*\n\r]', '', text)
    text = text.replace('\t', ' ')
    return text[:80].strip()


def process_video(i, total, v, log):
    """Przetwarza jeden film — wywoływane równolegle."""
    vid_id = v["id"]
    title  = v["title"]
    date   = v.get("date", "")
    filename = OUTPUT_DIR / f"{date}_{slugify(title)}.txt"

    tprint(f"  [{i}/{total}] {title[:70]}")

    lang, text = get_transcript_yt(vid_id)

    if lang is None and USE_GEMINI_FALLBACK:
        lang, text = transcribe_with_gemini(vid_id)

    if lang and lang not in ("DISABLED", "NOT_FOUND") and not str(text).startswith("GEMINI_ERROR"):
        content = f"# {title}\n"
        content += f"# ID: {vid_id} | Data: {date} | Język: {lang}\n"
        content += f"# URL: https://www.youtube.com/watch?v={vid_id}\n\n"
        content += text
        filename.write_text(content, encoding="utf-8")
        tprint(f"    → OK ({lang}), zapisano: {filename.name}")
        return vid_id, "ok", title, lang, str(filename)
    else:
        tprint(f"    → BRAK napisów ({text})")
        return vid_id, "failed", title, None, str(text)


def main():
    log = load_log()
    videos = get_channel_videos(CHANNEL_URL)

    if not videos:
        print("Brak filmów — sprawdź URL kanału lub połączenie.")
        return

    # Tryb --selection: pobierz tylko filmy wybrane przez Select-Videos.py
    selection_file = OUTPUT_DIR / "_selection.json"
    if "--selection" in sys.argv and selection_file.exists():
        selected_ids = set(json.loads(selection_file.read_text(encoding="utf-8")))
        videos = [v for v in videos if v["id"] in selected_ids]
        print(f"  → Tryb selekcji: {len(videos)} wybranych filmów.")

    todo = [v for v in videos if not (v["id"] in log and log[v["id"]].get("status") == "ok")]
    skipped = len(videos) - len(todo)
    total = len(videos)

    print(f"\n[2/3] Pobieranie transkrypcji równolegle ({MAX_WORKERS} wątków)...")
    print(f"      Do pobrania: {len(todo)}, pominiętych (już OK): {skipped}\n")

    ok = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_video, videos.index(v)+1, total, v, log): v
            for v in todo
        }
        for future in as_completed(futures):
            vid_id, status, title, lang, extra = future.result()
            with _log_lock:
                if status == "ok":
                    log[vid_id] = {"status": "ok", "title": title, "lang": lang, "file": extra}
                    ok += 1
                elif status == "failed":
                    log[vid_id] = {"status": "failed", "title": title, "reason": extra}
                    failed += 1
                save_log(log)

    print(f"\n[3/3] GOTOWE: {ok} transkrypcji, {skipped} pominiętych, {failed} bez napisów.")
    print(f"     Folder: {OUTPUT_DIR.resolve()}")
    if failed > 0:
        print(f"     Filmy bez napisów: {LOG_FILE.name}")

if __name__ == "__main__":
    main()
