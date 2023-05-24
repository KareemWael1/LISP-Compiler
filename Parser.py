import Scanner
import tkinter as tk
import pandas
import pandastable as pt
from nltk.tree import *


errors = []


def Program(index):
    productions = [Lists]
    return rule(productions, index, "Program")["node"]


def Lists(index):
    productions = [List, Lists_dash]
    return rule(productions, index, "Lists")


def Lists_dash(index):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, index, False)["node"] != ["error"]:
        productions = [List, Lists_dash]
        return rule(productions, index, "Lists`")
    else:
        out["node"] = Tree("Lists`", ["ε"])
        out["index"] = index
        return out


def List(index):
    productions = [Scanner.TokenType.OpenParenthesis, Content, Scanner.TokenType.CloseParenthesis]
    return rule(productions, index, "List")


def Content(index):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, index, False)["node"] != ["error"]:
        productions = [List]
        return rule(productions, index, "Content")
    elif lookahead([Scanner.TokenType.Dotimes, Scanner.TokenType.When], index):
        productions = [Block]
        return rule(productions, index, "Content")
    elif lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                    Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                    Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                    Scanner.TokenType.MultiplyOp,
                    Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
                    Scanner.TokenType.GreaterThanOrEqualOp,
                    Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp,
                    Scanner.TokenType.EqualOp,
                    Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read,
                    Scanner.TokenType.LogicalTrue,
                    Scanner.TokenType.LogicalFalse], index):
        productions = [Expression]
        return rule(productions, index, "Content")
    else:
        out["node"] = Tree("Content", ["ε"])
        out["index"] = index
        return out


def Block(index):
    out = {}
    if Match(Scanner.TokenType.Dotimes, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Dotimes, Scanner.TokenType.OpenParenthesis, Scanner.TokenType.Identifier,
                       Value, Scanner.TokenType.CloseParenthesis, Lists]
        return rule(productions, index, "Block")
    elif Match(Scanner.TokenType.When, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.When, Scanner.TokenType.OpenParenthesis, Expression,
                       Scanner.TokenType.CloseParenthesis, Lists]
        return rule(productions, index, "Block")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def Expression(index):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                  Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                  Scanner.TokenType.MultiplyOp,
                  Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
                  Scanner.TokenType.GreaterThanOrEqualOp,
                  Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp,
                  Scanner.TokenType.EqualOp,
                  Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read], index):
        productions = [Function]
        return rule(productions, index, "Expression")
    elif Match(Scanner.TokenType.LogicalTrue, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalTrue]
        return rule(productions, index, "Expression")
    elif Match(Scanner.TokenType.LogicalFalse, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalFalse]
        return rule(productions, index, "Expression")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def Function(index):
    out = {}
    if lookahead([Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan], index):
        productions = [UnaryFunction]
        return rule(productions, index, "Function")
    elif lookahead(
            [Scanner.TokenType.Setq, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
             Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
             Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
             Scanner.TokenType.NotEqualOp], index):
        productions = [BinaryFunction]
        return rule(productions, index, "Function")
    elif Match(Scanner.TokenType.Identifier, index, False)["node"] != ["error"]:
        productions = [OtherFunction]
        return rule(productions, index, "Function")
    elif Match(Scanner.TokenType.Read, index, False)["node"] != ["error"]:
        productions = [ReadFunction]
        return rule(productions, index, "Function")
    elif lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp], index):
        productions = [UnaryBinaryFunction]
        return rule(productions, index, "Function")
    elif lookahead(
            [Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
             Scanner.TokenType.DivideOp], index):
        productions = [BinaryMoreFunction]
        return rule(productions, index, "Function")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def ReadFunction(index):
    productions = [Scanner.TokenType.Read, ExtraValue]
    return rule(productions, index, "ReadFunction")


def UnaryFunction(index):
    productions = [UnaryFunctionName, Value]
    return rule(productions, index, "UnaryFunction")


def UnaryBinaryFunction(index):
    productions = [UnaryBinaryOperator, Scanner.TokenType.Identifier, ExtraValue]
    return rule(productions, index, "UnaryBinaryFunction")


def ExtraValue(index):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.OpenParenthesis,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], index):
        productions = [Value]
        return rule(productions, index, "ExtraValue")
    else:
        out["node"] = Tree("ExtraValue", ["ε"])
        out["index"] = index
        return out


def UnaryFunctionName(index):
    out = {}
    if Match(Scanner.TokenType.Write, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Write]
        return rule(productions, index, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Sin, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Sin]
        return rule(productions, index, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Cos, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Cos]
        return rule(productions, index, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Tan, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Tan]
        return rule(productions, index, "UnaryFunctionName")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def BinaryFunction(index):
    out = {}
    if Match(Scanner.TokenType.Setq, index, False)["node"] != ["error"]:
        productions = [SetqFunction]
        return rule(productions, index, "BinaryFunction")
    elif lookahead([Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
                    Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                    Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp,
                    Scanner.TokenType.LessThanOrEqualOp,
                    Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
                    Scanner.TokenType.NotEqualOp], index):
        productions = [BinaryOperatorFunction]
        return rule(productions, index, "BinaryFunction")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def SetqFunction(index):
    productions = [Scanner.TokenType.Setq, Scanner.TokenType.Identifier, Value]
    return rule(productions, index, "SetqFunction")


def BinaryOperatorFunction(index):
    productions = [BinaryOperator, Value, Value]
    return rule(productions, index, "BinaryOperatorFunction")


def OtherFunction(index):
    productions = [Scanner.TokenType.Identifier, Parameters]
    return rule(productions, index, "OtherFunction")


def UnaryBinaryOperator(index):
    out = {}
    if Match(Scanner.TokenType.IncrementOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.IncrementOp]
        return rule(productions, index, "UnaryOperator")
    elif Match(Scanner.TokenType.DecrementOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.DecrementOp]
        return rule(productions, index, "UnaryOperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def BinaryMoreFunction(index):
    productions = [BinaryMoreOperator, Value, Value, Parameters]
    return rule(productions, index, "BinaryMoreFunction")


def BinaryMoreOperator(index):
    out = {}
    if Match(Scanner.TokenType.PlusOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.PlusOp]
        return rule(productions, index, "BinaryMoreOperator")
    elif Match(Scanner.TokenType.MinusOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.MinusOp]
        return rule(productions, index, "BinaryMoreOperator")
    elif Match(Scanner.TokenType.MultiplyOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.MultiplyOp]
        return rule(productions, index, "BinaryMoreOperator")
    elif Match(Scanner.TokenType.DivideOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.DivideOp]
        return rule(productions, index, "BinaryMoreOperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def BinaryOperator(index):
    out = {}
    if Match(Scanner.TokenType.ModOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.ModOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.RemOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.RemOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.GreaterThanOrEqualOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.GreaterThanOrEqualOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.LessThanOrEqualOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LessThanOrEqualOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.GreaterThanOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.GreaterThanOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.LessThanOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LessThanOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.EqualOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.EqualOp]
        return rule(productions, index, "BinaryOperator")
    elif Match(Scanner.TokenType.NotEqualOp, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.NotEqualOp]
        return rule(productions, index, "BinaryOperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def Parameters(index):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.OpenParenthesis,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], index):
        productions = [Value, Parameters_dash]
        return rule(productions, index, "Parameters")
    else:
        out["node"] = Tree("Parameters", ["ε"])
        out["index"] = index
        return out


def Parameters_dash(index):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.OpenParenthesis,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], index):
        productions = [Value, Parameters_dash]
        return rule(productions, index, "Parameters`")
    else:
        out["node"] = Tree("Parameters`", ["ε"])
        out["index"] = index
        return out


def Value(index):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number], index):
        productions = [Atom]
        return rule(productions, index, "Value")
    elif lookahead([Scanner.TokenType.OpenParenthesis], index):
        productions = [Scanner.TokenType.OpenParenthesis, Function, Scanner.TokenType.CloseParenthesis]
        return rule(productions, index, "Value")
    elif Match(Scanner.TokenType.LogicalTrue, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalTrue]
        return rule(productions, index, "Value")
    elif Match(Scanner.TokenType.LogicalFalse, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalFalse]
        return rule(productions, index, "Value")
    elif Match(Scanner.TokenType.String, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.String]
        return rule(productions, index, "Value")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        errors.append("Syntax error : " + F" Expected Value")
        return out


def Atom(index):
    out = {}
    if Match(Scanner.TokenType.Identifier, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Identifier]
        return rule(productions, index, "Atom")
    elif Match(Scanner.TokenType.Number, index, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Number]
        return rule(productions, index, "Atom")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = index
        return out


def is_error(arr):
    return 'mode' in arr[-1].keys() and arr[-1]['mode'] == ['error']


def match_production(arr, match, position, j):
    if callable(match):
        if position == 0:
            arr.append(match(j))
        else:
            arr.append(match(arr[-1]['index']))
    else:
        if position == 0:
            arr.append(Match(match, j))
        else:
            arr.append(Match(match, arr[-1]['index']))
    return arr


def lookahead(Arr, index):
    for i in Arr:
        if Match(i, index, False)["node"] != ["error"]:
            return True
    return False


def rule(productions, index, func_name):
    arr = []
    out = {}
    children = []
    i = 0
    while i < len(productions):
        production = productions[i]
        arr = match_production(arr, production, i, index)
        index = arr[-1]["index"]
        children.append(arr[-1]["node"])
        if is_error(arr):
            while index < len(Scanner.Tokens) and Scanner.Tokens[index].lex != ")":
                index += 1
            arr[-1]["index"] = index
            if Scanner.TokenType.CloseParenthesis in productions[i:]:
                i = productions[i:].index(Scanner.TokenType.CloseParenthesis) + i
                continue
            else:
                out["mode"] = ["error"]
                out["index"] = index
                out["node"] = Tree(func_name, children)
                return out
        index += 1
        i += 1
    out["node"] = Tree(func_name, children)
    out["index"] = arr[-1]["index"]
    return out


def Match(a, j, report=True):
    output = dict()
    if j < len(Scanner.Tokens):
        temp = Scanner.Tokens[j].to_dict()
        if temp["token_type"] == a:
            output["node"] = [temp["Lex"]]
            output["index"] = j + 1
            return output
        else:
            output["mode"] = ["error"]
            output["node"] = ["error"]
            output["index"] = j
            if report:
                errors.append("Syntax error : " + temp["Lex"] + F" Expected {a}")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j
        if report:
            errors.append("Syntax error : " + F" Expected {a}")
        return output


def parse():
    x1 = Scanner.input_box.get("1.0", "end-1c")
    Scanner.tokenize(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Scanner.Tokens])
    # print(df)

    # to display token stream as table
    d_t_da1 = tk.Toplevel()
    d_t_da1.title('Token Stream')
    d_t_da_pt = pt.Table(d_t_da1, dataframe=df, showtoolbar=True, showstatusbar=True)
    d_t_da_pt.show()

    # start Parsing
    node = Program(0)

    # to display error list

    df1 = pandas.DataFrame(errors)
    d_t_da2 = tk.Toplevel()
    d_t_da2.title('Error List')
    d_t_da_pt2 = pt.Table(d_t_da2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    d_t_da_pt2.show()

    Scanner.Tokens.clear()
    errors.clear()
    node.draw()
