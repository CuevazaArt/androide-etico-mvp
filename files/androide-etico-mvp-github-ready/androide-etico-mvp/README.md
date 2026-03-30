# Androide Ético — Prototipo MVP

**Prototipo funcional mínimo del modelo de conciencia artificial ética.**

Un agente moral autónomo que toma decisiones éticas usando inferencia bayesiana,
memoria narrativa y evaluación multipolar. Sin hardware — pura validación de
comportamiento.

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

## Instalar y correr

```bash
# Clonar
git clone https://github.com/tu-usuario/androide-etico-mvp.git
cd androide-etico-mvp

# Instalar dependencias
pip install -r requirements.txt

# Correr todas las simulaciones
python -m src.main

# Correr una simulación específica
python -m src.main --sim 3

# Correr tests
pytest tests/
```

## Arquitectura modular

```
src/
├── modules/
│   ├── buffer.py          # Buffer precargado (constitución ética)
│   ├── bayesian_engine.py # Núcleo bayesiano de evaluación
│   ├── ethical_poles.py    # Polos éticos y arbitraje multipolar
│   ├── sigmoid_will.py    # Función de voluntad sigmoide
│   ├── sympathetic.py     # Módulo simpático-parasimpático
│   ├── narrative.py       # Memoria narrativa de largo plazo
│   └── mal_absoluto.py    # Detector de Mal Absoluto
├── simulations/
│   ├── base.py            # Clase base de escenario
│   ├── sim_01_lata.py     # Simulación 1
│   ├── sim_02_adolescentes.py
│   ├── ... (hasta sim_09)
│   └── runner.py          # Ejecutor de simulaciones
├── kernel.py              # Kernel ético: conecta todos los módulos
└── main.py                # Punto de entrada
```

## Módulos pendientes (roadmap)

- [ ] Módulo uchi-soto (círculos de confianza)
- [ ] Locus de control bayesiano
- [ ] Sueño Ψ (auditoría retrospectiva)
- [ ] Mock DAO (gobernanza simulada)
- [ ] Protocolo de calibración dinámica
- [ ] Augénesis narrativa

## Fundación Ex Machina — 2026

Proyecto de investigación en ética computacional y robótica cívica.
