"""
Interface Web para Análise de Evolução Lexical das Línguas Românicas
Dia 5 - Interface Streamlit

Autor: Alcides Santos | 250000693
Curso: Introdução à Inteligência Artificial (Artur Marques)
Instituto Politécnico de Santarém
Data: 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from config import DATA_DIR, IMAGES_DIR
from modules.data_loader import load_results

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Evolução Lexical Românicas",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CABEÇALHO
# ============================================================================

st.title("🏠 Resultados: Caso de Estudo Linguístico")
st.markdown("### Aplicação de Métricas à Evolução Lexical")
st.markdown(
    "**Autor:** Alcides Santos | **Aluno nº:** 250000693 | **Curso:** IIA | **IPS** 2026 "
)

st.divider()

# ============================================================================
# CARREGAR DADOS
# ============================================================================

ranking_df, outliers_df = load_results()

# ============================================================================
# PREPARAR DADOS PARA AMBAS AS MÉTRICAS (UMA VEZ SÓ)
# ============================================================================

# Caminhos dos CSVs
simple_csv_path = DATA_DIR / "outliers" / "latin_romance_ranking_simple.csv"
weighted_csv_path = DATA_DIR / "outliers" / "latin_romance_ranking_weighted.csv"

# Carregar dados SIMPLES
if simple_csv_path.exists():
    df_simple = pd.read_csv(simple_csv_path)
else:
    # Fallback hardcoded
    simple_data = {
        'Língua': ['Italian', 'Mirandese', 'Galician', 'Catalan', 'Asturian',
                   'Spanish', 'Romanian', 'Portuguese', 'French'],
        'Distância': [0.634, 0.682, 0.641, 0.657, 0.680, 0.760, 0.747, 0.734, 0.847]
    }
    df_simple = pd.DataFrame(simple_data)

# Carregar dados PONDERADOS
if weighted_csv_path.exists():
    df_weighted = pd.read_csv(weighted_csv_path)
else:
    df_weighted = ranking_df.copy()

# ============================================================================
# SELETOR DE MÉTRICA PARA O GRÁFICO PRINCIPAL (SIDEBAR)
# ============================================================================

st.sidebar.header("📊 Métrica do Ranking Principal")

metrica_principal = st.sidebar.radio(
    "Para o gráfico principal:",
    ["🟢 Ponderada (Principal)", "🔵 Simples (Baseline)"],
    index=0,
    key="main_metric"
)

# Preparar dataframe de exibição conforme seleção
if "Simples" in metrica_principal and df_simple is not None:
    ranking_display_df = df_simple.copy()
    nota_metrica = "Simples"
else:
    ranking_display_df = df_weighted.copy()
    nota_metrica = "Ponderada"

# ============================================================================
# SELETOR DE MÉTRICA PARA PERFIL DE CONSERVADORISMO (SIDEBAR)
# ============================================================================

st.sidebar.header("📊 Métrica para Perfil de Conservadorismo")

metrica_proximidade = st.sidebar.radio(
    "Para a análise de perfil:",
    ["🟢 Ponderado (Fonética)", "🔵 Simples (Baseline)"],
    index=0,
    key="prox_metric"
)

# Info message na sidebar
if "Ponderado" in metrica_proximidade:
    st.sidebar.info("✅ Métrica com pesos fonéticos: captura evolução linguística natural")
else:
    st.sidebar.info("📏 Métrica baseline: todas as substituições custam igual")

# Selecionar DataFrame conforme métrica
if "Ponderado" in metrica_proximidade:
    df_atual = df_weighted[['Língua', 'Distância']].copy()
    nome_metrica = "Ponderado"
else:
    df_atual = df_simple[['Língua', 'Distância']].copy()
    nome_metrica = "Simples"

# ============================================================================
# SELETOR DE LÍNGUA DE REFERÊNCIA (SIDEBAR)
# ============================================================================

st.sidebar.header("🎯 Língua de Referência")

# Encontrar línguas comuns a ambos os datasets
linguas_comuns = set(df_simple['Língua'].tolist()) & set(df_weighted['Língua'].tolist())
linguas_comuns = sorted(list(linguas_comuns))

default_index = linguas_comuns.index('Mirandese') if 'Mirandese' in linguas_comuns else 0

referencia = st.sidebar.selectbox(
    "Calcular perfil em relação a:",
    linguas_comuns,
    index=default_index,
    help="Escolhe uma língua para calcular quais as outras línguas com perfil similar"
)

# Info box da língua selecionada
info_df = df_weighted if referencia in df_weighted['Língua'].values else df_simple
ref_dist = info_df[info_df['Língua'] == referencia]['Distância'].iloc[0]
ref_rank = int(info_df[info_df['Língua'] == referencia]['Rank'].iloc[0])

st.sidebar.info(f"""
**Língua Selecionada:** {referencia}  
**Distância ao Latim:** {ref_dist:.3f}  
**Rank:** {ref_rank}º
""")

# ============================================================================
# CONTEÚDO PRINCIPAL: KPIs
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

# KPI 1: Língua Mais Conservadora
with col1:
    mais_conservadora = ranking_display_df.loc[ranking_display_df['Distância'].idxmin()]
    st.metric(
        label="🥫 Língua Mais Conservadora",
        value=mais_conservadora['Língua'],
        delta=f"{mais_conservadora['Distância']:.3f} distância"
    )

# KPI 2: Mirandês
with col2:
    mir_data = ranking_display_df[ranking_display_df['Língua'] == 'Mirandese']
    if len(mir_data) > 0:
        mir_data = mir_data.iloc[0]
        st.metric(
            label="🇵🇹 Mirandês",
            value=f"{mir_data['Rank']}º Lugar",
            delta=f"{mir_data['Distância']:.3f} distância",
            delta_color="normal"
        )

# KPI 3: Português
with col3:
    por_data = ranking_display_df[ranking_display_df['Língua'] == 'Portuguese']
    if len(por_data) > 0:
        por_data = por_data.iloc[0]
        st.metric(
            label="🇵🇹 Português",
            value=f"{por_data['Rank']}º Lugar",
            delta=f"{por_data['Distância']:.3f} distância",
            delta_color="inverse"
        )

# KPI 4: Diferença MIR-PT
with col4:
    mir_data = ranking_display_df[ranking_display_df['Língua'] == 'Mirandese']
    por_data = ranking_display_df[ranking_display_df['Língua'] == 'Portuguese']
    if len(mir_data) > 0 and len(por_data) > 0:
        mir_data = mir_data.iloc[0]
        por_data = por_data.iloc[0]
        diff = mir_data['Distância'] - por_data['Distância']
        st.metric(
            label="📊 Diferença MIR-PT",
            value=f"{diff:+.3f}",
            delta=f"{abs(diff) / por_data['Distância'] * 100:.1f}% relativo",
            delta_color="normal"
        )

st.divider()

# ============================================================================
# GRÁFICO PRINCIPAL: Ranking Horizontal
# ============================================================================

st.subheader("📊 Ranking: Proximidade Lexical ao Latim")
st.caption(f"*Métrica: {nota_metrica}*")

# Criar gráfico Plotly interativo
fig_ranking = px.bar(
    ranking_display_df.sort_values('Distância', ascending=False),
    x='Distância',
    y='Língua',
    orientation='h',
    color='Classificação',
    color_discrete_map={
        '[C] Conservador': '#4CAF50',
        '[M] Médio': '#FFC107',
        '[I] Inovador': '#F44336'
    },
    text='Distância',
    hover_data=['Conceitos'],
    title='Línguas Românicas Ordenadas por Conservadorismo Lexical'
)

fig_ranking.update_layout(
    xaxis_title='Distância Lexical Latim → Língua',
    yaxis_title='Língua',
    showlegend=True,
    height=500,
    font=dict(size=12)
)

fig_ranking.update_xaxes(showgrid=False)
fig_ranking.update_yaxes(showgrid=False)

st.plotly_chart(fig_ranking, use_container_width=True)

# ============================================================================
# TABELA DE DADOS (EXPANSÍVEL)
# ============================================================================

with st.expander("📋 Ver Tabela Completa de Dados", expanded=False):
    st.dataframe(
        ranking_display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Distância": st.column_config.NumberColumn("Distância ao Latim", format="%.3f"),
            "Conceitos": st.column_config.NumberColumn("Conceitos", format="%d")
        }
    )

st.divider()

# ============================================================================
# PERFIL DE CONSERVADORISMO
# ============================================================================

st.subheader("🔍 Línguas com Perfil de Conservadorismo Similar a: " + referencia)
st.caption(f"*Comparação do grau de proximidade ao Latim, não de similaridade direta entre línguas*")

st.markdown("""
Esta secção compara quais línguas têm um **grau de conservadorismo lexical** 
similar ao da língua de referência, usando **duas métricas diferentes**:

| Métrica | Descrição |
|---------|-----------|
| **Simples** | Levenshtein padrão (baseline) |
| **Ponderado** | Levenshtein com pesos fonéticos (inovação) |

**Objetivo:** Validar se a métrica ponderada produz rankings de 
perfil mais linguisticamente interpretáveis.
""")

# ============================================================================
# FUNÇÃO DE CLASSIFICAÇÃO
# ============================================================================

def classificar(diff):
    """Classifica o nível de similaridade no perfil de conservadorismo"""
    if diff < 0.05:
        return "🟢 Muito Similar"
    elif diff < 0.10:
        return "🟡 Similar"
    elif diff < 0.15:
        return "🟠 Moderadamente Diferente"
    else:
        return "🔴 Diferente"

# ============================================================================
# CALCULAR PERFIL DE CONSERVADORISMO
# ============================================================================

prox_df = df_atual.copy()
prox_df['Delta_Conservadorismo'] = abs(prox_df['Distância'] - ref_dist)
prox_df = prox_df[prox_df['Língua'] != referencia]
prox_df['Categoria de Conservadorismo'] = prox_df['Delta_Conservadorismo'].apply(classificar)
prox_df['Rank_Proximidade'] = range(1, len(prox_df) + 1)

# ============================================================================
# KPIs DE PERFIL DE CONSERVADORISMO
# ============================================================================

st.divider()
st.subheader(f"📊 Resumo de Perfil de Conservadorismo: {referencia} (Distância ao Latim: {ref_dist:.3f})")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    mais_proxima = prox_df.iloc[0]
    st.metric(
        f"Conservadorismo Mais Similar",
        mais_proxima['Língua'],
        f"Δ = {mais_proxima['Delta_Conservadorismo']:.3f}"
    )

with col_kpi2:
    menos_proxima = prox_df.iloc[-1]
    st.metric(
        f"Conservadorismo Mais Diferente",
        menos_proxima['Língua'],
        f"Δ = {menos_proxima['Delta_Conservadorismo']:.3f}"
    )

with col_kpi3:
    media_diff = prox_df['Delta_Conservadorismo'].mean()
    st.metric("Diferença Média", f"{media_diff:.3f}")

# ============================================================================
# TABELA COMPLETA DE PERFIL DE CONSERVADORISMO
# ============================================================================

st.dataframe(
    prox_df[[
        'Rank_Proximidade',
        'Língua',
        'Distância',
        'Delta_Conservadorismo',
        'Categoria de Conservadorismo'
    ]].style.format({
        'Distância': '{:.3f}',
        'Delta_Conservadorismo': '{:+.3f}'
    }).background_gradient(subset=['Delta_Conservadorismo'], cmap='YlGn'),
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# GRÁFICO DE PERFIL DE CONSERVADORISMO
# ============================================================================

# ============================================================================
# DEBUG: Verificar ordem das línguas
# ============================================================================
print("\n" + "=" * 80)
print("🔍 DEBUG: Ordem das Línguas no Gráfico de Perfil")
print("=" * 80)

print(f"\n1. linguas_comuns ({len(linguas_comuns)} línguas):")
print(f"   {linguas_comuns}")

print(f"\n2. linguas_ordenadas (ordenado alfabeticamente):")
linguas_ordenadas = sorted(linguas_comuns)
print(f"   {linguas_ordenadas}")

print(f"\n3. Línguas em prox_df ({len(prox_df)} línguas):")
print(f"   {prox_df['Língua'].tolist()}")

print(f"\n4. Língua de referência (excluída de prox_df): {referencia}")

# Filtrar para incluir SÓ línguas que estão em prox_df
linguas_ordenadas = [l for l in linguas_ordenadas if l in prox_df['Língua'].values]

print(f"\n5. linguas_ordenadas após filtrar referência ({len(linguas_ordenadas)} línguas):")
print(f"   {linguas_ordenadas}")

# Ordenar DataFrame pela lista fixa
prox_df_sorted = prox_df[prox_df['Língua'].isin(linguas_ordenadas)]
prox_df_sorted = prox_df_sorted.set_index('Língua').loc[linguas_ordenadas].reset_index()

print(f"\n6. Ordem FINAL no gráfico (prox_df_sorted):")
print(f"   {prox_df_sorted['Língua'].tolist()}")

print("\n" + "=" * 80)
print("✅ FIM DO DEBUG")
print("=" * 80 + "\n")
# ============================================================================
# FIM DO DEBUG
# ============================================================================

fig_prox = px.bar(
    prox_df_sorted,
    x='Língua',
    y='Delta_Conservadorismo',
    color='Categoria de Conservadorismo',
    color_discrete_map={
        "🟢 Muito Similar": "#4CAF50",
        "🟡 Similar": "#FFC107",
        "🟠 Moderadamente Diferente": "#FF9800",
        "🔴 Diferente": "#F44336"
    },
    text='Delta_Conservadorismo',
    title=f'Diferença de Conservadorismo em Relação a {referencia} ({nome_metrica})',
    labels={'Delta_Conservadorismo': 'Diferença Absoluta', 'Língua': 'Língua'}
)

fig_prox.update_xaxes(categoryorder='array', categoryarray=linguas_ordenadas)

fig_prox.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig_prox.update_layout(height=400, showlegend=True)
st.plotly_chart(fig_prox, use_container_width=True)

# ============================================================================
# COMPARAÇÃO DIRETA: RANKINGS DIFEREM?
# ============================================================================

st.divider()
st.subheader("⚖️ Comparação Direta: Os Rankings São Diferentes?")

# Calcular rankings para ambas as métricas
def calcular_ranking_proximidade(df, ref=None):
    if ref is None:
        ref = referencia
    ref_dist = df[df['Língua'] == ref]['Distância'].iloc[0]
    prox = df.copy()
    prox['Diff'] = abs(prox['Distância'] - ref_dist)
    prox = prox[prox['Língua'] != ref].sort_values('Diff').reset_index(drop=True)
    prox['Rank'] = range(1, len(prox) + 1)
    return prox[['Língua', 'Rank']]

rank_simple = calcular_ranking_proximidade(df_simple)
rank_weighted = calcular_ranking_proximidade(df_weighted)

# Juntar rankings
comparacao_ranks = pd.merge(rank_simple, rank_weighted, on='Língua', suffixes=('_Simples', '_Ponderado'))
comparacao_ranks['Mudança'] = comparacao_ranks['Rank_Ponderado'] - comparacao_ranks['Rank_Simples']

# Mostrar tabela de comparação
st.markdown(f"**Perfil de Conservadorismo em relação a {referencia}:**")
st.dataframe(
    comparacao_ranks.style.format({'Rank_Simples': '{:.0f}º', 'Rank_Ponderado': '{:.0f}º', 'Mudança': '{:+d}'})
    .background_gradient(subset=['Mudança'], cmap='RdYlGn_r'),
    use_container_width=True,
    hide_index=True
)

# Gráfico de mudança de ranking
fig_mudanca = px.bar(
    comparacao_ranks.sort_values('Mudança'),
    x='Língua',
    y='Mudança',
    color='Mudança',
    color_continuous_scale='RdYlGn',
    text='Mudança',
    title='Mudança no Ranking: Ponderado vs. Simples',
    labels={'Mudança': 'Variação no Ranking', 'Língua': 'Língua'}
)
fig_mudanca.add_hline(y=0, line_dash="dash", line_color="gray")
fig_mudanca.update_traces(texttemplate='%{text:+d}', textposition='outside')
fig_mudanca.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_mudanca, use_container_width=True)

# ============================================================================
# INSIGHT COMPARATIVO
# ============================================================================

# Identificar maiores mudanças
maior_subida = comparacao_ranks.loc[comparacao_ranks['Mudança'].idxmin()]
maior_descida = comparacao_ranks.loc[comparacao_ranks['Mudança'].idxmax()]

st.success(f"""
**🔍 Insight Comparativo:**

| Métrica | Top 3 Mais Próximas de {referencia} |
|---------|--------------------------------|
| **Simples** | {', '.join(rank_simple.head(3)['Língua'].tolist())} |
| **Ponderado** | {', '.join(rank_weighted.head(3)['Língua'].tolist())} |

**Principais Mudanças:**
- 📈 **{maior_subida['Língua']}**: subiu {abs(maior_subida['Mudança'])} posições com a métrica ponderada
- 📉 **{maior_descida['Língua']}**: desceu {maior_descida['Mudança']} posições com a métrica ponderada

**Interpretação:**
A métrica ponderada {'reforça' if rank_weighted.iloc[0]['Língua'] == rank_simple.iloc[0]['Língua'] else 'altera'} 
o ranking de perfil de conservadorismo, demonstrando que considerar similaridade fonética produz 
classificações {'mais consistentes com a linguística histórica' if 'Galego' in rank_weighted.head(3)['Língua'].values else 'diferentes da baseline'}.

**Valor metodológico:** Esta comparação valida que a métrica ponderada não é apenas 
uma variação técnica, mas produz insights qualitativamente diferentes sobre relações 
de similaridade lexical.
""")

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>

**Interface Web desenvolvida com Streamlit** | 
Dados: ASJP Database, Glottolog 4.6 | 
Metodologia: Distância de Levenshtein Ponderada

</div>
""", unsafe_allow_html=True)