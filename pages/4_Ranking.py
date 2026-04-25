import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from config import DATA_DIR

st.set_page_config(
    page_title="Ranking",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Ranking: Resultados da Análise")
st.markdown("""
**Visualização dos resultados** obtidos com a métrica ponderada.
Estes dados demonstram a aplicação prática do sistema de similaridade.
""")
st.divider()

# ============================================================================
# CARREGAR DADOS (mesma função da app principal)
# ============================================================================

from modules.data_loader import load_results

ranking_df, _ = load_results()

# ============================================================================
# GRÁFICO PRINCIPAL: Distribuição de Distâncias
# ============================================================================

st.subheader("📈 Distribuição de Distâncias")

fig_scatter = px.scatter(
    ranking_df,
    x='Rank',
    y='Distância',
    size='Conceitos',
    color='Classificação',
    text='Língua',
    title='Distância vs. Rank (tamanho = nº conceitos)',
    color_discrete_map={
        '[C] Conservador': '#4CAF50',
        '[M] Médio': '#FFC107',
        '[I] Inovador': '#F44336'
    }
)

fig_scatter.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(height=450, showlegend=True)

st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================================
# TABELA COMPLETA
# ============================================================================

st.subheader("📋 Tabela Completa")
st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", format="%d"),
        "Distância": st.column_config.NumberColumn("Distância", format="%.3f"),
        "Conceitos": st.column_config.NumberColumn("Conceitos", format="%d")
    }
)

# ============================================================================
# NOVA SECÇÃO: Comparação Direta de Distribuições (Ambas as Métricas)
# ============================================================================

st.divider()
st.subheader("🔍 Comparação Direta: Métrica Ponderada vs. Simples")

st.markdown("""
**Visualização lado a lado** das duas métricas. 
Nota como a métrica ponderada (esquerda) produz distâncias geralmente menores, 
especialmente para línguas conservadoras.
""")

# Carregar dados de ambas as métricas
simple_csv = DATA_DIR / "outliers" / "latin_romance_ranking_simple.csv"
weighted_csv = DATA_DIR / "outliers" / "latin_romance_ranking_weighted.csv"

if simple_csv.exists() and weighted_csv.exists():
    # Carregar e preparar dados
    df_simple = pd.read_csv(simple_csv)[['Língua', 'Distância', 'Rank']].copy()
    df_simple.columns = ['Língua', 'Distância_Simples', 'Rank_Simples']

    df_weighted = pd.read_csv(weighted_csv)[['Língua', 'Distância', 'Rank']].copy()
    df_weighted.columns = ['Língua', 'Distância_Ponderado', 'Rank_Ponderado']

    # Juntar para comparação (merge por Língua)
    df_compare = pd.merge(df_simple, df_weighted, on='Língua', how='inner')

    # Ordenar por rank ponderado (para consistência visual)
    df_compare = df_compare.sort_values('Rank_Ponderado').reset_index(drop=True)

    # Mostrar gráficos lado a lado
    col1, col2 = st.columns(2)

    with col1:
        fig_weighted = px.bar(
            df_compare,
            x='Distância_Ponderado',
            y='Língua',
            orientation='h',
            color='Distância_Ponderado',
            color_continuous_scale='Greens',
            title='🟢 Métrica Ponderada',
            labels={'Distância_Ponderado': 'Distância', 'Língua': 'Língua'},
            range_x=[0, 1.0]  # Mesmo eixo X para comparação justa
        )
        fig_weighted.update_layout(showlegend=False, height=500, xaxis_title='Distância Lexical')
        st.plotly_chart(fig_weighted, use_container_width=True)

    with col2:
        fig_simple = px.bar(
            df_compare,
            x='Distância_Simples',
            y='Língua',
            orientation='h',
            color='Distância_Simples',
            color_continuous_scale='Blues',
            title='🔵 Métrica Simples',
            labels={'Distância_Simples': 'Distância', 'Língua': 'Língua'},
            range_x=[0, 1.0]  # Mesmo eixo X para comparação justa
        )
        fig_simple.update_layout(showlegend=False, height=500, xaxis_title='Distância Lexical')
        st.plotly_chart(fig_simple, use_container_width=True)

    # Insight automático
    st.info("""
    **🔍 O que observar:**

    - **Barras mais curtas à esquerda**: A métrica ponderada reduz distâncias 
      para mudanças foneticamente "naturais" (ex: p→b, t→d)

    - **Diferença maior no topo**: Línguas conservadoras (Italiano, Sardo, Mirandês) 
      beneficiam mais da ponderação — as suas mudanças são mais regulares

    - **Diferença menor na base**: Línguas inovadoras (Francês) mantêm distâncias 
      elevadas em ambas as métricas — mudanças mais "drásticas" ou empréstimos

    - **Ordenação similar**: O ranking relativo mantém-se, validando robustez metodológica

    **Conclusão:** A métrica ponderada não altera a ordem geral, mas **amplifica** 
    as diferenças entre línguas conservadoras e inovadoras — exatamente o que 
    queremos para estudos de evolução lexical!
    """)

    # Tabela de diferenças (opcional, mas útil)
    with st.expander("📊 Ver Tabela de Diferenças"):
        df_compare['Diferença'] = df_compare['Distância_Simples'] - df_compare['Distância_Ponderado']
        df_compare['Redução_%'] = df_compare['Diferença'] / df_compare['Distância_Simples'] * 100

        st.dataframe(
            df_compare[['Língua', 'Distância_Ponderado', 'Distância_Simples', 'Diferença', 'Redução_%']]
            .style.format({
                'Distância_Ponderado': '{:.3f}',
                'Distância_Simples': '{:.3f}',
                'Diferença': '{:+.3f}',
                'Redução_%': '{:+.1f}%'
            })
            .background_gradient(subset=['Redução_%'], cmap='RdYlGn_r'),
            use_container_width=True,
            hide_index=True
        )

        st.caption("Valores positivos em 'Diferença' = a métrica ponderada reduziu a distância")

else:
    st.warning("""
    ⚠️ **Dados de ambas as métricas necessários para comparação.**

    Para gerar os dados:
    1. Executa `python compare_two_layer.py` com `USE_WEIGHTED_DISTANCE = True`
    2. Depois executa com `USE_WEIGHTED_DISTANCE = False`
    3. Renomeia o CSV simples: `latin_romance_ranking_simple.csv`

    Ambos os ficheiros devem estar em `data/outliers/`.
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Ranking de Conservadorismo Lexical** | 
Dados: ASJP Database, Glottolog 4.6 | 
Métrica: Levenshtein Ponderado por Similaridade Fonética

</div>
""", unsafe_allow_html=True)