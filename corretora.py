import customtkinter as ctk                 # Importei a biblioteca customtkinter para criar a interface gráfica
from config import USUARIO, SENHA          # Importando as credenciais de login do arquivo config.py

ctk.set_appearance_mode("dark")            # escolhi tema escuro
ctk.set_default_color_theme("blue")       # Cor das janelas

janela = ctk.CTk()                           # Criou a janela principal
janela.title("Corretora de Seguros")      # titulo da janela
janela.geometry("850x650")                  # aumentado o tamanho da janela 


# ============= BANCO DADO ==
bd_clientes = []                 # banco temporario até integracõa
bd_apolices = []                   
bd_vendas = []                       


# === FUNÇÃO LIMITA TAMANHO ==========

def limita_cpf(tamanho_texto):                                # faz o CPF não ultrapasse 11 numeros
    if len(tamanho_texto) <= 11:
        return True
    return False

def limita_apolice(texto_atual):                          # apolice nao ultrapassa 15 caracter 
    if len(texto_atual) <= 15:
        return True
    return False

def limita_venda(texto_atual):                            # ID da venda nao ultrapasse 10 caracteres
    if len(texto_atual) <= 10:
        return True
    return False

def limita_telefone(texto_atual):             # telefone nao ultrapasse 11 caracteres (considerando o DDD + número)
    if len(texto_atual) <= 11:
        return True
    return False


# Registra as funções para que possam ser usadas como validadores 
validador_cpf = janela.register(limita_cpf)
validador_apolice = janela.register(limita_apolice)
validador_venda = janela.register(limita_venda)
validador_telefone = janela.register(limita_telefone)


# ====== JANELA DE RESPOSTA =============

def mostrar_msg_sucesso(mensagem):                        # Função exibir janela de sucesso ou confirmação após as operações do CRUD
    popup = ctk.CTkToplevel(janela)                                # cria uma nova janela pop-up
    popup.title("Aviso do Sistema")                             # nome da Janela
    popup.geometry("400x220")                                   # Tamanho da janela expandido para os novos retornos
    popup.grab_set()                                            # Impede interação com a janela principal enquanto o pop-up estiver aberto
    
    ctk.CTkLabel(                                               # Label para mostrar a mensagem de sucesso ou informação.
        popup, 
        text=mensagem, 
        font=ctk.CTkFont(size=13, weight="bold"),
        wraplength=350
    ).pack(pady=(30, 20))
    
    ctk.CTkButton(                                              # botao para fechar msg sucesso
        popup, 
        text="OK", 
        width=100, 
        command=popup.destroy
    ).pack()


# ******* FUNÇÃO DE LOGIN ***8

def login():                                                                 # define a função de login
    usuario = entry_user.get()                                               # pega o texto digitado no campo de usuário (CPF) e armazena na variável "usuario"
    senha = entry_pass.get()                                                 # pega o texto digitado no campo de senha e armazena na variável "senha"

    if usuario == USUARIO and senha == SENHA:                                # condição que ve se o usuario e senha estão corretos
        label_erro.configure(text="")                                        # Limpa mensagem de erro
        frame_login.pack_forget()                                            # Esconde o painel de login
        frame_menu.pack(fill="both", expand=True)                            # mostra o painel do menu principal
        frame_lateral.pack(side="left", fill="y")                            # Ao logar, o menu lateral já deve aparecer fixo
        mostrar_tela_clientes()                                             # Exibe a seção de clientes por padrão ao entrar no sistema

    else:
        label_erro.configure(
            text="Usuário ou senha incorretos!",                            # se falso mostra a mensagem de erro
            text_color="red"
        )                                                                    

def login_entrar(event):                                                  # função disparar o login C/ enter 
    login()


# ******PAINEL DE LOGIN ============

frame_login = ctk.CTkFrame(master=janela)                        # Cria o painel de login
frame_login.pack(pady=20, padx=40, fill="both", expand=True)     # Posiciona o painel na janela

ctk.CTkLabel(                                                    # Label do título do login
    frame_login,
    text=" Corretora de Valores ",
    text_color="green",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(pady=(24, 4))                                             # Espaçamento do título

ctk.CTkLabel(                                                    # Label de instrução para o usuário
    frame_login,
    text="Informe seu LOGIN para continuar",
    font=ctk.CTkFont(size=12),
    text_color="white"
).pack(pady=(0, 16))                                             # Espaçamento inferior maior para separar do campo de entrada


entry_user = ctk.CTkEntry(                                       # campo de entreda do login
    frame_login,
    placeholder_text="LOGIN",                                      # Texto exibido quando vazio
    width=260,
    height=40
)
entry_user.pack(pady=8)                                          # Espaçamento entre os campos de entrada


entry_pass = ctk.CTkEntry(                                       # Campo de entrada para a senha
    frame_login,
    placeholder_text="Senha",
    show="*",                                                    # Substitui caracteres por "*"
    width=260,
    height=40
)
entry_pass.pack(pady=8)                                          # Espaçamento entre os campos de entrada


label_erro = ctk.CTkLabel(
    frame_login,                                                 # Label de erro (começa vazia)
    text="",
    font=ctk.CTkFont(size=12)
)
label_erro.pack(pady=(4, 0))                                     # Espaçamento superior para separar da senha


btn_login = ctk.CTkButton(                                       # cria o botão de login
    frame_login,
    text="Entrar",
    command=login,                                               # Chama a função login() ao clicar
    width=260,
    height=40,
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="green",                                            # cor do botão 
    hover_color="darkgreen"                                      # Muda a cor quando passa o mouse 
)
btn_login.pack(pady=16)                                          


janela.bind("<Return>", login_entrar)                    # Tecla Enter também aciona o login


# ********* PAINEL MENU PRINCIPAL ********

frame_menu = ctk.CTkFrame(master=janela)                         # Criou o painel do menu principal 


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(                                     # criei a barra superior do menu principal
    frame_menu,
    height=45,
    corner_radius=0,
    fg_color="#1a1a2e"
)

frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)                               # impede que o painel redimensione


ctk.CTkLabel(                                                    # Label do título na barra superior
    frame_topbar,
    text=" Corretora de Seguros - Sistema Interno",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="white"
).pack(side="left", padx=20)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                              # função para fechar o menu e voltar para a tela de login

    frame_menu.pack_forget()                                     # Esconde  painel  menu principal
    frame_lateral.pack_forget()                                  # Garante que i menu lateral também suma

    frame_login.pack(                                            # Mostra o painel de login outra vez
        pady=20,
        padx=40,
        fill="both",
        expand=True
    )

    entry_user.delete(0, "end")                                  # Limpa o campo de usuário
    entry_pass.delete(0, "end")                                  # Limpa o campo de senha


# ============= PAiNEL CENTRAL =============

frame_centro = ctk.CTkFrame(                                     # Cria o frame central do menu principal
    frame_menu,
    fg_color="transparent"
)

frame_centro.pack(fill="both", expand=True)                      # Preenche todo o espaço disponível


# ============= MENU LATERAL 

frame_lateral = ctk.CTkFrame(                                    # Cria o menu lateral fixo
    frame_centro,
    width=180,
    corner_radius=0,
    fg_color="#16213e"
)
frame_lateral.pack_propagate(False)                              # Mantém a largura fixa


ctk.CTkLabel(
    frame_lateral,
    text="NAVEGAÇÃO",
    font=ctk.CTkFont(size=12, weight="bold"),                    # Label do título do menu lateral
    text_color="gray"
).pack(pady=(20, 10), padx=12, anchor="w")


# ============= PAINEL DE CONTEÚDO 

frame_conteudo = ctk.CTkFrame(                                   # Cria o painel para exibir o conteúdo das seções
    frame_centro,
    fg_color="transparent"
)

frame_conteudo.pack(
    side="right",
    fill="both",
    expand=True
)


# ============= VARIÁVEIS   INPUTS 

campo1_ativo = None                           #variavel para armazenar tudo que o usuario digitar, tanto em clientes,vendas e apolices.
campo2_ativo = None
campo3_ativo = None
campo4_ativo = None
campo5_ativo = None
campo6_ativo = None
campo7_ativo = None
label_erro_crud = None                           # var mostar msg de erro do crud                
painel_usado = ""
chamar_acao = ""                                 # var para armazenar a ação do crud, se é acrescentar, atualizar etc, para usar na função de confirmação do crud


# ============= funçao de confirmação do crud  

def confirma_crud():                                  # função de confirmação 
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo, campo5_ativo, campo6_ativo, campo7_ativo   # var armazena os dados digitados
    global painel_usado, chamar_acao, label_erro_crud, bd_clientes, bd_apolices, bd_vendas         # var para mostrar msg de erro e bd temporario
    
    v1 = campo1_ativo.get().strip() if campo1_ativo else ""                 # variavel para armazenar o valor do campo1, se o campo existir, caso contrário, armazena uma string vazia. O método strip() é usado para remover espaços em branco extras.
    v2 = campo2_ativo.get().strip() if campo2_ativo else ""
    v3 = campo3_ativo.get().strip() if campo3_ativo else ""
    v4 = campo4_ativo.get().strip() if campo4_ativo else ""
    v5 = campo5_ativo.get().strip() if campo5_ativo else ""
    v6 = campo6_ativo.get().strip() if campo6_ativo else ""
    v7 = campo7_ativo.get().strip() if campo7_ativo else ""
    
    label_erro_crud.configure(text="")                           

    # --- FUNÇÃO DE VALIDAR DE CAMP VAZIO ---
    if chamar_acao in ["Acrescentar", "Atualizar"]:           # garante que todos os campos  devem ser preenchidos
        if (campo1_ativo and not v1) or (campo2_ativo and not v2) or (campo3_ativo and not v3) or \
           (campo4_ativo and not v4) or (campo5_ativo and not v5) or (campo6_ativo and not v6) or (campo7_ativo and not v7):
            label_erro_crud.configure(text="Erro: Preencha todos os campos do formulário!", text_color="#e74c3c")
            return
            
    elif chamar_acao in ["Pesquisar", "Remover"]:             # garante que pelo menos um campo  deve ser preenchido
        if not v1 and not v2 and not v3 and not v4 and not v5 and not v6 and not v7:
            label_erro_crud.configure(text="Erro: Preencha pelo menos um campo para buscar!", text_color="#e74c3c")
            return

    mensagem_alerta = "Operação realizada com sucesso!"     
    
    # ====== 1. CRUD DOS CLIENTES 
    if painel_usado == "Clientes":               # se o painel usado for = clientes
        if chamar_acao == "Acrescentar":       # se acao_aplicada for = Acrescentar
            novo_cliente = {                        #cria um dic c/ os dados do cliente
                "cpf_cnpj": v1, "nome_completo": v2, "email": v3,   # usa os campos,v1,v2 etc para preencher os dados do cliente
                "sexo": v4, "telefone": v5, "data_nascimento": v6, "status": v7
            }
            bd_clientes.append(novo_cliente)                 # adiciona o novo cliente ao bd temporário
            mensagem_alerta = "Cliente adicionado com sucesso"      #MSG de sucesso
            
        elif chamar_acao == "Pesquisar":
            cliente_encontrado = None
            for cliente in bd_clientes:
                if (v1 and cliente["cpf_cnpj"] == v1) or (v2 and cliente["nome_completo"].lower() == v2.lower()) or (v5 and cliente["telefone"] == v5):
                    cliente_encontrado = cliente
                    break
            
            if cliente_encontrado:
                mensagem_alerta = f"Cliente encontrado!\n\nCPF/CNPJ: {cliente_encontrado['cpf_cnpj']}\nNome: {cliente_encontrado['nome_completo']}\nEmail: {cliente_encontrado['email']}\nSexo: {cliente_encontrado['sexo']}\nTelefone: {cliente_encontrado['telefone']}\nNascimento: {cliente_encontrado['data_nascimento']}\nStatus: {cliente_encontrado['status']}"
            else:
                label_erro_crud.configure(text="Erro: Nenhum cliente localizado!", text_color="#e74c3c")
                return
                
        elif chamar_acao == "Atualizar":
            atualizou = False
            for cliente in bd_clientes: 
                if cliente["cpf_cnpj"] == v1:
                    cliente["nome_completo"] = v2
                    cliente["email"] = v3
                    cliente["sexo"] = v4
                    cliente["telefone"] = v5
                    cliente["data_nascimento"] = v6
                    cliente["status"] = v7
                    atualizou = True
                    break
            if atualizou:
                mensagem_alerta = "Dados atualizados com sucesso"
            else:
                label_erro_crud.configure(text="Erro: CPF/CNPJ não cadastrado para atualização!", text_color="#e74c3c")
                return
            
                # Ajuda do Professor Para atualizar um cliente, o código percorre o banco de dados de clientes procurando por um cliente cujo CPF/CNPJ corresponda ao valor do campo1 (v1). 
        elif chamar_acao == "Remover":    # para remover o cliente, primeiro localiza a posição do cliente no bd e depois remove usando del
            posicao_remover = -1              # var para armazenar  posição do cliente que vai ser removido, inicia com -1 
            for i in range(len(bd_clientes)):   # percorre o bd de clientes usando o índice para localizar a posição do cliente a ser removido
                cliente = bd_clientes[i]
                if (v1 and cliente["cpf_cnpj"] == v1) or (v2 and cliente["nome_completo"].lower() == v2.lower()) or (v5 and cliente["telefone"] == v5): # verifica se o cliente corresponde aos critérios de filtro para remoção
                    posicao_remover = i
                    break
            
            if posicao_remover != -1:
                del bd_clientes[posicao_remover]
                mensagem_alerta = "Cliente removido com sucesso"
            else:
                label_erro_crud.configure(text="Erro: Nenhum cliente localizado para remoção!", text_color="#e74c3c")
                return
            
    # 2. CRUD DE APÓLICES 
    elif painel_usado == "Apólices":
        if chamar_acao == "Acrescentar":
            nova_apolice = {"id_apolice": v1, "id_cotacao": v2, "inicio": v3, "fim": v4}
            bd_apolices.append(nova_apolice)
            mensagem_alerta = "Apólice adicionada com sucesso"
            
        elif chamar_acao == "Pesquisar":
            apolice_encontrada = None
            for apolice in bd_apolices:
                if (v1 and apolice["id_apolice"] == v1) or (v2 and apolice["id_cotacao"] == v2):
                    apolice_encontrada = apolice
                    break
            if apolice_encontrada:
                mensagem_alerta = f"Apólice localizada!\n\nID Apólice: {apolice_encontrada['id_apolice']}\nID Cotação: {apolice_encontrada['id_cotacao']}\nInício Vigência: {apolice_encontrada['inicio']}\nFim Vigência: {apolice_encontrada['fim']}"
            else:
                label_erro_crud.configure(text="Erro: Nenhuma apólice localizada!", text_color="#e74c3c")
                return
                
        elif chamar_acao == "Atualizar":    #  se usuario escolher atualizar, o código percorre o banco de dados de apólices  
            atualizou = False                       # var para indicar se a atualização foi realizada.
            for apolice in bd_apolices:                # percorre o banco de dados de apólices 
                if apolice["id_apolice"] == v1:      # verifica se o ID da apólice corresponde ao valor do campo1 (v1)
                    apolice["inicio"] = v3             # se encontrar a apólice, atualiza os campos de início e fim com os valores dos campos 3 e 4 (v3 e v4)
                    apolice["fim"] = v4              # atualiza a data de fim da apólice
                    atualizou = True                # indica que a atualização foi realizada
                    break
            if atualizou:                            # se a atualização foi realizada exibe a mensagem de sucesso
                mensagem_alerta = "Apólice atualizada com sucesso"
            else:
                label_erro_crud.configure(text="Erro: ID de apólice não cadastrado!", text_color="#e74c3c")
                return
                
        elif chamar_acao == "Remover":              # para remover a apólice localiza a posição da apólice no bd 
            posicao_remover = -1                     # var para armazenar a posição da apólice que vai ser removida, inicia com -1 indicando que ainda não foi encontrada
            for i in range(len(bd_apolices)):        # percorre o banco de dados de apólices usando o índice 
                apolice = bd_apolices[i]             # verifica se os critérios de filtro para remoção apólice corresponde ao valor do campo1 (v1) 
                if (v1 and apolice["id_apolice"] == v1) or (v2 and apolice["id_cotacao"] == v2):   #faz a busca pelo campo 1 e 2 ,apolice ou cotação, para localizar a apólice a ser removida
                    posicao_remover = i
                    break
            if posicao_remover != -1:
                del bd_apolices[posicao_remover]
                mensagem_alerta = "Apólice removida com sucesso"
            else:
                label_erro_crud.configure(text="Erro: Nenhuma apólice encontrada para remoção!", text_color="#e74c3c")
                return
            
    # 3. CRUD DE VENDAS 
    elif painel_usado == "Vendas":
        if chamar_acao == "Acrescentar":
            nova_venda = {"id_cotacao": v1, "id_pessoa": v2, "id_seguradora": v3, "id_plano": v4, "valor_cotacao": v5, "data_cotacao": v6}
            bd_vendas.append(nova_venda)
            mensagem_alerta = "Venda registrada com sucesso"
            
        elif chamar_acao == "Pesquisar":
            venda_encontrada = None
            for venda in bd_vendas:
                if (v1 and venda["id_cotacao"] == v1) or (v2 and venda["id_pessoa"] == v2):
                    venda_encontrada = venda
                    break
            if venda_encontrada:
                mensagem_alerta = f"Dados da venda carregados!\n\nID Cotação: {venda_encontrada['id_cotacao']}\nID Pessoa: {venda_encontrada['id_pessoa']}\nID Seguradora: {venda_encontrada['id_seguradora']}\nID Plano: {venda_encontrada['id_plano']}\nValor: R$ {venda_encontrada['valor_cotacao']}\nData: {venda_encontrada['data_cotacao']}"
            else:
                label_erro_crud.configure(text="Erro: Registro de venda não localizado!", text_color="#e74c3c")
                return
                
        elif chamar_acao == "Atualizar":
            atualizou = False
            for venda in bd_vendas:
                if venda["id_cotacao"] == v1:
                    venda["id_pessoa"] = v2
                    venda["id_seguradora"] = v3
                    venda["id_plano"] = v4
                    venda["valor_cotacao"] = v5
                    venda["data_cotacao"] = v6
                    atualizou = True
                    break
            if atualizou:
                mensagem_alerta = "Venda modificada com sucesso"
            else:
                label_erro_crud.configure(text="Erro: ID de cotação não cadastrado!", text_color="#e74c3c")
                return
                
        elif chamar_acao == "Remover":
            posicao_remover = -1
            for i in range(len(bd_vendas)):
                venda = bd_vendas[i]
                if (v1 and venda["id_cotacao"] == v1) or (v2 and venda["id_pessoa"] == v2):
                    posicao_remover = i
                    break
            if posicao_remover != -1:
                del bd_vendas[posicao_remover]
                mensagem_alerta = "Venda excluída com sucesso"
            else:
                label_erro_crud.configure(text="Erro: Registro de venda não encontrado para remoção!", text_color="#e74c3c")
                return

    # Limpa os dados dos campos de texto após o sucesso
    if campo1_ativo: campo1_ativo.delete(0, "end")
    if campo2_ativo: campo2_ativo.delete(0, "end")
    if campo3_ativo: campo3_ativo.delete(0, "end")
    if campo4_ativo: campo4_ativo.delete(0, "end")
    if campo5_ativo: campo5_ativo.delete(0, "end")
    if campo6_ativo: campo6_ativo.delete(0, "end")
    if campo7_ativo: campo7_ativo.delete(0, "end")
    
    # Exibe o Pop-up com as informações encontradas/cadastradas
    mostrar_msg_sucesso(mensagem_alerta)


# ============= CONSTRUÇÃO DINÂMICA DOS CAMPOS DO FORMULÁRIO =============

def gerar_campos_formulario(acao, nome_secao):
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo, campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud
    
    painel_usado = nome_secao
    chamar_acao = acao

    # Limpa a área de formulários anterior
    for w in frame_zona_inputs.winfo_children():
        w.destroy()

    # Título do formulário atual
    ctk.CTkLabel(
        frame_zona_inputs, 
        text=f"Formulário para: {acao} {nome_secao[:-1]}", 
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#3498db"
    ).pack(pady=(10, 5))

    # Cria a Label de Erro específica do CRUD dentro deste frame
    label_erro_crud = ctk.CTkLabel(frame_zona_inputs, text="", font=ctk.CTkFont(size=12, weight="bold"))
    label_erro_crud.pack(pady=2)

    lbl1, placeholder1, validador1 = None, None, None
    lbl2, placeholder2, validador2 = None, None, None
    lbl3, placeholder3, validador3 = None, None, None
    lbl4, placeholder4, validador4 = None, None, None
    lbl5, placeholder5, validador5 = None, None, None
    lbl6, placeholder6, validador6 = None, None, None
    lbl7, placeholder7, validador7 = None, None, None

    # Mapeamento completo e flexível alinhado às restrições do banco
    if nome_secao == "Clientes":
        if acao in ["Pesquisar", "Remover"]:
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Filtro):", "Deixe vazio para filtrar por outro", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo (Filtro):", "Deixe vazio para filtrar por outro", None
            lbl5, placeholder5, validador5 = "Telefone (Filtro):", "Deixe vazio para filtrar por outro", validador_telefone
        else:
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Max 11):", "Digite apenas números", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:", "Nome da pessoa", None
            lbl3, placeholder3, validador3 = "Email:", "exemplo@email.com", None
            lbl4, placeholder4, validador4 = "Sexo (M/F):", "Apenas 1 caractere", None
            lbl5, placeholder5, validador5 = "Telefone (Max 11):", "DDD + Número", validador_telefone
            lbl6, placeholder6, validador6 = "Data de Nascimento (AAAA-MM-DD):", "Formato do Banco (Date)", None
            lbl7, placeholder7, validador7 = "Status (Ativo/Inativo):", "Status cadastral", None

    elif nome_secao == "Apólices": # Tabela: Apolice
        if acao in ["Pesquisar", "Remover"]:
            lbl1, placeholder1, validador1 = "ID Apólice (Filtro):", "Filtrar por ID da Apólice", validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (Filtro):", "Filtrar por ID da Cotação", validador_venda
        else:
            lbl1, placeholder1, validador1 = "ID Apólice (id_apolice):", "Código identificador", validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (id_cotacao):", "Chave estrangeira de Cotações", validador_venda
            lbl3, placeholder3, validador3 = "Data Início (AAAA-MM-DD):", "Início do seguro", None
            lbl4, placeholder4, validador4 = "Data Fim (AAAA-MM-DD):", "Fim do seguro", None

    elif nome_secao == "Vendas": # Tabela: Cotacoes
        if acao in ["Pesquisar", "Remover"]:
            lbl1, placeholder1, validador1 = "ID Cotação (Filtro):", "Filtrar por Cotação", validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa (Filtro):", "Filtrar por ID do cliente", None
        else:
            lbl1, placeholder1, validador1 = "ID Cotação (id_cotacao):", "Código identificador", validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa (id_pessoa):", "Chave estrangeira de Pessoa", None
            lbl3, placeholder3, validador3 = "ID Seguradora:", "Chave estrangeira de Seguradora", None
            lbl4, placeholder4, validador4 = "ID Plano:", "Chave estrangeira de Plano", None
            lbl5, placeholder5, validador5 = "Valor da Cotação R$:", "Preço calculated", None
            lbl6, placeholder6, validador6 = "Data Cotação (AAAA-MM-DD):", "Data do processamento", None

    # Renderização empacotada dos componentes de entrada de dados baseado na regra selecionada
    campo1_ativo = None
    if lbl1:
        ctk.CTkLabel(frame_zona_inputs, text=lbl1, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo1_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder1, width=340, height=30)
        if validador1: campo1_ativo.configure(validate="key", validatecommand=(validador1, "%P"))
        campo1_ativo.pack(pady=(2, 4))

    campo2_ativo = None
    if lbl2:
        ctk.CTkLabel(frame_zona_inputs, text=lbl2, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo2_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder2, width=340, height=30)
        if validador2: campo2_ativo.configure(validate="key", validatecommand=(validador2, "%P"))
        campo2_ativo.pack(pady=(2, 4))

    campo3_ativo = None
    if lbl3:
        ctk.CTkLabel(frame_zona_inputs, text=lbl3, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo3_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder3, width=340, height=30)
        if validador3: campo3_ativo.configure(validate="key", validatecommand=(validador3, "%P"))
        campo3_ativo.pack(pady=(2, 4))

    campo4_ativo = None
    if lbl4:
        ctk.CTkLabel(frame_zona_inputs, text=lbl4, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo4_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder4, width=340, height=30)
        if validador4: campo4_ativo.configure(validate="key", validatecommand=(validador4, "%P"))
        campo4_ativo.pack(pady=(2, 4))

    campo5_ativo = None
    if lbl5:
        ctk.CTkLabel(frame_zona_inputs, text=lbl5, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo5_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder5, width=340, height=30)
        if validador5: campo5_ativo.configure(validate="key", validatecommand=(validador5, "%P"))
        campo5_ativo.pack(pady=(2, 4))

    campo6_ativo = None
    if lbl6:
        ctk.CTkLabel(frame_zona_inputs, text=lbl6, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo6_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder6, width=340, height=30)
        if validador6: campo6_ativo.configure(validate="key", validatecommand=(validador6, "%P"))
        campo6_ativo.pack(pady=(2, 4))

    campo7_ativo = None
    if lbl7:
        ctk.CTkLabel(frame_zona_inputs, text=lbl7, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
        campo7_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder7, width=340, height=30)
        if validador7: campo7_ativo.configure(validate="key", validatecommand=(validador7, "%P"))
        campo7_ativo.pack(pady=(2, 4))

    # Botão de confirmação associado à função normal 
    ctk.CTkButton(
        frame_zona_inputs,
        text=f"Confirmar {acao}",
        fg_color="#27ae60",
        hover_color="#2ecc71",
        width=200,
        height=35,
        command=confirma_crud
    ).pack(pady=12)


# ============= FUNÇÕES DE PONTE PARA OS BOTÕES DO CRUD  =============

def acao_acrescentar_clicada():
    gerar_campos_formulario("Acrescentar", secao_painel_aberto)

def acao_pesquisar_clicada():
    gerar_campos_formulario("Pesquisar", secao_painel_aberto)

def acao_atualizar_clicada():
    gerar_campos_formulario("Atualizar", secao_painel_aberto)

def acao_remover_clicada():
    gerar_campos_formulario("Remover", secao_painel_aberto)


# ============= FUNÇÃO GERAL PARA MONTAR A ESTRUTURA DO PAINEL =============

secao_painel_aberto = ""

def montar_estrutura_painel(nome):
    global frame_zona_inputs, secao_painel_aberto
    secao_painel_aberto = nome

    for w in frame_conteudo.winfo_children():                    
        w.destroy()

    ctk.CTkLabel(                                                
        frame_conteudo,
        text=f"Painel de {nome}",
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=(20, 15))

    frame_botoes_crud = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes_crud.pack(pady=10)

    ctk.CTkButton(frame_botoes_crud, text="Acrescentar", width=110, height=35, command=acao_acrescentar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Pesquisar", width=110, height=35, fg_color="#34495e", hover_color="#2c3e50", command=acao_pesquisar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Atualizar", width=110, height=35, fg_color="#2980b9", hover_color="#3498db", command=acao_atualizar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Remover", width=110, height=35, fg_color="#c0392b", hover_color="#e74c3c", command=acao_remover_clicada).pack(side="left", padx=5)

    frame_zona_inputs = ctk.CTkScrollableFrame(frame_conteudo, fg_color="transparent")
    frame_zona_inputs.pack(pady=10, fill="both", expand=True)


# ============= FUNÇÕES DE PONTE PARA O MENU LATERAL (SEM LAMBDA) =============

def mostrar_tela_clientes():
    montar_estrutura_painel("Clientes")

def mostrar_secao_apolices():
    montar_estrutura_painel("Apólices")

def mostrar_secao_vendas():
    montar_estrutura_painel("Vendas")


# ============= BOTÕES DO MENU LATERAL =============

ctk.CTkButton(frame_lateral, text=" CLIENTES", anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_tela_clientes).pack(pady=3, padx=10)
ctk.CTkButton(frame_lateral, text=" APÓLICES", anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_apolices).pack(pady=3, padx=10)
ctk.CTkButton(frame_lateral, text=" VENDAS", anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_vendas).pack(pady=3, padx=10)

# Botão SAIR (Fixo embaixo)
btn_sair_lateral = ctk.CTkButton(
    frame_lateral,
    text="SAIR",
    anchor="center",
    width=160,
    height=40,
    fg_color="#c0392b",
    hover_color="#e74c3c",
    font=ctk.CTkFont(size=13, weight="bold"),
    command=fechar_login                                         
)
btn_sair_lateral.pack(side="bottom", pady=20, padx=10)           


# ============= LOOP PRINCIPAL =============

janela.mainloop()