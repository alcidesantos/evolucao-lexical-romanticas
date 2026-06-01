"""Testar alinhamento de ranges"""

from modules.distance_calculator import normalized_levenshtein, weighted_levenshtein

# Pares representativos do teu corpus
test_cases = [
    ("aqua", "'agwɐ"),  # água: mudança moderada
    ("portu", "pɔɾtu"),  # porto: mudança pequena
    ("kasa", "kaza"),  # casa: mudança mínima
    ("ignis", "fɔgu"),  # fogo: mudança complexa
    ("pato", "pato"),  # idêntica
]

print("Alinhamento de Ranges:")
print(f"{'Par':<25} {'Simples':>10} {'Ponderada':>12} {'Diferença':>12}")
print("-" * 65)

for s1, s2 in test_cases:
    d_simple = normalized_levenshtein(s1, s2)
    d_weighted = weighted_levenshtein(s1, s2)
    diff = d_simple - d_weighted  # Positivo = ponderada é menor

    pair = s1 + "↔" + s2
    print(f"{pair:<25} {d_simple:>10.3f} {d_weighted:>12.3f} {diff:>12.3f}")

print("\n✅ Se Diferença ≈ 0.03-0.05, os ranges estão alinhados!")