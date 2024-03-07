# Introdução

Projeto de 4° período da disciplina Software Product: Analysis & Specification

# Integrantes:

- Ewerton Ferreira Costa  
- João Victor Machado Maniezzo  
- Pedro Luis da Paz dos Santos  

# banco
CREATE TABLE testebancoentrada (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    placa VARCHAR(20),  
    modelo VARCHAR(50),  
    horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);
