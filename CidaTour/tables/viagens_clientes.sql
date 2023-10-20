CREATE TABLE viagens_clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_viagem INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_viagem) REFERENCES viagens(id)
);