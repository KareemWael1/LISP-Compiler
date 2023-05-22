from enum import Enum
import re


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
    Setq = 23
    Error = 24
    Number = 25
    Identifier = 26
    Cos = 27
    Sin = 28
    Tan = 29


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
            "nil": TokenType.LogicalFalse,
            "setq": TokenType.Setq,
            "cos": TokenType.Cos,
            "tan": TokenType.Tan,
            "t": TokenType.LogicalTrue,
            "sin": TokenType.Sin
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


def tokenize(text):
    text = text.lower()  # because lisp is case-insensitive
    keywords_regex = '|'.join(re.escape(x) for x in Keywords.keys())
    operators_regex = '|'.join(re.escape(x) for x in Operators.keys())

    constants_regex = r"[0-9]+(\.[0-9]*)?"

    lisp_identifier_regex = r'[a-zA-Z][a-zA-Z0-9]*'
    while text:
        # ignore whitespace
        if text[0].isspace():
            text = text[1:]
            continue

        # remove comments
        if text[0] == ';':
            ending = text.find('\n')
            if ending == -1:
                text = ""
                break
            text = text[ending + 1:]
            continue

        # match brackets
        if text[0] == '(':
            Tokens.append(Token(text[0], TokenType.OpenParenthesis))
            text = text[1:]
            continue
        elif text[0] == ')':
            Tokens.append(Token(text[0], TokenType.CloseParenthesis))
            text = text[1:]
            continue

        # string found
        if text[0] == '"':
            closing = text.find('"', 1)
            if closing == -1:
                Tokens.append(Token(text, TokenType.Error))
                text = ""
            else:
                Tokens.append(Token(text[:closing + 1], TokenType.String))
                text = text[closing + 1:]
            continue

        if not text: break
        # search for reserved words
        keyword_match = re.match(keywords_regex, text)
        if keyword_match and check_end(keyword_match.end(), text):
            Tokens.append(Token(keyword_match.group(), Keywords[keyword_match.group()]))
            text = text[keyword_match.end():]
            continue

        # search for Ops

        op_match = re.match(operators_regex, text)
        if op_match and check_end(op_match.end(), text):
            Tokens.append(Token(op_match.group(), Operators[op_match.group()]))
            text = text[op_match.end():]
            continue

        # search for identifiers
        identifier_match = re.match(lisp_identifier_regex, text)
        if identifier_match and check_end(identifier_match.end(), text):
            Tokens.append(Token(identifier_match.group(), TokenType.Identifier))
            text = text[identifier_match.end():]
            continue

        # search for constants
        constant_match = re.match(constants_regex, text)
        if constant_match and check_end(constant_match.end(), text):
            Tokens.append(Token(constant_match.group(), TokenType.Number))
            text = text[constant_match.end():]
            continue

        # invalid token
        jump = -1  # mafrod akamel l7ad awl space wla law la2eet ")" awa2f???
        for i, char in enumerate(text):
            if char == ' ' or char == ')' or char == '(':
                jump = i
                break

        if jump == -1:
            Tokens.append(Token(text, TokenType.Error))
            text = ""
        else:
            Tokens.append(Token(text[:jump], TokenType.Error))
            text = text[jump:]


def check_end(idx, text):
    if (idx >= len(text) or text[idx] == ' ' or text[
        idx] == '('
            or text[idx] == ')' or text[idx] == '\n'):
        return True
    return False


def main():
    s = """tan x<= x <= 5 <=6 +4 3+3
     )(!@ 12.34(read f 11x) ("ah;med");vsvR \n(nil)\n("";) \n (dotimes (n 111x )\n (write n) (write (* n n)) \"this is a string\" \n (setq x 10)
    \n (> A B) \n (setq 54ght $d) 106t8 ) 12.34 mod /+ 3 44 +5 (* 2 3) 6dr f iden sin 3 cos f + tan 43 setq sin cos tan t when read write dotimes
    """
    tokenize(s)
    for t in Tokens:
        print(t.lex, ",", t.token_type)


if __name__ == "__main__":
    main()
