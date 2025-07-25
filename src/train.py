from data_merger import DataMerger
from model_trainer import ModelTrainer
import pandas as pd


def main():
    print("🚀 Start treningu...")

    # 🧹 Łączenie danych historycznych
    merger = DataMerger("outputs/dane_falownika_plus_roz_moc.csv", "data/solcast_history.csv")
    dane_treningowe = merger.dopasuj_i_przygotuj_dane()

    if dane_treningowe.empty:
        print("⚠️ Brak danych treningowych. Sprawdź zakres dat!")
        return

    # 🚀 Trenowanie modelu
    trainer = ModelTrainer(dane_treningowe)
    trainer.train()

    print("✅ Trening zakończony pomyślnie.")


if __name__ == "__main__":
    main()
