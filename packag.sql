CREATE OR REPLACE PACKAGE RM93613_PKG_PETS AS

  PROCEDURE CP1_CADASTRO_PET(p_tipoPet VARCHAR, p_nomePet VARCHAR, p_idade NUMBER);
  FUNCTION CP1_GET_PET(p_id NUMBER) RETURN VARCHAR2;
  PROCEDURE CP1_ALTERA_PET(p_id NUMBER, p_tipoPet VARCHAR, p_nomePet VARCHAR, p_idade NUMBER);
  PROCEDURE CP1_EXCLUI_PET(p_id NUMBER);
  PROCEDURE CP1_EXCLUI_TODOS;
  
END RM93613_PKG_PETS;

CREATE OR REPLACE PACKAGE BODY RM93613_PKG_PETS AS

    -- Uma Procedure para Cadastrar um Pet

    PROCEDURE CP1_CADASTRO_PET (
        p_tipoPet IN VARCHAR,
        p_nomePet IN VARCHAR,
        p_idade IN NUMBER
    ) IS
    BEGIN
    
        INSERT INTO PETSHOP (TIPO_PET, NOME_PET, IDADE)
        VALUES (p_tipoPet, p_nomePet, p_idade);
        
        commit;
    
    END CP1_CADASTRO_PET;


    -- Uma Função para recuperar dados de um Pet com base no parâmetro ID.
    
    FUNCTION CP1_GET_PET(p_id NUMBER)
    RETURN VARCHAR2
    IS
        dados_pet VARCHAR2(4000);
    BEGIN
        
        SELECT 
            'ID: ' || ID || CHR(10) ||
            'Nome: ' || NOME_PET || CHR(10) ||
            'Tipo: ' || TIPO_PET || CHR(10) ||
            'Idade: ' || IDADE
        INTO dados_pet
        FROM PETSHOP
        WHERE ID = p_id;
    
        
        IF dados_pet IS NOT NULL THEN
            RETURN dados_pet;
        ELSE
            RETURN 'Pet nÃ£o encontrado para o ID ' || p_id;
        END IF;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 'Pet nÃ£o encontrado para o ID ' || p_id;
    END CP1_GET_PET;


    -- Uma Procedure para alterar dados de um Pet com base no parâmetro ID
    
    PROCEDURE CP1_ALTERA_PET (
        p_id IN NUMBER,
        p_tipoPet IN VARCHAR,
        p_nomePet IN VARCHAR,
        p_idade IN NUMBER
    )
    IS
    BEGIN
    
        UPDATE PETSHOP
        SET TIPO_PET = p_tipoPet,
        NOME_PET = p_nomePet,
        IDADE = p_idade
        WHERE ID = p_id;
        
        commit;
    
    END CP1_ALTERA_PET;


    -- Uma Procedure para excluir um Pet com base no parâmetro ID
    
    PROCEDURE CP1_EXCLUI_PET (
        p_id IN NUMBER
    )
    IS
    BEGIN
    
        DELETE PETSHOP
        WHERE ID = p_id;
        
        commit;
    
    END CP1_EXCLUI_PET;
    

    -- Uma Procedure para excluir todos as linhas da Tabela
    
    PROCEDURE CP1_EXCLUI_TODOS
    IS
    BEGIN
    
        DELETE FROM PETSHOP;
        
        commit;
    
    END CP1_EXCLUI_TODOS;

END RM93613_PKG_PETS;