create table petshop(
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo_pet VARCHAR2(30),
    nome_pet VARCHAR2(30),
    idade INT
);

DROP TABLE audit_petshop;

CREATE TABLE audit_petshop (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario VARCHAR2(30),
    data_registro DATE,
    comando VARCHAR2(6),
    valor_tipo_antigo VARCHAR2(30),
    valor_nome_antigo VARCHAR2(30),
    valor_idade_antigo NUMBER,
    valor_tipo_novo VARCHAR2(30),
    valor_nome_novo VARCHAR2(30),
    valor_idade_novo NUMBER
)