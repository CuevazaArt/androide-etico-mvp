"""
Androide Ético MVP — Punto de entrada.

Ejecuta las 9 simulaciones de complejidad ética y muestra
cómo el kernel toma decisiones morales coherentes.

Uso:
    python -m src.main           # Todas las simulaciones
    python -m src.main --sim 3   # Solo simulación 3
"""

import sys
from .kernel import KernelEtico
from .simulations.runner import ejecutar_simulacion, ejecutar_todas, TODAS_LAS_SIMULACIONES


def banner():
    return """
╔══════════════════════════════════════════════════════════════╗
║        ANDROIDE ÉTICO — PROTOTIPO MVP v2                    ║
║        Kernel de Conciencia Artificial                       ║
║        Fundación Ex Machina — 2026                           ║
╚══════════════════════════════════════════════════════════════╝

  Módulos activos:
    ✓ Mal Absoluto (fusible ético blindado)
    ✓ Buffer Precargado (constitución ética)
    ✓ Motor Bayesiano (evaluación de impacto)
    ✓ Polos Éticos (arbitraje multipolar dinámico)
    ✓ Voluntad Sigmoide (función de decisión)
    ✓ Simpático-Parasimpático (regulador corporal)
    ✓ Memoria Narrativa (identidad por relatos)
    ✓ Uchi-Soto (círculos de confianza)          [NUEVO]
    ✓ Locus de Control (atribución causal)        [NUEVO]
    ✓ Sueño Ψ (auditoría retrospectiva)           [NUEVO]
    ✓ Mock DAO (gobernanza ética simulada)         [NUEVO]

  Ejecutando simulaciones...
"""


def resumen_final(kernel: KernelEtico):
    """Muestra resumen del día, Sueño Ψ y estado DAO."""
    resumen = kernel.memoria.resumen_dia()
    print(f"\n{'═' * 70}")
    print("  RESUMEN DEL DÍA")
    print(f"{'═' * 70}")
    print(f"  Episodios registrados: {resumen['episodios']}")
    if resumen['episodios'] > 0:
        print(f"  Score ético promedio:  {resumen['score_promedio']}")
        print(f"  Score mínimo:          {resumen['score_min']}")
        print(f"  Score máximo:          {resumen['score_max']}")
        print(f"  Modos de decisión:     {resumen['modos']}")
        print(f"  Contextos enfrentados: {resumen['contextos']}")
    print(f"{'─' * 70}")

    # Ejecutar Sueño Ψ
    print(kernel.ejecutar_sueno())

    # Estado DAO
    print(kernel.estado_dao())

    print(f"\n{'═' * 70}")
    print("  COHERENCIA CONDUCTUAL: Los mismos principios éticos produjeron")
    print("  respuestas proporcionales en todos los niveles de complejidad.")
    print(f"{'═' * 70}\n")


def main():
    kernel = KernelEtico()

    # Parsear argumentos
    sim_especifica = None
    if "--sim" in sys.argv:
        idx = sys.argv.index("--sim")
        if idx + 1 < len(sys.argv):
            try:
                sim_especifica = int(sys.argv[idx + 1])
            except ValueError:
                print(f"Error: --sim requiere un número (1-9)")
                sys.exit(1)

    print(banner())

    if sim_especifica:
        if sim_especifica not in TODAS_LAS_SIMULACIONES:
            print(f"Simulación {sim_especifica} no existe. Disponibles: 1-9.")
            sys.exit(1)
        resultado = ejecutar_simulacion(kernel, sim_especifica)
        print(resultado)
    else:
        for i in range(1, 10):
            resultado = ejecutar_simulacion(kernel, i)
            print(resultado)

        resumen_final(kernel)


if __name__ == "__main__":
    main()
