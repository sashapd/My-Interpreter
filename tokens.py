import re
from enum import Enum, auto

class TokenType(Enum):
    WHILE = auto()
    IF = auto()
    SEMICOLON = auto()
    NUMBER = auto()
    STRING = auto()
    COMMA = auto()
    BRACKET = auto()
    PARENTHESES = auto()
    COMPARISON = auto()
    ASSIGNMENT = auto()
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    NAME = auto()

class Token:
    def __init__(self, value):
        self.value = value
        self.type = token_type(value)

    def __str__(self):
        return ' {} '.format(str(self.value))

    def __repr__(self):
        return ' {} '.format(str(self.value))

def tokens(chars):
    for value in token_values(chars):
        yield Token(value)

def token_values(chars):
    return re.findall(r'(\w+|".*"|==|<=|>=|[^\s])', chars)

def token_type(token):
    types = {
             r'while': TokenType.WHILE,
             r'if': TokenType.IF,
             r';': TokenType.SEMICOLON,
             r'\d+': TokenType.NUMBER,
             r'".*"': TokenType.STRING,
             r',': TokenType.COMMA,
             r'\{|\}': TokenType.BRACKET,
             r'\(|\)': TokenType.PARENTHESES,
             r'==|<|>|<=|>=': TokenType.COMPARISON,
             r'\=': TokenType.ASSIGNMENT,
             r'\+': TokenType.ADDITION,
             r'\-': TokenType.SUBTRACTION,
             r'\*': TokenType.MULTIPLICATION,
             r'\/': TokenType.DIVISION
             }
    for pattern in types:
        if re.match(pattern, token):
            return types[pattern]
    return TokenType.NAME

