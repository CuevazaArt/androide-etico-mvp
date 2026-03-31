"""
Protocolo de Inmortalidad — Backup y restore de identidad.

Backup(G, θ) → {DAO, Nube, Local, Blockchain}
Restore(G, θ) → NuevoKernel

Garantiza que el "alma" del androide (memoria narrativa,
parámetros bayesianos, estado de perdón, configuración de
polos) sobreviva a la destrucción total del hardware.

4 capas de respaldo para verificación cruzada de integridad.
"""

import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Snapshot:
    """Captura completa del estado del alma."""
    id: str
    timestamp: str
    version: str

    # Memoria narrativa
    episodios_count: int
    ultimo_episodio_id: str

    # Parámetros bayesianos
    umbral_poda: float
    pesos_hipotesis: List[float]

    # Estado del locus
    alpha_locus: float
    beta_locus: float

    # Estado del perdón
    carga_negativa: float
    recuerdos_perdonados: int

    # Configuración de debilidad
    tipo_debilidad: str
    intensidad_debilidad: float
    carga_emocional: float

    # Polos éticos
    pesos_polos: Dict[str, float]

    # Hash de integridad
    hash_integridad: str = ""


@dataclass
class ResultadoRestore:
    """Resultado de una operación de restauración."""
    exito: bool
    fuente: str               # "local", "nube", "dao", "blockchain"
    snapshot_id: str
    integridad_verificada: bool
    discrepancias: List[str]
    narrativa: str


class ProtocoloInmortalidad:
    """
    Sistema de respaldo distribuido y restauración de identidad.

    4 capas de respaldo:
    1. Local: snapshot rápido para restauración inmediata
    2. Nube: copia completa para desastres físicos
    3. DAO: registros auditables de decisiones y moralejas
    4. Blockchain/IPFS: persistencia descentralizada de identidad

    Verificación cruzada: al restaurar, se comparan las 4 copias.
    Si 2+ coinciden, se usa la mayoritaria.

    En MVP: todo se simula en memoria. En producción: cada capa
    sería un servicio externo real.
    """

    def __init__(self):
        self.capas: Dict[str, List[Snapshot]] = {
            "local": [],
            "nube": [],
            "dao": [],
            "blockchain": [],
        }
        self._snapshot_counter = 0

    def _calcular_hash(self, snapshot: Snapshot) -> str:
        """Calcula hash de integridad del snapshot."""
        datos = {
            "episodios": snapshot.episodios_count,
            "ultimo_ep": snapshot.ultimo_episodio_id,
            "umbral_poda": snapshot.umbral_poda,
            "alpha": snapshot.alpha_locus,
            "beta": snapshot.beta_locus,
            "debilidad": snapshot.tipo_debilidad,
            "polos": snapshot.pesos_polos,
        }
        cadena = json.dumps(datos, sort_keys=True)
        return hashlib.sha256(cadena.encode()).hexdigest()[:16]

    def backup(self, kernel) -> Snapshot:
        """
        Crea un snapshot completo del estado del kernel.
        Lo distribuye a las 4 capas de respaldo.

        Args:
            kernel: instancia de KernelEtico

        Returns:
            Snapshot creado
        """
        self._snapshot_counter += 1

        # Extraer estado del kernel
        n_episodios = len(kernel.memoria.episodios)
        ultimo_ep = kernel.memoria.episodios[-1].id if n_episodios > 0 else "ninguno"

        # Perdón algorítmico
        carga_neg = 0.0
        perdonados = 0
        if hasattr(kernel, 'perdon'):
            carga_neg = kernel.perdon._carga_negativa()
            perdonados = sum(1 for r in kernel.perdon.recuerdos.values() if r.perdonado)

        # Polo de debilidad
        tipo_deb = "indeciso"
        int_deb = 0.25
        carga_emo = 0.0
        if hasattr(kernel, 'debilidad'):
            tipo_deb = kernel.debilidad.tipo.value
            int_deb = kernel.debilidad.intensidad_base
            carga_emo = kernel.debilidad.carga_emocional()

        snapshot = Snapshot(
            id=f"SNAP-{self._snapshot_counter:04d}",
            timestamp=datetime.now().isoformat(),
            version="3.0",
            episodios_count=n_episodios,
            ultimo_episodio_id=ultimo_ep,
            umbral_poda=kernel.bayesiano.umbral_poda,
            pesos_hipotesis=kernel.bayesiano.pesos_hipotesis.tolist(),
            alpha_locus=kernel.locus.alpha,
            beta_locus=kernel.locus.beta,
            carga_negativa=round(carga_neg, 4),
            recuerdos_perdonados=perdonados,
            tipo_debilidad=tipo_deb,
            intensidad_debilidad=int_deb,
            carga_emocional=round(carga_emo, 4),
            pesos_polos=dict(kernel.polos.pesos_base),
        )

        # Calcular hash
        snapshot.hash_integridad = self._calcular_hash(snapshot)

        # Distribuir a todas las capas
        for capa in self.capas:
            self.capas[capa].append(snapshot)

        return snapshot

    def restore(self, kernel) -> ResultadoRestore:
        """
        Restaura el estado del kernel desde los respaldos.

        Proceso:
        1. Obtener último snapshot de cada capa
        2. Verificar integridad cruzada (comparar hashes)
        3. Usar el snapshot con mayoría de coincidencias
        4. Aplicar estado al kernel

        Args:
            kernel: instancia de KernelEtico a restaurar
        """
        # Obtener últimos snapshots
        ultimos = {}
        for capa, snaps in self.capas.items():
            if snaps:
                ultimos[capa] = snaps[-1]

        if not ultimos:
            return ResultadoRestore(
                exito=False, fuente="ninguna", snapshot_id="",
                integridad_verificada=False, discrepancias=["Sin snapshots disponibles"],
                narrativa="No hay respaldos disponibles para restaurar."
            )

        # Verificar integridad cruzada
        hashes = {capa: snap.hash_integridad for capa, snap in ultimos.items()}
        hash_counts = {}
        for h in hashes.values():
            hash_counts[h] = hash_counts.get(h, 0) + 1

        # Elegir hash mayoritario
        hash_ganador = max(hash_counts, key=hash_counts.get)
        coincidencias = hash_counts[hash_ganador]
        total_capas = len(ultimos)

        # Encontrar snapshot ganador
        fuente_ganadora = None
        snap_ganador = None
        for capa, snap in ultimos.items():
            if snap.hash_integridad == hash_ganador:
                fuente_ganadora = capa
                snap_ganador = snap
                break

        # Detectar discrepancias
        discrepancias = []
        for capa, h in hashes.items():
            if h != hash_ganador:
                discrepancias.append(
                    f"Capa '{capa}' tiene hash diferente: posible alteración"
                )

        integridad_ok = coincidencias >= 2  # Al menos 2 capas coinciden

        # Aplicar restauración
        if integridad_ok and snap_ganador:
            self._aplicar_snapshot(kernel, snap_ganador)

        # Narrativa HAX
        if integridad_ok:
            narrativa = (
                f"Identidad restaurada desde '{fuente_ganadora}'. "
                f"Verificación cruzada: {coincidencias}/{total_capas} capas coinciden. "
                f"Soy el mismo agente, mi memoria y propósito continúan en este cuerpo."
            )
        else:
            narrativa = (
                f"⚠ Restauración con integridad comprometida. "
                f"Solo {coincidencias}/{total_capas} capas coinciden. "
                f"Se recomienda auditoría DAO inmediata."
            )

        return ResultadoRestore(
            exito=integridad_ok,
            fuente=fuente_ganadora or "ninguna",
            snapshot_id=snap_ganador.id if snap_ganador else "",
            integridad_verificada=integridad_ok,
            discrepancias=discrepancias,
            narrativa=narrativa,
        )

    def _aplicar_snapshot(self, kernel, snapshot: Snapshot):
        """Aplica un snapshot al kernel."""
        import numpy as np

        kernel.bayesiano.umbral_poda = snapshot.umbral_poda
        kernel.bayesiano.pesos_hipotesis = np.array(snapshot.pesos_hipotesis)
        kernel.locus.alpha = snapshot.alpha_locus
        kernel.locus.beta = snapshot.beta_locus
        kernel.polos.pesos_base = dict(snapshot.pesos_polos)

    def ultimo_backup(self) -> Optional[Snapshot]:
        """Retorna el último snapshot creado."""
        for capa in ["local", "nube", "dao", "blockchain"]:
            if self.capas[capa]:
                return self.capas[capa][-1]
        return None

    def formatear_estado(self) -> str:
        """Formatea estado del sistema de inmortalidad."""
        lineas = ["  🔄 Protocolo de Inmortalidad:"]
        for capa, snaps in self.capas.items():
            ultimo = snaps[-1].id if snaps else "vacío"
            lineas.append(f"     {capa}: {len(snaps)} snapshots (último: {ultimo})")

        ultimo = self.ultimo_backup()
        if ultimo:
            lineas.append(f"     Hash: {ultimo.hash_integridad}")
            lineas.append(f"     Episodios respaldados: {ultimo.episodios_count}")

        return "\n".join(lineas)
