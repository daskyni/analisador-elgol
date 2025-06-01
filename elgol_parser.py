import ply.yacc as yacc
from elgol_lexer import tokens, lexer

def p_programa(p):
    '''programa : funcoes_opc principal_opc'''
    p[0] = {
        'funcoes': p[1],
        'principal': p[2]
    }

def p_funcoes_opc(p):
    '''funcoes_opc : funcoes
                   | empty'''
    p[0] = p[1]

def p_funcoes(p):
    '''funcoes : funcao funcoes
               | funcao'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_funcao(p):
    '''funcao : funcao_declaracao comandos_corpo'''
    p[0] = {
        'declaracao': p[1],
        'corpo': p[2]
    }

def p_funcao_declaracao(p):
    '''funcao_declaracao : INTEIRO FUNC_ID ABRE_PAREN parametros_opc FECHA_PAREN PONTO'''
    p[0] = {
        'tipo': 'inteiro',
        'nome': p[2],
        'parametros': p[4]
    }

def p_parametros_opc(p):
    '''parametros_opc : parametros
                      | empty'''
    p[0] = p[1]

def p_parametros(p):
    '''parametros : parametro VIRGULA parametros
                  | parametro'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_parametro(p):
    '''parametro : INTEIRO ID'''
    p[0] = {
        'tipo': 'inteiro',
        'nome': p[2]
    }

def p_principal_opc(p):
    '''principal_opc : comandos_corpo
                     | empty'''
    p[0] = p[1]

def p_comandos_corpo(p):
    '''comandos_corpo : inicio comandos_opc fim'''
    p[0] = {
        'inicio': p[1],
        'comandos': p[2],
        'fim': p[3]
    }

def p_comandos_opc(p):
    '''comandos_opc : comandos
                    | empty'''
    p[0] = p[1]

def p_comandos(p):
    '''comandos : comando comandos
                | comando'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_comando(p):
    '''comando : atribuicao
               | declaracao
               | atribuicao_elgio
               | laco
               | condicional'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : ID ATRIB expressao PONTO'''
    p[0] = ('atribuicao', p[1], p[3])

def p_declaracao(p):
    '''declaracao : INTEIRO ID PONTO'''
    p[0] = ('declaracao', 'inteiro', p[2])

def p_atribuicao_elgio(p):
    '''atribuicao_elgio : ELGIO ATRIB expressao_sem_func PONTO'''
    p[0] = ('atribuicao_elgio', p[3])

def p_laco(p):
    '''laco : ENQUANTO expressao_logica PONTO comandos_corpo'''
    p[0] = ('enquanto', p[2], p[4])

def p_condicional(p):
    '''condicional : SE expressao_logica PONTO entao comandos_corpo senao comandos_corpo'''
    p[0] = ('se', p[2], p[5], p[6], p[7])

def p_expressao_logica(p):
    '''expressao_logica : termo_sem_func operador_logico termo_sem_func'''
    p[0] = ('logico', p[2], p[1], p[3])

def p_operador_logico(p):
    '''operador_logico : MAIOR
                       | MENOR
                       | IGUAL
                       | DIFERENTE'''
    p[0] = p[1]

def p_expressao(p):
    '''expressao : termo operador expressao
                 | termo'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_operador(p):
    '''operador : MAIS
                | MENOS
                | MULT
                | DIV'''
    p[0] = p[1]

def p_termo(p):
    '''termo : ID
             | NUM
             | ZERO
             | chamada_funcao'''
    p[0] = p[1]

def p_chamada_funcao(p):
    '''chamada_funcao : FUNC_ID ABRE_PAREN argumentos_opc FECHA_PAREN'''
    p[0] = ('chamada_funcao', p[1], p[3])

def p_argumentos_opc(p):
    '''argumentos_opc : argumentos
                      | empty'''
    p[0] = p[1]

def p_argumentos(p):
    '''argumentos : termo_sem_func VIRGULA argumentos
                  | termo_sem_func'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expressao_sem_func(p):
    '''expressao_sem_func : termo_sem_func operador expressao_sem_func
                          | termo_sem_func'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_termo_sem_func(p):
    '''termo_sem_func : ID
                      | NUM
                      | ZERO'''
    p[0] = p[1]

def p_inicio(p):
    '''inicio : INICIO PONTO'''
    p[0] = 'INICIO'

def p_fim(p):
    '''fim : FIM PONTO'''
    p[0] = 'FIM'

def p_entao(p):
    '''entao : ENTAO PONTO'''
    p[0] = 'ENTAO'

def p_senao(p):
    '''senao : SENAO PONTO'''
    p[0] = 'SENAO'

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    if p:
        print(f"Erro sintático na linha {p.lineno}")
    else:
        print("Erro de sintaxe")

parser = yacc.yacc()