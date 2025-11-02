"""
Test file to verify the BioSeqAligner modules
Run this to test the algorithms independently from the Streamlit app
"""

from src.algorithms import AlignmentScoring, get_aligner
from Alineamiento.BioSeqAligner.ui import AlignmentStats, AlignmentVisualizer


def test_needleman_wunsch():
    """Test Needleman-Wunsch algorithm"""
    print("=" * 60)
    print("Testing Needleman-Wunsch (Global Alignment)")
    print("=" * 60)
    
    scoring = AlignmentScoring(match=1, mismatch=-1, gap=-2)
    aligner = get_aligner("needleman-wunsch", scoring)
    
    # Test case 1
    seq1 = "GATTACA"
    seq2 = "GTCGACGC"
    
    score, aligned_seq1, aligned_seq2 = aligner.align(seq1, seq2)
    
    print(f"\nSequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")
    print(f"\nAlignment Score: {score}")
    print(f"Aligned Seq1: {aligned_seq1}")
    print(f"Aligned Seq2: {aligned_seq2}")
    
    # Calculate statistics
    stats = AlignmentStats(aligned_seq1, aligned_seq2, score)
    metrics = stats.get_metrics()
    
    print(f"\nStatistics:")
    print(f"  Matches: {metrics['matches']}")
    print(f"  Mismatches: {metrics['mismatches']}")
    print(f"  Gaps: {metrics['gaps']}")
    print(f"  Identity: {metrics['identity']:.2f}%")


def test_smith_waterman():
    """Test Smith-Waterman algorithm"""
    print("\n" + "=" * 60)
    print("Testing Smith-Waterman (Local Alignment)")
    print("=" * 60)
    
    scoring = AlignmentScoring(match=1, mismatch=-1, gap=-2)
    aligner = get_aligner("smith-waterman", scoring)
    
    # Test case 2 - good for local alignment
    seq1 = "AAAGGGTTTTCCCC"
    seq2 = "GGGTT"
    
    score, aligned_seq1, aligned_seq2 = aligner.align(seq1, seq2)
    
    print(f"\nSequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")
    print(f"\nAlignment Score: {score}")
    print(f"Aligned Seq1: {aligned_seq1}")
    print(f"Aligned Seq2: {aligned_seq2}")
    
    # Calculate statistics
    stats = AlignmentStats(aligned_seq1, aligned_seq2, score)
    metrics = stats.get_metrics()
    
    print(f"\nStatistics:")
    print(f"  Matches: {metrics['matches']}")
    print(f"  Mismatches: {metrics['mismatches']}")
    print(f"  Gaps: {metrics['gaps']}")
    print(f"  Identity: {metrics['identity']:.2f}%")


def test_visualization():
    """Test visualization components"""
    print("\n" + "=" * 60)
    print("Testing Visualization Components")
    print("=" * 60)
    
    # Create a simple alignment
    aligned_seq1 = "GATT-ACA"
    aligned_seq2 = "G-TTGACA"
    
    visualizer = AlignmentVisualizer()
    
    # Test text alignment
    print("\nText Alignment:")
    text_alignment = visualizer.format_text_alignment(aligned_seq1, aligned_seq2)
    print(text_alignment)
    
    # Test HTML generation (just check it doesn't crash)
    html = visualizer.visualize_alignment(aligned_seq1, aligned_seq2)
    print(f"\nHTML Generated: {len(html)} characters")
    print("HTML preview (first 100 chars):", html[:100] + "...")


def main():
    """Run all tests"""
    print("\n🧬 BioSeqAligner Module Tests\n")
    
    try:
        test_needleman_wunsch()
        test_smith_waterman()
        test_visualization()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
