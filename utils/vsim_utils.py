import os, re, subprocess
from models.models import SyntaxResponse

def syntax_checker(code:str):
    filename = "prueba.sv"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            ["vlog", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return SyntaxResponse(
                result="OK"
            )
        else:
            errors = error_trace_extractor(trace=result.stdout)
            return SyntaxResponse(
                result=errors
            )
    except Exception as e:
        print(e)
    finally:
        # Clean up auxiliary file
        if os.path.exists(filename):
            os.remove(filename)

def error_trace_extractor(trace: str)-> str:
    pattern = r"(\*\* Error:.*(?:\n\*\* Error:.*)*)"
    matches = re.findall(pattern, trace)
    combined = "\n".join(matches)
    return combined