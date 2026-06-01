"""Verificar qual factor está a ser usado"""

from modules.distance_calculator import normalized_levenshtein, weighted_levenshtein

# Par de teste conhecido
s1, s2 = "pato", "gato"

d_simple = normalized_levenshtein(s1, s2)
d_weighted = weighted_levenshtein(s1, s2)
ratio = d_weighted / d_simple if d_simple > 0 else 1.0

print(f"{s1}↔{s2}: Simples={d_simple:.3f}, Ponderada={d_weighted:.3f}, Ratio={ratio:.2f}x")

if 0.80 <= ratio <= 0.90:
    print("✅ Factor correcto (~5.5)")
elif ratio < 0.70:
    print("⚠️ Factor demasiado alto (>8.0)")
else:
    print("⚠️ Factor demasiado baixo (<4.0)")