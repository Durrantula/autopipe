// Benchmark "ADD2" written by ABC on Tue Apr 13 09:44:13 2021

module ADD2 ( clock, 
    a0, a1, b0, b1,
    z0, z1, z2  );
  input  clock;
  input  a0, a1, b0, b1;
  output z0, z1, z2;
  reg z2, z1, z0;
  wire \new_ADD2|c_ , new_n30_, new_n32_, new_n34_, new_n36_, new_n38_,
    \new_ADD2|0_ , new_n42_, new_n44_, new_n46_, new_n48_, new_n50_, n20,
    n23, n26;
  assign \new_ADD2|c_  = 1'b0;
  assign new_n30_ = a0 & b0;
  assign new_n32_ = ~a0 & ~b0;
  assign new_n34_ = ~new_n30_ & ~new_n32_;
  assign new_n36_ = \new_ADD2|c_  & new_n34_;
  assign new_n38_ = ~\new_ADD2|c_  & ~new_n34_;
  assign n26 = ~new_n36_ & ~new_n38_;
  assign \new_ADD2|0_  = new_n30_ | new_n36_;
  assign new_n42_ = a1 & b1;
  assign new_n44_ = ~a1 & ~b1;
  assign new_n46_ = ~new_n42_ & ~new_n44_;
  assign new_n48_ = \new_ADD2|0_  & new_n46_;
  assign new_n50_ = ~\new_ADD2|0_  & ~new_n46_;
  assign n23 = ~new_n48_ & ~new_n50_;
  assign n20 = new_n42_ | new_n48_;
  always @ (posedge clock) begin
    z2 <= n20;
    z1 <= n23;
    z0 <= n26;
  end
endmodule


