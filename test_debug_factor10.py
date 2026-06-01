"""Testar se as métricas estão normalizadas para [0, 1]"""

from modules.distance_calculator import normalized_levenshtein, weighted_levenshtein

test_cases = [
    ("aqua", "agua"),
    ("pato", "gato"),
    ("casa", "zaza"),
]

print("Teste com Factor=10.0:")
print("-" * 45)

for s1, s2 in test_cases:
    d_simple = normalized_levenshtein(s1, s2)
    d_weighted = weighted_levenshtein(s1, s2)
    ok = "✅" if d_weighted < d_simple else "❌"

    # ✅ CORREÇÃO: Criar variável separada PRIMEIRO
    pair = s1 + " <-> " + s2

    # ✅ DEPOIS formatar a variável
    print(pair.ljust(20) + str(round(d_simple, 3)).rjust(10) + str(round(d_weighted, 3)).rjust(12) + ok.rjust(8))