"""
Página 4: Ranking
Foco: Visualização limpa dos resultados + exportação

Autor: Alcides Santos | 250000693
Curso: Introdução à Inteligência Artificial (Artur Marques)
Instituto Politécnico de Santarém
Data: 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import load_results

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Ranking",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("📊 Ranking: Conservadorismo Lexical")
st.markdown("""
**Resultados da métrica ponderada** (PanPhon) — línguas românicas ordenadas 
por proximidade lexical ao Latim.

> **Nota:** Valores menores indicam maior conservadorismo (mais próximo do Latim).
""")
st.divider()

# ============================================================================
# CARREGAR DADOS
# ============================================================================

ranking_df, _ = load_results()

# ============================================================================
# SCATTER ÚNICO: Rank vs. Distância ao Latim
# ============================================================================

st.subheader("📈 Rank vs. Distância ao Latim")
st.caption("Tamanho da bolha = nº de conceitos analisados (mais = ranking mais robusto)")

fig_scatter = px.scatter(
    ranking_df,
    x='Rank',
    y='Distância',
    size='Conceitos',
    color='Classificação',
    text='Língua',
    color_discrete_map={
        '[C] Conservador': '#4CAF50',
        '[M] Médio': '#FFC107',
        '[I] Inovador': '#F44336'
    },
    title='Distribuição de Conservadorismo nas Línguas Românicas',
    labels={
        'Rank': 'Posição no Ranking',
        'Distância': 'Distância ao Latim',
        'Conceitos': 'Nº de Conceitos'
    }
)

fig_scatter.update_traces(
    textposition='top center',
    marker=dict(line=dict(width=1, color='DarkSlateGrey'))
)
fig_scatter.update_layout(height=450, showlegend=True)

st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================================
# INSIGHT: Conceitos vs. Confiabilidade
# ============================================================================

st.info("""
**🔍 Nota metodológica: Número de Conceitos**

Línguas com mais conceitos analisados (bolhas maiores) têm rankings mais robustos:

| Conceitos | Interpretação |
|-----------|--------------|
| ≥ 45 | ✅ Ranking altamente confiável |
| 40-44 | ⚠️ Ranking confiável, com margem de erro reduzida |
| < 40 | 🔸 Interpretar com cautela — dados limitados |

**Neste estudo:** Italiano, Mirandês e Português têm ~50 conceitos; 
outras línguas podem ter menos devido a dados missing na base ASJP.
""")

# ============================================================================
# TABELA COMPLETA + EXPORTAÇÃO
# ============================================================================

st.subheader("📋 Tabela Completa de Resultados")

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", format="%d"),
        "Distância": st.column_config.NumberColumn("Distância ao Latim", format="%.3f"),
        "Conceitos": st.column_config.NumberColumn("Conceitos", format="%d"),
        "Classificação": st.column_config.TextColumn("Classificação")
    }
)

# Botão de exportação
st.download_button(
    label="📥 Exportar Ranking (CSV)",
    data=ranking_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
    file_name="ranking_conservadorismo_lexical.csv",
    mime="text/csv",
    help="Descarrega a tabela completa em formato CSV para análise externa"
)

# ============================================================================
# RESUMO ESTATÍSTICO RÁPIDO
# ============================================================================

st.divider()
st.subheader("📊 Resumo Estatístico")

col1, col2, col3 = st.columns(3)

with col1:
    mais_conservadora = ranking_df.loc[ranking_df['Distância'].idxmin()]
    st.metric(
        "🥫 Mais Conservadora",
        mais_conservadora['Língua'],
        f"{mais_conservadora['Distância']:.3f}"
    )

with col2:
    mais_inovadora = ranking_df.loc[ranking_df['Distância'].idxmax()]
    st.metric(
        "🚀 Mais Inovadora",
        mais_inovadora['Língua'],
        f"{mais_inovadora['Distância']:.3f}"
    )

with col3:
    media = ranking_df['Distância'].mean()
    st.metric(
        "📈 Média do Grupo",
        f"{media:.3f}",
        f"{len(ranking_df)} línguas"
    )

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Métrica:** Levenshtein Ponderado por Similaridade Fonética (PanPhon) | 
**Dados:** ASJP Database + Glottolog 4.6 | 
**Autor:** Alcides Santos | 250000693 | IPS 2026

</div>
""", unsafe_allow_html=True)