"""
Sequence Alignment Algorithms Module
Contains implementations of Needleman-Wunsch and Smith-Waterman algorithms
"""

import numpy as np


class AlignmentScoring:
    """Scoring parameters for sequence alignment"""
    
    def __init__(self, match=1, mismatch=-1, gap=-2):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap
    
    def similarity(self, x, y):
        """Calculate similarity score between two characters"""
        return self.match if x == y else self.mismatch


class SequenceAligner:
    """Base class for sequence alignment algorithms"""
    
    def __init__(self, scoring: AlignmentScoring):
        self.scoring = scoring
    
    def align(self, seq1, seq2):
        """Perform sequence alignment. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement align method")


class NeedlemanWunsch(SequenceAligner):
    """
    Needleman-Wunsch Global Alignment Algorithm
    Finds the best alignment between two complete sequences
    """
    
    def _traceback(self, F, a, b):
        """Perform traceback to reconstruct alignment"""
        aln_a = []
        aln_b = []
        i, j = len(a), len(b)
        
        while i > 0 or j > 0:
            if i > 0 and j > 0 and F[i, j] == F[i-1, j-1] + self.scoring.similarity(a[i-1], b[j-1]):
                # Match/Mismatch - move diagonally
                aln_a.append(a[i-1])
                aln_b.append(b[j-1])
                i -= 1
                j -= 1
            elif i > 0 and F[i, j] == F[i-1, j] + self.scoring.gap:
                # Gap in sequence B - move up
                aln_a.append(a[i-1])
                aln_b.append('-')
                i -= 1
            elif j > 0 and F[i, j] == F[i, j-1] + self.scoring.gap:
                # Gap in sequence A - move left
                aln_a.append('-')
                aln_b.append(b[j-1])
                j -= 1
        
        # Reverse alignments (built backwards)
        aln_a.reverse()
        aln_b.reverse()
        
        return ''.join(aln_a), ''.join(aln_b)
    
    def align(self, seq1, seq2):
        """
        Perform Needleman-Wunsch global alignment
        
        Args:
            seq1: First sequence (string or list)
            seq2: Second sequence (string or list)
        
        Returns:
            tuple: (score, aligned_seq1, aligned_seq2)
        """
        a = list(seq1) if isinstance(seq1, str) else seq1
        b = list(seq2) if isinstance(seq2, str) else seq2
        
        n, m = len(a), len(b)
        
        # Initialize DP matrix
        F = np.zeros((n+1, m+1), dtype=int)
        F[1:, 0] = np.arange(1, n+1) * self.scoring.gap
        F[0, 1:] = np.arange(1, m+1) * self.scoring.gap
        
        # Fill DP matrix
        for i in range(1, n+1):
            for j in range(1, m+1):
                diag = F[i-1, j-1] + self.scoring.similarity(a[i-1], b[j-1])
                up = F[i-1, j] + self.scoring.gap
                left = F[i, j-1] + self.scoring.gap
                F[i, j] = max(diag, up, left)
        
        # Traceback to get alignment
        aligned_a, aligned_b = self._traceback(F, a, b)
        
        return F[n, m], aligned_a, aligned_b


class SmithWaterman(SequenceAligner):
    """
    Smith-Waterman Local Alignment Algorithm
    Finds the best matching subsequence between two sequences
    """
    
    def _traceback(self, F, a, b, max_pos):
        """Perform traceback from maximum score position"""
        aln_a = []
        aln_b = []
        i, j = max_pos
        
        # Traceback until hitting 0
        while i > 0 and j > 0 and F[i, j] > 0:
            score = F[i, j]
            match_score = self.scoring.similarity(a[i-1], b[j-1])
            
            if score == F[i-1, j-1] + match_score:
                # Match/Mismatch - move diagonally
                aln_a.append(a[i-1])
                aln_b.append(b[j-1])
                i -= 1
                j -= 1
            elif score == F[i-1, j] + self.scoring.gap:
                # Gap in sequence B - move up
                aln_a.append(a[i-1])
                aln_b.append('-')
                i -= 1
            else:
                # Gap in sequence A - move left
                aln_a.append('-')
                aln_b.append(b[j-1])
                j -= 1
        
        # Reverse alignments
        aln_a.reverse()
        aln_b.reverse()
        
        return ''.join(aln_a), ''.join(aln_b)
    
    def align(self, seq1, seq2):
        """
        Perform Smith-Waterman local alignment
        
        Args:
            seq1: First sequence (string or list)
            seq2: Second sequence (string or list)
        
        Returns:
            tuple: (score, aligned_seq1, aligned_seq2)
        """
        a = list(seq1) if isinstance(seq1, str) else seq1
        b = list(seq2) if isinstance(seq2, str) else seq2
        
        n, m = len(a), len(b)
        
        # Initialize DP matrix
        F = np.zeros((n+1, m+1), dtype=int)
        max_score = 0
        max_pos = (0, 0)
        
        # Fill DP matrix
        for i in range(1, n+1):
            for j in range(1, m+1):
                # Can restart alignment (key difference from Needleman-Wunsch)
                F[i, j] = max(
                    0,
                    F[i-1, j-1] + self.scoring.similarity(a[i-1], b[j-1]),
                    F[i-1, j] + self.scoring.gap,
                    F[i, j-1] + self.scoring.gap
                )
                
                # Track maximum score position
                if F[i, j] > max_score:
                    max_score = F[i, j]
                    max_pos = (i, j)
        
        # Traceback from maximum score
        aligned_a, aligned_b = self._traceback(F, a, b, max_pos)
        
        return max_score, aligned_a, aligned_b


def get_aligner(algorithm_type, scoring):
    """
    Factory function to get appropriate aligner
    
    Args:
        algorithm_type: "needleman-wunsch" or "smith-waterman"
        scoring: AlignmentScoring object
    
    Returns:
        SequenceAligner instance
    """
    if algorithm_type.lower() in ["needleman-wunsch", "needleman", "global"]:
        return NeedlemanWunsch(scoring)
    elif algorithm_type.lower() in ["smith-waterman", "smith", "local"]:
        return SmithWaterman(scoring)
    else:
        raise ValueError(f"Unknown algorithm type: {algorithm_type}")
