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
