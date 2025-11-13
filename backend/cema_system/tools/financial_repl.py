import pandas as pd
import sys
from io import StringIO
from pathlib import Path


def _load_dre_data():
    csv_path = Path(__file__).parent.parent / "knowledge_base" / "PEQUENA" / "doc2_dre.csv"
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        return pd.DataFrame()

_DRE_DF = _load_dre_data()

def financial_python_repl(code: str) -> str:
    """
    Executes Python code for financial analysis.

    The environment already has a pandas DataFrame loaded in the df variable. This DataFrame contains the Income Statement (DRE) data.

    Args: 
        code (str): Valid Python code to execute. 
                    Use print() to return results.

    Returns: 
        str: The output printed to stdout or an error message.
    """
    # Buffer to return print() statements
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
# Define the local execution scope with pre-loaded data
    local_scope = {
        "pd": pd,
        "df": _DRE_DF,
        "result": None
    }
    
    try:
        # Using exec() implies trusting the generated code (safe for tests)
        exec(code, {}, local_scope)

        # Retrieve captured output
        output = redirected_output.getvalue()
        
        if not output.strip():
            return "Code executed successfully, but produced no output. YOU HAVE to use `print()`?"
            
        return output

    except Exception as e:
        return f"PYTHON EXECUTION ERROR: {str(e)}"
    finally:
        # Restore standard stdout
        sys.stdout = old_stdout
