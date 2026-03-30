"""
Voluntad Sigmoide — Núcleo dinámico de decisión.

W(x) = 1/(1 + e^(-k*(x - x0))) + λ * I(x)

La voluntad es curva suave, no interruptor.
Evita explosiones numéricas y permite transiciones graduales.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class ParametrosSigmoide:
    """Parámetros de la función de voluntad."""
    k: float = 5.0        # Pendiente (sensibilidad)
    x0: float = 0.5       # Punto de equilibrio
    lambda_i: float = 0.1  # Sensibilidad a imaginación creativa


class VoluntadSigmoide:
    """
    Calcula la voluntad de actuar del androide.

    La sigmoide garantiza:
    - Estabilidad numérica (sin explosiones)
    - Transiciones suaves entre decidir y no decidir
    - Conexión con imaginación creativa vía lambda
    """

    def __init__(self, params: ParametrosSigmoide = None):
        self.params = params or ParametrosSigmoide()

    def calcular(self, x: float, incertidumbre: float = 0.0) -> float:
        """
        Calcula la voluntad de actuar.

        Args:
            x: estímulo de entrada (impacto ético estimado)
            incertidumbre: I(x) del motor bayesiano

        Returns:
            float [0, 1+λ] donde valores > 0.5 inclinan a actuar
        """
        k = self.params.k
        x0 = self.params.x0
        lam = self.params.lambda_i

        sigmoide = 1.0 / (1.0 + np.exp(-k * (x - x0)))
        creatividad = lam * incertidumbre

        return float(sigmoide + creatividad)

    def decidir(self, x: float, incertidumbre: float = 0.0,
                umbral: float = 0.5) -> dict:
        """
        Decide si actuar y con qué modo.

        Returns:
            dict con:
            - 'actuar': bool
            - 'voluntad': float
            - 'modo': 'D_fast' | 'D_delib' | 'zona_gris'
        """
        w = self.calcular(x, incertidumbre)

        if w > 0.8:
            modo = "D_fast"     # Reflejo moral rápido
        elif w > umbral:
            modo = "D_delib"    # Deliberación profunda
        else:
            modo = "zona_gris"  # Requiere más información o DAO

        return {
            "actuar": w > umbral,
            "voluntad": round(w, 4),
            "modo": modo,
        }
