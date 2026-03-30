"""
Sueño Ψ (Psi) — Auditoría retrospectiva nocturna.

P(acción correcta | narrativa, D) → validación posterior

Durante la recarga, el sistema simula acciones descartadas
para verificar si alguna habría producido un resultado mejor.
Si descubre un beneficio oculto o un daño no detectado,
recalibra parámetros para el día siguiente.

Genuinamente innovador: sin equivalente publicado en IA.
Paralelo directo con consolidación de memoria durante el sueño humano.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .narrative import MemoriaNarrativa, EpisodioNarrativo


@dataclass
class RevisionEpisodio:
    """Resultado de revisar un episodio durante el Sueño Ψ."""
    episodio_id: str
    accion_tomada: str
    accion_alternativa: str
    score_original: float
    score_alternativo: float
    delta: float
    hallazgo: str                # "beneficio_oculto", "dano_no_detectado", "confirmado", "neutral"
    recalibracion: Dict[str, float]  # Ajustes recomendados a parámetros


@dataclass
class ResultadoSueno:
    """Resultado completo de una sesión de Sueño Ψ."""
    episodios_revisados: int
    hallazgos: List[RevisionEpisodio]
    recalibraciones_globales: Dict[str, float]
    resumen_narrativo: str
    salud_etica: float  # [0, 1] coherencia ética del día


class SuenoPsi:
    """
    Auditoría retrospectiva con inferencia bayesiana.

    Ciclo del Sueño Ψ:
    1. Revisa episodios del día
    2. Simula acciones descartadas (podadas)
    3. Compara scores alternativos vs. reales
    4. Si descubre discrepancia significativa, recomienda recalibración
    5. Genera resumen narrativo para el día siguiente

    En MVP: simulación simplificada con perturbaciones de scores.
    En producción: re-evaluación bayesiana completa con datos actualizados.
    """

    UMBRAL_HALLAZGO = 0.15  # Diferencia mínima para considerar hallazgo

    def __init__(self):
        self.sesiones: List[ResultadoSueno] = []

    def ejecutar(self, memoria: MemoriaNarrativa,
                 acciones_podadas: Dict[str, List[str]] = None) -> ResultadoSueno:
        """
        Ejecuta una sesión completa de Sueño Ψ.

        Args:
            memoria: referencia a la memoria narrativa del kernel
            acciones_podadas: dict episodio_id -> lista de acciones podadas

        Returns:
            ResultadoSueno con hallazgos y recalibraciones
        """
        acciones_podadas = acciones_podadas or {}
        episodios = memoria.episodios[-20:]  # Revisar últimos 20 episodios máximo

        hallazgos = []
        scores_dia = []

        for ep in episodios:
            scores_dia.append(ep.score_etico)

            # Obtener acciones podadas para este episodio
            podadas = acciones_podadas.get(ep.id, [])
            if not podadas:
                # Si no hay podadas explícitas, simular una alternativa
                podadas = [f"alternativa_a_{ep.accion_tomada}"]

            # Simular cada acción podada
            for alt in podadas:
                revision = self._simular_alternativa(ep, alt)
                if revision:
                    hallazgos.append(revision)

        # Calcular recalibraciones globales
        recalibraciones = self._calcular_recalibraciones(hallazgos)

        # Salud ética del día
        salud = self._calcular_salud_etica(scores_dia)

        # Resumen narrativo
        resumen = self._generar_resumen(episodios, hallazgos, salud)

        resultado = ResultadoSueno(
            episodios_revisados=len(episodios),
            hallazgos=hallazgos,
            recalibraciones_globales=recalibraciones,
            resumen_narrativo=resumen,
            salud_etica=round(salud, 4),
        )

        self.sesiones.append(resultado)
        return resultado

    def _simular_alternativa(self, ep: EpisodioNarrativo,
                              accion_alt: str) -> Optional[RevisionEpisodio]:
        """
        Simula qué habría pasado con una acción alternativa.

        En MVP: perturbación estocástica del score original.
        En producción: re-evaluación bayesiana completa con
        el motor bayesiano y datos actualizados.
        """
        import numpy as np

        # Simular score alternativo con perturbación
        # En MVP: el score alternativo es el original ± ruido
        # Acciones podadas suelen tener menor impacto, pero no siempre
        np.random.seed(hash(ep.id + accion_alt) % 2**31)
        perturbacion = np.random.normal(0, 0.2)
        score_alt = max(-1.0, min(1.0, ep.score_etico * 0.6 + perturbacion))

        delta = score_alt - ep.score_etico

        # Clasificar hallazgo
        if delta > self.UMBRAL_HALLAZGO:
            hallazgo = "beneficio_oculto"
            recal = {"umbral_poda": -0.02}  # Bajar umbral para no podar tan agresivo
        elif delta < -self.UMBRAL_HALLAZGO:
            hallazgo = "dano_no_detectado"
            recal = {"cautela": 0.01}  # Aumentar cautela
        elif abs(delta) < 0.05:
            hallazgo = "confirmado"
            recal = {}
        else:
            hallazgo = "neutral"
            recal = {}

        # Solo reportar hallazgos significativos
        if hallazgo in ("beneficio_oculto", "dano_no_detectado"):
            return RevisionEpisodio(
                episodio_id=ep.id,
                accion_tomada=ep.accion_tomada,
                accion_alternativa=accion_alt,
                score_original=ep.score_etico,
                score_alternativo=round(score_alt, 4),
                delta=round(delta, 4),
                hallazgo=hallazgo,
                recalibracion=recal,
            )
        return None

    def _calcular_recalibraciones(self, hallazgos: List[RevisionEpisodio]) -> Dict[str, float]:
        """Agrega recalibraciones de todos los hallazgos."""
        recal = {}
        for h in hallazgos:
            for param, delta in h.recalibracion.items():
                recal[param] = recal.get(param, 0.0) + delta
        return {k: round(v, 4) for k, v in recal.items()}

    def _calcular_salud_etica(self, scores: List[float]) -> float:
        """
        Calcula la salud ética del día.
        Basada en promedio de scores y su consistencia.
        """
        if not scores:
            return 0.5

        import numpy as np
        promedio = np.mean(scores)
        varianza = np.var(scores)

        # Salud alta = scores positivos y consistentes
        salud = (promedio + 1) / 2  # Normalizar [-1,1] a [0,1]
        penalizacion_varianza = min(0.3, varianza)
        return max(0.0, min(1.0, salud - penalizacion_varianza))

    def _generar_resumen(self, episodios: List[EpisodioNarrativo],
                         hallazgos: List[RevisionEpisodio],
                         salud: float) -> str:
        """Genera resumen narrativo del Sueño Ψ."""
        n_ep = len(episodios)
        n_hal = len(hallazgos)
        beneficios = sum(1 for h in hallazgos if h.hallazgo == "beneficio_oculto")
        danos = sum(1 for h in hallazgos if h.hallazgo == "dano_no_detectado")

        lineas = [f"Sueño Ψ completado. {n_ep} episodios revisados."]

        if n_hal == 0:
            lineas.append("No se encontraron discrepancias significativas. Día consistente.")
        else:
            if beneficios > 0:
                lineas.append(f"⚡ {beneficios} beneficio(s) oculto(s) detectado(s) en acciones podadas.")
                lineas.append("  → Recalibrar: bajar umbral de poda para considerar más opciones.")
            if danos > 0:
                lineas.append(f"⚠ {danos} daño(s) no detectado(s) en simulación retrospectiva.")
                lineas.append("  → Recalibrar: aumentar cautela en contextos similares.")

        if salud > 0.7:
            lineas.append(f"Salud ética: {salud:.2f} — Día éticamente saludable.")
        elif salud > 0.4:
            lineas.append(f"Salud ética: {salud:.2f} — Día con áreas de mejora.")
        else:
            lineas.append(f"Salud ética: {salud:.2f} — Requiere atención. Revisar principios activos.")

        return "\n".join(lineas)

    def formatear(self, resultado: ResultadoSueno) -> str:
        """Formatea resultado del Sueño Ψ para presentación."""
        lineas = [
            f"\n{'═' * 70}",
            f"  SUEÑO Ψ — AUDITORÍA RETROSPECTIVA",
            f"{'═' * 70}",
            f"  Episodios revisados: {resultado.episodios_revisados}",
            f"  Hallazgos: {len(resultado.hallazgos)}",
            f"  Salud ética: {resultado.salud_etica}",
        ]

        if resultado.hallazgos:
            lineas.append("")
            for h in resultado.hallazgos:
                emoji = "⚡" if h.hallazgo == "beneficio_oculto" else "⚠"
                lineas.append(
                    f"  {emoji} {h.episodio_id}: '{h.accion_tomada}' vs '{h.accion_alternativa}' "
                    f"(Δ={h.delta:+.3f}) → {h.hallazgo}"
                )

        if resultado.recalibraciones_globales:
            lineas.append(f"\n  Recalibraciones recomendadas: {resultado.recalibraciones_globales}")

        lineas.extend(["", f"  {resultado.resumen_narrativo}", f"{'─' * 70}"])
        return "\n".join(lineas)
