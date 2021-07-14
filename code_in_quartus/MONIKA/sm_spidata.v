module sm_spidata (
	input clk, reset_n, nss, stsourcevalid,
	input [7:0] spibus,
	output reg [7:0] addr, data,
	output reg update,
	output [1:0] state
);

parameter IDLE = 2'b00;
parameter get_addr = 2'b01;
parameter get_data = 2'b10;
parameter complete = 2'b11;
 
//内部信号声明
reg [1:0] current_state;
reg [1:0] next_state;

always @ (posedge clk or negedge reset_n) begin
    if(!reset_n)
        current_state <= IDLE;
    else
        current_state <= next_state;
end

reg nss_buf, stsourcevalid_buf;
always @(posedge clk)
	nss_buf <= nss;
always @(posedge clk)
	stsourcevalid_buf <= stsourcevalid;

always @ (nss or stsourcevalid or current_state) begin
	case(current_state)
		IDLE:		begin
							if(nss_buf==1'b1 && nss==1'b0) next_state = get_addr;
							else   next_state = IDLE;
						end
		get_addr:  	begin
							if (nss==1'b1) next_state = IDLE;
							else if(stsourcevalid_buf==1'b1 && stsourcevalid==1'b0) next_state = get_data;
							else    next_state = get_addr;
						end
		get_data:  	begin
							if (nss==1'b1) next_state = IDLE;
							else if(stsourcevalid_buf==1'b1 && stsourcevalid==1'b0) next_state = complete;
							else    next_state = get_data;
						end
		complete:  	begin
							if (nss==1'b1) next_state = IDLE;
							else next_state = complete;
						end
        default : next_state = 2'bxx;
   endcase
end
assign state = current_state;

reg [1:0] state_buf;
always @(posedge clk)
	state_buf <= current_state;

always @(posedge clk or negedge reset_n)
	if (!reset_n)
		addr <= 8'd0;
	else if (state_buf==get_addr && current_state==get_data)
		addr <= spibus;
	else
		addr <= addr;

always @(posedge clk or negedge reset_n)
	if (!reset_n)
		data <= 8'd0;
	else if (state_buf==get_data && current_state==complete)
		data <= spibus;
	else
		data <= data;

always @(posedge clk or negedge reset_n)
	if (!reset_n)
		update <= 1'd0;
	else if (state_buf==complete && current_state==IDLE)
		update <= 1'b1;
	else
		update <= 1'b0;

endmodule

