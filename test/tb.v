`timescale 1ns / 1ps
`default_nettype none

module tb;

    // Déclaration des signaux (qui seront désormais pilotés exclusivement par Python/Cocotb)
    reg  [7:0] ui_in;
    reg  [7:0] uio_in;
    reg        ena;
    reg        clk;
    reg        rst_n;

    wire [7:0] uo_out;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;

    // Instanciation du module à tester (DUT)[cite: 9]
    tt_um_alu_MariusL00 uut (
        .ui_in   (ui_in),
        .uo_out  (uo_out),
        .uio_in  (uio_in),
        .uio_out (uio_out),
        .uio_oe  (uio_oe),
        .ena     (ena),
        .clk     (clk),
        .rst_n   (rst_n)
    );

    // Création du fichier pour visualiser les ondes sous GTKWave[cite: 10]
    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb);
    end

endmodule
