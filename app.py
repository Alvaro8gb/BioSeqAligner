"""
BioSeqAligner - Streamlit Web Application
Main application file with UI components and views
"""

import streamlit as st
from src.algorithms import AlignmentScoring, get_aligner
from ui import (
    AlignmentStats,
    AlignmentVisualizer,
    LegendComponent,
    ExamplesComponent
)

import streamlit.components.v1 as components


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    """Render sidebar with algorithm selection and parameters"""
    st.header("⚙️ Settings")
    
    # Algorithm selection
    algorithm = st.selectbox(
        "Select Algorithm",
        ["Needleman-Wunsch (Global)", "Smith-Waterman (Local)"],
        help="Needleman-Wunsch: Global alignment\nSmith-Waterman: Local alignment"
    )
    
    # Scoring parameters
    st.subheader("Scoring Parameters")
    match_score = st.number_input("Match Score", value=1, min_value=-10, max_value=10)
    mismatch_score = st.number_input("Mismatch Score", value=-1, min_value=-10, max_value=10)
    gap_penalty = st.number_input("Gap Penalty", value=-2, min_value=-10, max_value=0)
    
    # Legend
    st.markdown("---")
    st.markdown(LegendComponent.get_legend_markdown())
    
    return algorithm, AlignmentScoring(match_score, mismatch_score, gap_penalty)


def render_sequence_inputs():
    """Render input fields for sequences"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sequence 1 (Reference)")
        seq1_input = st.text_area(
            "Enter first sequence",
            value="GATTACA",
            height=100,
            help="Enter DNA/RNA sequence (A, T, G, C, U)"
        )
    
    with col2:
        st.subheader("Sequence 2 (Query)")
        seq2_input = st.text_area(
            "Enter second sequence",
            value="GTCGACGC",
            height=100,
            help="Enter DNA/RNA sequence (A, T, G, C, U)"
        )
    
    # Clean sequences
    seq1 = seq1_input.strip().upper().replace(" ", "").replace("\n", "")
    seq2 = seq2_input.strip().upper().replace(" ", "").replace("\n", "")
    
    return seq1, seq2


def render_metrics(stats):
    """Render alignment metrics in columns"""
    metrics = stats.get_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Alignment Score", metrics['score'])
    with col2:
        st.metric("Matches", metrics['matches'])
    with col3:
        st.metric("Mismatches", metrics['mismatches'])
    with col4:
        st.metric("Gaps", metrics['gaps'])


def render_alignment_result(aligned_seq1, aligned_seq2, stats, algorithm_name):
    """Render alignment visualization and details"""
    st.success("✅ Alignment completed!")
    
    render_metrics(stats)
    
    st.markdown("---")
    st.subheader(f"📊 Alignment Visualization - {algorithm_name}")
    
    visualizer = AlignmentVisualizer()
    alignment_html = visualizer.visualize_alignment(aligned_seq1, aligned_seq2)
    st.markdown(alignment_html, unsafe_allow_html=True)
    
    # Details in expander
    with st.expander("📋 View Alignment Details"):
        text_alignment = visualizer.format_text_alignment(aligned_seq1, aligned_seq2)
        st.code(text_alignment)
        
        metrics = stats.get_metrics()
        st.write(f"**Identity:** {metrics['identity']:.2f}%")
        st.write(f"**Alignment Length:** {metrics['length']}")


def render_explanation(): 
    """Render explantion  section"""
    url = "https://experiments.mostafa.io/needleman-wunsch/"
    with st.expander("💡  Algorithm Understanding"):
        # Crear un iframe
        components.html(
            f"""
            <iframe src="{url}" 
                    width="800" 
                    height="600" 
                    style="border:none; background-color:white;">
            </iframe>
            """,
            height=600,
        )
    
def render_examples():
    """Render examples section"""
    with st.expander("🗨️ Example Sequences"):
        st.markdown(ExamplesComponent.get_examples_markdown())


def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
            BioSeqAligner 
            <a href='https://creativecommons.org/licenses/by-nc/4.0/' target='_blank'>
                CC BY-NC 4.0
            </a><br>
            Desarrollado por Álvaro García Barragán y Pablo Fernandez Lopez.
        </div>
        """,
        unsafe_allow_html=True
    )



# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="BioSeqAligner",
        page_icon="🧬",
        layout="wide"
    )

   
    # Header
    st.title("🧬 BioSeqAligner - Sequence Alignment Visualizer")
    st.markdown("Compare two DNA/RNA sequences using Needleman-Wunsch or Smith-Waterman algorithms")
    
    # Sidebar
    with st.sidebar:
        algorithm_choice, scoring = render_sidebar()
    
    # Main content
    seq1, seq2 = render_sequence_inputs()
    
    if st.button("🔍 Align Sequences", type="primary", use_container_width=True):
        if not seq1 or not seq2:
            st.error("⚠️ Please enter both sequences!")
        else:
            with st.spinner("Aligning sequences..."):
                try:
                    if "Needleman-Wunsch" in algorithm_choice:
                        aligner = get_aligner("needleman-wunsch", scoring)
                        algo_name = "Needleman-Wunsch (Global Alignment)"
                    else:
                        aligner = get_aligner("smith-waterman", scoring)
                        algo_name = "Smith-Waterman (Local Alignment)"
                    
                    score, aligned_seq1, aligned_seq2 = aligner.align(seq1, seq2)
                    
                    stats = AlignmentStats(aligned_seq1, aligned_seq2, score)
                    
                    render_alignment_result(aligned_seq1, aligned_seq2, stats, algo_name)
                    
                except Exception as e:
                    st.error(f"❌ Error during alignment: {str(e)}")
    
    render_examples()
    render_explanation()
    render_footer()


if __name__ == "__main__":
    main()

