# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import numpy as np

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

   
    #dut.seq_seen.value= output

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await RisingEdge(dut.clk) 
    await Timer(2, units='ns')

    #dut.reset.value = 0
    #await RisingEdge(dut.clk)
    #await Timer(20, units='ns')

    input_seq=[0,0,0,0];
    for i in range(300):

        input=random.randint(0,1)
        dut.inp_bit.value= input
        input_seq.append(input)

        await Timer(12, units='ns')
        #print(input)
        #print(input_seq)
        #print(input_seq[i+1:i+5])
        #print(f'input is {input_seq[i+1:i+5]} and output is {dut.seq_seen.value}')
        dut._log.info(f'input is {input_seq[i+1:i+5]} and output is {dut.seq_seen.value}')
        #assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
 





    
