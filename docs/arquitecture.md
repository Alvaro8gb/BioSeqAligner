# BioSeqAligner - MVC Architecture Documentation

## Overview

BioSeqAligner follows the **Model-View-Controller (MVC)** design pattern to separate concerns and improve code maintainability, testability, and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                   app.py                        │
│              (Controller + View)                │
│  ┌───────────────────────────────────────────┐  │
│  │  • main()                                 │  │
│  │  • render_sidebar()                       │  │
│  │  • render_sequence_inputs()              │  │
│  │  • render_metrics()                       │  │
│  │  • render_alignment_result()             │  │
│  │  • render_examples()                      │  │
│  │  • render_footer()                        │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│   algorithms.py      │    │  visualization.py    │
│      (Model)         │    │       (View)         │
│                      │    │                      │
│ • AlignmentScoring   │    │ • AlignmentStats     │
│ • SequenceAligner    │    │ • AlignmentVisualizer│
│ • NeedlemanWunsch    │    │ • LegendComponent    │
│ • SmithWaterman      │    │ • ExamplesComponent  │
│ • get_aligner()      │    │                      │
└──────────────────────┘    └──────────────────────┘
           ▲                            ▲
           │                            │
           └────────────┬───────────────┘
                        │
                  ┌─────────────┐
                  │  config.py  │
                  │             │
                  │ • Constants │
                  │ • Defaults  │
                  │ • Schemes   │
                  └─────────────┘
```

## Module Breakdown

### 1. Model Layer (`algorithms.py`)

**Purpose**: Contains the core business logic for sequence alignment algorithms.

**Classes**:

- `AlignmentScoring`: Encapsulates scoring parameters (match, mismatch, gap)
- `SequenceAligner`: Abstract base class for alignment algorithms
- `NeedlemanWunsch`: Implements global alignment algorithm
- `SmithWaterman`: Implements local alignment algorithm

**Functions**:
- `get_aligner(algorithm_type, scoring)`: Factory function to instantiate aligners

**Responsibilities**:
- Perform sequence alignment calculations
- Manage dynamic programming matrices
- Execute traceback procedures
- Return alignment scores and aligned sequences

**No dependencies on**: UI framework, visualization logic

### 2. View Layer (`visualization.py`)

**Purpose**: Handles presentation logic and data formatting.

**Classes**:

- `AlignmentStats`: Calculates statistics from alignment results
  - Methods: `_calculate_stats()`, `get_metrics()`
  - Computes: matches, mismatches, gaps, identity percentage

- `AlignmentVisualizer`: Generates HTML visualizations
  - Methods: `visualize_alignment()`, `format_text_alignment()`
  - Color-codes nucleotides (green=match, red=mismatch, yellow=gap)

- `LegendComponent`: Provides legend UI components
  - Methods: `get_legend_markdown()`, `get_legend_html()`

- `ExamplesComponent`: Manages example sequences
  - Attributes: `EXAMPLES` dictionary
  - Methods: `get_examples_markdown()`, `get_example()`, `get_all_examples()`

**Responsibilities**:
- Format alignment results for display
- Generate HTML/Markdown for UI components
- Calculate and present statistics
- Provide reusable UI elements

**No dependencies on**: Algorithm implementation details

### 3. Controller Layer (`app.py`)

**Purpose**: Orchestrates user interaction, coordinates between Model and View.

**Main Functions**:

- `main()`: Application entry point, sets up page configuration
- `render_sidebar()`: Handles algorithm selection and parameter inputs
- `render_sequence_inputs()`: Manages sequence input fields
- `render_metrics()`: Displays alignment statistics
- `render_alignment_result()`: Coordinates visualization of results
- `render_examples()`: Shows example sequences
- `render_footer()`: Renders application footer

**Workflow**:
```
User Input → Controller → Model (compute alignment)
                ↓
          View (format results)
                ↓
          Controller → Display to User
```

**Responsibilities**:
- Handle user input and events
- Validate sequences
- Call appropriate Model methods
- Pass results to View for formatting
- Manage Streamlit UI state
- Error handling and user feedback

### 4. Configuration (`config.py`)

**Purpose**: Centralized configuration and constants.

**Contents**:
- Default scoring parameters
- Predefined scoring schemes
- UI configuration (title, icons, colors)
- Default example sequences
- Algorithm metadata

**Benefits**:
- Easy to modify application-wide settings
- No magic numbers in code
- Simplified testing with different configurations

## Data Flow

### Alignment Request Flow

```
1. User enters sequences in UI (Controller)
2. User clicks "Align Sequences" button (Controller)
3. Controller validates input
4. Controller creates AlignmentScoring object (Model)
5. Controller calls get_aligner() to instantiate algorithm (Model)
6. Algorithm performs alignment and returns (score, seq1, seq2) (Model)
7. Controller creates AlignmentStats object (View)
8. Controller calls AlignmentVisualizer to generate HTML (View)
9. Controller displays results in UI (Controller)
```

### Class Interaction

```python
# Controller coordinates:
scoring = AlignmentScoring(match=1, mismatch=-1, gap=-2)  # Model
aligner = get_aligner("needleman-wunsch", scoring)         # Model
score, seq1, seq2 = aligner.align("GATTACA", "GTCGACGC")  # Model

stats = AlignmentStats(seq1, seq2, score)                  # View
visualizer = AlignmentVisualizer()                         # View
html = visualizer.visualize_alignment(seq1, seq2)          # View

st.markdown(html, unsafe_allow_html=True)                  # Controller
```


