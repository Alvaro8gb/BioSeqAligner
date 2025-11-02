import numpy as np


MATCH=1
MISMATCH=-1
GAP=-2

def sim(x, y):
        return MATCH if x == y else MISMATCH


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