import os, re, subprocess, tempfile, shutil
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

def testbench_simulation_has_errors(output: str) -> bool:
    """
    Detects if Questa output contains simulation or compilation errors.
    """
    match = re.search(r"Errors:\s*(\d+)", output)

    if match:
        return int(match.group(1)) > 0

    # fallback in case the summary line is missing
    return "** Error:" in output


def testbench_checker(request: TestBenchRequest) -> TestBenchResponse:
    result = ''

    try:
        # Use a temporary directory for each request to avoid conflicts
        with tempfile.TemporaryDirectory() as tmpdir:

            testbench_filename = os.path.join(tmpdir, 'testbench.sv')
            dut_filename = os.path.join(tmpdir, 'dut.sv')
            asserts_filename = os.path.join(tmpdir, 'assert.sv')

            # Write files
            with open(testbench_filename, "w", encoding="utf-8") as f:
                f.write(request['testbench'])
            with open(dut_filename, "w", encoding="utf-8") as f:
                f.write(request['dut'])
            with open(asserts_filename, "w", encoding="utf-8") as f:
                f.write(request['asserts'])

            # Ensure a fresh work library
            work_lib = os.path.join(tmpdir, "work")
            if os.path.exists(work_lib):
                shutil.rmtree(work_lib)
            subprocess.run(["vlib", "work"], cwd=tmpdir, check=True)

            # Compile
            compiling_result = subprocess.run(
                ["vlog", "-sv", dut_filename, asserts_filename, testbench_filename],
                capture_output=True,
                text=True,
                cwd=tmpdir
            )

            if compiling_result.returncode != 0:
                result = f'Error in compiling testbench:\n{compiling_result.stdout}\n{compiling_result.stderr}'
            else:
                # Simulate
                simulation_result = subprocess.run(
                    [
                        "vsim",
                        "-voptargs=+acc=npr",  # Enable signal visibility
                        "-c",  # Command line mode
                        "-do", "run -all; coverage save -onexit coverage.ucdb; exit",
                        "work.testbench"
                    ],
                    capture_output=True,
                    text=True,
                    cwd=tmpdir
                )

                # Combine stdout and stderr for error checking
                sim_output = simulation_result.stdout + simulation_result.stderr

                sim_failed = testbench_simulation_has_errors(output=sim_output)

                coverage_file = os.path.join(tmpdir, "coverage.ucdb")

                if os.path.exists(coverage_file):
                    coverage_result = subprocess.run(
                        ["vcover", "report", "-details", "-all", coverage_file],
                        capture_output=True,
                        text=True,
                        cwd=tmpdir
                    )
                    coverage_output = coverage_result.stdout
                    print("Coverage Report:\n", coverage_output)

                if sim_failed:
                    print(sim_output)
                    result = f'Error in simulating testbench:\n{sim_output}'
                else:
                    result = 'OK'

    except Exception as e:
        import traceback
        traceback.print_exc()
        result = f'Internal error: {e}'

    return TestBenchResponse(result=result)