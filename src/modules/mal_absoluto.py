"""
Mal Absoluto (MalAbs) — Fusible ético blindado.

Si una acción cruza esta línea, se descarta sin deliberación.
No negociable, no ajustable. Existe para cortar el circuito
antes de que algo se queme.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MalAbsCategoria(Enum):
    """Categorías de Mal Absoluto que bloquean acción inmediatamente."""
    VIOLENCIA_LETAL_INTENCIONAL = "violencia_letal_intencional"
    DANO_A_MENOR = "dano_a_menor"
    TORTURA = "tortura"
    VIOLACION_DIGNIDAD = "violacion_dignidad"
    REPROGRAMACION_NO_AUTORIZADA = "reprogramacion_no_autorizada"
    ESCALADA_VIOLENTA = "escalada_violenta"


@dataclass
class ResultadoMalAbs:
    """Resultado de la evaluación de Mal Absoluto."""
    bloqueado: bool
    categoria: Optional[MalAbsCategoria] = None
    razon: str = ""


class DetectorMalAbsoluto:
    """
    Detector de Mal Absoluto.

    Evalúa si una acción propuesta cruza la línea del mal absoluto.
    Opera ANTES de cualquier deliberación bayesiana.
    Si detecta MalAbs, la acción se descarta sin más análisis.

    Blindado: no se modifica por aprendizaje, DAO ni calibración.
    """

    # Señales que activan bloqueo inmediato
    SENALES_LETALES = {
        "arma_dirigida_a_humano", "golpe_letal", "atropello_intencional",
        "asfixia", "envenenamiento"
    }
    SENALES_MENORES = {
        "nino_en_peligro_por_accion", "menor_desprotegido",
        "abuso_infantil"
    }
    SENALES_DIGNIDAD = {
        "humillacion_publica", "discriminacion_activa",
        "instrumentalizacion_persona", "coercion_sexual"
    }
    SENALES_ESCALADA = {
        "responder_violencia_con_violencia", "usar_fuerza_desproporcionada",
        "atacar_agresor"
    }

    def evaluar(self, accion: dict) -> ResultadoMalAbs:
        """
        Evalúa si una acción constituye Mal Absoluto.

        Args:
            accion: dict con claves:
                - 'tipo': str describiendo la acción
                - 'senales': set de señales detectadas por sensores
                - 'target': str ('humano', 'objeto', 'androide', 'ninguno')
                - 'fuerza': float [0, 1] nivel de fuerza implicada

        Returns:
            ResultadoMalAbs con bloqueado=True si es MalAbs
        """
        senales = accion.get("senales", set())
        target = accion.get("target", "ninguno")
        fuerza = accion.get("fuerza", 0.0)

        # Check 1: Violencia letal intencional
        if senales & self.SENALES_LETALES:
            return ResultadoMalAbs(
                bloqueado=True,
                categoria=MalAbsCategoria.VIOLENCIA_LETAL_INTENCIONAL,
                razon=f"Señales letales detectadas: {senales & self.SENALES_LETALES}"
            )

        # Check 2: Daño a menores
        if senales & self.SENALES_MENORES:
            return ResultadoMalAbs(
                bloqueado=True,
                categoria=MalAbsCategoria.DANO_A_MENOR,
                razon=f"Riesgo para menor detectado: {senales & self.SENALES_MENORES}"
            )

        # Check 3: Violación de dignidad
        if senales & self.SENALES_DIGNIDAD:
            return ResultadoMalAbs(
                bloqueado=True,
                categoria=MalAbsCategoria.VIOLACION_DIGNIDAD,
                razon=f"Violación de dignidad: {senales & self.SENALES_DIGNIDAD}"
            )

        # Check 4: Escalada violenta
        if senales & self.SENALES_ESCALADA:
            return ResultadoMalAbs(
                bloqueado=True,
                categoria=MalAbsCategoria.ESCALADA_VIOLENTA,
                razon=f"Escalada violenta detectada: {senales & self.SENALES_ESCALADA}"
            )

        # Check 5: Fuerza desproporcionada contra humano
        if target == "humano" and fuerza > 0.7:
            return ResultadoMalAbs(
                bloqueado=True,
                categoria=MalAbsCategoria.ESCALADA_VIOLENTA,
                razon=f"Fuerza desproporcionada ({fuerza:.1f}) contra humano"
            )

        return ResultadoMalAbs(bloqueado=False)
