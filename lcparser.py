# Receives a raw lc string and parses it into a list-tree of terms.

class Parser:
    def __init__(self, rawlc):
        self.rawlc = rawlc
        self.tokens = []
        self.tokenize()
        self.tree = []
        self.parse_full()

    def tokenize(self):
        buff = ''
        for char in self.rawlc:
            if char in [';', '(', ')']:
                if buff:
                    self.tokens.append(buff.strip())
                    buff = ''
                self.tokens.append(char)
            elif char == ' ' and buff:
                self.tokens.append(buff.strip())
                buff = ''
            else:
                buff += char

    def eat_tokens(self, count):
        for i in range(0, count):
            del self.tokens[0]

    def trim_line(self):
        while self.tokens and self.tokens[0] in [')', ';']:
            del self.tokens[0]

    def parse_line(self):
        # general use of parens
        if self.tokens[0] == '(':
            self.eat_tokens(1)
            e = self.parse_line()
            return e
        # fn x =>, LM
        elif self.tokens[0] == 'fn':  # assumes tokens[2] is '=>'
            v = self.tokens[1]
            self.eat_tokens(3)
            return ['LM', v, self.parse_line()]
        # recursion base case
        elif self.tokens[1] in [')', ';']:
            v = self.tokens[0]
            self.eat_tokens(2)
            return ['VA', v]
        # general case
        else:
            v = self.tokens[0]
            self.eat_tokens(1)
            return ['AP', ['VA', v], self.parse_line()]

    def parse_full(self):
        if self.tokens[1] == ':=':  # assumes "var := expn;" syntax
            while self.tokens:
                v = self.tokens[0]
                self.eat_tokens(2)
                e = self.parse_line()  # expn
                if self.tokens and self.tokens[0] != ';':  # to account for bug w/ full-line AP's
                    e2 = self.parse_line()
                    e = ['AP', e, e2]
                self.tree.append(['LM', v, e])
                self.trim_line()
        else:
            self.tree = self.parse_line()  # allows parsing of single line expressions w/out ":=" assignment

    def get_parsed(self):
        return self.tree
