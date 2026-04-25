"""
Procurar Mirandês especificamente
"""
from modules.asjp_loader import ASJPLoader

loader = ASJPLoader()
loader.load()

print("=" * 70)
print("🔍 PROCURAR MIRANDÊS")
print("=" * 70)

# Procurar por vários termos possíveis
search_terms = ['mirand', 'miranda', 'astur', 'leones', 'liones']

found = []
for _, row in loader.languages_df.iterrows():
    name = str(row.get('Name', '')).lower()
    glotto = str(row.get('Glottocode', '')).lower()

    for term in search_terms:
        if term in name or term in glotto:
            found.append({
                'ID': row['ID'],
                'Name': row['Name'],
                'Glottocode': row['Glottocode'],
                'Family': row.get('Family', 'N/A')
            })

if found:
    print(f"\n✅ {len(found)} resultado(s) encontrado(s):\n")
    for lang in found:
        print(f"   {lang['Glottocode']:15} → {lang['ID']:30} ({lang['Name']})")
else:
    print("\n❌ Mirandês NÃO encontrado no ASJP!")

# Mostrar glottocode oficial do Glottolog
print("\n" + "=" * 70)
print("📋 INFORMAÇÃO OFICIAL (Glottolog)")
print("=" * 70)
print("   Língua: Mirandese / Mirandês")
print("   Glottocode oficial: mira1284")
print("   Família: Indo-European > Italic > Romance > Italo-Western >")
print("              Western > Ibero-Romance > Astur-Leonese > Eastern")
print("   Falantes: ~15.000")
print("   Status: Co-oficial em Portugal (desde 1999)")