# ============================================================================ #
#                                                                              #
# Antes de executar o Script Python, instale as Bibliotecas necessárias        #
# Execute no Terminal:                                                         #
#                                                                              #
# pip install oracledb                                                         #
# pip install pandas                                                           #
#                                                                              #
# ============================================================================ #
#
# Importação dos módulos
#
import os
import platform
import oracledb
import pandas as pd

# Try para tentativa de Conexão com o Banco de Dados Oracle
try:

    # Conectar ao banco de dados
    
    # ================================================================================================================== #
    # CUIDADO!!! ==>>> COM 3 TENTATIVAS ERRADAS SUA CONTA FICA EM LOCK (Solicitar ao Help Desk via Whats para desbloquear)
    # ================================================================================================================== #

    conn = oracledb.connect(user="rm93613", password="150503", dsn="oracle.fiap.com.br:1521/orcl")

    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()

except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True

margem = ' ' * 4 # Define uma margem para a exibição da aplicação

# Recupera o Sistema Operacional do Cliente
sist_oper = platform.system()

# Enquanto o flag conexao estiver apontado com True
while conexao:

    # Limpa a tela via SO - Windows: cls   Mac / Linux: clear
    if sist_oper == 'Windows':
       os.system('cls')
    else: 
        os.system('clear')

    # Apresenta o menu
    print("------- CRUD - PETSHOP -------")
    print("""
    1 - Cadastrar Pet
    2 - Listar Pets por ID
    3 - Listar Todos os Pets
    4 - Alterar Pet
    5 - Excluir Pet
    6 - EXCLUIR TODOS OS PETS
    7 - SAIR
    """)

    # Captura a escolha do usuário
    escolha = input(margem + "Escolha -> ")

    # Verifica se o número digitado é um valor numérico
    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 7
        print("Digite um número.\nReinicie a Aplicação!")

    # Limpa a tela via SO
    if sist_oper == 'Windows':
       os.system('cls')
    else: 
        os.system('clear')

    # VERIFICA QUAL A ESCOLHA DO USUÁRIO

    # CADASTRAR UM PET
    if escolha == 1:

        print("----- CADASTRAR PET -----\n")

        # Recebe os valores para cadastro
        tipo = input(margem + "Digite o tipo....: ")
        nome = input(margem + "Digite o nome....: ")
        idade = int(input(margem + "Digite a idade...: "))

        # Chama a procedure para inserir um novo Pet - SEM SE PREOCUPAR COM A ORDEM DOS PARÂMETROS

        # inst_cadastro.callproc('CP1_CADASTRO_PET',
        # keywordParameters={"p_tipoPet": tipo, "p_nomePet": nome, "p_nomePet": idade})

        inst_cadastro.callproc('CP1_CADASTRO_PET',
        parameters=[tipo, nome, idade])

        
        conn.commit()

        #
        # Para realizar um Roolback, caso necessário:
        #
        #conn.rollback()

        # Caso haja sucesso na gravação
        print("\n##### Dados GRAVADOS #####")


    # LISTAR PETS POR ID
    elif escolha == 2:

        print("----- LISTAR PET POR ID-----\n")

        # Permite o usuário escolher um Pet pelo id
        pet_id = int(input(margem + "Escolha um Id: "))  

        # Chama a Função para Recuperar um Pet (Uma linha somente)

        lista = inst_consulta.callfunc('CP1_GET_PET',
                                str,  ## int para retorno com NUMBER na Função. Em nosso caso retorna uma String (VARCHAR2)
                                [pet_id])

        print(lista)

        print("\n##### LISTADO! #####")


    # LISTAR TODOS OS PETS
    elif escolha == 3:
            
        # Lista para a captura de dados do Banco
        lista_dados = []

        # Monta a instrução SQL de seleção de todos os registros da tabela
        inst_consulta.execute('SELECT * FROM petshop')
        # Captura todos os registros da tabela e armazena no objeto data
        data = inst_consulta.fetchall()

        # Insere os valores da tabela na Lista
        for dt in data:
            lista_dados.append(dt)

        # ordena a lista
        lista_dados = sorted(lista_dados)

        # Gera um DataFrame com os dados da lista utilizando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'], index='Id')

        # Verifica se não há registro através do dataframe
        if dados_df.empty:
            print(f"Não há um Pets cadastrados!")
        else:
            print(dados_df) # Exibe os dados selecionados da tabela

        print("\n##### LISTADOS! #####")

    # ALTERAR OS DADOS DE UM REGISTRO
    elif escolha == 4:

        # ALTERANDO UM REGISTRO
        print("----- ALTERAR DADOS DO PET -----\n")

        # Lista para a captura de dados da tabela
        lista_dados = []

        # Permite o usuário escolher um Pet pelo id
        pet_id = int(input(margem + "Escolha um Id: "))

        # Constroi a instrução de consulta para verificar a existencia ou não do id
        consulta = f""" SELECT * FROM petshop WHERE id = {pet_id}"""
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        # Preenche a lista com o registro encontrado (ou não)
        for dt in data:
            lista_dados.append(dt)

        # analisa se foi encontrado algo
        if len(lista_dados) == 0: # se não há o id
            print(f"Não há um pet cadastrado com o ID = {pet_id}")
            input("\nPressione ENTER")
        else:
            # Captura os novos dados
            novo_tipo = input(margem + "Digite um novo tipo: ")
            novo_nome = input(margem + "Digite um novo nome: ")
            nova_idade = input(margem + "Digite uma nova idade: ")

            # Chama a procedure para atualizar um novo Pet - SEM SE PREOCUPAR COM A ORDEM DOS PARÊMETROS
            # inst_alteracao.callproc('nomeProcedure',
            # keywordParameters={"nomeParam1_naProc": param1, "nomeParam2_naProc": param2, "nomeParam3_naProc": param3, "nomeParam4_naProc": param4})

            inst_cadastro.callproc('CP1_ALTERA_PET',
                parameters=[pet_id, novo_tipo, novo_nome, nova_idade])

            conn.commit()

            if len(lista_dados) == 0:
                print("\n##### ID NÃO ENCONTRADO! #####")
            else:
                print("\n##### Dados ATUALIZADOS! #####")

    # EXCLUIR UM REGISTRO
    elif escolha == 5:

        print("----- EXCLUIR PET -----\n")

        # Lista para a captura de dados da tabela
        lista_dados = []

        # Permite o usuário escolher um Pet pelo ID
        pet_id = input(margem + "Escolha um Id: ")

        if pet_id.isdigit():
            pet_id = int(pet_id)
            consulta = f""" SELECT * FROM petshop WHERE id = {pet_id}"""
            inst_consulta.execute(consulta)
            data = inst_consulta.fetchall()

            # Insere os valores da tabela na lista
            for dt in data:
                lista_dados.append(dt)

            # Verifica se o registro está cadastrado
            if len(lista_dados) == 0:
                print(f"Não há um pet cadastrado com o ID = {pet_id}")
            else:

                # Chama a procedure para deletar um novo Pet - SEM SE PREOCUPAR COM A ORDEM DOS PARÂMETROS
                inst_exclusao.callproc('CP1_EXCLUI_PET', parameters=[pet_id] )

                conn.commit()
                print("\n##### Pet APAGADO! #####")  # Exibe mensagem caso haja sucesso
        else:
            print("O Id não é numérico!")


    # EXCLUIR TODOS OS REGISTROS
    elif escolha == 6:

        print("\n!!!!! EXCLUI TODOS OS DADOS TABELA !!!!!\n")
        
        confirma = input(margem + "CONFIRMA A EXCLUSÃO DE TODOS OS PETS? [S]im ou [N]ÃO?")
        
        if confirma.upper() == "S":

            # Chama a procedure para limpar a tabela
            inst_exclusao.callproc('CP1_EXCLUI_TODOS') ## A Procedure não recebe parâmetros

            conn.commit()

            # Depois de excluir todos os registros ele zera o ID
            data_reset_ids = """ ALTER TABLE petshop MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) """
            inst_exclusao.execute(data_reset_ids)

            print("##### Todos os registros foram excluídos! #####")
        else:
            print(margem + "Operação cancelada pelo usuário!")


    # SAI DA APLICAÇÃO
    elif escolha == 7:

        # Modificando o flag da conexão
        conexao = False


    # CASO O NUMERO DIGITADO NÃO SEJA UM DO MENU
    else:

        input(margem + "Digite um número entre 1 e 7.")

    # Pausa o fluxo da aplicação para a leitura das informações
    input(margem + "Pressione ENTER")
else:
    # Fechar a conexão com o Banco - NUNCA ESQUEÇA DE FECHAR SUA CONEXÃO COM O BANCO DE DADOS
    inst_cadastro.close()
    inst_consulta.close()
    inst_alteracao.close()
    inst_exclusao.close()
    conn.close()
    print("Obrigado por utilizar a nossa aplicação! :)")
    print("⡶⠛⢲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⣇⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⢹⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⢤⡀")
    print("⠸⡆⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⢸⠇")
    print("⠀⣇⠀⠀⢷⠀⣀⣄⣀⠀⢀⣀⡀⠀⢠⠇⠀⢸⠀")
    print("⠀⢹⠀⢀⣼⣿⡿⣆⠈⣷⠏⠉⠉⣷⣾⠀⠀⡏⠀")
    print("⠀⣸⢷⠟⠛⠋⢰⠏⠀⣿⠀⠀⠀⣿⠀⠀⢠⡇⠀")
    print("⠀⡏⠀⠀⢀⡴⣏⣀⣀⣿⣄⣀⡀⡇⠀⠀⢸⠁⠀")
    print("⠀⢳⠀⠀⠘⣧⣿⡉⠸⣿⡏⢀⣿⠃⠀⠀⢸⠀⠀")
    print("⠀⠈⣧⠀⠀⠘⣟⠛⠚⠃⠙⠚⠛⠀⠀⠀⣾⠀⠀")
    print("⠀⠀⠸⡄⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠀")
    print("⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀")
    print("⠀⠀⠀⠘⠣⠤⠤⠀⣀⣀⣀⡀⠤⠤⠖⠃⠀⠀⠀")

