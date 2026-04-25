"""
Pipeline Principal - Distância Linguística Multi-Dimensional
"""
from modules.distance_calculator import LinguisticDistanceCalculator
from modules.visualizer import plot_distance_matrix, plot_mds_embedding
from config import TEST_LANGUAGES, IMAGES_DIR

def main():
    print("=" * 60)
    print("🌍 PIPELINE DE DISTÂNCIA LINGUÍSTICA")
    print("=" * 60)

    # Inicializar calculadora
    calculator = LinguisticDistanceCalculator()

    # Línguas para analisar
    languages = TEST_LANGUAGES
    print(f"\n📋 Línguas a analisar: {len(languages)}")
    for lang in languages:
        print(f"   - {lang}")

    # Calcular matriz de distâncias
    print("\n🔢 A calcular matriz de distâncias...")
    distance_matrix = calculator.create_distance_matrix(languages)

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("📊 MATRIZ DE DISTÂNCIAS")
    print("=" * 60)
    print(distance_matrix.round(3))

    # Visualizar
    print("\n📈 A gerar visualizações...")
    plot_distance_matrix(distance_matrix)

    plot_mds_embedding(distance_matrix)

    # Adicionar plot geográfico (opcional mas recomendado)
    print("\n🗺️ A gerar mapa geográfico...")
    from modules.visualizer import plot_geographic_scatter
    plot_geographic_scatter(
        calculator.asjp,
        languages,
        title="Línguas Românicas: Distribuição Geográfica",
        output_file="geographic_map.png"
    )

    # Exemplo: Distâncias detalhadas para um par
    print("\n" + "=" * 60)
    print("🔍 EXEMPLO: Português vs Romeno")
    print("=" * 60)
    detailed = calculator.calculate_all_distances('port1281', 'roma1244')
    for dim, dist in detailed.items():
        print(f"   {dim}: {dist:.3f}" if dist else f"   {dim}: N/A")

    print("\n✅ Pipeline concluído!")

    print("\n" + "=" * 60)
    print("📁 FICHEIROS GERADOS")
    print("=" * 60)
    print(f"   📊 Matriz de distâncias: {IMAGES_DIR / 'distance_matrix.png'}")
    print(f"   🗺️ MDS Embedding: {IMAGES_DIR / 'mds_embedding.png'}")
    print(f"   🌍 Mapa geográfico: {IMAGES_DIR / 'geographic_map.png'}")
    print("\n✅ Pipeline concluído!")


if __name__ == "__main__":
    main()