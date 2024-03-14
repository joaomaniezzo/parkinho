# Introdução

Projeto de 4° período da disciplina Software Product: Analysis & Specification

# Integrantes:

- Ewerton Ferreira Costa  
- João Victor Machado Maniezzo  
- Pedro Luis da Paz dos Santos  

# banco
CREATE schema parkinho

USE parkinho

CREATE TABLE historico (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    data DATE NOT NULL,  
    placa VARCHAR(20) NOT NULL,  
    modelo VARCHAR(50) NOT NULL,  
    horario_entrada TIME NOT NULL,  
    horario_saida TIME  
);  

CREATE TABLE mensalistas (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    placa VARCHAR(8) NOT NULL,  
    nome VARCHAR(255) NOT NULL  
);
