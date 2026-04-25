"""
Visualização de resultados - Com nomes amigáveis
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.manifold import MDS
from config import TEST_LANGUAGES_NAMED, IMAGES_DIR

def get_language_names(codes):
    """
    Converte lista de glottocodes para nomes amigáveis

    Args:
        codes: Lista de glottocodes (ex: ['port1283', 'stan1288'])

    Returns:
        Lista de nomes (ex: ['Português', 'Espanhol'])
    """
    names = []
    for code in codes:
        # Tenta obter nome do dicionário, ou usa o código se não existir
        name = TEST_LANGUAGES_NAMED.get(code, code)
        names.append(name)
    return names

def plot_distance_matrix(matrix_df, title="Matriz de Distâncias Linguísticas",
                          output_file="distance_matrix.png", dpi=300):
    """
    Plota heatmap da matriz de distâncias com nomes amigáveis

    Args:
        matrix_df: DataFrame com matriz de distâncias (índices = glottocodes)
        title: Título do gráfico
        output_file: Nome do ficheiro de saída
        dpi: Resolução da imagem
    """
    # Converter índices e colunas para nomes amigáveis
    labels = get_language_names(matrix_df.index.tolist())

    # Criar novo DataFrame com nomes
    matrix_named = matrix_df.copy()
    matrix_named.index = labels
    matrix_named.columns = labels

    output_path = IMAGES_DIR / output_file

    # Configurar plot
    plt.figure(figsize=(12, 10))

    # Heatmap com anotações
    sns.heatmap(
        matrix_named,
        annot=True,
        fmt='.3f',
        cmap='YlOrRd',
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Distância (0-1)'}
    )

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Língua', fontsize=12)
    plt.ylabel('Língua', fontsize=12)

    # Rotacionar labels para melhor leitura
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"   ✅ Heatmap guardado: {output_path}")
    plt.show()

def plot_mds_embedding(matrix_df, title="Embedding MDS - Proximidade Linguística",
                        output_file="mds_embedding.png", dpi=300):
    """
    Plota embedding MDS com nomes amigáveis

    Args:
        matrix_df: DataFrame com matriz de distâncias
        title: Título do gráfico
        output_file: Nome do ficheiro de saída
        dpi: Resolução da imagem
    """

    plt.clf()
    plt.close('all')

    # Converter para numpy
    distances = matrix_df.values

    # MDS para 2D
    mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
    embedding = mds.fit_transform(distances)

    # Obter nomes amigáveis
    labels = get_language_names(matrix_df.index.tolist())

    output_path = IMAGES_DIR / output_file

    # Configurar plot
    plt.figure(figsize=(12, 10))

    # Cores por família linguística (opcional - podes personalizar)
    colors = sns.color_palette("husl", len(labels))

    # Scatter plot
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        s=200,
        c=colors,
        alpha=0.8,
        edgecolors='black',
        linewidths=1.5
    )

    # Adicionar labels com offset para não sobrepor
    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (embedding[i, 0], embedding[i, 1]),
            fontsize=11,
            fontweight='bold',
            ha='center',
            va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
        )

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Dimensão 1", fontsize=12)
    plt.ylabel("Dimensão 2", fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"   ✅ MDS guardado: {output_path}")
    plt.show()

def plot_geographic_scatter(asjp_loader, language_codes,
                             title="Distribuição Geográfica das Línguas",
                             output_file="geographic_map.png", dpi=300):
    """
    Plota línguas num mapa simples (scatter geográfico)

    Args:
        asjp_loader: Instância do ASJPLoader com dados carregados
        language_codes: Lista de glottocodes
        title: Título do gráfico
        output_file: Nome do ficheiro de saída
    """
    # Coletar coordenadas
    coords = []
    names = []

    for code in language_codes:
        coord = asjp_loader.get_language_coordinates(code)
        if coord:
            coords.append(coord)
            names.append(TEST_LANGUAGES_NAMED.get(code, code))

    if not coords:
        print("   ⚠️ Sem coordenadas disponíveis para plot geográfico")
        return

    coords = np.array(coords)

    output_path = IMAGES_DIR / output_file

    # Configurar plot
    plt.figure(figsize=(14, 10))

    # Scatter com cores
    colors = sns.color_palette("viridis", len(names))
    plt.scatter(
        coords[:, 1],  # Longitude (eixo X)
        coords[:, 0],  # Latitude (eixo Y)
        s=200,
        c=colors,
        alpha=0.8,
        edgecolors='black',
        linewidths=1.5
    )

    # Labels
    for i, name in enumerate(names):
        plt.annotate(
            name,
            (coords[i, 1], coords[i, 0]),
            fontsize=10,
            fontweight='bold',
            ha='center',
            va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
        )

    # Configurar eixos
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel("Latitude", fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')

    # Inverter eixo Y para norte no topo
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"   ✅ Mapa geográfico guardado: {output_path}")
    plt.show()