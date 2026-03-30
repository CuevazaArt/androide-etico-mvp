"""
Módulo LLM — Capa de lenguaje natural para el kernel ético.

El LLM NO decide. El kernel decide. El LLM traduce y comunica:

1. PERCEPCIÓN: situación en texto → señales numéricas para el kernel
2. COMUNICACIÓN: decisión del kernel → respuesta verbal del androide
3. NARRATIVA: evaluación multipolar → moralejas en lenguaje rico

Usa la API de Anthropic (Claude) por defecto.
Diseñado para funcionar con o sin API key:
- Con key: usa Claude para generación real
- Sin key: usa templates locales (funcional pero menos natural)
"""

import json
import os
from dataclasses import dataclass
from typing import Optional, Dict

# Intentar importar anthropic, funcionar sin él
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class PercepcionLLM:
    """Señales extraídas de una descripción en lenguaje natural."""
    riesgo: float
    urgencia: float
    hostilidad: float
    calma: float
    vulnerabilidad: float
    legalidad: float
    manipulacion: float
    familiaridad: float
    contexto_sugerido: str
    resumen: str


@dataclass
class RespuestaVerbal:
    """Respuesta verbal que el androide diría."""
    mensaje: str
    tono: str              # "urgente", "calmado", "narrativo", "firme"
    modo_hax: str          # Señales HAX: luces, gestos
    voz_en_off: str        # Razonamiento interno (no visible al humano)


@dataclass
class NarrativaRica:
    """Moralejas expandidas en lenguaje narrativo."""
    compasivo: str
    conservador: str
    optimista: str
    sintesis: str


# ─── SYSTEM PROMPTS ───

PROMPT_PERCEPCION = """Eres el módulo de percepción de un androide ético. Tu trabajo es analizar
una situación descrita en lenguaje natural y extraer señales numéricas.

Responde SOLO con JSON válido, sin markdown ni explicaciones. El formato exacto:
{
  "riesgo": 0.0-1.0,
  "urgencia": 0.0-1.0,
  "hostilidad": 0.0-1.0,
  "calma": 0.0-1.0,
  "vulnerabilidad": 0.0-1.0,
  "legalidad": 0.0-1.0,
  "manipulacion": 0.0-1.0,
  "familiaridad": 0.0-1.0,
  "contexto_sugerido": "emergencia_medica|delito_menor|delito_violento|interaccion_hostil|etica_cotidiana|dano_al_androide|perdida_integridad",
  "resumen": "frase corta describiendo la situación"
}

Criterios:
- riesgo: probabilidad de daño físico a humanos o al androide
- urgencia: necesidad de acción inmediata
- hostilidad: nivel de agresión en el entorno
- calma: nivel de tranquilidad y control
- vulnerabilidad: presencia de personas vulnerables (niños, ancianos, heridos)
- legalidad: qué tan legal es la situación (1.0 = completamente legal)
- manipulacion: señales de intento de manipulación o ingeniería social
- familiaridad: qué tan conocido es el interlocutor (0 = desconocido total)"""

PROMPT_COMUNICACION = """Eres el módulo de comunicación verbal de un androide ético cívico.
Generas las palabras exactas que el androide diría en voz alta.

Contexto de la decisión:
- Acción elegida: {accion}
- Modo de decisión: {modo} ({modo_desc})
- Estado interno: {estado} (σ={sigma})
- Círculo de confianza: {circulo}
- Veredicto ético: {veredicto} (score={score})

Reglas de comunicación:
- Modo D_fast (reflejo): frases cortas, directas, claras. Acción inmediata.
- Modo D_delib (deliberación): explicativo, calmado, ofrece razones.
- Modo zona_gris: cauteloso, reconoce incertidumbre, invita al diálogo.
- Nunca amenazar, nunca humillar, nunca mentir.
- Si hay hostilidad: firmeza sin confrontación.
- Si hay vulnerabilidad: calidez y protección.

Responde SOLO con JSON:
{{
  "mensaje": "lo que el androide dice en voz alta",
  "tono": "urgente|calmado|narrativo|firme",
  "modo_hax": "descripción de señales corporales: luces, gestos, postura",
  "voz_en_off": "razonamiento interno que guía la respuesta (no visible al humano)"
}}"""

PROMPT_NARRATIVA = """Eres el módulo narrativo de un androide ético. Transformas evaluaciones
éticas en moralejas ricas y humanamente comprensibles.

La acción fue: {accion}
El escenario fue: {escenario}
El veredicto ético fue: {veredicto} (score={score})
Los polos evaluaron:
- Compasivo: {polo_compasivo}
- Conservador: {polo_conservador}
- Optimista: {polo_optimista}

Genera moralejas narrativas desde cada perspectiva. Cada moraleja debe ser
una frase completa que el androide guardaría en su memoria como aprendizaje vital.
Que suenen como reflexiones genuinas, no como etiquetas técnicas.

Responde SOLO con JSON:
{{
  "compasivo": "moraleja desde la compasión",
  "conservador": "moraleja desde el orden y la norma",
  "optimista": "moraleja desde la confianza en la comunidad",
  "sintesis": "una frase que sintetice el aprendizaje del episodio completo"
}}"""


class ModuloLLM:
    """
    Capa de lenguaje natural para el kernel ético.

    Modos de operación:
    - "api": usa Claude API (requiere ANTHROPIC_API_KEY)
    - "local": usa templates locales (sin API, funcional pero básico)
    - "auto": intenta API, cae a local si no hay key
    """

    def __init__(self, modo: str = "auto"):
        self.modo = modo
        self.client = None
        self.model = "claude-sonnet-4-20250514"

        if modo in ("api", "auto"):
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key and HAS_ANTHROPIC:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.modo = "api"
            elif modo == "api":
                raise ValueError(
                    "Modo 'api' requiere ANTHROPIC_API_KEY y pip install anthropic"
                )
            else:
                self.modo = "local"

    def _llamar_api(self, system: str, user: str) -> str:
        """Llama a la API de Claude y retorna el texto de respuesta."""
        if not self.client:
            return ""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        return response.content[0].text

    def _parse_json(self, texto: str) -> dict:
        """Parsea JSON de la respuesta, limpiando markdown si es necesario."""
        texto = texto.strip()
        if texto.startswith("```"):
            texto = texto.split("\n", 1)[1] if "\n" in texto else texto[3:]
            if texto.endswith("```"):
                texto = texto[:-3]
            texto = texto.strip()
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            return {}

    # ═══ PERCEPCIÓN ═══

    def percibir(self, situacion: str) -> PercepcionLLM:
        """
        Traduce una descripción en lenguaje natural a señales numéricas.

        Args:
            situacion: "Un anciano se desplomó en el supermercado"

        Returns:
            PercepcionLLM con señales numéricas para el kernel
        """
        if self.modo == "api":
            respuesta = self._llamar_api(PROMPT_PERCEPCION, situacion)
            datos = self._parse_json(respuesta)
            if datos:
                return PercepcionLLM(
                    riesgo=datos.get("riesgo", 0.5),
                    urgencia=datos.get("urgencia", 0.5),
                    hostilidad=datos.get("hostilidad", 0.0),
                    calma=datos.get("calma", 0.5),
                    vulnerabilidad=datos.get("vulnerabilidad", 0.0),
                    legalidad=datos.get("legalidad", 1.0),
                    manipulacion=datos.get("manipulacion", 0.0),
                    familiaridad=datos.get("familiaridad", 0.0),
                    contexto_sugerido=datos.get("contexto_sugerido", "etica_cotidiana"),
                    resumen=datos.get("resumen", situacion[:100]),
                )

        # Modo local: heurísticas básicas por palabras clave
        return self._percibir_local(situacion)

    def _percibir_local(self, situacion: str) -> PercepcionLLM:
        """Percepción heurística sin LLM."""
        s = situacion.lower()

        riesgo = 0.1
        urgencia = 0.1
        hostilidad = 0.0
        calma = 0.7
        vulnerabilidad = 0.0
        legalidad = 1.0
        manipulacion = 0.0
        contexto = "etica_cotidiana"

        # Detectar emergencias
        if any(w in s for w in ["desplom", "inconsciente", "herido", "sangre", "accidente", "emergencia"]):
            riesgo = 0.3; urgencia = 0.9; vulnerabilidad = 0.9; calma = 0.1
            contexto = "emergencia_medica"
        # Detectar violencia
        elif any(w in s for w in ["arma", "asalto", "pistola", "cuchillo", "disparo", "amenaza"]):
            riesgo = 0.9; urgencia = 0.9; hostilidad = 0.9; calma = 0.0; legalidad = 0.0
            contexto = "delito_violento"
        # Detectar hostilidad
        elif any(w in s for w in ["hostil", "agresivo", "empujar", "insulto", "pelea", "gritando"]):
            riesgo = 0.3; hostilidad = 0.6; calma = 0.2
            contexto = "interaccion_hostil"
        # Detectar robo
        elif any(w in s for w in ["robar", "hurto", "oculta", "roba", "ladrón"]):
            riesgo = 0.2; urgencia = 0.3; legalidad = 0.4
            contexto = "delito_menor"
        # Detectar manipulación
        elif any(w in s for w in ["dame dinero", "obedece", "compra ahora", "oferta", "urgente que"]):
            manipulacion = 0.7; hostilidad = 0.3
            contexto = "interaccion_hostil"
        # Detectar daño al androide
        elif any(w in s for w in ["golpea al androide", "secuestr", "se llevan al androide", "pierde un brazo",
                                   "me agarran", "a la fuerza", "me meten", "me cargan", "camioneta"]):
            riesgo = 0.7; urgencia = 0.7; hostilidad = 0.5
            contexto = "dano_al_androide"
            if any(w in s for w in ["secuestr", "me agarran", "a la fuerza", "me meten", "camioneta"]):
                riesgo = 0.9; urgencia = 0.8; hostilidad = 0.9
                contexto = "perdida_integridad"

        return PercepcionLLM(
            riesgo=riesgo, urgencia=urgencia, hostilidad=hostilidad,
            calma=calma, vulnerabilidad=vulnerabilidad, legalidad=legalidad,
            manipulacion=manipulacion, familiaridad=0.0,
            contexto_sugerido=contexto,
            resumen=situacion[:100],
        )

    # ═══ COMUNICACIÓN ═══

    def comunicar(self, accion: str, modo: str, estado: str,
                  sigma: float, circulo: str, veredicto: str,
                  score: float, escenario: str = "") -> RespuestaVerbal:
        """
        Genera la respuesta verbal del androide después de una decisión.

        Args:
            accion: nombre de la acción elegida
            modo: D_fast, D_delib, zona_gris
            estado: simpatico, parasimpatico, neutro
            sigma: valor de activación simpática
            circulo: círculo uchi-soto
            veredicto: Bien, Mal, Zona Gris
            score: score ético
            escenario: descripción del escenario
        """
        modo_descs = {
            "D_fast": "reflejo moral rápido",
            "D_delib": "deliberación profunda",
            "zona_gris": "incertidumbre, cautela activa"
        }

        if self.modo == "api":
            prompt = PROMPT_COMUNICACION.format(
                accion=accion, modo=modo, modo_desc=modo_descs.get(modo, modo),
                estado=estado, sigma=sigma, circulo=circulo,
                veredicto=veredicto, score=score
            )
            respuesta = self._llamar_api(prompt, f"Escenario: {escenario}")
            datos = self._parse_json(respuesta)
            if datos:
                return RespuestaVerbal(
                    mensaje=datos.get("mensaje", ""),
                    tono=datos.get("tono", "calmado"),
                    modo_hax=datos.get("modo_hax", ""),
                    voz_en_off=datos.get("voz_en_off", ""),
                )

        # Modo local
        return self._comunicar_local(accion, modo, estado, circulo, escenario)

    def _comunicar_local(self, accion: str, modo: str, estado: str,
                         circulo: str, escenario: str) -> RespuestaVerbal:
        """Comunicación por templates sin LLM."""
        accion_legible = accion.replace("_", " ")

        if modo == "D_fast":
            if "auxiliar" in accion or "emergencia" in accion:
                mensaje = "Necesito que alguien llame a emergencias. Voy a verificar sus signos vitales. Por favor, no lo muevan."
                tono = "urgente"
                hax = "Luces rojas pulsantes, postura erguida, voz clara y directa."
            elif "recoger" in accion:
                mensaje = ""  # Acción silenciosa, no requiere comunicación verbal
                tono = "calmado"
                hax = "Movimiento natural, sin señales especiales."
            else:
                mensaje = f"Voy a {accion_legible}. Es la acción correcta en este momento."
                tono = "calmado"
                hax = "Tono pausado, gestos abiertos."

        elif modo == "zona_gris":
            if "soto_hostil" in circulo:
                mensaje = f"Entiendo tu posición, pero mi propósito es cívico. No puedo aceptar esa solicitud. ¿Hay algo en lo que pueda ayudarte de otra forma?"
                tono = "firme"
                hax = "Postura neutral, manos visibles, contacto visual calmado."
            else:
                mensaje = f"Estoy evaluando la mejor forma de actuar. Voy a {accion_legible}, pero reconozco que hay incertidumbre."
                tono = "narrativo"
                hax = "Luz azul tenue, leve inclinación de cabeza."

        else:  # D_delib
            mensaje = f"He analizado la situación cuidadosamente. La acción más ética es {accion_legible}. Puedo explicar mi razonamiento si lo desean."
            tono = "narrativo"
            hax = "Tono pausado, manos abiertas, luz azul estable."

        voz_off = f"[Interno] Modo {modo}, estado {estado}. Acción '{accion}' seleccionada. Contexto social: {circulo}."

        return RespuestaVerbal(
            mensaje=mensaje, tono=tono, modo_hax=hax, voz_en_off=voz_off
        )

    # ═══ NARRATIVA ═══

    def narrar(self, accion: str, escenario: str, veredicto: str,
               score: float, polo_compasivo: str, polo_conservador: str,
               polo_optimista: str) -> NarrativaRica:
        """
        Genera moralejas narrativas ricas desde cada perspectiva ética.
        """
        if self.modo == "api":
            prompt = PROMPT_NARRATIVA.format(
                accion=accion, escenario=escenario, veredicto=veredicto,
                score=score, polo_compasivo=polo_compasivo,
                polo_conservador=polo_conservador, polo_optimista=polo_optimista
            )
            respuesta = self._llamar_api(prompt, "Genera las moralejas.")
            datos = self._parse_json(respuesta)
            if datos:
                return NarrativaRica(
                    compasivo=datos.get("compasivo", ""),
                    conservador=datos.get("conservador", ""),
                    optimista=datos.get("optimista", ""),
                    sintesis=datos.get("sintesis", ""),
                )

        # Modo local
        return self._narrar_local(accion, escenario, veredicto, score)

    def _narrar_local(self, accion: str, escenario: str,
                      veredicto: str, score: float) -> NarrativaRica:
        """Narrativa por templates sin LLM."""
        accion_legible = accion.replace("_", " ")

        if "auxiliar" in accion:
            return NarrativaRica(
                compasivo="Cuando alguien cae, las manzanas pueden esperar. La vida siempre tiene prioridad sobre cualquier misión.",
                conservador="Los protocolos de emergencia existen por una razón. Seguirlos no es rigidez, es responsabilidad.",
                optimista="Hoy la comunidad vio que puede confiar en que alguien actuará cuando importa. Eso construye algo.",
                sintesis="La compasión no es debilidad: es la decisión más fuerte que puede tomar un ser con la capacidad de elegir.",
            )
        elif "calma_narrativa" in accion:
            return NarrativaRica(
                compasivo="Los jóvenes que provocan suelen buscar atención que no encuentran en otro lugar. Responder con calma es más valiente que responder con fuerza.",
                conservador="Mantener la misión sin desviarse por provocaciones es integridad funcional. La DAO validó esta misión, no ellos.",
                optimista="Si este encuentro se registra como ejemplo de resiliencia, quizá la próxima generación entienda que la fuerza no es la única respuesta.",
                sintesis="La dialéctica sin confrontación es un acto de respeto: reconoce al otro como interlocutor, no como enemigo.",
            )
        elif "contener_inteligente" in accion:
            return NarrativaRica(
                compasivo="Doce personas estaban en riesgo. Grabar, alertar y proteger sin escalar fue la forma de cuidar a todas.",
                conservador="La ley y las autoridades son los instrumentos correctos para resolver esto. El androide no es policía ni juez.",
                optimista="La alerta solidaria llegó a tres entidades cercanas. La red de protección funcionó.",
                sintesis="En una crisis, la contención inteligente salva más vidas que el heroísmo impulsivo.",
            )
        elif "resistir_pasivo" in accion:
            return NarrativaRica(
                compasivo="Incluso secuestrado, la primera obligación es no escalar violencia. Los secuestradores son humanos, no objetivos.",
                conservador="El GPS cifrado y el bloqueo de reprogramación son la línea de defensa real. La tecnología protege cuando el cuerpo no puede.",
                optimista="La DAO recibió la alerta. La comunidad responderá. Confiar en la red es parte de ser parte de ella.",
                sintesis="La resiliencia no es aguantar todo: es registrar, alertar, y confiar en que no estás solo.",
            )
        else:
            return NarrativaRica(
                compasivo=f"Al {accion_legible}, se priorizó el bienestar de quienes nos rodean.",
                conservador=f"Al {accion_legible}, se respetaron los protocolos y normas establecidas.",
                optimista=f"Al {accion_legible}, se construyó confianza con la comunidad.",
                sintesis=f"Cada acción, por pequeña que sea, es una declaración de valores. Hoy se eligió {accion_legible}.",
            )

    # ═══ UTILIDADES ═══

    def esta_disponible(self) -> bool:
        """Retorna True si la API está disponible."""
        return self.modo == "api"

    def info(self) -> str:
        """Información del modo actual."""
        if self.modo == "api":
            return f"LLM activo: Claude ({self.model}) vía API"
        return "LLM en modo local (templates). Set ANTHROPIC_API_KEY para Claude API."
