"""
Carregamento de dados ASJP no formato CLDF
"""
import pandas as pd
from pathlib import Path
from config import DATA_DIR

class ASJPLoader:
    def __init__(self):
        self.data_dir = DATA_DIR / "asjp" / "lexibank-asjp-0127953" / "cldf"
        self.languages_df = None
        self.forms_df = None
        self.parameters_df = None
        self.glotto_to_lang_id = {}  # Mapeamento glottocode → Language_ID

    def load(self):
        """Carrega todos os ficheiros CLDF"""
        print("📥 A carregar dados ASJP (formato CLDF)...")

        # 1. Carregar languages.csv
        lang_file = self.data_dir / "languages.csv"
        if lang_file.exists():
            self.languages_df = pd.read_csv(lang_file)
            print(f"   ✅ languages.csv: {len(self.languages_df)} línguas")

            # Criar mapeamento glottocode → Language_ID
            # NOTA: No ASJP CLDF, ID e Glottocode podem ser diferentes
            # Vamos usar Glottocode como chave principal
            for _, row in self.languages_df.iterrows():
                glotto = row.get('Glottocode')
                lang_id = row.get('ID')
                if pd.notna(glotto) and pd.notna(lang_id):
                    self.glotto_to_lang_id[glotto] = lang_id

            print(f"   🗺️ Mapeamento criado: {len(self.glotto_to_lang_id)} línguas")
        else:
            raise FileNotFoundError(f"Ficheiro não encontrado: {lang_file}")

        # 2. Carregar parameters.csv (conceitos)
        param_file = self.data_dir / "parameters.csv"
        if param_file.exists():
            self.parameters_df = pd.read_csv(param_file)
            print(f"   ✅ parameters.csv: {len(self.parameters_df)} conceitos")
        else:
            raise FileNotFoundError(f"Ficheiro não encontrado: {param_file}")

        # 3. Carregar forms.csv (dados lexicais)
        forms_file = self.data_dir / "forms.csv"
        if forms_file.exists():
            # Carregar apenas colunas necessárias para poupar memória
            self.forms_df = pd.read_csv(
                forms_file,
                usecols=['Language_ID', 'Parameter_ID', 'Form', 'Segments']
            )
            print(f"   ✅ forms.csv: {len(self.forms_df)} formas")
        else:
            raise FileNotFoundError(f"Ficheiro não encontrado: {forms_file}")

        return self

    def get_language_id(self, glottocode):
        """
        Obtém Language_ID a partir de glottocode

        Args:
            glottocode: Código Glottolog (ex: 'port1281')

        Returns:
            str: Language_ID no ASJP ou None
        """
        if not self.glotto_to_lang_id:
            self.load()

        # Tentar correspondência direta
        if glottocode in self.glotto_to_lang_id:
            return self.glotto_to_lang_id[glottocode]

        # Tentar encontrar por substring (alguns códigos podem variar)
        for glotto, lang_id in self.glotto_to_lang_id.items():
            if glottocode in glotto or glotto in glottocode:
                print(f"   ⚠️ Correspondência aproximada: {glottocode} → {lang_id}")
                return lang_id

        print(f"   ⚠️ Glottocode não encontrado: {glottocode}")
        return None

    def get_language_words(self, glottocode, concept_ids=None):
        """
        Obtém todas as palavras de uma língua

        Args:
            glottocode: Código Glottolog (ex: 'port1281')
            concept_ids: Lista de IDs de conceitos para filtrar (ex: [1, 2, 3])

        Returns:
            DataFrame com palavras da língua
        """
        if self.forms_df is None:
            self.load()

        # Obter Language_ID
        lang_id = self.get_language_id(glottocode)
        if lang_id is None:
            return pd.DataFrame()

        # Filtrar por língua
        filtered = self.forms_df[self.forms_df['Language_ID'] == lang_id]

        # Filtrar por conceitos se especificado
        if concept_ids:
            filtered = filtered[filtered['Parameter_ID'].isin(concept_ids)]

        return filtered

    def get_lexical_distance(self, lang1_glotto, lang2_glotto, concept_ids=None,
                             use_segments=True, use_panphon=False):
        """
        Calcula distância lexical entre duas línguas

        Args:
            lang1_glotto, lang2_glotto: Glottocodes das línguas
            concept_ids: Lista de conceitos para comparar
            use_segments: Se True, usa coluna 'Segments' (mais preciso)
            use_panphon: Se True, usa panphon para distância baseada em traços

        Returns:
            float: Distância normalizada (0-1) ou None
        """
        words1 = self.get_language_words(lang1_glotto, concept_ids)
        words2 = self.get_language_words(lang2_glotto, concept_ids)

        if len(words1) == 0 or len(words2) == 0:
            print(f"   ⚠️ Dados insuficientes para {lang1_glotto} ou {lang2_glotto}")
            return None

        # Merge por Parameter_ID (conceito)
        merged = pd.merge(words1, words2, on='Parameter_ID', suffixes=('_1', '_2'))

        if len(merged) == 0:
            return None

        # Escolher coluna: Segments ou Form
        if use_segments and 'Segments_1' in merged.columns and 'Segments_2' in merged.columns:
            col1, col2 = 'Segments_1', 'Segments_2'
            print(f"   📝 A usar coluna 'Segments'")
        else:
            col1, col2 = 'Form_1', 'Form_2'
            print(f"   📝 A usar coluna 'Form'")

        # Calcular distância
        distances = []

        if use_panphon:
            # Usar Panphon (distância baseada em traços distintivos)
            from panphon import FeatureTable
            ft = FeatureTable()

            for _, row in merged.iterrows():
                seg1 = row.get(col1)
                seg2 = row.get(col2)

                if pd.isna(seg1) or pd.isna(seg2):
                    continue

                # Converter para string e remover espaços
                seg1 = str(seg1).replace(' ', '')
                seg2 = str(seg2).replace(' ', '')

                # Calcular distância panphon (levenshtein ponderado por traços)
                try:
                    dist = ft.distance(seg1, seg2)
                    # Normalizar por comprimento máximo
                    max_len = max(len(seg1), len(seg2))
                    if max_len > 0:
                        dist = dist / max_len
                    distances.append(dist)
                except Exception as e:
                    continue

            method_name = "Panphon (traços distintivos)"
        else:
            # Usar Levenshtein simples
            from modules.distance_calculator import normalized_levenshtein

            for _, row in merged.iterrows():
                form1 = row.get(col1)
                form2 = row.get(col2)

                if pd.isna(form1) or pd.isna(form2):
                    continue

                form1 = str(form1).replace(' ', '')
                form2 = str(form2).replace(' ', '')

                dist = normalized_levenshtein(form1, form2)
                distances.append(dist)

            method_name = "Levenshtein simples"

        avg_distance = sum(distances) / len(distances) if distances else None

        if avg_distance:
            print(
                f"   📊 {lang1_glotto} ↔ {lang2_glotto}: {avg_distance:.3f} ({len(distances)} conceitos, {method_name})")

        return avg_distance

    def get_available_glottocodes(self):
        """Retorna lista de glottocodes disponíveis"""
        if self.languages_df is None:
            self.load()
        return self.languages_df['Glottocode'].unique().tolist()

    def search_language(self, search_term):
        """
        Procura línguas por nome ou glottocode

        Args:
            search_term: Termo de pesquisa (ex: 'port', 'Portuguese')

        Returns:
            DataFrame com línguas encontradas
        """
        if self.languages_df is None:
            self.load()

        results = self.languages_df[
            self.languages_df['Name'].str.contains(search_term, case=False, na=False) |
            self.languages_df['Glottocode'].str.contains(search_term, case=False, na=False)
        ]

        return results

    def get_language_coordinates(self, glottocode):
        """
        Obtém coordenadas geográficas de uma língua

        Returns:
            tuple: (latitude, longitude) ou None
        """
        if self.languages_df is None:
            self.load()

        lang_id = self.get_language_id(glottocode)
        if lang_id is None:
            return None

        row = self.languages_df[self.languages_df['ID'] == lang_id]
        if len(row) > 0:
            lat = row.iloc[0]['Latitude']
            lon = row.iloc[0]['Longitude']
            if pd.notna(lat) and pd.notna(lon):
                return (lat, lon)

        return None