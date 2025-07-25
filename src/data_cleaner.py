import pandas as pd


class MQTTDataCleaner:
    def __init__(self, mqtt_csv_file):
        self.mqtt_csv_file = mqtt_csv_file
        self.cleaned_file = "outputs/dane_falownik.csv"
        self.pivoted_file = "outputs/dane_falownik_ustawienie_kolumn.csv"
        self.final_file = "outputs/dane_falownika_plus_roz_moc.csv"

    def load_and_clean(self):
        df = pd.read_csv(self.mqtt_csv_file, header=None, names=['timestamp', 'topic', 'value'])
        frazy = [
            'if0754/fca/m9', 'if0754/fca/m10', 'if0754/fca/m11',
            'if0754/fca/connected', 'if0754/fca/m12', 'if0754/connected'
        ]
        df['topic'] = df['topic'].astype(str).str.strip()
        df_filtered = df[~df['topic'].isin(frazy)]
        df_filtered.to_csv(self.cleaned_file, index=False)
        return df_filtered

    def pivot_and_rename(self):
        df = pd.read_csv(self.cleaned_file)
        df_pivot = df.pivot(index='timestamp', columns='topic', values='value')
        df2 = df_pivot.reset_index()
        df2.columns = ['timestamp', 'Napięcie Ua', 'Napięcie Ub', 'Napięcie Uc',
                       'Prąd Idc', 'Napięcie Udc', 'Moc chwilowa Pdc', 'Moc suma P ALL', 'SF']
        df2.to_csv(self.pivoted_file, index=False)
        return df2

    def resample_data(self):
        df = pd.read_csv(self.pivoted_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df_resampled = df.resample('5min').max().reset_index()

        df_resampled['energia [kW/h]'] = df_resampled['Moc suma P ALL'].diff().round(4)
        df_resampled['energia [kW/h]'] = df_resampled['energia [kW/h]'].fillna(0)

        df_resampled["Moc P DC po SF"] = df_resampled.apply(self.przeskaluj, axis=1)
        df_resampled.to_csv(self.final_file, index=False)
        return df_resampled

    @staticmethod
    def przeskaluj(row):
        if row["SF"] == 65535.0:
            return row["Moc chwilowa Pdc"] / 10
        elif row["SF"] == 65534.0:
            return row["Moc chwilowa Pdc"] / 100
        elif row["SF"] == 65533.0:
            return row["Moc chwilowa Pdc"] / 1000
        else:
            return row["Moc chwilowa Pdc"]
