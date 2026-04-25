"""
Análise de informação temporal nas línguas do ASJP
"""
import pandas as pd
from pathlib import Path
from config import DATA_DIR, TEST_LANGUAGES, TEST_LANGUAGES_NAMED


def main():
    print("=" * 70)
    print("🕐 ANÁLISE DE INFORMAÇÃO TEMPORAL")
    print("=" * 70)

    # Carregar languages.csv do ASJP
    asjp_lang_file = DATA_DIR / "asjp" / "lexibank-asjp-0127953" / "cldf" / "languages.csv"

    if not asjp_lang_file.exists():
        print(f"❌ Ficheiro não encontrado: {asjp_lang_file}")
        return

    df = pd.read_csv(asjp_lang_file)
    print(f"✅ {len(df)} línguas carregadas")

    # Filtrar apenas as línguas do nosso estudo
    print(f"\n📋 Línguas em análise:")
    print("-" * 70)

    results = []
    for glotto in TEST_LANGUAGES:
        row = df[df['Glottocode'] == glotto]

        if len(row) > 0:
            lang = row.iloc[0]
            name = TEST_LANGUAGES_NAMED.get(glotto, glotto)

            # Extrair informação temporal
            recently_extinct = lang.get('recently_extinct', False)
            long_extinct = lang.get('long_extinct', False)
            year_extinct = lang.get('year_of_extinction')

            # Interpretar status temporal
            if long_extinct:
                status = "🏛️ Extinta (antiga)"
            elif recently_extinct and pd.notna(year_extinct):
                status = f"⚰️ Extinta (~{int(year_extinct)})"
            elif recently_extinct:
                status = "⚰️ Extinta (século XX)"
            else:
                status = "✅ Viva / Attestada"

            results.append({
                'glottocode': glotto,
                'name': name,
                'status': status,
                'year_extinct': year_extinct,
                'family': lang.get('Family', 'N/A')
            })

            print(f"\n{name} ({glotto})")
            print(f"   Status: {status}")
            if pd.notna(year_extinct):
                print(f"   Ano de extinção: {int(year_extinct)}")
            print(f"   Família: {lang.get('Family', 'N/A')}")
        else:
            print(f"\n⚠️ {glotto} não encontrado no ASJP")

    # Tabela resumo
    print("\n" + "=" * 70)
    print("📋 RESUMO TEMPORAL")
    print("=" * 70)

    summary_df = pd.DataFrame(results)
    print(summary_df[['name', 'status', 'year_extinct']].to_string(index=False))

    # Estatísticas
    alive = len([r for r in results if 'Viva' in r['status']])
    extinct = len([r for r in results if 'Extinta' in r['status']])

    print(f"\n📊 Estatísticas:")
    print(f"   Línguas vivas/atestadas: {alive}/{len(results)}")
    print(f"   Línguas extintas: {extinct}/{len(results)}")

    # Implicações para análise
    print("\n" + "=" * 70)
    print("⚠️ IMPLICAÇÕES METODOLÓGICAS")
    print("=" * 70)

    if extinct > 0:
        print(f"""
   • {extinct} língua(s) extinta(s) no dataset
   • Dados lexicais podem representar estádios históricos
   • Comparação com línguas vivas requer cautela temporal
   • Distâncias podem refletir mudança diacrónica, não apenas divergência
        """)
    else:
        print("""
   • Todas as línguas estão atestadas em período moderno
   • Distâncias refletem principalmente divergência genealógica
   • Limitação: não capturamos mudança histórica profunda (ex: Latim → Português)
        """)


if __name__ == "__main__":
    main()