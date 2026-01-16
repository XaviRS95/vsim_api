
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
