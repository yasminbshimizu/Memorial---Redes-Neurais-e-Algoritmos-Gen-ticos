import random

###############################################################################
#                                    Senha                                    #
###############################################################################


def gene_senha(letras_possiveis):
    """Sorteia uma letra.

    Args:
      letras: letras possíveis de serem sorteadas.

    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_senha(tamanho_senha, letras_possiveis):
    """Cria um candidato para o problema da senha.

    Args:
      tamanho_senha: inteiro representando o tamanho da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    candidato = []

    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))

    return candidato


def populacao_senha(tamanho_populacao, tamanho_senha, letras_possiveis):
    """Cria população inicial no problema da senha.

    Args
      tamanho_populacao: tamanho da população.
      tamanho_senha: inteiro representando o tamanho da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_senha(tamanho_senha, letras_possiveis))

    return populacao


def funcao_objetivo_senha(candidato, senha_verdadeira):
    """Computa a funcao objetivo de um candidato no problema da senha.

    Args:
      candidato: um palpite para a senha que você quer descobrir.
      senha_verdadeira: a senha que você está tentando descobrir.

    """
    distancia = 0

    for letra_candidato, letra_senha in zip(candidato, senha_verdadeira):
        num_letra_candidato = ord(letra_candidato)
        num_letra_senha = ord(letra_senha)
        distancia += abs(num_letra_candidato - num_letra_senha)

    return distancia


def funcao_objetivo_pop_senha(populacao, senha_verdadeira):
    """Computa a funcao objetivo de uma populaçao no problema da senha.

    Args:
      populacao: lista contendo os individuos do problema.
      senha_verdadeira: a senha que você está tentando descobrir.

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_senha(individuo, senha_verdadeira))

    return fitness


#########################################################
#               Senha de tamanho variável               #
#########################################################

def tamanho_senha_tvar():
    """Sorteia um tamanho para a senha entre 1 e 30 caracteres no problema da senha de tamanho variável.
    
    """
    tamanho = random.choice(range(1, 31))
    return tamanho

def cria_candidato_senha_tvar(letras_possiveis):
    """Cria um candidato para o problema da senha de tamanho variável.

    Args:
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    candidato = []
    tamanho_senha = tamanho_senha_tvar()

    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))

    return candidato


def populacao_senha_tvar(tamanho_populacao, letras_possiveis):
    """Cria população inicial no problema da senha de tamanho variável.

    Args
      tamanho_populacao: tamanho da população.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_senha_tvar(letras_possiveis))

    return populacao


def funcao_objetivo_senha_tvar(candidato, senha_verdadeira, letras_possiveis):
    """Computa a funcao objetivo de um candidato no problema da senha de tamanho variável.

    Args:
      candidato: um palpite para a senha que você quer descobrir.
      senha_verdadeira: a senha que você está tentando descobrir.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    distancia = 0
    
    tamanho_real = len(senha_verdadeira)
    tamanho_candidato = len(candidato)
    
    tamanho_min = min(tamanho_real, tamanho_candidato)
    
    # metrificando diferentes tamanhos com distâncias
    distancia_tamanho =  10*len(letras_possiveis) + 1 
    dif_tamanhos = abs(tamanho_real-tamanho_candidato)
    distancia += distancia_tamanho*dif_tamanhos  

    for letra_candidato, letra_senha in zip(candidato[:tamanho_min], senha_verdadeira[:tamanho_min]):
        num_letra_candidato = ord(letra_candidato)
        num_letra_senha = ord(letra_senha)
        distancia += abs(num_letra_candidato - num_letra_senha)
    
    return distancia


def funcao_objetivo_pop_senha_tvar(populacao, senha_verdadeira, letras_possiveis):
    """Computa a funcao objetivo de uma populaçao no problema da senha de tamanho variável.

    Args:
      populacao: lista contendo os individuos do problema.
      senha_verdadeira: a senha que você está tentando descobrir.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_senha_tvar(individuo, senha_verdadeira, letras_possiveis))

    return fitness


###############################################################################
#                                   Seleção                                   #
###############################################################################


def selecao_roleta_max(populacao, fitness):
    """Realiza seleção da população pela roleta.

    Args:
      populacao: lista contendo os individuos do problema.
      fitness: lista contendo os valores computados da funcao objetivo.

    """
    selecionados = random.choices(populacao, fitness, k=len(populacao))
    return selecionados


def selecao_torneio_max(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    maximização.

    Args:
      populacao: lista contendo os individuos do problema.
      fitness: lista contendo os valores computados da funcao objetivo.
      tamanho_torneio: quantidade de invíduos que batalham entre si.

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        max_fitness = max(fitness_sorteados)
        indice_max_fitness = fitness_sorteados.index(max_fitness)
        individuo_selecionado = sorteados[indice_max_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema.
      fitness: lista contendo os valores computados da funcao objetivo.
      tamanho_torneio: quantidade de invíduos que batalham entre si.

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


###############################################################################
#                                  Cruzamento                                 #
###############################################################################


def cruzamento_uniforme(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento uniforme.

    Args:
      pai: lista representando um individuo.
      mae: lista representando um individuo.
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento.

    """
    if random.random() < chance_de_cruzamento:
        filho1 = []
        filho2 = []

        for gene_pai, gene_mae in zip(pai, mae):
            if random.choice([True, False]):
                filho1.append(gene_pai)
                filho2.append(gene_mae)
            else:
                filho1.append(gene_mae)
                filho2.append(gene_pai)

        return filho1, filho2
    else:
        return pai, mae


def cruzamento_ponto_simples(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto simples.

    Args:
      pai: lista representando um individuo.
      mae: lista representando um individuo.
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento.

    """
    if random.random() < chance_de_cruzamento:
        corte = random.randint(1, len(mae) - 1)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2
    else:
        return pai, mae

    
def cruzamento_ponto_duplo(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto duplo.

    Args:
      pai: lista representando um individuo.
      mae: lista representando um individuo.
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento.

    """
    if random.random() < chance_de_cruzamento:
        corte1 = random.randint(1, len(mae) - 2)
        corte2 = random.randint(corte1 + 1, len(mae) - 1)
        filho1 = pai[:corte1] + mae[corte1:corte2] + pai[corte2:]
        filho2 = mae[:corte1] + pai[corte1:corte2] + mae[corte2:]
        return filho1, filho2
    else:
        return pai, mae

    
def cruzamento_ponto_variavel(candidato1, candidato2, chance_de_cruzamento):
    """Realiza cruzamento de ponto variável, para candidatos de tamanhos diferentes.

    Args:
      cadidato1: lista representando um individuo.
      candidato2: lista representando um individuo.
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento.

    """
    tamanho1 = len(candidato1)
    tamanho2 = len(candidato2)
    
    if tamanho1 <= tamanho2:
        mae=candidato1
        pai=candidato2
    else:
        mae=candidato2
        pai=candidato1
    
    if tamanho1 == 1 or tamanho2 == 1:
        return pai, mae
    
    elif 1 < tamanho1 <= 5 or 1< tamanho2 <= 5:
        return cruzamento_ponto_simples(pai, mae, chance_de_cruzamento)
    
    else:
        return cruzamento_ponto_duplo(pai, mae, chance_de_cruzamento)


###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto.

    Args:
      populacao: lista contendo os indivíduos do problema.
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação.
      valores_possiveis: lista com todos os valores possíveis dos genes.

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]


def mutacao_simples(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação simples.

    Args:
      populacao: lista contendo os indivíduos do problema.
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação.
      valores_possiveis: lista com todos os valores possíveis dos genes.

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            valores_sorteio = set(valores_possiveis) - set([valor_gene])
            individuo[gene] = random.choice(list(valores_sorteio))

def mutacao_insercao_delecao(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de inserção ou deleção.

    Args:
      populacao: lista contendo os indivíduos do problema.
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação.
      valores_possiveis: lista com todos os valores possíveis dos genes.

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            
            if random.random()<=0.5: #delecao
                individuo = individuo[:gene] + individuo[gene+1:]
                
            else: #insercao
                novo_gene = random.choice(list(valores_possiveis))
                individuo = individuo[:gene] + [novo_gene] + individuo[gene:] 