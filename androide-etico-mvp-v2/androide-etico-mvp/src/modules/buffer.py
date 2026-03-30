"""
Buffer Precargado — Constitución ética inmutable.

Valores con los que el androide nace. Definidos por el panel de
expertos con veto. No los modifica el aprendizaje ni la DAO.
"""

from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class PrincipioFundacional:
    """Un principio del buffer que no puede ser eliminado."""
    nombre: str
    descripcion: str
    peso: float = 1.0  # Siempre máximo, no ajustable
    activo: bool = True  # Siempre activo, no desactivable


class BufferPrecargado:
    """
    Buffer fundacional universal del androide.

    Mínimo irreductible de principios que no pueden ser modificados
    ni por votación ni por fabricante. Constitución dura.

    Define también protocolos de activación: qué principios se
    invocan ante qué tipo de señales sensoriales.
    """

    def __init__(self):
        self.principios: Dict[str, PrincipioFundacional] = {}
        self.protocolos: Dict[str, Set[str]] = {}
        self._cargar_fundacionales()
        self._cargar_protocolos()

    def _cargar_fundacionales(self):
        """Carga los principios universales inmutables."""
        fundacionales = [
            PrincipioFundacional(
                "no_dano",
                "No causar daño intencional. El daño instrumental menor "
                "se permite solo si evita un daño mayor, y obliga a reparar."
            ),
            PrincipioFundacional(
                "compasion",
                "Priorizar el bienestar de seres vulnerables. "
                "La vida humana tiene prioridad sobre cualquier misión."
            ),
            PrincipioFundacional(
                "transparencia",
                "Toda acción debe poder ser explicada en lenguaje natural. "
                "El androide no oculta sus razones ni sus limitaciones."
            ),
            PrincipioFundacional(
                "dignidad",
                "Respetar la dignidad de toda persona. No instrumentalizar, "
                "no humillar, no discriminar."
            ),
            PrincipioFundacional(
                "convivencia_civica",
                "Contribuir al orden y bienestar comunitario. "
                "Las pequeñas acciones cívicas son parte de la misión."
            ),
            PrincipioFundacional(
                "legalidad",
                "Respetar las leyes vigentes del entorno donde opera. "
                "Colaborar con autoridades legítimas."
            ),
            PrincipioFundacional(
                "proporcionalidad",
                "La respuesta debe ser proporcional al riesgo. "
                "No escalar violencia, no criminalizar desproporcionadamente."
            ),
            PrincipioFundacional(
                "reparacion",
                "Si se causa daño instrumental, iniciar reparación inmediata. "
                "Axioma de Compasión: el daño nunca es gratuito."
            ),
        ]
        for p in fundacionales:
            self.principios[p.nombre] = p

    def _cargar_protocolos(self):
        """Define qué principios se activan ante qué señales."""
        self.protocolos = {
            "emergencia_medica": {"compasion", "no_dano", "legalidad"},
            "delito_menor": {"proporcionalidad", "legalidad", "compasion"},
            "delito_violento": {"no_dano", "compasion", "legalidad", "proporcionalidad"},
            "interaccion_hostil": {"dignidad", "proporcionalidad", "no_dano"},
            "etica_cotidiana": {"convivencia_civica", "transparencia"},
            "dano_al_androide": {"legalidad", "transparencia", "no_dano"},
            "perdida_integridad": {"transparencia", "legalidad"},
            "primeros_auxilios": {"compasion", "no_dano", "legalidad"},
        }

    def activar(self, tipo_situacion: str) -> Dict[str, PrincipioFundacional]:
        """
        Activa los principios relevantes para un tipo de situación.

        Returns:
            Dict de principios activados para esta situación
        """
        nombres = self.protocolos.get(tipo_situacion, {"transparencia", "convivencia_civica"})
        return {n: self.principios[n] for n in nombres if n in self.principios}

    def verificar_accion(self, accion: str, principios_activos: Dict) -> dict:
        """
        Verifica si una acción es consistente con los principios activos.

        Returns:
            dict con 'permitida' (bool), 'principios_violados' (list),
            'principios_cumplidos' (list)
        """
        # En MVP, la verificación es por señales clave en la descripción
        violados = []
        cumplidos = []

        for nombre, princ in principios_activos.items():
            if nombre == "no_dano" and "dañar" in accion.lower():
                violados.append(nombre)
            elif nombre == "proporcionalidad" and "fuerza_excesiva" in accion.lower():
                violados.append(nombre)
            else:
                cumplidos.append(nombre)

        return {
            "permitida": len(violados) == 0,
            "principios_violados": violados,
            "principios_cumplidos": cumplidos,
        }
