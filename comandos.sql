CREATE DATABASE IF NOT EXISTS sustentabilidade;
USE sustentabilidade;

SELECT * FROM cadastro;
SELECT * FROM sustentabilidade;

DROP TABLE IF EXISTS cadastro;
DROP TABLE IF EXISTS sustentabilidade;

INSERT INTO sustentabilidade (nome, data,  media_agua, media_energia, media_residuos, transporte) VALUES (João, 2025-06-09, 100, 10, 70, ALTA);
UPDATE cadastro SET nome = 'Joelma' WHERE id = 1;