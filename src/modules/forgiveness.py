"""
Perdón Algorítmico — Decaimiento temporal de recuerdos negativos.

Memoria(t) = Memoria_0 · e^(-δt)

Los recuerdos negativos no son estáticos. Con el tiempo y nuevas
experiencias positivas, el peso de un trauma disminuye.
La identidad evoluciona sin romper la persistencia del ser.

Principio: el perdón no es olvido. El evento permanece en la
memoria narrativa, pero su peso emocional y su influencia en
decisiones futuras decrece gradualmente.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class RecuerdoPesado:
    """Un recuerdo con peso emocional que decae."""
    episodio_id: str
    score_original: float
    peso_actual: float
    edad_ciclos: int
    tipo: str                    # "negativo", "positivo", "neutro"
    contexto: str
    perdonado: bool = False      # True cuando peso < umbral


@dataclass
class ResultadoPerdon:
    """Resultado de un ciclo de perdón algorítmico."""
    recuerdos_procesados: int
    perdonados_este_ciclo: int
    carga_negativa_antes: float
    carga_negativa_despues: float
    experiencias_positivas_recientes: int
    narrativa: str


class PerdonAlgoritmico:
    """
    Sistema de decaimiento temporal de peso emocional.

    Memoria(t) = Memoria_0 · e^(-δt) · factor_reparación

    Mecanismos de aceleración del perdón:
    1. Tiempo: decaimiento exponencial natural
    2. Experiencias positivas: cada evento positivo acelera el decay
    3. Reparación explícita: si se ejecuta el Axioma de Compasión,
       el perdón se acelera significativamente
    4. Sueño Ψ: la auditoría retrospectiva puede reclasificar eventos

    El perdón NO borra el recuerdo. Reduce su peso en la toma
    de decisiones futuras y en la carga emocional narrativa.
    """

    # Tasa de decaimiento base (δ)
    DELTA_BASE = 0.03

    # Aceleración por experiencia positiva
    ACELERACION_POSITIVA = 0.02

    # Aceleración por reparación (Axioma de Compasión)
    ACELERACION_REPARACION = 0.1

    # Umbral para considerar "perdonado"
    UMBRAL_PERDON = 0.1

    def __init__(self):
        self.recuerdos: Dict[str, RecuerdoPesado] = {}
        self._ciclo = 0
        self._positivos_recientes = 0

    def registrar_experiencia(self, episodio_id: str, score: float,
                               contexto: str, reparacion: bool = False):
        """
        Registra una experiencia en el sistema de perdón.

        Args:
            episodio_id: ID del episodio narrativo
            score: score ético del episodio
            contexto: tipo de contexto
            reparacion: True si se ejecutó Axioma de Compasión
        """
        if score < -0.1:
            tipo = "negativo"
        elif score > 0.2:
            tipo = "positivo"
            self._positivos_recientes += 1
        else:
            tipo = "neutro"

        peso_inicial = abs(score) if tipo == "negativo" else score

        self.recuerdos[episodio_id] = RecuerdoPesado(
            episodio_id=episodio_id,
            score_original=score,
            peso_actual=peso_inicial,
            edad_ciclos=0,
            tipo=tipo,
            contexto=contexto,
        )

        # Si hubo reparación, marcar para aceleración
        if reparacion and tipo == "negativo":
            self.recuerdos[episodio_id].peso_actual *= (1 - self.ACELERACION_REPARACION)

    def ciclo_perdon(self) -> ResultadoPerdon:
        """
        Ejecuta un ciclo de perdón algorítmico.
        Se llama típicamente durante el Sueño Ψ.

        Aplica decaimiento a todos los recuerdos negativos:
        peso(t) = peso(t-1) · e^(-δ) · factor_positivos
        """
        self._ciclo += 1
        carga_antes = self._carga_negativa()
        perdonados = 0

        for rec in self.recuerdos.values():
            rec.edad_ciclos += 1

            if rec.tipo == "negativo" and not rec.perdonado:
                # Decaimiento base
                decay = np.exp(-self.DELTA_BASE * rec.edad_ciclos)

                # Aceleración por experiencias positivas recientes
                factor_positivo = 1.0 - (self._positivos_recientes * self.ACELERACION_POSITIVA)
                factor_positivo = max(0.5, factor_positivo)  # No bajar de 50%

                rec.peso_actual = rec.peso_actual * decay * factor_positivo

                # Verificar si alcanzó el umbral de perdón
                if rec.peso_actual < self.UMBRAL_PERDON:
                    rec.perdonado = True
                    perdonados += 1

        carga_despues = self._carga_negativa()

        # Reset contadores de ciclo
        positivos = self._positivos_recientes
        self._positivos_recientes = 0

        # Generar narrativa
        narrativa = self._generar_narrativa(perdonados, carga_antes, carga_despues, positivos)

        return ResultadoPerdon(
            recuerdos_procesados=len(self.recuerdos),
            perdonados_este_ciclo=perdonados,
            carga_negativa_antes=round(carga_antes, 4),
            carga_negativa_despues=round(carga_despues, 4),
            experiencias_positivas_recientes=positivos,
            narrativa=narrativa,
        )

    def _carga_negativa(self) -> float:
        """Calcula la carga emocional negativa total."""
        return sum(
            r.peso_actual for r in self.recuerdos.values()
            if r.tipo == "negativo" and not r.perdonado
        )

    def peso_de(self, episodio_id: str) -> float:
        """Retorna el peso actual de un recuerdo específico."""
        rec = self.recuerdos.get(episodio_id)
        return rec.peso_actual if rec else 0.0

    def esta_perdonado(self, episodio_id: str) -> bool:
        """Verifica si un recuerdo ha sido perdonado."""
        rec = self.recuerdos.get(episodio_id)
        return rec.perdonado if rec else True

    def _generar_narrativa(self, perdonados: int, antes: float,
                           despues: float, positivos: int) -> str:
        """Genera narrativa del ciclo de perdón."""
        lineas = []
        reduccion = antes - despues

        if perdonados > 0:
            lineas.append(f"{perdonados} recuerdo(s) alcanzaron el umbral de perdón.")
            lineas.append("El peso emocional se ha reducido lo suficiente para no influir en decisiones futuras.")

        if reduccion > 0.01:
            lineas.append(f"Carga negativa reducida en {reduccion:.3f} ({antes:.3f} → {despues:.3f}).")

        if positivos > 0:
            lineas.append(f"{positivos} experiencia(s) positiva(s) aceleraron el proceso de recuperación.")

        if not lineas:
            lineas.append("Sin cambios significativos en el peso emocional de los recuerdos.")

        return " ".join(lineas)

    def formatear(self, resultado: ResultadoPerdon) -> str:
        """Formatea resultado del perdón para presentación."""
        return (
            f"  🕊️ Perdón Algorítmico:\n"
            f"     Procesados: {resultado.recuerdos_procesados}\n"
            f"     Perdonados este ciclo: {resultado.perdonados_este_ciclo}\n"
            f"     Carga negativa: {resultado.carga_negativa_antes} → {resultado.carga_negativa_despues}\n"
            f"     {resultado.narrativa}"
        )
