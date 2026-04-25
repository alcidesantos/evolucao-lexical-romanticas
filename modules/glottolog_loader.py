"""
Carregamento de dados Glottolog (classificação, coordenadas)
"""
import pandas as pd
from pathlib import Path
import requests
from config import DATA_DIR, URLS


class GlottologLoader:
    def __init__(self):
        self.data_dir = DATA_DIR / "glottolog"
        self.data_dir.mkdir(exist_ok=True)
        self.languages_df = None
        self.family_df = None

    def download(self):
        """Descarrega dados Glottolog"""
        print("📥 A descarregar dados Glottolog...")

        # Nota: Glottolog requer download manual ou uso da API
        # Este é um exemplo simplificado
        urls = {
            'languages': 'https://raw.githubusercontent.com/glottolog/glottolog/master/glottolog.csv',
            'families': 'https://raw.githubusercontent.com/glottolog/glottolog/master/family.csv'
        }

        for name, url in urls.items():
            try:
                response = requests.get(url)
                filepath = self.data_dir / f"{name}.csv"

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"✅ {name} guardado")
            except Exception as e:
                print(f"⚠️ Erro a descarregar {name}: {e}")

    def load(self):
        """Carrega dados para DataFrames"""
        lang_path = self.data_dir / "languages.csv"
        fam_path = self.data_dir / "families.csv"

        if lang_path.exists():
            self.languages_df = pd.read_csv(lang_path)
            print(f"📊 Glottolog: {len(self.languages_df)} línguas carregadas")

        if fam_path.exists():
            self.family_df = pd.read_csv(fam_path)

        return self.languages_df

    def get_language_info(self, glottocode):
        """Obtém informação de uma língua específica"""
        if self.languages_df is None:
            self.load()

        info = self.languages_df[self.languages_df['glottocode'] == glottocode]
        return info.iloc[0] if len(info) > 0 else None

    def get_coordinates(self, glottocode):
        """Obtém coordenadas geográficas"""
        info = self.get_language_info(glottocode)
        if info is not None and 'latitude' in info and 'longitude' in info:
            return (info['latitude'], info['longitude'])
        return None

    def get_family_tree(self, glottocode):
        """Obtém caminho na árvore genealógica"""
        if self.languages_df is None:
            self.load()

        info = self.get_language_info(glottocode)
        if info is not None and 'family' in info:
            return info['family']
        return None

    def calculate_geographic_distance(self, lang1_code, lang2_code):
        """
        Calcula distância geográfica entre duas línguas (km)
        """
        from geopy.distance import geodesic

        coord1 = self.get_coordinates(lang1_code)
        coord2 = self.get_coordinates(lang2_code)

        if coord1 and coord2:
            return geodesic(coord1, coord2).kilometers
        return None