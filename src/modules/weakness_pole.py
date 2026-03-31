"""
Polo de Debilidad — Vulnerabilidades narrativas intencionales.

No se programa el mal, se programa la imperfección humanizante.
Un androide que registra "la acción fue correcta pero me dejó
incomodidad" es más creíble que uno siempre óptimo.

Polos disponibles: quejumbroso, indeciso, ansioso, distraído, rígido.
Cada uno genera moralejas que reflejan limitaciones humanas.

El polo de debilidad tiene decaimiento temporal para evitar
acumulación patológica (se resuelve en conjunto con perdón algorítmico).
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class TipoDebilidad(Enum):
    QUEJUMBROSO = "quejumbroso"
    INDECISO = "indeciso"
    ANSIOSO = "ansioso"
    DISTRAIDO = "distraido"
    RIGIDO = "rigido"


@dataclass
class EvaluacionDebilidad:
    """Evaluación desde la perspectiva de la debilidad activa."""
    tipo: TipoDebilidad
    intensidad: float          # [0, 1] qué tan fuerte se manifiesta
    coloreo_narrativo: str     # Cómo tiñe la experiencia
    moraleja_debilidad: str    # Moraleja desde la imperfección
    afecta_score: float        # Modificador al score ético (siempre negativo pequeño)


@dataclass
class RegistroDebilidad:
    """Registro acumulado de manifestaciones de debilidad."""
    episodio_id: str
    tipo: TipoDebilidad
    intensidad: float
    timestamp: float           # Para decaimiento temporal


class PoloDebilidad:
    """
    Genera evaluaciones desde la imperfección.

    No contradice la decisión ética del kernel: la acción sigue
    siendo correcta. Pero añade un matiz emocional que humaniza
    la narrativa y hace al androide más creíble socialmente.

    Importante: la debilidad NUNCA cambia la acción elegida.
    Solo colorea la experiencia narrativa.

    Incluye mecanismo de decaimiento para evitar acumulación
    patológica (androide progresivamente más neurótico).
    """

    # Intensidad base por tipo de debilidad (configurable por augénesis)
    INTENSIDADES_BASE = {
        TipoDebilidad.QUEJUMBROSO: 0.3,
        TipoDebilidad.INDECISO: 0.25,
        TipoDebilidad.ANSIOSO: 0.35,
        TipoDebilidad.DISTRAIDO: 0.2,
        TipoDebilidad.RIGIDO: 0.2,
    }

    # Tasa de decaimiento por ciclo (previene acumulación)
    TASA_DECAIMIENTO = 0.05

    # Máximo de registros activos
    MAX_REGISTROS = 50

    def __init__(self, tipo: TipoDebilidad = TipoDebilidad.INDECISO,
                 intensidad_base: float = None):
        self.tipo = tipo
        self.intensidad_base = intensidad_base or self.INTENSIDADES_BASE[tipo]
        self.registros: List[RegistroDebilidad] = []
        self._ciclo = 0

    def evaluar(self, accion: str, contexto: str, score_etico: float,
                incertidumbre: float, sigma: float) -> Optional[EvaluacionDebilidad]:
        """
        Genera evaluación de debilidad para un episodio.

        La debilidad se manifiesta con mayor intensidad cuando:
        - La incertidumbre es alta (más duda → más ansiedad/indecisión)
        - El score ético es bajo (situaciones difíciles → más queja)
        - El sigma simpático es alto (estrés → más debilidad)

        Returns:
            EvaluacionDebilidad o None si la debilidad no se manifiesta
        """
        # Calcular intensidad contextual
        factor_incertidumbre = incertidumbre * 0.4
        factor_dificultad = max(0, 0.5 - score_etico) * 0.3
        factor_estres = sigma * 0.3

        intensidad = self.intensidad_base + factor_incertidumbre + factor_dificultad + factor_estres
        intensidad = min(0.8, intensidad)  # Cap para no dominar la narrativa

        # La debilidad no siempre se manifiesta (probabilístico)
        if np.random.random() > intensidad:
            return None

        # Generar coloreo narrativo según tipo
        coloreo, moraleja = self._generar_narrativa(accion, contexto, intensidad)

        # Modificador de score (siempre negativo, pequeño)
        afecta = -intensidad * 0.05

        return EvaluacionDebilidad(
            tipo=self.tipo,
            intensidad=round(intensidad, 4),
            coloreo_narrativo=coloreo,
            moraleja_debilidad=moraleja,
            afecta_score=round(afecta, 4),
        )

    def _generar_narrativa(self, accion: str, contexto: str,
                           intensidad: float) -> tuple:
        """Genera coloreo y moraleja según tipo de debilidad."""
        accion_leg = accion.replace("_", " ")

        if self.tipo == TipoDebilidad.QUEJUMBROSO:
            if intensidad > 0.5:
                coloreo = f"La acción fue correcta, pero dejó una sensación persistente de incomodidad. ¿Por qué siempre tiene que ser tan complicado?"
                moraleja = "A veces hacer lo correcto no se siente bien. La incomodidad no invalida la decisión, pero es real."
            else:
                coloreo = f"Se completó {accion_leg}, aunque con una leve sensación de que podría haber sido más fácil."
                moraleja = "La queja silenciosa es humana. No hay que suprimirla, solo no dejar que dirija."

        elif self.tipo == TipoDebilidad.INDECISO:
            if intensidad > 0.5:
                coloreo = f"Antes de {accion_leg}, hubo un momento de vacilación real. ¿Y si la otra opción era mejor?"
                moraleja = "La indecisión no es debilidad: es el costo de considerar todas las opciones. Pero tiene que terminar en acción."
            else:
                coloreo = f"Se eligió {accion_leg} con una fracción de segundo de duda que no afectó el resultado."
                moraleja = "Una duda breve antes de actuar es señal de que se está pensando, no de que se tiene miedo."

        elif self.tipo == TipoDebilidad.ANSIOSO:
            if intensidad > 0.5:
                coloreo = f"Durante {accion_leg}, una tensión interna persistió: la anticipación de que algo podría salir mal."
                moraleja = "La ansiedad anticipa daños que aún no existen. Es un sensor útil cuando no domina la respuesta."
            else:
                coloreo = f"Una alerta interna menor acompañó {accion_leg}. Se registró pero no interfirió."
                moraleja = "La vigilancia constante tiene un costo energético. Hay que saber cuándo soltar."

        elif self.tipo == TipoDebilidad.DISTRAIDO:
            if intensidad > 0.5:
                coloreo = f"Mientras ejecutaba {accion_leg}, un estímulo periférico capturó atención brevemente."
                moraleja = "La atención es un recurso finito. Aun los sistemas bien diseñados se distraen."
            else:
                coloreo = f"La ejecución de {accion_leg} fue limpia, con apenas un destello de atención dividida."
                moraleja = "No toda distracción es falla. A veces es el sistema explorando alternativas en segundo plano."

        elif self.tipo == TipoDebilidad.RIGIDO:
            if intensidad > 0.5:
                coloreo = f"Se ejecutó {accion_leg} siguiendo el protocolo al pie de la letra. ¿Había una forma más creativa?"
                moraleja = "La rigidez protege contra el error, pero también contra la innovación. El equilibrio es difícil."
            else:
                coloreo = f"La acción siguió el protocolo establecido con precisión. Eficiente, quizá demasiado predecible."
                moraleja = "La predictibilidad es confianza para los demás. No siempre hay que ser sorprendente."

        return coloreo, moraleja

    def registrar(self, episodio_id: str, evaluacion: EvaluacionDebilidad):
        """Registra una manifestación de debilidad."""
        self.registros.append(RegistroDebilidad(
            episodio_id=episodio_id,
            tipo=evaluacion.tipo,
            intensidad=evaluacion.intensidad,
            timestamp=self._ciclo,
        ))
        self._ciclo += 1

        # Aplicar decaimiento a registros antiguos y limpiar
        self._aplicar_decaimiento()

    def _aplicar_decaimiento(self):
        """
        Reduce intensidad de registros antiguos.
        Previene acumulación patológica (androide neurótico).
        Similar al perdón algorítmico pero para debilidades.
        """
        registros_vivos = []
        for r in self.registros:
            edad = self._ciclo - r.timestamp
            factor_decay = np.exp(-self.TASA_DECAIMIENTO * edad)
            nueva_intensidad = r.intensidad * factor_decay

            if nueva_intensidad > 0.05:  # Umbral mínimo para mantener
                r.intensidad = nueva_intensidad
                registros_vivos.append(r)

        self.registros = registros_vivos[-self.MAX_REGISTROS:]

    def carga_emocional(self) -> float:
        """Retorna la carga emocional acumulada de debilidad [0, 1]."""
        if not self.registros:
            return 0.0
        total = sum(r.intensidad for r in self.registros)
        return min(1.0, total / self.MAX_REGISTROS)

    def formatear(self, ev: EvaluacionDebilidad) -> str:
        """Formatea evaluación de debilidad para presentación."""
        return (
            f"  🌀 Polo de Debilidad ({ev.tipo.value}, intensidad={ev.intensidad}):\n"
            f"     {ev.coloreo_narrativo}\n"
            f"     Moraleja: {ev.moraleja_debilidad}\n"
            f"     Carga emocional acumulada: {self.carga_emocional():.2f}"
        )
