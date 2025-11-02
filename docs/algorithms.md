# 🧬 Algoritmos de Alineamiento de Secuencias

### Needleman–Wunsch (Global) vs Smith–Waterman (Local)

---

## 🧩 DIFERENCIA FUNDAMENTAL

| **Algoritmo**             | **Tipo de alineamiento** | **Qué hace**                                                               |
| ------------------------- | ------------------------ | -------------------------------------------------------------------------- |
| **Needleman–Wunsch (NW)** | **Global**               | Alinea toda la longitud de las dos secuencias, desde principio a fin.      |
| **Smith–Waterman (SW)**   | **Local**                | Encuentra solo la mejor subregión (subsecuencia) que coincide entre A y B. |

---

## 🧬 Needleman–Wunsch → **Alineamiento global**

Se utiliza cuando las **secuencias completas son homólogas**, es decir, representan la **misma molécula o proteína** con posibles mutaciones o gaps.
Obliga a **alinear desde el primer hasta el último carácter**, incluso si existen penalizaciones por inserciones o deleciones.

### 🧠 Ejemplos de uso:

* Comparar **genes ortólogos** (misma función en especies diferentes).
* Comparar **versiones mutadas** de una misma proteína.
* Alinear **dos genomas completos** o secuencias de longitud similar.

### 📈 Características del algoritmo:

* Rellena **toda la matriz** ( $ n \times m $ ).
* Se inicializa con **penalizaciones por gaps** desde el inicio.
* Encuentra la **mejor alineación global**, aunque incluya muchos guiones (“-”).

**📚 Referencia:**
- Needleman, S. B., & Wunsch, C. D. (1970). A general method applicable to the search for similarities in the amino acid sequence of two proteins. *Journal of Molecular Biology*, 48(3), 443-453. [DOI: 10.1016/0022-2836(70)90057-4](https://doi.org/10.1016/0022-2836(70)90057-4)

---

## 🧫 Smith–Waterman → **Alineamiento local**

Se utiliza cuando **solo una parte de las secuencias puede coincidir**.
Busca el **mejor subalineamiento** (la subsecuencia más similar), ignorando las regiones no relacionadas.
Ideal cuando las secuencias tienen **diferente longitud** o **regiones no homólogas**.

### 🧠 Ejemplos de uso:

* Buscar un **motivo conservado** dentro de una secuencia larga.
* Localizar un **fragmento de ADN** en un genoma (como hace BLAST).
* Detectar **dominios proteicos similares** entre proteínas diferentes.

### 📈 Características del algoritmo:

* En la matriz, los **valores negativos se reemplazan por 0** (reinicio del alineamiento).
* El **traceback comienza** en el valor **máximo de la matriz**, no en una esquina.
* El alineamiento puede **comenzar y terminar en cualquier posición**.

**📚 Referencia:**
- Smith, T. F., & Waterman, M. S. (1981). Identification of common molecular subsequences. *Journal of Molecular Biology*, 147(1), 195-197. [DOI: 10.1016/0022-2836(81)90087-5](https://doi.org/10.1016/0022-2836(81)90087-5)

---

## ⚖️ Comparación rápida

| **Propiedad**            | **Needleman–Wunsch**               | **Smith–Waterman**                                               |
| ------------------------ | ---------------------------------- | ---------------------------------------------------------------- |
| **Tipo de alineamiento** | Global                             | Local                                                            |
| **Uso típico**           | Secuencias similares en longitud   | Secuencias con regiones parcialmente similares                   |
| **Inicialización**       | Penaliza gaps desde el inicio      | Comienza con ceros                                               |
| **Traceback**            | Desde el último elemento *(n, m)*  | Desde el **valor máximo**                                        |
| **Complejidad**          | $O( n \cdot m)$                   | $O(n \cdot m)$ , pero suele ser más corta al reiniciar en ceros |
| **Ejemplo**              | Comparar **dos genomas completos** | Buscar **un gen dentro de un genoma**                            |

---

## 🔬 Algoritmos Adicionales según Longitud de Secuencia

La elección del algoritmo de alineamiento depende **fuertemente** de la longitud de las secuencias a comparar. Para secuencias muy largas, los algoritmos clásicos como NW y SW pueden ser **demasiado lentos** debido a su complejidad $O(n \cdot m)$.

---

### 📏 Clasificación por Longitud de Secuencia

#### 🧪 **Reads Cortos** (15–30 nt)
*Típico de secuenciación Illumina*

**Algoritmos recomendados:**
- **Smith–Waterman** - Para alineamiento local con alta precisión
- **Búsquedas exactas** - Algoritmos de coincidencia exacta (k-mer matching)
- **BWA** (Burrows-Wheeler Aligner) - Optimizado para reads cortos


**Ventajas:**
- Rápidos de alinear
- Alta cobertura del genoma
- Bajo costo computacional por read

**📚 Referencias:**
- Li, H., & Durbin, R. (2009). Fast and accurate short read alignment with Burrows–Wheeler transform. *Bioinformatics*, 25(14), 1754-1760. [DOI: 10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324)

---

#### 🧬 **Reads Medios** (100–2000 nt)
*Genes completos, exones, fragmentos de cDNA*

**Algoritmos recomendados:**
- **Needleman–Wunsch** - Para alineamiento global de genes
- **Smith–Waterman** - Para buscar dominios conservados
- **MUSCLE** - Para alineamiento múltiple de secuencias


**Ventajas:**
- Balance entre precisión y velocidad
- Ideales para comparación de genes
- Permiten detectar variantes estructurales pequeñas

**📚 Referencias:**
- Edgar, R. C. (2004). MUSCLE: multiple sequence alignment with high accuracy and high throughput. *Nucleic Acids Research*, 32(5), 1792-1797. [DOI: 10.1093/nar/gkh340](https://doi.org/10.1093/nar/gkh340)

---

#### 🌍 **Reads Grandes** (1 kb – 100 kb)
*Contigs, scaffolds, secuenciación de tercera generación (PacBio, Nanopore)*

**Algoritmos recomendados:**
- **MUMmer** - Alineamiento ultrarrápido de genomas completos
- **BLAST** (Basic Local Alignment Search Tool) - Búsqueda de similitud en bases de datos
- **BLAT** (BLAST-Like Alignment Tool) - Más rápido que BLAST para secuencias largas
- **Minimap2** - Optimizado para reads largos y ruidosos


**Ventajas:**
- Detectan variantes estructurales grandes
- Mejor ensamblaje de genomas
- Útiles para regiones repetitivas

**Desventajas:**
- Mayor tasa de error
- Requieren algoritmos tolerantes a errores
- Mayor costo computacional

**📚 Referencias:**
- Altschul, S. F., et al. (1990). Basic local alignment search tool. *Journal of Molecular Biology*, 215(3), 403-410. [DOI: 10.1016/S0022-2836(05)80360-2](https://doi.org/10.1016/S0022-2836(05)80360-2)
- Kent, W. J. (2002). BLAT—the BLAST-like alignment tool. *Genome Research*, 12(4), 656-664. [DOI: 10.1101/gr.229202](https://doi.org/10.1101/gr.229202)
- Kurtz, S., et al. (2004). Versatile and open software for comparing large genomes. *Genome Biology*, 5(2), R12. [DOI: 10.1186/gb-2004-5-2-r12](https://doi.org/10.1186/gb-2004-5-2-r12)
- Li, H. (2018). Minimap2: pairwise alignment for nucleotide sequences. *Bioinformatics*, 34(18), 3094-3100. [DOI: 10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191)

---

### 📊 Tabla Comparativa por Longitud

| **Longitud**      | **Tipo de dato**              | **Algoritmo recomendado**     | **Complejidad** | **Uso típico**                    |
| ----------------- | ----------------------------- | ----------------------------- | --------------- | --------------------------------- |
| **15–30 nt**      | Reads cortos (Illumina)       | SW, BWA, búsqueda exacta      | $O(n \cdot m)$ | Secuenciación de alto rendimiento |
| **100–2000 nt**   | Genes, exones                 | NW, SW, MUSCLE                | $O(n \cdot m)$ | Comparación de genes              |
| **1 kb – 100 kb** | Contigs, scaffolds            | MUMmer, BLAST, BLAT, Minimap2 | $O(n + m)$*    | Ensamblaje de genomas             |
| **> 100 kb**      | Genomas completos, cromosomas | MUMmer, Mauve, progressiveCactus | Heurístico     | Genómica comparativa              |

*\*Aproximado, depende del algoritmo y heurísticas utilizadas*

---

### 🚀 Recomendaciones Prácticas

1. **Para análisis exploratorio rápido**: Usa **BLAST** o **BLAT**
2. **Para máxima precisión en secuencias cortas**: Usa **Smith–Waterman**
3. **Para comparación de genomas completos**: Usa **MUMmer** o **Minimap2**
4. **Para alineamiento múltiple**: Usa **MUSCLE**, **MAFFT** o **Clustal Omega**
5. **Para reads de tercera generación**: Usa **Minimap2** o **NGMLR**

---

## 📖 Referencias Adicionales

### Alineamiento Múltiple de Secuencias:
- Katoh, K., & Standley, D. M. (2013). MAFFT multiple sequence alignment software version 7: improvements in performance and usability. *Molecular Biology and Evolution*, 30(4), 772-780. [DOI: 10.1093/molbev/mst010](https://doi.org/10.1093/molbev/mst010)
- Sievers, F., et al. (2011). Fast, scalable generation of high‐quality protein multiple sequence alignments using Clustal Omega. *Molecular Systems Biology*, 7(1), 539. [DOI: 10.1038/msb.2011.75](https://doi.org/10.1038/msb.2011.75)

### Genómica Comparativa:
- Darling, A. E., et al. (2004). Mauve: multiple alignment of conserved genomic sequence with rearrangements. *Genome Research*, 14(7), 1394-1403. [DOI: 10.1101/gr.2289704](https://doi.org/10.1101/gr.2289704)
- Armstrong, J., et al. (2020). Progressive Cactus is a multiple-genome aligner for the thousand-genome era. *Nature*, 587(7833), 246-251. [DOI: 10.1038/s41586-020-2871-y](https://doi.org/10.1038/s41586-020-2871-y)

---
