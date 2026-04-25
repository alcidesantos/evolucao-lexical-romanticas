"""
Configuração centralizada de thresholds de classificação
Dia 3 - Camada Latina
"""

# ============================================================================
# THRESHOLDS PARA CLASSIFICAÇÃO DE CONSERVADORISMO
# ============================================================================

# Distância Latim → Românicas
THRESHOLD_LATIN_CONSERVATIVE = 0.66  # Abaixo disto = conservador
THRESHOLD_LATIN_INNOVATIVE = 0.74  # Acima disto = inovador

# Distância PIE → Língua (para análise PIE direta)
THRESHOLD_PIE_CONSERVATIVE = 0.83
THRESHOLD_PIE_INNOVATIVE = 0.87


# ============================================================================
# FUNÇÕES DE CLASSIFICAÇÃO
# ============================================================================

def classify_latin_distance(distance):
    """
    Classifica distância Latim → Românica

    Args:
        distance: Distância lexical (0-1)

    Returns:
        str: 'conservative', 'medium', ou 'innovative'
    """
    if distance < THRESHOLD_LATIN_CONSERVATIVE:
        return 'conservative'
    elif distance < THRESHOLD_LATIN_INNOVATIVE:
        return 'medium'
    else:
        return 'innovative'


def classify_pie_distance(distance):
    """
    Classifica distância PIE → Língua

    Args:
        distance: Distância lexical (0-1)

    Returns:
        str: 'conservative', 'medium', ou 'innovative'
    """
    if distance < THRESHOLD_PIE_CONSERVATIVE:
        return 'conservative'
    elif distance < THRESHOLD_PIE_INNOVATIVE:
        return 'medium'
    else:
        return 'innovative'


def get_speed_label(speed_class):
    """
    Retorna label formatado para classe de velocidade

    Args:
        speed_class: 'conservative', 'medium', ou 'innovative'

    Returns:
        str: Label formatado
    """
    label_map = {
        'conservative': '[C] Conservador',
        'medium': '[M] Médio',
        'innovative': '[I] Inovador'
    }
    return label_map.get(speed_class, '[?]')


def get_speed_color(speed_class):
    """
    Retorna cor para classe de velocidade

    Args:
        speed_class: 'conservative', 'medium', ou 'innovative'

    Returns:
        str: Código hexadecimal da cor
    """
    color_map = {
        'conservative': '#4CAF50',  # Verde
        'medium': '#FFC107',  # Amarelo
        'innovative': '#F44336'  # Vermelho
    }
    return color_map.get(speed_class, '#999999')


def get_thresholds_for_analysis(analysis_type='latin'):
    """
    Retorna thresholds para um tipo de análise

    Args:
        analysis_type: 'latin', 'latin_weighted', 'latin_simple', 'pie', etc.

    Returns:
        tuple: (threshold_conservative, threshold_innovative)
    """
    from config import USE_WEIGHTED_DISTANCE

    # Se não especificar weighted/simple, usa configuração global
    if analysis_type == 'latin':
        if USE_WEIGHTED_DISTANCE:
            return THRESHOLD_LATIN_CONSERVATIVE, THRESHOLD_LATIN_INNOVATIVE
        else:
            return 0.66, 0.74  # Thresholds simples
    elif analysis_type == 'latin_weighted':
        return THRESHOLD_LATIN_CONSERVATIVE, THRESHOLD_LATIN_INNOVATIVE
    elif analysis_type == 'latin_simple':
        return 0.66, 0.74
    elif analysis_type == 'pie':
        if USE_WEIGHTED_DISTANCE:
            return THRESHOLD_PIE_CONSERVATIVE, THRESHOLD_PIE_INNOVATIVE
        else:
            return 0.83, 0.87
    else:
        # Fallback
        return 0.66, 0.74