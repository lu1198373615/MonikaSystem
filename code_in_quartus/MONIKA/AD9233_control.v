module AD9233_control (
	input clk,
	input [11:0] AD9233,
	input [3:0] BIT_IN,
	output reg [11:0] AD9233_REG,
	output clk_p, clk_n,
	output [3:0] BIT_GAIN,
	output reg DENB
);
	
	always @(posedge clk)
		AD9233_REG <= {~AD9233[11],AD9233[10:0]};
	assign clk_p =  clk;
	assign clk_n = ~clk;
	
	assign BIT_GAIN = BIT_IN;
	
	reg [3:0] bit_buf1,bit_buf2;
	always @(posedge clk) begin
		bit_buf1 <= BIT_IN;
		bit_buf2 <= bit_buf1;
	end
	always @(posedge clk)
		if (bit_buf2!=BIT_IN)
			DENB <= 1'd1;
		else
			DENB <= 1'd0;
	

endmodule
	
	