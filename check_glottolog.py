"""
Verificar se os dados do Glottolog estão disponíveis
"""
from pathlib import Path
import pandas as pd

# Caminhos possíveis para dados do Glottolog
possible_paths = [
    Path("data/glottolog"),
    Path("data/glottolog/glottolog.csv"),
    Path("data/glottolog/languages.csv"),
    Path("data/glottolog/glottolog-4.6/languages.csv"),
]

print("=" * 70)
print("🔍 VERIFICAR DADOS DO GLOTTLOG")
print("=" * 70)

# 1. Verificar pastas e ficheiros
print("\n📂 Estrutura da pasta data/:")
data_dir = Path("data")
if data_dir.exists():
    for item in data_dir.iterdir():
        if item.is_dir():
            print(f"   📁 {item.name}/")
            # Listar conteúdo de subpastas
            for subitem in item.iterdir():
                if subitem.is_file():
                    size_kb = subitem.stat().st_size / 1024
                    print(f"      📄 {subitem.name} ({size_kb:.1f} KB)")
                else:
                    print(f"      📁 {subitem.name}/")
        else:
            print(f"   📄 {item.name}")
else:
    print("   ❌ Pasta 'data' não encontrada!")

# 2. Procurar ficheiros CSV do Glottolog
print("\n" + "=" * 70)
print("📄 PROCURAR FICHEIROS GLOTTLOG")
print("=" * 70)

glottolog_files = list(Path(".").rglob("glottolog*.csv")) + list(Path(".").rglob("languages*.csv"))

if glottolog_files:
    print(f"\n✅ {len(glottolog_files)} ficheiro(s) encontrado(s):\n")
    for f in glottolog_files[:10]:  # Mostrar primeiros 10
        size_mb = f.stat().st_size / 1024 / 1024
        print(f"   📄 {f} ({size_mb:.2f} MB)")
else:
    print("\n❌ Nenhum ficheiro do Glottolog encontrado!")

# 3. Analisar primeiro ficheiro encontrado
print("\n" + "=" * 70)
print("📊 ANALISAR ESTRUTURA DO PRIMEIRO FICHEIRO")
print("=" * 70)

if glottolog_files:
    first_file = glottolog_files[0]
    print(f"\nFicheiro: {first_file}")

    try:
        df = pd.read_csv(first_file, nrows=5)
        print(f"\n📋 Colunas ({len(df.columns)}):")
        for i, col in enumerate(df.columns):
            print(f"   {i}: '{col}'")

        print(f"\n📄 Primeiras 3 linhas:")
        print(df.head(3).to_string())

        # Procurar colunas importantes
        print("\n🔍 Colunas relevantes:")
        col_lower = [str(c).lower() for c in df.columns]
        for target in ['glotto', 'id', 'name', 'lat', 'lon', 'family']:
            for i, col in enumerate(df.columns):
                if target in str(col).lower():
                    print(f"   ✅ '{col}' (contém '{target}')")

    except Exception as e:
        print(f"\n❌ Erro ao ler ficheiro: {e}")
else:
    print("\n⚠️ Sem ficheiros para analisar")

# 4. Verificar se ASJP tem coordenadas (alternativa)
print("\n" + "=" * 70)
print("📊 ALTERNATIVA: COORDENADAS NO ASJP")
print("=" * 70)

asjp_lang_file = Path("data/asjp/lexibank-asjp-0127953/cldf/languages.csv")
if asjp_lang_file.exists():
    print(f"\n✅ Ficheiro ASJP languages.csv encontrado!")

    try:
        df_asjp = pd.read_csv(asjp_lang_file, nrows=5)
        print(f"\n📋 Colunas disponíveis:")
        for i, col in enumerate(df_asjp.columns):
            print(f"   {i}: '{col}'")

        # Verificar coordenadas
        has_coords = 'Latitude' in df_asjp.columns and 'Longitude' in df_asjp.columns
        has_glotto = 'Glottocode' in df_asjp.columns

        print(f"\n🗺️ Coordenadas: {'✅ Sim' if has_coords else '❌ Não'}")
        print(f"🔖 Glottocodes: {'✅ Sim' if has_glotto else '❌ Não'}")

        if has_coords and has_glotto:
            print("\n💡 CONCLUSÃO: Podes usar o ASJP para coordenadas!")
            print("   Não é necessário descarregar Glottolog separado.")

    except Exception as e:
        print(f"\n❌ Erro ao ler ASJP: {e}")
else:
    print(f"\n❌ Ficheiro ASJP não encontrado: {asjp_lang_file}")

print("\n" + "=" * 70)
print("✅ Verificação concluída!")
print("=" * 70)