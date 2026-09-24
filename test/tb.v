`timescale 1ns / 1ps
`default_nettype none

module tb_tt_um_alu_MariusL00;

    // Déclaration des signaux
    reg  [7:0] ui_in;
    reg  [7:0] uio_in;
    reg        ena;
    reg        clk;
    reg        rst_n;

    wire [7:0] uo_out;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;

    // Instanciation du module à tester (DUT : Device Under Test)
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

    // Génération de l'horloge (Période = 10ns -> 100 MHz)
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    // Bloc de stimulus
    initial begin
        // Création du fichier pour visualiser les ondes (GTKWave)
        $dumpfile("tb_tt_um_alu_MariusL00.vcd");
        $dumpvars(0, tb_tt_um_alu_Marius_L00);

        // 1. Initialisation des signaux
        ui_in  = 8'b0;
        uio_in = 8'b0;
        ena    = 1'b1;
        rst_n  = 1'b0; // Reset actif

        // 2. Attente de quelques cycles puis désactivation du reset
        #20;
        rst_n  = 1'b1;
        #10;

        // 3. Cas de test 1 : 5 + 10 = 15
        ui_in  = 8'd5;
        uio_in = 8'd10;
        #10; // On attend un cycle d'horloge pour que le résultat soit enregistré

        // 4. Cas de test 2 : 100 + 50 = 150
        ui_in  = 8'd100;
        uio_in = 8'd50;
        #10;

        // 5. Cas de test 3 : Test de l'overflow (200 + 100 = 300 -> 44 sur 8 bits)
        ui_in  = 8'd200;
        uio_in = 8'd100;
        #10;

        // 6. Cas de test 4 : 255 + 1 = 0 (Bouclage complet)
        ui_in  = 8'd255;
        uio_in = 8'd1;
        #10;

        // 7. Test du Reset asynchrone pendant une opération
        ui_in  = 8'd50;
        uio_in = 8'd50;
        #2;        // On attend un peu, mais pas un cycle complet
        rst_n = 0; // On déclenche le reset
        #8;
        rst_n = 1;

        // Fin de la simulation
        #20;
        $display("Simulation terminée avec succès !");
        $finish;
    end

    // Affichage des résultats dans la console
    initial begin
        $monitor("Temps = %0t | rst_n = %b | ui_in (A) = %3d | uio_in (B) = %3d | uo_out (Res) = %3d", 
                 $time, rst_n, ui_in, uio_in, uo_out);
    end

endmodule
