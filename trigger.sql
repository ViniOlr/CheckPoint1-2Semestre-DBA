CREATE OR REPLACE TRIGGER RM93613_trg_audit_petshop
AFTER INSERT OR UPDATE OR DELETE ON petshop
FOR EACH ROW
DECLARE

    v_comando VARCHAR2(6);

    v_valorTipoAntigo VARCHAR2(30);
    v_valorNomeAntigo VARCHAR2(30);
    v_valorIdadeAntigo NUMBER;

    v_valorTipoNovo VARCHAR2(30);
    v_valorNomeNovo VARCHAR2(30);
    v_valorIdadeNovo NUMBER;

BEGIN

    IF INSERTING THEN
        v_comando := 'INSERT';

        v_valorTipoAntigo := null;
        v_valorNomeAntigo := null;
        v_valorIdadeAntigo := null;

        v_valorTipoNovo := :new.tipo_pet;
        v_valorNomeNovo := :new.nome_pet;
        v_valorIdadeNovo := :new.idade;

    ELSIF UPDATING THEN
        v_comando := 'UPDATE';

        v_valorTipoAntigo := :old.tipo_pet;
        v_valorNomeAntigo := :old.nome_pet;
        v_valorIdadeAntigo := :old.idade;

        v_valorTipoNovo := :new.tipo_pet;
        v_valorNomeNovo := :new.nome_pet;
        v_valorIdadeNovo := :new.idade;

    ELSIF DELETING THEN
        v_comando := 'DELETE';

        v_valorTipoAntigo := :old.tipo_pet;
        v_valorNomeAntigo := :old.nome_pet;
        v_valorIdadeAntigo := :old.idade;

        v_valorTipoNovo := null;
        v_valorNomeNovo := null;
        v_valorIdadeNovo := null;
        
    END IF;

    INSERT INTO audit_petshop(usuario, data_registro, comando, valor_tipo_antigo, valor_nome_antigo, valor_idade_antigo, valor_tipo_novo, valor_nome_novo, valor_idade_novo)
    VALUES (USER, SYSDATE, v_comando, v_valorTipoAntigo, v_valorNomeAntigo, v_valorIdadeAntigo, v_valorTipoNovo, v_valorNomeNovo, v_valorIdadeNovo);

EXCEPTION

    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Ocorreu um erro: ' || SQLERRM);

END;