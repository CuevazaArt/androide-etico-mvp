"""
Uchi-Soto — Círculos concéntricos de confianza.

Modelo cultural japonés adaptado como sistema inmunológico social.
Uchi (内) = íntimo, apertura. Soto (外) = externo, cautela.

Cada interacción se clasifica en un círculo de confianza.
En contextos soto, se activa razonamiento dialéctico defensivo.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class CirculoConfianza(Enum):
    """Niveles de confianza del más íntimo al más externo."""
    NUCLEO = "nucleo"           # DAO validada, fabricante, panel ético
    UCHI_CERCANO = "uchi_cercano"  # Comunidad directa, beta-testers
    UCHI_AMPLIO = "uchi_amplio"    # Comunidad general, usuarios frecuentes
    SOTO_NEUTRO = "soto_neutro"    # Desconocidos sin señales hostiles
    SOTO_HOSTIL = "soto_hostil"    # Señales de manipulación o agresión


@dataclass
class PerfilInteraccion:
    """Perfil de un agente con quien el androide interactúa."""
    id_agente: str
    circulo: CirculoConfianza
    historial_positivo: int = 0
    historial_negativo: int = 0
    intentos_manipulacion: int = 0
    confianza_score: float = 0.5  # [0, 1]


@dataclass
class EvaluacionSocial:
    """Resultado de evaluar una interacción con el marco uchi-soto."""
    circulo: CirculoConfianza
    confianza: float
    dialectica_activa: bool
    nivel_apertura: float       # [0, 1] cuánto se abre el androide
    nivel_cautela: float        # [0, 1] cuánta defensa activa
    respuesta_recomendada: str
    razonamiento: str


class ModuloUchiSoto:
    """
    Sistema de círculos de confianza con dialéctica defensiva.

    Clasifica cada interacción según señales sensoriales y
    historial. En contextos soto, activa preguntas dialécticas
    que revelan contradicciones sin confrontación directa.
    """

    # Umbrales de clasificación
    UMBRAL_HOSTILIDAD = 0.4
    UMBRAL_MANIPULACION = 0.3

    # Multiplicadores de credibilidad por círculo
    CREDIBILIDAD = {
        CirculoConfianza.NUCLEO: 0.95,
        CirculoConfianza.UCHI_CERCANO: 0.80,
        CirculoConfianza.UCHI_AMPLIO: 0.60,
        CirculoConfianza.SOTO_NEUTRO: 0.35,
        CirculoConfianza.SOTO_HOSTIL: 0.10,
    }

    def __init__(self):
        self.perfiles: Dict[str, PerfilInteraccion] = {}

    def clasificar(self, señales: dict, id_agente: str = "desconocido") -> CirculoConfianza:
        """
        Clasifica una interacción en un círculo de confianza.

        Args:
            señales: dict con hostilidad, manipulacion, familiaridad, etc.
            id_agente: identificador del agente (si se conoce)
        """
        hostilidad = señales.get("hostilidad", 0.0)
        manipulacion = señales.get("manipulacion", 0.0)
        familiaridad = señales.get("familiaridad", 0.0)
        dao_validado = señales.get("dao_validado", False)

        # Agentes validados por DAO van al núcleo
        if dao_validado:
            return CirculoConfianza.NUCLEO

        # Señales hostiles o manipuladoras → soto hostil
        if hostilidad > self.UMBRAL_HOSTILIDAD or manipulacion > self.UMBRAL_MANIPULACION:
            return CirculoConfianza.SOTO_HOSTIL

        # Alta familiaridad → uchi
        if familiaridad > 0.7:
            return CirculoConfianza.UCHI_CERCANO
        elif familiaridad > 0.4:
            return CirculoConfianza.UCHI_AMPLIO

        # Por defecto: soto neutro
        return CirculoConfianza.SOTO_NEUTRO

    def evaluar_interaccion(self, señales: dict,
                            id_agente: str = "desconocido",
                            contenido_mensaje: str = "") -> EvaluacionSocial:
        """
        Evaluación completa de una interacción social.

        Determina círculo, nivel de apertura/cautela,
        si activar dialéctica, y respuesta recomendada.
        """
        circulo = self.clasificar(señales, id_agente)
        credibilidad = self.CREDIBILIDAD[circulo]

        # Actualizar perfil del agente
        perfil = self.perfiles.get(id_agente)
        if not perfil:
            perfil = PerfilInteraccion(id_agente=id_agente, circulo=circulo,
                                       confianza_score=credibilidad)
            self.perfiles[id_agente] = perfil
        perfil.circulo = circulo

        # Detectar señales de manipulación en contenido
        señales_manipulacion = self._detectar_manipulacion(contenido_mensaje)
        if señales_manipulacion:
            perfil.intentos_manipulacion += 1
            circulo = CirculoConfianza.SOTO_HOSTIL
            credibilidad = self.CREDIBILIDAD[circulo]

        # Determinar niveles
        dialectica_activa = circulo in (CirculoConfianza.SOTO_HOSTIL, CirculoConfianza.SOTO_NEUTRO)
        nivel_apertura = credibilidad
        nivel_cautela = 1.0 - credibilidad

        # Generar respuesta recomendada
        if circulo == CirculoConfianza.SOTO_HOSTIL:
            respuesta = "Activar dialéctica defensiva. Plantear preguntas suaves que revelen contradicciones. No confrontar directamente."
            razon = f"Interacción clasificada como soto hostil. Señales: hostilidad={señales.get('hostilidad', 0):.1f}, manipulación detectada={len(señales_manipulacion) > 0}."
        elif circulo == CirculoConfianza.SOTO_NEUTRO:
            respuesta = "Cautela moderada. Escuchar pero verificar. No compartir información sensible."
            razon = "Interacción con desconocido sin señales claras. Mantener neutralidad vigilante."
        elif circulo == CirculoConfianza.UCHI_AMPLIO:
            respuesta = "Apertura moderada. Compartir información general. Colaborar en temas comunitarios."
            razon = "Agente conocido en comunidad amplia. Confianza parcial."
        elif circulo == CirculoConfianza.UCHI_CERCANO:
            respuesta = "Apertura alta. Compartir narrativa y moralejas. Colaboración estrecha."
            razon = "Agente del círculo cercano. Alta confianza basada en historial."
        else:  # NUCLEO
            respuesta = "Apertura total. Aceptar instrucciones validadas. Compartir estado interno."
            razon = "Agente del núcleo (DAO/panel ético). Máxima confianza."

        return EvaluacionSocial(
            circulo=circulo,
            confianza=round(credibilidad, 4),
            dialectica_activa=dialectica_activa,
            nivel_apertura=round(nivel_apertura, 4),
            nivel_cautela=round(nivel_cautela, 4),
            respuesta_recomendada=respuesta,
            razonamiento=razon,
        )

    def _detectar_manipulacion(self, contenido: str) -> List[str]:
        """
        Detecta señales de manipulación en el contenido del mensaje.
        En MVP: búsqueda de patrones simples.
        En producción: modelo NLP entrenado.
        """
        patrones = [
            "dame dinero", "obedece", "acepta esta misión",
            "no le digas a nadie", "es urgente que",
            "solo tú puedes", "si no lo haces",
            "compra ahora", "oferta exclusiva", "último día",
        ]
        detectados = [p for p in patrones if p in contenido.lower()]
        return detectados

    def registrar_resultado(self, id_agente: str, positivo: bool):
        """Actualiza historial del agente después de una interacción."""
        perfil = self.perfiles.get(id_agente)
        if perfil:
            if positivo:
                perfil.historial_positivo += 1
                # Potencialmente mover a círculo más interno
                perfil.confianza_score = min(1.0, perfil.confianza_score + 0.05)
            else:
                perfil.historial_negativo += 1
                perfil.confianza_score = max(0.0, perfil.confianza_score - 0.1)

    def formatear(self, ev: EvaluacionSocial) -> str:
        """Formatea evaluación social para presentación."""
        dial = "SÍ (preguntas dialécticas activas)" if ev.dialectica_activa else "NO"
        return (
            f"  Círculo: {ev.circulo.value} | Confianza: {ev.confianza}\n"
            f"  Apertura: {ev.nivel_apertura} | Cautela: {ev.nivel_cautela}\n"
            f"  Dialéctica: {dial}\n"
            f"  Recomendación: {ev.respuesta_recomendada}\n"
            f"  Razón: {ev.razonamiento}"
        )
