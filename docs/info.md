<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
This project implements a simple 4-bit by 4-bit combinational multiplier using Verilog.

The design takes two 4-bit unsigned operands, A and B, from the Tiny Tapeout input pins and computes their product. The resulting multiplication output is an 8-bit value P = A × B, which is sent to the output pins.

The multiplier logic is implemented in the module `mult.v`. This module performs the multiplication operation between the two 4-bit operands. Since the design is purely combinational, the output product is updated immediately whenever the input values change.

The top-level module `tt_um_mult_top.v` connects the multiplier module to the standard Tiny Tapeout interface signals. It maps the external input pins (`ui_in`) to the internal signals used by the multiplier and routes the computed product to the output pins (`uo_out`).

Pin mapping is defined as follows:

Inputs:
- ui[7] → A[3]
- ui[6] → A[2]
- ui[5] → A[1]
- ui[4] → A[0]
- ui[3] → B[3]
- ui[2] → B[2]
- ui[1] → B[1]
- ui[0] → B[0]

Outputs:
- uo[7:0] → P[7:0] (product of A × B)

This design does not use the bidirectional IO pins (`uio`) or any additional peripherals. The circuit simply performs binary multiplication and outputs the result directly.

## How to test


The functionality of this design can be tested by providing two 4-bit input values and observing the multiplication result at the output pins.

Testing procedure:

1. Apply a 4-bit value for operand A to input pins ui[7:4].
2. Apply a 4-bit value for operand B to input pins ui[3:0].
3. The multiplier computes the product P = A × B.
4. The 8-bit result appears on output pins uo[7:0].

For example:

A = 3 (binary 0011)  
B = 5 (binary 0101)

Inputs applied to the chip:

ui_in = 0011 0101

Expected output:

P = 15 (binary 00001111)

The design has been verified using the provided testbench `mult_tb.v`. The testbench automatically applies multiple combinations of A and B values and compares the multiplier output with the expected multiplication result. If all tests pass, the multiplier is considered functionally correct.

## External hardware

No external hardware is required for this project.

The multiplier operates entirely within the Tiny Tapeout chip and only uses the standard input and output pins provided by the Tiny Tapeout interface.

All required signals are supplied through the digital input pins (`ui_in`), and the multiplication result is observed on the digital output pins (`uo_out`). The bidirectional pins (`uio`) are not used in this design.

Therefore, the project can be tested entirely in simulation or on the Tiny Tapeout platform without connecting any additional external devices such as LEDs, displays, or PMOD modules.
