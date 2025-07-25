import pandas as pd
import numpy as np


class DataMerger:
    def __init__(self, plik_falownik, plik_solcast):
        self.plik_falownik = plik_falownik
        self.plik_solcast = plik_solcast
        self.wynik_dopasowany = "outputs/dopasowane_finalnie.csv"
        self.wynik_treningowy = "outputs/dane_treningowe.csv"

    def dopasuj_i_przygotuj_dane(self):
        dane_falownik = pd.read_csv(self.plik_falownik)
        dane_solcast = pd.read_csv(self.plik_solcast)

        dane_falownik['timestamp'] = pd.to_datetime(dane_falownik['timestamp'])
        dane_falownik['timestamp'] = dane_falownik['timestamp'].dt.tz_localize('Europe/Warsaw').dt.tz_convert('UTC')
        dane_solcast['period_end'] = pd.to_datetime(dane_solcast['period_end'], utc=True)

        dane_falownik = dane_falownik.sort_values('timestamp')
        dane_solcast = dane_solcast.sort_values('period_end')

        dane_polaczone = pd.merge_asof(
            dane_falownik,
            dane_solcast[['period_end', 'ghi', 'air_temp']],
            left_on='timestamp',
            right_on='period_end',
            direction='nearest',
            tolerance=pd.Timedelta('3min')
        )

        print(f"Liczba niedopasowanych wierszy: {dane_polaczone['ghi'].isna().sum()}")

        dane_polaczone = dane_polaczone.reset_index(drop=True).set_index('timestamp')

        energia_15min = (
            dane_polaczone['energia [kW/h]']
            .resample('15min')
            .sum()
            .round(4)
            .to_frame(name='energia_15min [kWh]')
        )

        energia_15min['energia_15min [kWh]'] = energia_15min['energia_15min [kWh]'].clip(lower=0.0)
        energia_15min.loc[energia_15min['energia_15min [kWh]'] > 2.0, 'energia_15min [kWh]'] = 0.0

        dane_polaczone = dane_polaczone.join([energia_15min]).reset_index()

        dane_polaczone['hour_decimal'] = dane_polaczone['timestamp'].dt.hour + dane_polaczone['timestamp'].dt.minute / 60
        dane_polaczone['day_of_year'] = dane_polaczone['timestamp'].dt.dayofyear
        dane_polaczone['sin_hour'] = np.sin(2 * np.pi * dane_polaczone['hour_decimal'] / 24)
        dane_polaczone['cos_hour'] = np.cos(2 * np.pi * dane_polaczone['hour_decimal'] / 24)

        dane_polaczone.to_csv(self.wynik_dopasowany, index=False)

        dane_treningowe = dane_polaczone[
            (dane_polaczone['ghi'] >= 0) &
            (dane_polaczone['energia_15min [kWh]'].notna())
        ][[
            'timestamp', 'ghi', 'air_temp', 'sin_hour', 'cos_hour', 'day_of_year', 'energia_15min [kWh]'
        ]]

        dane_treningowe.to_csv(self.wynik_treningowy, index=False)

        return dane_treningowe
