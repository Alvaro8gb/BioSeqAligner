import numpy as np
from numba import jit

MATCH=1
MISMATCH=-1
GAP=-2

DEBUG = False

@jit
def sim(x, y):
        return MATCH if x == y else MISMATCH

def indexes_diagonal(i, filas, columnas):
    # if DEBUG: print("i",i, "filas", filas, "columnas", columnas)
    indices_I, indices_J = [], []
    if i < max(filas, columnas):
        if filas > columnas:
            inicio_fila = i
            inicio_columnas = 1
        else:
            inicio_fila = 1
            inicio_columnas = i
    else:
        if filas > columnas:
            inicio_fila = filas - 1
            inicio_columnas = i - columnas
        else:
            inicio_fila = i - filas
            inicio_columnas = columnas - 1

    signo_columna = 1 if filas > columnas else -1
    signo_fila = -1 if filas > columnas else 1

    while inicio_fila > 0 and inicio_columnas > 0 and inicio_fila < filas and inicio_columnas < columnas:
        indices_I.append(inicio_fila)
        indices_J.append(inicio_columnas)
        inicio_fila += signo_fila
        inicio_columnas += signo_columna

    indices_I = np.array(indices_I, dtype=np.int64)
    indices_J = np.array(indices_J, dtype=np.int64)

    # if DEBUG: print(indices_I, indices_J)
    return indices_I, indices_J

@jit
def indexes_diagonal2(d, filas, columnas):
    """
    Return (I, J) arrays of indices in F on diagonal where i + j == d,
    considering only 1 <= i < filas and 1 <= j < columnas (i,j are F indices).
    Uses vectorized numpy operations for speed.
    """
    i_size = d if d < filas else filas
    i = np.arange(1, i_size)
    j = d - i
    mask = (j >= 1) & (j < columnas)
    return i[mask].astype(np.int64), j[mask].astype(np.int64)

# Traceforward 
def traceforward(F, a, b):
    alnA = []
    alnB = []
    i, j = len(a), len(b)
   

    # Traceback backwards to (0, 0)
    while i > 0 or j > 0: 
        if i > 0 and j > 0 and F[i, j] == F[i-1, j-1] + sim(a[i-1], b[j-1]):
            # Match/Mismatch - move diagonally
            alnA.append(a[i-1])
            alnB.append(b[j-1])
            i -= 1
            j -= 1
        elif i > 0 and F[i, j] == F[i-1, j] + GAP:
            # Gap in B - move up
            alnA.append(a[i-1])
            alnB.append('-')
            i -= 1
        elif j > 0 and F[i, j] == F[i, j-1] + GAP:
            # Gap in A - move left
            alnA.append('-')
            alnB.append(b[j-1])
            j -= 1

    # Reverse the alignments (since we built them backwards)
    alnA.reverse()
    alnB.reverse()

    return ''.join(alnA), ''.join(alnB)


def needleman_wunsch(a, b):
    """
    Global Aligment
    """
    n, m = len(a), len(b)

    F = np.zeros((n+1, m+1), dtype=np.int64)
    F[1:, 0] = np.arange(1, n+1) * GAP
    F[0, 1:] = np.arange(1, m+1) * GAP
    
    # Rellenar matriz
    for i in range(1, n+1):
        for j in range(1, m+1):
            diag = F[i-1][j-1] + sim(a[i-1], b[j-1])
            up   = F[i-1][j] + GAP
            left = F[i][j-1] + GAP
            F[i][j] = max(diag, up, left)

    ref, best_align = traceforward(F, a, b)

    return F[n][m], ref, best_align

@jit
def fill_scores(a, b):

    n, m = len(a), len(b)

    F = np.zeros((n+1, m+1), dtype=np.int64)
    F[1:, 0] = np.arange(1, n+1) * GAP
    F[0, 1:] = np.arange(1, m+1) * GAP
    
    # Rellenar matriz
    for i in range(1, n+1):
        for j in range(1, m+1):
            diag = F[i-1][j-1] + sim(a[i-1], b[j-1])
            up   = F[i-1][j] + GAP
            left = F[i][j-1] + GAP
            F[i][j] = max(diag, up, left)

    return F

def fill_scores_diag(a, b, diag_func):
    n, m = len(a), len(b)

    F = np.full((n+1, m+1), -np.inf, dtype=np.float64)
    F[0,0] = 0
    F[1:, 0] = np.arange(1, n+1) * GAP
    F[0, 1:] = np.arange(1, m+1) * GAP

    i_diag = 1
    diag_amount = F.shape[0] + F.shape[1] - 1
    if DEBUG: print("N", n, "M", m, "diag_amount", diag_amount)
    # Rellenar matriz
    while i_diag <= diag_amount:
        if DEBUG: print("i_diag",i_diag, "diag_amount", diag_amount)
        I, J = diag_func(i_diag + 1, n+1, m+1)
        if DEBUG: print("I",I,"J",J)
        i_diag += 1
        if not I.any() or not J.any():
            if DEBUG: print("BREAK")
            break

        diag_vals = F[I-1, J-1] + np.where(a[I-1] == b[J-1], MATCH, MISMATCH)
        up_vals   = F[I-1, J] + GAP
        left_vals = F[I, J-1] + GAP

        F[I, J] = np.maximum.reduce([diag_vals, up_vals, left_vals])
    if DEBUG: print(F)
    return F


def needleman_wunsch_numba(a, b):
    """
    Global Aligment
    """
    n, m = len(a), len(b)

    F = fill_scores(a, b)

    ref, best_align = traceforward(F, a, b)

    return F[n][m], ref, best_align


def needleman_wunsch_diag_numpy(a, b):
    n, m = len(a), len(b)
    a = np.array(list(a))
    b = np.array(list(b))

    F = fill_scores_diag(a, b, indexes_diagonal2)
    
    ref, best_align = traceforward(F, a, b)

    return F[n][m], ref, best_align


def indexes_diagonal_bounded(d, filas, columnas, bound = 0.4):
    """
    Return (I, J) arrays of indices in F on diagonal where i + j == d,
    considering only 1 <= i < filas and 1 <= j < columnas (i,j are F indices).
    Uses vectorized numpy operations for speed.
    """

    i_size = filas # d if d < filas else filas
    i = np.arange(1, i_size)
    #print("I:",i)
    j = d - i
    #print("J:",j)
    mask = (j >= 1 ) & (j < columnas)
    i_masked = i[mask].astype(int)
    j_masked = j[mask].astype(int)

    indexes_count = i_masked.size
    min_side = min(filas,columnas)

    max_elems = int(min_side * bound)
    if DEBUG: print(max_elems, indexes_count)
    if max_elems >= indexes_count:
        return i_masked, j_masked
    else:
        differ = indexes_count - max_elems
        outside_bounds = differ // 2
        if outside_bounds == 0:
            return i_masked, j_masked
        # print("outside_bounds", outside_bounds)
        return i_masked[outside_bounds:-outside_bounds], j_masked[outside_bounds:-outside_bounds]



def needleman_wunsch_diagbounded_numpy(a, b):
    a = np.array(list(a))
    b = np.array(list(b))

    n, m = len(a), len(b)
    if DEBUG: print("n", n, "m", m)
    F = fill_scores_diag(a, b, indexes_diagonal_bounded)
    ref, best_align = traceforward(F, a, b)

    return F[n][m], ref, best_align



def smith_waterman(a, b):
    """Local alignment algorithm"""
    n, m = len(a), len(b)
    
    F = np.zeros((n+1, m+1), dtype=np.int64)
    F[1:, 0] = np.arange(1, n+1) * GAP
    F[0, 1:] = np.arange(1, m+1) * GAP
    
    max_score = 0
    max_pos = (0, 0)
    
    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            F[i, j] = max(
                0,  # Can restart alignment 
                F[i-1, j-1] + sim(a[i-1], b[j-1]),
                F[i-1, j] + GAP,
                F[i, j-1] + GAP
            )
            if F[i, j] > max_score:
                max_score = F[i, j]
                max_pos = (i, j)
    
    # Traceback from max_pos until hitting 0
    alnA, alnB = [], []
    i, j = max_pos
    
    while i > 0 and j > 0 and F[i, j] > 0:
        score = F[i, j]
        match_score = sim(a[i-1], b[j-1])
        
        if score == F[i-1, j-1] + match_score:
            alnA.append(a[i-1])
            alnB.append(b[j-1])
            i -= 1
            j -= 1
        elif score == F[i-1, j] + GAP:
            alnA.append(a[i-1])
            alnB.append('-')
            i -= 1
        else:
            alnA.append('-')
            alnB.append(b[j-1])
            j -= 1
    
    alnA.reverse()
    alnB.reverse()
    
    return max_score, ''.join(alnA), ''.join(alnB)