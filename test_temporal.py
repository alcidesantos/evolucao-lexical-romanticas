"""
Teste do Temporal Loader - Dia 1
"""
from modules.temporal_loader import TemporalLoader
from config import TEST_LANGUAGES, TEST_LANGUAGES_NAMED


def main():
    print("=" * 70)
    print("🕐 TESTE DO TEMPORAL LOADER - DIA 1")
    print("=" * 70)

    # Inicializar loader
    temporal = TemporalLoader()

    # Carregar dados
    if temporal.load() is None:
        print("\n❌ Falhou ao carregar dados temporais!")
        print("   Verifica se o ficheiro existe:")
        print("   data/temporal/divergence_dates.csv")
        return

    # Testar todas as línguas do estudo
    print(f"\n📋 Línguas disponíveis: {len(temporal.list_languages())}")
    print("\n" + "=" * 70)
    print("📊 DADOS TEMPORAIS DAS LÍNGUAS EM ESTUDO")
    print("=" * 70)
    print(f"\n{'Língua':<15} {'Glottocode':<12} {'Tempo (ky)':<12} {'Ano a.C.':<10} {'Confiança'}")
    print("-" * 70)

    for glotto in TEST_LANGUAGES:
        name = TEST_LANGUAGES_NAMED.get(glotto, glotto)
        time_ky = temporal.get_divergence_time(glotto, 'ky')
        time_bc = temporal.get_divergence_time(glotto, 'bc')
        conf = temporal.get_confidence(glotto)

        if time_ky:
            print(f"{name:<15} {glotto:<12} {time_ky:<12.1f} {time_bc:<10} {conf:<10}")
        else:
            print(f"{name:<15} {glotto:<12} {'N/A':<12} {'N/A':<10} {'N/A':<10}")

    # Teste específico: Latim vs Românicas
    print("\n" + "=" * 70)
    print("🏛️ COMPARAÇÃO: LATIM vs ROMÂNICAS")
    print("=" * 70)

    latin_time = temporal.get_divergence_time('lati1261', 'ky')
    rom_time = temporal.get_divergence_time('port1283', 'ky')

    if latin_time and rom_time:
        diff = latin_time - rom_time
        print(f"\nLatim:      {latin_time:.1f} ky BP (~{temporal.get_divergence_time('lati1261', 'bc')} a.C.)")
        print(f"Português:  {rom_time:.1f} ky BP (~{temporal.get_divergence_time('port1283', 'bc')} a.C.)")
        print(f"Diferença:  {diff:.1f} ky (Latim divergiu {diff * 1000:.0f} anos antes)")

    print("\n" + "=" * 70)
    print("✅ TESTE DO DIA 1 CONCLUÍDO!")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("🌍 DISTRIBUIÇÃO POR RAMO INDO-EUROPEU")
    print("=" * 70)

    branch_counts = temporal.get_branch_distribution()
    for branch, count in sorted(branch_counts.items(), key=lambda x: -x[1]):
        print(f"   {branch:15} : {count} língua(s)")


if __name__ == "__main__":
    main()