"""
LaTeX Validation Module

This module provides functionality to validate LaTeX expressions for syntactic correctness
using the pylatexenc library. It serves as the core validation engine for the latex-validator
package, offering robust syntactic parsing validation.

The primary function `validate_latex()` checks LaTeX code for:
- Proper syntax (balanced braces, matched delimiters, valid command structure)
- Structural integrity (math mode consistency, environment matching)

Key Features:
- Strict syntactic validation using pylatexenc's non-tolerant parsing mode
- Detection of unmatched braces, brackets, and math mode delimiters
- Comprehensive error reporting with specific error messages
- JSON-compatible output format for easy integration
- Handles both simple expressions and complex LaTeX structures

Example Usage:
    >>> from latex_validator.validate import validate_latex
    >>> result = validate_latex(r"\\textbf{hello world}")
    >>> print(result)
    {'expression': '\\textbf{hello world}', 'is_valid': True, 'error': None}
    
    >>> result = validate_latex(r"\\textbf{unclosed")
    >>> print(result)
    {'expression': '\\textbf{unclosed', 'is_valid': False, 'error': 'LaTeX syntax error: ...'}

Implementation Notes:
- Uses pylatexenc.LatexWalker with tolerant_parsing=False for strict validation
- Performs secondary validation via text conversion to catch structural issues
- Focuses on syntactic correctness rather than semantic validation (e.g., \\txtbf 
  will pass validation as it's syntactically valid, even though it's not a standard 
  LaTeX command)
- Designed to be fast and lightweight for use in CLI tools and batch processing

Dependencies:
- pylatexenc >= 2.10: For LaTeX parsing and text conversion
- typing: For type hints (Python 3.5+)

Author: Your Name
License: MIT
Version: 1.0.0
"""
from typing import Dict, Any
from pylatexenc.latexwalker import LatexWalker, LatexWalkerError, LatexWalkerParseError
from pylatexenc.latex2text import LatexNodes2Text

def validate_latex(latex_string: str) -> Dict[str, Any]:
    """
    Checks if a given string of LaTeX code is syntactically valid.

    Args:
        latex_string: The string containing the LaTeX expression.

    Returns:
        A dictionary with keys 'expression' (str), 'is_valid' (bool), and 'error' (str or None).
    """
    result = {
        "expression": latex_string.strip(),
        "is_valid": False,
        "error": None
    }
    
    clean_string = latex_string.strip()
    if not clean_string:
        result["error"] = "Empty input"
        return result

    try:
        # Key fix: Disable tolerant parsing and enable strict braces
        lw = LatexWalker(
            clean_string, 
            tolerant_parsing=False,  # This is the crucial setting!
            strict_braces=True       # Also enable strict brace checking
        )
        
        # Use the older API since it's more widely supported
        nodes, _, _ = lw.get_latex_nodes()
        
        # Additional validation: try to render to text to catch structural issues
        # This helps catch things like unmatched math mode delimiters
        try:
            converter = LatexNodes2Text()
            # This will fail on structural problems
            _ = converter.nodelist_to_text(nodes)
        except Exception as text_error:
            result["error"] = f"LaTeX structure error: {str(text_error)}"
            return result
            
        result["is_valid"] = True
        
    except LatexWalkerParseError as e:
        result["error"] = f"LaTeX syntax error: {str(e)}"
    except LatexWalkerError as e:
        result["error"] = f"LaTeX parsing error: {str(e)}"  
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        
    return result