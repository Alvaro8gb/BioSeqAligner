import numpy as np


MATCH=1
MISMATCH=-1
GAP=-2

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

    indices_I = np.array(indices_I, dtype=int)
    indices_J = np.array(indices_J, dtype=int)

    # if DEBUG: print(indices_I, indices_J)
    return indices_I, indices_J

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
    return i[mask].astype(int), j[mask].astype(int)

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

    F = np.zeros((n+1, m+1), dtype=int)
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

def needleman_optimized(a, b):
    a = np.asarray(a)
    b = np.asarray(b)

    n, m = len(a), len(b)
    N, M = n+1, m+1

    F = np.zeros((N, M), dtype=int)
    F[1:, 0] = np.arange(1, N) * GAP
    F[0, 1:] = np.arange(1, M) * GAP

    i_diag = 1
    diag_amount = N + M - 1
    # Rellenar matriz
    while i_diag <= diag_amount:
        # if DEBUG: print("i_diag",i_diag, "diag_amount", diag_amount)
        I, J = indexes_diagonal2(i_diag,N,M)
        print("I",I,"J",J)
        i_diag += 1
        if not I.any() or not J.any():
            break

        diag_vals = F[I-1, J-1] + np.where(a[I-1] == b[J-1], MATCH, MISMATCH)
        up_vals   = F[I-1, J] + GAP
        left_vals = F[I, J-1] + GAP

        F[I, J] = np.maximum(np.maximum(diag_vals, up_vals), left_vals)

    # if DEBUG: print_matrix(F,N,M)
    ref, best_align = traceforward(F, a, b)

    return F[n][m], ref, best_align

def smith_waterman(a, b):
    """Local alignment algorithm"""
    n, m = len(a), len(b)
    
    F = np.zeros((n+1, m+1), dtype=int)
    F[1:, 0] = np.arange(1, n+1) * GAP
    F[0, 1:] = np.arange(1, m+1) * GAP
    
    max_score = 0
    max_pos = (0, 0)
    
    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            F[i, j] = max(
                0,  # Can restart alignment (key difference!)
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