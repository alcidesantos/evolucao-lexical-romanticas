import pandas as pd
from pathlib import Path

asjp_file = Path("data/asjp/asjp.csv")

if asjp_file.exists():
    df = pd.read_csv(asjp_file, nrows=5)

    print("=" * 60)
    print("📋 COLUNAS DISPONÍVEIS:")
    print("=" * 60)
    for i, col in enumerate(df.columns):
        print(f"  {i}: '{col}'")

    print("\n" + "=" * 60)
    print("📄 PRIMEIRAS 3 LINHAS:")
    print("=" * 60)
    print(df.head(3).to_string())

    print("\n" + "=" * 60)
    print("🔍 VALORES ÚNICOS (Language/ID):")
    print("=" * 60)
    for col in df.columns[:3]:
        print(f"\n{col}: {df[col].unique()[:5]}")
else:
    print("⚠️ Ficheiro não encontrado!")