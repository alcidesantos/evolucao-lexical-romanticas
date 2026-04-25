"""
Análise detalhada dos ficheiros CLDF do ASJP
"""
import pandas as pd
from pathlib import Path

# Ajusta este caminho para onde descomprimiste os dados
asjp_base = Path("data/asjp/lexibank-asjp-0127953/cldf")

print("=" * 70)
print("📊 ANÁLISE DOS FICHEIROS CLDF")
print("=" * 70)

# 1. ANALISAR languages.csv
print("\n" + "=" * 70)
print("1️⃣ LANGUAGES.CSV")
print("=" * 70)

lang_file = asjp_base / "languages.csv"
if lang_file.exists():
    df_lang = pd.read_csv(lang_file)
    print(f"\n📋 Dimensões: {len(df_lang)} línguas × {len(df_lang.columns)} colunas")
    print(f"\n📑 Colunas:")
    for i, col in enumerate(df_lang.columns):
        print(f"   {i}: '{col}'")

    print(f"\n📄 Primeiras 3 línguas:")
    print(df_lang.head(3).to_string())

    # Procurar colunas importantes
    print("\n🔍 Colunas-chave:")
    for col in df_lang.columns:
        col_lower = str(col).lower()
        if 'glotto' in col_lower:
            print(f"   ✅ Glottocode: '{col}'")
            print(f"      Exemplos: {df_lang[col].head(3).tolist()}")
        if 'id' == col_lower or 'languageid' in col_lower:
            print(f"   ✅ ID: '{col}'")
        if 'name' in col_lower:
            print(f"   ✅ Nome: '{col}'")
        if 'iso' in col_lower:
            print(f"   ✅ ISO: '{col}'")
else:
    print(f"❌ Ficheiro não encontrado: {lang_file}")

# 2. ANALISAR parameters.csv (conceitos)
print("\n" + "=" * 70)
print("2️⃣ PARAMETERS.CSV (Conceitos)")
print("=" * 70)

param_file = asjp_base / "parameters.csv"
if param_file.exists():
    df_param = pd.read_csv(param_file)
    print(f"\n📋 Dimensões: {len(df_param)} conceitos × {len(df_param.columns)} colunas")
    print(f"\n📑 Colunas:")
    for i, col in enumerate(df_param.columns):
        print(f"   {i}: '{col}'")

    print(f"\n📄 Primeiros 10 conceitos:")
    print(df_param.head(10).to_string())
else:
    print(f"❌ Ficheiro não encontrado: {param_file}")

# 3. ANALISAR forms.csv (dados principais)
print("\n" + "=" * 70)
print("3️⃣ FORMS.CSV (Dados lexicais)")
print("=" * 70)

forms_file = asjp_base / "forms.csv"
if forms_file.exists():
    # Ler apenas primeiras linhas para não sobrecarregar
    df_forms = pd.read_csv(forms_file, nrows=100)
    print(f"\n📋 Amostra: {len(df_forms)} linhas × {len(df_forms.columns)} colunas")
    print(f"   (Ficheiro completo: {forms_file.stat().st_size / 1024 / 1024:.1f} MB)")

    print(f"\n📑 Colunas:")
    for i, col in enumerate(df_forms.columns):
        print(f"   {i}: '{col}'")

    print(f"\n📄 Primeiras 10 linhas:")
    print(df_forms.head(10).to_string())

    # Identificar colunas importantes
    print("\n🔍 Mapeamento de colunas:")
    col_map = {}
    for col in df_forms.columns:
        col_lower = str(col).lower()
        if 'language' in col_lower and 'id' in col_lower:
            col_map['language_id'] = col
        elif 'glotto' in col_lower:
            col_map['glottocode'] = col
        elif 'parameter' in col_lower or 'concept' in col_lower:
            col_map['concept'] = col
        elif 'form' in col_lower or 'value' in col_lower or 'transcription' in col_lower:
            col_map['form'] = col

    for key, value in col_map.items():
        print(f"   {key}: '{value}'")

    # Estatísticas
    print(f"\n📊 Estatísticas:")
    if 'Language_ID' in df_forms.columns:
        n_langs = df_forms['Language_ID'].nunique()
        print(f"   • Línguas na amostra: {n_langs}")
    if 'Parameter_ID' in df_forms.columns:
        n_concepts = df_forms['Parameter_ID'].nunique()
        print(f"   • Conceitos na amostra: {n_concepts}")
    print(f"   • Total de formas: {len(df_forms)}")

    # Verificar dados de Português
    print(f"\n🇵🇹 Exemplo: Português (port1281)")
    if 'Language_ID' in df_forms.columns:
        pt_data = df_forms[df_forms['Language_ID'] == 'port1281']
        if len(pt_data) > 0:
            print(f"   • Formas encontradas: {len(pt_data)}")
            print(f"   • Exemplos:")
            for _, row in pt_data.head(5).iterrows():
                concept = row.get('Parameter_ID', 'N/A')
                form = row.get('Form', row.get('Value', 'N/A'))
                print(f"     - {concept}: {form}")
        else:
            print("   ⚠️ Português não encontrado na amostra")
else:
    print(f"❌ Ficheiro não encontrado: {forms_file}")

print("\n" + "=" * 70)
print("✅ Análise concluída!")
print("=" * 70)