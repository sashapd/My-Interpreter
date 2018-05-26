from abc import ABC
from tokens import TokenType

class ASTNode(ABC):
    def __init__(self, tokens):
        self._next_node = None
        self._tokens = tokens

    def get_next(self):
        return self._next_node

    def validate(self):
        pass

    def eval(self, memory, functions):
        pass

class ASTBlock(ASTNode):
    def __init__(self, tokens):
        super().__init__(tokens)
        self._nodes  = []
        self._build(tokens)
        self.validate()

    def _get_closing_bracket_index(self, tokens, opening_index, opening, closing):
        bracket_balance = 0
        for i in range(opening_index, len(tokens)):
            if tokens[i].value == opening:
                bracket_balance += 1
            elif tokens[i].value == closing:
                bracket_balance -= 1
            if bracket_balance == 0:
                return i

    def _build(self, tokens):
        statement_beginning = 0
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.SEMICOLON:
                self._nodes.append(ASTStatement(tokens[statement_beginning:i+1]))
                statement_beginning = i + 1
            elif token.type == TokenType.BRACKET and token.value == '{':
                closing_index = self._get_closing_bracket_index(tokens, i, *'{}')
                self._nodes.append(ASTBlock(tokens[i+1:closing_index-1]))
                i = closing_index
            elif token.type == TokenType.WHILE or token.type == TokenType.IF:
                closing_parenth_index = self._get_closing_bracket_index(tokens, i + 1, *'()')
                closing_brace_index = self._get_closing_bracket_index(tokens, closing_parenth_index + 1, *'{}')
                if token.type == TokenType.WHILE:
                    self._nodes.append(ASTWhile(tokens[i+2:closing_parenth_index], tokens[closing_parenth_index+2: closing_brace_index]))
                elif token.type == TokenType.IF:
                    self._nodes.append(ASTIf(tokens[i+2:closing_parenth_index], tokens[closing_parenth_index+2: closing_brace_index]))
                i = closing_brace_index
            i += 1

    def validate(self):
       for node in self._nodes:
           node.validate()

    def eval(self, memory, functions):
        for node in self._nodes:
            node.eval(memory, functions)

class ASTWhile(ASTNode):
    def __init__(self, condition_tokens, block_tokens):
        super().__init__(block_tokens)
        self._condition_node = ASTExpression(condition_tokens)
        self._block = ASTBlock(block_tokens)

    def validate(self):
        return True

    def eval(self, memory, functions):
        while self._condition_node.eval(memory, functions):
            self._block.eval(memory, functions)


class ASTIf(ASTNode):
    def __init__(self, condition_tokens, block_tokens):
        super().__init__(block_tokens)
        self._condition_node = ASTExpression(condition_tokens)
        self._block = ASTBlock(block_tokens)

    def validate(self):
        return True

    def eval(self, memory, functions):
        if self._condition_node.eval(memory, functions):
            self._block.eval(memory, functions)


class ASTStatement(ASTNode):
    def __init__(self, tokens, next_node=None):
        super().__init__(tokens)
        if len(tokens) > 2:
            self.expr = ASTExpression(tokens[:-1])
        else:
            self.expr = ASTValue(tokens[:-1])
        self.next_node = next_node

    def validate(self):
        assert(self._tokens[-1].type == TokenType.SEMICOLON)

    def eval(self, memory, functions):
        return self.expr.eval(memory, functions)


class ASTExpression(ASTNode):
    def __init__(self, tokens):
        super().__init__(tokens)
        self._operators_by_precedence = [
                                   TokenType.ASSIGNMENT,
                                   TokenType.COMPARISON,
                                   TokenType.ADDITION,
                                   TokenType.SUBTRACTION,
                                   TokenType.MULTIPLICATION,
                                   TokenType.DIVISION]

        self._operator_functions = {
            TokenType.ASSIGNMENT: self._op_assignment,
            TokenType.COMPARISON: self._op_comparison,
            TokenType.ADDITION: self._op_addition,
            TokenType.SUBTRACTION: self._op_subtraction,
            TokenType.MULTIPLICATION: self._op_multiplication,
            TokenType.DIVISION: self._op_division
        }
        self._left = None
        self._right = None
        self._operator_type = None
        self._operator = None
        self._build()

    def _build_operand(self, tokens):
        if len(tokens) > 1:
            return ASTExpression(tokens)
        else:
            if self._operator_type == TokenType.ASSIGNMENT and self._left is None:
                return ASTLValue(tokens)
            else:
                return ASTValue(tokens)

    def _build(self):
        if self._tokens[0].value == '(' and self._tokens[-1].value == ')':
            self._tokens = self._tokens[1:-1]

        operator_positions = {}
        parenth_balance = 0
        for i, token in reversed(list(enumerate(self._tokens))):
            if token.type == TokenType.PARENTHESES:
                parenth_balance += 1 if token.value == '(' else -1
            if parenth_balance == 0:
                operator_positions[token.type] = i

        for op in self._operators_by_precedence:
            if op in operator_positions:
                self._operator_type = op
                pos = operator_positions[op]
                self._operator = self._tokens[pos]
                self._left = self._build_operand(self._tokens[:pos])
                self._right = self._build_operand(self._tokens[pos + 1:])
                return

    def validate(self):
        return True

    def eval(self, memory, functions):
        # Declaration
        if len(self._tokens) == 2:
            if self._tokens[1] not in memory:
                if self._tokens[0].value == 'num':
                    memory[self._tokens[1].value] = 0
                elif self._tokens[0].value == 'str':
                    memory[self._tokens[1].value] = ''
            return self._tokens[1].value
        return self._operator_functions[self._operator_type](memory, functions)

    def _op_assignment(self, memory, functions):
        left_val = self._left.eval(memory, functions)
        memory[left_val] = self._right.eval(memory, functions)
        return memory[left_val]

    def _op_comparison(self, memory, functions):
        if self._operator.value == '==':
            return self._left.eval(memory, functions) == self._right.eval(memory, functions)
        elif self._operator.value == '>':
            return self._left.eval(memory, functions) > self._right.eval(memory, functions)
        elif self._operator.value == '<':
            return self._left.eval(memory, functions) < self._right.eval(memory, functions)

    def _op_addition(self, memory, functions):
        return self._left.eval(memory, functions) + self._right.eval(memory, functions)

    def _op_subtraction(self, memory, functions):
        return self._left.eval(memory, functions) - self._right.eval(memory, functions)

    def _op_multiplication(self, memory, functions):
        return self._left.eval(memory, functions) * self._right.eval(memory, functions)

    def _op_division(self, memory, functions):
        return self._left.eval(memory, functions) / self._right.eval(memory, functions)

class ASTValue(ASTNode):
    def __init__(self, tokens):
        super().__init__(tokens)
        assert(len(tokens) == 1)
        self.val = tokens[0]

    def eval(self, memory, functions):
        if self.val.type == TokenType.NUMBER:
            return float(self.val.value)
        elif self.val.type == TokenType.STRING:
            return str(self.val.value[1:-1])
        elif self.val.type == TokenType.NAME:
            return memory[self.val.value]

    def validate(self):
        return True

class ASTLValue(ASTNode):
    def __init__(self, tokens):
        super().__init__(tokens)
        assert(len(tokens) == 1)
        self.val = tokens[0]

    def eval(self, memory, functions):
        return self.val.value

    def validate(self):
        return True


def buildAST(tokens):
    return ASTBlock(list(tokens))