"""
Verificar estrutura do ficheiro WALS
"""
import pandas as pd
from pathlib import Path

wals_file = Path("data/wals/wals.csv")

if wals_file.exists():
    print("=" * 70)
    print("📊 ESTRUTURA DO WALS")
    print("=" * 70)

    df = pd.read_csv(wals_file, nrows=10)

    print(f"\n📋 Dimensões: {len(df)} linhas × {len(df.columns)} colunas")
    print(f"\n📑 Colunas:")
    for i, col in enumerate(df.columns):
        print(f"   {i}: '{col}'")

    print(f"\n📄 Primeiras 5 linhas:")
    print(df.head().to_string())

    print(f"\n🔍 Valores únicos por coluna:")
    for col in df.columns[:5]:
        print(f"\n   {col}:")
        print(f"   {df[col].unique()[:5]}")
else:
    print("❌ Ficheiro WALS não encontrado!")