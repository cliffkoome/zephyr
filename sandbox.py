import subprocess
import tempfile
import os

def execute_code(code_string: str) -> dict:
    """
    Executes Python code in a strictly isolated subprocess.
    Enforces a 3-second timeout to prevent infinite loops from crashing the server.
    """
    # Write the code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_script:
        temp_script.write(code_string)
        temp_file_path = temp_script.name

    try:
        # Run the script as a distinct process
        result = subprocess.run(
            ['python3', temp_file_path],
            capture_output=True,
            text=True,
            timeout=3.0  # Hard timeout constraint for ADTC rules
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "timeout": False
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "Error: Execution timed out (exceeded 3 seconds).",
            "timeout": True
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"System Error: {str(e)}",
            "timeout": False
        }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)