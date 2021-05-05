module ADD2 ( clock,
	  a0, a1, b0, b1, 
	  s0, s1, s2);
	input clock; 
	input a0, a1, b0, b1;
	output s0, s1, s2;
	reg __ADD2_s_a0, __ADD2_s_a1, __ADD2_s_b0, __ADD2_s_b1;
	wire new_n8_, new_n9_, new_n11_, new_n12_, new_n13_, new_n14_, new_n15_;
	wire new_w0, new_w1, new_w2, new_w3;
	assign new_n8_ = __ADD2_s_a0 & __ADD2_s_b0;
	assign new_n9_ = ~__ADD2_s_a0 & ~__ADD2_s_b0;
	assign s0 = ~new_n8_ & ~new_n9_;
	assign new_n11_ = __ADD2_s_a1 & __ADD2_s_b1;
	assign new_n12_ = ~__ADD2_s_a1 & ~__ADD2_s_b1;
	assign new_n13_ = ~new_n11_ & ~new_n12_;
	assign new_n14_ = new_n8_ & new_n13_;
	assign new_n15_ = ~new_n8_ & ~new_n13_;
	assign s1 = ~new_n14_ & ~new_n15_;
	assign s2 = new_n11_ | new_n14_;
	assign new_w0 = a0;
	assign new_w1 = a1;
	assign new_w2 = b0;
	assign new_w3 = b1;
	always @ (posedge clock) begin
		__ADD2_s_a0 <= new_w0;
		__ADD2_s_a1 <= new_w1;
		__ADD2_s_b0 <= new_w2;
		__ADD2_s_b1 <= new_w3;
	end
endmodule
