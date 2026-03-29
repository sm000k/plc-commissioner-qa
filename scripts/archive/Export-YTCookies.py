"""
Eksport cookies YouTube do pliku cookies.txt

Uruchom ten skrypt gdy przeglądarka (Edge/Chrome) jest ZAMKNIĘTA.
Plik cookies.txt zostanie zapisany w głównym folderze workspace.

Alternatywa (bez zamykania przeglądarki):
  1. Zainstaluj rozszerzenie "Get cookies.txt LOCALLY" w Chrome/Edge
  2. Wejdź na youtube.com
  3. Kliknij ikonę rozszerzenia → "Export" → zapisz jako cookies.txt

Użycie:
  python scripts/Export-YTCookies.py [chrome|edge|firefox]
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
COOKIES_FILE = WORKSPACE / "cookies.txt"

def export_cookies(browser="edge"):
    print(f"Eksportowanie cookies z {browser}...")
    print(f"UWAGA: Przeglądarka {browser} musi być ZAMKNIĘTA!")
    print()

    result = subprocess.run(
        [
            "yt-dlp",
            "--cookies-from-browser", browser,
            "--cookies", str(COOKIES_FILE),
            "--quiet",
            "--no-download",
            "--no-playlist",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ],
        capture_output=True, encoding="utf-8", errors="replace"
    )

    if COOKIES_FILE.exists() and COOKIES_FILE.stat().st_size > 100:
        print(f"✓ Cookies zapisane: {COOKIES_FILE}")
        lines = COOKIES_FILE.read_text(encoding="utf-8").splitlines()
        yt_lines = [l for l in lines if "youtube.com" in l]
        print(f"  Znalezione cookie YouTube: {len(yt_lines)}")
        if len(yt_lines) < 3:
            print("  OSTRZEŻENIE: Mało cookies YouTube — może być nieuważniony")
        return True
    else:
        print(f"BŁĄD eksportu cookies.")
        print(f"stdout: {result.stdout[:500]}")
        print(f"stderr: {result.stderr[:500]}")
        return False

if __name__ == "__main__":
    browser = sys.argv[1] if len(sys.argv) > 1 else "chrome"
    if browser not in ("chrome", "edge", "firefox", "brave", "chromium"):
        print(f"Nieznana przeglądarka: {browser}")
        sys.exit(1)
    success = export_cookies(browser)
    if success:
        print()
        print("Teraz uruchom: python scripts/Get-YouTubeTranscripts.py")
