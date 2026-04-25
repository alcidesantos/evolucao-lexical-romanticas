"""
Teste do loader ASJP CLDF - Versão Corrigida
"""
from modules.asjp_loader import ASJPLoader

# Inicializar loader
loader = ASJPLoader()
loader.load()

# Glottocodes corretos para línguas românicas
TEST_LANGUAGES = {
    'port1283': 'Português',  # ASJP usa port1283 para Português moderno
    'span1282': 'Espanhol',
    'fren1253': 'Francês',
    'ital1282': 'Italiano',
    'roma1244': 'Romeno',
}

print("=" * 70)
print("📊 TESTE COM GLOTOCODES EXATOS")
print("=" * 70)

for glottocode, name in TEST_LANGUAGES.items():
    print(f"\n🇵🇹 {name} ({glottocode})")
    print("-" * 50)

    # Verificar se o glottocode existe
    lang_id = loader.get_language_id(glottocode)
    if lang_id:
        print(f"   ✅ Language_ID: {lang_id}")

        # Obter coordenadas
        coords = loader.get_language_coordinates(glottocode)
        if coords:
            print(f"   🗺️ Coordenadas: {coords}")

        # Contar palavras
        words = loader.get_language_words(glottocode)
        print(f"   📝 Palavras: {len(words)}")

        # Mostrar primeiras 5 palavras
        if len(words) > 0:
            words_with_concepts = words.merge(
                loader.parameters_df,
                left_on='Parameter_ID',
                right_on='ID',
                suffixes=('', '_concept')
            )
            print(f"   📄 Exemplos:")
            for _, row in words_with_concepts.head(5).iterrows():
                concept = row.get('Name_concept', row.get('Name', 'N/A'))
                form = row.get('Form', 'N/A')
                print(f"      {concept}: {form}")
    else:
        print(f"   ❌ Não encontrado no ASJP")

# Calcular distâncias entre línguas românicas
print("\n" + "=" * 70)
print("📊 DISTÂNCIAS LEXICAIS ENTRE ROMÂNICAS")
print("=" * 70)

available = [gc for gc in TEST_LANGUAGES.keys() if loader.get_language_id(gc)]

for i, lang1 in enumerate(available):
    for lang2 in available[i+1:]:
        distance = loader.get_lexical_distance(lang1, lang2)
        if distance:
            print(f"   {TEST_LANGUAGES[lang1]:12} ↔ {TEST_LANGUAGES[lang2]:12}: {distance:.3f}")

print("\n✅ Teste concluído!")