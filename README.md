# Pipeline de Distância Linguística Multi-Dimensional

## Instalação

```bash
pip install -r requirements.txt

## 🎯 Objetivo

Este projeto aplica **Inteligência Artificial Simbólica** à análise da evolução lexical 
das línguas românicas, comparando duas métricas de distância:

- **Baseline**: Levenshtein simples (todas as substituições = custo 1.0)
- **Inovação**: Levenshtein ponderado por similaridade fonética (PanPhon, 21 features articulatórias)

## 📊 Resultados Principais

- ✅ 15 línguas românicas analisadas (~50 conceitos ASJP)
- ✅ Métrica ponderada reduz distâncias em ~17% vs. baseline
- ✅ Amplificação da diferença Mirandês-Português: -0.052 → -0.108 (+108%)
- ✅ Interface interativa Streamlit para exploração de resultados

## 🚀 Como Executar

- Pré-requisitos
`pip install -r requirements.txt`

- Executar análise
`python compare_two_layer.py`

- Iniciar aplicação web
`streamlit run pages/0_Metodologia.py`

- ou usar o script de arranque:
`python iniciar_app.py`

## 🔬 Metodologia
#### Carregamento de dados: ASJP Database (IPA Unicode), reconstruções latinas
#### Cálculo de distâncias:
- Simples: Levenshtein normalizado
- Ponderado: PanPhon weighted_feature_edit_distance (21 features)
#### Análise estatística: Z-score para deteção de outliers (|Z| > 2.0)
#### Validação experimental: Comparação direta das duas métricas
#### Visualização: Streamlit + Plotly para exploração interativa

## 📚 Referências
- ASJP Database: https://asjp.clld.org/
- PanPhon: Mortensen et al. (2016) - https://github.com/mortense/panphon
- Glottolog: https://glottolog.org/

## 👤 Autor
- Alcides Santos
- Instituto Politécnico de Santarém | 2026
- Introdução à Inteligência Artificial (Prof. Artur Marques)

## 📄 Licença
MIT License



