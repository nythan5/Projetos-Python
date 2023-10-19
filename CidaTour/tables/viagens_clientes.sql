CREATE TABLE viagens_clientes (
    id SERIAL PRIMARY KEY,
    cliente_id INT,
    viagem_id INT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (viagem_id) REFERENCES viagens(id)
);