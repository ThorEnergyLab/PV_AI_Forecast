import pandas as pd
import sys


def sprawdz_zakres_danych(plik_falownik, plik_solcast):
    try:
        df_falownik = pd.read_csv(plik_falownik)
        df_solcast = pd.read_csv(plik_solcast)

        df_falownik['timestamp'] = pd.to_datetime(df_falownik['timestamp'])
        df_solcast['period_end'] = pd.to_datetime(df_solcast['period_end'])

        min_fal, max_fal = df_falownik['timestamp'].min(), df_falownik['timestamp'].max()
        min_sol, max_sol = df_solcast['period_end'].min(), df_solcast['period_end'].max()

        print("\n===========================")
        print("📅 SPRAWDZANIE ZAKRESÓW DAT")
        print("===========================\n")
        print(f"Falownik: {min_fal} → {max_fal}")
        print(f"Solcast : {min_sol} → {max_sol}")

        if max_fal < min_sol or min_fal > max_sol:
            print("\n❌ ❌ Brak pokrywających się zakresów danych!")
            sys.exit(1)
        else:
            print("\n✅ Zakresy danych są OK. Możesz kontynuować.\n")

    except Exception as e:
        print(f"\n❌ Błąd podczas sprawdzania zakresów danych: {e}")
        sys.exit(1)


def sprawdz_braki(plik):
    df = pd.read_csv(plik)
    nan_counts = df.isna().sum()

    print("\n🕵️‍♂️ Sprawdzanie braków w danych:")
    print(nan_counts[nan_counts > 0])

    if nan_counts.sum() > 0:
        print("⚠️ Dane zawierają braki!\n")
    else:
        print("✅ Brak braków w danych.\n")
