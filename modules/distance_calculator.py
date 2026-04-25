"""
Calculadora de distâncias multi-dimensional
"""
import pandas as pd
import numpy as np
from modules.asjp_loader import ASJPLoader
from modules.glottolog_loader import GlottologLoader
from modules.unimorph_loader import UniMorphLoader
from modules.wals_loader import WALSLoader
from config import DIMENSION_WEIGHTS, PHONETIC_SETTINGS


def normalized_levenshtein(s1, s2):
    """Distância de Levenshtein normalizada (0-1)"""
    if len(s1) == 0 and len(s2) == 0:
        return 0.0

    # Implementação simples
    max_len = max(len(s1), len(s2))

    # Matriz de distância
    matrix = np.zeros((len(s1) + 1, len(s2) + 1))

    for i in range(len(s1) + 1):
        matrix[i, 0] = i
    for j in range(len(s2) + 1):
        matrix[0, j] = j

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i, j] = min(
                matrix[i - 1, j] + 1,  # deleção
                matrix[i, j - 1] + 1,  # inserção
                matrix[i - 1, j - 1] + cost  # substituição
            )

    return matrix[len(s1), len(s2)] / max_len

def weighted_levenshtein(s1, s2, weights=None, normalize=True):
    """
    Calcula distância de Levenshtein com custos de substituição ponderados

    Baseado em similaridade fonética: substituições entre sons similares
    têm custo reduzido, refletindo melhor a evolução linguística natural.

    Args:
        s1: Primeira string (ex: forma latina em ASJPcode)
        s2: Segunda string (ex: forma românica em ASJPcode)
        weights: Dicionário {(c1,c2): similarity} ou None para custos uniformes
        normalize: Se True, retorna valor normalizado [0,1]; se False, retorna distância bruta

    Returns:
        float: Distância normalizada [0,1] ou bruta
    """
    # Fallback para versão simples se não houver pesos
    if weights is None:
        return normalized_levenshtein(s1, s2) if normalize else levenshtein_distance(s1, s2)

    # Importar função de custo
    from modules.phonetic_weights import get_substitution_cost

    m, n = len(s1), len(s2)

    # Casos base
    if m == 0:
        return n if not normalize else 1.0
    if n == 0:
        return m if not normalize else 1.0

    # Matriz de programação dinâmica
    # dp[i][j] = custo mínimo para transformar s1[:i] em s2[:j]
    dp = [[0.0] * (n + 1) for _ in range(m + 1)]

    # Inicializar primeira coluna (deleções)
    for i in range(m + 1):
        dp[i][0] = float(i)  # Custo de deleção = 1 sempre

    # Inicializar primeira linha (inserções)
    for j in range(n + 1):
        dp[0][j] = float(j)  # Custo de inserção = 1 sempre

    # Preencher matriz
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Caracteres iguais: sem custo
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Calcular custos das três operações
                deletion_cost = dp[i - 1][j] + 1.0  # Deletar de s1
                insertion_cost = dp[i][j - 1] + 1.0  # Inserir em s1
                substitution_cost = dp[i - 1][j - 1] + get_substitution_cost(s1[i - 1], s2[j - 1],
                                                                             similarity_matrix=weights)

                # Escolher mínimo
                dp[i][j] = min(deletion_cost, insertion_cost, substitution_cost)

    # Resultado bruto
    raw_distance = dp[m][n]

    # Normalizar se solicitado
    if normalize:
        max_dist = float(max(m, n))
        return raw_distance / max_dist if max_dist > 0 else 0.0

    return raw_distance


def levenshtein_distance(s1, s2):
    """
    Versão não-normalizada de Levenshtein (para compatibilidade)

    Returns:
        int: Distância bruta (número de edições)
    """
    return normalized_levenshtein(s1, s2) * max(len(s1), len(s2))


class LinguisticDistanceCalculator:
    def __init__(self):
        self.asjp = ASJPLoader()
        # self.glottolog = GlottologLoader()
        self.unimorph = UniMorphLoader()
        self.wals = WALSLoader()

        # Carregar dados
        self.asjp.load()
        # self.glottolog.load()

    def calculate_all_distances(self, lang1_code, lang2_code):
        """
        Calcula todas as dimensões de distância entre duas línguas
        """
        distances = {}

        # 1. Distância Lexical (ASJP)
        print("  📝 Lexical...")
        distances['lexical'] = self.asjp.get_lexical_distance(
            lang1_code,
            lang2_code,
            use_segments=PHONETIC_SETTINGS['use_segments'],
            use_panphon=PHONETIC_SETTINGS['use_panphon']
        )

        # 2. Distância Geográfica (USAR ASJP, não Glottolog!)
        print("  🗺️ Geográfica...")
        coord1 = self.asjp.get_language_coordinates(lang1_code)
        coord2 = self.asjp.get_language_coordinates(lang2_code)

        if coord1 and coord2:
            try:
                from geopy.distance import geodesic
                geo_dist = geodesic(coord1, coord2).kilometers
                distances['geographic'] = geo_dist / 20000  # Normalizar (max ~20000km)
                print(f"     {coord1} ↔ {coord2} = {geo_dist:.0f} km")
            except Exception as e:
                print(f"     ⚠️ Erro ao calcular distância: {e}")
                distances['geographic'] = None
        else:
            distances['geographic'] = None
            print(f"     ⚠️ Coordenadas não disponíveis")

        # 3. Distância Morfológica (UniMorph)
        print("  🔤 Morfológica... ⚠️ Ignorada")
        distances['morphological'] = None

        # 4. Distância Tipológica (WALS)
        print("  📐 Tipológica... ❌ Ignorada")
        distances['typological'] = None

        return distances

    def calculate_weighted_distance(self, lang1_code, lang2_code, weights=None):
        """
        Calcula distância total ponderada

        Args:
            weights: Dicionário de pesos (usa DIMENSION_WEIGHTS se None)

        Returns:
            float: Distância total (0-1)
        """
        if weights is None:
            weights = DIMENSION_WEIGHTS

        distances = self.calculate_all_distances(lang1_code, lang2_code)

        # Calcular média ponderada (ignorando Nones)
        total = 0
        total_weight = 0

        for dim, weight in weights.items():
            dist = distances.get(dim)
            if dist is not None:
                total += dist * weight
                total_weight += weight

        return total / total_weight if total_weight > 0 else None

    def create_distance_matrix(self, language_codes):
        """
        Cria matriz de distâncias para múltiplas línguas

        Returns:
            DataFrame: Matriz de distâncias
        """
        n = len(language_codes)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i, n):
                if i == j:
                    matrix[i, j] = 0
                else:
                    dist = self.calculate_weighted_distance(
                        language_codes[i],
                        language_codes[j]
                    )
                    matrix[i, j] = dist if dist else 0
                    matrix[j, i] = matrix[i, j]

        return pd.DataFrame(matrix, index=language_codes, columns=language_codes)