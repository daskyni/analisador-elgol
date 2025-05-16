import ply.lex as lex
import re

# palavras reservadas
reserved = {'elgio', 'inteiro', 'zero', 'comp', 'enquanto', 'se', 'entao', 'senao', 'inicio', 'fim', 'maior', 'menor', 'igual', 'diferente'}

# lista de tokens
tokens = ['ID', 'FUNC_ID', 'NUM', 'PONTO', 'VIRGULA', 'IGUAL', 'MAIS', 'MENOS', 'MULT', 'DIV', 'ABRE_PAREN', 'FECHA_PAREN', 'ERRO', 'RESERVADA']

# ignora espacos e tabulacoes
t_ignore = ' \t'

# lista de simbolos
symbol_list = []

# funcao para adicionar um simbolo na lista
def add_symbol(value, tipo):
    for s in symbol_list:
        if s['valor'] == value:
            return s['id']
    idx = len(symbol_list) + 1
    symbol_list.append({'id': idx, 'tipo': tipo, 'valor': value})
    return idx

# reconhece ponto
def t_PONTO(t):
    r'\.'
    add_symbol(t.value, 'PONTO')
    return t

# reconhece vírgula
def t_VIRGULA(t):
    r'\,'
    add_symbol(t.value, 'VIRGULA')
    return t

# reconhece sinal de igual
def t_IGUAL(t):
    r'='
    add_symbol(t.value, 'IGUAL')
    return t

# reconhece sinal de mais
def t_MAIS(t):
    r'\+'
    add_symbol(t.value, 'MAIS')
    return t

# reconhece sinal de menos
def t_MENOS(t):
    r'-'
    add_symbol(t.value, 'MENOS')
    return t

# reconhece sinal de multiplicacao
def t_MULT(t):
    r'x'
    add_symbol(t.value, 'MULT')
    return t

# reconhece sinal de divisao
def t_DIV(t):
    r'/'
    add_symbol(t.value, 'DIV')
    return t

# reconhece parentese de abertura
def t_ABRE_PAREN(t):
    r'\('
    add_symbol(t.value, 'ABRE_PAREN')
    return t

# reconhece parentese de fechamento
def t_FECHA_PAREN(t):
    r'\)'
    add_symbol(t.value, 'FECHA_PAREN')
    return t

# reconhece palavras reservadas
def t_RESERVED(t):
    r'^[a-z]+$'
    if t.value in reserved:
        t.type = 'RESERVADA'
        add_symbol(t.value, 'RESERVADA')
    else:
        t.type = 'ERRO'
        add_symbol(t.value, 'ERRO')
    return t

# reconhece funcoes (_ seguido de id)
def t_FUNC_ID(t):
    r'^_[A-Z][a-zA-Z]{2,}$'
    add_symbol(t.value, 'FUNC_ID')
    return t

# reconhece ids
def t_ID(t):
    r'^[A-Z][a-zA-Z]{2,}$'
    if len(t.value) >= 3 and t.value.isalpha() and str(t.value)[0].isupper():
        add_symbol(t.value, 'ID')
        return t
    else:
        t.type = 'ERRO'
        add_symbol(t.value, 'ERRO')
        return t

# reconhece numeros (sem comecar com 0)
def t_NUM(t):
    r'^[0-9]+$'
    if t.value.startswith('0'):
        t.type = 'ERRO'
        add_symbol(t.value, 'ERRO')
    else:
        t.value = int(t.value)
        add_symbol(str(t.value), 'NUM')
    return t

# atualiza o numero da linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# reconhece caracteres invalidos
def t_error(t):
    match = re.match(r'[^\s]+', t.value)
    erro = match.group(0)
    t.type = 'ERRO'
    t.value = erro
    add_symbol(erro, 'ERRO')
    t.lexer.skip(len(erro))
    return t

# cria o analisador lexico
lexer = lex.lex()

# função para encontrar coluna
def find_column(line, token_start, word):
    return line.find(word, token_start)

# funcao para testar o lexer e imprimir os tokens
def test_lexer(code):
    lexer.lineno = 1
    all_lines = code.split('\n')
    line_tokens = [[] for _ in all_lines]

    # adiciona espaco antes e depois das pontuacoes 
    code = re.sub(r'([\,\(\)\.\-\+\=\/])', r' \1 ', code)

    for lineno, line in enumerate(code.splitlines()):
        original_line = line  # linha original sem substituições
        line = re.sub(r'#.*', '', line)
        words = line.split()
        pos = 0  # posição atual para buscar coluna

        for word in words:
            col = find_column(original_line, pos, word)
            pos = col + len(word)  # atualiza a posição

            lexer.input(word)
            tok = lexer.token()
            if tok:
                tok.lineno = lineno + 1
                tok.col = col + 1  # coluna começa em 1
                line_tokens[lineno].append(tok)

    # imprime a tabela de simbolos
    print("\n--- Tabela de Símbolos ---")
    print(f"{'ID':<5}{'Tipo':<12}{'Valor'}")
    for s in symbol_list:
        print(f"{s['id']:<5}{s['tipo']:<12}{s['valor']}")

    # imprime a lista de tokens no formato <tipo, linha, coluna, id>
    print("\n--- Lista de Tokens ---")
    for tokens in line_tokens:
        if tokens:
            for tok in tokens:
                idx = next((s['id'] for s in symbol_list if s['valor'] == str(tok.value)), -1)
                print(f"<{tok.type}, {tok.lineno - 1}, {tok.col}, {idx}>", end=" ")
            print()

# exemplo para teste
teste_elgol = '''
# Linguagem Elgol
# autor Elgio Schlemer
# sem erros
inteiro _Fazalgo (inteiro Fazum, inteiro Fazdois) .
inicio .
   inteiro Lixo .
   
   Lixo = Fazum x Fazdois + zero .
   elgio = Lixo .
fim .

# programa principal, fora de função
# deve começar também com inicio e fim que seriam os
# { e } do C
inicio .
  inteiro Variavel .
  inteiro Teste .
  
  Variavel = zero .
  Teste = 45 x _Fazalgo (45, Variavel) .  
  Variavel = Variavel + 3 - 5 x 2 / 2 + Teste .
fim.
'''

test_lexer(teste_elgol)
