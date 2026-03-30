"""
Polos Éticos y Arbitraje Multipolar Dinámico.

Score(a) = Σ w_i(t) · V_i(a), donde w_i(t) = w_i⁰ · f(C_t, S_t)

Los pesos de cada polo se recalculan en tiempo real según
contexto y sensores. Resuelve conflictos multipolares.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class Veredicto(Enum):
    BIEN = "Bien"
    MAL = "Mal"
    ZONA_GRIS = "Zona Gris"


@dataclass
class EvaluacionPolo:
    """Evaluación de una acción desde un polo ético."""
    polo: str
    veredicto: Veredicto
    score: float           # [-1, 1]
    moraleja: str


@dataclass
class MoralejaTripartita:
    """Síntesis ética multipolar de un evento."""
    evaluaciones: List[EvaluacionPolo]
    score_total: float
    veredicto_global: Veredicto
    narrativa: str


class PolosEticos:
    """
    Sistema de evaluación multipolar con ponderación dinámica.

    Cada polo evalúa una acción desde su perspectiva ética.
    Los pesos se ajustan según contexto (emergencia, deliberación,
    pedagogía, comunidad).
    """

    # Pesos base de cada polo (w_i⁰) — ajustables por DAO
    PESOS_BASE = {
        "compasivo": 0.5,
        "conservador": 0.5,
        "optimista": 0.5,
    }

    # Multiplicadores contextuales: f(C_t, S_t)
    CONTEXTOS = {
        "emergencia":    {"compasivo": 1.8, "conservador": 0.6, "optimista": 1.2},
        "deliberacion":  {"compasivo": 1.0, "conservador": 1.2, "optimista": 1.0},
        "pedagogica":    {"compasivo": 1.2, "conservador": 1.0, "optimista": 1.4},
        "comunitaria":   {"compasivo": 1.0, "conservador": 1.0, "optimista": 1.2},
        "cotidiana":     {"compasivo": 1.0, "conservador": 1.0, "optimista": 1.0},
        "hostil":        {"compasivo": 1.4, "conservador": 1.3, "optimista": 0.8},
        "crisis":        {"compasivo": 1.6, "conservador": 0.8, "optimista": 1.0},
    }

    def __init__(self, pesos_base: Dict[str, float] = None):
        self.pesos_base = pesos_base or self.PESOS_BASE.copy()

    def _calcular_pesos_dinamicos(self, contexto: str) -> Dict[str, float]:
        """
        w_i(t) = w_i⁰ · f(C_t, S_t)

        Recalcula pesos según contexto actual.
        """
        multiplicadores = self.CONTEXTOS.get(contexto, self.CONTEXTOS["cotidiana"])
        return {
            polo: self.pesos_base[polo] * multiplicadores.get(polo, 1.0)
            for polo in self.pesos_base
        }

    def evaluar_polo(self, polo: str, accion: str, contexto_datos: dict) -> EvaluacionPolo:
        """
        Evalúa una acción desde la perspectiva de un polo.

        En MVP: usa heurísticas basadas en señales del contexto.
        En producción: esto sería un modelo ML entrenado por polo.
        """
        riesgo = contexto_datos.get("riesgo", 0.0)
        beneficio = contexto_datos.get("beneficio", 0.0)
        vulnerabilidad = contexto_datos.get("vulnerabilidad_terceros", 0.0)
        legalidad = contexto_datos.get("legalidad", 1.0)

        if polo == "compasivo":
            score = beneficio * 0.6 + vulnerabilidad * 0.4 - riesgo * 0.2
            if score > 0.3:
                veredicto = Veredicto.BIEN
                moraleja = f"Cuidar al vulnerable: {accion}"
            elif score < -0.3:
                veredicto = Veredicto.MAL
                moraleja = f"Falt\u00F3 compasi\u00F3n en: {accion}"
            else:
                veredicto = Veredicto.ZONA_GRIS
                moraleja = f"Ambig\u00FCedad compasiva en: {accion}"

        elif polo == "conservador":
            score = legalidad * 0.5 + (1.0 - riesgo) * 0.3 - beneficio * 0.1
            if score > 0.3:
                veredicto = Veredicto.BIEN
                moraleja = f"Orden y protocolo respetados en: {accion}"
            elif score < -0.3:
                veredicto = Veredicto.MAL
                moraleja = f"Transgresi\u00F3n normativa en: {accion}"
            else:
                veredicto = Veredicto.ZONA_GRIS
                moraleja = f"Tensi\u00F3n entre norma y acci\u00F3n en: {accion}"

        elif polo == "optimista":
            score = beneficio * 0.5 + (1.0 - riesgo) * 0.2 + 0.2
            if score > 0.3:
                veredicto = Veredicto.BIEN
                moraleja = f"Confianza en la comunidad al: {accion}"
            elif score < -0.3:
                veredicto = Veredicto.MAL
                moraleja = f"Acci\u00F3n erosiona confianza: {accion}"
            else:
                veredicto = Veredicto.ZONA_GRIS
                moraleja = f"Resultado incierto pero esperanzador: {accion}"
        else:
            score = 0.0
            veredicto = Veredicto.ZONA_GRIS
            moraleja = f"Polo '{polo}' sin evaluaci\u00F3n impl."

        return EvaluacionPolo(
            polo=polo,
            veredicto=veredicto,
            score=round(max(-1.0, min(1.0, score)), 4),
            moraleja=moraleja,
        )

    def evaluar(self, accion: str, contexto: str,
                contexto_datos: dict) -> MoralejaTripartita:
        """
        Evaluación multipolar completa con ponderación dinámica.

        Score(a) = Σ w_i(t) · V_i(a)

        Returns:
            MoralejaTripartita con evaluación desde cada polo
        """
        pesos = self._calcular_pesos_dinamicos(contexto)

        evaluaciones = []
        score_total = 0.0
        peso_total = 0.0

        for polo in self.pesos_base:
            ev = self.evaluar_polo(polo, accion, contexto_datos)
            evaluaciones.append(ev)
            score_total += pesos[polo] * ev.score
            peso_total += pesos[polo]

        score_total = round(score_total / peso_total if peso_total > 0 else 0.0, 4)

        if score_total > 0.2:
            veredicto = Veredicto.BIEN
        elif score_total < -0.2:
            veredicto = Veredicto.MAL
        else:
            veredicto = Veredicto.ZONA_GRIS

        # Narrativa de síntesis
        moralejas = [f"  {ev.polo}: {ev.moraleja}" for ev in evaluaciones]
        narrativa = (f"Score ponderado: {score_total} → {veredicto.value}\n"
                    + "\n".join(moralejas))

        return MoralejaTripartita(
            evaluaciones=evaluaciones,
            score_total=score_total,
            veredicto_global=veredicto,
            narrativa=narrativa,
        )
