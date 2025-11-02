"""
Configuration Module
Contains default settings and configuration options for the application
"""

# Default scoring parameters
DEFAULT_MATCH_SCORE = 1
DEFAULT_MISMATCH_SCORE = -1
DEFAULT_GAP_PENALTY = -2

# Predefined scoring schemes
SCORING_SCHEMES = {
    "Standard": {
        "match": 1,
        "mismatch": -1,
        "gap": -2,
        "description": "Standard scoring for DNA/RNA sequences"
    },
    "Strict": {
        "match": 2,
        "mismatch": -2,
        "gap": -3,
        "description": "Stricter penalties for mismatches and gaps"
    },
    "Lenient": {
        "match": 1,
        "mismatch": 0,
        "gap": -1,
        "description": "More lenient scoring for divergent sequences"
    },
    "BLAST-like": {
        "match": 1,
        "mismatch": -3,
        "gap": -2,
        "description": "Similar to BLAST default parameters"
    }
}

# UI Configuration
APP_TITLE = "BioSeqAligner"
APP_ICON = "🧬"
APP_SUBTITLE = "Sequence Alignment Visualizer"

# Color scheme for visualization
COLORS = {
    'gap': '#FFD700',           # Yellow
    'match': '#90EE90',         # Light green
    'mismatch': '#FF6B6B',      # Red
    'reference': '#FFFFFF',     # White
    'border': '#ccc'            # Light gray
}

# Example sequences
DEFAULT_SEQUENCE_1 = "GATTACA"
DEFAULT_SEQUENCE_2 = "GTCGACGC"

# Algorithm options
ALGORITHMS = {
    "Needleman-Wunsch": {
        "name": "Needleman-Wunsch (Global)",
        "type": "needleman-wunsch",
        "description": "Global alignment - best for sequences of similar length"
    },
    "Smith-Waterman": {
        "name": "Smith-Waterman (Local)",
        "type": "smith-waterman",
        "description": "Local alignment - best for finding similar regions"
    }
}
