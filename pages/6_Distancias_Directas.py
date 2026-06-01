"""
Página 5: Distâncias Diretas Entre Línguas

Compara similaridade lexical direta entre línguas românicas,
sem passar pelo Latim como intermediário.

Autor: Alcides Santos | 250000693
Curso: Introdução à Inteligência Artificial (Artur Marques)
Instituto Politécnico de Santarém
Data: 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from config import DATA_DIR, TEST_LANGUAGES_NAMED

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Distâncias Diretas",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("🔗 Distâncias Diretas Entre Línguas Românicas")
st.markdown("""
**Comparação de similaridade lexical direta** entre pares de línguas românicas,
sem passar pelo Latim como ponto de referência.

> **Nota metodológica:** Esta secção mede **similaridade mútua** entre línguas,
> não conservadorismo em relação ao Latim. Duas línguas podem ser lexicalmente
> próximas por empréstimos, contacto histórico ou evolução convergente.
""")

st.divider()

# ============================================================================
# CARREGAR MATRIZES PRÉ-CALCULADAS
# ============================================================================

@st.cache_data(ttl=3600)
def load_distance_matrices():
    """Carrega matrizes de distâncias pré-calculadas"""
    simple_csv = DATA_DIR / "outliers" / "direct_distances_simple.csv"
    weighted_csv = DATA_DIR / "outliers" / "direct_distances_weighted.csv"

    if simple_csv.exists() and weighted_csv.exists():
        matrix_simple = pd.read_csv(simple_csv, index_col=0)
        matrix_weighted = pd.read_csv(weighted_csv, index_col=0)
        return matrix_simple, matrix_weighted
    else:
        return None, None

matrix_simple, matrix_weighted = load_distance_matrices()

# Verificar se os dados existem
if matrix_simple is None or matrix_weighted is None:
    st.error("""
    ❌ **Matrizes de distâncias não encontradas.**
    
    **Para gerar os dados:**
    ```bash
    python scripts/precompute_distances.py
    ```
    
    Este script pré-calcula todas as distâncias diretas entre línguas românicas
    e guarda em CSVs que a app carrega instantaneamente.
    """)
    st.stop()

linguas = list(matrix_simple.index)
st.caption(f"*{len(linguas)} línguas carregadas (dados pré-calculados)*")

# ============================================================================
# SIDEBAR: CONTROLOS
# ============================================================================

st.sidebar.header("⚙️ Configurações")

# Seletor de métrica
metrica = st.sidebar.radio(
    "Métrica de distância:",
    ["🟢 Ponderada (Fonética)", "🔵 Simples (Baseline)"],
    index=0
)
metric_type = 'weighted' if 'Ponderada' in metrica else 'simple'

# Selecionar matriz conforme métrica
distance_matrix = matrix_weighted if metric_type == 'weighted' else matrix_simple

# Seletor para comparador de pares
st.sidebar.header("🔍 Comparador de Pares")
lang1 = st.sidebar.selectbox("Língua 1:", linguas, index=linguas.index('Portuguese') if 'Portuguese' in linguas else 0)
lang2 = st.sidebar.selectbox("Língua 2:", [l for l in linguas if l != lang1], index=0)

# Seletor para Top-N
st.sidebar.header("🏆 Top-N Mais Próximas")
lang_reference = st.sidebar.selectbox("Referência:", linguas, index=linguas.index('Mirandese') if 'Mirandese' in linguas else 0)
top_n = st.sidebar.slider("N:", 1, len(linguas)-1, 3)

# ============================================================================
# HEATMAP: MATRIZ DE DISTÂNCIAS
# ============================================================================

st.subheader("🗺️ Heatmap de Distâncias Diretas")
st.caption(f"*Métrica: {metric_type}*")

# Plotar heatmap
fig_heatmap = px.imshow(
    distance_matrix,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdYlGn_r',  # ✅ Verde = próximo, Vermelho = distante
    labels={'x': 'Língua', 'y': 'Língua', 'color': 'Distância'},
    title='Similaridade Lexical Direta Entre Línguas Românicas'
)
fig_heatmap.update_layout(height=600, font=dict(size=10))
st.plotly_chart(fig_heatmap, use_container_width=True)

with st.expander("📖 Como Interpretar o Heatmap"):
    st.markdown("""
    - **🟢 Cores verdes**: Línguas lexicalmente próximas (distância baixa)
    - **🟡 Cores amarelas**: Similaridade moderada (distância intermédia)
    - **🔴 Cores vermelhas**: Línguas lexicalmente distintas (distância alta)
    - **Diagonal = 0**: Cada língua é idêntica a si própria
    - **Matriz simétrica**: Distância(A,B) = Distância(B,A)

    **Como explorar:**
    1. Usar o **Comparador de Pares** na sidebar para verificar distâncias específicas
    2. Usar **Top-N Mais Próximas** para identificar as línguas mais similares a uma referência
    3. Passar o cursor sobre o heatmap para ver valores com maior exactidão

    **Atenção:** Similaridade lexical não implica parentesco direto — 
    pode resultar de empréstimos, contacto histórico ou evolução convergente.
    """)

# ============================================================================
# COMPARADOR DE PARES
# ============================================================================

st.divider()
st.subheader(f"🔍 Comparação Direta: {lang1} ↔ {lang2}")

# Obter distâncias de ambas as métricas
d_simple = matrix_simple.loc[lang1, lang2]
d_weighted = matrix_weighted.loc[lang1, lang2]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Distância (Simples)", f"{d_simple:.3f}")

with col2:
    st.metric("Distância (Ponderada)", f"{d_weighted:.3f}",
              delta=f"{(d_simple - d_weighted):+.3f}")

with col3:
    reduction = (d_simple - d_weighted) / d_simple * 100
    st.metric("Redução com Ponderação", f"{reduction:.1f}%")

# Explicação contextual
if d_weighted < 0.15:
    st.success(f"✅ **{lang1} e {lang2} são lexicalmente muito próximas** (distância < 0.15)")
elif d_weighted < 0.25:
    st.info(f"🟡 **{lang1} e {lang2} têm similaridade moderada** (0.15 ≤ distância < 0.25)")
else:
    st.warning(f"🔴 **{lang1} e {lang2} são lexicalmente distintas** (distância ≥ 0.25)")

# ============================================================================
# TOP-N MAIS PRÓXIMAS
# ============================================================================

st.divider()
st.subheader(f"🏆 Top {top_n} Línguas Mais Próximas de: {lang_reference}")

# Obter linha da matriz para a língua de referência
ref_row = distance_matrix.loc[lang_reference].drop(lang_reference).sort_values()
top_closest = ref_row.head(top_n)

# Mostrar como tabela
top_df = pd.DataFrame({
    'Língua': top_closest.index.tolist(),
    'Distância Direta': top_closest.values,
    'Interpretação': ['🟢 Muito Próxima' if d < 0.15 else '🟡 Próxima' if d < 0.25 else '🟠 Moderadamente Distante'
                      for d in top_closest.values]
})

st.dataframe(
    top_df.style.format({'Distância Direta': '{:.3f}'})
    .background_gradient(subset=['Distância Direta'], cmap='YlGn_r'),
    use_container_width=True,
    hide_index=True
)

# Gráfico de barras
fig_top = px.bar(
    top_df,
    x='Distância Direta',
    y='Língua',
    orientation='h',
    color='Interpretação',
    color_discrete_map={'🟢 Muito Próxima': '#4CAF50', '🟡 Próxima': '#FFC107', '🟠 Moderadamente Distante': '#FF9800'},
    text='Distância Direta',
    title=f'Línguas Lexicalmente Mais Próximas de {lang_reference}',
    labels={'Distância Direta': 'Distância', 'Língua': 'Língua'}
)
fig_top.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig_top.update_layout(height=300, showlegend=True)
st.plotly_chart(fig_top, use_container_width=True)

# ============================================================================
# NOTA METODOLÓGICA FINAL
# ============================================================================

st.divider()
st.info("""
### 📚 Nota Metodológica: Similaridade Direta vs. Conservadorismo

Esta página mede **similaridade lexical direta** entre línguas românicas.
É importante distinguir:

| Conceito | Medido em | Interpretação |
|----------|-----------|---------------|
| **Conservadorismo** | Páginas Ranking, Resultados | Proximidade ao Latim (ancestral comum) |
| **Similaridade Direta** | Esta página | Proximidade mútua entre línguas atuais |

**Por que os resultados podem diferir?**
- Duas línguas podem ser **ambas conservadoras** (próximas do Latim) mas **diferentes entre si** 
  (ex: Italiano e Sardo evoluíram em direções distintas)
- Duas línguas podem ser **ambas inovadoras** (distantes do Latim) mas **similares entre si** 
  (ex: Francês e Occitano partilham inovações gallo-românicas)
- Empréstimos linguísticos podem criar similaridade **sem parentesco direto**

**Valor desta análise:** Complementa o estudo de evolução diacrónica com uma 
perspetiva sincrónica de relações lexicais atuais.
""")

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Distâncias Diretas entre Línguas Românicas** | 
Dados: ASJP Database (IPA Unicode) | 
Métricas: Levenshtein Simples e Ponderado (PanPhon) | 
**Pré-calculado para performance**

</div>
""", unsafe_allow_html=True)