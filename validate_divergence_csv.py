"""
Validar integridade do divergence_dates.csv
Dia 1 - Fundação Temporal
"""
import pandas as pd
from pathlib import Path
from config import DATA_DIR, TEST_LANGUAGES, TEST_LANGUAGES_NAMED


def main():
    print("=" * 80)
    print("🔍 VALIDAÇÃO DO DIVERGENCE_DATES.CSV")
    print("=" * 80)

    filepath = DATA_DIR / "temporal" / "divergence_dates.csv"

    # ==========================================================================
    # 1. VERIFICAR SE FICHEIRO EXISTE
    # ==========================================================================
    print(f"\n📁 Ficheiro: {filepath}")

    if not filepath.exists():
        print(f"   ❌ Ficheiro NÃO encontrado!")
        print(f"\n   Ação necessária:")
        print(f"   1. Cria a pasta: data/temporal/")
        print(f"   2. Cria o ficheiro: divergence_dates.csv")
        print(f"   3. Adiciona cabeçalho e dados (ver template)")
        return

    print(f"   ✅ Ficheiro encontrado")

    # ==========================================================================
    # 2. CARREGAR DADOS
    # ==========================================================================
    try:
        # Ler CSV ignorando comentários (#)
        df = pd.read_csv(filepath, comment='#')
        print(f"   ✅ {len(df)} línguas carregadas")
    except Exception as e:
        print(f"   ❌ Erro ao ler ficheiro: {e}")
        return

    # ==========================================================================
    # 3. VERIFICAR COLUNAS OBRIGATÓRIAS
    # ==========================================================================
    print(f"\n📋 Colunas obrigatórias:")

    required_cols = [
        'glottocode',
        'language',
        'branch',
        'pie_divergence_bp',
        'pie_divergence_bc',
        'source',
        'confidence',
        'notes'
    ]

    missing_cols = [c for c in required_cols if c not in df.columns]

    if missing_cols:
        print(f"   ❌ Colunas em falta: {missing_cols}")
        print(f"\n   Colunas encontradas: {list(df.columns)}")
        return

    print(f"   ✅ Todas as colunas obrigatórias presentes")
    print(f"   📑 Colunas: {', '.join(df.columns)}")

    # ==========================================================================
    # 4. VERIFICAR GLOTTOCODES DUPLICADOS
    # ==========================================================================
    print(f"\n🔍 Glottocodes duplicados:")

    duplicates = df[df.duplicated('glottocode', keep=False)]

    if len(duplicates) > 0:
        print(f"   ⚠️ {len(duplicates)} glottocodes duplicados:")
        print(f"\n   {'Glottocode':<15} {'Language':<20} {'Branch':<15}")
        print(f"   {'-' * 50}")
        for _, row in duplicates.iterrows():
            print(f"   {row['glottocode']:<15} {row['language']:<20} {row['branch']:<15}")
        print(f"\n   Ação: Remove duplicados ou usa glottocodes únicos")
    else:
        print(f"   ✅ Zero duplicados")

    # ==========================================================================
    # 5. VERIFICAR VALORES N/A EM CAMPOS CRÍTICOS
    # ==========================================================================
    print(f"\n⚠️ Valores N/A em campos críticos:")

    critical_fields = ['pie_divergence_bp', 'pie_divergence_bc', 'branch']
    outgroup_branches = ['Uralic', 'Turkic', 'Dravidian', 'Afro-Asiatic', 'Sino-Tibetan']

    issues_found = False
    for field in critical_fields:
        # Verificar N/A apenas para línguas IE
        ie_df = df[~df['branch'].isin(outgroup_branches)]
        na_count = ie_df[field].isna().sum()

        if na_count > 0:
            print(f"   ⚠️ {field}: {na_count} valores N/A em línguas IE:")
            na_rows = ie_df[ie_df[field].isna()].head(3)
            for _, row in na_rows.iterrows():
                print(f"      - {row['glottocode']} ({row['language']})")
            issues_found = True
        else:
            # Contar N/A em outgroups (esperado)
            outgroup_df = df[df['branch'].isin(outgroup_branches)]
            outgroup_na = outgroup_df[field].isna().sum()
            if outgroup_na > 0:
                print(f"   ℹ️ {field}: {outgroup_na} N/A em outgroups (esperado)")

    if not issues_found:
        print(f"   ✅ Zero valores N/A em línguas IE")

    # ==========================================================================
    # 6. VERIFICAR COBERTURA DAS LÍNGUAS DE ESTUDO
    # ==========================================================================
    print(f"\n🎯 Cobertura das línguas de estudo ({len(TEST_LANGUAGES)}):")

    coverage_ok = True
    for glotto in TEST_LANGUAGES:
        name = TEST_LANGUAGES_NAMED.get(glotto, glotto)
        if glotto in df['glottocode'].values:
            row = df[df['glottocode'] == glotto].iloc[0]
            time_ky = row['pie_divergence_bp'] / 1000 if pd.notna(row['pie_divergence_bp']) else 'N/A'
            print(f"   ✅ {name:<15} ({glotto}) - {time_ky} ky [{row['branch']}]")
        else:
            print(f"   ❌ {name:<15} ({glotto}) - NÃO ENCONTRADO")
            coverage_ok = False

    if not coverage_ok:
        print(f"\n   Ação: Adiciona línguas em falta ao CSV")
    else:
        print(f"   ✅ Todas as línguas de estudo cobertas")

    # ==========================================================================
    # 7. DISTRIBUIÇÃO POR RAMO
    # ==========================================================================
    print(f"\n📊 Distribuição por ramo:")

    branch_counts = df['branch'].value_counts()
    for branch, count in branch_counts.items():
        ie_status = "IE" if branch not in ['Uralic', 'Turkic', 'Dravidian'] else "Não-IE"
        print(f"   {branch:<20} : {count:3} línguas ({ie_status})")

    # ==========================================================================
    # 8. ESTATÍSTICAS DE TEMPO DE DIVERGÊNCIA
    # ==========================================================================
    print(f"\n📈 Estatísticas de tempo de divergência (BP):")

    valid_times = df['pie_divergence_bp'].dropna()
    if len(valid_times) > 0:
        print(f"   Mínimo: {valid_times.min():.0f} anos ({valid_times.min() / 1000:.1f} ky)")
        print(f"   Máximo: {valid_times.max():.0f} anos ({valid_times.max() / 1000:.1f} ky)")
        print(f"   Média:  {valid_times.mean():.0f} anos ({valid_times.mean() / 1000:.1f} ky)")
        print(f"   Mediana: {valid_times.median():.0f} anos ({valid_times.median() / 1000:.1f} ky)")
    else:
        print(f"   ⚠️ Sem dados temporais válidos")

    # ==========================================================================
    # 9. VERIFICAR LITUANO (VALIDAÇÃO CHAVE)
    # ==========================================================================
    print(f"\n🔍 Validação crítica: Lituano")

    lithuanian = df[df['glottocode'] == 'lith1251']
    if len(lithuanian) > 0:
        row = lithuanian.iloc[0]
        time_ky = row['pie_divergence_bp'] / 1000 if pd.notna(row['pie_divergence_bp']) else 'N/A'
        print(f"   ✅ Lituano encontrado: {time_ky} ky BP [{row['confidence']}]")
        print(f"   Nota: Lituano deve emergir como mais conservador nos testes")
    else:
        print(f"   ⚠️ Lituano NÃO encontrado - recomendado adicionar para validação")

    # ==========================================================================
    # 10. RESUMO FINAL
    # ==========================================================================
    print(f"\n" + "=" * 80)
    print("📋 RESUMO DA VALIDAÇÃO")
    print("=" * 80)

    issues = []

    if len(duplicates) > 0:
        issues.append("Glottocodes duplicados")
    if issues_found:
        issues.append("Valores N/A em campos críticos")
    if not coverage_ok:
        issues.append("Línguas de estudo em falta")
    if len(lithuanian) == 0:
        issues.append("Lituano não incluído (recomendado)")

    if issues:
        print(f"\n⚠️ {len(issues)} problema(s) detetado(s):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print(f"\n   ✅ Podes prosseguir, mas resolve os problemas antes da análise final")
    else:
        print(f"\n✅ VALIDAÇÃO PASSEI!")
        print(f"   • Ficheiro estruturalmente correto")
        print(f"   • Todas as línguas de estudo cobertas")
        print(f"   • Zero duplicados ou N/A críticos")
        print(f"   • Pronto para Dia 1")

    print(f"\n" + "=" * 80)


if __name__ == "__main__":
    main()