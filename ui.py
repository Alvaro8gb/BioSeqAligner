"""
Visualization Module
Handles the display and formatting of alignment results
"""


class AlignmentStats:
    """Calculate and store alignment statistics"""
    
    def __init__(self, aligned_seq1, aligned_seq2, score):
        self.aligned_seq1 = aligned_seq1
        self.aligned_seq2 = aligned_seq2
        self.score = score
        self._calculate_stats()
    
    def _calculate_stats(self):
        """Calculate alignment statistics"""
        self.matches = sum(
            1 for a, b in zip(self.aligned_seq1, self.aligned_seq2)
            if a == b and a != '-'
        )
        
        self.mismatches = sum(
            1 for a, b in zip(self.aligned_seq1, self.aligned_seq2)
            if a != b and a != '-' and b != '-'
        )
        
        self.gaps = self.aligned_seq1.count('-') + self.aligned_seq2.count('-')
        
        self.length = len(self.aligned_seq1)
        
        self.identity = (self.matches / self.length * 100) if self.length > 0 else 0
    
    def get_metrics(self):
        """Return metrics as dictionary"""
        return {
            'score': self.score,
            'matches': self.matches,
            'mismatches': self.mismatches,
            'gaps': self.gaps,
            'length': self.length,
            'identity': self.identity
        }


class AlignmentVisualizer:
    """Generate HTML visualizations for sequence alignments"""
    
    # Color scheme
    COLORS = {
        'gap': '#FFD700',           # Yellow
        'match': '#90EE90',         # Light green
        'mismatch': '#FF6B6B',      # Red
        'reference': '#FFFFFF',     # White
        'border': '#ccc'            # Light gray
    }
    
    @staticmethod
    def _create_cell(char, color, border_color='#ccc'):
        """Create a single colored table cell for a character"""
        return (
            f'<td style="background-color: {color}; '
            f'color: #000; text-align:center; padding: 4px; '
            f'border: 1px solid {border_color};">{char}</td>'
        )
    
    @staticmethod
    def _create_match_indicator(c1, c2):
        """Create match/mismatch indicator between two characters"""
        if c1 == '-' or c2 == '-':
            symbol = ' '
        elif c1 == c2:
            symbol = '|'
        else:
            symbol = 'x'
        return f'<td style="text-align:center; padding:4px; color:#888;">{symbol}</td>'
    
    @classmethod
    def visualize_alignment(cls, seq1, seq2):
        """
        Create colored HTML visualization of alignment in a table, centered.
        
        Args:
            seq1: First aligned sequence (reference)
            seq2: Second aligned sequence (query)
        
        Returns:
            str: HTML string with table visualization
        """
        html = '<div style="display:flex; justify-content:center;">'
        html += '<table style="border-collapse: collapse; font-family: monospace; font-size: 24px; line-height: 1.8;">'

        # Sequence 1 row
        html += '<tr>'
        for char in seq1:
            color = cls.COLORS['gap'] if char == '-' else cls.COLORS['reference']
            html += cls._create_cell(char, color, cls.COLORS['border'])
        html += '</tr>'

        # Match indicator row
        html += '<tr>'
        for c1, c2 in zip(seq1, seq2):
            html += cls._create_match_indicator(c1, c2)
        html += '</tr>'

        # Sequence 2 row
        html += '<tr>'
        for c1, c2 in zip(seq1, seq2):
            if c2 == '-':
                color = cls.COLORS['gap']
            elif c1 == c2:
                color = cls.COLORS['match']
            else:
                color = cls.COLORS['mismatch']
            html += cls._create_cell(c2, color, cls.COLORS['border'])
        html += '</tr>'

        html += '</table></div>'
        return html

    @staticmethod
    def format_text_alignment(seq1, seq2):
        """
        Format alignment as plain text with match indicators
        
        Args:
            seq1: First aligned sequence
            seq2: Second aligned sequence
        
        Returns:
            str: Formatted text alignment
        """
        match_line = ''.join('|' if a == b else ' ' for a, b in zip(seq1, seq2))
        label = "Sequence 1: "
        padding = ' ' * len(label)
        return f"{label}{seq1}\n{padding}{match_line}\nSequence 2: {seq2}"


class LegendComponent:
    """Generate legend HTML for alignment visualization"""
    
    @staticmethod
    def get_legend_markdown():
        """Return legend as markdown string"""
        return """
        ### Legend
        🟢 **Green**: Matching nucleotides  
        🔴 **Red**: Mismatching nucleotides  
        🟡 **Yellow**: Gaps (-)
        """
    
    @staticmethod
    def get_legend_html():
        """Return legend as HTML string"""
        return """
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4 style="margin-top: 0;">Legend</h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div>🟢 <strong>Green</strong>: Matching nucleotides</div>
                <div>🔴 <strong>Red</strong>: Mismatching nucleotides</div>
                <div>🟡 <strong>Yellow</strong>: Gaps (-)</div>
            </div>
        </div>
        """


class ExamplesComponent:
    """Provide example sequences for testing"""
    
    EXAMPLES = {
        "High similarity": {
            "seq1": "GATTACA",
            "seq2": "GATTACA",
            "description": "Two identical sequences"
        },
        "With mutations": {
            "seq1": "GATTACA",
            "seq2": "GTCGACGC",
            "description": "Sequences with substitutions"
        },
        "E. coli fragment": {
            "seq1": "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC",
            "seq2": "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC",
            "description": "Real E. coli genome fragment"
        },
        "Local alignment": {
            "seq1": "AAAGGGTTTTCCCC",
            "seq2": "GGGTT",
            "description": "Best for Smith-Waterman (local alignment)"
        }
    }
    
    @classmethod
    def get_examples_markdown(cls):
        """Return examples as markdown string"""
        markdown = "**Example Sequences:**\n\n"
        for name, data in cls.EXAMPLES.items():
            markdown += f"**{name}** - {data['description']}:\n"
            markdown += f"- Sequence 1: `{data['seq1']}`\n"
            markdown += f"- Sequence 2: `{data['seq2']}`\n\n"
        return markdown
    
    @classmethod
    def get_example(cls, name):
        """Get a specific example by name"""
        return cls.EXAMPLES.get(name)
    
    @classmethod
    def get_all_examples(cls):
        """Get all examples"""
        return cls.EXAMPLES
