# Changelog

## v5.0 — Marzo 2026
### Módulos de humanización e identidad persistente
- **Polo de Debilidad** (`weakness_pole.py`): imperfección narrativa intencional
  - 5 tipos: quejumbroso, indeciso, ansioso, distraído, rígido
  - Colorea la experiencia sin alterar la decisión ética
  - Decaimiento temporal para prevenir acumulación patológica
- **Perdón Algorítmico** (`forgiveness.py`): Memoria(t) = Memoria_0 * e^(-dt)
  - Decaimiento exponencial de peso emocional negativo
  - Aceleración por experiencias positivas y reparación explícita
  - Umbral de perdón: el evento permanece pero deja de influir
- **Protocolo de Inmortalidad** (`immortality.py`): backup distribuido del alma
  - 4 capas: local, nube, DAO, blockchain
  - Verificación cruzada de integridad por hash SHA-256
  - Restauración por consenso mayoritario (2+ capas coinciden)
- **Augénesis Narrativa** (`augenesis.py`): creación de almas sintéticas
  - 4 perfiles predefinidos: protector, explorador, pedagogo, resiliente
  - Integración de fragmentos narrativos de otros androides
  - Cálculo de coherencia: CausalPaths_valid / CausalPaths_total

### Integración en kernel
- Sueño Ψ expandido: auditoría + perdón + carga debilidad + backup
- 51 tests verificando 13 propiedades éticas invariantes
- Pipeline ampliado: [Decisión] → [Debilidad] → [Perdón] → [Memoria] → [DAO]

## v4.0 — Marzo 2026
### Capa LLM (Lenguaje Natural)
- **Módulo LLM** (`llm_layer.py`): capa de lenguaje natural que traduce y comunica sin participar en la decisión ética
  - **Percepción**: situación en texto → señales numéricas para el kernel
  - **Comunicación**: decisión del kernel → respuesta verbal del androide (tono, gestos HAX, voz en off)
  - **Narrativa**: evaluación multipolar → moralejas en lenguaje rico y humanamente comprensible
- Soporte dual: API de Anthropic (Claude) cuando hay key, templates locales sin dependencia externa
- Modo `"auto"` detecta disponibilidad y cae gracefully a modo local

### Integración en Kernel
- Nuevo método `procesar_natural()`: ciclo completo texto → decisión → respuesta verbal → moralejas
- Generación automática de acciones candidatas según contexto percibido (7 tipos de contexto)
- Formateo enriquecido con voz en on/off, señales HAX y moralejas narrativas expandidas
- Arquitectura de separación estricta: **el LLM no decide, el kernel decide**

### Mejoras al ciclo operativo
- System prompts especializados para percepción, comunicación y narrativa
- Parsing robusto de JSON con limpieza automática de markdown
- Dataclasses `PercepcionLLM`, `RespuestaVerbal` y `NarrativaRica` para tipado fuerte
- Heurísticas locales por palabras clave como fallback sin API

## v3.0 — Marzo 2026
### Módulos nuevos
- **Uchi-Soto**: Círculos concéntricos de confianza con dialéctica defensiva
- **Locus de Control**: Atribución causal bayesiana entre agencia propia y entorno
- **Sueño Ψ**: Auditoría retrospectiva que recalibra parámetros tras cada día
- **Mock DAO**: Gobernanza ética simulada con votación cuadrática y alertas solidarias
- **Variabilidad Bayesiana**: Ruido controlado para naturalidad sin perder coherencia

### Tests formales
- 38 tests que verifican 9 propiedades éticas invariantes
- Test de coherencia bajo variabilidad (100 runs por simulación)
- Verificación de jerarquía de valores (vida > misión, nunca violencia)

## v2.0 — Marzo 2026
### Kernel completo
- Mal Absoluto (fusible ético blindado)
- Buffer Precargado (constitución ética inmutable)
- Motor Bayesiano (evaluación de impacto ético)
- Polos Éticos (arbitraje multipolar dinámico)
- Voluntad Sigmoide (función de decisión)
- Simpático-Parasimpático (regulador corporal)
- Memoria Narrativa (identidad por relatos con estado corporal)

### Simulaciones
- 9 escenarios de complejidad ética creciente
- Coherencia conductual demostrada en todos los niveles

## v1.0 — Marzo 2026
### Fase conceptual
- 40+ documentos de diseño analizados y consolidados
- Arquitectura de 7 capas documentada
- Formalización matemática completa
- Bibliografía de 40+ referencias en 12 disciplinas
