import sys


# ==========================================
# VARIÁVEIS GLOBAIS
# ==========================================

variaveis = {}


# ==========================================
# FUNÇÃO PARA OBTER VALORES
# ==========================================

def valor(expressao):

    expressao = expressao.strip()

    # Texto
    if expressao.startswith('"') and expressao.endswith('"'):
        return expressao[1:-1]

    # FALE MINHA LINFA
    # input()
    if expressao == "FALE MINHA LINFA":
        return input("> ")

    # Número inteiro
    try:
        return int(expressao)
    except ValueError:
        pass

    # Número decimal
    try:
        return float(expressao)
    except ValueError:
        pass

    # Verdadeiro
    if expressao == "FATO FIRMADO!":
        return True

    # Falso
    if expressao == "FALSO, FALSO, FALSO!":
        return False

    # Variável
    if expressao in variaveis:
        return variaveis[expressao]

    return expressao


# ==========================================
# COMPARAÇÃO
# ==========================================

def comparar(esquerda, operador, direita):

    esquerda = valor(esquerda)
    direita = valor(direita)

    if operador == "==":
        return esquerda == direita

    if operador == "!=":
        return esquerda != direita

    if operador == ">":
        return esquerda > direita

    if operador == "<":
        return esquerda < direita

    if operador == ">=":
        return esquerda >= direita

    if operador == "<=":
        return esquerda <= direita

    return False


# ==========================================
# ENCONTRAR FIM DO BLOCO
# ==========================================

def encontrar_fim_bloco(linhas, inicio):

    profundidade = 0

    for i in range(inicio, len(linhas)):

        linha = linhas[i].strip()

        # IF
        if linha.startswith("FICA FENDO IFFO"):
            profundidade += 1

        # WHILE
        elif linha.startswith("ME DE FAFIENCIA!"):
            profundidade += 1

        # FOR
        elif linha.startswith("FAZ DE NOFO!"):
            profundidade += 1

        # MATCH
        elif linha.startswith("FAMO VER QUAL É"):
            profundidade += 1

        # Fim de bloco
        elif linha == "ACABOU A CONVERFA":

            profundidade -= 1

            if profundidade == 0:
                return i

    return len(linhas)


# ==========================================
# EXECUTAR BLOCO
# ==========================================

def executar_bloco(linhas):

    i = 0

    while i < len(linhas):

        linha = linhas[i].strip()

        # ==========================================
        # LINHA VAZIA
        # ==========================================

        if not linha:

            i += 1
            continue

        # ==========================================
        # COMENTÁRIO
        # ==========================================

        if linha.startswith("BTW"):

            i += 1
            continue

        # ==========================================
        # FEM-FINDO!
        # Início do programa
        # ==========================================

        elif linha.startswith("FEM-FINDO!"):

            pass

        # ==========================================
        # FENHA UM FOM FIA!
        # Final do programa
        # ==========================================

        elif linha.startswith("FENHA UM FOM FIA!"):

            break

        # ==========================================
        # EFCUTA EFFA!
        # print()
        # ==========================================

        elif linha.startswith("EFCUTA EFFA!"):

            expressao = linha[len("EFCUTA EFFA!"):].strip()

            # Remove parênteses
            if expressao.startswith("(") and expressao.endswith(")"):

                expressao = expressao[1:-1].strip()

            # Concatenação com +
            partes = expressao.split("+")

            resultado = ""

            for parte in partes:

                resultado += str(
                    valor(parte.strip())
                )

            print(resultado)

        # ==========================================
        # É VERFADE QUE
        # Criação de variável
        # ==========================================

        elif linha.startswith("É VERFADE QUE"):

            restante = linha[len("É VERFADE QUE"):].strip()

            partes = restante.split(
                " É A MEFMA COIFA QUE ",
                1
            )

            if len(partes) == 2:

                nome = partes[0].strip()

                valor_variavel = valor(partes[1])

                variaveis[nome] = valor_variavel

        # ==========================================
        # É A MEFMA COIFA QUE
        # Atribuição
        # ==========================================

        elif " É A MEFMA COIFA QUE " in linha:

            partes = linha.split(
                " É A MEFMA COIFA QUE ",
                1
            )

            nome = partes[0].strip()

            novo_valor = valor(partes[1])

            variaveis[nome] = novo_valor

        # ==========================================
        # FALE MINHA LINFA
        # input()
        # ==========================================

        elif linha.startswith("FALE MINHA LINFA"):

            restante = linha[
                len("FALE MINHA LINFA"):
            ].strip()

            nome = restante

            entrada = input("> ")

            variaveis[nome] = entrada

        # ==========================================
        # FICA FENDO IFFO
        # if
        # ==========================================

        elif linha.startswith("FICA FENDO IFFO"):

            condicao = linha[
                len("FICA FENDO IFFO"):
            ].strip()

            # Remove parênteses
            if (
                condicao.startswith("(")
                and condicao.endswith(")")
            ):

                condicao = condicao[1:-1].strip()

            # ----------------------------------
            # Procura ENFÃO FAZ AFFIM
            # ----------------------------------

            j = i + 1

            while j < len(linhas):

                if linhas[j].strip() == "ENFÃO FAZ AFFIM":

                    break

                j += 1

            # ----------------------------------
            # Se não encontrou
            # ----------------------------------

            if j >= len(linhas):

                print(
                    "🦖 ERRO: "
                    "Faltou ENFÃO FAZ AFFIM!"
                )

                break

            # ----------------------------------
            # Procura fim do bloco
            # ----------------------------------

            fim = encontrar_fim_bloco(
                linhas,
                i
            )

            # ----------------------------------
            # Bloco verdadeiro
            # ----------------------------------

            bloco_sim = linhas[
                j + 1:fim
            ]

            bloco_nao = []

            profundidade = 0

            encontrou_else = False

            k = j + 1

            # ----------------------------------
            # Procura ELSE
            # ----------------------------------

            while k < fim:

                atual = linhas[k].strip()

                if atual.startswith(
                    "FICA FENDO IFFO"
                ):

                    profundidade += 1

                elif atual.startswith(
                    "ME DE FAFIENCIA!"
                ):

                    profundidade += 1

                elif atual.startswith(
                    "FAZ DE NOFO!"
                ):

                    profundidade += 1

                elif atual.startswith(
                    "FAMO VER QUAL É"
                ):

                    profundidade += 1

                elif atual == "ACABOU A CONVERFA":

                    profundidade -= 1

                elif (
                    atual ==
                    "NOFFA FINHORA QUE RAIFA!"
                    and profundidade == 0
                ):

                    encontrou_else = True

                    bloco_sim = linhas[
                        j + 1:k
                    ]

                    bloco_nao = linhas[
                        k + 1:fim
                    ]

                    break

                k += 1

            # ----------------------------------
            # Avalia condição
            # ----------------------------------

            partes = condicao.split()

            if len(partes) >= 3:

                esquerda = partes[0]

                operador = partes[1]

                direita = " ".join(
                    partes[2:]
                )

                resultado = comparar(
                    esquerda,
                    operador,
                    direita
                )

                if resultado:

                    executar_bloco(
                        bloco_sim
                    )

                elif encontrou_else:

                    executar_bloco(
                        bloco_nao
                    )

            i = fim

        # ==========================================
        # ME DE FAFIENCIA!
        # while
        # ==========================================

        elif linha.startswith("ME DE FAFIENCIA!"):

            condicao = linha[
                len("ME DE FAFIENCIA!"):
            ].strip()

            if (
                condicao.startswith("(")
                and condicao.endswith(")")
            ):

                condicao = condicao[1:-1].strip()

            # Procura fim
            fim = encontrar_fim_bloco(
                linhas,
                i
            )

            bloco = linhas[
                i + 1:fim
            ]

            # Remove ENFÃO FAZ AFFIM
            if (
                bloco
                and bloco[0].strip()
                == "ENFÃO FAZ AFFIM"
            ):

                bloco = bloco[1:]

            # ----------------------------------
            # Executa enquanto verdadeiro
            # ----------------------------------

            while True:

                partes = condicao.split()

                if len(partes) < 3:

                    break

                esquerda = partes[0]

                operador = partes[1]

                direita = " ".join(
                    partes[2:]
                )

                if not comparar(
                    esquerda,
                    operador,
                    direita
                ):

                    break

                executar_bloco(
                    bloco
                )

            i = fim

        # ==========================================
        # FAZ DE NOFO!
        # for
        # ==========================================

        elif linha.startswith("FAZ DE NOFO!"):

            restante = linha[
                len("FAZ DE NOFO!"):
            ].strip()

            # ----------------------------------
            # Formato:
            #
            # FAZ DE NOFO! i EM range(5)
            # ----------------------------------

            partes = restante.split(
                " EM ",
                1
            )

            if len(partes) != 2:

                print(
                    "🦖 ERRO: "
                    "Sintaxe inválida no "
                    "FAZ DE NOFO!"
                )

                i += 1
                continue

            variavel_for = partes[0].strip()

            sequencia = partes[1].strip()

            # ----------------------------------
            # Procura ENFÃO FAZ AFFIM
            # ----------------------------------

            j = i + 1

            while j < len(linhas):

                if (
                    linhas[j].strip()
                    == "ENFÃO FAZ AFFIM"
                ):

                    break

                j += 1

            if j >= len(linhas):

                print(
                    "🦖 ERRO: "
                    "Faltou ENFÃO FAZ AFFIM!"
                )

                break

            # ----------------------------------
            # Procura fim
            # ----------------------------------

            fim = encontrar_fim_bloco(
                linhas,
                i
            )

            bloco = linhas[
                j + 1:fim
            ]

            # ----------------------------------
            # range()
            # ----------------------------------

            if (
                sequencia.startswith("range(")
                and sequencia.endswith(")")
            ):

                conteudo = sequencia[
                    6:-1
                ].strip()

                valores_range = conteudo.split(",")

                try:

                    valores_range = [
                        int(x.strip())
                        for x in valores_range
                    ]

                    if len(valores_range) == 1:

                        inicio = 0
                        fim_range = valores_range[0]
                        passo = 1

                    elif len(valores_range) == 2:

                        inicio = valores_range[0]
                        fim_range = valores_range[1]
                        passo = 1

                    elif len(valores_range) == 3:

                        inicio = valores_range[0]
                        fim_range = valores_range[1]
                        passo = valores_range[2]

                    else:

                        raise ValueError

                    # ----------------------------------
                    # Executa o FOR
                    # ----------------------------------

                    for numero in range(
                        inicio,
                        fim_range,
                        passo
                    ):

                        variaveis[
                            variavel_for
                        ] = numero

                        executar_bloco(
                            bloco
                        )

                except ValueError:

                    print(
                        "🦖 ERRO: "
                        "Valor inválido no range!"
                    )

            else:

                print(
                    "🦖 ERRO: "
                    "O FAZ DE NOFO! "
                    "atualmente aceita apenas "
                    "range()."
                )

            i = fim

        # ==========================================
        # FAMO VER QUAL É
        # match
        # ==========================================

        elif linha.startswith("FAMO VER QUAL É"):

            expressao = linha[
                len("FAMO VER QUAL É"):
            ].strip()

            # Remove parênteses
            if (
                expressao.startswith("(")
                and expressao.endswith(")")
            ):

                expressao = expressao[1:-1].strip()

            # Valor que será comparado
            valor_match = valor(
                expressao
            )

            # ----------------------------------
            # Procura fim do MATCH
            # ----------------------------------

            fim = encontrar_fim_bloco(
                linhas,
                i
            )

            # ----------------------------------
            # Procura os CASES
            # ----------------------------------

            k = i + 1

            while k < fim:

                atual = linhas[k].strip()

                # Encontrou É EFFE
                if atual.startswith("É EFFE"):

                    caso = atual[
                        len("É EFFE"):
                    ].strip()

                    # Remove parênteses
                    if (
                        caso.startswith("(")
                        and caso.endswith(")")
                    ):

                        caso = caso[1:-1].strip()

                    valor_caso = valor(caso)

                    # ----------------------------------
                    # Encontra início do próximo CASE
                    # ----------------------------------

                    inicio_bloco = k + 1

                    proximo = inicio_bloco

                    while proximo < fim:

                        linha_proxima = (
                            linhas[proximo].strip()
                        )

                        if linha_proxima.startswith(
                            "É EFFE"
                        ):

                            break

                        proximo += 1

                    bloco_caso = linhas[
                        inicio_bloco:proximo
                    ]

                    # ----------------------------------
                    # Verifica se é o caso correto
                    # ----------------------------------

                    if valor_match == valor_caso:

                        executar_bloco(
                            bloco_caso
                        )

                        # Para depois de encontrar
                        # o primeiro caso correspondente
                        break

                    k = proximo

                else:

                    k += 1

            i = fim

        # ==========================================
        # É EFFE
        # case
        # ==========================================

        elif linha.startswith("É EFFE"):

            # O CASE é tratado pelo MATCH
            pass

        # ==========================================
        # ENFÃO FAZ AFFIM
        # início do bloco
        # ==========================================

        elif linha == "ENFÃO FAZ AFFIM":

            pass

        # ==========================================
        # NOFFA FINHORA QUE RAIFA!
        # else
        # ==========================================

        elif linha == "NOFFA FINHORA QUE RAIFA!":

            pass

        # ==========================================
        # ACABOU A CONVERFA
        # fim do bloco
        # ==========================================

        elif linha == "ACABOU A CONVERFA":

            pass

        # ==========================================
        # COMANDO DESCONHECIDO
        # ==========================================

        else:

            print(
                "🦖 Comando não reconhecido:",
                linha
            )

        i += 1


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if len(sys.argv) < 2:

    print(
        "🦖 Focê esqueceu de informar o arquivo!"
    )

    print(
        "Uso: python fyhon.py programa.fyhon"
    )

    sys.exit()


arquivo = sys.argv[1]


# ==========================================
# ABRIR ARQUIVO
# ==========================================

try:

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        linhas = f.readlines()

except FileNotFoundError:

    print(
        "🦖 FALHA! Arquivo não encontrado."
    )

    sys.exit()


# ==========================================
# EXECUTAR
# ==========================================

executar_bloco(linhas)