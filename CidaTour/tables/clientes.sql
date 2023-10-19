CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    rg VARCHAR(14) NOT NULL UNIQUE,  -- Adicionado UNIQUE para o campo RG
    cpf VARCHAR(14) NOT NULL UNIQUE,  -- Adicionado UNIQUE para o campo CPF
    data_nascimento DATE,
    telefone VARCHAR(15),
    status_cliente BOOLEAN default True,
    data_cadastro DATETIME DEFAULT NOW()
);


