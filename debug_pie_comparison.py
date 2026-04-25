"""
Debug detalhado da comparação PIE → Línguas Românicas
"""
from modules.asjp_loader import ASJPLoader
from modules.pie_loader import PIELoader
from config import TEST_LANGUAGES_NAMED


def main():
    print("=" * 80)
    print("🔍 DEBUG: COMPARAÇÃO PIE → ROMÂNICAS")
    print("=" * 80)

    # Carregar dados
    asjp = ASJPLoader()
    asjp.load()

    pie = PIELoader()
    if pie.load() is None:
        print("❌ PIE não carregado")
        return

    # Línguas para debug
    debug_languages = ['port1283', 'stan1290']  # PT e FR
    concept_ids = list(range(1, 21))  # Primeiros 20 conceitos

    print(f"\n📋 Comparando {len(debug_languages)} línguas × {len(concept_ids)} conceitos")
    print("=" * 80)

    for glotto in debug_languages:
        name = TEST_LANGUAGES_NAMED.get(glotto, glotto)
        print(f"\n🇵🇹 {name} ({glotto})")
        print("-" * 80)

        # Obter palavras da língua
        words = asjp.get_language_words(glotto, concept_ids)
        pie_forms = pie.get_forms_dict()

        # Contadores
        matched = 0
        total_dist = 0
        examples = []

        for cid in concept_ids:
            # Forma PIE
            if cid not in pie_forms:
                continue
            pie_form = pie_forms[cid]

            # Forma da língua alvo
            lang_words = words[words['Parameter_ID'] == cid]
            if len(lang_words) == 0:
                continue

            lang_form = lang_words.iloc[0].get('Segments', lang_words.iloc[0].get('Form', ''))
            if pd.isna(lang_form):
                continue

            # Limpar formas
            pie_clean = str(pie_form).replace(' ', '')
            lang_clean = str(lang_form).replace(' ', '')

            if not pie_clean or not lang_clean:
                continue

            # Calcular distância
            from modules.distance_calculator import normalized_levenshtein
            dist = normalized_levenshtein(pie_clean, lang_clean)

            matched += 1
            total_dist += dist

            # Guardar exemplos extremos
            if dist > 0.8 or dist < 0.2:
                examples.append({
                    'concept': cid,
                    'pie': pie_form,
                    'lang': lang_form,
                    'dist': dist
                })

        # Estatísticas
        if matched > 0:
            avg_dist = total_dist / matched
            print(f"   Conceitos comparados: {matched}/{len(concept_ids)}")
            print(f"   Distância média: {avg_dist:.3f}")

            # Exemplos extremos
            if examples:
                print(f"\n   🔍 Exemplos {'mais distantes' if avg_dist > 0.7 else 'mais próximos'}:")
                for ex in examples[:5]:
                    print(
                        f"      #{ex['concept']:2d}: PIE '{ex['pie']:10}' ↔ {name[:3]} '{ex['lang']:10}' = {ex['dist']:.3f}")
        else:
            print(f"   ⚠️ Nenhum conceito comparável encontrado!")


if __name__ == "__main__":
    import pandas as pd

    main()