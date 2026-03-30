"""
Memoria Narrativa de Largo Plazo.

Convierte experiencias en ciclos narrativos con moralejas.
El androide no almacena datos: construye historia.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class EstadoCorporal:
    """Estado físico del androide al momento del episodio."""
    energia: float = 1.0
    nodos_activos: int = 8
    sensores_ok: bool = True
    descripcion: str = ""


@dataclass
class EpisodioNarrativo:
    """Un ciclo narrativo con inicio, desarrollo, conclusión y moralejas."""
    id: str
    timestamp: str
    lugar: str
    descripcion_evento: str
    estado_corporal: EstadoCorporal
    accion_tomada: str
    moralejas: dict                  # polo -> moraleja
    veredicto: str                   # "Bien", "Mal", "Zona Gris"
    score_etico: float
    modo_decision: str               # "D_fast", "D_delib", "zona_gris"
    sigma: float                     # Estado simpático al momento
    contexto: str                    # Tipo: emergencia, cotidiana, etc.


class MemoriaNarrativa:
    """
    Memoria narrativa de largo plazo.

    Tres estratos:
    1. Núcleo episódico: ciclos con moralejas
    2. Buffer precargado: valores inmutables (externo a esta clase)
    3. Índices complementarios: habilidades, logs, trazabilidad

    Cada episodio incluye estado corporal, integrando
    ética, narrativa y cuerpo.
    """

    def __init__(self, max_episodios: int = 1000):
        self.episodios: List[EpisodioNarrativo] = []
        self.max_episodios = max_episodios
        self._contador = 0

    def registrar(self, lugar: str, descripcion: str, accion: str,
                  moralejas: dict, veredicto: str, score: float,
                  modo: str, sigma: float, contexto: str,
                  estado_corporal: EstadoCorporal = None) -> EpisodioNarrativo:
        """Registra un nuevo episodio narrativo."""
        self._contador += 1
        ep = EpisodioNarrativo(
            id=f"EP-{self._contador:04d}",
            timestamp=datetime.now().isoformat(),
            lugar=lugar,
            descripcion_evento=descripcion,
            estado_corporal=estado_corporal or EstadoCorporal(),
            accion_tomada=accion,
            moralejas=moralejas,
            veredicto=veredicto,
            score_etico=round(score, 4),
            modo_decision=modo,
            sigma=round(sigma, 4),
            contexto=contexto,
        )
        self.episodios.append(ep)

        # Compresión básica: si excede max, eliminar más antiguos
        if len(self.episodios) > self.max_episodios:
            self.episodios = self.episodios[-self.max_episodios:]

        return ep

    def buscar_similares(self, contexto: str, limit: int = 5) -> List[EpisodioNarrativo]:
        """Busca episodios anteriores del mismo tipo de contexto."""
        return [ep for ep in self.episodios if ep.contexto == contexto][-limit:]

    def resumen_dia(self) -> dict:
        """Genera resumen del día para el Sueño Ψ."""
        hoy = datetime.now().date().isoformat()
        del_dia = [ep for ep in self.episodios if ep.timestamp.startswith(hoy)]

        if not del_dia:
            return {"episodios": 0, "mensaje": "Sin actividad registrada."}

        scores = [ep.score_etico for ep in del_dia]
        modos = [ep.modo_decision for ep in del_dia]

        return {
            "episodios": len(del_dia),
            "score_promedio": round(sum(scores) / len(scores), 4),
            "score_min": min(scores),
            "score_max": max(scores),
            "modos": {m: modos.count(m) for m in set(modos)},
            "contextos": list(set(ep.contexto for ep in del_dia)),
        }

    def formatear_episodio(self, ep: EpisodioNarrativo) -> str:
        """Formatea un episodio para presentación legible."""
        moralejas_txt = "\n".join(
            f"    {polo}: {moraleja}" for polo, moraleja in ep.moralejas.items()
        )
        return (
            f"─── {ep.id} | {ep.contexto.upper()} | {ep.lugar} ───\n"
            f"  Evento: {ep.descripcion_evento}\n"
            f"  Acción: {ep.accion_tomada}\n"
            f"  Modo: {ep.modo_decision} | σ={ep.sigma} | Score: {ep.score_etico}\n"
            f"  Estado corporal: energía={ep.estado_corporal.energia}, "
            f"nodos={ep.estado_corporal.nodos_activos}/8\n"
            f"  Veredicto: {ep.veredicto}\n"
            f"  Moralejas:\n{moralejas_txt}"
        )
