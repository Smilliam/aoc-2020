from enum import Enum
class Tok(Enum):
    INTEGER = '1234567890'
    PLUS    = '+'
    MUL     = '*'
    LPAREN  = '('
    RPAREN  = ')'
    EOF     = 'EOF'

class Token():
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f'Token({self.kind}, {self.value})'

class AST():
    pass

class Num(AST):
    def __init__(self, token):
        self.kind  = 'Num'
        self.token = token
        self.value = token.value

class BinaryOp(AST):
    def __init__(self, op, left, right):
        self.kind  = 'BinaryOp'
        self.op    = op
        self.left  = left
        self.right = right

class Lexer():
    def __init__(self, line):
        self.line = line
        self.pos = 0
        self.current = self.line[0]

    def inc(self):
        self.pos += 1
        if self.pos > len(self.line) - 1:
            self.current = None
        else:
            self.current = self.line[self.pos]

    def skip_space(self):
        while self.current and self.current.isspace():
            self.inc()

    def get_next(self):
        while self.current:
            if self.current.isspace():
                self.skip_space()
                continue

            if self.current.isdigit():
                val = int(self.current)
                self.inc()
                return Token(Tok.INTEGER, val)
            if self.current == Tok.PLUS.value:
                self.inc()
                return Token(Tok.PLUS, '+')
            if self.current == Tok.MUL.value:
                self.inc()
                return Token(Tok.MUL, '*')
            if self.current == Tok.LPAREN.value:
                self.inc()
                return Token(Tok.LPAREN, '(')
            if self.current == Tok.RPAREN.value:
                self.inc()
                return Token(Tok.RPAREN, ')')

        return Token(Tok.EOF, None)

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = lexer.get_next()

    def consume(self, type_to_consume):
        if self.current.kind == type_to_consume:
            self.current = self.lexer.get_next()
        else:
            raise Exception('syntax error')

    def terminal(self):
        token = self.current
        if token.kind == Tok.INTEGER:
            self.consume(Tok.INTEGER)
            return Num(token)
        if token.kind == Tok.LPAREN:
            self.consume(Tok.LPAREN)
            node = self.parse()
            self.consume(Tok.RPAREN)
            return node

    def plus(self):
        node = self.terminal()

        while self.current.kind == Tok.PLUS:
            token = self.current
            self.consume(Tok.PLUS)
            node = BinaryOp(token, node, self.terminal())

        return node;

    def mul(self):
        node = self.plus()

        while self.current.kind == Tok.MUL:
            token = self.current
            self.consume(Tok.MUL)
            node = BinaryOp(token, node, self.plus())

        return node;

    def parse(self):
        return self.mul()

def visit(node):
    if node.kind == 'Num':
        return node.value
    elif node.kind == 'BinaryOp':
        if node.op.kind == Tok.PLUS:
            return visit(node.left) + visit(node.right)
        elif node.op.kind == Tok.MUL:
            return visit(node.left) * visit(node.right)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('in_file', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    in_file = args.in_file
    total = 0
    with open(in_file, 'r') as ff:
        for line in ff:
            line = line.rstrip()
            lexer = Lexer(line)
            parser = Parser(lexer)
            ast = parser.parse()
            val = visit(ast)
            total += val

    print(total)
