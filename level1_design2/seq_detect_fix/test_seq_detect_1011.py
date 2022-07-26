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

    dut.reset.value = 0
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')

    input_seq=[0,0,0,0,0]
    f=0
    n=1000
    valid_case=0
    for i in range(n):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.inp_bit.value= input
        input_seq.append(input)
        await Timer(10, units='ns')
        
        if(input_seq[i+1:i+5]==[1 , 0, 1, 1]):
            valid_case=valid_case+1
            if(dut.seq_seen.value==1):
                result='-----------PASSED------------'
            else:
                result='-----------FAILED------------'
                f=f+1

        else:
            if(dut.seq_seen.value==1):
                result='------FAILED EXPLICITLY------'
                f=f+1
            else:
                #Implicitly PASSED Case
                result='-----------------------------'

        dut._log.info(f'Next_Input_bit={input}  last 4bits seq={input_seq[i+1:i+5]}  output={dut.seq_seen.value}, result={result}')
        #assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
    print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Valid Cases={valid_case} Failed Cases={f}, Passed Cases={valid_case-f}  *')
    print(f'***************************************************************************')

    assert f==0, 'The design fails for Some inputs'