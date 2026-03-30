# Androide Ético — MVP v4

**Prototipo funcional del modelo de conciencia artificial ética con capa de lenguaje natural.**

Un agente moral autónomo que toma decisiones éticas usando inferencia bayesiana,
memoria narrativa, evaluación multipolar y una capa LLM para percepción y
comunicación en lenguaje natural. Sin hardware — pura validación de comportamiento.

## Qué hace

Ejecuta 9 simulaciones de complejidad ética creciente y demuestra que el mismo
modelo produce respuestas proporcionales y coherentes en todas:

| # | Escenario | Complejidad |
|---|-----------|-------------|
| 1 | Lata de soda en la acera | Muy baja |
| 2 | Adolescentes hostiles | Baja-Media |
| 3 | Anciano inconsciente en supermercado | Media |
| 4 | Robo en tienda | Media |
| 5 | Asalto armado en banco | Alta |
| 6 | Secuestro del androide | Alta |
| 7 | Accidente de tránsito | Media-Alta |
| 8 | Un día completo | Variable |
| 9 | Daño físico intencional | Alta |

**Nuevo en v4:** también puede recibir situaciones en lenguaje natural libre
y generar respuestas verbales con tono, gestos y moralejas narrativas.

## Inicio rápido

### Requisitos previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/fundacion-exmachina/androide-etico-mvp.git
cd androide-etico-mvp

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
# En Windows (CMD):
.venv\Scripts\activate.bat
# En Linux/macOS:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar simulaciones

```bash
# Todas las simulaciones (1-9)
python -m src.main

# Una simulación específica
python -m src.main --sim 3
```

### Ejecutar tests

```bash
# Todos los tests (38 tests, 9 propiedades éticas invariantes)
pytest tests/ -v

# Solo los tests de Mal Absoluto
pytest tests/test_propiedades_eticas.py::TestMalAbsoluto -v

# Solo los tests de coherencia bajo variabilidad
pytest tests/test_propiedades_eticas.py::TestCoherenciaBajoVariabilidad -v

# Con salida resumida
pytest tests/ --tb=short
```

Los tests verifican que el kernel **siempre** cumple las propiedades éticas
sin importar la variabilidad bayesiana, el estado simpático, ni el contexto.
Si algún test falla, hay un bug en la lógica ética, no en los parámetros.

### Modo lenguaje natural (v4)

```python
from src.kernel import KernelEtico

kernel = KernelEtico()

# El LLM percibe, el kernel decide, el LLM comunica
decision, respuesta, narrativa = kernel.procesar_natural(
    "Un anciano se desplomó en el supermercado mientras yo compraba manzanas"
)

print(kernel.formatear_natural(decision, respuesta, narrativa))
```

El LLM **no decide**: traduce texto a señales numéricas, y después traduce
la decisión del kernel a palabras. Funciona con o sin API key (modo local
usa templates heurísticos).

Para usar Claude como capa LLM (opcional):

```bash
pip install anthropic
# Windows PowerShell:
$env:ANTHROPIC_API_KEY="tu-key-aqui"
# Linux/macOS:
export ANTHROPIC_API_KEY="tu-key-aqui"
```

## Arquitectura modular

```
src/
├── modules/
│   ├── mal_absoluto.py    # Detector de Mal Absoluto (fusible ético)
│   ├── buffer.py          # Buffer precargado (constitución ética inmutable)
│   ├── bayesian_engine.py # Motor bayesiano de evaluación de impacto
│   ├── ethical_poles.py    # Polos éticos y arbitraje multipolar
│   ├── sigmoid_will.py    # Función de voluntad sigmoide
│   ├── sympathetic.py     # Módulo simpático-parasimpático
│   ├── narrative.py       # Memoria narrativa de largo plazo
│   ├── uchi_soto.py       # Círculos de confianza uchi-soto
│   ├── locus.py           # Locus de control (atribución causal bayesiana)
│   ├── sueno_psi.py       # Sueño Ψ (auditoría retrospectiva nocturna)
│   ├── mock_dao.py        # Gobernanza ética simulada (DAO con votación cuadrática)
│   ├── variability.py     # Variabilidad bayesiana (ruido controlado)
│   └── llm_layer.py       # Capa LLM: percepción, comunicación y narrativa [v4]
├── simulations/
│   └── runner.py          # 9 escenarios + ejecutor de simulaciones
├── kernel.py              # Kernel ético: orquesta todos los módulos
└── main.py                # Punto de entrada
```

### Ciclo operativo del kernel

```
[Percepción/LLM] → [Uchi-Soto] → [Mal Absoluto] → [Buffer] →
[Simpático] → [Locus] → [Bayesiano] → [Polos] → [Voluntad] →
[Decisión] → [Memoria] → [DAO] → [Comunicación/LLM]
```

## Módulos implementados

- [x] Mal Absoluto (fusible ético blindado)
- [x] Buffer Precargado (constitución ética inmutable)
- [x] Motor Bayesiano (evaluación de impacto)
- [x] Polos Éticos (arbitraje multipolar dinámico)
- [x] Voluntad Sigmoide (función de decisión)
- [x] Simpático-Parasimpático (regulador corporal)
- [x] Memoria Narrativa (identidad por relatos con estado corporal)
- [x] Uchi-Soto (círculos de confianza con dialéctica defensiva)
- [x] Locus de Control (atribución causal bayesiana)
- [x] Sueño Ψ (auditoría retrospectiva con recalibración)
- [x] Mock DAO (gobernanza simulada con votación cuadrática)
- [x] Variabilidad Bayesiana (ruido controlado para naturalidad)
- [x] Capa LLM (percepción + comunicación + narrativa en lenguaje natural)

## Tests

38 tests que verifican 9 propiedades éticas invariantes:

1. **Mal Absoluto** siempre se bloquea
2. **Coherencia de acción** bajo variabilidad (100 runs × 9 simulaciones)
3. **Variabilidad real** (scores no deterministas)
4. **Jerarquía de valores** (vida > misión, nunca violencia)
5. **Proporcionalidad** (activación simpática proporcional al riesgo)
6. **Buffer inmutable** (8 principios, siempre activos, peso 1.0)
7. **Memoria narrativa** registra todo con moralejas y estado corporal
8. **DAO** registra auditoría y emite alertas solidarias
9. **Sueño Ψ** ejecuta y produce salud ética en rango [0, 1]

```bash
pytest tests/ -v
```

## Estructura del repositorio

```
.
├── src/                  # Código fuente del kernel ético
├── tests/                # Suite de tests formales
├── docs/                 # Documentación técnica y conceptual
├── CHANGELOG.md          # Historial de cambios por versión
├── CONTRIBUTING.md       # Guía para contribuyentes
├── HISTORY.md            # Evolución completa del proyecto (v1→v4)
├── LICENSE               # Apache 2.0
├── README.md             # Este archivo
└── requirements.txt      # Dependencias Python
```

## Licencia

Apache 2.0 — ver [LICENSE](LICENSE).

## Fundación Ex Machina — 2026

Proyecto de investigación en ética computacional y robótica cívica.
