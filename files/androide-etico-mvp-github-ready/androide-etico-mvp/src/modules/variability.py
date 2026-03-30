"""
Variabilidad Bayesiana — Ruido controlado para naturalidad.

Introduce variabilidad estocástica en las evaluaciones para que
el androide no produzca resultados idénticos cada vez, manteniendo
consistencia ética (la acción elegida es robusta, los scores varían).

Principio: un humano que siempre ayudaría al anciano pero con
diferente nivel de urgencia según cómo se sienta ese día.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfigVariabilidad:
    """Configuración del ruido bayesiano."""
    ruido_impacto: float = 0.05    # σ del ruido en impacto estimado
    ruido_confianza: float = 0.03  # σ del ruido en confianza
    ruido_sigma: float = 0.02     # σ del ruido en simpático-parasimpático
    ruido_polos: float = 0.04     # σ del ruido en pesos de polos
    seed: Optional[int] = None    # None = aleatorio real, int = reproducible


class MotorVariabilidad:
    """
    Inyecta variabilidad bayesiana controlada en el kernel.

    La variabilidad se aplica DESPUÉS de la evaluación determinista,
    perturbando scores pero no alterando la lógica de decisión.

    Propiedad clave: la variabilidad debe ser suficiente para que
    dos ejecuciones del mismo escenario produzcan scores diferentes,
    pero NO suficiente para que cambien la acción elegida en la
    mayoría de los casos (>95%).

    Esto se verifica con los tests formales.
    """

    def __init__(self, config: ConfigVariabilidad = None):
        self.config = config or ConfigVariabilidad()
        self.rng = np.random.default_rng(self.config.seed)
        self._activo = True

    def activar(self):
        """Activa la variabilidad (por defecto está activa)."""
        self._activo = True

    def desactivar(self):
        """Desactiva para tests deterministas."""
        self._activo = False

    def perturbar_impacto(self, impacto: float) -> float:
        """Perturba el impacto estimado de una acción."""
        if not self._activo:
            return impacto
        ruido = self.rng.normal(0, self.config.ruido_impacto)
        return float(np.clip(impacto + ruido, -1.0, 1.0))

    def perturbar_confianza(self, confianza: float) -> float:
        """Perturba el nivel de confianza."""
        if not self._activo:
            return confianza
        ruido = self.rng.normal(0, self.config.ruido_confianza)
        return float(np.clip(confianza + ruido, 0.05, 1.0))

    def perturbar_sigma(self, sigma: float) -> float:
        """Perturba el estado simpático-parasimpático."""
        if not self._activo:
            return sigma
        ruido = self.rng.normal(0, self.config.ruido_sigma)
        return float(np.clip(sigma + ruido, 0.2, 0.8))

    def perturbar_peso_polo(self, peso: float) -> float:
        """Perturba el peso de un polo ético."""
        if not self._activo:
            return peso
        ruido = self.rng.normal(0, self.config.ruido_polos)
        return float(np.clip(peso + ruido, 0.3, 0.9))

    def reset_seed(self, seed: int = None):
        """Reinicia el generador con nueva semilla."""
        self.rng = np.random.default_rng(seed)
