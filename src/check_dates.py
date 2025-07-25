import pandas as pd
import os

# 🔍 Sprawdzanie, czy pliki istnieją
plik_falownik = "outputs/dane_falownika_plus_roz_moc.csv"
plik_solcast_history = "data/solcast_history.csv"
plik_solcast_forecast = "data/solcast_forecast.csv"

def sprawdz_daty(plik, kolumna_czasu, opis):
    if not os.path.isfile(plik):
        print(f"❌ Plik {plik} nie istnieje!")
        return

    try:
        df = pd.read_csv(plik)
        df[kolumna_czasu] = pd.to_datetime(df[kolumna_czasu])
        print(f"\n📄 {opis} ({plik}):")
        print(f"➡️ Zakres dat: {df[kolumna_czasu].min()} → {df[kolumna_czasu].max()}")
        print(f"➡️ Liczba rekordów: {len(df)}")
    except Exception as e:
        print(f"❌ Błąd podczas odczytu {plik}: {e}")

print("\n===========================")
print("📅 SPRAWDZANIE ZAKRESÓW DAT")
print("===========================\n")

sprawdz_daty(plik_falownik, "timestamp", "Dane falownika")
sprawdz_daty(plik_solcast_history, "period_end", "Solcast HISTORY")
sprawdz_daty(plik_solcast_forecast, "period_end", "Solcast FORECAST")

print("\n===========================")
