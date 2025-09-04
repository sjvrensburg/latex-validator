from typing import Dict, Any
from pylatexenc.latexwalker import LatexWalker, LatexWalkerError

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
        lw = LatexWalker(clean_string)
        lw.get_latex_nodes()
        result["is_valid"] = True
    except LatexWalkerError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        
    return result