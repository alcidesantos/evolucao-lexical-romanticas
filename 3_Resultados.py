"""
Interface Web para Análise de Evolução Lexical das Línguas Românicas

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



# ============================================================================
# SIDEBAR: CONTROLES E NAVEGAÇÃO
# ============================================================================



# ============================================================================
# CARREGAR DADOS
# ============================================================================

ranking_df, outliers_df = load_results()

# ============================================================================
# PASSO 1: PREPARAR DADOS PARA AMBAS AS MÉTRICAS
# ============================================================================

# Caminhos dos CSVs
simple_csv_path = DATA_DIR / "outliers" / "latin_romance_ranking_simple.csv"
weighted_csv_path = DATA_DIR / "outliers" / "latin_romance_ranking_weighted.csv"

# Carregar dados SIMPLES
if simple_csv_path.exists():
    df_simple = pd.read_csv(simple_csv_path)
    print(f"✅ df_simple carregado: {len(df_simple)} línguas")
else:
    df_simple = None
    print("⚠️ df_simple NÃO carregado (ficheiro não existe)")

# Carregar dados PONDERADOS
if weighted_csv_path.exists():
    df_weighted = pd.read_csv(weighted_csv_path)
    print(f"✅ df_weighted carregado: {len(df_weighted)} línguas")
else:
    df_weighted = ranking_df.copy()
    print("⚠️ df_weighted NÃO carregado (a usar ranking_df)")

# Seletor na sidebar (apenas para testar se funciona)
st.sidebar.header("📊 Métrica do Ranking Principal")

metrica_principal = st.sidebar.radio(
    "Para o gráfico principal:",
    ["🟢 Ponderada (Principal)", "🔵 Simples (Baseline)"],
    index=0,
    key="main_metric"
)

# Preparar dataframe de exibição (ainda NÃO usamos no gráfico - só para teste)
if "Simples" in metrica_principal and df_simple is not None:
    ranking_display_df = df_simple.copy()
    nota_metrica = "Simples"
else:
    ranking_display_df = df_weighted.copy()
    nota_metrica = "Ponderada"

# === DEBUG: Mostrar qual métrica está selecionada ===
st.sidebar.success(f"**Métrica selecionada:** {nota_metrica}")
st.sidebar.info(f"**Línguas disponíveis:** {len(ranking_display_df)}")
# ====================================================

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

# Métricas em destaque (KPIs)
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

#if not show_grid:
fig_ranking.update_xaxes(showgrid=False)
fig_ranking.update_yaxes(showgrid=False)

st.plotly_chart(fig_ranking, use_container_width=True)

# ============================================================================
# TABELA DE DADOS
# ============================================================================

with st.expander("📋 Ver Tabela Completa de Dados", expanded=False):
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
# DADOS DE AMBAS AS MÉTRICAS
# ============================================================================

# Carregar dados SIMPLES diretamente do CSV (garante consistência de nomes)
simple_csv_path = DATA_DIR / "outliers" / "latin_romance_ranking_simple.csv"
if simple_csv_path.exists():
    df_simple = pd.read_csv(simple_csv_path)
    print(f"✅ Dados simples carregados: {len(df_simple)} línguas")
else:
    # Fallback para dados hardcoded (9 línguas originais)
    simple_data = {
        'Língua': ['Italian', 'Mirandese', 'Galician', 'Catalan', 'Asturian',
                   'Spanish', 'Romanian', 'Portuguese', 'French'],
        'Distância': [0.634, 0.682, 0.641, 0.657, 0.680, 0.760, 0.747, 0.734, 0.847]
    }
    df_simple = pd.DataFrame(simple_data)
    print(f"⚠️ CSV simples não encontrado, a usar fallback (9 línguas)")

# Dados da métrica PONDERADA (já carregados em ranking_df)
df_weighted = ranking_df[['Língua', 'Distância']].copy()

# ============================================================================
# SELETOR DE MÉTRICA (na sidebar)
# ============================================================================

st.sidebar.header("📊 Métrica para Proximidade")

metrica_selecionada = st.sidebar.radio(
    "Para a análise de proximidade:",
    ["🟢 Ponderado (Fonética)", "🔵 Simples (Baseline)"],
    index=0
)

# Info message também na sidebar
if "Ponderado" in metrica_selecionada:
    st.sidebar.info("✅ Métrica com pesos fonéticos: captura evolução linguística natural")
else:
    st.sidebar.info("📏 Métrica baseline: todas as substituições custam igual")

# Selecionar DataFrame conforme métrica (esta lógica fica igual, só muda a origem do radio)
if "Ponderado" in metrica_selecionada:
    df_atual = df_weighted.copy()
    nome_metrica = "Ponderado"
    cor_destaque = "#4CAF50"
else:
    df_atual = df_simple.copy()
    nome_metrica = "Simples"
    cor_destaque = "#2196F3"

# ============================================================================
# SELETOR DE LÍNGUA DE REFERÊNCIA
# ============================================================================

st.subheader("🔍 Proximidade a Língua de Referência: Comparação de Métricas")

st.markdown("""
Comparamos quais línguas são lexicalmente mais próximas do Mirandês 
usando **duas métricas diferentes**:

| Métrica | Descrição |
|---------|-----------|
| **Simples** | Levenshtein padrão (baseline) |
| **Ponderado** | Levenshtein com pesos fonéticos (inovação) |

**Objetivo:** Validar se a métrica ponderada produz rankings de 
proximidade mais linguisticamente interpretáveis.
""")

st.sidebar.header("🎯 Língua de Referência")

referencia = st.sidebar.selectbox(
    "Calcular proximidade em relação a:",
    ranking_df['Língua'].tolist(),
    index=int(ranking_df[ranking_df['Língua'] == 'Mirandese'].index[0]),  # ← Converter para int!
    help="Escolhe uma língua para calcular quais as outras línguas mais próximas"
)

st.sidebar.info(f"""
**Língua Selecionada:** {referencia}  
**Distância:** {ranking_df[ranking_df['Língua'] == referencia]['Distância'].iloc[0]:.3f}  
**Rank:** {ranking_df[ranking_df['Língua'] == referencia]['Rank'].iloc[0]}º
""")

# ============================================================================
# FUNÇÃO DE CLASSIFICAÇÃO DE PROXIMIDADE
# ============================================================================

def classificar(diff):
    """Classifica o nível de proximidade baseado na diferença absoluta"""
    if diff < 0.05:
        return "🟢 Muito Próxima"
    elif diff < 0.10:
        return "🟡 Próxima"
    elif diff < 0.15:
        return "🟠 Moderadamente Distante"
    else:
        return "🔴 Distante"

# ============================================================================
# CALCULAR PROXIMIDADE A REFREÊNCIA
# ============================================================================

mir_dist = df_atual[df_atual['Língua'] == referencia]['Distância'].iloc[0]

prox_df = df_atual.copy()
prox_df['Diferença_vs_Referência'] = abs(prox_df['Distância'] - mir_dist)
prox_df = prox_df[prox_df['Língua'] != 'Mirandese']
prox_df['Proximidade'] = prox_df['Diferença_vs_Referência'].apply(classificar)
prox_df['Rank_Proximidade'] = range(1, len(prox_df) + 1)

# Classificar proximidade
def classificar(diff):
    if diff < 0.05:
        return "🟢 Muito Próxima"
    elif diff < 0.10:
        return "🟡 Próxima"
    elif diff < 0.15:
        return "🟠 Moderadamente Distante"
    else:
        return "🔴 Distante"

prox_df['Proximidade'] = prox_df['Diferença_vs_Referência'].apply(classificar)

# ============================================================================
# KPIs
# ============================================================================

st.divider()
st.subheader(f"📊 Línguas Mais Próximas de: {referencia}")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    mais_proxima = prox_df.iloc[0]
    st.metric(
        f"Mais Próxima de {referencia}",
        mais_proxima['Língua'],
        f"Δ = {mais_proxima['Diferença_vs_Referência']:.3f}"
    )

with col_kpi2:
    menos_proxima = prox_df.iloc[-1]
    st.metric(
        f"Mais Distante de {referencia}",
        menos_proxima['Língua'],
        f"Δ = {menos_proxima['Diferença_vs_Referência']:.3f}"
    )

with col_kpi3:
    media_diff = prox_df['Diferença_vs_Referência'].mean()
    st.metric("Diferença Média", f"{media_diff:.3f}")

# ============================================================================
# TABELA COMPLETA
# ============================================================================

st.dataframe(
    prox_df[[
        'Rank_Proximidade',
        'Língua',
        'Distância',
        'Diferença_vs_Referência',
        'Proximidade'
    ]].style.format({
        'Distância': '{:.3f}',
        'Diferença_vs_Referência': '{:+.3f}'
    }).background_gradient(subset=['Diferença_vs_Referência'], cmap='YlGn'),
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# GRÁFICO
# ============================================================================

fig_prox = px.bar(
    prox_df,
    x='Língua',
    y='Diferença_vs_Referência',
    color='Proximidade',
    color_discrete_map={
        "🟢 Muito Próxima": "#4CAF50",
        "🟡 Próxima": "#FFC107",
        "🟠 Moderadamente Distante": "#FF9800",
        "🔴 Distante": "#F44336"
    },
    text='Diferença_vs_Referência',
    title=f'Distância Lexical em Relação a {referencia} ({nome_metrica})',
    labels={'Diferença_vs_Referência': 'Diferença Absoluta', 'Língua': 'Língua'}
)

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
st.markdown(f"**Ranking de Proximidade a {referencia}:**")
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
maior_subida = comparacao_ranks.loc[comparacao_ranks['Mudança'].idxmin()]  # Mais negativo = subiu mais
maior_descida = comparacao_ranks.loc[comparacao_ranks['Mudança'].idxmax()]  # Mais positivo = desceu mais

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
o ranking de proximidade, demonstrando que considerar similaridade fonética produz 
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
Dados: ASJP Database, Glottolog 4.6 

</div>
""", unsafe_allow_html=True)