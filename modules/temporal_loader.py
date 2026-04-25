"""
Loader para informação temporal de divergência linguística
"""
import pandas as pd
from pathlib import Path
from config import DATA_DIR


class TemporalLoader:
    """
    Carrega datas de divergência em relação ao PIE
    """

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = DATA_DIR / "temporal" / "divergence_dates.csv"
        self.filepath = filepath
        self.df = None

    def load(self):
        """Carrega dados temporais"""
        if not self.filepath.exists():
            print(f"⚠️ Ficheiro temporal não encontrado: {self.filepath}")
            return None

        self.df = pd.read_csv(self.filepath)
        print(f"✅ Temporal: {len(self.df)} línguas com dados temporais")
        return self.df

    def get_divergence_time(self, glottocode, unit='ky'):
        """Obtém tempo de divergência, retornando None para não-IE"""
        if self.df is None:
            self.load()

        row = self.df[self.df['glottocode'] == glottocode]
        if len(row) == 0:
            return None

        pie_div = row.iloc[0]['pie_divergence_bp']

        # Tratar N/A ou valores não-numéricos
        if pd.isna(pie_div) or pie_div == 'N/A' or not isinstance(pie_div, (int, float)):
            return None

        if unit == 'ky':
            return pie_div / 1000
        elif unit == 'yr':
            return pie_div
        elif unit == 'bc':
            bc_val = row.iloc[0]['pie_divergence_bc']
            return bc_val if pd.notna(bc_val) else None

        return None

    def get_confidence(self, glottocode):
        """Retorna nível de confiança da estimativa"""
        if self.df is None:
            self.load()
        row = self.df[self.df['glottocode'] == glottocode]
        return row.iloc[0]['confidence'] if len(row) > 0 else None

    def get_all_times(self, unit='ky'):
        """Retorna dicionário {glottocode: time} para todas as línguas"""
        if self.df is None:
            self.load()
        return {
            row['glottocode']: self.get_divergence_time(row['glottocode'], unit)
            for _, row in self.df.iterrows()
        }

    def list_languages(self):
        """Lista todas as línguas disponíveis"""
        if self.df is None:
            self.load()
        return list(self.df['language'].values)


    def get_languages_by_branch(self, branch):
        """Retorna lista de glottocodes para um ramo específico"""
        if self.df is None:
            self.load()
        return self.df[self.df['branch'] == branch]['glottocode'].tolist()

    def get_branch_distribution(self):
        """Retorna contagem de línguas por ramo"""
        if self.df is None:
            self.load()
        return self.df['branch'].value_counts().to_dict()

    def get_language_name(self, glottocode):
        """
        Obtém nome amigável da língua
        Usa o CSV como fonte única de verdade
        """
        if self.df is None:
            self.load()

        row = self.df[self.df['glottocode'] == glottocode]
        if len(row) > 0:
            return row.iloc[0]['language']
        return glottocode  # Fallback para glottocode se não encontrar

    def get_all_names(self):
        """Retorna dicionário {glottocode: language}"""
        if self.df is None:
            self.load()
        return dict(zip(self.df['glottocode'], self.df['language']))

    def get_language_branch(self, glottocode):
        """Obtém ramo/família da língua"""
        if self.df is None:
            self.load()
        row = self.df[self.df['glottocode'] == glottocode]
        return row.iloc[0]['branch'] if len(row) > 0 else 'Unknown'