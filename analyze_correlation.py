"""
Análise de correlação entre distância lexical e geográfica
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from geopy.distance import geodesic
from modules.asjp_loader import ASJPLoader
from modules.distance_calculator import LinguisticDistanceCalculator
from config import TEST_LANGUAGES, TEST_LANGUAGES_NAMED, IMAGES_DIR


def main():
    print("=" * 70)
    print("📊 CORRELAÇÃO: DISTÂNCIA LEXICAL vs GEOGRÁFICA")
    print("=" * 70)

    # Carregar dados
    loader = ASJPLoader()
    loader.load()

    calculator = LinguisticDistanceCalculator()

    # Línguas para análise
    languages = TEST_LANGUAGES

    print(f"\n📋 {len(languages)} línguas em análise")

    # 1. Calcular distâncias lexicais (já calculadas)
    print("\n🔢 A calcular distâncias lexicais...")
    lexical_matrix = calculator.create_distance_matrix(languages)

    # 2. Calcular distâncias geográficas
    print("🗺️ A calcular distâncias geográficas...")
    geo_distances = []
    lexical_distances = []
    pairs = []

    for i, lang1 in enumerate(languages):
        for j, lang2 in enumerate(languages):
            if i < j:  # Apenas metade da matriz (sem duplicados)
                # Obter coordenadas
                coord1 = loader.get_language_coordinates(lang1)
                coord2 = loader.get_language_coordinates(lang2)

                # Obter tempo de divergência
                time1 = temporal.get_divergence_time(lang1, 'ky')
                time2 = temporal.get_divergence_time(lang2, 'ky')
                if time1 is None or time2 is None:
                    # Um ou ambos são outgroups (não-IE)
                    continue  # Ignorar este par na análise temporal

                if coord1 and coord2:
                    # Calcular distância geográfica (km)
                    geo_dist = geodesic(coord1, coord2).kilometers

                    # Obter distância lexical
                    lex_dist = lexical_matrix.loc[lang1, lang2]

                    geo_distances.append(geo_dist)
                    lexical_distances.append(lex_dist)
                    pairs.append((lang1, lang2))

    # Converter para arrays numpy
    geo_distances = np.array(geo_distances)
    lexical_distances = np.array(lexical_distances)

    # 3. Calcular correlações
    print("\n" + "=" * 70)
    print("📈 RESULTADOS DA CORRELAÇÃO")
    print("=" * 70)

    # Pearson (correlação linear)
    pearson_r, pearson_p = stats.pearsonr(geo_distances, lexical_distances)

    # Spearman (correlação de rank - mais robusto)
    spearman_r, spearman_p = stats.spearmanr(geo_distances, lexical_distances)

    print(f"\n📊 Correlação de Pearson:")
    print(f"   r = {pearson_r:.4f}")
    print(f"   p-value = {pearson_p:.6f}")
    print(f"   Interpretação: {interpret_correlation(pearson_r)}")

    print(f"\n📊 Correlação de Spearman:")
    print(f"   ρ = {spearman_r:.4f}")
    print(f"   p-value = {spearman_p:.6f}")
    print(f"   Interpretação: {interpret_correlation(spearman_r)}")

    # 4. Visualizar correlação
    print("\n📈 A gerar gráfico de correlação...")
    plot_correlation(
        geo_distances,
        lexical_distances,
        pairs,
        pearson_r,
        pearson_p,
        highlight_languages=['mira1251'],  # ← Destacar Mirandês
        output_file="correlation_lexical_geographic.png"
    )

    # 5. Mostrar pares extremos
    print("\n" + "=" * 70)
    print("🔍 PARES EXTREMOS")
    print("=" * 70)

    # Pares mais próximos geograficamente
    print("\n📍 Mais próximos geograficamente:")
    sorted_geo = sorted(zip(pairs, geo_distances), key=lambda x: x[1])
    for pair, dist in sorted_geo[:5]:
        lang1_name = TEST_LANGUAGES_NAMED.get(pair[0], pair[0])
        lang2_name = TEST_LANGUAGES_NAMED.get(pair[1], pair[1])
        lex_idx = pairs.index(pair)
        lex_dist = lexical_distances[lex_idx]
        print(f"   {lang1_name} ↔ {lang2_name}: {dist:.0f} km (lexical: {lex_dist:.3f})")

    # Pares mais distantes geograficamente
    print("\n📍 Mais distantes geograficamente:")
    for pair, dist in sorted_geo[-5:][::-1]:
        lang1_name = TEST_LANGUAGES_NAMED.get(pair[0], pair[0])
        lang2_name = TEST_LANGUAGES_NAMED.get(pair[1], pair[1])
        lex_idx = pairs.index(pair)
        lex_dist = lexical_distances[lex_idx]
        print(f"   {lang1_name} ↔ {lang2_name}: {dist:.0f} km (lexical: {lex_dist:.3f})")

    # Pares mais próximos lexicalmente
    print("\n🔤 Mais próximos lexicalmente:")
    sorted_lex = sorted(zip(pairs, lexical_distances), key=lambda x: x[1])
    for pair, dist in sorted_lex[:5]:
        lang1_name = TEST_LANGUAGES_NAMED.get(pair[0], pair[0])
        lang2_name = TEST_LANGUAGES_NAMED.get(pair[1], pair[1])
        geo_idx = pairs.index(pair)
        geo_dist = geo_distances[geo_idx]
        print(f"   {lang1_name} ↔ {lang2_name}: {dist:.3f} (geográfica: {geo_dist:.0f} km)")

    # Pares mais distantes lexicalmente
    print("\n🔤 Mais distantes lexicalmente:")
    for pair, dist in sorted_lex[-5:][::-1]:
        lang1_name = TEST_LANGUAGES_NAMED.get(pair[0], pair[0])
        lang2_name = TEST_LANGUAGES_NAMED.get(pair[1], pair[1])
        geo_idx = pairs.index(pair)
        geo_dist = geo_distances[geo_idx]
        print(f"   {lang1_name} ↔ {lang2_name}: {dist:.3f} (geográfica: {geo_dist:.0f} km)")

    print("\n" + "=" * 70)
    print("✅ Análise concluída!")
    print("=" * 70)


def interpret_correlation(r):
    """Interpreta o valor da correlação"""
    abs_r = abs(r)
    if abs_r >= 0.7:
        return "Forte"
    elif abs_r >= 0.5:
        return "Moderada"
    elif abs_r >= 0.3:
        return "Fraca"
    else:
        return "Muito fraca/Nula"


def plot_correlation(geo_distances, lexical_distances, pairs, pearson_r, pearson_p,
                     highlight_languages=None, output_file="correlation_lexical_geographic.png"):
    """
    Plota scatter plot da correlação com destaque para línguas específicas

    Args:
        geo_distances: Array com distâncias geográficas
        lexical_distances: Array com distâncias lexicais
        pairs: Lista de pares de glottocodes [(lang1, lang2), ...]
        pearson_r: Coeficiente de Pearson
        pearson_p: P-value de Pearson
        highlight_languages: Lista de glottocodes para destacar (ex: ['mira1251'])
        output_file: Nome do ficheiro de saída
    """
    if highlight_languages is None:
        highlight_languages = []

    plt.figure(figsize=(14, 10))

    # Scatter plot base
    plt.scatter(geo_distances, lexical_distances,
                alpha=0.6, s=80, c='lightgray', edgecolors='black', linewidth=0.5)

    # Linha de regressão
    z = np.polyfit(geo_distances, lexical_distances, 1)
    p = np.poly1d(z)
    plt.plot(geo_distances, p(geo_distances),
             "r--", linewidth=2, alpha=0.8,
             label=f'Regressão linear (r={pearson_r:.3f})')

    # Identificar pontos para anotar
    annotated_indices = set()

    # 1. Pares com línguas destacadas (ex: Mirandês)
    highlight_indices = []
    for i, (lang1, lang2) in enumerate(pairs):
        if any(lang in [lang1, lang2] for lang in highlight_languages):
            highlight_indices.append(i)
            annotated_indices.add(i)

    # 2. Pares mais próximos lexicalmente (top 3)
    lex_closest = np.argsort(lexical_distances)[:3]
    for idx in lex_closest:
        annotated_indices.add(idx)

    # 3. Pares mais distantes lexicalmente (top 3)
    lex_farthest = np.argsort(lexical_distances)[-3:]
    for idx in lex_farthest:
        annotated_indices.add(idx)

    # 4. Outliers (maior desvio da regressão - top 5)
    residuals = np.abs(lexical_distances - p(geo_distances))
    outlier_indices = np.argsort(residuals)[-5:]
    for idx in outlier_indices:
        annotated_indices.add(idx)

    # Plotar pontos destacados (línguas específicas)
    for i in highlight_indices:
        plt.scatter(geo_distances[i], lexical_distances[i],
                    s=150, c='red', edgecolors='darkred', linewidth=2, zorder=5)

    # Plotar outliers
    for i in outlier_indices:
        if i not in highlight_indices:
            plt.scatter(geo_distances[i], lexical_distances[i],
                        s=120, c='orange', edgecolors='darkorange', linewidth=2, zorder=4)

    # Plotar extremos lexicais
    for i in list(lex_closest) + list(lex_farthest):
        if i not in highlight_indices and i not in outlier_indices:
            plt.scatter(geo_distances[i], lexical_distances[i],
                        s=100, c='steelblue', edgecolors='darkblue', linewidth=2, zorder=3)

    # Anotar pontos selecionados
    for i in annotated_indices:
        lang1, lang2 = pairs[i]
        name1 = TEST_LANGUAGES_NAMED.get(lang1, lang1)
        name2 = TEST_LANGUAGES_NAMED.get(lang2, lang2)

        # Determinar tipo de ponto para estilo
        is_highlight = i in highlight_indices
        is_outlier = i in outlier_indices and not is_highlight
        is_extreme = i in lex_closest or i in lex_farthest

        # Label
        if is_highlight:
            label = f"{name1}-{name2}"
            fontsize = 9
            fontweight = 'bold'
            color = 'darkred'
            bbox_color = '#FFEB3B'  # Amarelo
            offset_y = 0.015
        elif is_outlier:
            label = f"{name1[:3]}-{name2[:3]}"
            fontsize = 8
            fontweight = 'bold'
            color = 'darkorange'
            bbox_color = '#FFE0B2'  # Laranja claro
            offset_y = -0.015
        else:
            label = f"{name1[:3]}-{name2[:3]}"
            fontsize = 7
            fontweight = 'normal'
            color = 'darkblue'
            bbox_color = 'white'
            offset_y = 0.01

        # Offset horizontal para evitar sobreposição
        offset_x = np.random.uniform(-80, 80)

        plt.annotate(
            label,
            (geo_distances[i] + offset_x, lexical_distances[i] + offset_y),
            fontsize=fontsize,
            fontweight=fontweight,
            color=color,
            ha='center',
            va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=bbox_color, alpha=0.8, edgecolor=color)
        )

    # Legenda personalizada
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
                   markersize=12, label=f'Línguas destacadas ({len(highlight_languages)})'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange',
                   markersize=10, label='Outliers'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='steelblue',
                   markersize=8, label='Pares extremos'),
        plt.Line2D([0], [0], color='red', linestyle='--', linewidth=2,
                   label=f'Regressão (r={pearson_r:.3f}, p={pearson_p:.4f})')
    ]
    plt.legend(handles=legend_elements, fontsize=9, loc='upper right')

    plt.xlabel('Distância Geográfica (km)', fontsize=12)
    plt.ylabel('Distância Lexical (0-1)', fontsize=12)
    plt.title(
        f'Correlação: Distância Geográfica vs Lexical\n'
        f'{len(pairs)} pares de línguas românicas',
        fontsize=14, fontweight='bold'
    )
    plt.grid(True, alpha=0.3, linestyle='--')

    # Guardar
    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()

if __name__ == "__main__":
    main()