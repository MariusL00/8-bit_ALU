library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tt_um_alu_MariusL00  is
    port (
        ui_in   : in  std_logic_vector(7 downto 0); -- Entrée A (8 bits)
        uo_out  : out std_logic_vector(7 downto 0); -- Sortie Résultat (8 bits)
        uio_in  : in  std_logic_vector(7 downto 0); -- Entrée B (8 bits)
        uio_out : out std_logic_vector(7 downto 0); -- Inutilisé
        uio_oe  : out std_logic_vector(7 downto 0); -- Inutilisé
        ena     : in  std_logic;                    -- Toujours à 1
        clk     : in  std_logic;                    -- Horloge
        rst_n   : in  std_logic                     -- Reset actif bas
    );
end entity tt_um_alu_MariusL00 ;

architecture rtl of tt_um_alu_MariusL00  is

    signal result : unsigned(7 downto 0);
    signal unused : std_logic;

begin

    -- Désactivation des broches bidirectionnelles
    uio_out <= (others => '0');
    uio_oe  <= (others => '0');

    -- ALU simplifiée sur 8 bits (addition synchrone)
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            result <= (others => '0');
        elsif rising_edge(clk) then
            -- Addition de ui_in (A) et uio_in (B) convertis en unsigned
            result <= unsigned(ui_in) + unsigned(uio_in);
        end if;
    end process;

    uo_out <= std_logic_vector(result);

    -- Évite les warnings de compilation pour le signal ena non utilisé
    unused <= ena;

end architecture rtl;
