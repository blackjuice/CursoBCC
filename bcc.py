# MAE0121+MAE0212 dispensa MAE0119
# sys.argv()
import sys


#---------------------------------------------------------------
def main(argv=None):

    # pegue argumentos da linha de comando
    if argv == None:
        argv = sys.argv # apelido para os argumentos
        
    # pegue o nome de programa    
    nome_programa = argv[0]
    
    # deve ter apenas um argumento na linha
    argc = len(argv)
    if argc != 2:
        help(nome_programa)
        return None

    # crie dicionario com as disciplinas obrigatórias
    obrigatorias = crie_dicionario(OBRIGATORIAS)

    # crie dicionario com as disciplinas que implicam em dispensa automática
    dispensas = crie_dicionario(DISPENSAS_AUTOMATICAS)

    # crie dicionário com as optativas de ciência
    opt_ciencias = crie_dicionario(CIENCIAS)
    
    # crie dicionário com as optativas de estatística e probabilidade
    opt_estat_prob = crie_dicionario(ESTAT_PROB)
    
    # crie dicionário com as optativas eletivas
    opt_eletivas = crie_dicionario(ELETIVAS)

    # crie dicionário com as optativas livres: no momento so MAC0335
    opt_livres = crie_dicionario(LIVRES)
    
    # pegue o nome do arquivo com as siglas das disciplnas cursadas
    nome_arq = argv[1]

    # pegue as disciplinas cursadas do arquivo
    disc_cursadas = leia_disciplinas(nome_arq)

    # se ocorreu algum problema, abandone execução.
    if disc_cursadas == None: return None

    #------------------------------------------------------------------
    # registre discipinas cursadas nas categorias
    disc_desconhecidas = []
    for sigla in disc_cursadas:
        if sigla in obrigatorias:
            obrigatorias[sigla] = True
        elif sigla in dispensas:
            dispensas[sigla] = True
        elif sigla in opt_ciencias:
            opt_ciencias[sigla] = True
        elif sigla in opt_estat_prob:
            opt_estat_prob[sigla] = True
        elif sigla in opt_eletivas:
            opt_eletivas[sigla] = True
        elif sigla in opt_livres:
            opt_livres[sigla] = True
        else:
           disc_desconhecidas.append(sigla)

    #---------------------------------------------------------------------------       
    # realize dispensas
    for disciplina in DISPENSAS_AUTOMATICAS:
        sigla      = disciplina[SIGLA]
        dispensada = disciplina[-1] 
        if dispensas[sigla]:
            if sigla == "MAT0139": # hard coded
                obrigatorias["MAT0112"] = obrigatorias["MAT0122"] = True
            elif sigla in ["MAE0121", "MAE0212"]:
                pass # vamos tratar logo abaixo
            elif sigla == "4310137":
                opt_ciencias["4302112"] = True
            else:
                obrigatorias[dispensada] = True

    # remendo feio
    # print("AVISO: dispensa de MAE0119 exige aprovação em MAE0121 e MAE0212.")
    if dispensas["MAE0121"] and dispensas["MAE0212"]:
        obrigatorias["MAE0119"] = True

        
                
    #----------------------------------------------------------------
    # contabilize créditos em optativas
    
    # contabilize créditos em optativas em ciências
    creditos_ciencias = 0
    for disciplina in CIENCIAS:
        sigla = disciplina[SIGLA]
        if opt_ciencias[sigla]:
            creditos_ciencias += disciplina[CRED_AULA] \
                                 + disciplina[CRED_TRAB]
        # Hmmm aqui tem um ERRO.
        # Vamos deixar para corrigr quando alguém reclamar.
        # Se um aluno cursar várias disciplinas de ciências devesse,
        # a partir de um ponto, contabilizar créditos como eletivas.
        # Digamos que depois que o pote de ciências
        # estiver cheio, todos os créditos devem ir para eletiva.
            

    # contabilize créditos em optativas estatística e probabilidade
    creditos_estat_prob = 0
    for disciplina in ESTAT_PROB:
        sigla = disciplina[SIGLA]
        if opt_estat_prob[sigla]:
            creditos_estat_prob += disciplina[CRED_AULA] \
                                   + disciplina[CRED_TRAB]
        # Hmmm aqui tem um erro.
        # Vamos deixar para corrigr quando alguém reclamar.
        # Se um aluno cursar várias disciplinas de MAE devemos,
        # a partir de um ponto, contabilizar creditos como eletivas.
        # Digamos que depois que o pote de estatística/probabilidade
        # estiver cheio, todos os créditos devem ir para eletiva.

    # contabilize créditos em optativas eletivas
    creditos_eletivas = 0
    for disciplina in ELETIVAS:
        sigla = disciplina[SIGLA]
        if opt_eletivas[sigla]:
            creditos_eletivas += disciplina[CRED_AULA] \
                                 + disciplina[CRED_TRAB]

    # contabilize créditos em optativas livres (hmmm, no momento só tem MAC0335)
    creditos_livres = 0
    for disciplina in LIVRES:
        sigla = disciplina[SIGLA]
        if opt_livres[sigla]:
            creditos_livres += disciplina[CRED_AULA] \
                               + disciplina[CRED_TRAB]
            
        
    # imprima relatório de disciplinas obrigatórias
    print("RELATÓRIO DE DISCIPLINAS CURSADAS")
    print("---------------------------------")
    
    # disciplinas obrigatórias cursadas
    print("\nOBRIGATÓRIAS:")
    print(". . . . . . .")
    if True not in obrigatorias.values():
        print("Nenhuma... Estranho...")
    else:    
        for disciplina in OBRIGATORIAS:
            if obrigatorias[disciplina[SIGLA]]:
                print("%7s %s, %do. sem, %d+%d" %disciplina)
    pause()
    
    # disciplinas que produzem dispensa cursadas
    print("\nGERAM DISPENSAS:")
    print(". . . . . . . . .")
    if True not in obrigatorias.values():
        print("Nenhuma...")
    else:    
        for disciplina in DISPENSAS_AUTOMATICAS:
            if dispensas[disciplina[SIGLA]]:
                print("%7s %s, %d+%d, dispensa %s" %disciplina)
    pause()
    
    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS DE CIÊNCIAS:")
    print(". . . . . . . . . . . . . .")
    if creditos_ciencias == 0:
        print("Nenhuma...")
    else:      
        for disciplina in CIENCIAS:
            if opt_ciencias[disciplina[SIGLA]]:
                print("%7s %s, %d+%d" %disciplina)
    pause()
    
    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS DE ESTATÍSTICA/PROBABILIDADE:")
    print(". . . . . . . . . . . . . .")
    if creditos_estat_prob == 0:
        print("Nenhuma...")
    else:      
        for disciplina in ESTAT_PROB:
            if opt_estat_prob[disciplina[SIGLA]]:
                print("%7s %s, %d+%d" %disciplina)
    pause()


    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS ELETIVAS:")
    print(". . . . . . . . . . ")
    if creditos_eletivas == 0:
        print("Nenhuma...")
    else:      
        for disciplina in ELETIVAS:
            if opt_eletivas[disciplina[SIGLA]]:
                print("%7s %s, %d+%d" %disciplina)
    pause()

    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS LIVRES:")
    print(". . . . . . . . . . ")
    if creditos_livres == 0:
        print("Nenhuma...")
    else:      
        for disciplina in LIVRES:
            if opt_livres[disciplina[SIGLA]]:
                print("%7s %s, %d+%d" %disciplina)
    pause()


    # mostre lista de disciplinas não encontradas
    print("\nDISCIPLINAS NAO ENCONTRADAS:")
    print(". . . . . . . . . . . . . . .")
    for sigla in disc_desconhecidas:
        print(sigla, end = " ")
    print()    
    pause()    

    # imprima relatório de disciplinas obrigatórias 
    print("\nRELATÓRIO DE DISCIPLINAS A SEREM CURSADAS NO CURRÍCULO 45052")
    print("============================================================")
            
    # disciplinas obrigatorias que ainda precisam ser cursadas
    print("\nOBRIGATÓRIAS:")
    print(". . . . . . .")
    for disciplina in OBRIGATORIAS:
        if not obrigatorias[disciplina[SIGLA]]:
            print("%7s %s, %do. sem, %d+%d" %disciplina)
            
    # for sigla in obrigatorias:
    #     if not obrigatorias[sigla]:
    #         print(sigla)

    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS CIÊNCIAS:")
    print(". . . . . . . . . .")
    print("Número mínimo de créditos que devem ser cursados:", CREDITOS_CIENCIAS)
    print("Número de créditos cursados: ", creditos_ciencias)
    if creditos_ciencias > 0:
        print("Disciplinas: ", end="")
        for sigla in opt_ciencias:
            if opt_ciencias[sigla]:
                print(sigla, end=" ")
        print()
        
    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS ESTATÍSTICA/PROBABILIDADE:")
    print(". . . . . . . . . . . . . . . . . . ")
    print("Número mínimo de créditos que devem ser cursados:", CREDITOS_ESTAT_PROB)
    print("Número de créditos cursados: ", creditos_estat_prob)
    if creditos_estat_prob > 0:
        print("Disciplinas: ", end="")
        for sigla in opt_estat_prob:
            if opt_estat_prob[sigla]:
                print(sigla, end=" ")
        print()        

    # disciplinas de ciêcias cursadas
    print("\nOPTATIVAS ELETIVAS E LIVRES:")
    print(". . . . . .  . . . ")
    print("Número mínimo de créditos que devem ser cursados:", CREDITOS_ELETIVAS + CREDITOS_LIVRES)
    print("Número de créditos cursados: ", creditos_eletivas + creditos_livres)
    if creditos_eletivas + creditos_livres > 0:
        print("Disciplinas: ", end="")
        for sigla in opt_eletivas:
            if opt_eletivas[sigla]:
                print(sigla, end=" ")
        for sigla in opt_livres:
            if opt_livres[sigla]:
                print(sigla, end=" ")
        print()
        
    print()            
    print("Não deixe de curtir a nossa página no feiçebuqui.")


    
#==================================================================
# F U N C O E S
#
#-------------------------------------------------------------------    
def crie_dicionario(tabela):
    '''(list) -> dict

    Recebe uma lista em que cada posições tem informações sobre 
    uma disciplina. Em particular, para cada i, tabela[i][SIGLA] 
    contém a sigla da disciplina.

    A função cria e retorna um dicionário em que as chaves são as siglas 
    das disciplinas na tabela e valor correspondente é False.
    '''
    dicio = {} # dicionário vazio

    for disciplina in tabela:
        sigla = disciplina[SIGLA]
        if sigla not in dicio:
            dicio[sigla] = False
        else:
           print("AVISO: crie_dicionario: disciplina '%s' foi duplica." %sigla)
           
    return dicio    


#--------------------------------------------------------------------
def leia_disciplinas(nome_arq):
    '''(str) -> list 

    Recebe o nome nome_arq de um arquivo e cria e retorna uma 
    lista com as siglas de disciplinas contidas no arquivo.
    '''
    # lista que será retornada com as siglas das disciplinas 
    lista_siglas = []
    
    # abra o arquivo com as siglas das disciplinas usadas
    try: 
        cursadas = open(nome_arq, 'r', encoding = 'utf-8')
    except IOError:
        print("ERRO: '%s' não pode ser aberto."%nome_arq)
        help(nome_programa)
        return None

    # leia o arquivo
    for linha in cursadas:
        # pegue as siglas das disciplinas
        lista_siglas.extend(pega_siglas(linha))
        # print(lista_siglas)

    # feche o arquivo             
    cursadas.close()

    return lista_siglas

#--------------------------------------------------------------------
def pega_siglas(s):
    '''(str) -> list

    Recebe um string s e retorna uma lista com todas as palavras 
    em s. Todas as letras na palavra serão convertidas para maiúsculas.

    Tudo que está depois de um símbolo '#' em s será ignorado.

    Pré-condição: a função supõe que as palavras no arquivo correspondem
                  a siglas de disciplinas. 
    '''
    lista = []  # lista  vazia 
    sigla = ''  # string vazio
    for c in s:
        # str.isalnum(): retorna True se todo símbolo em str é uma
        #               letra ou número
        if c.isalnum(): 
            sigla += c   # concatena a nova letra
        elif sigla != '':
            lista.append(sigla.upper())
            sigla = ''
        if c == '#': return lista

    # ponhe, possivelmente, a última sigla na lista
    if sigla != '':
        lista.append(sigla.upper())

    return lista     

#------------------------------------------------------------
def help(nome_programa):
    '''(str) -> None

    Recebe o nome do programa e mostra mensagem que indica como 
    usar o script.
    '''
    msg = "Uso: python3 %s <arq disc>\n" %nome_programa \
          + "     <arq disc> = nome de um arquivo com as siglas das diciplinas\n" \
          + "                  cursadas separadas por um branco.\n" \
          + "     Exemplo de arquivo:\n" \
          + "     # este é um comentário\n" \
          + "     mAc0121  MAT0111 # as siglas podem ser em letra maiúcula ou minúscula\n" \
          + "     mat121 # exemplo de sigla errada, o certo é mat0121\n" \
          + "     mac0335 MAE0228 # fim arquivo.\n"

    print(msg)
        
#------------------------------------------------------------
def pause():
    input("\nTecle ENTER para continuar.")


####################################################################
'''
    Grade curricular do BCC para os ingressantes em 2016.

    http://bcc.ime.usp.br/


    O código do currículo atual do BCC é 45-052 e vale para os alunos
    que ingressaram em 2016 e anos seguintes. Para os alunos que
    ingressaram em anos anteriores e são do curso 45-051 a grade
    curricular é a de 2015.

    Cada disciplina é representada por uma tuple com o seguinte 
    formato:

    (sigla, nome, semestre, créditos aula, créditos trabalho) 

    sendo que 

        disciplina[0] = sigla: str
        disciplina[1] = nome:  str
        disciplina[3] = créditos aula: int
        disciplina[4] = créditos trabalho: int
        disciplina[2] = semestre: int
'''

#-------------------------------------------------------------------------
'''
    Além das disciplinas obrigatórias, cada aluno deve cursar: disciplinas
    optativas eletivas de Estatística/Probabilidade em número suficiente
    para obter pelo menos 4 créditos (isso corresponde, usualmente, à
    disciplina indicada acima); disciplinas optativas eletivas de Ciências
    em número suficiente para obter pelo menos 4 créditos (isso corresponde,
    usualmente, à disciplina indicada acima); disciplinas optativas eletivas
    em número suficiente para obter pelo menos outros 52 créditos (isso
    corresponde, usualmente, a 13 das 19 disciplinas otativas indicadas
    acima); disciplinas optativas livres em número suficiente para obter
    pelos menos outros 24 créditos
'''

CREDITOS_CIENCIAS   = 4

CREDITOS_ESTAT_PROB = 4

CREDITOS_ELETIVAS   = 52

CREDITOS_LIVRES     = 24

#--------------------------------------------------------------------
# indices da sigla, nome, semestre, créditos aula e créditos trabalho
# nas tabelas abaixo.
SIGLA      =  0
NOME       =  1
SEMESTRE   =  2
CRED_AULA  = -2
CRED_TRAB  = -1

#--------------------------------------------------------------------
OBRIGATORIAS = [
    # 1º semestre
    ("MAC0101", "Integração na Universidade e na Profissão",   1, 2, 0),
    ("MAC0105", "Fundamentos de Matemática para a Computação", 1, 4, 0),
    ("MAC0110", "Introdução à Computação",                     1, 4, 0),
    ("MAC0329", "Álgebra Booleana e Circuitos Digitais",       1, 4, 0),
    ("MAT2453", "Cálculo Diferencial e Integral I",            1, 6, 0),
    ("MAT0112", "Vetores e Geometria",                         1, 4, 0),
    #2º semestre
    ("MAC0121", "Algoritmos e Estruturas de Dados I",             2, 4, 0),
    ("MAC0216", "Técnicas de Programação I",                      2, 4, 2),
    ("MAC0239", "Introdução à Lógica e Verificação de Programas", 2, 4, 0),
    ("MAE0119", "Introdução à Probabilidade e à Estatística",     2, 6, 0),
    ("MAT2454", "Cálculo Diferencial e Integral II",              2, 4, 0),
    ("MAT0122", "Álgebra Linear I",                               2, 4, 0),
    # 3º semestre
    ("MAC0102", "Caminhos no Bacharelado em Ciência da Computação", 3, 2, 0),
    ("MAC0209", "Modelagem e Simulação",                       3, 4, 0),
    ("MAC0210", "Laboratório de Métodos Numéricos",                 3, 4, 0),
    ("MAC0323", "Algoritmos e Estruturas de Dados II",              3, 4, 2),
    ("MAT0236", "Funções Diferenciáveis e Séries",                  3, 4, 0),
    # . . .  optativa Estatística/Probabilidade  4+0
    # 4º semestre
    ("MAC0316", "Conceitos Fundamentais de Linguagens de Programação", 4, 4, 0),
    ("MAC0338", "Análise de Algoritmos",                               4, 4, 0),
    ("MAC0422", "Sistemas Operacionais",                               4, 4, 2),
    #. . .  optativa Ciências  4+0
    # 5º semestre
    ("MAC0350", "Introdução ao Desenvolvimento de Sistemas de Software", 5, 4, 2),
    #
    # 7º semestre
    ("FLC0474", "Língua Portuguesa", 7, 3, 0),
    ("MAC0499", "Trabalho de Formatura Supervisionado", 7, 0, 16) # anual
]

#--------------------------------------------------------------------
CIENCIAS = [
    ("4302112", "Física II", 6, 0),
    ("4302401",	"Mecânica Estatística", 4, 0),
    ("GMG0630",	"Elementos de Mineralogia e Petrologia", 4, 0),
    ("0440620", "Geologia Geral", 4, 0),
    ("QBQ0104", "Bioquímica e Biologia Molecular", 4, 0),
    ("QBQ1252", "Bioquímica Metabólica", 4,1),
    ("QBQ1354", "Bioquímica Molecular", 4,1)
]

#--------------------------------------------------------------------
ESTAT_PROB = [
    ("MAE0217", "Estatística Descritiva", 4, 0),
    ("MAE0221", "Probabilidade I", 6, 0),
    ("MAE0228", "Noções de Probabilidade e Processos Estocásticos", 4, 0)    
]

#--------------------------------------------------------------------
ELETIVAS = [
    ("ACH2007", "Engenharia de Sistemas de Informação II", 4, 2),
    ("ACH2028", "Qualidade de Software", 4, 0),
    ("ACH2037", "Métodos Quantitativos Aplicados à Sistemas de Informação", 4, 0),
    ("ACH2038", "Laboratório de Redes de Computadores", 4, 2),
    ("ACH2046", "Soluções de T.I. Baseadas em Software Livre (desativada: 11/03/2014)", 4, 2),
    ("ACH2048", "Redes de Alto Desempenho", 4, 1),
    ("ACH2058", "Elaboração de Projetos (desativada: 11/03/2014)", 4, 0),
    ("ACH2066", "Tópicos Especiais em Bancos de Dados", 4, 2),
    ("ACH2067", "Gestão de Processos de Negócios", 4, 0),
    ("ACH2068", "Avaliação de Desempenho de Sistemas Computacionais", 4, 0),
    ("ACH2076", "Segurança da Informação", 4, 0),
    ("ACH2077", "Soluções Web Baseadas em Software Livre", 4, 2),
    ("ACH2078", "Gestão Empresarial", 4, 0),
    ("ACH2086", "Hipermídia", 4, 2),
    ("ACH2087", "Construção de Compiladores", 4, 2),
    ("ACH2096", "Laboratório de Sistemas Operacionais", 4, 0),
    ("ACH2097", "Análise e Projeto Orientados a Objetos (desativada: 11/03/2014)", 4, 2),
    ("ACH2098", "Web Semântica", 4, 0),
    ("ACH2106", "Projeto Integrado de Sistemas de Informação", 4, 2),
    ("ACH2107", "Desafios de Programação I", 4, 0),
    ("ACH2108", "Desafios de Programação II", 4, 0),
    ("ACH2117", "Computação Gráfica", 4, 0),
    ("ACH2118", "Introdução ao Processamento de Língua Natural", 4, 2),
    ("ACH2127", "Governança de Tecnologia da Informação", 4, 2),
    ("ACH2137", "Tópicos em Planejamento em Inteligência Artificial", 4, 0),
    ("1610041", "Design: História e Projeto", 4, 0),
    ("AUH2803", "Aspectos Conceituais e Estéticos do Design de Interface", 4, 0),
    ("AUP1301", "Tópicos de Design para Ambientes Digitais: Informação, Interface, Interação, Ação e Colaboração", 4, 1),
    ("AUP2409", "Teoria do Design", 4, 0),
    # ("4302112", "Física II", 6, 0), para contar como ciência
    ("4302401", "Mecânica Estatística", 4, 0),
    ("IOF0115", "Modelagem Numérica em Oceanografia", 4, 0),
    ("IOF0255", "Oceanografia por Satélites", 2, 0),
    ("IOF0265", "Técnicas de Visualização e Distribuição de Dados Oceanográficos", 4, 0),
    ("GMG0630", "Elementos de Mineralogia e Petrologia", 4, 0),
    ("0440620", "Geologia Geral", 4, 0),
    ("CJE0642", "Design de Interação para Editoração", 4, 2),
    ("MAC0213", "Atividade Curricular em Comunidade", 0, 4),
    ("MAC0214", "Atividade Curricular em Cultura e Extensão", 0, 4),
    ("MAC0215", "Atividade Curricular em Pesquisa", 0, 4),
    ("MAC0242", "Laboratório de Programação II", 4, 2),
    ("MAC0300", "Métodos Numéricos da Álgebra Linear", 4, 0),
    ("MAC0310", "Matemática Concreta (desativada: 11/03/2014)", 4, 0),
    ("MAC0315", "Programação Linear", 4, 0),
    ("MAC0317", "Algoritmos para Processamento de Áudio, Imagem e Vídeo", 4, 0),
    ("MAC0318", "Introdução à Programação de Robôs Móveis", 4, 0),
    ("MAC0319", "Programação Funcional Contemporânea", 4, 0),
    ("MAC0320", "Introdução à Teoria do Grafos", 4, 0),
    ("MAC0322", "Introdução à Análise de Sistemas", 4, 0),
    ("MAC0325", "Otimização Combinatória", 4, 0),
    ("MAC0326", "Computação, Cibernética e Sistemas Cognitivos", 4, 0),
    ("MAC0327", "Desafios de Programação", 0, 4),
    ("MAC0328", "Algoritmos em Grafos", 4, 0),
    ("MAC0330", "Algoritmos Algébricos (desativada: 11/03/2014)", 4, 0),
    ("MAC0331", "Geometria Computacional", 4, 0),
    ("MAC0332", "Engenharia de Software", 4, 0),
    ("MAC0333", "Armazenamento e Recuperação de Informação", 4, 0),
    # ("MAC0335", "Leitura Dramática", 3, 0), conta apena como livre
    ("MAC0336", "Criptografia para Segurança de Dados", 4, 2),
    ("MAC0337", "Computação Musical", 4, 0),
    ("MAC0339", "Informação, Comunicação e a Sociedade do Conhecimento", 4, 0),
    ("MAC0340", "Laboratório de Engenharia de Software", 4, 2),
    ("MAC0341", "Introdução a Bioinformática", 4, 0),
    ("MAC0342", "Laboratório de Programação eXtrema", 4, 2),
    ("MAC0343", "Programação Semidefinida e Aplicações", 4, 0),
    ("MAC0351", "Algoritmos em Bioinformática", 4, 0),
    ("MAC0375", "Biologia de Sistemas", 4, 0),
    ("MAC0410", "Introdução à Compilação (desativada: 31/10/2005)", 6, 2),
    ("MAC0412", "Organização de Computadores", 4, 0),
    ("MAC0413", "Tópicos de Programação Orientada a Objetos", 4, 2),
    ("MAC0414", "Autômatos, Computabilidade e Complexidade", 4, 0),
    ("MAC0415", "Projeto de Compiladores (desativada: 02/08/2011)", 4, 2),
    ("MAC0416", "Tópicos de Sistemas Distribuídos", 4, 2),
    ("MAC0417", "Visão e Processamento de Imagens", 4, 0),
    ("MAC0418", "Tópicos Especiais de Programação Matemática (desativada: 02/08/2011)", 4, 0),
    ("MAC0419", "Métodos de Otimização em Finanças", 4, 0),
    ("MAC0420", "Introdução à Computação Gráfica", 4, 0),
    ("MAC0421", "Computação Gráfica (desativada: 02/08/2011)", 4, 0),
    ("MAC0423", "Introdução à Teoria da Computabilidade (desativada: 02/08/2011)", 4, 0),
    ("MAC0424", "O Computador na Sociedade e na Empresa", 4, 0),
    ("MAC0425", "Inteligência Artificial", 4, 0),
    ("MAC0426", "Sistemas de Bancos de Dados", 4, 0),
    ("MAC0427", "Programação não-Linear", 4, 0),
    ("MAC0430", "Algoritmos e Complexidade de Computação", 4, 0),
    ("MAC0431", "Introdução à Computação Paralela e Distribuída", 4, 0),
    ("MAC0432", "Processamento Digital de Imagens: Teoria e Aplicações", 4, 0),
    ("MAC0433", "Administração de Sistemas UNIX (desativada: 02/08/2011)", 4, 0),
    ("MAC0434", "Tópicos de Sistemas de Computação", 4, 0),
    ("MAC0435", "Métodos Formais para Especificação e Construção de Programas", 4, 0),
    ("MAC0436", "Tópicos de Matemática Discreta", 4, 0),
    ("MAC0437", "Redes de Dados (desativada: 02/08/2011)", 4, 0),
    ("MAC0438", "Programação Concorrente", 4, 0),
    ("MAC0439", "Laboratório de Bancos de Dados", 4, 0),
    ("MAC0440", "Sistemas de Objetos Distribuídos (desativada: 11/03/2014)", 4, 0),
    ("MAC0441", "Programação Orientada a Objetos", 4, 2),
    ("MAC0442", "Análise Orientada a Objetos (desativada: 02/08/2011)", 4, 0),
    ("MAC0443", "Projeto Orientado a Objetos (desativada: 02/08/2011)", 4, 0),
    ("MAC0444", "Sistemas Baseados em Conhecimento", 4, 0),
    ("MAC0445", "Laboratório de Análise e Projeto Orientado a Objetos (desativada: 02/08/2011)", 0, 6),
    ("MAC0446", "Princípios de Interação Humano-Computador", 4, 0),
    ("MAC0447", "Análise e Reconhecimento de Formas: Teoria e Prática", 4, 0),
    ("MAC0448", "Programação para Redes de Computadores", 4, 0),
    ("MAC0449", "Sistemas Operacionais Distribuídos (desativada: 02/08/2011)", 4, 2),
    ("MAC0450", "Algoritmos de Aproximação", 4, 0),
    ("MAC0451", "Tópicos Especiais em Desenvolvimento para Web", 4, 0),
    ("MAC0452", "Tópicos de Otimização Combinatória", 4, 0),
    ("MAC0453", "Princípios de Pesquisa Operacional e Logística", 4, 0),
    ("MAC0454", "Sistemas de Middleware (desativada: 11/03/2014)", 4, 0),
    ("MAC0455", "Desenvolvimento de Sistemas Colaborativos (desativada: 11/03/2014)", 4, 0),
    ("MAC0456", "Tópicos Especiais em Engenharia de Software", 4, 0),
    ("MAC0457", "Engenharia de Software Empírica", 4, 0),
    ("MAC0458", "Direito e Software", 2, 0),
    ("MAC0459", "Ciência e Engenharia de Dados", 4, 0),
    ("MAC0460", "Aprendizagem Computacional: Modelos, Algoritmos e Aplicações", 4, 0),
    ("MAC0461", "Introdução ao Escalonamento e Aplicações (desativada: 11/03/2014)", 4, 0),
    ("MAC0462", "Sistemas de Middleware Avançados (desativada: 11/03/2014)", 4, 0),
    ("MAC0463", "Computação Móvel", 4, 0),
    ("MAC0464", "Sistemas Humano-Computacionais", 4, 0),
    ("MAC0465", "Biologia Computacional", 4, 0),
    ("MAC0466", "Teoria dos Jogos Algorítmica", 4, 0),
    ("MAC0467", "Empreendedorismo Digital", 4, 2),
    ("MAC0468", "Tópicos em Computação Gráfica", 4, 0),
    ("MAC0470", "Desenvolvimento de Software Livre", 4, 2),
    ("MAE0217", "Estatística Descritiva", 4, 0),
    ("MAE0221", "Probabilidade I", 6, 0),
    ("MAE0224", "Probabilidade II", 4, 0),
    ("MAE0228", "Noções de Probabilidade e Processos Estocásticos", 4, 0),
    ("MAE0311", "Inferência Estatística", 6, 0),
    ("MAE0312", "Introdução aos Processos Estocásticos", 4, 0),
    ("MAE0314", "Análise Estatística", 4, 0),
    ("MAE0315", "Tecnologia da Amostragem", 4, 0),
    ("MAE0325", "Séries Temporais", 4, 0),
    ("MAE0326", "Aplicações de Processos Estocásticos", 4, 0),
    ("MAE0328", "Análise de Regressão", 4, 0),
    ("MAE0330", "Análise Multivariada e Dados", 6, 0),
    ("MAE0515", "Introdução à Teoria dos Jogos", 4, 0),
    ("MAE0532", "Controle Estatístico de Qualidade", 4, 0),
    ("MAP0313", "Cálculo de Diferenças Finitas", 4, 0),
    ("MAP0421", "Simulação", 4, 0),
    ("MAP2001", "Matemática, Arquitetura e Design (desativada: 31/12/2015)", 4, 0),
    ("MAP2210", "Aplicações de Álgebra Linear", 4, 2),
    ("MAP2220", "Fundamentos de Análise Numérica", 4, 2),
    ("MAP2310", "Simulação", 4, 0),
    ("MAP2321", "Técnicas em Teoria de Controle", 4, 2),
    ("MAP2411", "Matemática Industrial I", 4, 0),
    ("MAT0206", "Análise Real", 6, 0),
    ("MAT0213", "Álgebra II (está prestes a ser desativada)", 6, 0),
    ("MAT0222", "Álgebra Linear II", 4, 0),
    ("MAT0223", "Introdução à Teoria dos Números", 4, 0),
    ("MAT0225", "Funções Analíticas", 4, 0),
    ("MAT0234", "Medida e Integração", 4, 0),
    ("MAT0264", "Anéis e Corpos", 4, 0),
    ("MAT0265", "Grupos", 4, 0),
    ("MAT0311", "Cálculo Diferencial e Integral V", 6, 0),
    ("MAT0330", "Teoria dos Conjuntos", 4, 0),
    ("MAT0350", "Introdução aos Fundamentos de Matemática", 4, 0),
    ("MAT0359", "Lógica", 4, 0),
    ("MAT0364", "Teoria de Galois", 4, 0),
    ("0323100", "Introdução à Engenharia Elétrica", 3, 2),
    ("PCS0210", "Redes de Computadores", 4, 0),
    ("PCS0216", "Sistemas de Tempo Real", 4, 0),
    ("PCS2305", "Laboratório Digital I", 4, 0),
    ("PCS2308", "Laboratório Digital II", 4, 0),
    ("PCS2530", "Design e Programação de Games", 4, 1),
    ("PCS2590", "Criação e Administração de Empresas de Computação", 4, 0),
    ("QBQ0102", "Bioquímica e Biologia Molecular", 8, 0),
    ("QBQ0104", "Bioquímica e Biologia Molecular", 4, 0),
    ("QBQ0106", "Bioquímica", 6, 0),
    ("QBQ0116", "Bioquímica: Estrutura de Biomoléculas e Metabolismo", 8, 0),
    ("QBQ0126", "Biologia Molecular", 6, 0),
    ("QBQ0204", "Bioquímica e Biologia Molecular", 8, 0),
    ("QBQ0230", "Bioquímica: Estrutura de Biomoléculas e Metabolismo", 8, 0),
    ("QBQ0250", "Bioquímica: Estrutura de Biomoléculas e Metabolismo", 8, 0),
    ("QBQ0317", "Biologia Molecular", 6, 0),
    ("QBQ1252", "Bioquímica Metabólica", 4, 1),
    ("QBQ1354", "Bioquímica Molecular", 4, 1),
    ("QBQ2453", "Biologia Molecular", 4, 0),
    ("QBQ2457", "Tecnologia do DNA Recombinante", 4, 0),
    ("QBQ2502", "Enzimologia", 2, 0),
    ("QBQ2503", "Expressão Gênica", 2, 0),
    ("QBQ2505", "Biologia Estrutural", 4, 0),
    ("QBQ2507", "Biologia Molecular Computacional", 4, 0),
    ("QBQ2508", "Transporte e Sinalização Celular", 2, 0),
    ("QBQ2509", "Radicais Livres em Sistemas Biológicos", 2, 0),
    # disciplinas a seguir eram obrigatórias no grade 45051 e podem ser computadas
    # como eletivas. As disciplinas da sigla MAC na mesma situação já estão incluídas acima
    ("4310126", "Física I", 6, 0),
    ("MAT0211", "Cálculo Diferencial e Integral III", 6, 0),
    ("MAT0221", "Cálculo Diferencial e Integral IV", 4, 0)
]

#--------------------------------------------------------------------
LIVRES = [
        ("MAC0335", "Leitura Dramática", 3, 0)
]

#--------------------------------------------------------------------
DISPENSAS_AUTOMATICAS = [
    ("MAC0211", "Laboratório de Programação I", 4, 2, "MAC0216"), # dispensa MAC0216
    ("MAC0122", "Princípios de Desenvolvimento de Algoritmos", 4, 0, "MAC0121"), # (cursada até 2014) dispensa MAC0121
    ("MAE0121", "Introdução à Probabilidade e à Estatística I",  4, 0, "MAC0119?"),
    ("MAE0212", "Introdução à Probabilidade e à Estatística II", 4, 0, "MAC0119?"), # MAE0121+MAE0212 dispensam MAE0119
    ("MAT0111", "Cálculo Diferencial e Integral I",  6, 0, "MAT2453"), # dispensa MAT2453
    ("MAT0121", "Cálculo Diferencial e Integral II", 6, 0, "MAT2454"), #dispensa MAT2454 
    ("MAT0138", "Álgebra I para Computação", 4, 0, "MAC0105"), # dispensa MAC0105
    ("MAT0139", "Álgebra Linear para Computação", 6, 0, "MAT0112+MAT0122"), # dispensa MAT0112+MAT0122
    ("4310137", "Física II", 6, 0, "4302112") #  dispensa 4302112 Física II (optativa de ciência)
]

#---------------------------------------------------
if __name__ == "__main__":
    main()
