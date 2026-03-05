module tt_um_mult_top(
	input wire [7:0] ui_in,
	output wire [7:0] uo_out,
	input wire [7:0] uio_in,
	output wire [7:0] uio_out,
	output wire [7:0] uio_oe,
	input wire ena,
	input wire clk,
	input wire rst_n

);
//state what inuts are not used
wire _unused = &{uio_in};


//A, B, P
reg [3:0] A, B;
wire [7:0] P;

//add multiplier
mult MULT (.A(A), .B(B), .P(P));

//assign outputs
assign uo_out = P;
assign uio_out = {8{1'b0}};
assign uio_oe = {8{1'b0}};

//cascade inputs
reg [7:0] ui_in_1;
reg ena_1, rst_n_1, rst_n_2;
always @(posedge clk)begin
	ui_in_1 <= ui_in;
	ena_1 <= ena;
	rst_n_1 <= rst_n;
	rst_n_2 <= rst_n_1;
end

//assign inputs
always @(*) begin
	if(!rst_n_2) begin
		A = {4{1'b0}};
		B = {4{1'b0}};
	end
	else begin
		if(ena_1)begin
			A = ui_in_1[7:4];
			B = ui_in_1[3:0];
		end
		else begin
			A = {4{1'b0}};
			B = {4{1'b0}};
		end
		
	end
	
end


endmodule
