"""
Interaktywny wybór filmów do pobrania transkrypcji.

Użycie:
  python scripts/Select-Videos.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CHANNEL_URL = "https://www.youtube.com/@controlbytepl"
OUTPUT_DIR  = Path("transcripts/controlbyte")
LOG_FILE    = OUTPUT_DIR / "_log.json"
SELECTION_FILE = OUTPUT_DIR / "_selection.json"


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return {}


def get_channel_videos():
    print("Pobieram listę filmów z kanału...\n")
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(id)s\t%(title)s\t%(upload_date)s",
         CHANNEL_URL + "/videos"],
        capture_output=True, encoding="utf-8", errors="replace"
    )
    videos = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            videos.append({"id": parts[0].strip(), "title": parts[1].strip(), "date": parts[2].strip()})
    return videos


def main():
    log = load_log()
    videos = get_channel_videos()

    if not videos:
        print("Nie udało się pobrać listy filmów.")
        return

    # Wczytaj poprzedni wybór jeśli istnieje
    selected_ids = set()
    if SELECTION_FILE.exists():
        selected_ids = set(json.loads(SELECTION_FILE.read_text(encoding="utf-8")))

    print("=" * 70)
    print("LISTA FILMÓW — wybierz które chcesz pobrać")
    print("=" * 70)
    print()

    for i, v in enumerate(videos):
        vid_id = v["id"]
        title  = v["title"]
        date   = v["date"]

        status_log = log.get(vid_id, {}).get("status", "")
        if status_log == "ok":
            marker = "[✓ POBRANO]"
        elif vid_id in selected_ids:
            marker = "[✓ WYBRANO]"
        else:
            marker = "[ ]"

        print(f"  {i+1:3}. {marker} [{date}] {title[:65]}")

    print()
    print("─" * 70)
    print("Podaj numery filmów do pobrania:")
    print("  • pojedyncze:  1 3 7")
    print("  • zakresy:     10-20")
    print("  • mieszane:    1 3 10-15 22")
    print("  • wszystkie:   *")
    print("  • wyczyść:     clear")
    print("  • zatwierdź:   enter (pusty)")
    print("─" * 70)
    print()

    while True:
        raw = input("Twój wybór: ").strip()

        if raw == "":
            break
        elif raw.lower() == "clear":
            selected_ids.clear()
            print("  → Wyczyszczono wszystkie wybory.\n")
            continue
        elif raw == "*":
            selected_ids = {v["id"] for v in videos if log.get(v["id"], {}).get("status") != "ok"}
            print(f"  → Wybrano wszystkie {len(selected_ids)} niepobranych filmów.\n")
            continue

        # Parsuj numery i zakresy
        nums = set()
        for token in raw.replace(",", " ").split():
            if "-" in token:
                try:
                    a, b = token.split("-", 1)
                    for n in range(int(a), int(b)+1):
                        nums.add(n)
                except ValueError:
                    print(f"  ! Ignoruję: {token}")
            else:
                try:
                    nums.add(int(token))
                except ValueError:
                    print(f"  ! Ignoruję: {token}")

        added = 0
        for n in sorted(nums):
            if 1 <= n <= len(videos):
                vid_id = videos[n-1]["id"]
                if log.get(vid_id, {}).get("status") == "ok":
                    print(f"  ! #{n} już pobrano — pomijam")
                else:
                    selected_ids.add(vid_id)
                    added += 1
            else:
                print(f"  ! #{n} poza zakresem")

        print(f"  → Dodano {added}. Łącznie wybrano: {len(selected_ids)} filmów.\n")

    if not selected_ids:
        print("\nNie wybrano żadnych filmów. Koniec.")
        return

    # Zapisz wybór
    SELECTION_FILE.write_text(json.dumps(list(selected_ids), ensure_ascii=False), encoding="utf-8")

    print(f"\nWybrano {len(selected_ids)} filmów. Zapisano do: {SELECTION_FILE}")
    print()
    print("Uruchom teraz:")
    print(f"  $env:GEMINI_API_KEY='...'; python scripts/Get-YouTubeTranscripts.py --selection")
    print()

    # Podsumowanie wyboru
    print("Wybrane filmy:")
    for i, v in enumerate(videos):
        if v["id"] in selected_ids:
            print(f"  {i+1:3}. [{v['date']}] {v['title'][:70]}")


if __name__ == "__main__":
    main()
