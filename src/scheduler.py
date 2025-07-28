import time
import datetime
import subprocess
import traceback
import os

#  Scheduled test times: (hour, minute)
#  Zaplanowane czasy uruchomienia (godzina, minuta)
SCHEDULED_TIMES = [(12, 0), (20, 0), (4, 0)]

#  Set base directory of the project (where this file is located)
#  Ustal katalog główny projektu (tam gdzie jest ten plik)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.txt")  # ścieżka do pliku logów / log file path

def log(text):
    """Log message with timestamp to console and log file"""
    # Loguj wiadomość z timestampem na konsolę i do pliku logów
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_predict():
    """Run the predict.py script and log output"""
    # Uruchom skrypt predict.py i zapisz logi
    try:
        log(" Starting predict.py")
        result = subprocess.run(["python", "predict.py"], capture_output=True, text=True)

        if result.returncode == 0:
            log(" predict.py completed successfully.")
        else:
            log(f" predict.py returned error (code: {result.returncode}).")
            log(f" stdout:\n{result.stdout}")
            log(f" stderr:\n{result.stderr}")

    except Exception as e:
        log(f" Exception while running predict.py: {e}")
        log(traceback.format_exc())

last_run = None  # store last run time to avoid duplicate runs in the same minute

while True:
    now = datetime.datetime.now()

    if (now.hour, now.minute) in SCHEDULED_TIMES:
        current_time_str = f"{now.date()}-{now.hour}-{now.minute}"

        if current_time_str != last_run:
            log(f" Time to run predict.py at {now.hour:02d}:{now.minute:02d}")
            run_predict()
            last_run = current_time_str

            # Wait 61 seconds to avoid running twice within the same minute
            # Poczekaj minutę, aby nie uruchomić skryptu dwa razy w tym samym czasie
            time.sleep(61)
        else:
            # Log heartbeat every minute that the scheduler is alive
            # Co minutę loguj, że program działa i czeka
            if now.second % 60 == 0:
                log(f" Waiting... ({now.hour:02d}:{now.minute:02d})")
            time.sleep(10)

    else:
        # Log heartbeat every minute when not in scheduled time
        # Co minutę loguj, że program działa i czeka
        if now.second % 60 == 0:
            log(f" Waiting... ({now.hour:02d}:{now.minute:02d})")
        time.sleep(10)
