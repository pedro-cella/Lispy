from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol


class LispTransformer(InlineTransformer):
    def start(self, *args): 
        return [Symbol.BEGIN, *args]  # (begin x1 x2 x3 ...)

    def int(self, i):
        return int(i)

    def float(self, f):
        return float(f)

    def true(self, x):
        return True
 
    def false(self, x):
        return False

    def symbol(self, x):
        return Symbol(x)

    def string(self, x):
        return str(x)[1:-1].replace(r"\n", "\n").replace(r"\t", "\t").replace(r"\"", "\"")

    def list(self, *args): # *args passa um numero nao contabilizado de argumentos, transformando-os numa lista
        return list(args)

    def nested_list(self, *args):
        return list(args)

    def quote(self, x):
        return [Symbol.QUOTE, x]

    def op(self, *args):
        op = [args[1], args[0], args[2]]
        return (op)

    def let(self, *args):
        *expr1, expr2 = args
        d = []
        l = d
        for i in range(0, len(expr1), 2):
            l.append([expr1[i], expr1[i+1]])
        return [Symbol.LET, d, expr2]
    
    def cond_if(self, *args):
        cond, a, b = args
        if cond == True:
            return a
        else:
            return b

    def cond_if(self, x, y, z):
        return list(tuple((Symbol.IF, x, y, z)))

    def cond_if_alt(self, x, y, z):
        return list(tuple((Symbol.IF, x, y, z)))

def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()