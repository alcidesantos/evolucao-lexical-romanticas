"""
Carregamento de Dados para Interface Web
Módulo puro de dados - SEM comandos Streamlit
"""

import pandas as pd
from pathlib import Path
from config import DATA_DIR

def load_results():
    """Carrega resultados da análise (função pura, sem @st.cache_data)"""

    # ==========================================================================
    # CARREGAR OUTLIERS (conceitos individuais)
    # ==========================================================================

    outliers_path = DATA_DIR / "outliers" / "latin_romance_outliers.csv"
    if outliers_path.exists():
        outliers_df = pd.read_csv(outliers_path)
    else:
        outliers_df = pd.DataFrame()
        print(f"⚠️ Ficheiro de outliers não encontrado: {outliers_path}")

    # ==========================================================================
    # CARREGAR RANKING (uma linha por língua)
    # ==========================================================================

    # Tentar carregar ranking ponderado (principal)
    ranking_path = DATA_DIR / "outliers" / "latin_romance_ranking_weighted.csv"

    if ranking_path.exists():
        ranking_df = pd.read_csv(ranking_path)
        print(f"✅ Ranking carregado: {len(ranking_df)} línguas")
    else:
        # Fallback: dados hardcoded (9 línguas originais)
        print(f"⚠️ Ranking não encontrado: {ranking_path}")
        print("   A usar dados hardcoded (9 línguas)")

        ranking_data = {
            'Rank': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'Língua': ['Italian', 'Mirandese', 'Galician', 'Catalan', 'Asturian',
                       'Spanish', 'Romanian', 'Portuguese', 'French'],
            'Distância': [0.481, 0.520, 0.526, 0.530, 0.562, 0.626, 0.627, 0.628, 0.757],
            'Conceitos': [41, 39, 39, 38, 46, 107, 110, 111, 108],
            'Classificação': ['[C] Conservador'] * 8 + ['[I] Inovador']
        }
        ranking_df = pd.DataFrame(ranking_data)

    return ranking_df, outliers_df