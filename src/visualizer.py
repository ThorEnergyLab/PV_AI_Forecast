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
        Creates a plot for the day with the most data points and saves it as a PDF.
        Tworzy wykres dla dnia z największą liczbą danych i zapisuje go jako PDF.
        """

        df['period_end'] = pd.to_datetime(df['period_end'], utc=True).dt.tz_convert('Europe/Warsaw')
        df['date'] = df['period_end'].dt.date
        counts = df['date'].value_counts().sort_index()

        if counts.empty:
            print(" No data available to plot.")
            return

        best_date = counts.idxmax()
        print(f" Plotting data for day: {best_date} (records: {counts.max()})")

        start = pd.Timestamp(str(best_date) + ' 00:00').tz_localize('Europe/Warsaw')
        end = start + pd.Timedelta(days=1)
        df_day = df[(df['period_end'] >= start) & (df['period_end'] < end)].copy()

        if df_day.empty:
            print(" No data for the selected day.")
            return

        df_day['current_power_kW'] = df_day['energy_15min_pred_kWh']

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
                power_sum = fragment['current_power_kW'].iloc[:4].sum()
                results.append({'period_end': hour, 'power_1h_sum_kW': power_sum})

        df_hourly = pd.DataFrame(results)
        total_energy = df_day['energy_15min_pred_kWh'].sum()

        with PdfPages(output_file) as pdf:
            plt.figure(figsize=(12, 6))

            plt.plot(df_day['period_end'], df_day['current_power_kW'],
                     marker='o', linestyle='-', label='Every 15 minutes')

            if not df_hourly.empty:
                plt.bar(df_hourly['period_end'], df_hourly['power_1h_sum_kW'],
                        width=0.03, alpha=0.6, label='Sum 1h (4×)')
            else:
                print(" No data for hourly bars.")

            plt.title(f'Production PV – {best_date}')
            plt.xlabel('Time')
            plt.ylabel('Power [kW]')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)

            # Dodaj tekst sumy produkcji pod wykresem:
            plt.figtext(0.5, 0.01, f"Total predicted energy: {total_energy:.2f} kWh", ha="center", fontsize=12)

            plt.tight_layout(rect=[0, 0.03, 1, 1])  # zostaw miejsce pod tekst

            pdf.savefig()
            plt.close()

        print(f" Total predicted energy on {best_date}: {total_energy:.2f} kWh")
        if not df_hourly.empty:
            max_power = df_hourly['power_1h_sum_kW'].max()
            print(f" Max 1h power sum: {max_power:.2f} kW")
        else:
            print(" No hourly sums calculated.")

