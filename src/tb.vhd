library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_tt_um_alu_MariusL00 is
end entity tb_tt_um_alu_MariusL00 ;

architecture sim of tb_tt_um_alu_MariusL00  is

    -- Déclaration des signaux de test
    signal ui_in   : std_logic_vector(7 downto 0) := (others => '0');
    signal uio_in  : std_logic_vector(7 downto 0) := (others => '0');
    signal ena     : std_logic := '1';
    signal clk     : std_logic := '0';
    signal rst_n   : std_logic := '0';

    signal uo_out  : std_logic_vector(7 downto 0);
    signal uio_out : std_logic_vector(7 downto 0);
    signal uio_oe  : std_logic_vector(7 downto 0);

    -- Constante pour la période de l'horloge (10 ns -> 100 MHz)
    constant clk_period : time := 10 ns;

begin

    -- Instantiation du composant à tester (UUT)
    uut: entity work.tt_um_alu_MariusL00 
        port map (
            ui_in   => ui_in,
            uo_out  => uo_out,
            uio_in  => uio_in,
            uio_out => uio_out,
            uio_oe  => uio_oe,
            ena     => ena,
            clk     => clk,
            rst_n   => rst_n
        );

    -- Processus de génération de l'horloge
    clk_process : process
    begin
        clk <= '0';
        wait for clk_period / 2;
        clk <= '1';
        wait for clk_period / 2;
    end process;

    -- Processus de simulation et de stimulus
    stim_process : process
    begin
        -- Initialisation des signaux
        ui_in  <= (others => '0');
        uio_in <= (others => '0');
        rst_n  <= '0'; -- Application du reset actif bas

        -- Attente de 20 ns puis relâchement du reset
        wait for 20 ns;
        rst_n <= '1';
        wait for 10 ns;

        -- Test 1 : 5 + 3
        ui_in  <= std_logic_vector(to_unsigned(5, 8));
        uio_in <= std_logic_vector(to_unsigned(3, 8));
        wait for 10 ns;
        report "Temps = " & time'image(now) & " | A = 5, B = 3 -> Résultat = " & integer'image(to_integer(unsigned(uo_out))) & " (Attendu: 8)";

        -- Test 2 : 10 + 20
        ui_in  <= std_logic_vector(to_unsigned(10, 8));
        uio_in <= std_logic_vector(to_unsigned(20, 8));
        wait for 10 ns;
        report "Temps = " & time'image(now) & " | A = 10, B = 20 -> Résultat = " & integer'image(to_integer(unsigned(uo_out))) & " (Attendu: 30)";

        -- Test 3 : Test d'overflow (250 + 10 = 260 -> 4 en 8 bits)
        ui_in  <= std_logic_vector(to_unsigned(250, 8));
        uio_in <= std_logic_vector(to_unsigned(10, 8));
        wait for 10 ns;
        report "Temps = " & time'image(now) & " | A = 250, B = 10 -> Résultat = " & integer'image(to_integer(unsigned(uo_out))) & " (Attendu: 4)";

        -- Test 4 : Application du reset en cours de route
        rst_n  <= '0';
        ui_in  <= std_logic_vector(to_unsigned(100, 8));
        uio_in <= std_logic_vector(to_unsigned(50, 8));
        wait for 10 ns;
        report "Temps = " & time'image(now) & " (Reset actif) -> Résultat = " & integer'image(to_integer(unsigned(uo_out))) & " (Attendu: 0)";

        rst_n  <= '1';
        wait for 10 ns;
        report "Temps = " & time'image(now) & " (Fin reset) | A = 100, B = 50 -> Résultat = " & integer'image(to_integer(unsigned(uo_out))) & " (Attendu: 150)";

        -- Fin de la simulation
        wait for 20 ns;
        assert false report "Fin de simulation réussie" severity failure;
    end process;

end architecture sim;
