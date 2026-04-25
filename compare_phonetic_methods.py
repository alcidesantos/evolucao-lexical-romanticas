"""
Comparar diferentes métodos de distância fonética - Versão Limpa
"""
import sys
import io
from contextlib import contextmanager
from modules.asjp_loader import ASJPLoader

# Forçar encoding UTF-8 (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

@contextmanager
def suppress_output():
    """Suprime temporariamente output para stdout"""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout

def main():
    loader = ASJPLoader()

    # Carregar dados (permite output aqui)
    loader.load()

    print("=" * 70)
    print("🔍 COMPARAR MÉTODOS FONÉTICOS")
    print("=" * 70)

    # Pares de línguas para comparar
    pairs = [
        ('port1283', 'stan1288', 'Português', 'Espanhol'),
        ('port1283', 'mira1251', 'Português', 'Mirandês'),
        ('mira1251', 'astu1245', 'Mirandês', 'Asturiano'),
        ('port1283', 'stan1290', 'Português', 'Francês'),
    ]

    # Coletar resultados silenciosamente
    results = []

    for gc1, gc2, name1, name2 in pairs:
        # Método 1: Form + Levenshtein (silencioso)
        with suppress_output():
            dist1 = loader.get_lexical_distance(gc1, gc2, use_segments=False, use_panphon=False)

        # Método 2: Segments + Levenshtein (silencioso)
        with suppress_output():
            dist2 = loader.get_lexical_distance(gc1, gc2, use_segments=True, use_panphon=False)

        results.append({
            'pair': f"{name1} ↔ {name2}",
            'form_lev': dist1,
            'seg_lev': dist2
        })

    # Mostrar tabela limpa
    print("\n📊 Resultados por Método:\n")
    print(f"{'Par de Línguas':<35} {'Form+Lev':<12} {'Seg+Lev':<12}")
    print("-" * 60)

    for r in results:
        if r['form_lev'] and r['seg_lev']:
            print(f"{r['pair']:<35} {r['form_lev']:.3f}        {r['seg_lev']:.3f}")

    print("\n" + "=" * 70)
    print("💡 Interpretação:")
    print("   - Form+Lev: Transcrição compacta ASJP (41 símbolos)")
    print("   - Seg+Lev: Fonemas separados ✅ (método principal)")
    print("=" * 70)

if __name__ == "__main__":
    main()


