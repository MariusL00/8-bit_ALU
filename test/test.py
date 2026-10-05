# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Démarrage de la simulation")

    # Génération de l'horloge (période de 10 us -> 100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # 1. Initialisation stricte
    dut._log.info("Phase de Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # 2. Cas de test 1 : 5 + 10 = 15
    dut._log.info("Test 1: Addition simple (5 + 10 = 15)")
    dut.ui_in.value = 5
    dut.uio_in.value = 10
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 15

    # 3. Cas de test 2 : 100 + 50 = 150
    dut._log.info("Test 2: Addition (100 + 50 = 150)")
    dut.ui_in.value = 100
    dut.uio_in.value = 50
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 150

    # 4. Cas de test 3 : Test de l'overflow (200 + 100 = 44)
    dut._log.info("Test 3: Débordement (200 + 100 = 44)")
    dut.ui_in.value = 200
    dut.uio_in.value = 100
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 44

    # 5. Cas de test 4 : 255 + 1 = 0
    dut._log.info("Test 4: Bouclage 8 bits (255 + 1 = 0)")
    dut.ui_in.value = 255
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0

    # 6. Test du Reset asynchrone
    dut._log.info("Test 5: Reset asynchrone en cours d'opération")
    dut.ui_in.value = 50
    dut.uio_in.value = 50
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 100

    dut.rst_n.value = 0
    await Timer(2, units="us") 
    assert dut.uo_out.value == 0

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 100

    dut._log.info("Simulation terminée avec succès !")
