`default_nettype none

module tt_um_alu_MariusL00 (
    input  wire [7:0] ui_in,    // Entrée A (8 bits)
    output wire [7:0] uo_out,   // Sortie Résultat (8 bits)
    input  wire [7:0] uio_in,   // Entrée B (8 bits)
    output wire [7:0] uio_out,  // Inutilisé
    output wire [7:0] uio_oe,   // Inutilisé
    input  wire       ena,      // Toujours à 1
    input  wire       clk,      // Horloge
    input  wire       rst_n     // Reset actif bas
);

    // Désactivation des broches bidirectionnelles
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // ALU simplifiée sur 8 bits pour tester le flux complet
    reg [7:0] result;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            result <= 8'b0;
        end else begin
            result <= ui_in + uio_in; // Addition de ui_in (A) et uio_in (B)
        end
    end

    assign uo_out = result;

    // Évite les warnings de compilation pour les signaux non utilisés
    wire _unused = &{ena, 1'b0};

endmodule 
