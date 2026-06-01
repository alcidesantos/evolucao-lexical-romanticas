"""
Pré-Calcular Matrizes de Distâncias Diretas Entre Línguas Românicas

Gera CSVs que a app Streamlit carrega instantaneamente.
Executar sempre que se adicionam/removem línguas ou se alteram métricas.

Autor: Alcides Santos | 250000693
Curso: Introdução à Inteligência Artificial (Artur Marques)
Instituto Politécnico de Santarém
Data: 2026
"""

import sys
from pathlib import Path

# Adicionar pasta raiz ao path (para encontrar config.py, modules/, etc.)
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import numpy as np
from pathlib import Path
from config import DATA_DIR, TEST_LANGUAGES_NAMED
from modules.asjp_loader import ASJPLoader
from modules.distance_calculator import (
    normalized_levenshtein,
    weighted_levenshtein,
    language_pair_distance
)
from modules.phonetic_weights import PHONETIC_SIMILARITY
import time

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

OUTPUT_DIR = DATA_DIR / "outliers"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🔗 PRÉ-CÁLCULO: Matrizes de Distâncias Diretas")
print("=" * 80)

# ============================================================================
# CARREGAR DADOS FONÉTICOS
# ============================================================================

print("\n📥 A carregar dados ASJP...")
asjp = ASJPLoader()
asjp.load()

forms_by_language = {}
for glotto, name in TEST_LANGUAGES_NAMED.items():
    words_df = asjp.get_language_words(glotto)
    forms = words_df.set_index('Parameter_ID')['Segments'].to_dict()
    # Limpar espaços para compatibilidade com PanPhon
    forms = {k: v.replace(' ', '') for k, v in forms.items()}
    forms_by_language[name] = forms

linguas = list(forms_by_language.keys())
print(f"✅ {len(linguas)} línguas carregadas: {', '.join(linguas)}")


# ============================================================================
# FUNÇÃO PARA CALCULAR MATRIZ
# ============================================================================

def compute_distance_matrix(forms_dict, linguas, distance_func, weights=None, metric_name=""):
    """
    Calcula matriz de distâncias diretas entre todas as línguas
    """
    print(f"\n🔢 A calcular matriz {metric_name}...")

    n = len(linguas)
    matrix = pd.DataFrame(np.zeros((n, n)), index=linguas, columns=linguas)

    total_pairs = n * (n - 1) // 2
    current_pair = 0
    start_time = time.time()

    for i, lang1 in enumerate(linguas):
        for j, lang2 in enumerate(linguas):
            if i == j:
                matrix.loc[lang1, lang2] = 0.0
            elif i < j:  # Só calcular metade (matriz simétrica)
                d = language_pair_distance(
                    forms_dict[lang1],
                    forms_dict[lang2],
                    distance_func,
                    weights
                )
                if d is not None:
                    matrix.loc[lang1, lang2] = d
                    matrix.loc[lang2, lang1] = d

                current_pair += 1
                elapsed = time.time() - start_time
                eta = (elapsed / current_pair * (total_pairs - current_pair)) if current_pair > 0 else 0
                print(f"   Progresso: {current_pair}/{total_pairs} pares ({eta:.0f}s restantes)", end='\r')

    elapsed_total = time.time() - start_time
    print(f"\n   ✅ Concluído em {elapsed_total:.1f} segundos")

    return matrix.astype(float)


# ============================================================================
# CALCULAR AMBAS AS MÉTRICAS
# ============================================================================

# Métrica 1: Simples (Levenshtein)
matrix_simple = compute_distance_matrix(
    forms_by_language,
    linguas,
    normalized_levenshtein,
    weights=None,
    metric_name="SIMPLES"
)

# Métrica 2: Ponderada (PanPhon)
matrix_weighted = compute_distance_matrix(
    forms_by_language,
    linguas,
    weighted_levenshtein,
    weights=PHONETIC_SIMILARITY,
    metric_name="PONDERADA"
)

# ============================================================================
# EXPORTAR PARA CSV
# ============================================================================

print("\n💾 A exportar matrizes para CSV...")

# CSV Simples
simple_csv = OUTPUT_DIR / "direct_distances_simple.csv"
matrix_simple.to_csv(simple_csv, encoding='utf-8-sig')
print(f"   ✅ {simple_csv}")

# CSV Ponderado
weighted_csv = OUTPUT_DIR / "direct_distances_weighted.csv"
matrix_weighted.to_csv(weighted_csv, encoding='utf-8-sig')
print(f"   ✅ {weighted_csv}")

# ============================================================================
# RESUMO ESTATÍSTICO
# ============================================================================

print("\n" + "=" * 80)
print("📊 RESUMO ESTATÍSTICO")
print("=" * 80)

for name, matrix in [("Simples", matrix_simple), ("Ponderada", matrix_weighted)]:
    # Extrair triângulo superior (sem diagonal)
    upper_tri = matrix.where(np.triu(np.ones(matrix.shape), k=1).astype(bool))
    values = upper_tri.stack().values

    # Encontrar par com distância mínima
    min_idx = np.unravel_index(np.argmin(upper_tri.values), upper_tri.shape)
    min_lang1 = upper_tri.index[min_idx[0]]
    min_lang2 = upper_tri.columns[min_idx[1]]

    # Encontrar par com distância máxima
    max_idx = np.unravel_index(np.argmax(upper_tri.values), upper_tri.shape)
    max_lang1 = upper_tri.index[max_idx[0]]
    max_lang2 = upper_tri.columns[max_idx[1]]

    print(f"\n{name}:")
    print(f"   Mínimo: {values.min():.3f} ({min_lang1} ↔ {min_lang2})")
    print(f"   Máximo: {values.max():.3f} ({max_lang1} ↔ {max_lang2})")
    print(f"   Média:  {values.mean():.3f}")
    print(f"   Mediana: {np.median(values):.3f}")

print("\n" + "=" * 80)
print("✅ PRÉ-CÁLCULO CONCLUÍDO!")
print("=" * 80)
print("\nAgora podes executar a app Streamlit:")
print("   streamlit run pages/3_Resultados.py")
print("\nA página 5 (Distâncias Diretas) carregará instantaneamente!")