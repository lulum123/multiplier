# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    
    
    # Reset
    dut._log.info("Reset")
    #create output variable
    output = cocotb.types.LogicArray.from_unsigned(0x00, 8)
    #Turn on the module
    dut.ena.value = 1
    #Set inputs to module
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    #Reset the module
    dut.rst_n.value = 0
    #wait 10 clk cycles then continue
    await ClockCycles(dut.clk, 10)
    #Turn off reset
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")
    correct = 0
    # Set the input values you want to test
    for i in range(0,1000):
        A = cocotb.types.LogicArray.from_unsigned(0x00, 8)
        B = cocotb.types.LogicArray.from_unsigned(0x00, 8)

        #randomly create 2 logic arrays of 4 bits to concatenate together
        for j in range(0,4):
            A = cocotb.types.LogicArray.from_unsigned((random.random()>0.5)<<(j+4),8) | A;
            B = cocotb.types.LogicArray.from_unsigned((random.random()>0.5)<<j,8) | B;
        u_in = A | B;
        #cast logic arrays to ints and multiply them
        A_int = int(A) >> 4
        B_int = int(B)
        P_int = A_int * B_int
        P = cocotb.types.LogicArray.from_unsigned(0x00, 8)
        P.value = P_int

        #send in new value to the array
        dut.ui_in.value = u_in
        #wait for 3 clk cycles
        await ClockCycles(dut.clk, 3)
        #record the output
        output.value = dut.uo_out.value
        correct = (P.value == output.value) + correct
        #test if output matches expected value
        assert (P.value == output.value)
        
    #print out final statement
    fin_out_str = f"{correct} out of 1000 tests have succeeded"
    dut._log.info(fin_out_str)
