import re


def extract_assertion_data(report_text):
    # 1. Isolate the ASSERTION RESULTS section
    # Matches from the header until the "End time" marker
    section_pattern = r"ASSERTION RESULTS:.*?(?=End time:)"
    section_match = re.search(section_pattern, report_text, re.DOTALL)

    if not section_match:
        return None

    section_content = section_match.group(0)

    # 2. Extract Table Rows
    # This pattern looks for the path, then the file(line) on the next line,
    # and finally the failure/pass counts.
    table_pattern = r"(/[^\s]+)\s+([^\s]+\(\d+\))\s+(\d+)\s+(\d+)"
    table_data = re.findall(table_pattern, section_content)
    # Formatted as: [(Name, File_Line, Failure_Count, Pass_Count), ...]

    # 3. Extract Coverage Percentage
    coverage_match = re.search(r"Total Coverage.*?: ([\d.]+)%", section_content)
    coverage = coverage_match.group(1) if coverage_match else None

    # 4. Extract Total Errors
    # We look outside the specific assertion section for the final summary line
    error_match = re.search(r"Errors:\s*(\d+)", report_text)
    errors = error_match.group(1) if error_match else None

    return {
        "table": table_data,
        "coverage_pct": coverage,
        "total_errors": errors
    }


# --- Example Usage ---
report = """

QuestaSim-64 vcover 2023.4 Coverage Utility 2023.10 Oct  9 2023
Start time: 12:00:40 on Mar 13,2026
vcover report -details -all /tmp/tmpthbf3d8r/coverage.ucdb 
Coverage Report by instance with details

=================================================================================
=== Instance: /tb/dut
=== Design Unit: work.case6
=================================================================================
Branch Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Branches                         4         4         0   100.00%

================================Branch Details================================

Branch Coverage for instance /tb/dut

    Line         Item                      Count     Source 
    ----         ----                      -----     ------ 
  File dut.sv
------------------------------------CASE Branch------------------------------------
    3                                         83     Count coming in to CASE
    4               1                         20     
    5               1                         19     
    6               1                         24     
    7               1                         20     
Branch totals: 4 hits of 4 branches = 100.00%


Statement Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Statements                       5         5         0   100.00%

================================Statement Details================================

Statement Coverage for instance /tb/dut --

    Line         Item                      Count     Source 
    ----         ----                      -----     ------ 
  File dut.sv
    2               1                         83     
    4               1                         20     
    5               1                         19     
    6               1                         24     
    7               1                         20     
Toggle Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Toggles                         10        10         0   100.00%

================================Toggle Details================================

Toggle Coverage for instance /tb/dut --

                                              Node      1H->0L      0L->1H  "Coverage"
                                              ---------------------------------------
                                        light[0-2]           1           1      100.00 
                                        state[0-1]           1           1      100.00 

Total Node Count     =          5 
Toggled Node Count   =          5 
Untoggled Node Count =          0 

Toggle Coverage      =     100.00% (10 of 10 bins)

=================================================================================
=== Instance: /tb/assertions
=== Design Unit: work.case6_asserts
=================================================================================

Assertion Coverage:
    Assertions                       3         3         0   100.00%
--------------------------------------------------------------------
Name                 File(Line)                   Failure      Pass 
                                                  Count        Count
--------------------------------------------------------------------
/tb/assertions/aoogioobjpdfknkiocnfdmkfcenmalei
                     assert.sv(7)                       0          1
/tb/assertions/aocjbnoleigmkbkfbcmcknoglchbjcke
                     assert.sv(8)                       0          1
/tb/assertions/dhdpngbaknfpkainpnbikjeilljknmaj
                     assert.sv(9)                       0          1
Toggle Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Toggles                         10        10         0   100.00%

================================Toggle Details================================

Toggle Coverage for instance /tb/assertions --

                                              Node      1H->0L      0L->1H  "Coverage"
                                              ---------------------------------------
                                        light[0-2]           1           1      100.00 
                                        state[0-1]           1           1      100.00 

Total Node Count     =          5 
Toggled Node Count   =          5 
Untoggled Node Count =          0 

Toggle Coverage      =     100.00% (10 of 10 bins)

=================================================================================
=== Instance: /tb
=== Design Unit: work.tb
=================================================================================
Statement Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Statements                       7         7         0   100.00%

================================Statement Details================================

Statement Coverage for instance /tb --

    Line         Item                      Count     Source 
    ----         ----                      -----     ------ 
  File testbench.sv
    20              1                          1     
    20              2                        100     
    22              1                        100     
    24              1                        100     
    25              1                        100     
    27              1                          1     
    28              1                          1     
Toggle Coverage:
    Enabled Coverage              Bins      Hits    Misses  Coverage
    ----------------              ----      ----    ------  --------
    Toggles                         10        10         0   100.00%

================================Toggle Details================================

Toggle Coverage for instance /tb --

                                              Node      1H->0L      0L->1H  "Coverage"
                                              ---------------------------------------
                                        light[0-2]           1           1      100.00 
                                        state[0-1]           1           1      100.00 

Total Node Count     =          5 
Toggled Node Count   =          5 
Untoggled Node Count =          0 

Toggle Coverage      =     100.00% (10 of 10 bins)


ASSERTION RESULTS:
--------------------------------------------------------------------
Name                 File(Line)                   Failure      Pass 
                                                  Count        Count
--------------------------------------------------------------------
/tb/assertions/aoogioobjpdfknkiocnfdmkfcenmalei
                     assert.sv(7)                       0          1
/tb/assertions/aocjbnoleigmkbkfbcmcknoglchbjcke
                     assert.sv(8)                       0          1
/tb/assertions/dhdpngbaknfpkainpnbikjeilljknmaj
                     assert.sv(9)                       0          1

Total Coverage By Instance (filtered view): 100.00%

End time: 12:00:40 on Mar 13,2026, Elapsed time: 0:00:00
Errors: 0, Warnings: 0


"""

results = extract_assertion_data(report)
print(results)