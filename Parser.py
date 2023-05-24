import Scanner
import tkinter as tk
import pandas
import pandastable as pt
from nltk.tree import *


errors = []


def Program(ind):
    productions = [Lists]
    return rule(productions, ind, "Program")["node"]


def Lists(ind):
    productions = [List, Lists_dash]
    return rule(productions, ind, "Lists")


def Lists_dash(ind):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, ind, False)["node"] != ["error"]:
        productions = [List, Lists_dash]
        return rule(productions, ind, "Lists`")
    else:
        out["node"] = Tree("Lists`", ["ε"])
        out["index"] = ind
        return out


def List(ind):
    productions = [Scanner.TokenType.OpenParenthesis, Contents, Scanner.TokenType.CloseParenthesis]
    return rule(productions, ind, "List")


def Contents(ind):
    productions = [Content, Contents_dash]
    return rule(productions, ind, "Contents")


def Contents_dash(ind):
    out = {}
    if lookahead([Scanner.TokenType.OpenParenthesis, Scanner.TokenType.Dotimes, Scanner.TokenType.When,
                  Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan,
                  Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                  Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                  Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                  Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
                  Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse], ind):
        productions = [Content, Contents_dash]
        return rule(productions, ind, "Contents`")
    else:
        out["node"] = Tree("Contents`", ["ε"])
        out["index"] = ind
        return out


def Content(ind):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, ind, False)["node"] != ["error"]:
        productions = [List]
        return rule(productions, ind, "Content")
    elif lookahead([Scanner.TokenType.Dotimes, Scanner.TokenType.When], ind):
        productions = [Block]
        return rule(productions, ind, "Content")
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
                    Scanner.TokenType.LogicalFalse], ind):
        productions = [Expression]
        return rule(productions, ind, "Content")
    else:
        out["node"] = Tree("Content", ["ε"])
        out["index"] = ind
        return out


def Block(ind):
    out = {}
    if Match(Scanner.TokenType.Dotimes, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Dotimes, Scanner.TokenType.OpenParenthesis, Scanner.TokenType.Identifier,
                       Scanner.TokenType.Number, Scanner.TokenType.CloseParenthesis, Lists]
        return rule(productions, ind, "Block")
    elif Match(Scanner.TokenType.When, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.When, Scanner.TokenType.OpenParenthesis, Expression,
                       Scanner.TokenType.CloseParenthesis, Lists]
        return rule(productions, ind, "Block")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Expression(ind):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                  Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                  Scanner.TokenType.MultiplyOp,
                  Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
                  Scanner.TokenType.GreaterThanOrEqualOp,
                  Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp,
                  Scanner.TokenType.EqualOp,
                  Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read], ind):
        productions = [Function]
        return rule(productions, ind, "Expression")
    elif Match(Scanner.TokenType.LogicalTrue, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalTrue]
        return rule(productions, ind, "Expression")
    elif Match(Scanner.TokenType.LogicalFalse, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalFalse]
        return rule(productions, ind, "Expression")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Function(ind):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                  Scanner.TokenType.Tan], ind):
        productions = [UnaryFunction]
        return rule(productions, ind, "Function")
    elif lookahead(
            [Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
             Scanner.TokenType.DivideOp,
             Scanner.TokenType.ModOp, Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp,
             Scanner.TokenType.LessThanOrEqualOp,
             Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
             Scanner.TokenType.NotEqualOp], ind):
        productions = [BinaryFunction]
        return rule(productions, ind, "Function")
    elif Match(Scanner.TokenType.Identifier, ind, False)["node"] != ["error"]:
        productions = [OtherFunction]
        return rule(productions, ind, "Function")
    elif Match(Scanner.TokenType.Read, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Read]
        return rule(productions, ind, "Function")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def UnaryFunction(ind):
    out = {}
    if lookahead([Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan], ind):
        productions = [UnaryFunctionName, Value]
        return rule(productions, ind, "UnaryFunction")
    elif lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp], ind):
        productions = [UnaryOperator, Scanner.TokenType.Identifier]
        return rule(productions, ind, "UnaryFunction")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def UnaryFunctionName(ind):
    out = {}
    if Match(Scanner.TokenType.Write, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Write]
        return rule(productions, ind, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Sin, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Sin]
        return rule(productions, ind, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Cos, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Cos]
        return rule(productions, ind, "UnaryFunctionName")
    elif Match(Scanner.TokenType.Tan, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Tan]
        return rule(productions, ind, "UnaryFunctionName")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def BinaryFunction(ind):
    out = {}
    if Match(Scanner.TokenType.Setq, ind, False)["node"] != ["error"]:
        productions = [SetqFunction]
        return rule(productions, ind, "BinaryFunction")
    elif lookahead([Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
                    Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                    Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp,
                    Scanner.TokenType.LessThanOrEqualOp,
                    Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
                    Scanner.TokenType.NotEqualOp], ind):
        productions = [BinaryOperatorFunction]
        return rule(productions, ind, "BinaryFunction")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def SetqFunction(ind):
    productions = [Scanner.TokenType.Setq, Scanner.TokenType.Identifier, Value]
    return rule(productions, ind, "SetqFunction")


def BinaryOperatorFunction(ind):
    productions = [BinaryOperator, Value, Value]
    return rule(productions, ind, "BinaryOperatorFunction")


def OtherFunction(ind):
    productions = [Scanner.TokenType.Identifier, Parameters]
    return rule(productions, ind, "OtherFunction")


def UnaryOperator(ind):
    out = {}
    if Match(Scanner.TokenType.IncrementOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.IncrementOp]
        return rule(productions, ind, "UnaryOperator")
    elif Match(Scanner.TokenType.DecrementOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.DecrementOp]
        return rule(productions, ind, "UnaryOperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def BinaryOperator(ind):
    out = {}
    if Match(Scanner.TokenType.PlusOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.PlusOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.MinusOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.MinusOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.MultiplyOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.MultiplyOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.DivideOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.DivideOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.ModOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.ModOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.RemOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.RemOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.GreaterThanOrEqualOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.GreaterThanOrEqualOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.LessThanOrEqualOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LessThanOrEqualOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.GreaterThanOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.GreaterThanOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.LessThanOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LessThanOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.EqualOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.EqualOp]
        return rule(productions, ind, "BinaryOperator")
    elif Match(Scanner.TokenType.NotEqualOp, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.NotEqualOp]
        return rule(productions, ind, "BinaryOperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Parameters(ind):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.IncrementOp,
                  Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan, Scanner.TokenType.Setq,
                  Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                  Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                  Scanner.TokenType.RemOp,
                  Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                  Scanner.TokenType.GreaterThanOp,
                  Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp,
                  Scanner.TokenType.Identifier, Scanner.TokenType.Read,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], ind):
        productions = [Value, Parameters_dash]
        return rule(productions, ind, "Parameters")
    else:
        out["node"] = Tree("Parameters", ["ε"])
        out["index"] = ind
        return out


def Parameters_dash(ind):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.IncrementOp,
                  Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
                  Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan, Scanner.TokenType.Setq,
                  Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
                  Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                  Scanner.TokenType.RemOp,
                  Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                  Scanner.TokenType.GreaterThanOp,
                  Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp,
                  Scanner.TokenType.Identifier, Scanner.TokenType.Read,
                  Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], ind):
        productions = [Value, Parameters_dash]
        return rule(productions, ind, "Parameters`")
    else:
        out["node"] = Tree("Parameters`", ["ε"])
        out["index"] = ind
        return out


def Value(ind):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number], ind):
        productions = [Atom]
        return rule(productions, ind, "Value")
    elif lookahead([Scanner.TokenType.OpenParenthesis], ind):
        productions = [Scanner.TokenType.OpenParenthesis, Function, Scanner.TokenType.CloseParenthesis]
        return rule(productions, ind, "Value")
    elif Match(Scanner.TokenType.LogicalTrue, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalTrue]
        return rule(productions, ind, "Value")
    elif Match(Scanner.TokenType.LogicalFalse, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.LogicalFalse]
        return rule(productions, ind, "Value")
    elif Match(Scanner.TokenType.String, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.String]
        return rule(productions, ind, "Value")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Atom(ind):
    out = {}
    if Match(Scanner.TokenType.Identifier, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Identifier]
        return rule(productions, ind, "Atom")
    elif Match(Scanner.TokenType.Number, ind, False)["node"] != ["error"]:
        productions = [Scanner.TokenType.Number]
        return rule(productions, ind, "Atom")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
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


def lookahead(Arr, ind):
    for i in Arr:
        if Match(i, ind, False)["node"] != ["error"]:
            return True
    return False


def rule(productions, ind, func_name):
    arr = []
    out = {}
    children = []
    i = 0
    while i < len(productions):
        match = productions[i]
        arr = match_production(arr, match, i, ind)
        ind = arr[-1]["index"]
        children.append(arr[-1]["node"])
        if is_error(arr):
            while ind < len(Scanner.Tokens) and Scanner.Tokens[ind].lex != ")":
                ind += 1
            arr[-1]["index"] = ind
            if Scanner.TokenType.CloseParenthesis in productions[i:]:
                i = productions[i:].index(Scanner.TokenType.CloseParenthesis) + i
                continue
            else:
                out["mode"] = ["error"]
                out["index"] = ind
                out["node"] = Tree(func_name, children)
                return out
        ind += 1
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
    node.draw()

