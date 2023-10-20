CREATE TABLE pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_viagens_clientes INT,
    data_pagamento DATE,
    valor_pago DECIMAL(10, 2),
    FOREIGN KEY (id_viagens_clientes) REFERENCES viagens_clientes(id)
);