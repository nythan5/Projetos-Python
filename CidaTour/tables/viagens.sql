CREATE TABLE viagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL UNIQUE,
    descricao VARCHAR(255),
    data_check_in date NOT NULL ,  -- Adicionado UNIQUE para o campo RG
    data_check_out date NOT NULL ,  -- Adicionado UNIQUE para o campo CPF
    custo  FLOAT,
    status_viagem BOOLEAN default True,
    data_cadastro DATETIME DEFAULT NOW()
);