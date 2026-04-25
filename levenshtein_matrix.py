import numpy as np

def print_levenshtein_matrix(s1, s2):
    """
    Imprime a matriz de Levenshtein completa para debugging
    """
    matrix = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)

    # Inicializar
    for i in range(len(s1) + 1):
        matrix[i, 0] = i
    for j in range(len(s2) + 1):
        matrix[0, j] = j

    # Preencher
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i, j] = min(
                matrix[i - 1, j] + 1,
                matrix[i, j - 1] + 1,
                matrix[i - 1, j - 1] + cost
            )

    # Imprimir
    print(f"\nMatriz de Levenshtein: '{s1}' ↔ '{s2}'")
    print(f"\n  ", end="")
    for c in " " + s2:
        print(f"{c:>4}", end="")
    print()

    for i in range(len(s1) + 1):
        if i == 0:
            print(f"  ", end="")
        else:
            print(f"{s1[i - 1]} ", end="")
        for j in range(len(s2) + 1):
            print(f"{matrix[i, j]:>4}", end="")
        print()

    print(f"\nDistância bruta: {matrix[len(s1), len(s2)]}")
    print(f"Distância normalizada: {matrix[len(s1), len(s2)] / max(len(s1), len(s2)):.3f}")


# Exemplo de uso
print_levenshtein_matrix("ew", "jo")