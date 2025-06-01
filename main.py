from elgol_lexer import lexer
from elgol_parser import parser
import os

def analisar_codigo(codigo):
    lexer.lineno = 1
    lexer.input(codigo)

    tem_erro_lexico = False

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == 'ERRO':
            tem_erro_lexico = True

    if tem_erro_lexico:
        print("Erros léxicos encontrados. Análise sintática não iniciada.")
    else:
        lexer.lineno = 1
        lexer.input(codigo)

        resultado = parser.parse(codigo, lexer=lexer)
        print(resultado)

if __name__ == '__main__':
    # colocar o caminho do arquivo de teste aqui
    caminho_arquivo = os.path.join('exemplos', '1_certo.txt')
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        codigo_exemplo = f.read()
        analisar_codigo(codigo_exemplo)