module pingpang_fifo (
	input clk, reset_n,
	input [11:0] data_in,
	input w_cs_n_input, w_dclk_input,
	output [11:0] w_miso
);
	
	//树莓派GPIO过来的信号是异步信号，需要向本时钟域同步
	//其实这里两级寄存器打拍就可以了，但打四拍没意见吧
	reg w_cs_n_buf_one, w_cs_n_buf_two, w_cs_n_buf_three, w_cs_n;
	always @(posedge clk) begin
		w_cs_n_buf_one <= w_cs_n_input;
		w_cs_n_buf_two <= w_cs_n_buf_one;
		w_cs_n_buf_three <= w_cs_n_buf_two;
		w_cs_n <= w_cs_n_buf_three;
	end
	reg w_dclk_buf_one, w_dclk_buf_two, w_dclk_buf_three, w_dclk;
	always @(posedge clk) begin
		w_dclk_buf_one <= w_dclk_input;
		w_dclk_buf_two <= w_dclk_buf_one;
		w_dclk_buf_three <= w_dclk_buf_two;
		w_dclk <= w_dclk_buf_three;
	end

	//内部信号声明
	parameter PING_CLEAR = 2'b00;
	parameter PANG_READ  = 2'b01;
	parameter PANG_CLEAR = 2'b10;
	parameter PING_READ  = 2'b11;
	reg [1:0] current_state;
	reg [1:0] next_state;
	
	//描述状态转移
	always @ (posedge clk or negedge reset_n) begin
		if(!reset_n)
			current_state <= PING_CLEAR;
		else
			current_state <= next_state;
	end

	//组合逻辑判断状态转移条件
	always @ (*)
		case(current_state)
			PING_CLEAR:	next_state = ~w_cs_n ? PANG_READ : PING_CLEAR;
			PANG_READ:  next_state =  w_cs_n ? PANG_CLEAR : PANG_READ;
			PANG_CLEAR: next_state = ~w_cs_n ? PING_READ : PANG_CLEAR;
			PING_READ:  next_state =  w_cs_n ? PING_CLEAR : PING_READ;
		endcase
	
	//同步时序描述状态输出
	reg sclr_ping, sclr_pang, rd_ping, rd_pang, wr_ping, wr_pang;
	always @(posedge clk or negedge reset_n)
		if (!reset_n)
			begin
								sclr_ping <= 1'd1;		sclr_pang <= 1'd1;//双清
								rd_ping <= 1'd0;		rd_pang <= 1'd0;
								wr_ping <= 1'd0;		wr_pang <= 1'd0;
			end
		else
			case(current_state)
				PING_CLEAR:	begin
								sclr_ping <= 1'd1;		sclr_pang <= 1'd0;//清ping
								rd_ping <= 1'd0;		rd_pang <= 1'd0;//写pang
								wr_ping <= 1'd0;		wr_pang <= 1'd1;
								end
				PANG_READ:  begin
								sclr_ping <= 1'd0;		sclr_pang <= 1'd0;//不清
								rd_ping <= 1'd0;		rd_pang <= 1'd1;//读pang写ping
								wr_ping <= 1'd1;		wr_pang <= 1'd0;
								end
				PANG_CLEAR: begin
								sclr_ping <= 1'd0;		sclr_pang <= 1'd1;//清pang写ping
								rd_ping <= 1'd0;		rd_pang <= 1'd0;//写ping
								wr_ping <= 1'd1;		wr_pang <= 1'd0;
								end
				PING_READ:  begin
								sclr_ping <= 1'd0;		sclr_pang <= 1'd0;//不清
								rd_ping <= 1'd1;		rd_pang <= 1'd0;//读ping写pang
								wr_ping <= 1'd0;		wr_pang <= 1'd1;
								end
			endcase

	wire [11:0] data_ping, data_pang;
	my_fifo ping (
		.aclr(sclr_ping),
		.data(data_in),
		.rdclk(w_dclk),
		.rdreq(rd_ping),
		.wrclk(clk),
		.wrreq(wr_ping),
		.q(data_ping)
	);
	my_fifo pang (
		.aclr(sclr_pang),
		.data(data_in),
		.rdclk(w_dclk),
		.rdreq(rd_pang),
		.wrclk(clk),
		.wrreq(wr_pang),
		.q(data_pang)
	);
	reg [11:0] data_pingpang;
	always @(posedge clk)
		if (current_state==PING_READ)
			data_pingpang <= data_ping;
		else if (current_state==PANG_READ)
			data_pingpang <= data_pang;
		else
			data_pingpang <= 12'd0;
	assign w_miso = data_pingpang;
endmodule
