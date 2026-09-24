<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an 8-bit synchronous adder. On every rising edge of the clock signal (clk), the circuit adds two 8-bit operands:

Operand A received via the dedicated input pins (ui_in).

Operand B received via the bidirectional pins, which are configured as inputs here (uio_in).

The result of this addition is stored in an internal register and routed to the output pins (uo_out). The register can be asynchronously reset to zero by applying a low level to the reset pin (rst_n). The bidirectional output pins (uio_out and uio_oe) are unused and continuously driven to zero.

## How to test

To verify the circuit's correct operation, you can follow this sequence:

Apply a low level (0) to rst_n to reset the module, then pull it back high (1).

Provide a first 8-bit binary value to the ui_in pins (e.g., 00000101 for 5).

Provide a second 8-bit binary value to the uio_in pins (e.g., 00000011 for 3).

Generate a pulse (rising edge) on the clock signal clk.

Read the output on the uo_out pins. The displayed result should match the mathematical sum of the two inputs (in this case, 00001000 for 8).

## External hardware

No complex external hardware is required. For testing on a physical development board, the module only needs:

Two rows of 8 DIP switches or jumpers to drive the ui_in and uio_in inputs.

A row of 8 LEDs connected to uo_out to visualize the result of the addition.

A push button or signal generator to manually drive the clock (clk) and reset (rst_n) signals.
