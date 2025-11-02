# BioSeqAligner 🧬

Un visualizador de alineamiento de secuencias basado en web construido con Streamlit. Compara secuencias de ADN/ARN utilizando los algoritmos de alineamiento Needleman-Wunsch (global) o Smith-Waterman (local) con una hermosa visualización codificada por colores.

## Características

- **Múltiples Algoritmos**: Elige entre Needleman-Wunsch (alineamiento global) y Smith-Waterman (alineamiento local)
- **Visualización Interactiva**:
  - 🟢 Verde: Nucleótidos coincidentes
  - 🔴 Rojo: Nucleótidos no coincidentes
  - 🟡 Amarillo: Gaps (-)
- **Parámetros Personalizables**: Ajusta las puntuaciones de coincidencia, penalizaciones por desajuste y penalizaciones por gaps
- **Alineamiento en Tiempo Real**: Resultados instantáneos con métricas detalladas
- **Arquitectura MVC**: Separación clara de responsabilidades con diseño modular

## Estructura del Proyecto

```
BioSeqAligner/
├── app.py              # Aplicación principal de Streamlit (Vistas y Controladores)
├── algorithms.py       # Algoritmos de alineamiento (Modelo)
├── visualization.py    # Componentes de visualización (Helpers de Vista)
├── __init__.py        # Inicialización del paquete
├── requirements.txt    # Dependencias
└── README.md          # Documentación
```

### Arquitectura

El proyecto sigue el patrón **MVC (Modelo-Vista-Controlador)**:

- **Modelo** (`algorithms.py`):
  - `AlignmentScoring`: Parámetros de puntuación para alineamientos
  - `NeedlemanWunsch`: Algoritmo de alineamiento global
  - `SmithWaterman`: Algoritmo de alineamiento local
  - `get_aligner()`: Función factory para selección de algoritmo

- **Vista** (`visualization.py`):
  - `AlignmentVisualizer`: Generación de HTML para visualización de alineamiento
  - `AlignmentStats`: Cálculos estadísticos
  - `LegendComponent`: Componente UI de leyenda
  - `ExamplesComponent`: Proveedor de secuencias de ejemplo

- **Controlador** (`app.py`):
  - `main()`: Punto de entrada de la aplicación
  - `render_*()`: Funciones de renderizado de componentes UI
  - Manejo de interacción del usuario y orquestación del flujo de trabajo

## Instalación

1. Clona este repositorio o descarga los archivos

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador predeterminado en `http://localhost:8501`

## Cómo Usar

1. **Ingresa las Secuencias**: Introduce tus secuencias de ADN/ARN en las áreas de texto
2. **Selecciona el Algoritmo**: Elige entre Needleman-Wunsch o Smith-Waterman desde la barra lateral
3. **Ajusta los Parámetros** (opcional): Modifica los parámetros de puntuación en la barra lateral
4. **Haz clic en "Alinear Secuencias"**: Visualiza los resultados del alineamiento con visualización codificada por colores

## Secuencias de Ejemplo

Prueba estos ejemplos:

**Alta similitud:**

- Secuencia 1: `GATTACA`
- Secuencia 2: `GATTACA`

**Con mutaciones:**

- Secuencia 1: `GATTACA`
- Secuencia 2: `GTCGACGC`

**Alineamiento local:**

- Secuencia 1: `AAAGGGTTTTCCCC`
- Secuencia 2: `GGGTT`

## Algoritmos

### Needleman-Wunsch (Alineamiento Global)

Encuentra el mejor alineamiento entre dos secuencias completas. Ideal para comparar secuencias de longitud similar.

**Referencia:**
- Needleman, S. B., & Wunsch, C. D. (1970). A general method applicable to the search for similarities in the amino acid sequence of two proteins. *Journal of Molecular Biology*, 48(3), 443-453. [DOI: 10.1016/0022-2836(70)90057-4](https://doi.org/10.1016/0022-2836(70)90057-4)

### Smith-Waterman (Alineamiento Local)

Encuentra la mejor subsecuencia coincidente entre dos secuencias. Ideal para encontrar regiones similares en secuencias de diferentes longitudes.

**Referencia:**
- Smith, T. F., & Waterman, M. S. (1981). Identification of common molecular subsequences. *Journal of Molecular Biology*, 147(1), 195-197. [DOI: 10.1016/0022-2836(81)90087-5](https://doi.org/10.1016/0022-2836(81)90087-5)

## Desarrollo

### Uso como Módulo de Python

También puedes usar los algoritmos de alineamiento programáticamente:

```python
from algorithms import AlignmentScoring, get_aligner

# Crear esquema de puntuación
scoring = AlignmentScoring(match=1, mismatch=-1, gap=-2)

# Obtener el alineador
aligner = get_aligner("needleman-wunsch", scoring)

# Realizar alineamiento
score, aligned_seq1, aligned_seq2 = aligner.align("GATTACA", "GTCGACGC")

print(f"Puntuación: {score}")
print(f"Seq1: {aligned_seq1}")
print(f"Seq2: {aligned_seq2}")
```

### Extender la Aplicación

- Agregar nuevos algoritmos: Extiende la clase `SequenceAligner` en `algorithms.py`
- Personalizar visualización: Modifica `AlignmentVisualizer` en `visualization.py`
- Agregar componentes UI: Crea nuevas funciones `render_*()` en `app.py`


## Licencia

Licencia MIT - Ver el archivo [LICENSE](LICENSE) para más detalles.


## Atribución

Para cualquier otra duda contactar: 
- **Álvaro García Barragán**
- **Pablo Fernández**
