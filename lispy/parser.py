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