module key_qudou (
	input clk_100M, key_in,
	output reg key_out
);

	reg [19:0] cnt;
	always @(posedge clk_100M)
		cnt <= cnt + 1'd1;
	wire clk_200Hz;
	assign clk_200Hz = cnt[18];				//100M分频为200Hz
	
	reg [7:0] state;
	always @(posedge clk_200Hz)
		if (key_in==1'd1)							//按键没有被按下
			state <= 8'd0;
		else if (state<8'd8)						//按键按下时间不足
			state <= state + 1'd1;
		else											//按键按下了足够的时间，但是希望按键松开才能使state归位
			state <= state;

	always @(posedge clk_100M)
		if (state==8'd8)
			key_out <= 1'd0;						//认为按键被按下了
		else
			key_out <= 1'd1;

endmodule
