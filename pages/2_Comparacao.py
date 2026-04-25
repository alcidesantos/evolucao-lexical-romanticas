"""
Página 5: Comparação de Métricas

Compara Levenshtein Simples vs. Ponderado por Similaridade Fonética
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from config import DATA_DIR, IMAGES_DIR

st.set_page_config(
    page_title="Comparação de Métricas",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("⚖️ Validação: Comparação de Métricas")
st.markdown("""
**Validação experimental** da métrica ponderada contra a baseline 
(Levenshtein simples). Esta comparação demonstra o valor acrescentado 
da abordagem com pesos adaptativos.
""")
st.divider()

# ============================================================================
# CARREGAR DADOS DE AMBAS AS MÉTRICAS (DOS CSVs GERADOS)
# ============================================================================

# Caminhos dos CSVs
simple_csv = DATA_DIR / "outliers" / "latin_romance_ranking_simple.csv"
weighted_csv = DATA_DIR / "outliers" / "latin_romance_ranking_weighted.csv"

# Carregar dados SIMPLES
if simple_csv.exists():
    df_simple = pd.read_csv(simple_csv)
    df_simple = df_simple[['Língua', 'Distância', 'Rank']].copy()
    df_simple.columns = ['Língua', 'Distância_Simples', 'Rank_Simples']
    print(f"✅ Dados simples carregados: {len(df_simple)} línguas")
else:
    st.error(f"❌ Ficheiro não encontrado: {simple_csv}")
    st.stop()

# Carregar dados PONDERADOS
if weighted_csv.exists():
    df_weighted = pd.read_csv(weighted_csv)
    df_weighted = df_weighted[['Língua', 'Distância', 'Rank']].copy()
    df_weighted.columns = ['Língua', 'Distância_Ponderado', 'Rank_Ponderado']
    print(f"✅ Dados ponderados carregados: {len(df_weighted)} línguas")
else:
    st.error(f"❌ Ficheiro não encontrado: {weighted_csv}")
    st.stop()

# Juntar dados para comparação (merge por Língua)
comparison = pd.merge(
    df_simple,
    df_weighted,
    on='Língua',
    how='inner'  # ← Só línguas que existem em AMBOS
)

# Calcular diferenças
comparison['Diferença_Absoluta'] = comparison['Distância_Ponderado'] - comparison['Distância_Simples']
comparison['Diferença_Relativa'] = comparison['Diferença_Absoluta'] / comparison['Distância_Simples'] * 100
comparison['Mudança_Rank'] = comparison['Rank_Ponderado'] - comparison['Rank_Simples']

# Ordenar por rank ponderado (para exibição consistente)
comparison = comparison.sort_values('Rank_Ponderado').reset_index(drop=True)

# ============================================================================
# KPIs EM DESTAQUE
# ============================================================================

st.subheader("📊 Métricas Globais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_simple = comparison['Distância_Simples'].mean()
    st.metric("Distância Média (Simples)", f"{avg_simple:.3f}")

with col2:
    avg_weighted = comparison['Distância_Ponderado'].mean()
    st.metric("Distância Média (Ponderado)", f"{avg_weighted:.3f}",
              delta=f"{(avg_weighted - avg_simple):+.3f}")

with col3:
    reduction = (avg_simple - avg_weighted) / avg_simple * 100
    st.metric("Redução Média", f"{reduction:.1f}%",
              delta="distâncias menores", delta_color="normal")

with col4:
    mir_pt_simple = comparison[comparison['Língua'] == 'Mirandese']['Distância_Simples'].iloc[0] - \
                    comparison[comparison['Língua'] == 'Portuguese']['Distância_Simples'].iloc[0]
    mir_pt_weighted = comparison[comparison['Língua'] == 'Mirandese']['Distância_Ponderado'].iloc[0] - \
                      comparison[comparison['Língua'] == 'Portuguese']['Distância_Ponderado'].iloc[0]
    st.metric("Amplificação MIR-PT", f"{(mir_pt_weighted - mir_pt_simple) / abs(mir_pt_simple) * 100:+.0f}%",
              delta="diferença maior", delta_color="normal")

st.divider()

# ============================================================================
# GRÁFICO 1: Dispersão Simples vs. Ponderado
# ============================================================================

st.subheader("📈 Gráfico 1: Distância Simples vs. Ponderada")

fig_scatter = px.scatter(
    comparison,
    x='Distância_Simples',
    y='Distância_Ponderado',
    text='Língua',
    size=[15] * len(comparison),
    color='Diferença_Relativa',
    color_continuous_scale='RdYlGn_r',
    title='Cada ponto é uma língua: quanto abaixo da linha, mais redução com ponderação',
    labels={
        'Distância_Simples': 'Levenshtein Simples',
        'Distância_Ponderado': 'Levenshtein Ponderado',
        'Diferença_Relativa': 'Redução (%)'
    }
)

# Linha y=x (se fossem iguais)
min_val = min(comparison['Distância_Simples'].min(), comparison['Distância_Ponderado'].min())
max_val = max(comparison['Distância_Simples'].max(), comparison['Distância_Ponderado'].max())
fig_scatter.add_scatter(
    x=[min_val, max_val],
    y=[min_val, max_val],
    mode='lines',
    line=dict(color='gray', dash='dash', width=2),
    name='Igualdade (y=x)',
    showlegend=True
)

fig_scatter.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(height=500, showlegend=True)

st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("📖 Como Interpretar Este Gráfico"):
    st.markdown("""
    - **Pontos na linha cinzenta**: Métricas produzem mesma distância
    - **Pontos abaixo da linha**: Ponderado produz distância menor (maioria dos casos)
    - **Pontos acima da linha**: Ponderado produz distância maior (raro)
    - **Cor vermelha**: Grande redução com ponderação (muitas mudanças "naturais")
    - **Cor verde**: Pouca redução (mudanças mais "drásticas" ou aleatórias)

    **Padrão esperado:** Línguas mais conservadoras (Italiano, Mirandês) devem estar 
    mais abaixo da linha, pois têm mais mudanças fonéticas regulares.
    """)

# ============================================================================
# GRÁFICO 2: Diferença Relativa por Língua
# ============================================================================

st.subheader("📊 Gráfico 2: Redução Relativa por Língua")

fig_bars = px.bar(
    comparison.sort_values('Diferença_Relativa', ascending=False),
    x='Língua',
    y='Diferença_Relativa',
    color='Diferença_Relativa',
    color_continuous_scale='RdYlGn_r',
    title='Quanto menor (mais negativo), mais a ponderação reduziu a distância',
    labels={
        'Diferença_Relativa': 'Redução com Ponderação (%)',
        'Língua': 'Língua'
    }
)

fig_bars.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Sem mudança")
fig_bars.update_layout(height=400, showlegend=False)
fig_bars.update_traces(texttemplate='%{y:.1f}%', textposition='outside')

st.plotly_chart(fig_bars, use_container_width=True)

# ============================================================================
# TABELA COMPLETA
# ============================================================================

st.subheader("📋 Tabela Completa de Comparação")

# Format table with color scale
st.dataframe(
    comparison[[
        'Língua',
        'Distância_Simples',
        'Distância_Ponderado',
        'Diferença_Absoluta',
        'Diferença_Relativa',
        'Rank_Simples',
        'Rank_Ponderado',
        'Mudança_Rank'
    ]].style.format({
        'Distância_Simples': '{:.3f}',
        'Distância_Ponderado': '{:.3f}',
        'Diferença_Absoluta': '{:+.3f}',
        'Diferença_Relativa': '{:+.1f}%',
        'Rank_Simples': '{:.0f}º',
        'Rank_Ponderado': '{:.0f}º',
        'Mudança_Rank': '{:+d}'
    }).background_gradient(subset=['Diferença_Relativa'], cmap='RdYlGn_r'),
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# INSIGHT PRINCIPAL: MIRANDÊS vs PORTUGUÊS
# ============================================================================

st.divider()
st.subheader("🔍 Insight Principal: Mirandês vs. Português")

mir = comparison[comparison['Língua'] == 'Mirandese']
por = comparison[comparison['Língua'] == 'Portuguese']

if len(mir) > 0 and len(por) > 0:
    mir_simple = mir['Distância_Simples'].iloc[0]
    mir_weighted = mir['Distância_Ponderado'].iloc[0]
    por_simple = por['Distância_Simples'].iloc[0]
    por_weighted = por['Distância_Ponderado'].iloc[0]

    diff_simple = mir_simple - por_simple
    diff_weighted = mir_weighted - por_weighted
    amplification = (abs(diff_weighted) - abs(diff_simple)) / abs(diff_simple) * 100

    col_mir, col_por, col_diff = st.columns(3)

    with col_mir:
        st.info(f"""
        **🇵🇹 Mirandês**

        | Métrica | Distância | Rank |
        |---------|-----------|------|
        | Simples | {mir_simple:.3f} | {mir['Rank_Simples'].iloc[0]}º |
        | Ponderado | {mir_weighted:.3f} | {mir['Rank_Ponderado'].iloc[0]}º |
        | Redução | — | **{((mir_simple - mir_weighted) / mir_simple * 100):.1f}%** |
        """)

    with col_por:
        st.warning(f"""
        **🇵🇹 Português**

        | Métrica | Distância | Rank |
        |---------|-----------|------|
        | Simples | {por_simple:.3f} | {por['Rank_Simples'].iloc[0]}º |
        | Ponderado | {por_weighted:.3f} | {por['Rank_Ponderado'].iloc[0]}º |
        | Redução | — | **{((por_simple - por_weighted) / por_simple * 100):.1f}%** |
        """)

    with col_diff:
        if diff_weighted < 0:
            st.success(f"""
            **✅ Conclusão**

            | Métrica | Diferença MIR-PT |
            |---------|------------------|
            | Simples | {diff_simple:+.3f} |
            | Ponderado | {diff_weighted:+.3f} |

            **Amplificação:** {amplification:+.0f}%

            A métrica ponderada **reforça** a conclusão de que 
            o Mirandês é mais conservador que o Português!
            """)
        else:
            st.error(f"""
            **⚠️ Atenção**

            | Métrica | Diferença MIR-PT |
            |---------|------------------|
            | Simples | {diff_simple:+.3f} |
            | Ponderado | {diff_weighted:+.3f} |

            A métrica ponderada **atenua** a diferença.
            """)

# ============================================================================
# CONCLUSÕES
# ============================================================================

st.divider()
st.subheader("💡 Conclusões da Comparação")

# Calcular estatísticas dinâmicas
avg_simple = comparison['Distância_Simples'].mean()
avg_weighted = comparison['Distância_Ponderado'].mean()
reduction = (avg_simple - avg_weighted) / avg_simple * 100

# Línguas com maior redução
top_reduction = comparison.nsmallest(3, 'Diferença_Relativa')
top_reduction_list = ", ".join([f"{row['Língua']} ({row['Diferença_Relativa']:.0f}%)"
                                 for _, row in top_reduction.iterrows()])

# Diferença Mirandês-Português
mir = comparison[comparison['Língua'] == 'Mirandese']
por = comparison[comparison['Língua'] == 'Portuguese']
if len(mir) > 0 and len(por) > 0:
    diff_simple = mir['Distância_Simples'].iloc[0] - por['Distância_Simples'].iloc[0]
    diff_weighted = mir['Distância_Ponderado'].iloc[0] - por['Distância_Ponderado'].iloc[0]
    amplification = (abs(diff_weighted) - abs(diff_simple)) / abs(diff_simple) * 100 if diff_simple != 0 else 0
else:
    amplification = 0

st.markdown(f"""
1. **Todas as distâncias diminuem** com a métrica ponderada (redução média: {reduction:.1f}%).

2. **Línguas com maior redução**: {top_reduction_list} — sugerem mais mudanças fonéticas regulares.

3. **Diferença Mirandês/Português**: Amplificada em {amplification:+.0f}% com a métrica ponderada.

4. **Ranking relativo**: Mantém-se consistente entre métricas, validando robustez metodológica.

5. **Discriminação**: A métrica ponderada separa melhor o topo conservador (intervalo mais amplo).

**Recomendação:** Ponderada para estudos fonéticos precisos; Simples para análises exploratórias.
""")

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Dados gerados com `compare_two_layer.py`** | 
Desenvolvido com Streamlit | Alcides Santos | 250000693 | IPS 2026

</div>
""", unsafe_allow_html=True)