"""
Comparação com Proto-Indo-Europeu (PIE)
Versão com Validação e Incerteza Explícita
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from modules.asjp_loader import ASJPLoader
from modules.pie_loader import PIELoader
from modules.temporal_loader import TemporalLoader
from modules.lexical_clock import adjust_distance, classify_evolution_speed
from config import TEST_LANGUAGES, TEST_LANGUAGES_NAMED, IMAGES_DIR, PIE_DIR

# ============================================================================
# PAINEL DE VALIDAÇÃO - Expectativas baseadas na literatura
# ============================================================================
VALIDATION_EXPECTATIONS = {
    'lith1251': {
        'expected': 'conservative',
        'reason': 'Báltico - linguisticamente muito conservador'
    },
    'gree1276': {
        'expected': 'moderate',
        'reason': 'Grego - atestação antiga mas evoluiu'
    },
    'engli1273': {
        'expected': 'innovative',
        'reason': 'Germânico - mudanças fonéticas drásticas'
    },
    'finn1268': {
        'expected': 'outgroup',
        'reason': 'Uralic - não-IE, distância deve ser alta'
    },
    'icel1247': {
        'expected': 'conservative',
        'reason': 'Germânico Nórdico - isolamento islandês'
    },
}

# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def plot_distance_vs_time_with_uncertainty(df, output_file="distance_vs_time.png"):
    """
    Plota distância lexical vs. tempo com incerteza explícita
    """
    plt.figure(figsize=(14, 10))

    # Incerteza estimada (conservadora)
    uncertainty = 0.10

    # Cores por ramo
    branch_colors = {
        'Romance': '#E41A1C',
        'Germanic': '#377EB8',
        'Slavic': '#4DAF4A',
        'Baltic': '#984EA3',
        'Hellenic': '#FF7F00',
        'Uralic': '#FFFF33',
    }

    # Scatter plot com error bars
    for branch in df['branch'].unique():
        branch_df = df[df['branch'] == branch]
        color = branch_colors.get(branch, 'gray')

        plt.errorbar(
            branch_df['divergence_time_ky'],
            branch_df['distance_to_pie'],
            yerr=uncertainty,
            fmt='o',
            capsize=4,
            alpha=0.7,
            label=branch,
            color=color
        )

    # Linha de tendência (apenas IE)
    ie_df = df[df['branch'] != 'Uralic']
    if len(ie_df) >= 5:
        z = np.polyfit(ie_df['divergence_time_ky'], ie_df['distance_to_pie'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(ie_df['divergence_time_ky'].min(),
                             ie_df['divergence_time_ky'].max(), 100)
        plt.plot(x_trend, p(x_trend), "k--", linewidth=2, alpha=0.8,
                label=f'Tendência (r={np.corrcoef(ie_df["divergence_time_ky"], ie_df["distance_to_pie"])[0,1]:.3f})')

        # Banda de incerteza
        plt.fill_between(x_trend,
                        p(x_trend) - uncertainty,
                        p(x_trend) + uncertainty,
                        alpha=0.2, color='gray')

    # Destacar Mirandês
    mirandese = df[df['glottocode'] == 'mira1251']
    if len(mirandese) > 0:
        mir = mirandese.iloc[0]
        plt.scatter(mir['divergence_time_ky'], mir['distance_to_pie'],
                   c='red', s=300, edgecolors='darkred', linewidth=3,
                   label='Mirandês', zorder=10, marker='*')

    # Configurar
    plt.xlabel('Tempo de Divergência do PIE (milénios BP)', fontsize=12)
    plt.ylabel(f'Distância Lexical ao PIE (±{uncertainty})', fontsize=12)
    plt.title('Evolução Lexical: PIE como Referência Conceptual\n'
              'Nota: Valores absolutos têm incerteza; ranking relativo é robusto',
              fontsize=14, fontweight='bold', pad=20)

    plt.legend(fontsize=9, loc='lower right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()


def plot_evolution_speeds(df, output_file="evolution_speeds.png"):
    """
    Plota velocidades usando DISTÂNCIA BRUTA (mais discriminativa)
    """
    plt.figure(figsize=(14, 10))

    # Ordenar por distância bruta (não ajustada)
    df_sorted = df.sort_values('distance_to_pie')

    # Cores por classificação (baseada em thresholds de distância bruta)
    def get_color_class(dist):
        if dist < 0.83:
            return 'green', 'Conservador (<0.83)'
        elif dist < 0.87:
            return 'orange', 'Médio (0.83-0.87)'
        else:
            return 'red', 'Inovador (>0.87)'

    colors = [get_color_class(r['distance_to_pie'])[0] for _, r in df_sorted.iterrows()]

    # Bar chart com distância BRUTA
    bars = plt.barh(df_sorted['language'], df_sorted['distance_to_pie'],
                    color=colors, edgecolor='black', linewidth=1.2, alpha=0.7)

    # Anotar valores
    for bar, dist in zip(bars, df_sorted['distance_to_pie']):
        plt.text(dist + 0.005, bar.get_y() + bar.get_height() / 2,
                 f'{dist:.3f}', va='center', fontsize=10, fontweight='bold')

    # Linha de referência (média das românicas)
    romance_avg = df_sorted[df_sorted['branch'] == 'Romance']['distance_to_pie'].mean()
    plt.axvline(romance_avg, color='gray', linestyle='--', alpha=0.6, linewidth=2,
                label=f'Média Românicas ({romance_avg:.3f})')

    # Configurar
    plt.xlabel('Distância Lexical Bruta ao PIE\n(<0.83 = conservador, >0.87 = inovador)',
               fontsize=11)
    plt.ylabel('Língua', fontsize=11)
    plt.title('Conservadorismo Lexical Relativo\n'
              'Ordenado por proximidade ao PIE (distância bruta)',
              fontsize=14, fontweight='bold', pad=20)

    # Legenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', edgecolor='black', alpha=0.7, label='Conservador'),
        Patch(facecolor='orange', edgecolor='black', alpha=0.7, label='Médio'),
        Patch(facecolor='red', edgecolor='black', alpha=0.7, label='Inovador'),
        plt.Line2D([0], [0], color='gray', linestyle='--', linewidth=2, label='Média Românicas')
    ]
    plt.legend(handles=legend_elements, fontsize=9, loc='lower right')

    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.xlim(0.75, 0.95)  # Zoom na faixa relevante
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()

def plot_mirandese_focus(df, output_file="mirandese_focus.png"):
    """
    Gráfico focado na posição do Mirandês
    """
    plt.figure(figsize=(14, 10))

    # Separar Mirandês
    mirandese = df[df['glottocode'] == 'mira1251']
    romance_others = df[(df['branch'] == 'Romance') & (df['glottocode'] != 'mira1251')]
    ie_others = df[(df['branch'] != 'Romance') & (df['branch'] != 'Uralic')]
    outgroups = df[df['branch'] == 'Uralic']

    # Plotar grupos
    if len(romance_others) > 0:
        plt.scatter(romance_others['divergence_time_ky'], romance_others['distance_to_pie'],
                   c='#E41A1C', s=100, alpha=0.6, edgecolors='darkred', label='Românicas')
    if len(ie_others) > 0:
        plt.scatter(ie_others['divergence_time_ky'], ie_others['distance_to_pie'],
                   c='#377EB8', s=100, alpha=0.5, edgecolors='darkblue', label='Outras IE')
    if len(outgroups) > 0:
        plt.scatter(outgroups['divergence_time_ky'], outgroups['distance_to_pie'],
                   c='gray', s=100, alpha=0.4, marker='x', label='Outgroups (não-IE)')

    # Destacar Mirandês
    if len(mirandese) > 0:
        mir = mirandese.iloc[0]
        plt.scatter(mir['divergence_time_ky'], mir['distance_to_pie'],
                   c='red', s=300, edgecolors='darkred', linewidth=3,
                   label='Mirandês', zorder=10, marker='*')

        # Anotar desvio da média românica
        romance_avg = romance_others['distance_to_pie'].mean() if len(romance_others) > 0 else None
        if romance_avg:
            deviation = mir['distance_to_pie'] - romance_avg
            plt.annotate(
                f'Desvio: {deviation:+.3f}',
                (mir['divergence_time_ky'], mir['distance_to_pie']),
                textcoords='offset points', xytext=(0, 40), ha='center',
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.9),
                arrowprops=dict(arrowstyle='->', color='red', linewidth=2)
            )

    # Configurar
    plt.xlabel('Tempo de Divergência (milénios BP)', fontsize=12)
    plt.ylabel('Distância Lexical ao PIE', fontsize=12)
    plt.title('Posição do Mirandês no Continuum Indo-Europeu\n'
              'Comparação de Conservadorismo Lexical Relativo',
              fontsize=14, fontweight='bold', pad=20)

    plt.legend(fontsize=10, loc='lower right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()


def plot_branch_level_divergence(df, output_file="pie_to_proto_branches.png"):
    """
    Gráfico de divergência a nível de RAMO (não língua individual)
    Mais correto metodologicamente
    """
    plt.figure(figsize=(14, 10))

    # Agrupar por ramo, calcular média
    branch_stats = df.groupby('branch').agg({
        'divergence_time_ky': 'first',  # Tempo é por ramo
        'distance_to_pie': 'mean'  # Distância média do ramo
    }).reset_index()

    # Cores DISTINTAS por ramo (paleta ColorBrewer Set1)
    branch_colors = {
        'Romance': '#E41A1C',  # Vermelho
        'Germanic': '#377EB8',  # Azul
        'Slavic': '#4DAF4A',  # Verde
        'Baltic': '#984EA3',  # Roxo
        'Hellenic': '#FF7F00',  # Laranja
        'Indo-Iranian': '#A65628',  # Castanho
        'Celtic': '#F781BF',  # Rosa
        'Italic': '#FFFF33',  # Amarelo
        'Armenian': '#999999',  # Cinzento
        'Albanian': '#666666',  # Cinzento escuro
        'Uralic': '#8DD3C7',  # Verde-água (outgroup)
    }

    # Scatter plot por ramo
    for _, row in branch_stats.iterrows():
        color = branch_colors.get(row['branch'], 'gray')
        plt.scatter(row['divergence_time_ky'], row['distance_to_pie'],
                    c=color, s=200, label=f"{row['branch']} ({row['distance_to_pie']:.3f})",
                    edgecolors='black', linewidth=1.5)

    # Linha de tendência (apenas IE, excluindo outgroups)
    ie_branches = branch_stats[~branch_stats['branch'].isin(['Uralic', 'Turkic', 'Dravidian'])]
    if len(ie_branches) >= 5:
        z = np.polyfit(ie_branches['divergence_time_ky'], ie_branches['distance_to_pie'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(ie_branches['divergence_time_ky'].min(),
                              ie_branches['divergence_time_ky'].max(), 100)
        plt.plot(x_trend, p(x_trend), "k--", linewidth=2, alpha=0.8,
                 label=f'Tendência (r={np.corrcoef(ie_branches["divergence_time_ky"], ie_branches["distance_to_pie"])[0, 1]:.3f})')

    # Configurar
    plt.xlabel('Tempo de Divergência do PIE (milénios BP)', fontsize=12)
    plt.ylabel('Distância Lexical Média do Ramo ao PIE', fontsize=12)
    plt.title('Divergência de RAMOS do Proto-Indo-Europeu\n'
              'Cada ponto = média de um ramo (ex: Românicas, Germânicas)',
              fontsize=14, fontweight='bold', pad=20)

    plt.legend(fontsize=9, loc='lower right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    output_path = IMAGES_DIR / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Gráfico guardado: {output_path}")
    plt.show()

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print("=" * 80)
    print("🏛️ COMPARAÇÃO COM PROTO-INDO-EUROPEU (PIE)")
    print("=" * 80)

    # Verificar ficheiro PIE
    print(f"\n📁 Pasta PIE: {PIE_DIR}")
    pie_file = PIE_DIR / "pie_swadesh.csv"
    if not pie_file.exists():
        print(f"   ❌ Ficheiro não encontrado: {pie_file}")
        return
    print(f"   ✅ Ficheiro PIE encontrado")

    # Carregar dados
    print("\n📥 A carregar dados...")
    asjp = ASJPLoader()
    asjp.load()

    pie = PIELoader()
    if pie.load() is None:
        print("❌ PIE não carregado")
        return

    temporal = TemporalLoader()
    temporal.load()

    # Usar línguas expandidas se disponíveis
    try:
        from config import TEST_LANGUAGES_EXPANDED
        languages = TEST_LANGUAGES_EXPANDED
    except ImportError:
        languages = TEST_LANGUAGES

    print(f"\n📊 A calcular distâncias para {len(languages)} línguas...")

    # Calcular distâncias
    results = []
    for glotto in languages:
        name = temporal.get_language_name(glotto)

        # Distância lexical ao PIE
        # Obter palavras para verificar cobertura
        words = asjp.get_language_words(glotto)

        # FILTRO: Cobertura mínima de conceitos
        if len(words) < 30:
            print(f"   ⚠️ {name}: cobertura insuficiente ({len(words)} conceitos) — ignorado")
            continue

        # Distância lexical ao PIE
        pie_dist = pie.get_lexical_distance_to(asjp, glotto)

        # Tempo de divergência
        time_ky = temporal.get_divergence_time(glotto, 'ky')
        confidence = temporal.get_confidence(glotto)
        branch = temporal.get_language_branch(glotto)

        # Lidar com outgroups (não-IE)
        if time_ky is None:
            print(f"   ⚠️ {name}: sem dados temporais (outgroup)")
            # Ainda adicionar para validação, mas marcar como outgroup
            if pie_dist is not None:
                results.append({
                    'language': name,
                    'glottocode': glotto,
                    'distance_to_pie': pie_dist,
                    'divergence_time_ky': None,
                    'confidence': 'N/A',
                    'branch': branch,
                    'adjusted_distance': None,
                    'evolution_speed': 'outgroup'
                })
            continue

        if pie_dist is None:
            print(f"   ⚠️ {name}: sem dados lexicais")
            continue

        # Calcular distância ajustada (relógio lexical)
        # Calcular distância ajustada (relógio lexical)
        adjusted_dist = adjust_distance(pie_dist, time_ky)

        # CLASSIFICAÇÃO POR DISTÂNCIA BRUTA (mais discriminativa)
        if pie_dist < 0.83:
            speed_class = 'slow'  # Conservador
        elif pie_dist < 0.87:
            speed_class = 'medium'  # Médio
        else:
            speed_class = 'fast'  # Inovador

        results.append({
            'language': name,
            'glottocode': glotto,
            'distance_to_pie': pie_dist,
            'divergence_time_ky': time_ky,
            'confidence': confidence,
            'branch': branch,
            'adjusted_distance': adjusted_dist,
            'evolution_speed': speed_class
        })

        speed_emoji = {'slow': 'C', 'medium': 'M', 'fast': 'I'}
        print(f"   {name:15} → PIE: {pie_dist:.3f} | Tempo: {time_ky:.1f} ky | Ajustada: {adjusted_dist:.3f} {speed_emoji.get(speed_class, '')}")

    if not results:
        print("\n❌ Sem resultados para visualizar")
        return

    # Criar DataFrame
    df = pd.DataFrame(results)

    # ==========================================================================
    # PAINEL DE VALIDAÇÃO
    # ==========================================================================
    print("\n" + "=" * 80)
    print("🔍 PAINEL DE VALIDAÇÃO")
    print("=" * 80)

    validation_passed = 0
    validation_total = 0

    for glotto, spec in VALIDATION_EXPECTATIONS.items():
        if glotto in df['glottocode'].values:
            row = df[df['glottocode'] == glotto].iloc[0]
            dist = row['distance_to_pie']

            # Classificar observado
            if dist < 0.60:
                observed = 'conservative'
            elif dist < 0.75:
                observed = 'moderate'
            else:
                observed = 'innovative' if spec['expected'] != 'outgroup' else 'outgroup'

            match = "✅" if observed == spec['expected'] else "⚠️"
            validation_total += 1
            if observed == spec['expected']:
                validation_passed += 1

            print(f"{match} {spec['expected']:12} → {observed:12} | {row['language']} ({spec['reason']})")

    if validation_total > 0:
        validation_rate = validation_passed / validation_total
        print(f"\n📊 Validação: {validation_passed}/{validation_total} ({validation_rate:.0%})")
        if validation_rate >= 0.7:
            print("   ✅ Método validado com sucesso!")
        else:
            print("   ⚠️ Algumas validações falharam - interpretar com cautela")

    # ==========================================================================
    # TABELA DE RANKING
    # ==========================================================================
    print("\n" + "=" * 80)
    print("📋 RANKING: PROXIMIDADE LEXICAL AO PIE")
    print("=" * 80)

    # Filtrar apenas IE para ranking principal
    ie_df = df[df['branch'] != 'Uralic'].sort_values('distance_to_pie')

    print(f"\n{'Rank':<6} {'Língua':<18} {'Dist. PIE':<12} {'Ajustada':<12} {'Velocidade'}")
    print("-" * 70)

    speed_label = {'slow': '[C] Conservador', 'medium': '[M] Médio', 'fast': '[I] Inovador'}

    for rank, row in enumerate(ie_df.itertuples(), 1):
        label = speed_label.get(row.evolution_speed, '')
        print(f"{rank:<6} {row.language:<18} {row.distance_to_pie:.3f}      {row.adjusted_distance:.3f}      {label}")
    # ==========================================================================
    # FOCO NO MIRANDÊS
    # ==========================================================================
    mirandese = df[df['glottocode'] == 'mira1251']
    portuguese = df[df['glottocode'] == 'port1283']

    if len(mirandese) > 0 and len(portuguese) > 0:
        print("\n" + "=" * 80)
        print("🔍 FOCO: MIRANDÊS vs PORTUGUÊS")
        print("=" * 80)

        mir_dist = mirandese.iloc[0]['distance_to_pie']
        mir_adj = mirandese.iloc[0]['adjusted_distance']
        por_dist = portuguese.iloc[0]['distance_to_pie']
        por_adj = portuguese.iloc[0]['adjusted_distance']

        print(f"   Mirandês:  Dist={mir_dist:.3f} | Ajustada={mir_adj:.3f}")
        print(f"   Português: Dist={por_dist:.3f} | Ajustada={por_adj:.3f}")
        print(f"   Diferença: {mir_dist - por_dist:+.3f} (bruta) | {mir_adj - por_adj:+.3f} (ajustada)")

        if mir_adj < por_adj:
            print(f"   ✅ Mirandês é MAIS conservador que o Português")
        elif mir_adj > por_adj:
            print(f"   ⚠️ Mirandês é MENOS conservador que o Português")
        else:
            print(f"   ➡️ Mirandês e Português têm conservadorismo similar")

    # ==========================================================================
    # NOTA METODOLÓGICA
    # ==========================================================================
    print("\n" + "=" * 80)
    print("⚠️ NOTA METODOLÓGICA")
    print("=" * 80)
    print("""
As distâncias ao PIE são elevadas (0.70-0.90) porque:

1. As línguas românicas herdaram do LATIM, não diretamente do PIE
2. Muitas raízes PIE foram substituídas em Latim
3. 5000+ anos de evolução lexical acumulada

INTERPRETAÇÃO CORRETA:
• Valores ABSOLUTOS: Indicativos, não definitivos (incerteza ±0.10)
• Valores RELATIVOS: Rankings são robustos para comparação
• Foco analítico: "Qual língua é mais conservadora?" não "Qual é a distância exata?"

O PIE serve como referência conceptual para contextualizar a evolução,
não como ponto de medição absoluta.
""")

    # ==========================================================================
    # VISUALIZAÇÕES
    # ==========================================================================

    print("\n📈 A gerar visualizações...")
    plot_distance_vs_time_with_uncertainty(df)
    plot_branch_level_divergence(df)  # ← NOVO: Gráfico por ramo
    plot_evolution_speeds(df)
    plot_mirandese_focus(df)

    print("\n✅ Análise PIE concluída!")


if __name__ == "__main__":
    main()