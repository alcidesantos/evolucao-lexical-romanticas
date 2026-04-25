"""
Detetor de Mudanças Irregulares / Possíveis Empréstimos
Abordagem 3: Análise Estatística de Resíduos
Dia 4 - Complemento à Distância Ponderada

Identifica palavras com distância lexical anormalmente alta
entre Latim e línguas românicas, sugerindo:
• Empréstimos de outras línguas (ex: Árabe, Germânico)
• Mudanças fonéticas irregulares
• Substituição lexical por analogia ou tabu

Autor: [Teu Nome]
Data: 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats


def detect_irregular_words(latin_forms, romance_words, distances, concept_names=None,
                           z_threshold=2.0, min_concepts=10):
    """
    Identifica palavras com distância anormalmente alta (possíveis empréstimos)

    Método: Z-score da distância em relação à distribuição da língua

    Args:
        latin_forms: dict {concept_id: latin_form_asjp}
        romance_words: DataFrame com palavras da língua alvo (formato ASJP)
        distances: list de distâncias calculadas para cada conceito
        concept_names: dict {concept_id: name} para labels mais legíveis
        z_threshold: Limite de Z-score para considerar outlier (padrão: 2.0 = 95% confiança)
        min_concepts: Mínimo de conceitos para análise válida

    Returns:
        list: Outliers ordenados por Z-score decrescente
    """
    if len(distances) < min_concepts:
        return []

    # Calcular estatísticas da distribuição
    mean_dist = np.mean(distances)
    std_dist = np.std(distances)

    if std_dist == 0:
        return []  # Sem variação, não há outliers

    outliers = []

    # Obter IDs dos conceitos comparados
    concept_ids = romance_words['Parameter_ID'].tolist()

    for i, (dist, cid) in enumerate(zip(distances, concept_ids)):
        z_score = (dist - mean_dist) / std_dist

        if abs(z_score) > z_threshold:
            # Obter formas para referência
            latin_form = latin_forms.get(cid, 'N/A')
            romance_row = romance_words[romance_words['Parameter_ID'] == cid]
            romance_form = romance_row.iloc[0].get('Segments', romance_row.iloc[0].get('Form', 'N/A')) if len(
                romance_row) > 0 else 'N/A'

            # Nome do conceito (se disponível)
            concept_name = concept_names.get(cid, f'Concept #{cid}') if concept_names else f'Concept #{cid}'

            outliers.append({
                'concept_id': cid,
                'concept_name': concept_name,
                'latin_form': latin_form,
                'romance_form': str(romance_form).replace(' ', ''),
                'distance': dist,
                'z_score': z_score,
                'interpretation': _interpret_outlier(z_score, dist, mean_dist)
            })

    # Ordenar por Z-score absoluto (mais extremos primeiro)
    return sorted(outliers, key=lambda x: -abs(x['z_score']))


def _interpret_outlier(z_score, distance, mean_distance):
    """
    Gera interpretação textual para um outlier

    Args:
        z_score: Valor Z do outlier
        distance: Distância observada
        mean_distance: Distância média da língua

    Returns:
        str: Interpretação em português
    """
    if z_score > 0:
        # Distância maior que a média → possível empréstimo ou mudança drástica
        if distance > 0.9:
            return "🔴 Distância muito alta: possível empréstimo ou substituição lexical completa"
        elif distance > 0.75:
            return "🟠 Distância elevada: possível empréstimo ou mudança fonética irregular"
        else:
            return "🟡 Distância acima da média: mudança menos regular que o habitual"
    else:
        # Distância menor que a média → conservação excepcional ou cognato muito próximo
        if distance < 0.3:
            return "🟢 Distância muito baixa: cognato excepcionalmente conservado"
        else:
            return "🔵 Distância abaixo da média: evolução mais conservadora que a média"


def summarize_outliers_by_language(outliers_by_language):
    """
    Gera resumo estatístico de outliers por língua

    Args:
        outliers_by_language: dict {language_name: list_of_outliers}

    Returns:
        DataFrame: Resumo com contagens e estatísticas
    """
    summary = []

    for lang, outliers in outliers_by_language.items():
        if not outliers:
            continue

        high_distance = [o for o in outliers if o['z_score'] > 0]
        low_distance = [o for o in outliers if o['z_score'] < 0]

        summary.append({
            'language': lang,
            'total_outliers': len(outliers),
            'high_distance_outliers': len(high_distance),  # Possíveis empréstimos
            'low_distance_outliers': len(low_distance),  # Conservação excepcional
            'avg_z_score': np.mean([o['z_score'] for o in outliers]),
            'max_z_score': max(o['z_score'] for o in outliers),
            'most_extreme_concept': max(outliers, key=lambda x: abs(x['z_score']))['concept_name']
        })

    return pd.DataFrame(summary).sort_values('total_outliers', ascending=False)


def print_outlier_report(outliers, language_name, top_n=10):
    """
    Imprime relatório formatado de outliers para uma língua

    Args:
        outliers: Lista de outliers detectados
        language_name: Nome da língua para o cabeçalho
        top_n: Número máximo de outliers a mostrar
    """
    if not outliers:
        print(f"   ✅ {language_name}: Sem outliers detetados (evolução regular)")
        return

    print(f"\n   🔍 {language_name}: {len(outliers)} outliers detetados")
    print(f"   {'Conceito':<20} {'Latim':<12} {language_name[:10]:<12} {'Dist':<6} {'Z':<6} {'Interpretação'}")
    print(f"   {'-' * 80}")

    for outlier in outliers[:top_n]:
        concept = outlier['concept_name'][:18]
        latin = outlier['latin_form'][:10]
        romance = outlier['romance_form'][:10]
        dist = f"{outlier['distance']:.3f}"
        z = f"{outlier['z_score']:+.2f}"
        interp = outlier['interpretation'].split(':')[0]  # Apenas o ícone + categoria

        print(f"   {concept:<20} {latin:<12} {romance:<12} {dist:<6} {z:<6} {interp}")

    if len(outliers) > top_n:
        print(f"   ... e mais {len(outliers) - top_n} outliers")


def export_outliers_to_csv(outliers_by_language, output_path):
    """
    Exporta outliers para CSV para análise posterior

    Args:
        outliers_by_language: dict {language: list_of_outliers}
        output_path: Caminho para o ficheiro CSV
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_outliers = []

    for lang, outliers in outliers_by_language.items():
        for o in outliers:
            row = o.copy()
            row['language'] = lang
            all_outliers.append(row)

    if all_outliers:
        df = pd.DataFrame(all_outliers)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"   ✅ Outliers exportados para: {output_path}")