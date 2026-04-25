"""
Carregamento de dados WALS (tipologia linguística)
"""
import pandas as pd
from pathlib import Path
import requests
from config import DATA_DIR, URLS


class WALSLoader:
    def __init__(self):
        self.data_dir = DATA_DIR / "wals"
        self.data_dir.mkdir(exist_ok=True)
        self.df = None

    def download(self):
        """Descarrega dados WALS"""
        print("📥 A descarregar dados WALS...")

        # WALS fornece dados em formato CSV
        url = "https://wals.info/static/download/wals.csv"
        filepath = self.data_dir / "wals.csv"

        try:
            response = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✅ Dados guardados em {filepath}")
        except Exception as e:
            print(f"⚠️ Erro: {e}")

    def load(self):
        """Carrega dados para DataFrame"""
        filepath = self.data_dir / "wals.csv"

        if not filepath.exists():
            self.download()

        self.df = pd.read_csv(filepath)
        print(f"📊 WALS: {len(self.df)} registos carregados")

        return self.df

    def get_language_features(self, glottocode):
        """
        Obtém features tipológicas para uma língua

        Returns:
            dict: {feature_id: value}
        """
        if self.df is None:
            self.load()

        filtered = self.df[self.df['glottocode'] == glottocode]

        if len(filtered) == 0:
            return {}

        # Converter para dicionário
        features = {}
        for _, row in filtered.iterrows():
            features[row['feature_id']] = row['value']

        return features

    def calculate_typological_distance(self, lang1_code, lang2_code, feature_ids=None):
        """
        Calcula distância tipológica entre duas línguas

        Args:
            feature_ids: Lista de features a comparar (None = todas)

        Returns:
            float: Distância normalizada (0-1)
        """
        feats1 = self.get_language_features(lang1_code)
        feats2 = self.get_language_features(lang2_code)

        if not feats1 or not feats2:
            return None

        # Features comuns
        common_features = set(feats1.keys()) & set(feats2.keys())

        if feature_ids:
            common_features = common_features & set(feature_ids)

        if len(common_features) == 0:
            return None

        # Contar diferenças
        differences = 0
        for feat_id in common_features:
            if feats1[feat_id] != feats2[feat_id]:
                differences += 1

        # Normalizar
        distance = differences / len(common_features)

        return distance