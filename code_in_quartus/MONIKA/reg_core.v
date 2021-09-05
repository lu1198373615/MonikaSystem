module reg_core (
	input clk,reset_n,update,
	input [7:0] addr,data,
	output [31:0] inc_phi,
	output [3:0] occupation,waveform,bit_gain //占空比和波形类型和AD8369增益
);

	reg update_buf;
	always @(posedge clk)
		update_buf <= update;
		
	reg [7:0] register0,register1,register2,register3,register4,register5;
	always @(posedge clk or negedge reset_n)
		if (!reset_n) begin
			register0 <= 8'd242;
			register1 <= 8'd0;
			register2 <= 8'd0;
			register3 <= 8'd82;
			register4 <= 8'd0;
			register5 <= 8'd0;
			end
		else if (update_buf==1'd0 && update==1'd1)
			case (addr)
				8'd0 : register0 <= data;
				8'd1 : register1 <= data;
				8'd2 : register2 <= data;
				8'd3 : register3 <= data;
				8'd4 : register4 <= data;
				8'd5 : register5 <= data;
			endcase
	
	assign inc_phi = {register4, register3, register2, register1};
	assign occupation = register0[7:4];
	assign waveform = register0[3:0];
	assign bit_gain = register5[3:0];
endmodule
		