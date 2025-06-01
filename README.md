# Compiladores
Trabalho de análise léxica e sintática da linguagem "Elgol".

## Observações
* Colocar diretório do código (.txt) no main.py para testar (exemplos prontos estão na pasta 'exemplos').

* Enquanto existirem erros léxicos no código, o analisador sintático não é iniciado.

* Em algumas situações, pode ser que nem todos os erros sintáticos sejam identificados de primeira, assim que for arrumando os erros, outros vão sendo identificados.

* Se o código estiver sem erros, o parser cria uma árvore sintática (as vezes ele consegue criar mesmo com erros, mas os erros ainda são notificados!).

* Se não for colocado o ponto no final de um comando, o erro sintático vai ser identificado na próxima linha.