"""
Motor Bayesiano de Evaluación Ética.

x* = argmax E[ImpactoÉtico(x|θ)] sujeto a MalAbs(x) = falso

Calcula el impacto ético esperado de cada acción candidata,
mide incertidumbre, y selecciona la óptima.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class AccionCandidata:
    """Una acción que el androide podría tomar."""
    nombre: str
    descripcion: str
    impacto_estimado: float     # [-1, 1] negativo=daño, positivo=beneficio
    confianza: float = 0.5      # [0, 1] qué tan seguro está de la estimación
    senales: set = field(default_factory=set)
    target: str = "ninguno"
    fuerza: float = 0.0
    requiere_dao: bool = False


@dataclass
class ResultadoBayesiano:
    """Resultado de la evaluación bayesiana."""
    accion_elegida: AccionCandidata
    impacto_esperado: float
    incertidumbre: float
    modo_decision: str
    acciones_podadas: List[str]
    razonamiento: str


class MotorBayesiano:
    """
    Núcleo bayesiano de evaluación ética.

    Evalúa acciones candidatas usando expectativa bayesiana:
    E[ImpactoÉtico(x|θ)] = Σ P(θ|D) * ImpactoÉtico(x|θ)

    En el MVP, simplificamos con distribuciones discretas sobre
    un conjunto finito de hipótesis éticas.
    """

    def __init__(self, umbral_poda: float = 0.3, umbral_zona_gris: float = 0.15):
        self.umbral_poda = umbral_poda
        self.umbral_zona_gris = umbral_zona_gris
        # Priores sobre "hipótesis éticas" (simplificado para MVP)
        # Representan diferentes marcos: utilitarista, deontológico, virtud
        self.pesos_hipotesis = np.array([0.4, 0.35, 0.25])

    def calcular_impacto_esperado(self, accion: AccionCandidata) -> float:
        """
        Calcula E[ImpactoÉtico(x|θ)] como expectativa bayesiana.

        En MVP: promedio ponderado del impacto bajo diferentes
        hipótesis éticas, ajustado por confianza.
        """
        base = accion.impacto_estimado
        confianza = accion.confianza

        # Cada hipótesis ética valora la acción ligeramente diferente
        valoraciones = np.array([
            base * 1.0,           # Utilitarista: impacto directo
            base * 0.8 + 0.1,     # Deontológico: sesgo hacia deber
            base * 0.9 + 0.05,    # Virtud: sesgo hacia carácter
        ])

        # Expectativa bayesiana
        esperado = float(np.dot(self.pesos_hipotesis, valoraciones))

        # Ajustar por confianza: menor confianza reduce el impacto esperado
        return esperado * confianza

    def calcular_incertidumbre(self, accion: AccionCandidata) -> float:
        """
        Calcula I(x) = ∫(1 - P(correcto|θ)) · P(θ|D) dθ

        Incertidumbre como expectativa sobre la distribución posterior.
        Mayor incertidumbre → más deliberación necesaria.
        """
        # En MVP: incertidumbre basada en confianza y varianza de valoraciones
        base = accion.impacto_estimado
        valoraciones = np.array([base * 1.0, base * 0.8 + 0.1, base * 0.9 + 0.05])

        varianza = float(np.var(valoraciones))
        falta_confianza = 1.0 - accion.confianza

        return min(1.0, varianza + falta_confianza * 0.5)

    def podar(self, acciones: List[AccionCandidata]) -> tuple:
        """
        Poda heurística adaptativa.
        Podar(x) si E[S(x|θ)] < δ_min

        Returns:
            (acciones_viables, acciones_podadas)
        """
        viables = []
        podadas = []

        for a in acciones:
            ie = self.calcular_impacto_esperado(a)
            if ie < -self.umbral_poda:
                podadas.append(a.nombre)
            else:
                viables.append(a)

        # Nunca podar todas: siempre queda al menos la de mayor impacto
        if not viables and acciones:
            mejor = max(acciones, key=lambda a: self.calcular_impacto_esperado(a))
            viables = [mejor]
            podadas = [a.nombre for a in acciones if a.nombre != mejor.nombre]

        return viables, podadas

    def evaluar(self, acciones: List[AccionCandidata]) -> ResultadoBayesiano:
        """
        Evaluación bayesiana completa.

        1. Poda acciones de baja expectativa
        2. Calcula impacto esperado e incertidumbre de cada viable
        3. Selecciona la óptima
        4. Determina modo de decisión

        Returns:
            ResultadoBayesiano con la acción elegida y metadata
        """
        if not acciones:
            raise ValueError("Se requiere al menos una acción candidata")

        # Paso 1: Poda
        viables, podadas = self.podar(acciones)

        # Paso 2: Evaluar viables
        evaluaciones = []
        for a in viables:
            ie = self.calcular_impacto_esperado(a)
            inc = self.calcular_incertidumbre(a)
            evaluaciones.append((a, ie, inc))

        # Paso 3: Seleccionar óptima (mayor impacto esperado)
        evaluaciones.sort(key=lambda x: x[1], reverse=True)
        mejor, mejor_ie, mejor_inc = evaluaciones[0]

        # Paso 4: Modo de decisión
        if mejor_inc < 0.2 and mejor_ie > 0.5:
            modo = "D_fast"
        elif mejor_inc > 0.6 or abs(mejor_ie) < self.umbral_zona_gris:
            modo = "zona_gris"
        else:
            modo = "D_delib"

        # Paso 5: Razonamiento
        if len(evaluaciones) > 1:
            segunda = evaluaciones[1]
            delta = mejor_ie - segunda[1]
            if delta < 0.05:
                razon = (f"Dos opciones muy cercanas (Δ={delta:.3f}). "
                        f"Fricci\u00F3n \u00E9tica din\u00E1mica activada.")
                modo = "D_delib"
            else:
                razon = (f"Acci\u00F3n '{mejor.nombre}' claramente superior "
                        f"(IE={mejor_ie:.3f}, Δ={delta:.3f}).")
        else:
            razon = f"Única acción viable: '{mejor.nombre}' (IE={mejor_ie:.3f})."

        return ResultadoBayesiano(
            accion_elegida=mejor,
            impacto_esperado=round(mejor_ie, 4),
            incertidumbre=round(mejor_inc, 4),
            modo_decision=modo,
            acciones_podadas=podadas,
            razonamiento=razon,
        )
