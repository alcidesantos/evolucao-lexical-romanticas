"""
Módulo para ajuste temporal de distâncias lexicais (Lei de Swadesh)
Dia 2 - Análise de Velocidade de Evolução
"""
import numpy as np


def expected_change(time_ky, lambda_rate=0.14):
    """
    Calcula mudança lexical esperada para um dado tempo

    Modelo exponencial: D(t) = 1 - e^(-λt)

    Args:
        time_ky: Tempo em milénios
        lambda_rate: Taxa de mudança (0.14 = referência Swadesh)

    Returns:
        float: Distância esperada [0, 1]
    """
    return 1 - np.exp(-lambda_rate * time_ky)


def adjust_distance(raw_distance, time_ky, lambda_rate=0.14):
    """
    Ajusta distância observada pelo tempo esperado

    Fórmula: adjusted = observed / expected

    Interpretação:
    - adjusted < 1.0 → evolução mais lenta que a média (conservador)
    - adjusted > 1.0 → evolução mais rápida que a média (inovador)

    Args:
        raw_distance: Distância lexical observada [0, 1]
        time_ky: Tempo de divergência em milénios
        lambda_rate: Taxa de referência

    Returns:
        float: Distância ajustada (normalizada para [0, 1.5])
    """
    if time_ky is None or time_ky <= 0 or raw_distance is None:
        return raw_distance

    expected = expected_change(time_ky, lambda_rate)

    if expected <= 0:
        return raw_distance

    adjusted = raw_distance / expected

    # Limitar superiormente para evitar outliers extremos
    # (mas não limitar a 1.0 para permitir identificar línguas muito inovadoras)
    return min(adjusted, 2.0)


def classify_evolution_speed(adjusted_distance, threshold_slow=0.9, threshold_fast=1.1):
    """
    Classifica velocidade de evolução com base na distância ajustada

    Args:
        adjusted_distance: Distância após ajuste temporal
        threshold_slow: Limite inferior para "lento"
        threshold_fast: Limite superior para "rápido"

    Returns:
        str: 'slow', 'medium', 'fast', ou 'unknown'
    """
    if adjusted_distance is None:
        return 'unknown'

    if adjusted_distance < threshold_slow:
        return 'slow'
    elif adjusted_distance > threshold_fast:
        return 'fast'
    else:
        return 'medium'


def get_speed_emoji(speed_class):
    """
    Retorna emoji para classe de velocidade

    Args:
        speed_class: 'slow', 'medium', 'fast', ou 'unknown'

    Returns:
        str: Emoji correspondente
    """
    emoji_map = {
        'slow': '🐢',
        'medium': '➡️',
        'fast': '🐇',
        'unknown': '⚠️'
    }
    return emoji_map.get(speed_class, '❓')


def get_speed_label(speed_class):
    """
    Retorna label descritivo para classe de velocidade

    Args:
        speed_class: 'slow', 'medium', 'fast', ou 'unknown'

    Returns:
        str: Label em português
    """
    label_map = {
        'slow': 'Conservador',
        'medium': 'Médio',
        'fast': 'Inovador',
        'unknown': 'Desconhecido'
    }
    return label_map.get(speed_class, 'N/A')


def calculate_retention_rate(distance, time_ky):
    """
    Calcula taxa de retenção lexical implícita

    Fórmula: retenção = 1 - distância
    Taxa anual: retenção^(1/tempo)

    Args:
        distance: Distância lexical [0, 1]
        time_ky: Tempo em milénios

    Returns:
        float: Taxa de retenção anual (0-1)
    """
    if time_ky is None or time_ky <= 0:
        return None

    retention = 1 - distance

    if retention <= 0:
        return 0.0

    # Taxa de retenção por milénio
    rate_per_ky = retention ** (1 / time_ky)

    return rate_per_ky