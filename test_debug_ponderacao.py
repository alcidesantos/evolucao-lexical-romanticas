"""Testar se as métricas estão normalizadas para [0, 1]"""

from modules.distance_calculator import normalized_levenshtein, weighted_levenshtein

# Testes com pares conhecidos
test_cases = [
    ("aqua", "aqua"),           # Idênticas → 0.0
    ("aqua", "agua"),           # 1 substituição → ~0.25
    ("pato", "gato"),           # 1 substituição → ~0.25
    ("casa", "zaza"),           # 2 substituições → ~0.50
    ("abcdefgh", "zyxwvuts"),   # Todas diferentes → ~1.0
]

print("Debug: Comparação de Métricas")
print("-" * 75)

for s1, s2 in test_cases:
    d_simple = normalized_levenshtein(s1, s2)
    d_weighted = weighted_levenshtein(s1, s2)
    diff = d_weighted - d_simple

    status = "✅" if diff < 0 else "⚠️"

    # ✅ CORREÇÃO: Criar variável intermédia para o par
    pair = f"{s1}↔{s2}"
    print(f"{pair:<25} {d_simple:>10.3f} {d_weighted:>12.3f} {diff:>12.3f} {status}")

print("\n✅ Teste concluído!")