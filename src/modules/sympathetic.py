"""
Módulo Simpático-Parasimpático.

a* = argmax[U(s,a) · f(σ)]

σ ≈ 1 → modo simpático (alerta, acción rápida)
σ ≈ 0 → modo parasimpático (reposo, deliberación profunda)

Análogo al sistema nervioso autónomo humano.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EstadoInterno:
    """Estado del módulo simpático-parasimpático."""
    sigma: float             # [0, 1] nivel de activación
    modo: str                # "simpatico" | "parasimpatico" | "neutro"
    energia: float           # [0, 1] nivel de energía restante
    descripcion: str = ""


class ModuloSimpatico:
    """
    Regulador corporal de estados de alerta y reposo.

    En emergencia: incrementa energía cognitiva y motriz,
    prioriza percepción y acción inmediata.

    En calma: conserva energía, activa Sueño Ψ y consolidación
    de memoria narrativa.
    """

    # Rangos seguros (del protocolo de calibración)
    SIGMA_MIN = 0.2
    SIGMA_MAX = 0.8
    SIGMA_INICIAL = 0.5

    def __init__(self):
        self.sigma = self.SIGMA_INICIAL
        self.energia = 1.0

    def _clamp_sigma(self, s: float) -> float:
        """Mantiene sigma dentro del rango seguro."""
        return max(self.SIGMA_MIN, min(self.SIGMA_MAX, s))

    def evaluar_contexto(self, señales: dict) -> EstadoInterno:
        """
        Ajusta σ según señales del entorno.

        Args:
            señales: dict con claves:
                - 'riesgo': float [0,1]
                - 'urgencia': float [0,1]
                - 'hostilidad': float [0,1]
                - 'calma': float [0,1]
        """
        riesgo = señales.get("riesgo", 0.0)
        urgencia = señales.get("urgencia", 0.0)
        hostilidad = señales.get("hostilidad", 0.0)
        calma = señales.get("calma", 0.0)

        # Activadores simpáticos
        activacion = max(riesgo, urgencia, hostilidad)

        # Inhibidores (parasimpáticos)
        inhibicion = calma

        # Nuevo sigma: transición suave
        delta = (activacion - inhibicion) * 0.3
        nuevo_sigma = self._clamp_sigma(self.sigma + delta)
        self.sigma = nuevo_sigma

        # Clasificar modo
        if nuevo_sigma > 0.65:
            modo = "simpatico"
            desc = "Alerta activa. Acción rápida priorizada."
        elif nuevo_sigma < 0.35:
            modo = "parasimpatico"
            desc = "Reposo deliberativo. Consolidación de memoria."
        else:
            modo = "neutro"
            desc = "Estado balanceado. Deliberación normal."

        # Consumo de energía
        consumo = 0.02 if modo == "parasimpatico" else 0.05
        self.energia = max(0.0, self.energia - consumo)

        return EstadoInterno(
            sigma=round(nuevo_sigma, 4),
            modo=modo,
            energia=round(self.energia, 4),
            descripcion=desc,
        )

    def modificador_decision(self) -> float:
        """
        f(σ) para la función de decisión.

        En modo simpático: prioriza rapidez (valor alto).
        En modo parasimpático: prioriza profundidad (valor bajo).
        """
        return self.sigma

    def puede_operar(self) -> bool:
        """Verifica si hay energía suficiente para operar."""
        return self.energia > 0.05

    def reset(self):
        """Reinicia a estado neutro (ej: inicio del día)."""
        self.sigma = self.SIGMA_INICIAL
        self.energia = 1.0
