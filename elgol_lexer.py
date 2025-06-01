import ply.lex as lex
import re

reserved = {
    'elgio': 'ELGIO',
    'inteiro': 'INTEIRO',
    'zero': 'ZERO',
    'comp': 'COMP',
    'enquanto': 'ENQUANTO',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'inicio': 'INICIO',
    'fim': 'FIM',
    'maior': 'MAIOR',
    'menor': 'MENOR',
    'igual': 'IGUAL',
    'diferente': 'DIFERENTE'
}

tokens = [
    'ID', 'FUNC_ID', 'NUM', 'PONTO', 'VIRGULA', 'ATRIB', 'MAIS', 'MENOS',
    'MULT', 'DIV', 'ABRE_PAREN', 'FECHA_PAREN', 'ERRO'
] + list(reserved.values())

t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_PONTO(t):
    r'\.'
    return t

def t_VIRGULA(t):
    r'\,'
    return t

def t_ATRIB(t):
    r'='
    return t

def t_MAIS(t):
    r'\+'
    return t

def t_MENOS(t):
    r'-'
    return t

def t_MULT(t):
    r'x'
    return t

def t_DIV(t):
    r'/'
    return t

def t_ABRE_PAREN(t):
    r'\('
    return t

def t_FECHA_PAREN(t):
    r'\)'
    return t

def t_PALAVRA(t):
    r'[^\s\.,\(\)=\+\-/]+'

    text = t.value
    if text in reserved:
        t.type = reserved[text]
        return t
    
    if re.fullmatch(r'_[A-Z][a-zA-Z]{2,}', text):
        t.type = 'FUNC_ID'
        return t
    
    if re.fullmatch(r'[A-Z][a-zA-Z]{2,}', text):
        t.type = 'ID'
        return t
    
    if re.fullmatch(r'[1-9][0-9]*', text):
        t.type = 'NUM'
        t.value = int(text)
        return t

    t.type = 'ERRO'
    print(f"Erro léxico na linha {t.lineno}: palavra inválida '{text}'")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

def t_error(t):
    text = t.value
    t.type = 'ERRO'
    print(f"Erro léxico na linha {t.lineno}: palavra inválida '{text}'")
    return t

lexer = lex.lex()