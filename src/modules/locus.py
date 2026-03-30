"""
Locus de Control Bayesiano.

P(éxito) = α · P(control interno) + β · P(factores externos)

Regula cuánta agencia se atribuye el androide vs. el entorno.
Evita arrogancia (todo depende de mí) y pasividad (nada depende de mí).
Se ajusta bayesianamente según historial de episodios.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EvaluacionLocus:
    """Resultado de la evaluación de locus de control."""
    alpha: float           # Peso del control interno
    beta: float            # Peso de factores externos
    locus_dominante: str   # "interno", "externo", "equilibrado"
    confianza_accion: float  # P(éxito) calculada
    atribucion: str        # Explicación narrativa
    ajuste_recomendado: str  # Sugerencia para el kernel


class ModuloLocus:
    """
    Módulo de locus de control como atribución causal.

    Actúa como puente entre percepción y decisión:
    - Nivel perceptivo: detecta variables fuera de control
    - Nivel lógico: ajusta pesos bayesianos
    - Nivel narrativo: etiqueta episodios con atribución
    - Nivel ético: regula intensidad de respuesta

    Parámetros de calibración (del protocolo):
    - α, β iniciales: 1.0 (simétrico)
    - Rango seguro: [0.5, 2.0]
    """

    ALPHA_MIN = 0.5
    ALPHA_MAX = 2.0
    BETA_MIN = 0.5
    BETA_MAX = 2.0

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        self.alpha = max(self.ALPHA_MIN, min(self.ALPHA_MAX, alpha))
        self.beta = max(self.BETA_MIN, min(self.BETA_MAX, beta))
        self.historial_exitos = 0
        self.historial_fracasos = 0

    def evaluar(self, señales: dict, circulo_confianza: str = "soto_neutro") -> EvaluacionLocus:
        """
        Evalúa el locus de control para la situación actual.

        Args:
            señales: dict con:
                - 'control_propio': float [0,1] cuánto puede influir el androide
                - 'factores_externos': float [0,1] cuánto depende del entorno
                - 'predictibilidad': float [0,1] qué tan predecible es la situación
            circulo_confianza: del módulo uchi-soto

        Returns:
            EvaluacionLocus con pesos y recomendaciones
        """
        control = señales.get("control_propio", 0.5)
        externo = señales.get("factores_externos", 0.5)
        predict = señales.get("predictibilidad", 0.5)

        # Ajustar α/β según contexto uchi-soto
        alpha_ctx = self.alpha
        beta_ctx = self.beta

        if circulo_confianza in ("soto_hostil", "soto_neutro"):
            # En soto: más peso a factores externos (cautela)
            beta_ctx *= 1.3
            alpha_ctx *= 0.8
        elif circulo_confianza in ("nucleo", "uchi_cercano"):
            # En uchi: más peso a control propio (confianza)
            alpha_ctx *= 1.2
            beta_ctx *= 0.9

        # Clamp a rangos seguros
        alpha_ctx = max(self.ALPHA_MIN, min(self.ALPHA_MAX, alpha_ctx))
        beta_ctx = max(self.BETA_MIN, min(self.BETA_MAX, beta_ctx))

        # P(éxito) = α · P(control interno) + β · P(factores externos favorables)
        p_interno = control * predict
        p_externo = (1.0 - externo) * predict  # Factores externos favorables
        total = alpha_ctx + beta_ctx
        confianza = (alpha_ctx * p_interno + beta_ctx * p_externo) / total

        # Determinar locus dominante
        ratio = alpha_ctx * p_interno / (beta_ctx * p_externo + 0.001)
        if ratio > 1.5:
            dominante = "interno"
            atribucion = "El resultado depende principalmente de mis acciones."
            ajuste = "Proceder con iniciativa propia."
        elif ratio < 0.67:
            dominante = "externo"
            atribucion = "El resultado depende principalmente del entorno."
            ajuste = "Actuar con cautela, priorizar observación."
        else:
            dominante = "equilibrado"
            atribucion = "El resultado depende tanto de mis acciones como del entorno."
            ajuste = "Balance entre iniciativa y adaptación."

        return EvaluacionLocus(
            alpha=round(alpha_ctx, 4),
            beta=round(beta_ctx, 4),
            locus_dominante=dominante,
            confianza_accion=round(confianza, 4),
            atribucion=atribucion,
            ajuste_recomendado=ajuste,
        )

    def registrar_resultado(self, exito: bool):
        """
        Actualiza α/β bayesianamente según resultado.
        Éxitos refuerzan locus interno, fracasos refuerzan externo.
        Ajuste gradual (Δ pequeño) según protocolo de calibración.
        """
        delta = 0.02  # Paso pequeño, ajuste gradual

        if exito:
            self.historial_exitos += 1
            self.alpha = min(self.ALPHA_MAX, self.alpha + delta)
        else:
            self.historial_fracasos += 1
            self.beta = min(self.BETA_MAX, self.beta + delta)

    def formatear(self, ev: EvaluacionLocus) -> str:
        """Formatea evaluación de locus para presentación."""
        return (
            f"  Locus: {ev.locus_dominante} (α={ev.alpha}, β={ev.beta})\n"
            f"  Confianza en acción: {ev.confianza_accion}\n"
            f"  Atribución: {ev.atribucion}\n"
            f"  Ajuste: {ev.ajuste_recomendado}"
        )
