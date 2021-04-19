// Benchmark "ADD2" written by ABC on Tue Apr 13 09:44:44 2021

module ADD2 ( 
    a0, a1, b0, b1,
    s0, s1, s2  );
  input  a0, a1, b0, b1;
  output s0, s1, s2;
  wire new_n8_, new_n9_, new_n11_, new_n12_, new_n13_, new_n14_, new_n15_;
  assign new_n8_ = a0 & b0;
  assign new_n9_ = ~a0 & ~b0;
  assign s0 = ~new_n8_ & ~new_n9_;
  assign new_n11_ = a1 & b1;
  assign new_n12_ = ~a1 & ~b1;
  assign new_n13_ = ~new_n11_ & ~new_n12_;
  assign new_n14_ = new_n8_ & new_n13_;
  assign new_n15_ = ~new_n8_ & ~new_n13_;
  assign s1 = ~new_n14_ & ~new_n15_;
  assign s2 = new_n11_ | new_n14_;
endmodule


