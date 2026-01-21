    module proto_case_7_assertions (input logic clk, rst, lock_req, unlock, output logic locked, input logic clk);



    property p_locked_reset;
  @(posedge clk) (rst == 1) |-> (locked == 0);
endproperty
assert property (p_locked_reset) else $error("Assertion failed: locked should be reset to 0 when rst is asserted.");

property p_locked_req_set;
  @(posedge clk) ((locked == 1'b0) && (lock_req == 1)) |-> (locked == 1);
endproperty
assert property (p_locked_req_set) else $error("Assertion failed: locked should be set to 1 when lock_req is asserted and locked was previously 0.");

property p_locked_unlock_reset;
  @(posedge clk) ((locked == 1'b1) && (unlock == 1)) |-> (locked == 0);
endproperty
assert property (p_locked_unlock_reset) else $error("Assertion failed: locked should be reset to 0 when unlock is asserted and locked was previously 1.");

    endmodule;