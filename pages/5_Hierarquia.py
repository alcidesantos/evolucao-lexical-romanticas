import streamlit as st
from pathlib import Path
from config import IMAGES_DIR

st.set_page_config(
    page_title="Hierarquia",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌳 Hierarquia PIE → Latim → Românicas")

st.markdown("""
**Comparação visual** das duas métricas de distância lexical.
Cada árvore mostra a evolução do PIE → Latim → Línguas Românicas,
com espessura das linhas proporcional à distância lexical.
""")

st.divider()

# ============================================================================
# CARREGAR AMBOS OS GRÁFICOS
# ============================================================================

weighted_path = IMAGES_DIR / "latin_hierarchy.png"
simple_path = IMAGES_DIR / "latin_hierarchy_simple.png"

# Verificar se existem ambos os ficheiros
if weighted_path.exists() and simple_path.exists():

    # Mostrar lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Métrica Ponderada")
        st.image(str(weighted_path), caption="Levenshtein Ponderado (Similaridade Fonética)")
        st.info("""
        **Características:**
        - Considera similaridade entre sons
        - Substituições fonéticas "naturais" têm custo reduzido
        - Melhor para estudos de evolução linguística
        """)

    with col2:
        st.subheader("🔵 Métrica Simples")
        st.image(str(simple_path), caption="Levenshtein Simples (Baseline)")
        st.info("""
        **Características:**
        - Todas as substituições custam igual
        - Baseline para comparação
        - Mais rápida, menos precisa foneticamente
        """)

    st.divider()

    # ============================================================================
    # COMPARAÇÃO DIRETA
    # ============================================================================

    st.subheader("🔍 Comparação Direta")

    st.markdown("""
    **O que observar:**

    1. **Espessura das linhas**: Linhas mais grossas = maior distância lexical
    2. **Cores dos nós**: Verde = conservador, Amarelo = médio, Vermelho = inovador
    3. **Diferenças entre métricas**: A ponderada tende a mostrar distâncias menores
       para línguas com mudanças fonéticas regulares

    **Padrão esperado:** Línguas conservadoras (Italiano, Sardo, Mirandês) devem ter 
    linhas mais finas na métrica ponderada, pois muitas mudanças são foneticamente 
    "naturais" (custo reduzido).
    """)

    # ============================================================================
    # NOTA METODOLÓGICA
    # ============================================================================

    with st.expander("📖 Nota Metodológica: Por Que Duas Métricas?"):
        st.markdown("""
        ### A Importância da Comparação

        A existência de **duas visualizações** permite:

        1. **Validação**: Se ambas mostram padrões similares, os resultados são robustos
        2. **Discriminação**: A ponderada separa melhor línguas no topo conservador
        3. **Interpretação**: Diferenças revelam quais mudanças são foneticamente "naturais"

        ### Como Funciona a Métrica Ponderada

        | Tipo de Mudança | Custo Simples | Custo Ponderado |
        |----------------|---------------|-----------------|
        | p → b (sonorização) | 1.0 | 0.3 (sons similares) |
        | a → i (vogal) | 1.0 | 0.6 (moderadamente diferentes) |
        | p → k (lugar diferente) | 1.0 | 0.8 (sons distintos) |
        | t → s (modo diferente) | 1.0 | 0.7 (moderadamente diferentes) |

        **Resultado:** Línguas com mudanças foneticamente regulares (Italiano, Mirandês) 
        têm distâncias **menores** na métrica ponderada, enquanto línguas com mudanças 
        mais "drásticas" ou empréstimos (Francês) mantêm distâncias elevadas em ambas.
        """)

else:
    # Um ou ambos os ficheiros não existem
    if not weighted_path.exists():
        st.error(
            "❌ Gráfico ponderado não encontrado. Executa `python compare_two_layer.py` com `USE_WEIGHTED_DISTANCE = True`.")

    if not simple_path.exists():
        st.error(
            "❌ Gráfico simples não encontrado. Executa `python compare_two_layer.py` com `USE_WEIGHTED_DISTANCE = False`.")

    st.warning("💡 **Solução:** Gera ambos os gráficos executando a análise duas vezes com métricas diferentes.")

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Visualização Hierárquica Comparativa** | 
Gráficos gerados por `compare_two_layer.py` | 
Streamlit App

</div>
""", unsafe_allow_html=True)