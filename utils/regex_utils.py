import re

def extract_report_data(coverage_report: str)-> dict:
    # 1. Isolate the ASSERTION RESULTS section
    # Matches from the header until the "End time" marker
    section_pattern = r"ASSERTION RESULTS:.*?(?=End time:)"
    section_match = re.search(section_pattern, coverage_report, re.DOTALL)

    if not section_match:
        return {
        "testing_data": '',
        "coverage_pct": 0,
        "total_errors": 0
        }


    section_content = section_match.group(0)

    # 2. Extract Table Rows
    # This pattern looks for the path, then the file(line) on the next line,
    # and finally the failure/pass counts.
    table_pattern = r"(/[^\s]+)\s+([^\s]+\(\d+\))\s+(\d+)\s+(\d+)"
    table_data = re.findall(table_pattern, section_content)
    # Formatted as: [(Name, File_Line, Failure_Count, Pass_Count), ...]

    # 3. Extract Coverage Percentage
    coverage_match = re.search(r"Total Coverage.*?: ([\d.]+)%", section_content)
    coverage = float(coverage_match.group(1)) if coverage_match else 0

    # 4. Extract Total Errors
    # We look outside the specific assertion section for the final summary line
    error_match = re.search(r"Errors:\s*(\d+)", coverage_report)
    errors = int(error_match.group(1)) if error_match else 0

    return {
        "testing_data": table_data,
        "coverage_pct": coverage,
        "total_errors": errors
    }