import os, re, subprocess, tempfile, shutil, traceback
from models.models import SyntaxResponse, TestBenchResponse, TestBenchRequest
from .regex_utils import extract_report_data

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
    total_errors = 0
    coverage_pct = 0
    testing_data = ''

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
                ["vlog",
                 "-sv",
                 "+cover=bcesft",
                 dut_filename,
                 asserts_filename,
                 testbench_filename
                 ],
                capture_output=True,
                text=True,
                cwd=tmpdir
            )

            if compiling_result.returncode != 0:
                #print(compiling_result.stdout)
                is_testbench_correct = False
            else:

                # Create do file with proper coverage save
                do_content = """
                # Set up automatic coverage save on exit
                coverage save -onexit -assert -directive -cvg -codeAll coverage.ucdb

                # Run the simulation
                run -all

                # In case the testbench doesn't have $finish, save explicitly
                coverage save coverage.ucdb

                # Quit
                quit -f
                """

                do_file = os.path.join(tmpdir, "run.do")
                with open(do_file, "w") as f:
                    f.write(do_content)

                # Simulate
                simulation_result = subprocess.run(
                    [
                        "vsim",
                        "-coverage",
                        "-voptargs=+acc=npr",
                        "-c",
                        "-do", "run.do",
                        "work.tb"
                    ],
                    capture_output=True,
                    text=True,
                    cwd=tmpdir
                )

                # Check if coverage file exists
                coverage_file = os.path.join(tmpdir, "coverage.ucdb")
                if os.path.exists(coverage_file):
                    print("Coverage file generated successfully!")
                else:
                    print("Coverage file NOT generated")

                    # Check if there were any issues with the save command
                    transcript_file = os.path.join(tmpdir, "transcript")
                    if os.path.exists(transcript_file):
                        with open(transcript_file, 'r') as f:
                            transcript = f.read()
                            #print("Last part of transcript:", transcript[-500:])  # Show last 500 chars

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
                    coverage_report = coverage_result.stdout

                    coverage_data = extract_report_data(coverage_report=coverage_report)

                    #print(coverage_data)

                    testing_data = coverage_data['testing_data']
                    coverage_pct = coverage_data['coverage_pct']
                    total_errors = coverage_data['total_errors']

                else:
                    print('Unable to locate coverage file', coverage_file)

                if sim_failed:
                    #print(sim_output)
                    pass


    except Exception as e:
        traceback.print_exc()


    return TestBenchResponse(
        total_errors = total_errors,
        coverage_pct = coverage_pct,
        testing_data = testing_data
    )