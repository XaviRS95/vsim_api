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
            print("OK")
            return SyntaxResponse(
                result="OK"
            )
        else:
            errors = error_trace_extractor(trace=result.stdout)
            #print(errors)
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
    print("Trace", trace)
    pattern = re.compile(r'^\*\*\s+Error\b.*$', re.MULTILINE)
    matches = pattern.findall(trace)
    combined = "\n".join(matches)
    print("Final traces:", combined)
    return combined