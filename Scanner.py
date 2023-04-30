
from enum import Enum


class TokenType(Enum):  # listing all tokens type

    # List Representation
    OpenParenthesis = 1
    CloseParenthesis = 2

    # Keywords
    Dotimes = 3
    When = 4
    Read = 5
    Write = 6
    LogicalTrue = 7
    LogicalFalse = 8

    # Operators
    Semicolon = 9
    PlusOp = 10
    MinusOp = 11
    MultiplyOp = 12
    DivideOp = 13
    ModOp = 14
    RemOp = 15
    IncrementOp = 16
    DecrementOp = 17
    GreaterThanOrEqualOp = 18
    LessThanOrEqualOp = 19
    EqualOp = 20
    NotEqualOp = 21

    # Other
    String = 22
    Identifier = 23
    Function = 24
    Error = 25


# class token to hold string and token type
class Token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
Keywords = {"(": TokenType.OpenParenthesis,
            ")": TokenType.CloseParenthesis,
            "dotimes": TokenType.Dotimes,
            "when": TokenType.When,
            "read": TokenType.Read,
            "write": TokenType.Write,
            "t": TokenType.LogicalTrue,
            "nil": TokenType.LogicalFalse
            }

Operators = {";": TokenType.Semicolon,
             "+": TokenType.PlusOp,
             "-": TokenType.MinusOp,
             "*": TokenType.MultiplyOp,
             "/": TokenType.DivideOp,
             "mod": TokenType.ModOp,
             "rem": TokenType.RemOp,
             "incf": TokenType.IncrementOp,
             "decf": TokenType.DecrementOp,
             "<=": TokenType.LessThanOrEqualOp,
             ">=": TokenType.GreaterThanOrEqualOp,
             "=": TokenType.EqualOp,
             "<>": TokenType.NotEqualOp
             }

Tokens = []  # to add tokens to list


def find_token(text):
    atoms = text.split()
