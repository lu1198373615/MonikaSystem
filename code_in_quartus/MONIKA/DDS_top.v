module DDS_top (
	input clk,reset_n,
	input [31:0] inc_phi, //频率
	input [3:0] occupation, waveform, //占空比和波形类型
	output [11:0] dds_data,
	output dds_clk,
	output zhankb
);
	
	wire [35:0] coe_inc;
	assign coe_inc = inc_phi * occupation + {4'd0,inc_phi};
	reg [35:0] n_cnt;
	always @(posedge clk or negedge reset_n)
		if(!reset_n)
			n_cnt <= 36'd0;
		else
			n_cnt <= n_cnt + coe_inc;
	
	assign zhankb = n_cnt[35:32]<=occupation ? 1'd1 : 1'd0;

	reg [31:0] phase;
	always @(posedge clk or negedge reset_n)
		if(!reset_n)
			phase <= 32'd0;
		else if (zhankb==1'd0)
			phase <= 32'd0;
		else
			phase <= phase + inc_phi;
	
	wire [11:0] data_sin,data_juchi_up,data_juchi_dn,data_sanjiao;
	rom_sin r1 (
		.address(phase[31:20]),
		.clock(clk),
		.q(data_sin)
	);
	rom_juchi_up r2 (
		.address(phase[31:20]),
		.clock(clk),
		.q(data_juchi_up)
	);
	rom_juchi_dn r3 (
		.address(phase[31:20]),
		.clock(clk),
		.q(data_juchi_dn)
	);
	rom_sanjiao r4 (
		.address(phase[31:20]),
		.clock(clk),
		.q(data_sanjiao)
	);
	
	reg [11:0] data_rom;
	always @(posedge clk)
		case (waveform)
			4'd0 : data_rom <= data_sin;
			4'd1 : data_rom <= data_sanjiao;
			4'd2 : data_rom <= data_juchi_up;
			4'd3 : data_rom <= data_juchi_dn;
			default : data_rom = data_sin;
		endcase
	
	assign dds_data = zhankb ? {~data_rom[11],data_rom[10:0]} : 12'd0;
	assign dds_clk = clk;
endmodule
