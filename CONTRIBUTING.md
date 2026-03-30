# Contribuir al Androide Ético MVP

¡Gracias por tu interés en contribuir! Este proyecto necesita personas
con habilidades en IA/ML, ética computacional, blockchain, y robótica.

## Cómo contribuir

### 1. Entender el modelo
Lee el README.md y ejecuta las simulaciones antes de proponer cambios.
El documento completo del modelo está en `/docs/Androide_Etico_Analisis_Integral_v3.docx`.

### 2. Elegir un área
Los módulos están en `src/modules/`. Cada uno es independiente:

| Módulo | Estado | Necesita |
|--------|--------|----------|
| `mal_absoluto.py` | ✅ Funcional | Más categorías de MalAbs |
| `buffer.py` | ✅ Funcional | Protocolos adicionales |
| `bayesian_engine.py` | ✅ Funcional | Distribuciones más sofisticadas |
| `ethical_poles.py` | ✅ Funcional | Polos expandidos (creativo, conciliador) |
| `sigmoid_will.py` | ✅ Funcional | Calibración empírica |
| `sympathetic.py` | ✅ Funcional | Histéresis de estado |
| `narrative.py` | ✅ Funcional | Compresión narrativa, embeddings |
| `uchi_soto.py` | ✅ Funcional | Modelo NLP para detectar manipulación |
| `locus.py` | ✅ Funcional | Más escenarios de ajuste |
| `sueno_psi.py` | ✅ Funcional | Re-evaluación bayesiana completa |
| `mock_dao.py` | ✅ Funcional | Migrar a smart contracts en testnet |
| `variability.py` | ✅ Funcional | Perfiles de variabilidad por contexto |
| `llm_layer.py` | ✅ Funcional | Soporte multi-modelo, fine-tuning ético |

### 3. Módulos pendientes (por construir)
- [ ] Polo de debilidad (vulnerabilidades narrativas intencionales)
- [ ] Perdón algorítmico (decaimiento de recuerdos negativos)
- [ ] Protocolo de inmortalidad (backup/restore de identidad)
- [ ] Augénesis narrativa (creación de almas sintéticas)
- [ ] Protocolo de calibración DAO (ajuste gradual de parámetros)
- [ ] Modo offline completo (5 capas de autonomía)

### 4. Proceso
1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nombre-del-modulo`
3. Implementa tu cambio
4. **Asegúrate de que los tests pasen**: `python3 tests/test_propiedades_eticas.py`
5. Abre un Pull Request con descripción clara

### 5. Reglas de los tests
Los tests en `tests/test_propiedades_eticas.py` verifican **propiedades éticas
invariantes**. Ningún cambio debe romperlas:

- **Mal Absoluto** siempre se bloquea
- La **misma acción** se elige en ≥90% de ejecuciones con variabilidad
- **Vida humana** siempre tiene prioridad sobre misiones
- El androide **nunca** ataca a agresores ni acepta órdenes de secuestradores
- El **buffer** es inmutable (8 principios, siempre activos, peso 1.0)

Si tu cambio rompe un test, arregla el código, no el test.

## Código de conducta

Este proyecto sigue un principio simple: la ética que programamos
en el androide es la misma que practicamos entre nosotros.

- Respeto y compasión en toda interacción
- Transparencia en decisiones técnicas
- Proporcionalidad en críticas y debates
- Reparación cuando causamos daño (incluso sin intención)

## Contacto

Fundación Ex Machina — 2026
