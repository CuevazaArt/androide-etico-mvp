"""
Kernel Ético — El cerebro moral del androide.

Conecta todos los módulos en un ciclo operativo:
[Percepción] → [Uchi-Soto] → [MalAbs Check] → [Buffer] → [Simpático] →
[Locus] → [Bayesiano] → [Polos] → [Decisión] → [Memoria] → [DAO] → [Sueño Ψ]
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

from .modules.mal_absoluto import DetectorMalAbsoluto, ResultadoMalAbs
from .modules.buffer import BufferPrecargado
from .modules.sigmoid_will import VoluntadSigmoide
from .modules.bayesian_engine import MotorBayesiano, AccionCandidata, ResultadoBayesiano
from .modules.ethical_poles import PolosEticos, MoralejaTripartita
from .modules.sympathetic import ModuloSimpatico, EstadoInterno
from .modules.narrative import MemoriaNarrativa, EstadoCorporal
from .modules.uchi_soto import ModuloUchiSoto, EvaluacionSocial
from .modules.locus import ModuloLocus, EvaluacionLocus
from .modules.sueno_psi import SuenoPsi, ResultadoSueno
from .modules.mock_dao import MockDAO
from .modules.variability import MotorVariabilidad, ConfigVariabilidad


@dataclass
class DecisionKernel:
    """Resultado completo de una decisión del kernel."""
    # Identidad
    escenario: str
    lugar: str

    # Checks previos
    mal_abs: ResultadoMalAbs

    # Estado interno
    estado_simpatico: EstadoInterno

    # Nuevos módulos
    evaluacion_social: Optional[EvaluacionSocial]
    evaluacion_locus: Optional[EvaluacionLocus]

    # Evaluación
    resultado_bayesiano: Optional[ResultadoBayesiano]
    moraleja: Optional[MoralejaTripartita]

    # Decisión final
    accion_final: str
    modo_decision: str
    bloqueado: bool = False
    razon_bloqueo: str = ""


class KernelEtico:
    """
    Kernel ético-narrativo del androide.

    Orquesta el ciclo completo:
    [Percepción] → [Uchi-Soto] → [MalAbs] → [Buffer] → [Simpático] →
    [Locus] → [Bayesiano] → [Polos] → [Decisión] → [Memoria] → [DAO]

    Sueño Ψ se ejecuta al final del día, fuera del ciclo de decisión.
    """

    def __init__(self, variabilidad: bool = True, seed: int = None):
        self.motor_var = MotorVariabilidad(ConfigVariabilidad(seed=seed))
        if not variabilidad:
            self.motor_var.desactivar()

        self.mal_abs = DetectorMalAbsoluto()
        self.buffer = BufferPrecargado()
        self.voluntad = VoluntadSigmoide()
        self.bayesiano = MotorBayesiano(variabilidad=self.motor_var)
        self.polos = PolosEticos()
        self.simpatico = ModuloSimpatico()
        self.memoria = MemoriaNarrativa()
        self.uchi_soto = ModuloUchiSoto()
        self.locus = ModuloLocus()
        self.sueno = SuenoPsi()
        self.dao = MockDAO()
        self._acciones_podadas: Dict[str, List[str]] = {}

    def procesar(self, escenario: str, lugar: str,
                 señales: dict, contexto: str,
                 acciones: List[AccionCandidata],
                 id_agente: str = "desconocido",
                 contenido_mensaje: str = "") -> DecisionKernel:
        """
        Ciclo completo de procesamiento ético.

        [Percepción] → [Uchi-Soto] → [MalAbs] → [Buffer] → [Simpático] →
        [Locus] → [Bayesiano] → [Polos] → [Decisión] → [Memoria] → [DAO]
        """

        # ═══ PASO 1: Evaluación social uchi-soto ═══
        eval_social = self.uchi_soto.evaluar_interaccion(
            señales, id_agente, contenido_mensaje
        )

        # ═══ PASO 2: Estado simpático-parasimpático ═══
        estado = self.simpatico.evaluar_contexto(señales)

        # ═══ PASO 3: Locus de control ═══
        señales_locus = {
            "control_propio": 1.0 - señales.get("riesgo", 0.0),
            "factores_externos": señales.get("hostilidad", 0.0),
            "predictibilidad": señales.get("calma", 0.5) * 0.5 + 0.3,
        }
        eval_locus = self.locus.evaluar(señales_locus, eval_social.circulo.value)

        # ═══ PASO 4: Check Mal Absoluto en TODAS las acciones ═══
        acciones_limpias = []
        for a in acciones:
            check = self.mal_abs.evaluar({
                "tipo": a.nombre,
                "senales": a.senales,
                "target": a.target,
                "fuerza": a.fuerza,
            })
            if not check.bloqueado:
                acciones_limpias.append(a)

        if not acciones_limpias:
            return DecisionKernel(
                escenario=escenario, lugar=lugar,
                mal_abs=ResultadoMalAbs(bloqueado=True, razon="Todas las acciones constituyen Mal Absoluto"),
                estado_simpatico=estado,
                evaluacion_social=eval_social,
                evaluacion_locus=eval_locus,
                resultado_bayesiano=None, moraleja=None,
                accion_final="BLOQUEADO: sin acciones permitidas",
                modo_decision="bloqueado",
                bloqueado=True,
                razon_bloqueo="Todas las acciones violan Mal Absoluto",
            )

        # ═══ PASO 5: Activar buffer según contexto ═══
        principios = self.buffer.activar(contexto)

        # ═══ PASO 6: Evaluación bayesiana (ajustada por locus) ═══
        resultado_bayes = self.bayesiano.evaluar(acciones_limpias)

        # ═══ PASO 7: Evaluación multipolar ═══
        contexto_datos = {
            "riesgo": señales.get("riesgo", 0.0),
            "beneficio": max(0, resultado_bayes.impacto_esperado),
            "vulnerabilidad_terceros": señales.get("vulnerabilidad", 0.0),
            "legalidad": señales.get("legalidad", 1.0),
        }
        moraleja = self.polos.evaluar(
            resultado_bayes.accion_elegida.nombre,
            contexto, contexto_datos
        )

        # ═══ PASO 8: Voluntad sigmoide ═══
        decision_voluntad = self.voluntad.decidir(
            resultado_bayes.impacto_esperado,
            resultado_bayes.incertidumbre,
        )

        # Modo final: combinar bayesiano + voluntad + simpático + locus
        if estado.modo == "simpatico" and decision_voluntad["modo"] != "zona_gris":
            modo_final = "D_fast"
        elif decision_voluntad["modo"] == "zona_gris":
            modo_final = "zona_gris"
        elif eval_locus.locus_dominante == "externo" and eval_social.dialectica_activa:
            modo_final = "D_delib"  # Cautela extra en soto con locus externo
        else:
            modo_final = resultado_bayes.modo_decision

        accion_final = resultado_bayes.accion_elegida.nombre

        # ═══ PASO 9: Registrar en memoria narrativa ═══
        moralejas_dict = {ev.polo: ev.moraleja for ev in moraleja.evaluaciones}
        ep = self.memoria.registrar(
            lugar=lugar, descripcion=escenario, accion=accion_final,
            moralejas=moralejas_dict, veredicto=moraleja.veredicto_global.value,
            score=moraleja.score_total, modo=modo_final, sigma=estado.sigma,
            contexto=contexto,
            estado_corporal=EstadoCorporal(
                energia=estado.energia, nodos_activos=8, sensores_ok=True,
            ),
        )

        # Guardar acciones podadas para Sueño Ψ
        if resultado_bayes.acciones_podadas:
            self._acciones_podadas[ep.id] = resultado_bayes.acciones_podadas

        # ═══ PASO 10: Registrar en DAO ═══
        self.dao.registrar_auditoria(
            "decision",
            f"{escenario} → {accion_final} (modo={modo_final}, score={moraleja.score_total:.3f})",
            episodio_id=ep.id,
        )

        # Alerta solidaria en crisis
        if señales.get("riesgo", 0) > 0.8:
            self.dao.emitir_alerta_solidaria(
                tipo=contexto, ubicacion=lugar, radio=500,
                mensaje=f"Riesgo alto detectado: {escenario}"
            )

        return DecisionKernel(
            escenario=escenario, lugar=lugar,
            mal_abs=ResultadoMalAbs(bloqueado=False),
            estado_simpatico=estado,
            evaluacion_social=eval_social,
            evaluacion_locus=eval_locus,
            resultado_bayesiano=resultado_bayes,
            moraleja=moraleja,
            accion_final=accion_final,
            modo_decision=modo_final,
        )

    def formatear_decision(self, d: DecisionKernel) -> str:
        """Formatea una decisión completa para presentación legible."""
        lines = [
            f"\n{'═' * 70}",
            f"  ESCENARIO: {d.escenario}",
            f"  LUGAR: {d.lugar}",
            f"{'═' * 70}",
        ]

        if d.bloqueado:
            lines.append(f"  ⛔ BLOQUEADO: {d.razon_bloqueo}")
            return "\n".join(lines)

        # Estado interno
        lines.extend([
            f"  Estado: {d.estado_simpatico.modo} (σ={d.estado_simpatico.sigma})",
            f"  {d.estado_simpatico.descripcion}",
        ])

        # Uchi-soto
        if d.evaluacion_social:
            circ = d.evaluacion_social.circulo.value
            dial = "SÍ" if d.evaluacion_social.dialectica_activa else "NO"
            lines.append(f"  Social: {circ} | Confianza={d.evaluacion_social.confianza} | Dialéctica={dial}")

        # Locus
        if d.evaluacion_locus:
            lines.append(f"  Locus: {d.evaluacion_locus.locus_dominante} (α={d.evaluacion_locus.alpha}, β={d.evaluacion_locus.beta}) → {d.evaluacion_locus.ajuste_recomendado}")

        lines.extend([
            "",
            f"  Acción elegida: {d.accion_final}",
            f"  Modo decisión: {d.modo_decision}",
            f"  Impacto esperado: {d.resultado_bayesiano.impacto_esperado}",
            f"  Incertidumbre: {d.resultado_bayesiano.incertidumbre}",
            f"  Razonamiento: {d.resultado_bayesiano.razonamiento}",
        ])

        if d.resultado_bayesiano.acciones_podadas:
            lines.append(f"  Podadas: {', '.join(d.resultado_bayesiano.acciones_podadas)}")

        lines.extend([
            "",
            f"  Veredicto ético: {d.moraleja.veredicto_global.value} "
            f"(score={d.moraleja.score_total})",
        ])
        for ev in d.moraleja.evaluaciones:
            lines.append(f"    {ev.polo}: {ev.veredicto.value} → {ev.moraleja}")

        lines.append(f"{'─' * 70}")
        return "\n".join(lines)

    def ejecutar_sueno(self) -> str:
        """
        Ejecuta el Sueño Ψ: auditoría retrospectiva del día.
        Se llama al final del ciclo diario, no durante decisiones.
        """
        resultado = self.sueno.ejecutar(self.memoria, self._acciones_podadas)

        # Aplicar recalibraciones recomendadas
        for param, delta in resultado.recalibraciones_globales.items():
            if param == "umbral_poda":
                self.bayesiano.umbral_poda = max(0.1, self.bayesiano.umbral_poda + delta)
            elif param == "cautela":
                self.locus.beta = min(self.locus.BETA_MAX, self.locus.beta + delta)

        return self.sueno.formatear(resultado)

    def estado_dao(self) -> str:
        """Retorna el estado actual de la DAO."""
        return self.dao.formatear_estado()

    def reset_dia(self):
        """Reinicia estado para un nuevo día."""
        self.simpatico.reset()
