module wire_qudou (
	input clk,keyin,reset_n,
	output keyout
);

	reg [3:0] state;
	reg keynow;
	
	always @(posedge clk)
		if (!reset_n)
			state <= 4'd0;
		else if (keynow == keyin)//不变
			state <= 4'd0;
		else if (state<4'd4)//按键按下时间不足
			state <= state + 4'd1;
		else//按键按下了足够的时间，但是希望按键松开才能使state归位
			state <= state;
	
	always @(posedge clk)
		if (!reset_n)
			keynow <= 1'd0;
		else if (state==4'd4)
			keynow <= keyin;
		else
			keynow <= keynow;
	assign keyout = keynow;
endmodule
