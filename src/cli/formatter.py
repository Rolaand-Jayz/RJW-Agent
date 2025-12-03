"""
Output formatting utilities for the CLI.

Provides colored and styled terminal output using only ANSI escape codes (no external dependencies).
"""


class Formatter:
    """
    Terminal output formatter using ANSI escape codes.
    
    Provides methods for styled output similar to modern CLI tools.
    """
    
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize formatter.
        
        Args:
            use_colors: Enable colored output (default: True)
        """
        self.use_colors = use_colors
    
    def _style(self, text: str, *styles) -> str:
        """
        Apply styles to text.
        
        Args:
            text: Text to style
            *styles: Style codes to apply
            
        Returns:
            Styled text
        """
        if not self.use_colors:
            return text
        
        style_str = ''.join(styles)
        return f"{style_str}{text}{self.RESET}"
    
    def bold(self, text: str) -> str:
        """Make text bold."""
        return self._style(text, self.BOLD)
    
    def dim(self, text: str) -> str:
        """Make text dim."""
        return self._style(text, self.DIM)
    
    def italic(self, text: str) -> str:
        """Make text italic."""
        return self._style(text, self.ITALIC)
    
    def underline(self, text: str) -> str:
        """Underline text."""
        return self._style(text, self.UNDERLINE)
    
    def success(self, text: str) -> str:
        """Format as success message (green)."""
        return self._style(text, self.GREEN)
    
    def error(self, text: str) -> str:
        """Format as error message (red)."""
        return self._style(text, self.BRIGHT_RED, self.BOLD)
    
    def warning(self, text: str) -> str:
        """Format as warning message (yellow)."""
        return self._style(text, self.YELLOW)
    
    def info(self, text: str) -> str:
        """Format as info message (cyan)."""
        return self._style(text, self.CYAN)
    
    def header(self, text: str) -> str:
        """Format as header (bold cyan)."""
        return self._style(text, self.BOLD, self.CYAN)
    
    def section(self, text: str) -> str:
        """Format as section header (bold)."""
        return self._style(text, self.BOLD)
    
    def prompt(self) -> str:
        """Format the input prompt."""
        return self._style("rjw> ", self.BRIGHT_BLUE, self.BOLD)
    
    def list_item(self, text: str) -> str:
        """Format as list item."""
        bullet = self._style("•", self.DIM)
        return f"  {bullet} {text}"
    
    def code(self, text: str) -> str:
        """Format as code (monospace style)."""
        return self._style(text, self.BRIGHT_BLACK)
    
    def highlight(self, text: str) -> str:
        """Highlight text (bright yellow)."""
        return self._style(text, self.BRIGHT_YELLOW, self.BOLD)
    
    def format_dict(self, data: dict, indent: int = 0) -> str:
        """
        Format a dictionary for display.
        
        Args:
            data: Dictionary to format
            indent: Indentation level
            
        Returns:
            Formatted string
        """
        lines = []
        prefix = "  " * indent
        
        for key, value in data.items():
            key_str = self.bold(str(key))
            
            if isinstance(value, dict):
                lines.append(f"{prefix}{key_str}:")
                lines.append(self.format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key_str}:")
                for item in value:
                    lines.append(f"{prefix}  {self.list_item(str(item))}")
            else:
                lines.append(f"{prefix}{key_str}: {value}")
        
        return '\n'.join(lines)
    
    def format_table(self, headers: list, rows: list) -> str:
        """
        Format data as a simple table.
        
        Args:
            headers: List of column headers
            rows: List of row data (each row is a list)
            
        Returns:
            Formatted table string
        """
        # Calculate column widths
        col_widths = [len(str(h)) for h in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Format header
        header_line = " | ".join(
            self.bold(str(h).ljust(w)) 
            for h, w in zip(headers, col_widths)
        )
        
        separator = "-+-".join("-" * w for w in col_widths)
        
        # Format rows
        row_lines = []
        for row in rows:
            row_line = " | ".join(
                str(cell).ljust(w)
                for cell, w in zip(row, col_widths)
            )
            row_lines.append(row_line)
        
        # Combine
        return "\n".join([header_line, separator] + row_lines)
