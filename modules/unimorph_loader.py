"""
Carregamento de dados UniMorph (morfologia)
"""
import pandas as pd
from pathlib import Path
import requests
import zipfile
from config import DATA_DIR, URLS


class UniMorphLoader:
    def __init__(self):
        self.data_dir = DATA_DIR / "unimorph"
        self.data_dir.mkdir(exist_ok=True)
        self.data = {}  # {lang_code: DataFrame}

    def download(self):
        """Descarrega dados UniMorph"""
        print("📥 A descarregar dados UniMorph...")

        # Download do repositório GitHub
        url = "https://github.com/unimorph/data/archive/refs/heads/master.zip"
        zip_path = self.data_dir / "unimorph.zip"

        response = requests.get(url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # Extrair
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.data_dir)

        print(f"✅ Dados extraídos em {self.data_dir}")

    def load_language(self, lang_code):
        """
        Carrega dados morfológicos para uma língua específica

        Args:
            lang_code: Código da língua (ex: 'por' para português)

        Returns:
            DataFrame com paradigmas morfológicos
        """
        if lang_code in self.data:
            return self.data[lang_code]

        # Procurar ficheiro
        filepath = self.data_dir / f"data-master/{lang_code}.unimorph"

        if not filepath.exists():
            print(f"⚠️ Ficheiro não encontrado: {filepath}")
            return None

        # Carregar dados
        df = pd.read_csv(
            filepath,
            sep='\t',
            header=None,
            names=['lemma', 'form', 'features']
        )

        self.data[lang_code] = df
        print(f"📊 UniMorph {lang_code}: {len(df)} formas carregadas")

        return df

    def calculate_morphological_complexity(self, lang_code):
        """
        Calcula índice de complexidade morfológica

        Returns:
            float: Número médio de formas por lema
        """
        df = self.load_language(lang_code)

        if df is None or len(df) == 0:
            return None

        # Contar formas únicas por lema
        forms_per_lemma = df.groupby('lemma')['form'].nunique()

        # Média
        avg_forms = forms_per_lemma.mean()

        return avg_forms

    def get_morphological_distance(self, lang1_code, lang2_code):
        """
        Calcula distância morfológica entre duas línguas

        Returns:
            float: Distância normalizada (0-1)
        """
        comp1 = self.calculate_morphological_complexity(lang1_code)
        comp2 = self.calculate_morphological_complexity(lang2_code)

        if comp1 is None or comp2 is None:
            return None

        # Normalizar (assumindo máximo de 100 formas)
        max_complexity = 100
        distance = abs(comp1 - comp2) / max_complexity

        return min(distance, 1.0)