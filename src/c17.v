// Benchmark "c17" written by ABC on Tue Apr 13 09:56:24 2021

module c17 ( 
    \1 , 2, 3, 6, 7,
    22, 23  );
  input  \1 , 2, 3, 6, 7;
  output 22, 23;
  wire new_n8_, new_n9_, new_n10_, new_n12_;
  assign new_n8_ = \1  & 3;
  assign new_n9_ = 3 & 6;
  assign new_n10_ = 2 & ~new_n9_;
  assign 22 = new_n8_ | new_n10_;
  assign new_n12_ = 7 & ~new_n9_;
  assign 23 = new_n10_ | new_n12_;
endmodule


