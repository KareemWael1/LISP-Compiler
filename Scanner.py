from enum import Enum
import re
import graphviz
import time
import imageio
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import tkinter as tk


class TokenType(Enum):  # listing all tokens type

    # List Representation
    OpenParenthesis = 1
    CloseParenthesis = 2

    # Keywords
    Dotimes = 3
    When = 4
    Read = 5
    Write = 6
    Setq = 7
    Cos = 8
    Sin = 9
    Tan = 10
    LogicalTrue = 11
    LogicalFalse = 12

    # Operators
    PlusOp = 13
    MinusOp = 14
    MultiplyOp = 15
    DivideOp = 16
    ModOp = 17
    RemOp = 18
    IncrementOp = 19
    DecrementOp = 20
    GreaterThanOrEqualOp = 21
    LessThanOrEqualOp = 22
    GreaterThanOp = 23
    LessThanOp = 24
    EqualOp = 25
    NotEqualOp = 26

    # Other
    String = 27
    Number = 28
    Identifier = 29
    Error = 30


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

Operators = {"+": TokenType.PlusOp,
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
             "<": TokenType.LessThanOp,
             ">": TokenType.GreaterThanOp,
             "<>": TokenType.NotEqualOp
             }

Tokens = []  # to add tokens to list

keywords_tokenType = [TokenType.OpenParenthesis,
                      TokenType.CloseParenthesis,
                      TokenType.Dotimes,
                      TokenType.When,
                      TokenType.Read,
                      TokenType.Write,
                      TokenType.LogicalFalse,
                      TokenType.Setq,
                      TokenType.Cos,
                      TokenType.Tan,
                      TokenType.LogicalTrue,
                      TokenType.Sin]

operators_tokenType = [TokenType.PlusOp,
                       TokenType.MinusOp,
                       TokenType.MultiplyOp,
                       TokenType.DivideOp,
                       TokenType.ModOp,
                       TokenType.RemOp,
                       TokenType.IncrementOp,
                       TokenType.DecrementOp,
                       TokenType.LessThanOrEqualOp,
                       TokenType.GreaterThanOrEqualOp,
                       TokenType.EqualOp,
                       TokenType.LessThanOp,
                       TokenType.GreaterThanOp]

input_chars = {
    'letter': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
    'digit': '0123456789',
    'operator': '+-*/<=>!&|~%',
    'identifier_operator': '+-*/<=>&_',
    'whitespace': ' \n\t',
    'dot': '.',
    'special_char': '#\')\"(`',
    'double_quote': '"',
    'ALL': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/<=>!&|~% \n\t.#\')(`'
}

Constant_transitions = [
    {'from': 0, 'to': 1, 'chars': input_chars['digit'], 'label': 'digit'},
    {'from': 0, 'to': 4, 'chars': input_chars['dot'], 'label': '.'},
    {'from': 1, 'to': 1, 'chars': input_chars['digit'], 'label': 'digit'},
    {'from': 1, 'to': 2, 'chars': input_chars['dot'], 'label': '.'},
    {'from': 2, 'to': 3, 'chars': input_chars['digit'], 'label': 'digit'},
    {'from': 2, 'to': 4, 'chars': input_chars['dot'], 'label': '.'},
    {'from': 3, 'to': 3, 'chars': input_chars['digit'], 'label': 'digit'},
    {'from': 3, 'to': 4, 'chars': input_chars['dot'], 'label': '.'},
    {'from': 4, 'to': 4, 'chars': input_chars['dot'] + input_chars['digit'], 'label': '. digit'},
]

identifiers_transitions = [
    {'from': 0, 'to': 1, 'chars': input_chars['letter'],
     'label': 'letter'},
    {'from': 0, 'to': 2, 'chars': input_chars['digit'] + input_chars['special_char'] + input_chars['identifier_operator'],
     'label': 'digit special_character +-*/<=>&_'},
    {'from': 1, 'to': 1, 'chars': input_chars['letter'] + input_chars['identifier_operator'] + input_chars['digit'],
     'label': 'letter +-*/<=>&_ digit'},
    {'from': 1, 'to': 2, 'chars': input_chars['special_char'], 'label': 'special_character'},
    {'from': 2, 'to': 2,
     'chars': input_chars['letter'] + input_chars['identifier_operator'] + input_chars['digit'] + input_chars[
         'special_char'], 'label': 'any'},
]

string_transitions = [
    {'from': 0, 'to': 1, 'chars': input_chars['double_quote'], 'label': '"'},
    {'from': 0, 'to': 0, 'chars': input_chars['ALL'], 'label': 'any input'},
    {'from': 1, 'to': 1, 'chars': input_chars['ALL'], 'label': 'any input'},
    {'from': 1, 'to': 2, 'chars': input_chars['double_quote'], 'label': '"'},
    {'from': 2, 'to': 1, 'chars': input_chars['double_quote'], 'label': '"'},
    {'from': 2, 'to': 3, 'chars': input_chars['ALL'], 'label': 'any input'},
    {'from': 3, 'to': 3, 'chars': input_chars['ALL'], 'label': 'any input'}
]

keywords_transition = [
    {'from': 0, 'to': 1, 'chars': 'd', 'label': 'd'},
    {'from': 1, 'to': 2, 'chars': 'o', 'label': 'o'},
    {'from': 2, 'to': 3, 'chars': 't', 'label': 't'},
    {'from': 3, 'to': 4, 'chars': 'i', 'label': 'i'},
    {'from': 4, 'to': 5, 'chars': 'm', 'label': 'm'},
    {'from': 5, 'to': 6, 'chars': 'e', 'label': 'e'},
    {'from': 6, 'to': 7, 'chars': 's', 'label': 's'},
    {'from': 0, 'to': 8, 'chars': 'w', 'label': 'w'},
    {'from': 8, 'to': 9, 'chars': 'h', 'label': 'h'},
    {'from': 9, 'to': 10, 'chars': 'e', 'label': 'e'},
    {'from': 10, 'to': 7, 'chars': 'n', 'label': 'n'},
    {'from': 8, 'to': 11, 'chars': 'r', 'label': 'r'},
    {'from': 11, 'to': 12, 'chars': 'i', 'label': 'i'},
    {'from': 12, 'to': 13, 'chars': 't', 'label': 't'},
    {'from': 13, 'to': 7, 'chars': 'e', 'label': 'e'},
    {'from': 0, 'to': 7, 'chars': ')(', 'label': ')('},
    {'from': 0, 'to': 14, 'chars': 'r', 'label': 'r'},
    {'from': 14, 'to': 15, 'chars': 'e', 'label': 'e'},
    {'from': 15, 'to': 16, 'chars': 'a', 'label': 'a'},
    {'from': 16, 'to': 7, 'chars': 'd', 'label': 'd'},
    {'from': 0, 'to': 17, 'chars': 'n', 'label': 'n'},
    {'from': 17, 'to': 18, 'chars': 'i', 'label': 'i'},
    {'from': 18, 'to': 7, 'chars': 'l', 'label': 'l'},
    {'from': 0, 'to': 19, 'chars': 's', 'label': 's'},
    {'from': 19, 'to': 20, 'chars': 'e', 'label': 'e'},
    {'from': 20, 'to': 21, 'chars': 't', 'label': 't'},
    {'from': 21, 'to': 7, 'chars': 'q', 'label': 'q'},

    {'from': 19, 'to': 25, 'chars': 'i', 'label': 'i'},
    {'from': 25, 'to': 7, 'chars': 'n', 'label': 'n'},
    {'from': 0, 'to': 23, 'chars': 'c', 'label': 'c'},
    {'from': 23, 'to': 24, 'chars': 'o', 'label': 'o'},
    {'from': 24, 'to': 7, 'chars': 's', 'label': 's'},
    {'from': 0, 'to': 26, 'chars': 't', 'label': 't'},
    {'from': 26, 'to': 27, 'chars': 'a', 'label': 'a'},
    {'from': 27, 'to': 7, 'chars': 'n', 'label': 'n'},

    {'from': 0, 'to': 22, 'chars': 'oimehalq', 'label': 'oimehalq'},
    {'from': 1, 'to': 22, 'chars': 'cdtimeswhnralq)(', 'label': 'cdtimeswhnralq)('},
    {'from': 2, 'to': 22, 'chars': 'cdoimeswhnralq)(', 'label': 'cdoimeswhnralq)('},
    {'from': 3, 'to': 22, 'chars': 'cdotmeswhnralq)(', 'label': 'cdotmeswhnralq)('},
    {'from': 4, 'to': 22, 'chars': 'cdotieswhnralq)(', 'label': 'cdotieswhnralq)('},
    {'from': 5, 'to': 22, 'chars': 'cdotimswhnralq)(', 'label': 'cdotimswhnralq)('},
    {'from': 6, 'to': 22, 'chars': 'cdotimewhnralq)(', 'label': 'cdotimewhnralq)('},
    {'from': 8, 'to': 22, 'chars': 'cdotimeswnalq)(', 'label': 'cdotimeswnalq)('},
    {'from': 9, 'to': 22, 'chars': 'cdotimswhnralq)(', 'label': 'cdotimswhnralq)('},
    {'from': 10, 'to': 22, 'chars': 'cdotimeswhralq)(', 'label': 'cdotimeswhralq)('},
    {'from': 11, 'to': 22, 'chars': 'cdotmeswhnralq)(', 'label': 'cdotmeswhnralq)('},
    {'from': 12, 'to': 22, 'chars': 'cdoimeswhnralq)(', 'label': 'cdoimeswhnralq)('},
    {'from': 13, 'to': 22, 'chars': 'cdotimswhnralq)(', 'label': 'cdotimswhnralq)('},
    {'from': 14, 'to': 22, 'chars': 'cdotimswhnralq)(', 'label': 'cdotimswhnralq)('},
    {'from': 15, 'to': 22, 'chars': 'cdotimeswhnrlq)(', 'label': 'cdotimeswhnrlq)('},
    {'from': 16, 'to': 22, 'chars': 'cotimeswhnralq)(', 'label': 'cotimeswhnralq)('},
    {'from': 17, 'to': 22, 'chars': 'cdotmeswhnralq)(', 'label': 'cdotmeswhnralq)('},
    {'from': 18, 'to': 22, 'chars': 'cdotimeswhnraq)(', 'label': 'cdotimeswhnraq)('},
    {'from': 19, 'to': 22, 'chars': 'cdotmswhnralq)(', 'label': 'cdotmswhnralq)('},
    {'from': 20, 'to': 22, 'chars': 'cdoimeswhnralq)(', 'label': 'cdoimeswhnralq)('},
    {'from': 21, 'to': 22, 'chars': 'cdotimeswhnral)(', 'label': 'cdotimeswhnral)('},

    {'from': 25, 'to': 22, 'chars': 'cdotimeswhralq)(', 'label': 'cdotimeswhralq)('},
    {'from': 23, 'to': 22, 'chars': 'cdtimeswhnralq)(', 'label': 'cdtimeswhnralq)('},
    {'from': 24, 'to': 22, 'chars': 'cdotimewhnralq)(', 'label': 'cdotimewhnralq)('},
    {'from': 27, 'to': 22, 'chars': 'cdotimeswhralq)(', 'label': 'cdotimeswhralq)('},

    {'from': 22, 'to': 22, 'chars': 'dotimeswhnralq)(', 'label': 'dotimeswhnralq)('},
    {'from': 7, 'to': 7, 'chars': ')(', 'label': ')('},
    {'from': 7, 'to': 1, 'chars': 'd', 'label': 'd'},
    {'from': 7, 'to': 8, 'chars': 'w', 'label': 'w'},
    {'from': 7, 'to': 14, 'chars': 'r', 'label': 'r'},
    {'from': 7, 'to': 17, 'chars': 'n', 'label': 'n'},
    {'from': 7, 'to': 19, 'chars': 's', 'label': 's'},
    {'from': 7, 'to': 23, 'chars': 'c', 'label': 'c'},
    {'from': 7, 'to': 26, 'chars': 't', 'label': 't'},
    {'from': 7, 'to': 22, 'chars': 'oimehalq', 'label': 'oimehalq'},

    {'from': 26, 'to': 7, 'chars': ')(', 'label': ')('},
    {'from': 26, 'to': 1, 'chars': 'd', 'label': 'd'},
    {'from': 26, 'to': 8, 'chars': 'w', 'label': 'w'},
    {'from': 26, 'to': 14, 'chars': 'r', 'label': 'r'},
    {'from': 26, 'to': 17, 'chars': 'n', 'label': 'n'},
    {'from': 26, 'to': 19, 'chars': 's', 'label': 's'},
    {'from': 26, 'to': 23, 'chars': 'c', 'label': 'c'},
    {'from': 26, 'to': 26, 'chars': 't', 'label': 't'},
    {'from': 26, 'to': 22, 'chars': 'oimehalq', 'label': 'oimehalq'},
]

operators_transitions = [
    {'from': 0, 'to': 1, 'chars': 'i', 'label': 'i'},
    {'from': 1, 'to': 2, 'chars': 'n', 'label': 'n'},
    {'from': 2, 'to': 5, 'chars': 'c', 'label': 'c'},
    {'from': 5, 'to': 6, 'chars': 'f', 'label': 'f'},
    {'from': 0, 'to': 3, 'chars': 'd', 'label': 'd'},
    {'from': 3, 'to': 4, 'chars': 'e', 'label': 'e'},
    {'from': 4, 'to': 5, 'chars': 'c', 'label': 'c'},
    {'from': 0, 'to': 7, 'chars': 'm', 'label': 'm'},
    {'from': 7, 'to': 8, 'chars': 'o', 'label': 'o'},
    {'from': 8, 'to': 6, 'chars': 'd', 'label': 'd'},
    {'from': 0, 'to': 9, 'chars': 'r', 'label': 'r'},
    {'from': 9, 'to': 10, 'chars': 'e', 'label': 'e'},
    {'from': 10, 'to': 6, 'chars': 'm', 'label': 'm'},
    {'from': 0, 'to': 6, 'chars': '+-*/=><', 'label': '+-*/=><'},
    {'from': 0, 'to': 11, 'chars': 'oencf', 'label': 'oencf'},
    {'from': 1, 'to': 11, 'chars': '+-*/<=>modreicf', 'label': '+-*/<=>modreicf'},
    {'from': 2, 'to': 11, 'chars': '+-*/<=>modreinf', 'label': '+-*/<=>modreinf'},
    {'from': 3, 'to': 11, 'chars': '+-*/<=>modrincf', 'label': '+-*/<=>modrincf'},
    {'from': 4, 'to': 11, 'chars': '+-*/<=>modreinf', 'label': '+-*/<=>modreinf'},
    {'from': 5, 'to': 11, 'chars': '+-*/<=>modreinc', 'label': '+-*/<=>modreinc'},
    {'from': 7, 'to': 11, 'chars': '+-*/<=>mdreincf', 'label': '+-*/<=>mdreincf'},
    {'from': 8, 'to': 11, 'chars': '+-*/<=>moreincf', 'label': '+-*/<=>moreincf'},
    {'from': 9, 'to': 11, 'chars': '+-*/<=>modrincf', 'label': '+-*/<=>modrincf'},
    {'from': 10, 'to': 11, 'chars': '+-*/<=>odreincf', 'label': '+-*/<=>odreincf'},
    {'from': 11, 'to': 11, 'chars': '+-*/<=>modreincf', 'label': '+-*/<=>modreincf'},
    {'from': 6, 'to': 1, 'chars': 'i', 'label': 'i'},
    {'from': 6, 'to': 3, 'chars': 'd', 'label': 'd'},
    {'from': 6, 'to': 7, 'chars': 'm', 'label': 'm'},
    {'from': 6, 'to': 9, 'chars': 'r', 'label': 'r'},
    {'from': 6, 'to': 6, 'chars': '+-*/<=>', 'label': '+-*/<=>'},
    {'from': 6, 'to': 11, 'chars': 'oencf', 'label': 'oencf'},

]

constant_dfa = graphviz.Digraph('G', filename='constant')
identifier_dfa = graphviz.Digraph('g', filename='identifier')
string_dfa = graphviz.Digraph('s', filename='string')
keywords_dfa = graphviz.Digraph('k', filename='keyword')
operators_dfa = graphviz.Digraph('o', filename='operator')

keywords_dfa.attr(size='12,9.5', rankdir='LR', ranksep='0.05', nodesep='0.2')
operators_dfa.attr(size='13,9.5', rankdir='LR', ranksep='0.05', nodesep='0.2')

#  constant dfa
const_accept_states = [1, 3]
const_reject_states = [4]

# identifier dfa
iden_accept_states = [1]
iden_reject_states = [2]

# string dfa
str_accpet_states = [2]
str_reject_states = [3]

# keywords dfa
key_accpet_states = [7, 26]
key_reject_states = [22]

# operator dfa
op_accpet_states = [6]
op_reject_states = [11]


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
        jump = -1
        for i, char in enumerate(text):
            if char == ' ' or char == ')' or char == '(' or char == '\n':
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


def create_dfa(wanted_dfa, wanted_transitions, accept_states, reject_states, st):
    start_state = 0
    wanted_dfa.node(st, shape='rectangle', label="token", labelloc='top', labeljust='center')

    for state in range(max(t['to'] for t in wanted_transitions) + 1):
        shape = 'circle'
        st = str(state)
        color = ''
        style = ''
        if state in accept_states:
            shape = 'doublecircle'
        elif state in reject_states:
            color = 'red'
            style = "filled"
        wanted_dfa.node(st, shape=shape, fillcolor=color, style=style)

    for t in wanted_transitions:
        label = '[' + t['label'] + ']'
        wanted_dfa.edge(str(t['from']), str(t['to']), label=label)


DFA = None
node_colors = {'0': 'white', '1': 'white', '2': 'white', '3': 'white', '4': 'red'}


def get_dfa(t_type):
    if t_type == TokenType.Number:
        DFA = constant_dfa
        node_colors = {'0': 'white', '1': 'white', '2': 'white', '3': 'white', '4': 'red'}
        Transisions = Constant_transitions
        label_node = '5'
    elif t_type == TokenType.Identifier:
        DFA = identifier_dfa
        node_colors = {'0': 'white', '1': 'white', '2': 'red'}
        Transisions = identifiers_transitions
        label_node = '3'
    elif t_type == TokenType.String:
        DFA = string_dfa
        node_colors = {'0': 'white', '1': 'white', '2': 'white', '3': 'red'}
        Transisions = string_transitions
        label_node = '4'
    elif t_type in keywords_tokenType:
        DFA = keywords_dfa
        node_colors = {'0': 'white', '1': 'white', '2': 'white', '3': 'white', '4': 'white', '5': 'white',
                       '6': 'white', '7': 'white', '8': 'white', '9': 'white', '10': 'white', '11': 'white',
                       '12': 'white', '13': 'white', '14': 'white', '15': 'white', '16': 'white', '17': 'white',
                       '18': 'white', '19': 'white', '20': 'white', '21': 'white', '22': 'red', '23': 'white',
                       '24': 'white', '25': 'white', '26': 'white', '27': 'white'}
        Transisions = keywords_transition
        label_node = '28'
    elif t_type in operators_tokenType:
        DFA = operators_dfa
        node_colors = {'0': 'white', '1': 'white', '2': 'white', '3': 'white', '4': 'white', '5': 'white',
                       '6': 'white', '7': 'white', '8': 'white', '9': 'white', '10': 'white', '11': 'red'}
        Transisions = operators_transitions
        label_node = '12'
    else:
        DFA = None
        node_colors = None
        Transisions = None
        label_node = None
    return DFA, node_colors, Transisions, label_node

frames = []


def update(frame):
    frames.clear()
    for token in Tokens:
        DFA, node_colors, Transisions, label_node = get_dfa(token.token_type)
        if DFA == None:
            break
        start_state = 0
        current_state = start_state
        for state, color in node_colors.items():
            DFA.node(state, fillcolor=color, style='filled')
        chars = token.lex
        DFA.node(label_node, shape='rectangle', label=str(chars))
        for char in chars:
            print(char)
            next_state = None
            for transition in Transisions:
                if transition['from'] == current_state and char in transition['chars']:
                    next_state = transition['to']
                    break

            if next_state is None:
                break

            node_colors[str(current_state)] = 'lightgrey'
            node_colors[str(next_state)] = 'lightblue'

            current_state = next_state

            for state, color in node_colors.items():
                DFA.node(state, fillcolor=color, style='filled')
            img = DFA.render(format='png')
            im = imageio.v2.imread(img)
            frames.append(im)

    return frames


root = tk.Tk()
root.configure(bg='white')
root.title("Lisp Compiler")

input_label = tk.Label(root, text="Enter Input:", bg='white')
input_label.pack()

input_box = tk.Text(root, height=6, width=50, bg = 'lightgray')
input_box.pack()

animation_label = None

already_pressed = False


def scan():
    global already_pressed, frames

    text = input_box.get("1.0", "end-1c")
    tokenize(text)
    for t in Tokens:
        print(t.lex, ",", t.token_type)
    update(0)
    max_shape = np.array(frames[0].shape)
    for frame in frames:
        shape = np.array(frame.shape)
        max_shape = np.maximum(max_shape, shape)

    combined_frames = np.zeros((len(frames), *max_shape[:2], 4), dtype=np.uint8)

    for i, frame in enumerate(frames):
        combined_frames[i, :frame.shape[0], :frame.shape[1], :3] = frame[..., :3]
        combined_frames[i, :frame.shape[0], :frame.shape[1], 3] = 255

    combined_frames = combined_frames[..., :3]
    imageio.mimsave('new.gif', combined_frames, format='GIF', duration=1000)
    Tokens.clear()
    display_animation()


def display_animation():
    global animation_label, already_pressed, frames
    if already_pressed:
        animation_label.destroy()
    animation_label = tk.Label(root, text="Animation")
    animation_label.pack()

    photo_images = []
    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        photo_image = ImageTk.PhotoImage(image)
        photo_images.append(photo_image)

    try:
        current_frame = tk.Label(animation_label, image=photo_images[0])
        current_frame.pack()
    except Exception:
        pass

    def update_image(index):
        try:
            current_frame.configure(image=photo_images[index])
            index = (index + 1) % len(photo_images)
            root.after(1000, update_image, index)
        except Exception:
            pass

    root.after(0, update_image, 1)
    already_pressed = True


tokenize_button = tk.Button(root, text="Tokenize Input", command=scan, bg='lightblue', width=12)
tokenize_button.pack()

create_dfa(constant_dfa, Constant_transitions, const_accept_states, const_reject_states, '5')
create_dfa(identifier_dfa, identifiers_transitions, iden_accept_states, iden_reject_states, '3')
create_dfa(string_dfa, string_transitions, str_accpet_states, str_reject_states, '4')
create_dfa(keywords_dfa, keywords_transition, key_accpet_states, key_reject_states, '28')
create_dfa(operators_dfa, operators_transitions, op_accpet_states, op_reject_states, '12')


# root.mainloop()


def main():
    root.mainloop()


if __name__ == "__main__":
    main()
