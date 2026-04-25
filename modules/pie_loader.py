"""
Loader para Proto-Indo-European (dados manuais reconstruídos)
"""
import pandas as pd
from pathlib import Path
from config import PIE_DIR


class PIELoader:
    """
    Loader para formas reconstruídas do PIE
    Dados baseados em reconstruções académicas consensuais
    """

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = PIE_DIR / "pie_swadesh.csv"
        self.filepath = filepath
        self.df = None
        self.GLOTTOCODE = "pie_reconstructed"

    def load(self):
        """Carrega dados do PIE"""
        if not self.filepath.exists():
            print(f"⚠️ Ficheiro PIE não encontrado: {self.filepath}")
            print(f"   Cria o ficheiro em: {self.filepath}")
            print(f"   Pasta PIE: {PIE_DIR}")
            return None

        self.df = pd.read_csv(self.filepath)
        print(f"✅ PIE: {len(self.df)} formas reconstruídas carregadas")
        return self.df

    def get_forms_dict(self):
        """Retorna dicionário {concept_id: asjp_code}"""
        if self.df is None:
            self.load()
        if 'asjp_concept_id' in self.df.columns:
            return dict(zip(self.df['asjp_concept_id'], self.df['asjp_code']))
        else:
            # Fallback para concept_id se coluna não existir
            return dict(zip(self.df['concept_id'], self.df['asjp_code']))

    def get_lexical_distance_to(self, asjp_loader, target_glotto, concept_ids=None):
        """Calcula distância lexical entre PIE e uma língua alvo"""
        if self.df is None:
            self.load()

        # Obter formas PIE (mapeadas por asjp_concept_id)
        pie_forms = self.get_forms_dict()

        # Obter palavras da língua alvo
        target_words = asjp_loader.get_language_words(target_glotto, concept_ids)

        if len(target_words) == 0:
            print(f"   ⚠️ Sem dados para {target_glotto}")
            return None

        from modules.distance_calculator import normalized_levenshtein

        distances = []
        matched_concepts = []

        for _, row in target_words.iterrows():
            concept_id = row['Parameter_ID']  # ID do ASJP

            # Procurar forma PIE correspondente
            if concept_id not in pie_forms:
                continue

            pie_form = pie_forms[concept_id]
            other_form = row.get('Segments', row.get('Form', ''))

            if pd.isna(other_form) or pd.isna(pie_form):
                continue

            # Limpar formas
            other_clean = str(other_form).replace(' ', '').strip()
            pie_clean = str(pie_form).replace(' ', '').strip()

            if len(other_clean) == 0 or len(pie_clean) == 0:
                continue

            dist = normalized_levenshtein(pie_clean, other_clean)
            distances.append(dist)
            matched_concepts.append(concept_id)

        if len(distances) < 10:
            print(f"   ⚠️ Poucos conceitos válidos: {len(distances)}")
            return None

        avg_dist = sum(distances) / len(distances)
        print(f"   {target_glotto}: {avg_dist:.3f} ({len(distances)} conceitos)")

        return avg_dist