import subprocess
import re
from models.models import SyntaxResponse

def syntax_checker(code:str):

    filename = "prueba.sv"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    result = subprocess.run(
        ["vlog",filename],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return SyntaxResponse(
            error = 0,
        )
    else

        return result.stdout

def error_trace_extractor(trace: str)-> list:

    pattern = r"(\*\* Error:.*(?:\n\*\* Error:.*)*)"

    matches = re.findall(pattern, trace)

    for match in matches:
        print("--- Error Trace ---")
        print(match)

    return matches

code = """
module case_example1(input logic [1:0] a, output logic y);
    always_comb begin
        case(a)
            2'b00: y = 0;
            2'b01: y = 1;
            2'b10: y = 1;
            2'b11: y = 0;
            default: y = 0;
        endcase
    end
endmodue
"""

print(syntax_checker(code=code))