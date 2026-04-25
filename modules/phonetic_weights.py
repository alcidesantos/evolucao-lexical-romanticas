"""
Pesos Fonéticos para Distância de Edição Ponderada
Dia 4 - Métrica Avançada de Similaridade Lexical

Baseado em características articulatórias do ASJPcode:
https://asjp.clld.org/asjpCode

Autor: [Teu Nome]
Data: 2026
"""

# ============================================================================
# MATRIZ DE SIMILARIDADE FONÉTICA (ASJPcode)
# ============================================================================

# Estrutura: (char1, char2): similaridade [0.0 a 1.0]
# Similaridade alta (0.8-1.0) → custo baixo de substituição
# Similaridade baixa (0.0-0.3) → custo alto de substituição

PHONETIC_SIMILARITY = {
    # ========================================================================
    # VOGAIS: Similaridade por altura, abertura e arredondamento
    # ========================================================================

    # Vogais centrais/abertas
    ('a', 'ɑ'): 0.95,  # Quase idênticas
    ('a', 'ɐ'): 0.90,  # Centralização comum em português
    ('a', 'ə'): 0.70,  # Redução vocálica
    ('a', 'ɛ'): 0.60,  # Abertura similar
    ('a', 'e'): 0.40,  # Diferença de altura

    # Vogais fechadas anteriores
    ('i', 'ɪ'): 0.90,  # Quase idênticas
    ('i', 'e'): 0.70,  # Mesma posição, altura diferente
    ('i', 'y'): 0.50,  # Mesma altura, arredondamento diferente

    # Vogais fechadas posteriores
    ('u', 'ʊ'): 0.90,
    ('u', 'o'): 0.70,
    ('u', 'w'): 0.60,  # Semivogal correspondente

    # Vogais médias
    ('e', 'ɛ'): 0.85,  # Abertura próxima (comum em românicas)
    ('e', 'ə'): 0.60,  # Redução
    ('o', 'ɔ'): 0.85,  # Abertura próxima
    ('o', 'ə'): 0.60,

    # Vogais nasais (comum em português)
    ('a', 'ã'): 0.70,
    ('e', 'ẽ'): 0.70,
    ('i', 'ĩ'): 0.70,
    ('o', 'õ'): 0.70,
    ('u', 'ũ'): 0.70,

    # ========================================================================
    # CONSOANTES OCLUSIVAS: Por ponto de articulação
    # ========================================================================

    # Bilabiais
    ('p', 'b'): 0.85,  # Mesmo ponto, só muda voicing
    ('p', 'm'): 0.60,  # Mesmo ponto, nasal vs oclusiva
    ('b', 'm'): 0.65,
    ('b', 'β'): 0.75,  # Oclusiva → fricativa (lenição comum)

    # Alveolares
    ('t', 'd'): 0.85,
    ('t', 'n'): 0.60,
    ('d', 'n'): 0.65,
    ('d', 'ð'): 0.75,  # Lenição t→d→ð comum em românicas

    # Velares
    ('k', 'g'): 0.85,
    ('k', 'ŋ'): 0.60,
    ('g', 'ŋ'): 0.65,
    ('g', 'ɣ'): 0.75,  # Lenição comum

    # Palatais
    ('c', 'ɟ'): 0.85,  # Notação ASJP para palatais
    ('c', 'ɲ'): 0.60,

    # ========================================================================
    # FRICATIVAS: Por ponto de articulação
    # ========================================================================

    # Labiodentais
    ('f', 'v'): 0.85,

    # Alveolares/dentais
    ('s', 'z'): 0.85,
    ('s', 'θ'): 0.70,  # Interdentalização
    ('s', 'ʃ'): 0.50,  # Palatalização

    # Palatais
    ('ʃ', 'ʒ'): 0.85,
    ('ʃ', 'ç'): 0.60,

    # Velares/glotais
    ('x', 'ɣ'): 0.70,  # Fricativa velar surda/sonora
    ('h', 'x'): 0.50,
    ('h', 'ʔ'): 0.40,

    # ========================================================================
    # APROXIMANTES/LÍQUIDAS
    # ========================================================================

    # Laterais
    ('l', 'ʎ'): 0.75,  # Palatalização comum em românicas
    ('l', 'ɫ'): 0.80,  # Velarização (português europeu)

    # Vibrantes
    ('r', 'ɾ'): 0.80,  # Múltipla vs simples (alófonos em muitas línguas)
    ('r', 'ʀ'): 0.60,  # Uvular vs alveolar

    # Aproximantes
    ('j', 'i'): 0.70,  # Semivogal vs vogal correspondente
    ('w', 'u'): 0.70,
    ('ɥ', 'y'): 0.70,

    # ========================================================================
    # NASALAS
    # ========================================================================
    ('m', 'n'): 0.60,  # Mudança de ponto (comum em assimilação)
    ('n', 'ɲ'): 0.75,  # Palatalização
    ('n', 'ŋ'): 0.70,  # Velarização

    # ========================================================================
    # MUDANÇAS ESPECÍFICAS DE ROMÂNICAS
    # ========================================================================

    # Palatalização de velares antes de vogais anteriores (Latim→Românicas)
    ('k', 'ʃ'): 0.50,  # /k/ → /ʃ/ antes de /e,i/ (ex: centum → cento)
    ('k', 'tʃ'): 0.45,
    ('g', 'ʒ'): 0.50,  # /g/ → /ʒ/ antes de /e,i/
    ('g', 'dʒ'): 0.45,

    # Lenição intervocálica (comum em românicas ocidentais)
    ('p', 'β'): 0.70,
    ('t', 'ð'): 0.70,
    ('k', 'ɣ'): 0.70,
    ('b', 'w'): 0.50,  # Ex: habere → haver

    # Perda de consoantes finais (comum em francês, português)
    # (tratada como deleção, não substituição)

    # Ditongação (tratada como substituição + inserção)
    ('e', 'je'): 0.60,  # Ex: petra → piedra
    ('o', 'we'): 0.60,  # Ex: porta → puerta

    # Nasalização vocálica (português)
    ('a', 'ɐ̃'): 0.65,
    ('e', 'ẽ'): 0.65,
    ('o', 'õ'): 0.65,
}


# ============================================================================
# FUNÇÕES DE CÁLCULO DE CUSTO
# ============================================================================

def get_substitution_cost(char1, char2, default_cost=1.0, similarity_matrix=None):
    """
    Calcula custo de substituição baseado em similaridade fonética

    Fórmula: custo = 1.0 - similaridade

    Args:
        char1: Primeiro caractere ASJPcode
        char2: Segundo caractere ASJPcode
        default_cost: Custo para pares não definidos (padrão: 1.0)
        similarity_matrix: Dicionário de similaridades (padrão: PHONETIC_SIMILARITY)

    Returns:
        float: Custo de substituição [0.0 a 1.0]
    """
    if similarity_matrix is None:
        similarity_matrix = PHONETIC_SIMILARITY

    # Sem custo se iguais
    if char1 == char2:
        return 0.0

    # Tentar par direto
    similarity = similarity_matrix.get((char1, char2))
    if similarity is not None:
        return 1.0 - similarity

    # Tentar par invertido (similaridade é simétrica)
    similarity = similarity_matrix.get((char2, char1))
    if similarity is not None:
        return 1.0 - similarity

    # Fallback: custo máximo para pares desconhecidos
    return default_cost


def get_insertion_cost(char, default_cost=1.0):
    """Custo de inserção (sempre 1.0 na versão atual)"""
    return default_cost


def get_deletion_cost(char, default_cost=1.0):
    """Custo de deleção (sempre 1.0 na versão atual)"""
    return default_cost


# ============================================================================
# UTILITÁRIOS
# ============================================================================

def list_similar_chars(char, min_similarity=0.7, similarity_matrix=None):
    """
    Lista caracteres similares a um dado caractere

    Args:
        char: Caractere ASJPcode de referência
        min_similarity: Limite mínimo de similaridade para incluir
        similarity_matrix: Dicionário de similaridades

    Returns:
        list: Caracteres similares com suas similaridades
    """
    if similarity_matrix is None:
        similarity_matrix = PHONETIC_SIMILARITY

    similar = []
    for (c1, c2), sim in similarity_matrix.items():
        if c1 == char and sim >= min_similarity:
            similar.append((c2, sim))
        elif c2 == char and sim >= min_similarity:
            similar.append((c1, sim))

    # Remover duplicados e ordenar
    similar = list(set(similar))
    return sorted(similar, key=lambda x: -x[1])


def print_phonetic_groups(similarity_matrix=None):
    """Imprime grupos fonéticos para referência"""
    if similarity_matrix is None:
        similarity_matrix = PHONETIC_SIMILARITY

    print("Grupos de alta similaridade (≥0.80):")
    printed = set()
    for (c1, c2), sim in sorted(similarity_matrix.items(), key=lambda x: -x[1]):
        if sim >= 0.80 and (c1, c2) not in printed and (c2, c1) not in printed:
            print(f"  {c1} ↔ {c2}: {sim:.2f}")
            printed.add((c1, c2))