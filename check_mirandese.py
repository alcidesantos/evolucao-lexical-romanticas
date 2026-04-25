"""
Verificar dados do Mirandês no ASJP
"""
from modules.asjp_loader import ASJPLoader

loader = ASJPLoader()
loader.load()

print("=" * 70)
print("📊 MIRANDÊS NO ASJP")
print("=" * 70)

# Obter informações
lang_id = loader.get_language_id('mira1251')
print(f"\n   Language_ID: {lang_id}")

coords = loader.get_language_coordinates('mira1251')
if coords:
    print(f"   Coordenadas: {coords}")

# Obter palavras
words = loader.get_language_words('mira1251')
print(f"   Número de palavras: {len(words)}")

# Mostrar primeiras 20 palavras com conceitos
if len(words) > 0:
    words_with_concepts = words.merge(
        loader.parameters_df,
        left_on='Parameter_ID',
        right_on='ID',
        suffixes=('', '_concept')
    )

    print(f"\n   📄 Primeiras 20 palavras:\n")
    print(f"   {'Conceito':<15} {'Forma':<15} {'Fonética':<20}")
    print(f"   {'-' * 50}")

    for _, row in words_with_concepts.head(20).iterrows():
        concept = row.get('Name_concept', 'N/A')
        form = row.get('Form', 'N/A')
        segments = row.get('Segments', 'N/A')
        print(f"   {concept:<15} {form:<15} {segments:<20}")

# Comparar com Português e Asturiano
print("\n" + "=" * 70)
print("📊 DISTÂNCIAS LEXICAIS")
print("=" * 70)

comparisons = [
    ('mira1251', 'port1283', 'Mirandês', 'Português'),
    ('mira1251', 'astu1245', 'Mirandês', 'Asturiano'),
    ('mira1251', 'stan1288', 'Mirandês', 'Espanhol'),
    ('mira1251', 'gali1258', 'Mirandês', 'Galego'),
]

for gc1, gc2, name1, name2 in comparisons:
    dist = loader.get_lexical_distance(gc1, gc2)
    if dist:
        print(f"   {name1:12} ↔ {name2:12}: {dist:.3f}")

print("\n✅ Verificação concluída!")