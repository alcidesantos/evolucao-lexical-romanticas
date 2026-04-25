import streamlit as st

st.set_page_config(
    page_title="Sobre",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📝 Sobre Este Projeto")

st.markdown("""
### 🎓 Contexto Académico

- **Curso:** Introdução à Inteligência Artificial
- **Docente:** Artur Marques
- **Autor:** Alcides Santos | 250000693
- **Instituição:** Instituto Politécnico de Santarém
- **Ano:** 2026

### 🎯 Objetivos

1. Analisar evolução lexical das línguas românicas
2. Comparar Mirandês e Português
3. Implementar abordagem em 2 camadas (PIE→Latim→Românicas)
4. Aplicar distância de edição ponderada por similaridade fonética

### 🛠️ Metodologia

- **Dados:** ASJP Database, reconstruções PIE, dados latinos manuais
- **Métrica:** Levenshtein ponderado com matriz fonética
- **Análise:** Deteção de outliers por Z-score
- **Interface:** Streamlit (web app local)

### 📊 Resultados Principais

| Língua | Distância | Rank |
|--------|-----------|------|
| Italiano | 0.481 | 1º |
| **Mirandês** | **0.520** | **2º** |
| Português | 0.628 | 8º |
| Francês | 0.757 | 9º |

**Conclusão:** Mirandês é **significativamente mais conservador** que Português (-0.108, ~18% relativo)

### 💻 Tecnologia

- Python 3.11
- Streamlit (interface web)
- Plotly (visualizações interativas)
- Pandas, NumPy, SciPy (análise de dados)

""")
col1, col2, col3, col4 = st.columns(4)
