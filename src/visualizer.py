import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime


class Visualizer:
    def __init__(self):
        pass

    def save_best_day(self, df, output_file):
        """
        Tworzy wykres dla dnia z największą liczbą danych i zapisuje go jako PDF.
        """

        df['period_end'] = pd.to_datetime(df['period_end'], utc=True).dt.tz_convert('Europe/Warsaw')
        df['data'] = df['period_end'].dt.date

        counts = df['data'].value_counts().sort_index()

        if counts.empty:
            print(" Brak danych do wykonania wykresu.")
            return

        best_date = counts.idxmax()

        print(f" Rysuję wykres dla dnia: {best_date} (rekordów: {counts.max()})")

        start = pd.Timestamp(str(best_date) + ' 00:00').tz_localize('Europe/Warsaw')
        end = start + pd.Timedelta(days=1)
        df_day = df[(df['period_end'] >= start) & (df['period_end'] < end)].copy()

        if df_day.empty:
            print(" Brak danych dla wybranego dnia.")
            return

        df_day['moc_chwilowa [kW]'] = df_day['energia_15min_pred [kWh]']

        # Grupowanie godzinowe
        hours = pd.date_range(
            start=df_day['period_end'].min().ceil('h'),
            end=df_day['period_end'].max().floor('h'),
            freq='1h'
        )

        results = []
        for hour in hours:
            mask = (df_day['period_end'] > hour - pd.Timedelta(minutes=30)) & \
                   (df_day['period_end'] <= hour + pd.Timedelta(minutes=30))
            fragment = df_day.loc[mask].sort_values('period_end')
            if len(fragment) >= 4:
                suma = fragment['moc_chwilowa [kW]'].iloc[:4].sum()
                results.append({'period_end': hour, 'moc_1h_sum [kW]': suma})

        df_hourly = pd.DataFrame(results)

        # Oblicz sumę energii dziennej
        suma_energii = df_day['energia_15min_pred [kWh]'].sum()

        with PdfPages(output_file) as pdf:
            plt.figure(figsize=(12, 6))
            plt.plot(df_day['period_end'], df_day['moc_chwilowa [kW]'],
                     marker='o', linestyle='-', label='Co 15 min')

            if not df_hourly.empty:
                plt.bar(df_hourly['period_end'], df_hourly['moc_1h_sum [kW]'],
                        width=0.03, label='Suma 1h (4×)')
            else:
                print(" Brak danych do słupków.")

            plt.title(f'Produkcja PV – {best_date}')
            plt.xlabel('Czas')
            plt.ylabel('Moc [kW]')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            pdf.savefig()
            plt.close()

        print(f" Prognozowana suma energii {best_date}: {suma_energii:.2f} kWh")

        if not df_hourly.empty:
            max_moc = df_hourly['moc_1h_sum [kW]'].max()
            print(f' Maksymalna suma 1h: {max_moc:.2f} kW')
        else:
            print(" Nie obliczono sum godzinnych.")
