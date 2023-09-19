<h1>1º Checkpoint – 2º Semestre</h1>
<h2>1) Crie os Procedimentos a seguir no Banco Oracle 19c da FIAP</h2>
<ul>
    <li>Uma Procedure para Cadastrar um PeT</li>
    <li>Uma Função para recuperar dados de um Pet com base no parâmetro ID</li>
    <li>Uma Procedure para alterar dados de um Pet com base no parâmetro ID</li>
    <li>Uma Procedure para excluir um Pet com base no parâmetro ID</li>
    <li>Uma Procedure para excluir todos as linhas da Tabela</li>
</ul>
<h2>2) Crie uma Package e uma Package Body com todos os Procedimentos criados empacotados</h2>
<h2>3) Criar um Trigger e uma Tabela para auditar as inserções, atualizações e deleções da tabela PETSHOP</h2>
<ul>
    <li>Crie uma tabela com o nome audit_petshop com os seguintes campos: ID, Usuário, Data, Comando (INSERT, UPDATE ou DELETE), Valor antigo e Valornovo</li>
    <li>Crie um Trigger na tabela PETSHOP que irá disparar para cada linha e que insira a auditoria natabela audit_petshop</li>
</ul>
