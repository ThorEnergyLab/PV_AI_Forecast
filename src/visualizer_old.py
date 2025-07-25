import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML


class Visualizer:
    def __init__(self):
        pass

    def plot_daily(self, df, target_date):
        df['period_end'] = pd.to_datetime(df['period_end'], utc=True).dt.tz_convert('Europe/Warsaw')

        start = pd.Timestamp(target_date + ' 00:00').tz_localize('Europe/Warsaw')
        end = start + pd.Timedelta(days=1)
        df_day = df[(df['period_end'] >= start) & (df['period_end'] < end)].copy()

        df_day['moc_chwilowa [kW]'] = df_day['energia_15min_pred [kWh]']

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

        suma_energii = df_day['energia_15min_pred [kWh]'].sum()
        print(f"Prognozowana suma produkcji energii {target_date}: {suma_energii:.2f} kWh")

        plt.figure(figsize=(12, 6))
        plt.plot(df_day['period_end'], df_day['moc_chwilowa [kW]'], marker='o', linestyle='-', label='Co 15 min')
        if not df_hourly.empty:
            plt.bar(df_hourly['period_end'], df_hourly['moc_1h_sum [kW]'], width=0.03, label='Suma 1h (4×)')
        else:
            print("Brak danych do słupków.")
        plt.title(f'Produkcja PV – {target_date}')
        plt.xlabel('Czas')
        plt.ylabel('Moc [kW]')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        if not df_hourly.empty:
            max_moc = df_hourly['moc_1h_sum [kW]'].max()
            print(f'Maksymalna suma 1h: {max_moc:.2f} kW')
        else:
            print("Nie obliczono sum godzinnych.")

        display(HTML(f"<span style='color: black; font-size: 20px; font-weight: bold;'>Suma energii prognozowanej {target_date}: {suma_energii:.2f} kWh</span>"))
