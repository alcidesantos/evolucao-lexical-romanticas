"""
Comparação em 2 Camadas: PIE → Latim → Românicas

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from modules.asjp_loader import ASJPLoader
from modules.pie_loader import PIELoader
from modules.latin_loader import LatinLoader
from modules.temporal_loader import TemporalLoader
from config import TEST_LANGUAGES_NAMED, IMAGES_DIR, DATA_DIR, USE_WEIGHTED_DISTANCE, WEIGHTED_DISTANCE_CONFIG, CLASSIFICATION_THRESHOLDS
from modules.classification_config import (
    classify_latin_distance,
    get_speed_label,
    get_speed_color,
    get_thresholds_for_analysis,
    THRESHOLD_LATIN_CONSERVATIVE,
    THRESHOLD_LATIN_INNOVATIVE
)
from modules.outlier_detector import (
    detect_irregular_words,
    print_outlier_report,
    summarize_outliers_by_language,
    export_outliers_to_csv
)

if USE_WEIGHTED_DISTANCE:
    from modules.distance_calculator import weighted_levenshtein
    from modules.phonetic_weights import PHONETIC_SIMILARITY
    distance_func = weighted_levenshtein
    weights = PHONETIC_SIMILARITY
    metric_suffix = '_weighted'
else:
    distance_func = None
    weights = None
    metric_suffix = '_simple'

# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def plot_two_layer_hierarchy(results_df, pie_latin_dist, output_file="latin_hierarchy.png"):
    """
    Visualização hierárquica: PIE → Latim → Românicas
    """

    results_df = results_df.copy()
    results_df['language'] = results_df['glottocode'].apply(
        lambda gc: TEST_LANGUAGES_NAMED.get(gc, gc)
    )

    plt.figure(figsize=(16, 12))

    # Posições verticais
    y_pie = 4.0
    y_latin = 2.5
    y_romance = 0.0

    # === PIE ===
    plt.scatter(0, y_pie, s=400, c='purple', edgecolors='black', linewidth=2, zorder=10)
    plt.text(0, y_pie + 0.3, 'PIE\n(~3500 BP)', ha='center', fontsize=12, fontweight='bold')

    # === LATIM ===
    plt.scatter(0, y_latin, s=300, c='darkred', edgecolors='black', linewidth=2, zorder=10)
    plt.text(0, y_latin + 0.2, f'Latim\n(d={pie_latin_dist:.3f})', ha='center', fontsize=11)

    # Linha PIE → Latim
    plt.plot([0, 0], [y_pie, y_latin], 'gray', linestyle='--', alpha=0.5, linewidth=2)
    plt.text(0.4, (y_pie + y_latin)/2, f'{pie_latin_dist:.3f}', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # === ROMÂNICAS ===
    # ✅ DEPOIS (aceita qualquer branch que contenha 'Romance' ou seja Unknown):
    # Filtrar línguas românicas: branch contém 'Romance' OU é Unknown (novas línguas)
    romance_df = results_df[
        results_df['branch'].str.contains('Romance', case=False, na=False) |
        (results_df['branch'] == 'Unknown')
        ].sort_values('latin_to_romance_dist')

    n_romance = len(romance_df)

    if n_romance > 0:
        x_positions = np.linspace(-3, 3, n_romance)

        # Cores por conservadorismo
        def get_color(dist):
            return get_speed_color(classify_latin_distance(dist))

        for i, (_, row) in enumerate(romance_df.iterrows()):
            x = x_positions[i]
            color = get_color(row['latin_to_romance_dist'])

            # Ponto
            plt.scatter(x, y_romance, s=200, c=color, edgecolors='black', linewidth=1.5, zorder=5)

            # Label
            plt.text(x, y_romance - 0.4, row['language'], ha='center', fontsize=9, rotation=45)

            # Distância
            plt.text(x, y_romance + 0.15, f'{row["latin_to_romance_dist"]:.3f}',
                    ha='center', fontsize=8, fontweight='bold')

            # Linha Latim → Românica
            plt.plot([0, x], [y_latin, y_romance], color='gray', alpha=0.3, linewidth=1)

        # Destacar Mirandês
        mirandese = romance_df[romance_df['glottocode'] == 'mira1251']
        if len(mirandese) > 0:
            mir_idx = list(romance_df.index).index(mirandese.index[0])
            mir_x = x_positions[mir_idx]
            plt.scatter(mir_x, y_romance, s=300, c='red', edgecolors='darkred',
                       linewidth=3, zorder=15, marker='*')
            plt.annotate('Mirandês', (mir_x, y_romance),
                        textcoords='offset points', xytext=(0, 35), ha='center',
                        fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9),
                        arrowprops=dict(arrowstyle='->', color='red', linewidth=2))

    # Configurar
    plt.ylim(-1, y_pie + 0.8)
    plt.xlim(-4, 4)
    plt.axis('off')

    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='purple', edgecolor='black', label='PIE'),
        Patch(facecolor='darkred', edgecolor='black', label='Latim'),
        Patch(facecolor=get_speed_color('conservative'), edgecolor='black',
              label=f'[C] Conservador (<{THRESHOLD_LATIN_CONSERVATIVE:.2f})'),
        Patch(facecolor=get_speed_color('medium'), edgecolor='black',
              label=f'[M] Médio ({THRESHOLD_LATIN_CONSERVATIVE:.2f}-{THRESHOLD_LATIN_INNOVATIVE:.2f})'),
        Patch(facecolor=get_speed_color('innovative'), edgecolor='black',
              label=f'[I] Inovador (>{THRESHOLD_LATIN_INNOVATIVE:.2f})'),
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

    plt.title('Evolução Lexical em 2 Camadas: PIE → Latim → Românicas\n'
              'Espessura das linhas ≈ distância lexical',
              fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico guardado: {output_path}")
    plt.show()


def plot_latin_to_romance_comparison(results_df, output_file="latin_to_romance.png"):
    """
    Bar chart: Distância Latim → Românicas
    """
    plt.figure(figsize=(14, max(10, len(results_df) * 0.8)))

    # Filtrar românicas e ordenar
    romance_df = results_df[results_df['branch'] == 'Romance'].sort_values('latin_to_romance_dist')

    # === OBTER THRESHOLDS DINÂMICOS (NO TOPO DA FUNÇÃO) ===
    from config import USE_WEIGHTED_DISTANCE
    threshold_c, threshold_i = get_thresholds_for_analysis('latin')
    metric_label = 'Ponderada' if USE_WEIGHTED_DISTANCE else 'Simples'

    # ======================================================

    # Cores por conservadorismo (usa módulo centralizado)
    def get_color(dist):
        return get_speed_color(classify_latin_distance(dist))

    colors = [get_color(r['latin_to_romance_dist']) for _, r in romance_df.iterrows()]

    # Bar chart
    bars = plt.barh(romance_df['language'], romance_df['latin_to_romance_dist'],
                    color=colors, edgecolor='black', linewidth=1.2)

    # Anotar valores
    for bar, dist in zip(bars, romance_df['latin_to_romance_dist']):
        plt.text(dist + 0.005, bar.get_y() + bar.get_height() / 2,
                 f'{dist:.3f}', va='center', fontsize=10, fontweight='bold')

    # Linha de referência (média)
    avg = romance_df['latin_to_romance_dist'].mean()
    plt.axvline(avg, color='gray', linestyle='--', alpha=0.6, linewidth=2,
                label=f'Média Românicas ({avg:.3f})')

    # Configurar
    # === CORREÇÃO: USAR VARIÁVEIS DINÂMICAS ===
    plt.xlabel(f'Distância Lexical Latim → Língua\n(<{threshold_c:.2f} = conservador, >{threshold_i:.2f} = inovador)',
               fontsize=11)
    # ===========================================
    plt.ylabel('Língua', fontsize=11)
    plt.title('Conservadorismo Lexical Relativo ao Latim\n'
              'Românicas ordenadas por proximidade ao Latim',
              fontsize=14, fontweight='bold', pad=20)

    # === LEGENDA COM MÉTRICA ===
    legend_elements = [
        Patch(facecolor=get_speed_color('conservative'),
              edgecolor='black',
              linewidth=1.2,
              label=f'[C] Conservador (<{threshold_c:.2f})'),
        Patch(facecolor=get_speed_color('medium'),
              edgecolor='black',
              linewidth=1.2,
              label=f'[M] Médio ({threshold_c:.2f}-{threshold_i:.2f})'),
        Patch(facecolor=get_speed_color('innovative'),
              edgecolor='black',
              linewidth=1.2,
              label=f'[I] Inovador (>{threshold_i:.2f})'),
        plt.Line2D([0], [0], color='gray', linestyle='--', linewidth=2,
                   label=f'Média ({avg:.3f}) • Métrica: {metric_label}')
    ]
    plt.legend(handles=legend_elements, fontsize=9, loc='lower right')
    # ===========================================

    plt.grid(axis='x', alpha=0.3, linestyle='--')
    min_dist = romance_df['latin_to_romance_dist'].min()
    max_dist = romance_df['latin_to_romance_dist'].max()
    plt.xlim(min_dist - 0.05, max_dist + 0.10)
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()


def plot_outliers_by_language(outliers_by_language, output_file="outliers_summary.png"):
    """
    Gráfico de barras: número de outliers por língua
    """
    if not outliers_by_language:
        return

    plt.figure(figsize=(12, 8))

    # Preparar dados
    languages = []
    counts = []
    colors = []

    for lang, outliers in sorted(outliers_by_language.items(), key=lambda x: -len(x[1])):
        languages.append(lang)
        counts.append(len(outliers))
        # Cor: verde se poucos outliers, vermelho se muitos
        if len(outliers) <= 3:
            colors.append('#4CAF50')  # Verde
        elif len(outliers) <= 6:
            colors.append('#FFC107')  # Amarelo
        else:
            colors.append('#F44336')  # Vermelho

    # Bar chart
    bars = plt.barh(languages, counts, color=colors, edgecolor='black', linewidth=1.2)

    # Anotar valores
    for bar, count in zip(bars, counts):
        plt.text(count + 0.2, bar.get_y() + bar.get_height() / 2,
                 f'{count}', va='center', fontsize=10, fontweight='bold')

    # Configurar
    plt.xlabel('Número de Palavras com Distância Anormal (|Z| > 2.0)', fontsize=11)
    plt.ylabel('Língua', fontsize=11)
    plt.title('Possíveis Empréstimos ou Mudanças Irregulares\n'
              'Valores altos sugerem mais influência externa ou inovação',
              fontsize=14, fontweight='bold', pad=20)

    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()


# ============================================================================
# EXPORTAR RANKING PARA CSV (PARA A APP STREAMLIT)
# ============================================================================

def export_ranking_to_csv(df, output_file="latin_romance_ranking_weighted.csv"):
    """
    Exporta ranking de línguas para CSV (uma linha por língua)
    Aplica nomes amigáveis do config.py
    """
    from config import DATA_DIR, TEST_LANGUAGES_NAMED

    # Preparar DataFrame para exportação
    export_df = df[['language', 'glottocode', 'branch', 'latin_to_romance_dist', 'concepts']].copy()
    export_df.columns = ['Língua', 'glottocode', 'branch', 'Distância', 'Conceitos']

    # === APLICAR NOMES AMIGÁVEIS ===
    # Substituir glottocode pelo nome amigável se existir no mapeamento
    export_df['Língua'] = export_df['glottocode'].apply(
        lambda gc: TEST_LANGUAGES_NAMED.get(gc, gc)  # ← Usa nome amigável ou mantém glottocode
    )
    # ================================

    # Adicionar Rank
    export_df['Rank'] = export_df['Distância'].rank(method='min').astype(int)

    # Adicionar Classificação
    from modules.classification_config import classify_latin_distance, get_speed_label
    export_df['Classificação'] = export_df['Distância'].apply(
        lambda d: get_speed_label(classify_latin_distance(d))
    )

    # Ordenar por Rank
    export_df = export_df.sort_values('Rank')

    # Reordenar colunas
    export_df = export_df[['Rank', 'Língua', 'glottocode', 'branch', 'Distância', 'Conceitos', 'Classificação']]

    # Guardar
    output_path = DATA_DIR / "outliers" / output_file
    export_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"   ✅ Ranking exportado: {output_path}")

    return export_df

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print("=" * 80)
    print("🏛️ COMPARAÇÃO EM 2 CAMADAS: PIE → LATIM → ROMÂNICAS")
    print("=" * 80)

    # Carregar dados
    print("\n📥 A carregar dados...")
    asjp = ASJPLoader()
    asjp.load()

    pie = PIELoader()
    if pie.load() is None:
        print("❌ PIE não carregado")
        return

    latin = LatinLoader()
    if latin.load() is None:
        print("❌ Latim não carregado")
        return

    temporal = TemporalLoader()
    temporal.load()

    outliers_by_language = {}

    # Obter thresholds apropriados para a métrica usada
    threshold_config = CLASSIFICATION_THRESHOLDS.get(f'latin{metric_suffix}',
                                                     CLASSIFICATION_THRESHOLDS['latin_simple'])
    THRESHOLD_C = threshold_config['conservative']
    THRESHOLD_I = threshold_config['innovative']

    print(f"   Métrica: {'Ponderada (fonética)' if USE_WEIGHTED_DISTANCE else 'Simples (Levenshtein)'}")
    print(f"   Thresholds: C={THRESHOLD_C:.2f}, I={THRESHOLD_I:.2f}")

    # ==========================================================================
    # CAMADA 1: PIE → LATIM
    # ==========================================================================
    print("\n" + "=" * 80)
    print("📊 CAMADA 1: PIE → LATIM")
    print("=" * 80)

    pie_latin_dist = latin.get_distance_to_pie(pie)

    if pie_latin_dist:
        print(f"   Distância PIE → Latim: {pie_latin_dist:.3f}")
        print(f"   Interpretação: {'Moderada' if pie_latin_dist < 0.60 else 'Elevada'} evolução")
    else:
        print("   ⚠️ Não foi possível calcular")
        pie_latin_dist = 0.55  # Valor estimado

    # ==========================================================================
    # CAMADA 2: LATIM → ROMÂNICAS
    # ==========================================================================
    print("\n" + "=" * 80)
    print("📊 CAMADA 2: LATIM → ROMÂNICAS")
    print("=" * 80)

    # Línguas românicas para comparar
    romance_languages = [
        # === IBÉRICAS (originais) ===
        'port1283',  # Português
        'stan1288',  # Espanhol
        'gali1258',  # Galego
        'stan1289',  # Catalão
        'astu1245',  # Asturiano
        'mira1251',  # Mirandês

        # === ITALO-ROMÂNICAS (novas) ===
        'ital1282',  # Italiano
        'sici1248',  # Siciliano ← NOVO
        'camp1261',  # Sardo (Campidanês) ← NOVO
        'cors1241',  # Corso ← NOVO

        # === GALO-ROMÂNICAS (nova) ===
        'stan1290',  # Francês
        'occi1239',  # Occitano (Aranês) ← NOVO

        # === RETO-ROMÂNICAS (novas) ===
        'roma1326',  # Romanche (Sursilvan) ← NOVO
        'friu1240',  # Friulano ← NOVO

        # === ROMENAS (nova) ===
        'roma1327',  # Romeno
        'arom1237',  # Aromeno ← NOVO
    ]

    results = []

    for glotto in romance_languages:
        name = temporal.get_language_name(glotto)
        branch = temporal.get_language_branch(glotto)

        # Calcular distância Latim → Românica
        latin_rom_dist = latin.get_distance_to_romance(
            asjp, glotto,
            distance_func=distance_func,
            weights=weights
        )

        if latin_rom_dist:
            # === ANÁLISE DE OUTLIERS (NOVO) ===
            # Obter formas e conceitos para análise detalhada
            latin_forms = latin.get_forms_dict()
            target_words = asjp.get_language_words(glotto)
            concept_names = dict(zip(asjp.parameters_df['ID'], asjp.parameters_df['Name']))

            # Recalcular distâncias por conceito para deteção de outliers
            concept_distances = []
            concept_ids = []
            for _, row in target_words.iterrows():
                cid = row['Parameter_ID']
                if cid in latin_forms:
                    latin_form = str(latin_forms[cid]).replace(' ', '')
                    romance_form = str(row.get('Segments', row.get('Form', ''))).replace(' ', '')
                    if latin_form and romance_form:
                        if distance_func:
                            d = distance_func(latin_form, romance_form, weights=weights)
                        else:
                            from modules.distance_calculator import normalized_levenshtein
                            d = normalized_levenshtein(latin_form, romance_form)
                        concept_distances.append(d)
                        concept_ids.append(cid)

            # Detetar outliers
            outliers = detect_irregular_words(
                latin_forms,
                target_words,
                concept_distances,
                concept_names=concept_names,
                z_threshold=2.0
            )

            # Guardar para resumo final
            outliers_by_language[name] = outliers
            # ================================

            results.append({
                'language': name,
                'glottocode': glotto,
                'branch': branch,
                'pie_to_latin': pie_latin_dist,
                'latin_to_romance_dist': latin_rom_dist,
                'concepts': len(target_words),
                'outliers_count': len(outliers)  # Novo campo
            })

    # Criar DataFrame
    df = pd.DataFrame(results)

    # ==========================================================================
    # RANKING
    # ==========================================================================
    print("\n" + "=" * 80)
    print("📋 RANKING: PROXIMIDADE AO LATIM")
    print("=" * 80)

    print(f"\n{'Rank':<6} {'Língua':<15} {'Latim→Rom':<12} {'Conceitos':<10} {'Status'}")
    print("-" * 70)

    for rank, row in enumerate(df.sort_values('latin_to_romance_dist').itertuples(), 1):
        speed_class = classify_latin_distance(row.latin_to_romance_dist)
        status = get_speed_label(speed_class)

        print(f"{rank:<6} {row.language:<15} {row.latin_to_romance_dist:.3f}      {row.concepts:<10} {status}")

    # ==========================================================================
    # RESUMO DE OUTLIERS / POSSÍVEIS EMPRÉSTIMOS
    # ==========================================================================
    print("\n" + "=" * 80)
    print("🔍 ANÁLISE DE MUDANÇAS IRREGULARES / POSSÍVEIS EMPRÉSTIMOS")
    print("=" * 80)

    # Imprimir relatório por língua
    for lang in ['Mirandês', 'Português', 'Italiano', 'Francês']:  # Foco nas relevantes
        if lang in outliers_by_language:
            print_outlier_report(outliers_by_language[lang], lang, top_n=5)

    # Resumo estatístico
    if outliers_by_language:
        summary_df = summarize_outliers_by_language(outliers_by_language)
        if not summary_df.empty:
            print(f"\n📊 Resumo por língua:")
            print(f"{'Língua':<15} {'Outliers':<10} {'Poss. Empréstimos':<20} {'Mais Extremo'}")
            print("-" * 70)
            for _, row in summary_df.iterrows():
                print(
                    f"{row['language']:<15} {row['total_outliers']:<10} {row['high_distance_outliers']:<20} {row['most_extreme_concept'][:15]}")

            # Exportar para CSV
            export_outliers_to_csv(outliers_by_language, DATA_DIR / "outliers" / "latin_romance_outliers.csv")

            outliers_path = DATA_DIR / "outliers" / "latin_romance_outliers.csv"
            if outliers_path.exists():
                # Ler o CSV
                outliers_df = pd.read_csv(outliers_path)

                # Substituir nomes na coluna 'language'
                if 'language' in outliers_df.columns:
                    outliers_df['language'] = outliers_df['language'].apply(
                        lambda x: TEST_LANGUAGES_NAMED.get(x, x)
                    )

                # Guardar novamente
                outliers_df.to_csv(outliers_path, index=False, encoding='utf-8-sig')
                print(f"   ✅ Nomes de outliers atualizados: {outliers_path}")

    # ==========================================================================
    # FOCO: MIRANDÊS vs PORTUGUÊS
    # ==========================================================================
    mirandese = df[df['glottocode'] == 'mira1251']
    portuguese = df[df['glottocode'] == 'port1283']

    if len(mirandese) > 0 and len(portuguese) > 0:
        print("\n" + "=" * 80)
        print("🔍 FOCO: MIRANDÊS vs PORTUGUÊS")
        print("=" * 80)

        mir_dist = mirandese.iloc[0]['latin_to_romance_dist']
        por_dist = portuguese.iloc[0]['latin_to_romance_dist']
        diff = mir_dist - por_dist

        print(f"   Mirandês:  Lat→Rom {mir_dist:.3f}")
        print(f"   Português: Lat→Rom {por_dist:.3f}")
        print(f"   Diferença: {diff:+.3f}")

        if diff < -0.02:
            print(f"   ✅ Mirandês é SIGNIFICATIVAMENTE mais conservador que o Português")
        elif diff < 0:
            print(f"   ✅ Mirandês é ligeiramente mais conservador que o Português")
        elif diff > 0.02:
            print(f"   ⚠️ Mirandês é SIGNIFICATIVAMENTE mais inovador que o Português")
        else:
            print(f"   ➡️ Mirandês e Português têm conservadorismo similar")

        # Comparar com média
        avg = df['latin_to_romance_dist'].mean()
        mir_deviation = mir_dist - avg
        por_deviation = por_dist - avg

        print(f"\n   Em relação à média das românicas ({avg:.3f}):")
        print(f"   Mirandês:  {mir_deviation:+.3f} ({'abaixo' if mir_deviation < 0 else 'acima'} da média)")
        print(f"   Português: {por_deviation:+.3f} ({'abaixo' if por_deviation < 0 else 'acima'} da média)")

    # ==========================================================================
    # NOTA METODOLÓGICA
    # ==========================================================================
    print("\n" + "=" * 80)
    print("⚠️ NOTA METODOLÓGICA")
    print("=" * 80)
    print("""
Esta análise em 2 camadas separa:

1. PIE → Latim: Evolução profunda (~3500 anos)
   • Distância típica: 0.50-0.60
   • Muitas substituições de raízes PIE

2. Latim → Românicas: Evolução recente (~2000 anos)
   • Distância típica: 0.30-0.45
   • Cognatos mais diretos, mais comparabilidade

VANTAGEM: A camada 2 permite ajuste temporal mais significativo
e comparação mais sensível entre línguas românicas.
""")

    # ==========================================================================
    # VISUALIZAÇÕES
    # ==========================================================================
    print("\n📈 A gerar visualizações...")
    plot_two_layer_hierarchy(df, pie_latin_dist)
    plot_latin_to_romance_comparison(df)
    plot_outliers_by_language(outliers_by_language)

    # ==========================================================================
    # EXPORTAR RANKING PARA A APP STREAMLIT
    # ==========================================================================
    export_ranking_to_csv(df, f"latin_romance_ranking{metric_suffix}.csv")

    print("\n✅ Análise em 2 camadas concluída!")


if __name__ == "__main__":
    main()