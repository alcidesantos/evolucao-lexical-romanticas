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

print("Teste de Normalização:")
print("-" * 55)

for s1, s2 in test_cases:
    d_simple = normalized_levenshtein(s1, s2)
    d_weighted = weighted_levenshtein(s1, s2)

    # Verificar se estão em [0, 1]
    assert 0.0 <= d_simple <= 1.0, f"Simples fora de [0,1]: {d_simple}"
    assert 0.0 <= d_weighted <= 1.0, f"Ponderada fora de [0,1]: {d_weighted}"

    # ✅ CORREÇÃO: Criar string separada para formatar
    pair = f"{s1} ↔ {s2}"
    print(f"{pair:<30} {d_simple:>10.3f} {d_weighted:>12.3f}")

print("\n✅ Todas as distâncias estão normalizadas para [0.0, 1.0]!")