class RENode:
    def __init__(self, _op='', _sy='', _pos=-1, _lc=None, _rc=None, _nullable=False, _fpos=None, _lpos=None):

        self._operator = _op  # '*', '.', '+', 'leaf'
        self._position = _pos  # only for non-^ leaf nodes
        self._lchild = _lc
        self._rchild = _rc  # only for . and +
        self._nullable = _nullable

        if self._operator == 'leaf':
            self._symbol = _sy  # only for leaf nodes
            self._firstpos = {self._position}
            self._lastpos = {self._position}

        elif self._operator == '.':
            self._firstpos = self._lchild._firstpos
            self._lastpos = self._rchild._lastpos

            if self._lchild._nullable:
                self._firstpos = self._firstpos.union(self._rchild._firstpos)

            if self._rchild._nullable:
                self._lastpos = self._lastpos.union(self._lchild._lastpos)

            self._nullable = self._lchild._nullable and self._rchild._nullable

        elif self._operator == '*':
            self._nullable = True
            self._firstpos = self._lchild._firstpos
            self._lastpos = self._lchild._lastpos

        elif self._operator == '+':
            self._firstpos = set().union(self._rchild._firstpos).union(self._lchild._firstpos)
            self._lastpos = set().union(self._rchild._lastpos).union(self._lchild._lastpos)
            self._nullable = self._lchild._nullable or self._rchild._nullable




    def to_string(self, n):
        result = ' ' * n
        if self._operator == 'leaf':
            result += 'SYMBOL: ' + self._symbol
            result += ' NULLABLE=' + str(self._nullable)
            result += ' FIRSTPOS=' + str(self._firstpos)
            result += ' LASTPOS=' + str(self._lastpos) + '\n'
        elif self._operator == '*':
            result += 'OPERATOR: STAR'
            result += ' NULLABLE=' + str(self._nullable)
            result += ' FIRSTPOS=' + str(self._firstpos)
            result += ' LASTPOS=' + str(self._lastpos) + '\n'
            result += self._lchild.to_string(n + 2)
        elif self._operator == '.':
            result += 'OPERATOR: DOT'
            result += ' NULLABLE=' + str(self._nullable)
            result += ' FIRSTPOS=' + str(self._firstpos)
            result += ' LASTPOS=' + str(self._lastpos) + '\n'
            result += self._lchild.to_string(n + 2)
            result += self._rchild.to_string(n + 2)
        elif self._operator == '+':
            result += 'OPERATOR: PLUS'
            result += ' NULLABLE=' + str(self._nullable)
            result += ' FIRSTPOS=' + str(self._firstpos)
            result += ' LASTPOS=' + str(self._lastpos) + '\n'
            result += self._lchild.to_string(n + 2)
            result += self._rchild.to_string(n + 2)
        else:
            result += 'SOMETHING WENT WRONG'
        return result

    def __repr__(self):
        return self.to_string(0)
