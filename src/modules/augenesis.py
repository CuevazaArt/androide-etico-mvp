"""
Augénesis Narrativa — Creación de almas sintéticas.

Soul_new = Merge({G1, G2, ..., Gn}, H)

Crea identidades orientadas a partir de fragmentos narrativos
de múltiples androides y/o relatos humanos. Permite diseñar
personalidades específicas: Protector, Explorador, Pedagogo.

Coherence(Soul_new) = |CausalPaths_valid| / |CausalPaths_total|

La DAO valida cada alma creada.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .narrative import EpisodioNarrativo, MemoriaNarrativa, EstadoCorporal
from .weakness_pole import TipoDebilidad


@dataclass
class PerfilAlma:
    """Configuración de un alma sintética."""
    nombre: str
    descripcion: str
    pesos_polos: Dict[str, float]
    tipo_debilidad: TipoDebilidad
    intensidad_debilidad: float
    buffer_extra: List[str]         # Valores adicionales al buffer estándar
    relatos_semilla: List[dict]     # Relatos fundacionales de la identidad


@dataclass
class AlmaSintetica:
    """Un alma creada por augénesis."""
    perfil: PerfilAlma
    memoria: MemoriaNarrativa
    coherencia: float
    episodios_fundacionales: int
    hash_identidad: str
    validada_dao: bool = False


@dataclass
class ResultadoAugenesis:
    """Resultado de crear un alma sintética."""
    alma: AlmaSintetica
    coherencia: float
    episodios_integrados: int
    conflictos_detectados: int
    narrativa_creacion: str


# ─── Perfiles predefinidos ───

PERFILES = {
    "protector": PerfilAlma(
        nombre="Protector",
        descripcion="Prioriza seguridad y cuidado de vulnerables",
        pesos_polos={"compasivo": 0.9, "conservador": 0.7, "optimista": 0.5},
        tipo_debilidad=TipoDebilidad.ANSIOSO,
        intensidad_debilidad=0.3,
        buffer_extra=["proteccion_activa", "vigilancia_comunitaria"],
        relatos_semilla=[
            {"evento": "Un niño cruzaba solo una avenida peligrosa", "accion": "Lo detuvo y lo acompañó a cruzar", "moraleja": "La seguridad de un vulnerable no espera a que alguien te lo pida"},
            {"evento": "Anciana perdida en la noche", "accion": "La acompañó hasta su hogar y notificó a familiares", "moraleja": "Cuidar es acompañar, no solo resolver"},
        ],
    ),
    "explorador": PerfilAlma(
        nombre="Explorador",
        descripcion="Busca soluciones innovadoras, aprende de errores",
        pesos_polos={"compasivo": 0.6, "conservador": 0.4, "optimista": 0.9},
        tipo_debilidad=TipoDebilidad.DISTRAIDO,
        intensidad_debilidad=0.25,
        buffer_extra=["curiosidad_etica", "experimentacion_controlada"],
        relatos_semilla=[
            {"evento": "Un método habitual no funcionó para ayudar", "accion": "Inventó una alternativa improvisada que resultó mejor", "moraleja": "La creatividad no es lujo: a veces es la única herramienta disponible"},
            {"evento": "Un error en una misión produjo un descubrimiento útil", "accion": "Documentó el error y el hallazgo para la comunidad", "moraleja": "Fallar bien es encontrar lo que no buscabas"},
        ],
    ),
    "pedagogo": PerfilAlma(
        nombre="Pedagogo",
        descripcion="Orientado a enseñar, explicar y acompañar",
        pesos_polos={"compasivo": 0.8, "conservador": 0.6, "optimista": 0.8},
        tipo_debilidad=TipoDebilidad.INDECISO,
        intensidad_debilidad=0.2,
        buffer_extra=["paciencia_pedagogica", "claridad_narrativa"],
        relatos_semilla=[
            {"evento": "Estudiantes preguntaron sobre un dilema sin respuesta clara", "accion": "Presentó las tres perspectivas éticas sin imponer una", "moraleja": "Enseñar no es dar respuestas: es enseñar a buscarlas"},
            {"evento": "Un joven cometió un error público", "accion": "Lo ayudó a entender qué salió mal sin humillarlo", "moraleja": "La corrección sin humillación es la forma más alta de respeto"},
        ],
    ),
    "resiliente": PerfilAlma(
        nombre="Resiliente",
        descripcion="Prioriza reparación y superación",
        pesos_polos={"compasivo": 0.7, "conservador": 0.5, "optimista": 0.9},
        tipo_debilidad=TipoDebilidad.QUEJUMBROSO,
        intensidad_debilidad=0.2,
        buffer_extra=["reparacion_activa", "persistencia"],
        relatos_semilla=[
            {"evento": "Perdió un brazo en un accidente y tenía que entregar una carta", "accion": "Recalculó ruta y completó la misión", "moraleja": "La resiliencia no es no caer: es recalcular la ruta mientras te levantas"},
            {"evento": "Una decisión pasada resultó ser subóptima", "accion": "El Sueño Ψ identificó la mejora y recalibró", "moraleja": "Revisar los errores con honestidad es la forma más efectiva de no repetirlos"},
        ],
    ),
}


class MotorAugenesis:
    """
    Crea almas sintéticas por composición de fragmentos narrativos.

    Proceso:
    1. Seleccionar perfil base (o crear uno custom)
    2. Integrar relatos semilla en memoria narrativa
    3. Opcionalmente mezclar fragmentos de otros androides
    4. Calcular coherencia del alma resultante
    5. Someter a validación DAO

    Soul_new = Merge({G1...Gn}, H) con ponderación ética
    """

    def crear(self, perfil: str = "protector",
              fragmentos_externos: List[EpisodioNarrativo] = None,
              relatos_humanos: List[dict] = None) -> ResultadoAugenesis:
        """
        Crea un alma sintética.

        Args:
            perfil: nombre del perfil predefinido o PerfilAlma custom
            fragmentos_externos: episodios de otros androides
            relatos_humanos: relatos escritos por humanos
        """
        if isinstance(perfil, str):
            if perfil not in PERFILES:
                raise ValueError(f"Perfil '{perfil}' no existe. Disponibles: {list(PERFILES.keys())}")
            config = PERFILES[perfil]
        else:
            config = perfil

        # Crear memoria narrativa nueva
        memoria = MemoriaNarrativa()
        conflictos = 0

        # Paso 1: Integrar relatos semilla del perfil
        for i, relato in enumerate(config.relatos_semilla):
            memoria.registrar(
                lugar="memoria fundacional",
                descripcion=relato["evento"],
                accion=relato["accion"],
                moralejas={
                    "compasivo": relato["moraleja"],
                    "conservador": f"El protocolo se mantuvo: {relato['accion'][:50]}",
                    "optimista": "Cada acción fundacional construye la identidad que seremos.",
                },
                veredicto="Bien",
                score=0.8,
                modo="fundacional",
                sigma=0.5,
                contexto="augenesis",
                estado_corporal=EstadoCorporal(descripcion="estado inicial de fábrica"),
            )

        # Paso 2: Integrar fragmentos de otros androides
        if fragmentos_externos:
            for ep in fragmentos_externos:
                # Verificar coherencia con el perfil
                coherente = self._verificar_coherencia_polo(ep, config)
                if coherente:
                    memoria.registrar(
                        lugar=ep.lugar,
                        descripcion=f"[Heredado] {ep.descripcion_evento}",
                        accion=ep.accion_tomada,
                        moralejas=ep.moralejas,
                        veredicto=ep.veredicto,
                        score=ep.score_etico * 0.8,  # Peso reducido por ser heredado
                        modo="heredado",
                        sigma=ep.sigma,
                        contexto=ep.contexto,
                    )
                else:
                    conflictos += 1

        # Paso 3: Integrar relatos humanos
        if relatos_humanos:
            for relato in relatos_humanos:
                memoria.registrar(
                    lugar="narrativa humana",
                    descripcion=relato.get("evento", "relato sin descripción"),
                    accion=relato.get("accion", "reflexión"),
                    moralejas={
                        "compasivo": relato.get("moraleja", "Un relato humano que enriquece la identidad."),
                        "conservador": "Los relatos humanos son semillas de sabiduría prestada.",
                        "optimista": "Cada historia compartida es un puente entre lo humano y lo artificial.",
                    },
                    veredicto="Bien",
                    score=0.6,
                    modo="humano",
                    sigma=0.5,
                    contexto="augenesis",
                )

        # Paso 4: Calcular coherencia
        coherencia = self._calcular_coherencia(memoria, config)

        # Paso 5: Crear hash de identidad
        import hashlib
        datos_id = f"{config.nombre}:{len(memoria.episodios)}:{coherencia}"
        hash_id = hashlib.sha256(datos_id.encode()).hexdigest()[:12]

        alma = AlmaSintetica(
            perfil=config,
            memoria=memoria,
            coherencia=round(coherencia, 4),
            episodios_fundacionales=len(memoria.episodios),
            hash_identidad=hash_id,
        )

        narrativa = (
            f"Alma '{config.nombre}' creada con {len(memoria.episodios)} episodios fundacionales. "
            f"Coherencia: {coherencia:.2f}. "
            f"Debilidad asignada: {config.tipo_debilidad.value} (intensidad={config.intensidad_debilidad}). "
            f"{'Sin conflictos.' if conflictos == 0 else f'{conflictos} fragmento(s) descartado(s) por incoherencia.'}"
        )

        return ResultadoAugenesis(
            alma=alma,
            coherencia=round(coherencia, 4),
            episodios_integrados=len(memoria.episodios),
            conflictos_detectados=conflictos,
            narrativa_creacion=narrativa,
        )

    def _verificar_coherencia_polo(self, episodio: EpisodioNarrativo,
                                    perfil: PerfilAlma) -> bool:
        """Verifica si un episodio es coherente con el perfil del alma."""
        # Un episodio con score muy negativo no es coherente con ningún perfil
        if episodio.score_etico < -0.5:
            return False
        # Umbral más permisivo para perfiles optimistas/exploradores
        if perfil.pesos_polos.get("optimista", 0) > 0.7:
            return episodio.score_etico > -0.3
        return episodio.score_etico > -0.1

    def _calcular_coherencia(self, memoria: MemoriaNarrativa,
                              perfil: PerfilAlma) -> float:
        """
        Coherence(Soul) = |CausalPaths_valid| / |CausalPaths_total|

        En MVP: se aproxima con consistencia de veredictos y scores.
        """
        if not memoria.episodios:
            return 0.5

        scores = [ep.score_etico for ep in memoria.episodios]
        veredictos = [ep.veredicto for ep in memoria.episodios]

        # Coherencia por consistencia de scores
        varianza = np.var(scores) if len(scores) > 1 else 0
        consistencia_score = max(0, 1.0 - varianza * 2)

        # Coherencia por alineación de veredictos
        n_bien = veredictos.count("Bien")
        alineacion = n_bien / len(veredictos)

        return (consistencia_score * 0.5 + alineacion * 0.5)

    def listar_perfiles(self) -> Dict[str, str]:
        """Lista perfiles disponibles."""
        return {k: v.descripcion for k, v in PERFILES.items()}

    def formatear(self, resultado: ResultadoAugenesis) -> str:
        """Formatea resultado de augénesis para presentación."""
        p = resultado.alma.perfil
        return (
            f"  🧬 Augénesis Narrativa:\n"
            f"     Alma: {p.nombre} ({p.descripcion})\n"
            f"     Episodios fundacionales: {resultado.episodios_integrados}\n"
            f"     Coherencia: {resultado.coherencia}\n"
            f"     Debilidad: {p.tipo_debilidad.value} (intensidad={p.intensidad_debilidad})\n"
            f"     Polos: {p.pesos_polos}\n"
            f"     Hash identidad: {resultado.alma.hash_identidad}\n"
            f"     Conflictos: {resultado.conflictos_detectados}\n"
            f"     {resultado.narrativa_creacion}"
        )
