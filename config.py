"""
Configurações globais do pipeline
"""
import os
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)
PIE_DIR = DATA_DIR / "PIE"
PIE_DIR.mkdir(exist_ok=True)

# URLs das bases de dados
URLS = {
    'asjp': 'https://asjp.clld.org/static/download/asjp.csv',
    'glottolog': 'https://glottolog.org/static/download/glottolog.csv',
    'unimorph': 'https://github.com/unimorph/data/archive/refs/heads/master.zip',
    'wals': 'https://wals.info/static/download/wals.csv'
}

# Línguas de exemplo para teste
TEST_LANGUAGES = [
    'port1283',  # Português
    'stan1288',  # Espanhol
    'stan1290',  # Francês
    'ital1282',  # Italiano
    'roma1327',  # Romeno
    'mira1251',  # Mirandês
    'gali1258',  # Galego
    'stan1289',  # Catalão
    'astu1245',  # Asturiano
]

TEST_LANGUAGES_EXPANDED = TEST_LANGUAGES + [
    'engli1273', 'dutc1256', 'germ1287', 'swed1254', 'icel1247',  # Germânicas
    'russ1263', 'poli1260', 'czech1258', 'bulg1262', 'serb1264',  # Eslavas
    'iris1253', 'wels1247',  # Célticas
    'gree1276', 'arme1235', 'pers1269', 'hind1269'  # Outros ramos
]

TEST_LANGUAGES_NAMED = {
    # === IBÉRICAS ===
    'port1283': 'Portuguese',
    'stan1288': 'Spanish',
    'gali1258': 'Galician',
    'stan1289': 'Catalan',
    'astu1245': 'Asturian',
    'mira1251': 'Mirandese',

    # === ITALO-ROMÂNICAS ===
    'ital1282': 'Italian',
    'camp1261': 'Sardinian',
    'cors1241': 'Corsican',
    'sici1248': 'Sicilian',

    # === GALO-ROMÂNICAS ===
    'stan1290': 'French',
    'occi1239': 'Occitan',

    # === RETO-ROMÂNICAS ===
    'roma1326': 'Romansh',
    'friu1240': 'Friulian',

    # === ROMENAS ===
    'roma1327': 'Romanian',
    'arom1237': 'Aromanian',
}

# Pesos para dimensões (ajustáveis)
DIMENSION_WEIGHTS = {
    'lexical': 0.60,
    'phonological': 0.00,
    'morphological': 0.00,
    'typological': 0.00,
    'geographic': 0.40,
}

# Configurações fonéticas
PHONETIC_SETTINGS = {
    'use_segments': True,      # True = usa Segments, False = usa Form
    'use_panphon': False,       # True = usa panphon, False = usa Levenshtein simples
}

# Em config.py

# Cores por sub-família (para visualizações)
LANGUAGE_COLORS = {
    'Ibero-Romance Western': '#FF6B6B',
    'Ibero-Romance Eastern': '#4ECDC4',
    'Gallo-Romance': '#45B7D1',
    'Italo-Romance': '#FFA07A',
    'Balkan-Romance': '#98D8C8',
    'Astur-Leonese': '#F7DC6F',
    'Rhaeto-Romance': '#B19CD9',
}

BRANCH_COLORS = {
    'Romance': '#E41A1C',      # Vermelho
    'Germanic': '#377EB8',     # Azul
    'Slavic': '#4DAF4A',       # Verde
    'Celtic': '#984EA3',       # Roxo
    'Hellenic': '#FF7F00',     # Laranja
    'Armenian': '#FFFF33',     # Amarelo
    'Indo-Iranian': '#A65628', # Castanho
    'Italic': '#F781BF',       # Rosa (Latim)
}

# Mapeamento glottocode → sub-família
LANGUAGE_FAMILY = {
    # === IBÉRICAS ===
    'port1283': 'Romance',  # ← Simplificado para 'Romance'
    'gali1258': 'Romance',
    'stan1288': 'Romance',
    'stan1289': 'Romance',
    'astu1245': 'Romance',
    'mira1251': 'Romance',

    # === ITALO-ROMÂNICAS ===
    'ital1282': 'Romance',
    'camp1261': 'Romance',  # ← Sardinian
    'cors1241': 'Romance',  # ← Corsican
    'sici1248': 'Romance',  # ← Sicilian

    # === GALO-ROMÂNICAS ===
    'stan1290': 'Romance',
    'occi1239': 'Romance',  # ← Occitan

    # === RETO-ROMÂNICAS ===
    'roma1326': 'Romance',  # ← Romansh
    'friu1240': 'Romance',  # ← Friulian

    # === ROMENAS ===
    'roma1327': 'Romance',
    'arom1237': 'Romance',  # ← Aromanian
}

# ============================================================================
# CONFIGURAÇÃO DE MÉTRICAS DE DISTÂNCIA
# ============================================================================

# Usar distância de edição ponderada (foneticamente informada)
# Quando True, substituições entre sons similares têm custo reduzido
# Quando False, usa Levenshtein padrão (todos os custos = 1)
USE_WEIGHTED_DISTANCE = True  # ← Alterar para False para usar versão simples

# Parâmetros para distância ponderada
WEIGHTED_DISTANCE_CONFIG = {
    'similarity_matrix': 'phonetic_weights.PHONETIC_SIMILARITY',  # Matriz a usar
    'default_substitution_cost': 1.0,  # Custo para pares não definidos
    'normalize': True,  # Retornar valor normalizado [0,1]
}

# Thresholds para classificação (ajustados para cada métrica)
# Nota: Valores diferentes para weighted vs. simple!
CLASSIFICATION_THRESHOLDS = {
    'latin_weighted': {'conservative': 0.58, 'innovative': 0.64},
    'latin_simple': {'conservative': 0.66, 'innovative': 0.74},
    'pie_weighted': {'conservative': 0.75, 'innovative': 0.82},
    'pie_simple': {'conservative': 0.83, 'innovative': 0.87},
}