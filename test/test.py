# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # 1. Initialisation stricte de TOUTES les entrées pour le Gate-Level
    dut._log.info("Reset")
    dut.ena.value = 1 
    dut.ui_in.value = 0 
    dut.uio_in.value = 0 
    dut.rst_n.value = 0 

    # 2. Attente de quelques cycles d'horloge pour propager le reset
    await ClockCycles(dut.clk, 5)

    # 3. Désactivation du reset
    dut.rst_n.value = 1 
    await ClockCycles(dut.clk, 2)

    dut._log.info("Test project behavior")

    # 4. Application des nouvelles entrées (ex: 20 + 30 = 50)
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Attente d'un cycle d'horloge pour laisser l'ALU calculer
    await ClockCycles(dut.clk, 2)

    # Vérification de la sortie
    assert dut.uo_out.value == 50

    # Ajoutez vos autres cas de tests ici en suivant le même schéma :
    # dut.ui_in.value = ...
    # dut.uio_in.value = ...
    # await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == ...
