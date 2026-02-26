import os, re, subprocess
from models.models import SyntaxResponse, TestBenchResponse, TestBenchRequest

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

def testbench_checker(request: TestBenchRequest) -> TestBenchResponse:
    testbench_filename = 'testbench.sv'
    dut_filename = 'dut.sv'
    asserts_filename = 'assert.sv'

    result = ''

    try:
        with open(testbench_filename, "w", encoding="utf-8") as f:
            f.write(request['testbench'])
        with open(dut_filename, "w", encoding="utf-8") as f:
            f.write(request['dut'])
        with open(asserts_filename, "w", encoding="utf-8") as f:
            f.write(request['asserts'])

        compiling_result = subprocess.run(
            ["vlog", "-sv", dut_filename, asserts_filename, testbench_filename],
            capture_output=True,
            text=True
        )

        compiling_result_stdout = compiling_result.stdout
        compiling_result_returncode = compiling_result.returncode

        if compiling_result_returncode != 0:

            print(f"COMPILING RESULT: {compiling_result}")

            result = f'Error in compiling testbench: {compiling_result_stdout}'

        else:

            simulation_result = subprocess.run([
                "vsim", "-c",
                "tb",
                "-voptargs=+acc=npr",
                "-do", "run -all; quit -f"
            ])
            simulation_returncode = simulation_result.returncode

            print(f"SIMULATION RESULT: {simulation_result}")

            if simulation_returncode !=0:

                result = f'Error in simulating testbench: {simulation_result}'

            else:

                result = 'OK'

    except Exception as e:
        print(e)

        result=f'Internal error: {e}'

    finally:
        if os.path.exists(testbench_filename):
            os.remove(testbench_filename)
        if os.path.exists(dut_filename):
            os.remove(dut_filename)
        if os.path.exists(asserts_filename):
            os.remove(asserts_filename)

        return TestBenchResponse(
                result=result
            )