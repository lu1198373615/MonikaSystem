module led (
	input clk,
	output LED1,LED2
);

	reg [31:0] cnt;
	reg flag;
	always @(posedge clk)
		if (cnt>32'd100000000) begin
			cnt <= 32'd0;
			flag <= ~flag;
			end
		else
			cnt <= cnt + 1'd1;
	
	assign LED1 =  flag;
	assign LED2 = ~flag;

endmodule
