"""
Loader para dados lexicais do Latim
Dia 3 - Camada Latina
"""
import pandas as pd
from pathlib import Path
from config import DATA_DIR

class LatinLoader:
    """
    Carrega formas latinas da lista Swadesh
    """

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = DATA_DIR / "latin" / "latin_swadesh.csv"
        self.filepath = filepath
        self.df = None
        self.GLOTTOCODE = "lati1261"

    def load(self):
        """Carrega dados do Latim"""
        if not self.filepath.exists():
            print(f"⚠️ Ficheiro Latim não encontrado: {self.filepath}")
            print(f"   Cria o ficheiro com formas latinas reconstruídas")
            return None

        self.df = pd.read_csv(self.filepath)
        print(f"✅ Latim: {len(self.df)} formas carregadas")
        return self.df

    def get_forms_dict(self):
        """
        Retorna dicionário {asjp_concept_id: asjp_code}
        Compatível com estrutura do ASJP
        """
        if self.df is None:
            self.load()

        return dict(zip(self.df['asjp_concept_id'], self.df['asjp_code']))

    def get_distance_to_pie(self, pie_loader):
        """
        Calcula distância lexical entre Latim e PIE

        Returns:
            float: Distância normalizada (0-1) ou None
        """
        if self.df is None:
            self.load()

        from modules.distance_calculator import normalized_levenshtein

        pie_forms = pie_loader.get_forms_dict()
        latin_forms = self.get_forms_dict()

        distances = []
        for concept_id, latin_form in latin_forms.items():
            if concept_id in pie_forms:
                pie_form = pie_forms[concept_id]
                dist = normalized_levenshtein(
                    str(pie_form).replace(' ', ''),
                    str(latin_form).replace(' ', '')
                )
                distances.append(dist)

        return sum(distances) / len(distances) if distances else None

    def get_distance_to_romance(self, asjp_loader, target_glotto, min_concepts=15,
                                distance_func=None, weights=None):
        """
        Calcula distância lexical entre Latim e língua românica

        Args:
            asjp_loader: Instância de ASJPLoader com dados carregados
            target_glotto: Glottocode da língua alvo (ex: 'port1283')
            min_concepts: Mínimo de conceitos para análise válida

        Returns:
            float: Distância normalizada (0-1) ou None
        """
        if self.df is None:
            self.load()

        from modules.distance_calculator import normalized_levenshtein

        latin_forms = self.get_forms_dict()
        target_words = asjp_loader.get_language_words(target_glotto)

        if len(target_words) == 0:
            return None

        distances = []
        matched_concepts = []

        for _, row in target_words.iterrows():
            concept_id = row['Parameter_ID']

            if concept_id in latin_forms:
                latin_form = latin_forms[concept_id]
                other_form = row.get('Segments', row.get('Form', ''))

                if pd.notna(other_form):
                    latin_clean = str(latin_form).replace(' ', '').strip()
                    other_clean = str(other_form).replace(' ', '').strip()

                    if len(latin_clean) > 0 and len(other_clean) > 0:
                        if distance_func:
                            dist = distance_func(latin_clean, other_clean, weights=weights)
                        else:
                            from modules.distance_calculator import normalized_levenshtein
                            dist = normalized_levenshtein(latin_clean, other_clean)
                        distances.append(dist)
                        matched_concepts.append(concept_id)

        if len(distances) < min_concepts:
            print(f"   ⚠️ {target_glotto}: poucos conceitos ({len(distances)}/{min_concepts})")
            return None

        avg_dist = sum(distances) / len(distances)
        return avg_dist