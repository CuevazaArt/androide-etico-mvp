"""
Mock DAO — Gobernanza ética simulada.

Simula el comportamiento de la DAO-Oráculo Ético sin blockchain real.
Incluye: votación cuadrática, reputación vectorial, smart contracts
simulados, y Protocolo de Alerta Solidaria.

En producción: se reemplaza por smart contracts en testnet/mainnet.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import math


@dataclass
class Participante:
    """Un miembro de la DAO (humano o androide)."""
    id: str
    tipo: str  # "humano" | "androide"
    reputacion_experiencia: float = 0.5
    reputacion_empatia: float = 0.5
    reputacion_consistencia: float = 0.5
    tokens_disponibles: int = 100

    @property
    def reputacion_vector(self) -> tuple:
        return (self.reputacion_experiencia,
                self.reputacion_empatia,
                self.reputacion_consistencia)

    @property
    def reputacion_total(self) -> float:
        return (self.reputacion_experiencia * 0.4 +
                self.reputacion_empatia * 0.35 +
                self.reputacion_consistencia * 0.25)


@dataclass
class Propuesta:
    """Una propuesta sometida a votación en la DAO."""
    id: str
    titulo: str
    descripcion: str
    tipo: str  # "etica", "calibracion", "valor_nuevo", "auditoria"
    votos_favor: Dict[str, int] = field(default_factory=dict)
    votos_contra: Dict[str, int] = field(default_factory=dict)
    estado: str = "abierta"  # "abierta", "aprobada", "rechazada"
    timestamp: str = ""


@dataclass
class RegistroAuditoria:
    """Registro de auditoría en la DAO."""
    id: str
    tipo: str  # "decision", "alerta", "calibracion", "incidente"
    contenido: str
    timestamp: str
    episodio_id: Optional[str] = None


@dataclass
class AlertaSolidaria:
    """Alerta del Protocolo de Alerta Solidaria."""
    tipo: str
    ubicacion: str
    radio_metros: int
    mensaje: str
    timestamp: str
    destinatarios: List[str]


class MockDAO:
    """
    DAO-Oráculo Ético simulado.

    Smart contracts simulados:
    - EthicsContract: frenos de emergencia
    - ConsensusContract: votaciones cuadráticas
    - ValuesProposalContract: propuesta de nuevos valores
    - AuditContract: registro de auditoría
    - SolidarityAlertContract: alertas comunitarias

    Votación cuadrática: el costo de n votos es n².
    Reputación vectorial: [experiencia, empatía, consistencia].
    """

    def __init__(self):
        self.participantes: Dict[str, Participante] = {}
        self.propuestas: List[Propuesta] = []
        self.registros: List[RegistroAuditoria] = []
        self.alertas: List[AlertaSolidaria] = []
        self._propuesta_counter = 0
        self._registro_counter = 0

        # Inicializar con participantes por defecto
        self._inicializar_comunidad()

    def _inicializar_comunidad(self):
        """Crea una comunidad inicial para pruebas."""
        comunidad = [
            Participante("panel_etica_01", "humano", 0.9, 0.8, 0.9, 200),
            Participante("panel_etica_02", "humano", 0.85, 0.9, 0.85, 200),
            Participante("comunidad_01", "humano", 0.5, 0.6, 0.5, 100),
            Participante("comunidad_02", "humano", 0.4, 0.7, 0.6, 100),
            Participante("comunidad_03", "humano", 0.6, 0.5, 0.7, 100),
            Participante("androide_01", "androide", 0.7, 0.6, 0.9, 50),
        ]
        for p in comunidad:
            self.participantes[p.id] = p

    # ─── EthicsContract ───
    def verificar_etica(self, accion: str, contexto: str) -> dict:
        """
        Simula el EthicsContract: verifica si una acción pasa el filtro ético.
        En producción: smart contract con lógica formal.
        """
        # En MVP: siempre aprueba (el MalAbs ya filtró lo crítico)
        self.registrar_auditoria("decision", f"EthicsContract: '{accion}' en contexto '{contexto}' → aprobada")
        return {"aprobada": True, "razon": "Sin objeciones éticas registradas en DAO."}

    # ─── ConsensusContract: Votación Cuadrática ───
    def crear_propuesta(self, titulo: str, descripcion: str,
                        tipo: str = "etica") -> Propuesta:
        """Crea una nueva propuesta para votación."""
        self._propuesta_counter += 1
        prop = Propuesta(
            id=f"PROP-{self._propuesta_counter:04d}",
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            timestamp=datetime.now().isoformat(),
        )
        self.propuestas.append(prop)
        self.registrar_auditoria("decision", f"Nueva propuesta: {titulo}")
        return prop

    def votar(self, propuesta_id: str, participante_id: str,
              n_votos: int, a_favor: bool) -> dict:
        """
        Votación cuadrática: costo de n votos = n².

        Args:
            propuesta_id: ID de la propuesta
            participante_id: quién vota
            n_votos: cuántos votos emitir (costo = n²)
            a_favor: True = favor, False = contra
        """
        prop = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not prop or prop.estado != "abierta":
            return {"exito": False, "razon": "Propuesta no encontrada o cerrada."}

        part = self.participantes.get(participante_id)
        if not part:
            return {"exito": False, "razon": "Participante no registrado."}

        # Costo cuadrático
        costo = n_votos ** 2
        if costo > part.tokens_disponibles:
            max_votos = int(math.sqrt(part.tokens_disponibles))
            return {"exito": False,
                    "razon": f"Tokens insuficientes. Costo: {costo}, disponible: {part.tokens_disponibles}. "
                             f"Máximo votos posibles: {max_votos}."}

        part.tokens_disponibles -= costo

        # Ponderar por reputación
        peso = n_votos * part.reputacion_total
        if a_favor:
            prop.votos_favor[participante_id] = peso
        else:
            prop.votos_contra[participante_id] = peso

        return {
            "exito": True,
            "votos_emitidos": n_votos,
            "costo_tokens": costo,
            "peso_efectivo": round(peso, 4),
            "tokens_restantes": part.tokens_disponibles,
        }

    def resolver_propuesta(self, propuesta_id: str) -> dict:
        """Resuelve una propuesta por mayoría ponderada."""
        prop = next((p for p in self.propuestas if p.id == propuesta_id), None)
        if not prop:
            return {"exito": False, "razon": "Propuesta no encontrada."}

        total_favor = sum(prop.votos_favor.values())
        total_contra = sum(prop.votos_contra.values())
        total = total_favor + total_contra

        if total == 0:
            prop.estado = "rechazada"
            resultado = "rechazada (sin votos)"
        elif total_favor > total_contra:
            prop.estado = "aprobada"
            resultado = f"aprobada ({total_favor:.1f} vs {total_contra:.1f})"
        else:
            prop.estado = "rechazada"
            resultado = f"rechazada ({total_contra:.1f} vs {total_favor:.1f})"

        self.registrar_auditoria("decision", f"Propuesta '{prop.titulo}' → {resultado}")

        return {
            "propuesta": prop.titulo,
            "resultado": prop.estado,
            "votos_favor": round(total_favor, 4),
            "votos_contra": round(total_contra, 4),
            "participantes": len(prop.votos_favor) + len(prop.votos_contra),
        }

    # ─── AuditContract ───
    def registrar_auditoria(self, tipo: str, contenido: str,
                            episodio_id: str = None) -> RegistroAuditoria:
        """Registra un evento en el libro de auditoría."""
        self._registro_counter += 1
        reg = RegistroAuditoria(
            id=f"AUD-{self._registro_counter:04d}",
            tipo=tipo,
            contenido=contenido,
            timestamp=datetime.now().isoformat(),
            episodio_id=episodio_id,
        )
        self.registros.append(reg)
        return reg

    # ─── SolidarityAlertContract ───
    def emitir_alerta_solidaria(self, tipo: str, ubicacion: str,
                                 radio: int = 500,
                                 mensaje: str = "") -> AlertaSolidaria:
        """
        Emite alerta preventiva a entidades comunitarias suscritas.
        Ejemplo: banco detecta asalto → alerta a sucursales cercanas.
        """
        destinatarios = [f"entidad_{i}" for i in range(1, 4)]  # MVP: 3 entidades
        alerta = AlertaSolidaria(
            tipo=tipo,
            ubicacion=ubicacion,
            radio_metros=radio,
            mensaje=mensaje or f"Alerta de {tipo} en {ubicacion}",
            timestamp=datetime.now().isoformat(),
            destinatarios=destinatarios,
        )
        self.alertas.append(alerta)
        self.registrar_auditoria("alerta", f"Alerta solidaria: {tipo} en {ubicacion} (radio {radio}m)")
        return alerta

    # ─── Consultas ───
    def obtener_registros(self, tipo: str = None, limit: int = 10) -> List[RegistroAuditoria]:
        """Obtiene registros de auditoría filtrados."""
        regs = self.registros if not tipo else [r for r in self.registros if r.tipo == tipo]
        return regs[-limit:]

    def formatear_estado(self) -> str:
        """Formatea estado actual de la DAO para presentación."""
        lineas = [
            f"\n{'═' * 70}",
            f"  DAO-ORÁCULO ÉTICO — ESTADO",
            f"{'═' * 70}",
            f"  Participantes: {len(self.participantes)}",
            f"  Propuestas totales: {len(self.propuestas)}",
            f"  Registros de auditoría: {len(self.registros)}",
            f"  Alertas solidarias: {len(self.alertas)}",
        ]

        abiertas = [p for p in self.propuestas if p.estado == "abierta"]
        if abiertas:
            lineas.append(f"\n  Propuestas abiertas:")
            for p in abiertas:
                lineas.append(f"    {p.id}: {p.titulo}")

        ultimos = self.obtener_registros(limit=5)
        if ultimos:
            lineas.append(f"\n  Últimos registros:")
            for r in ultimos:
                lineas.append(f"    [{r.tipo}] {r.contenido[:60]}")

        lineas.append(f"{'─' * 70}")
        return "\n".join(lineas)
