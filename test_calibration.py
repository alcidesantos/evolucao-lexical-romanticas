"""Testar calibração com factor=5.5"""

from modules.distance_calculator import normalized_levenshtein, weighted_levenshtein

# Pares reais do teu corpus (Latim → Românicas)
test_cases = [
    ("aqua", "'agwɐ"),  # água
    ("portu", "pɔɾtu"),  # porto
    ("kasa", "kaza"),  # casa
    ("pato", "pato"),  # idêntica
    ("ignis", "fɔgu"),  # fogo (mudança grande)
]

print("Calibração: Factor=5.5")
print(f"{'Par':<25} {'Simples':>10} {'Ponderada':>12} {'Ratio':>8} {'OK?':>6}")
print("-" * 65)

for s1, s2 in test_cases:
    d_simple = normalized_levenshtein(s1, s2)
    d_weighted = weighted_levenshtein(s1, s2)

    if d_simple > 0:
        ratio = d_weighted / d_simple
    else:
        ratio = 1.0 if d_weighted == 0 else float('inf')

    # Para mudanças pequenas, queremos ratio < 1.0; para grandes, pode ser ~1.0
    ok = "✅" if (d_simple < 0.5 and ratio < 1.0) or (d_simple >= 0.5) else "⚠️"

    pair = s1 + "↔" + s2
    print(f"{pair:<25} {d_simple:>10.3f} {d_weighted:>12.3f} {ratio:>8.2f}x {ok:>6}")