"""
Listar todas as línguas românicas disponíveis no ASJP
"""
from modules.asjp_loader import ASJPLoader

loader = ASJPLoader()
loader.load()

print("=" * 70)
print("🔍 LÍNGUAS ROMÂNICAS NO ASJP")
print("=" * 70)

# Procurar por nomes ou glottocodes relacionados
romance_keywords = ['port', 'span', 'fren', 'ital', 'roman', 'catal', 'galic', 'occitan']

found = []
for _, row in loader.languages_df.iterrows():
    name = str(row.get('Name', '')).lower()
    glotto = str(row.get('Glottocode', '')).lower()

    for keyword in romance_keywords:
        if keyword in name or keyword in glotto:
            found.append({
                'ID': row['ID'],
                'Name': row['Name'],
                'Glottocode': row['Glottocode'],
                'Family': row.get('Family', 'N/A')
            })
            break

# Mostrar resultados
print(f"\n📊 {len(found)} línguas românicas encontradas:\n")
for lang in found:
    print(f"   {lang['Glottocode']:15} → {lang['ID']:30} ({lang['Name']})")

# Guardar para referência
print("\n" + "=" * 70)
print("📋 GLOTOCODES PARA USAR NO CONFIG.PY")
print("=" * 70)
for lang in found:
    print(f"    '{lang['Glottocode']}',  # {lang['Name']}")