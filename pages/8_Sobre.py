"""
Página 7: Sobre
Informação sobre o projeto, autoria e contexto

Autor: Alcides Santos | 250000693
Curso: Introdução à Inteligência Artificial (Artur Marques)
Instituto Politécnico de Santarém
Data: 2026
"""

import streamlit as st

st.set_page_config(
    page_title="Sobre",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("📝 Sobre Este Projeto")

# ============================================================================
# CONTEXTO ACADÉMICO
# ============================================================================

st.markdown("""
### 🎓 Contexto Académico

| Campo | Valor |
|-------|-------|
| **Curso** | Introdução à Inteligência Artificial |
| **Docente** | Artur Marques |
| **Autor** | Alcides Santos \| 250000693 |
| **Instituição** | Instituto Politécnico de Santarém |
| **Ano** | 2026 |
""")

# ============================================================================
# OBJETIVOS
# ============================================================================

st.markdown("""
### 🎯 Objetivos

1. Analisar evolução lexical das línguas românicas em relação ao Latim
2. Comparar Mirandês e Português sob duas métricas de distância
3. Implementar abordagem em 2 camadas: PIE → Latim → Românicas
4. Aplicar distância de edição ponderada por similaridade fonética (PanPhon)
5. Validar experimentalmente a métrica ponderada contra baseline
""")

# ============================================================================
# METODOLOGIA
# ============================================================================

st.markdown("""
### 🛠️ Metodologia

| Componente | Descrição |
|------------|-----------|
| **Dados** | ASJP Database (IPA Unicode), reconstruções PIE, formas latinas |
| **Métrica** | Levenshtein ponderado com matriz de similaridade fonética (21 features) |
| **Análise** | Deteção de outliers por Z-score (\|Z\| > 2.0) |
| **Interface** | Streamlit (web app local, 5 páginas interativas) |
| **Validação** | Comparação direta: métrica ponderada vs. Levenshtein simples |

**Nota metodológica:** As distâncias calculadas medem proximidade ao Latim 
(ancestral comum), não similaridade direta entre línguas românicas.
""")

# ============================================================================
# CONCLUSÃO PRINCIPAL (SEM NÚMEROS HARDCODED)
# ============================================================================

st.markdown("""
### 📊 Conclusão Principal

**O Mirandês é significativamente mais conservador que o Português** 
em relação ao Latim, validando hipóteses da linguística histórica.

> *A métrica ponderada por similaridade fonética amplifica esta diferença, 
> demonstrando maior poder discriminativo que a baseline (Levenshtein simples).*

**Para explorar os resultados completos:**  
Navega para a página 🏠 **Resultados** no menu lateral.
""")

# ============================================================================
# TECNOLOGIA
# ============================================================================

st.markdown("""
### 💻 Stack Tecnológico

| Categoria | Tecnologias |
|-----------|------------|
| **Linguagem** | Python 3.11 |
| **Interface** | Streamlit, Plotly (interativo) |
| **Dados** | Pandas, NumPy, SciPy |
| **Fonética** | PanPhon (21 features articulatórias) |
| **Versionamento** | Git + GitHub |

**Reprodutibilidade:**  
Código e dados disponíveis em:  
[github.com/alcidesantos/evolucao-lexical-romanticas](https://github.com/alcidesantos/evolucao-lexical-romanticas)
""")

# ============================================================================
# AGRADECIMENTOS (OPCIONAL)
# ============================================================================

st.divider()
st.markdown("""
### 🙏 Agradecimentos

- Ao Prof. Artur Marques pela orientação e flexibilidade metodológica
- À comunidade open-source pelas bibliotecas que tornaram este projeto possível
- Às ferramentas de IA (DeepSeek, Qwen) que aceleraram a pesquisa e desenvolvimento

> *"A excelência não é um ato, mas um hábito."* — Aristóteles
""")

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Projeto de Introdução à Inteligência Artificial** | 
Instituto Politécnico de Santarém | 2026

</div>
""", unsafe_allow_html=True)