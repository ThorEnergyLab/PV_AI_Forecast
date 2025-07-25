import time
import datetime
import subprocess
import traceback
import os


# 🔧 Czasy testowe: (godzina, minuta)
SCHEDULED_TIMES = [(12,00), (20, 00), (4, 0)]


# 🔧 Ustal ścieżkę do katalogu projektu (tam, gdzie jest ten plik)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.txt")


def log(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_predict():
    try:
        log("🚀 Startuję predict.py")
        result = subprocess.run(["python", "src/predict.py"], capture_output=True, text=True)

        if result.returncode == 0:
            log("✅ Skrypt predict.py zakończony pomyślnie.")
        else:
            log(f"❌ Skrypt predict.py zwrócił błąd (kod: {result.returncode}).")
            log(f"⚠️ stdout:\n{result.stdout}")
            log(f"⚠️ stderr:\n{result.stderr}")

    except Exception as e:
        log(f"💥 Wyjątek podczas uruchamiania predict.py: {e}")
        log(traceback.format_exc())


last_run = None

while True:
    now = datetime.datetime.now()

    if (now.hour, now.minute) in SCHEDULED_TIMES:
        current_time_str = f"{now.date()}-{now.hour}-{now.minute}"

        if current_time_str != last_run:
            log(f"⏰ Czas na uruchomienie predict.py o godzinie {now.hour:02d}:{now.minute:02d}")
            run_predict()
            last_run = current_time_str

            # Poczekaj minutę, żeby nie odpalił dwa razy
            time.sleep(61)
        else:
            if now.second % 60 == 0:  # co minutę loguje, że żyje
                log(f"⏳ Czekam... ({now.hour:02d}:{now.minute:02d})")
            time.sleep(10)

    else:
        if now.second % 60 == 0:  # co minutę loguje, że żyje
            log(f"⏳ Czekam... ({now.hour:02d}:{now.minute:02d})")
        time.sleep(10)
