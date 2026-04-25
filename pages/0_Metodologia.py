"""
Página 0: Metodologia de Inteligência Artificial
Foco nas técnicas computacionais implementadas

Autor: Alcides
Curso: Introdução à Inteligência Artificial
IPS 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Metodologia IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("🤖 Metodologia de Inteligência Artificial")
st.markdown("""
### Sistema de Análise de Similaridade com Pesos Adaptativos

Este projeto implementa **técnicas computacionais avançadas** para análise 
de similaridade entre sequências de dados, com aplicação a múltiplos domínios.

**Caso de Estudo:** Evolução Lexical das Línguas Românicas  
**Técnicas:** Métricas de distância ponderada, matriz de similaridade, deteção de outliers  
**Framework:** Python + Streamlit + Plotly
""")

st.divider()

# ============================================================================
# PROBLEMA & SOLUÇÃO
# ============================================================================

st.subheader("🎯 Problema & Solução")

col1, col2 = st.columns(2)

with col1:
    st.error("""
    **PROBLEMA**

    As métricas de distância tradicionais (ex: Levenshtein) tratam 
    **todas as diferenças como igualmente significativas**.

    **Limitação:**
    - Substituição `k → ʃ` (palatalização comum) = custo 1.0
    - Substituição `p → z` (sem relação) = custo 1.0

    ❌ Ignora relações estruturais entre elementos
    """)

with col2:
    st.success("""
    **SOLUÇÃO**

    Implementámos uma **métrica ponderada** com matriz de similaridade.

    **Inovação:**
    - Substituição `k → ʃ` → custo 0.50 (similaridade 0.50)
    - Substituição `p → z` → custo 1.00 (similaridade 0.00)

    ✅ Captura padrões estruturais do domínio
    """)

st.divider()

# ============================================================================
# ARQUITETURA DO SISTEMA
# ============================================================================

st.subheader("🏗️ Arquitetura do Sistema")

st.markdown("""
### 📊 Fluxograma do Pipeline de Processamento

Este diagrama ilustra o fluxo completo de dados, desde o carregamento 
dos corpora até à visualização interativa na aplicação Streamlit.
""")

# Mostrar fluxograma
from config import IMAGES_DIR
from pathlib import Path

flowchart_path = IMAGES_DIR / "architecture_flowchart.png"

if flowchart_path.exists():
    st.image(
        str(flowchart_path),
        caption="Figura 1: Arquitetura do Sistema - Fluxo de Processamento de Dados",
        use_container_width=True
    )

    st.info("""
    **Legenda do Fluxograma:**

    1. **CONFIG.PY** → Define a métrica (USE_WEIGHTED_DISTANCE = True/False)
    2. **CARREGAR CORPORA** → ASJP (15 línguas), Latim (formas reconstruídas), PIE (referência)
    3. **CALCULAR DISTÂNCIAS** → Algoritmo condicionado pela flag (Ponderada vs. Simples)
    4. **DETEÇÃO DE OUTLIERS** → Critério |Z| > 2.0 identifica padrões anómalos
    5. **EXPORTAR RESULTADOS** → CSVs estruturados + visualizações PNG
    6. **APP STREAMLIT** → 5 painéis interativos para exploração dos resultados
    """)
else:
    st.warning("""
    ⚠️ **Fluxograma não encontrado.**

    **Para gerar o fluxograma:**
    1. Guarda a imagem em anexo como `architecture_flowchart.png`
    2. Coloca na pasta `images/`
    3. Recarrega esta página

    **Ou usa a versão textual abaixo:**
    """)

    # Fallback: versão textual simplificada
    st.markdown("""
    ###  Fluxo de Processamento (Versão Textual)

    ```
    CONFIG.PY (USE_WEIGHTED_DISTANCE=True)
              │
              ▼
    1. CARREGAR CORPORA
       • ASJP (15 línguas, ~50 conceitos)
       • Latim (formas reconstruídas)
       • PIE (distância referência)
              │
              ▼
    2. CALCULAR DISTÂNCIAS (Latim → Românica)
       Algoritmo condicionado pela flag
              │
         ┌────┴────┐
         ▼         ▼
    PONDERADA   SIMPLES
    (PanPhon)    (Levenshtein)
         │         │
         └────┬────┘
              ▼
    3. DETEÇÃO DE OUTLIERS
       Critério |Z| > 2.0
              │
              ▼
    4. EXPORTAR RESULTADOS (CSV + PNG)
       • RANKING_WEIGHTED.CSV
       • RANKING_SIMPLE.CSV
       • OUTLIERS.CSV
       • IMAGES/*.PNG (3 visualizações)
              │
              ▼
    5. APP STREAMLIT (5 painéis interativos)
    ```
    """)

st.divider()

# ============================================================================
# MATRIZ DE PESOS (EXEMPLOS CONCRETOS)
# ============================================================================

st.subheader("⚖️ Matriz de Similaridade (Sistema de Pesos)")

st.markdown("""
A **inovação principal** deste projeto é a matriz de similaridade, que atribui 
pesos diferenciados com base em características estruturais dos elementos.

**Exemplos de Pares Ponderados:**
""")

pesos_df = pd.DataFrame({
    'Par de Elementos': ['k → ʃ', 'l → ʎ', 'p → b', 'e → ɛ', 'a → ã', 'n → ɲ', 'p → z'],
    'Similaridade': [0.50, 0.75, 0.85, 0.85, 0.70, 0.75, 0.00],
    'Custo de Substituição': [0.50, 0.25, 0.15, 0.15, 0.30, 0.25, 1.00],
    'Tipo de Relação': [
        'Palatalização comum',
        'Palatalização lateral',
        'Mesmo ponto, voicing diferente',
        'Abertura vocálica próxima',
        'Nasalização',
        'Palatalização nasal',
        'Sem relação estrutural'
    ],
    'Redução vs. Baseline': [
        '-50%', '-75%', '-85%', '-85%', '-70%', '-75%', '0%'
    ]
})

st.dataframe(
    pesos_df.style.format({'Similaridade': '{:.2f}', 'Custo de Substituição': '{:.2f}'})
    .background_gradient(subset=['Similaridade'], cmap='RdYlGn')
    .background_gradient(subset=['Custo de Substituição'], cmap='RdYlGn_r'),
    use_container_width=True,
    hide_index=True
)

st.success("""
**Valor de IA:** 
Esta abordagem permite que o sistema "compreenda" que certas transformações 
são mais "naturais" que outras, capturando **padrões estruturais** do domínio 
em vez de tratar todas as mudanças como igualmente prováveis.

**Generalização:** A mesma abordagem pode ser aplicada a:
- Biologia (similaridade entre aminoácidos)
- Processamento de texto (caracteres visualmente similares: o-0, l-1)
- Bioinformática (bases complementares de DNA: A-T, G-C)
""")

st.divider()

# ============================================================================
# VALIDAÇÃO EXPERIMENTAL
# ============================================================================

st.subheader("📊 Validação Experimental: Comparação de Métricas")

st.markdown("""
Para validar a contribuição da métrica ponderada, comparamos os resultados 
com a **baseline** (Levenshtein simples).
""")

col_val1, col_val2 = st.columns(2)

with col_val1:
    st.metric("Redução Média da Distância", "-17.4%",
              delta="Distâncias menores = mais realistas")

    st.metric("Amplificação da Diferença MIR-PT", "+108%",
              delta="Maior poder discriminativo")

with col_val2:
    st.metric("Línguas Analisadas", "9",
              delta="Românicas principais")

    st.metric("Outliers Detetados", "11",
              delta="Possíveis empréstimos")

st.markdown("""
**Tabela Comparativa:**
""")

comparacao = pd.DataFrame({
    'Métrica': ['Simples (Baseline)', 'Ponderado (Inovação)'],
    'Distância Média': [0.707, 0.584],
    'Redução': ['—', '-17.4%'],
    'Diferença Mirandês-Português': ['-0.052', '-0.108'],
    'Amplificação': ['—', '+108%'],
    'Ranking Mais Conservador': ['Italiano (0.634)', 'Italiano (0.481)'],
    'Ranking Mais Inovador': ['Francês (0.847)', 'Francês (0.757)']
})

st.dataframe(comparacao, use_container_width=True, hide_index=True)

st.info("""
**Conclusão da Validação:**

✅ A métrica ponderada produz distâncias **menores e mais realistas**  
✅ **Amplifica** a diferença entre casos conservadores e inovadores  
✅ Demonstra **maior poder discriminativo** que a baseline  
✅ Mantém o **ranking relativo** (validação de consistência)
""")

st.divider()

# ============================================================================
# APLICABILIDADE A OUTROS DOMÍNIOS
# ============================================================================

st.subheader("🌍 Aplicabilidade a Outros Domínios")

st.markdown("""
Este sistema é **genérico** e pode ser aplicado a qualquer domínio com 
dados sequenciais. Basta substituir a matriz de similaridade.

**Exemplos de Aplicação:**
""")

dominios = pd.DataFrame({
    'Domínio': ['Linguística', 'Biologia Molecular', 'Processamento de Texto',
                'Bioinformática', 'Análise de Código', 'Reconhecimento de Padrões'],
    'Tipo de Sequência': ['Palavras (ASJPcode)', 'Sequências de DNA',
                          'Strings de texto', 'Sequências de proteínas',
                          'Código-fonte', 'Imagens vetorizadas'],
    'Exemplo de Similaridade': ['k-ʃ (palatalização)', 'A-T (complementar)',
                                'o-0 (visual)', 'Leu-Ile (hidrofóbicos)',
                                'if-elif (semântico)', 'bordas similares'],
    'Custo Típico': ['0.50', '0.20', '0.30', '0.40', '0.60', '0.50']
})

st.dataframe(dominios, use_container_width=True, hide_index=True)

st.success("""
**Adaptação:** 
Para aplicar a outro domínio, apenas é necessário:
1. Definir a matriz de similaridade apropriada
2. Ajustar o pré-processamento dos dados
3. Manter o core do algoritmo (já implementado)

**Tempo estimado de adaptação:** 2-4 horas
""")

st.divider()

# ============================================================================
# TECNOLOGIAS UTILIZADAS
# ============================================================================

st.subheader("💻 Stack Tecnológico")

col_tech1, col_tech2, col_tech3 = st.columns(3)

with col_tech1:
    st.markdown("""
    **Linguagem**
    - Python 3.11
    - Tipagem dinâmica
    - Programação funcional
    """)

with col_tech2:
    st.markdown("""
    **Bibliotecas IA/Dados**
    - NumPy (cálculo numérico)
    - Pandas (manipulação de dados)
    - SciPy (estatística)
    """)

with col_tech3:
    st.markdown("""
    **Visualização/Web**
    - Streamlit (interface web)
    - Plotly (gráficos interativos)
    - Matplotlib (gráficos estáticos)
    """)

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Sistema de Similaridade com Pesos Adaptativos** | 
Desenvolvido com Streamlit | Alcides Santos | 250000693 | IPS 2026

</div>
""", unsafe_allow_html=True)