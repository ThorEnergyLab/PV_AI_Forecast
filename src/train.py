from data_merger import DataMerger
from model_trainer import ModelTrainer
import pandas as pd

def main():
    print(" Starting training...")  # Start treningu...

    #  Merge historical data from inverter output and Solcast history
    #  Łączenie danych historycznych z falownika i Solcast
    merger = DataMerger("outputs/inverter_data_plus_power.csv", "data/solcast_history.csv")
    training_data = merger.match_and_prepare_data()  # dopasuj_i_przygotuj_dane()

    if training_data.empty:
        print("⚠️ No training data available. Check date ranges!")  # Brak danych treningowych. Sprawdź zakres dat!
        return

    #  Train the model with prepared training data
    #  Trenowanie modelu na przygotowanych danych
    trainer = ModelTrainer(training_data)
    trainer.train()

    print(" Training completed successfully.")  # Trening zakończony pomyślnie.

if __name__ == "__main__":
    main()
