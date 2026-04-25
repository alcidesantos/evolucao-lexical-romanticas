"""
Verificar nomes dos conceitos no ASJP
"""
from modules.asjp_loader import ASJPLoader

asjp = ASJPLoader()
asjp.load()

print("=" * 60)
print("📋 CONCEITOS DO ASJP (Primeiros 30)")
print("=" * 60)
print(f"{'ID':<6} {'Nome':<25} {'Concepticon_Gloss'}")
print("-" * 60)

for _, row in asjp.parameters_df.head(30).iterrows():
    print(f"{row['ID']:<6} {row['Name']:<25} {row.get('Concepticon_Gloss', 'N/A')}")