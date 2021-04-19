// Benchmark "ADD2" written by ABC on Tue Apr 13 09:46:54 2021

module ADD2 ( clock, 
    a0, a1, b0, b1,
    z0, z1, z2  );
  input  clock;
  input  a0, a1, b0, b1;
  output z0, z1, z2;
  reg \ADD2|s_a0 , \ADD2|s_a1 , \ADD2|s_b0 , \ADD2|s_b1 ;
  wire \new_ADD2|c_ , new_n34_, new_n36_, new_n38_, new_n40_, new_n42_,
    \new_ADD2|0_ , new_n46_, new_n48_, new_n50_, new_n52_, new_n54_, n21,
    n24, n27, n30;
  assign \new_ADD2|c_  = 1'b0;
  assign new_n34_ = \ADD2|s_a0  & \ADD2|s_b0 ;
  assign new_n36_ = ~\ADD2|s_a0  & ~\ADD2|s_b0 ;
  assign new_n38_ = ~new_n34_ & ~new_n36_;
  assign new_n40_ = \new_ADD2|c_  & new_n38_;
  assign new_n42_ = ~\new_ADD2|c_  & ~new_n38_;
  assign z0 = ~new_n40_ & ~new_n42_;
  assign \new_ADD2|0_  = new_n34_ | new_n40_;
  assign new_n46_ = \ADD2|s_a1  & \ADD2|s_b1 ;
  assign new_n48_ = ~\ADD2|s_a1  & ~\ADD2|s_b1 ;
  assign new_n50_ = ~new_n46_ & ~new_n48_;
  assign new_n52_ = \new_ADD2|0_  & new_n50_;
  assign new_n54_ = ~\new_ADD2|0_  & ~new_n50_;
  assign z1 = ~new_n52_ & ~new_n54_;
  assign z2 = new_n46_ | new_n52_;
  assign n21 = a0;
  assign n24 = a1;
  assign n27 = b0;
  assign n30 = b1;
  always @ (posedge clock) begin
    \ADD2|s_a0  <= n21;
    \ADD2|s_a1  <= n24;
    \ADD2|s_b0  <= n27;
    \ADD2|s_b1  <= n30;
  end
endmodule


