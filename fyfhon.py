
import ast
import re
import sys


# ============================================================
# FYFHON - Interpretador da linguagem
# ============================================================

INICIO = "FEM-FINDO!"
FIM = "FENHA UM FOM FIA!"
MOSTRAR = "EFCUTA EFFA!"
ATRIBUIR = "É VERFADE QUE"
IGUAL = "É A MEFMA COIFA QUE"
ENTRADA = "FALE MINHA LINFA"
SE = "FICA FENDO IFFO"
SENAO = "NOFFA FINHORA QUE RAIFA!"
ENQUANTO = "ME DE FAFIENCIA!"
PARA = "FAZ DE NOFO!"
ESCOLHER = "FAMO VER QUAL É?"
CASO = "É EFFE"
ENTAO = "ENFÃO FAZ AFFIM"
FIM_BLOCO = "ACABOU A CONVERFA"


# ============================================================
# EXPRESSÕES E VALORES
# ============================================================

FUNCOES = {
    "str": str,
    "int": int,
    "float": float,
    "len": len,
    "abs": abs,
    "round": round,
}


def traduzir_expressao(texto):
    """Traduz operadores FYFHON para operadores de expressão."""

    partes = re.split(
        r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')',
        texto
    )

    substituicoes = [
        (r"\bÉ DIFERENTE DE\b", "!="),
        (r"\bÉ MAIOR OU IGUAL A\b", ">="),
        (r"\bÉ MENOR OU IGUAL A\b", "<="),
        (r"\bÉ IGUAL A\b", "=="),
        (r"\bÉ MAIOR QUE\b", ">"),
        (r"\bÉ MENOR QUE\b", "<"),
        (r"\bE\b", "and"),
        (r"\bOU\b", "or"),
        (r"\bNÃO\b", "not"),
        (r"\bFATO FIRMADO!\b", "True"),
        (r"\bFALSO, FALSO, FALSO!\b", "False"),
    ]

    for i in range(0, len(partes), 2):
        for padrao, novo in substituicoes:
            partes[i] = re.sub(
                padrao, novo, partes[i], flags=re.IGNORECASE
            )

    return "".join(partes)



def avaliar(texto, variaveis):
    texto = texto.strip()

    # Lê uma entrada do usuário.
    if texto.startswith(ENTRADA):
        prompt = texto[len(ENTRADA):].strip()

        if prompt.startswith("(") and prompt.endswith(")"):
            prompt = prompt[1:-1].strip()

        if prompt:
            mensagem = avaliar(prompt, variaveis)
            return input(str(mensagem))

        return input("Digite um valor: ")

    texto = traduzir_expressao(texto)
    arvore = ast.parse(texto, mode="eval")

    permitidos = (
        ast.Expression, ast.Constant, ast.Name, ast.Load,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.Not,
        ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt,
        ast.LtE, ast.Gt, ast.GtE, ast.Call,
    )

    for no in ast.walk(arvore):
        if not isinstance(no, permitidos):
            raise ValueError(f"Expressão não permitida: {texto}")

        if isinstance(no, ast.Name):
            if no.id not in variaveis and no.id not in FUNCOES:
                raise ValueError(f"Variável não definida: {no.id}")

        if isinstance(no, ast.Call):
            if not isinstance(no.func, ast.Name) or no.func.id not in FUNCOES:
                raise ValueError("Função não permitida.")
            if no.keywords:
                raise ValueError("Argumentos nomeados não permitidos.")

    return eval(
        compile(arvore, "<FYFHON>", "eval"),
        {"__builtins__": {}},
        {**FUNCOES, **variaveis},
    )



# ============================================================
# ANALISADOR DE SINTAXE
# ============================================================

class InterpretadorFYFHON:

    def __init__(self, arquivo):
        with open(arquivo, "r", encoding="utf-8-sig") as f:
            self.linhas = [
                linha.strip()
                for linha in f
                if linha.strip() and not linha.strip().startswith("#")
            ]

        self.posicao = 0
        self.variaveis = {}

    def erro(self, mensagem):
        numero = min(self.posicao + 1, len(self.linhas))
        raise SyntaxError(f"Linha {numero}: {mensagem}")

    def atual(self):
        if self.posicao >= len(self.linhas):
            return None
        return self.linhas[self.posicao]

    def consumir(self, esperado=None):
        linha = self.atual()

        if linha is None:
            self.erro("Fim inesperado do arquivo.")

        if esperado is not None and linha != esperado:
            self.erro(f"Esperado '{esperado}', encontrado '{linha}'.")

        self.posicao += 1
        return linha

    def obter_condicao(self, linha, comando):
        resto = linha[len(comando):].strip()

        if not resto.endswith(ENTAO):
            self.erro(f"Esperado '{ENTAO}'.")

        return resto[:-len(ENTAO)].strip()

        
    
    def obter_bloco(self, paradas):
        comandos = []

        while self.atual() is not None:
            linha = self.atual()

            # Para antes do próximo caso ou do fim do bloco.
            if linha in paradas:
                break

            # Um caso pertence exclusivamente ao comando ESCOLHER.
            if linha.startswith(CASO):
                break

            comandos.append(self.ler_comando())

        return comandos


    def ler_comando(self):
        linha = self.atual()

        if linha is None:
            self.erro("Esperado um comando.")

        # Início e encerramento do programa
        if linha == INICIO:
            self.consumir()
            return ("inicio",)

        if linha == FIM:
            self.consumir()
            return ("fim",)

        # Exibição
        if linha.startswith(MOSTRAR):
            self.consumir()
            expressao = linha[len(MOSTRAR):].strip()
            return ("mostrar", expressao)

        # Atribuição de variável
        if linha.startswith(ATRIBUIR):
            self.consumir()
            resto = linha[len(ATRIBUIR):].strip()

            if IGUAL not in resto:
                self.erro(f"Esperado '{IGUAL}'.")

            nome, expressao = resto.split(IGUAL, 1)
            nome = nome.strip()
            expressao = expressao.strip()

            if not re.fullmatch(r"[A-Za-z_]\w*", nome):
                self.erro(f"Nome de variável inválido: {nome}")

            return ("atribuir", nome, expressao)

        # Condição: if / else
        if linha.startswith(SE):
            self.consumir()
            condicao = self.obter_condicao(linha, SE)

            verdadeiro = self.obter_bloco({SENAO, FIM_BLOCO})
            falso = []

            if self.atual() == SENAO:
                self.consumir(SENAO)
                falso = self.obter_bloco({FIM_BLOCO})

            self.consumir(FIM_BLOCO)
            return ("se", condicao, verdadeiro, falso)

        # Repetição while
        if linha.startswith(ENQUANTO):
            self.consumir()
            condicao = self.obter_condicao(linha, ENQUANTO)
            corpo = self.obter_bloco({FIM_BLOCO})
            self.consumir(FIM_BLOCO)
            return ("enquanto", condicao, corpo)

        # Repetição for: de início até fim, inclusive
        if linha.startswith(PARA):
            self.consumir()
            resto = self.obter_condicao(linha, PARA)

            padrao = (
                r"([A-Za-z_]\w*)\s+DE\s+(.+?)\s+ATÉ\s+(.+)"
            )
            resultado = re.fullmatch(
                padrao, resto, flags=re.IGNORECASE
            )

            if not resultado:
                self.erro(
                    "Use: FAZ DE NOFO! i DE 1 ATÉ 5 "
                    "ENFÃO FAZ AFFIM"
                )

            nome, inicio, fim = resultado.groups()
            corpo = self.obter_bloco({FIM_BLOCO})
            self.consumir(FIM_BLOCO)

            return ("para", nome, inicio, fim, corpo)

        # Seleção match / case
        
        if linha.startswith(ESCOLHER):
            self.consumir()
            expressao = self.obter_condicao(linha, ESCOLHER)
            casos = []

            while self.atual() is not None:
                linha_caso = self.atual()

                if linha_caso == FIM_BLOCO:
                    break

                if not linha_caso.startswith(CASO):
                    self.erro("Esperado um caso 'É EFFE'.")

                self.consumir()

                valor = self.obter_condicao(linha_caso, CASO)

                # Lê o corpo do caso até o próximo caso ou fim da seleção.
                corpo = self.obter_bloco({CASO, FIM_BLOCO})
                casos.append((valor, corpo))

            self.consumir(FIM_BLOCO)

            return ("escolher", expressao, casos)

        if linha == SENAO:
            self.erro("NOFFA FINHORA QUE RAIFA! sem um FICA FENDO IFFO.")

        if linha == FIM_BLOCO:
            self.erro("ACABOU A CONVERFA sem bloco aberto.")

        self.erro(f"Comando desconhecido: {linha}")


    # ========================================================
    # EXECUÇÃO DOS COMANDOS
    # ========================================================

    def executar_lista(self, comandos):
        for comando in comandos:
            tipo = comando[0]

            if tipo in ("inicio", "fim"):
                if tipo == "fim":
                    return "fim"
                continue

            if tipo == "mostrar":
                print(avaliar(comando[1], self.variaveis))

            elif tipo == "atribuir":
                _, nome, expressao = comando
                self.variaveis[nome] = avaliar(
                    expressao, self.variaveis
                )

            elif tipo == "se":
                _, condicao, verdadeiro, falso = comando

                if avaliar(condicao, self.variaveis):
                    resultado = self.executar_lista(verdadeiro)
                else:
                    resultado = self.executar_lista(falso)

                if resultado == "fim":
                    return "fim"

            elif tipo == "enquanto":
                _, condicao, corpo = comando
                repeticoes = 0

                while avaliar(condicao, self.variaveis):
                    repeticoes += 1

                    if repeticoes > 100000:
                        raise RuntimeError(
                            "Limite de repetições excedido."
                        )

                    if self.executar_lista(corpo) == "fim":
                        return "fim"

            elif tipo == "para":
                _, nome, inicio, fim, corpo = comando

                primeiro = int(avaliar(inicio, self.variaveis))
                ultimo = int(avaliar(fim, self.variaveis))

                passo = 1 if primeiro <= ultimo else -1

                for valor in range(primeiro, ultimo + passo, passo):
                    self.variaveis[nome] = valor

                    if self.executar_lista(corpo) == "fim":
                        return "fim"

            elif tipo == "escolher":
                _, expressao, casos = comando
                valor_escolhido = avaliar(
                    expressao, self.variaveis
                )

                caso_padrao = None

                for valor, corpo in casos:
                    if valor.strip() == "_":
                        caso_padrao = corpo
                        continue

                    valor_caso = avaliar(valor, self.variaveis)

                    if valor_escolhido == valor_caso:
                        if self.executar_lista(corpo) == "fim":
                            return "fim"
                        break
                else:
                    if caso_padrao is not None:
                        if self.executar_lista(caso_padrao) == "fim":
                            return "fim"

        return None

    def executar(self):
        try:
            programa = self.obter_bloco(set())

            self.executar_lista(programa)

        except (SyntaxError, ValueError, TypeError, NameError,
                ZeroDivisionError, RuntimeError, EOFError) as exc:
            print(f"Erro FYFHON: {exc}")


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Interpretador FYFHON")
        print("Uso: py fyfhon.py arquivo.fyfhon")
        sys.exit(1)

    try:
        interpretador = InterpretadorFYFHON(sys.argv[1])
        interpretador.executar()

    except OSError as exc:
        print(f"Erro ao abrir o arquivo: {exc}")