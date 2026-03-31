# Historial de Desarrollo — Androide Ético MVP

Registro de la evolución del proyecto desde su fase conceptual hasta la versión
actual. Este archivo preserva decisiones arquitectónicas clave, módulos
experimentales y artefactos que fueron parte del camino.

---

## Fundamentos intelectuales

El proyecto se sustenta en 104 referencias académicas de 14 disciplinas,
desde los clásicos fundacionales (Turing, Bayes, Aristóteles, Kant) hasta
la investigación contemporánea en IA safety y LLMs. Cada módulo del kernel
tiene raíces trazables en la literatura:

| Componente del kernel | Raíces principales |
|---|---|
| Inferencia bayesiana | Bayes (1763), Pearl (1988, 2018) |
| Voluntad sigmoide | Rosenblatt (1958), Kahneman (2011) |
| Memoria narrativa | Dennett (1991), Ricoeur (1984), Tulving (1972) |
| Mal Absoluto / Buffer | Kant (1785), Anthropic — Constitutional AI (2022) |
| Polos éticos | Aristóteles, Mill (1863), Floridi & Cowls (2019) |
| Modos D_fast / D_delib | Kahneman (2011), Brooks (1991), Bratman (1987) |
| Uchi-Soto | Nakane (1970), Lebra (1976), Dautenhahn (2007) |
| Sueño Ψ | Freud (1899), Walker (2017), Finn et al. — MAML (2017) |
| Mock DAO | Buterin (2014, 2021), Rawls (1971), Lamport (1982) |
| Capa LLM | Vaswani et al. (2017), Austin (1962), Bender et al. (2021) |
| Polo de debilidad | Damásio (1994), Nussbaum (2001), Brown (2012) |
| Perdón algorítmico | Ebbinghaus (1885), Arendt (1958), Enright (2000) |
| Protocolo de inmortalidad | Locke (1690), Parfit (1984), Schneier (2015) |
| Augénesis narrativa | Dennett (1992), Thagard (2006), Harari (2017) |

La bibliografía completa con las 104 referencias está en
[`docs/BIBLIOGRAPHY.md`](docs/BIBLIOGRAPHY.md).

---

## v1.0 — Marzo 2026 | Fase conceptual

- 40+ documentos de diseño analizados y consolidados.
- Arquitectura de 7 capas documentada.
- Formalización matemática completa.
- Bibliografía de 104 referencias en 14 disciplinas (ver `docs/BIBLIOGRAPHY.md`).
- **Artefacto principal:** `Androide_Etico_Analisis_Integral_v3.docx`
  (disponible en `docs/`).

## v2.0 — Marzo 2026 | Kernel base

Primer prototipo funcional con los módulos fundacionales:

| Módulo | Archivo | Rol |
|--------|---------|-----|
| Mal Absoluto | `mal_absoluto.py` | Fusible ético blindado |
| Buffer Precargado | `buffer.py` | Constitución ética inmutable (8 principios) |
| Motor Bayesiano | `bayesian_engine.py` | Evaluación probabilística de impacto |
| Polos Éticos | `ethical_poles.py` | Arbitraje multipolar (compasivo, conservador, optimista) |
| Voluntad Sigmoide | `sigmoid_will.py` | Función de decisión continua |
| Simpático-Parasimpático | `sympathetic.py` | Regulador corporal |
| Memoria Narrativa | `narrative.py` | Identidad por relatos con estado corporal |

- 9 escenarios de simulación de complejidad ética creciente.
- Dependencia única: `numpy`.

### Módulos experimentales (rama divergente, no incluidos en v3+)

Estos módulos fueron explorados en una rama paralela y representan ideas
valiosas que aún no se han integrado en la versión canónica:

- **`augenesis.py`** — Augénesis narrativa: condensaba contextos vividos en
  una línea de identidad en formación (16 hilos máximo). Concepto precursor
  de la Memoria Narrativa expandida.
- **`calibracion.py`** — Protocolo de calibración dinámica: ajustaba umbrales
  del motor bayesiano según la frecuencia reciente de modos de decisión
  (ventana de 12 episodios). Funcionalidad parcialmente absorbida por el
  Sueño Ψ en v3.
- **`locus_control.py`** — Locus de control bayesiano (versión inicial):
  mantenía P(control interno efectivo) como escalar en (0,1) y modulaba
  incertidumbre percibida. Reescrito completamente como `locus.py` en v3
  con atribución causal bayesiana completa.

## v3.0 — Marzo 2026 | Kernel integrado

Incorporó 5 módulos nuevos y el suite de tests formales:

| Módulo | Archivo | Rol |
|--------|---------|-----|
| Uchi-Soto | `uchi_soto.py` | Círculos concéntricos de confianza con dialéctica defensiva |
| Locus de Control | `locus.py` | Atribución causal bayesiana (reescritura de `locus_control.py`) |
| Sueño Ψ | `sueno_psi.py` | Auditoría retrospectiva con recalibración |
| Mock DAO | `mock_dao.py` | Gobernanza ética simulada con votación cuadrática |
| Variabilidad | `variability.py` | Ruido bayesiano controlado para naturalidad |

- **38 tests** verificando 9 propiedades éticas invariantes.
- Test de coherencia bajo variabilidad (100 runs × 9 simulaciones).
- Dashboard React (`dashboard_androide_etico.jsx`) para visualización
  interactiva de las simulaciones (artefacto de demostración, no integrado
  en el backend Python).

## v4.0 — Marzo 2026 | Capa LLM

Incorporó la capa de lenguaje natural sin comprometer la separación
kernel/comunicación:

| Módulo | Archivo | Rol |
|--------|---------|-----|
| Capa LLM | `llm_layer.py` | Percepción + comunicación + narrativa en lenguaje natural |

### Principio de diseño: **el LLM no decide, el kernel decide**

- **Percepción:** situación en texto → señales numéricas para el kernel.
- **Comunicación:** decisión del kernel → respuesta verbal (tono, gestos HAX,
  voz en off).
- **Narrativa:** evaluación multipolar → moralejas ricas y humanamente
  comprensibles.
- Soporte dual: API de Anthropic (Claude) o templates locales sin dependencia
  externa.
- Método `procesar_natural()` en kernel para ciclo completo
  texto → decisión → respuesta verbal → moralejas.

## v5.0 — Marzo 2026 | Humanización e identidad persistente (versión actual)

Integra 4 módulos que hacen al androide más creíble, resiliente y persistente:

| Módulo | Archivo | Rol |
|--------|---------|-----|
| Polo de Debilidad | `weakness_pole.py` | Imperfección narrativa intencional (5 tipos) |
| Perdón Algorítmico | `forgiveness.py` | Decaimiento exponencial de memorias negativas |
| Protocolo de Inmortalidad | `immortality.py` | Backup distribuido del alma en 4 capas |
| Augénesis Narrativa | `augenesis.py` | Creación de almas sintéticas por composición |

### Principios de diseño v5

- **El polo de debilidad nunca cambia la decisión ética.** Solo colorea la
  narrativa con matices de imperfección humanizante.
- **El perdón no es olvido.** El recuerdo permanece, su peso emocional decae:
  `Memoria(t) = Memoria_0 * e^(-δt)`.
- **La inmortalidad es verificable.** 4 copias distribuidas con hash SHA-256.
  Restauración por consenso mayoritario.
- **Cada alma creada es trazable.** La augénesis calcula coherencia narrativa
  y requiere validación DAO.

### Sueño Ψ expandido

El ciclo nocturno ahora incluye: auditoría retrospectiva → perdón algorítmico
→ carga emocional de debilidad → backup de inmortalidad.

- **51 tests** verificando 13 propiedades éticas invariantes.
- Dashboard interactivo (`dashboard.html`) para visualización en navegador.

---

## Artefactos históricos (no incluidos en el repo, disponibles localmente)

| Artefacto | Descripción |
|-----------|-------------|
| `androide-etico-mvp-v2/` | Snapshot del código v2 |
| `androide-etico-mvp-v3/` | Snapshot del código v3 (con `.pytest_cache`) |
| `androide-etico-mvp/` | Rama divergente con módulos experimentales |
| `files/androide-etico-mvp-github-ready/` | Exportación empaquetada pre-v4 |
| `files/dashboard_androide_etico.jsx` | Dashboard React de demostración (v3) |
| `EthosMVP/` | Meta-repo inicial de gobernanza colaborativa |
| `*.tar.gz` | Archivos comprimidos de cada versión |
| `Analisis_Integral_*.pdf` | Documentos de análisis integral en PDF |

---

## Roadmap (pendientes)

- [x] ~~Polo de debilidad~~ (implementado v5)
- [x] ~~Perdón algorítmico~~ (implementado v5)
- [x] ~~Protocolo de inmortalidad~~ (implementado v5)
- [x] ~~Augénesis narrativa~~ (implementado v5)
- [ ] Protocolo de calibración DAO (ajuste gradual de parámetros en testnet)
- [ ] Modo offline completo (5 capas de autonomía)
- [ ] Integración hardware (sensores, actuadores, protocolo de comunicación)
- [ ] Testnet DAO real (smart contracts en testnet Ethereum)

---

Fundación Ex Machina — 2026
