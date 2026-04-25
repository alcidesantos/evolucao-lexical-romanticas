# 🏛️ Evolução Lexical das Línguas Românicas

> **Análise computacional de similaridade lexical com métricas fonéticas ponderadas**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io)

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

### Pré-requisitos
```bash
Python 3.11+
pip install -r requirements.txt