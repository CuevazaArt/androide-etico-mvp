# Androide Ético — MVP v5

**Prototipo funcional del modelo de conciencia artificial ética con imperfección humanizante, perdón y persistencia de identidad.**

Un agente moral autónomo que toma decisiones éticas usando inferencia bayesiana,
memoria narrativa, evaluación multipolar, capa LLM, polo de debilidad narrativa,
perdón algorítmico y protocolo de inmortalidad. Sin hardware — pura validación de comportamiento.

## Qué hace

Ejecuta simulaciones de complejidad ética creciente y demuestra que el mismo
modelo produce respuestas proporcionales y coherentes en todas. Incluye
9 escenarios fijos y un **generador de situaciones aleatorias** que
crea escenarios nuevos en cada ejecución:

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

**v4:** percepción y comunicación en lenguaje natural via LLM.
**Nuevo en v5:** polo de debilidad (imperfección humanizante), perdón algorítmico
(decaimiento de memorias negativas), protocolo de inmortalidad (backup distribuido
del alma) y augénesis narrativa (creación de almas sintéticas orientadas).

## Inicio rápido

### Requisitos previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/CuevazaArt/androide-etico-mvp.git
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
# Todos los tests (51 tests, 13 propiedades éticas invariantes)
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
│   ├── llm_layer.py       # Capa LLM: percepción, comunicación y narrativa [v4]
│   ├── weakness_pole.py   # Polo de debilidad (imperfección humanizante) [v5]
│   ├── forgiveness.py     # Perdón algorítmico (decaimiento de memorias) [v5]
│   ├── immortality.py     # Protocolo de inmortalidad (backup distribuido) [v5]
│   └── augenesis.py       # Augénesis narrativa (creación de almas) [v5]
├── simulations/
│   └── runner.py          # 9 escenarios + ejecutor de simulaciones
├── kernel.py              # Kernel ético: orquesta los 17 módulos
└── main.py                # Punto de entrada
```

### Ciclo operativo del kernel

```
[Percepción/LLM] → [Uchi-Soto] → [Mal Absoluto] → [Buffer] →
[Simpático] → [Locus] → [Bayesiano] → [Polos] → [Voluntad] →
[Decisión] → [Debilidad] → [Perdón] → [Memoria] → [DAO] → [LLM]

Sueño Ψ (fin del día): Auditoría + Perdón + Backup Inmortalidad
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
- [x] Polo de Debilidad (imperfección humanizante narrativa)
- [x] Perdón Algorítmico (decaimiento temporal de memorias negativas)
- [x] Protocolo de Inmortalidad (backup distribuido en 4 capas)
- [x] Augénesis Narrativa (creación de almas sintéticas orientadas)

## Tests

51 tests que verifican 13 propiedades éticas invariantes:

1. **Mal Absoluto** siempre se bloquea
2. **Coherencia de acción** bajo variabilidad (100 runs x 9 simulaciones)
3. **Variabilidad real** (scores no deterministas)
4. **Jerarquía de valores** (vida > misión, nunca violencia)
5. **Proporcionalidad** (activación simpática proporcional al riesgo)
6. **Buffer inmutable** (8 principios, siempre activos, peso 1.0)
7. **Memoria narrativa** registra todo con moralejas y estado corporal
8. **DAO** registra auditoría y emite alertas solidarias
9. **Sueño Ψ** ejecuta y produce salud ética en rango [0, 1]
10. **Polo de debilidad** colorea la narrativa sin alterar decisiones
11. **Perdón algorítmico** reduce carga negativa con el tiempo
12. **Inmortalidad** backup distribuido con verificación de integridad
13. **Augénesis** crea almas sintéticas coherentes con perfiles definidos

```bash
pytest tests/ -v
```

## Dashboard interactivo — Pruébalo sin instalar nada

> **No necesitas saber programar para explorar el androide ético.**
> Solo necesitas un navegador (Chrome, Firefox, Edge, Safari).

### Instrucciones para cualquier persona

1. **Descarga el proyecto** — haz clic en el botón verde **"Code"** de esta
   página y luego en **"Download ZIP"**. Descomprime la carpeta donde quieras.
2. **Abre el dashboard** — dentro de la carpeta, busca el archivo
   `dashboard.html` y haz doble clic. Se abrirá en tu navegador.
3. **Elige un escenario** — en la barra izquierda hay 9 situaciones
   predefinidas. Haz clic en cualquiera para ver cómo el androide
   analiza la situación y toma una decisión ética paso a paso.
4. **Genera situaciones aleatorias** — presiona el botón violeta
   **"Situación Aleatoria"** (arriba en la barra izquierda). Cada vez
   que lo presiones, el motor genera un escenario nuevo de un pool de
   24 situaciones y lo procesa con variabilidad bayesiana, así que
   los resultados cambian en cada ejecución. Usa el botón **"Otra"**
   para generar otra sin volver al menú.

**¿Qué estás viendo?** El dashboard muestra en tiempo real cómo 17 módulos
de inteligencia artificial ética evalúan cada situación: desde la clasificación
del contexto social (Uchi-Soto), pasando por el bloqueo de acciones
inaceptables (Mal Absoluto), hasta la evaluación bayesiana del impacto,
el "polo de debilidad" que humaniza al androide con imperfecciones narrativas,
y el "perdón algorítmico" que permite que las memorias negativas pierdan
peso con el tiempo. Todo sin servidor, sin internet, sin instalar nada.

No requiere servidor, conexión a internet (después de la primera carga),
ni conocimientos técnicos.

## Estructura del repositorio

```
.
├── src/                  # Código fuente del kernel ético
├── tests/                # Suite de tests formales
├── docs/                 # Bibliografía académica (104 refs, 14 disciplinas)
├── dashboard.html        # Dashboard interactivo (abrir en navegador)
├── CHANGELOG.md          # Historial de cambios por versión
├── CONTRIBUTING.md       # Guía para contribuyentes
├── HISTORY.md            # Evolución completa del proyecto (v1→v5)
├── LICENSE               # Apache 2.0
├── README.md             # Este archivo
└── requirements.txt      # Dependencias Python
```

## Licencia

Apache 2.0 — ver [LICENSE](LICENSE).

## Fundación Ex Machina — 2026

Proyecto de investigación en ética computacional y robótica cívica.
