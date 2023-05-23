import Scanner
import tkinter as tk
import pandas
import pandastable as pt
from nltk.tree import *


errors = []


def Program(ind):
    matches = [Lists]
    return rule(matches, ind, "program")["node"]


def Lists(ind):
    matches = [List, Lists_dash]
    return rule(matches, ind, "lists")


def Lists_dash(ind):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, ind, False)["node"] != ["error"]:
        matches = [List, Lists_dash]
        return rule(matches, ind, "lists_dash")
    else:
        out["node"] = Tree("Lists_dash", ["ε"])
        out["index"] = ind
        return out


def List(ind):
    matches = [Scanner.TokenType.OpenParenthesis, Contents, Scanner.TokenType.CloseParenthesis]
    return rule(matches, ind, "list")


def Contents(ind):
    matches = [Content, Contents_dash]
    return rule(matches, ind, "contents")


def Contents_dash(ind):
    out = {}
    if lookahead([Scanner.TokenType.OpenParenthesis, Scanner.TokenType.Dotimes, Scanner.TokenType.When, Scanner.TokenType.IncrementOp,
                  Scanner.TokenType.DecrementOp, Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan,
                  Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp,
                  Scanner.TokenType.ModOp, Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                  Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp,
                  Scanner.TokenType.Identifier, Scanner.TokenType.Read, Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse], ind, False):
        matches = [Content, Contents_dash]
        return rule(matches, ind, "contents_dash")
    else:
        out["node"] = Tree("Contents_dash", ["ε"])
        out["index"] = ind
        return out


def Content(ind):
    out = {}
    if Match(Scanner.TokenType.OpenParenthesis, ind, False)["node"] != ["error"]:
        matches = [List]
        return rule(matches, ind, "content")
    elif lookahead([Scanner.TokenType.Dotimes, Scanner.TokenType.When], ind, False):
        matches = [Block]
        return rule(matches, ind, "content")
    elif lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                    Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
                    Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp,
                    Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
                    Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read, Scanner.TokenType.LogicalTrue,
                    Scanner.TokenType.LogicalFalse], ind, False):
        matches = [Expression]
        return rule(matches, ind, "content")
    else:
        out["node"] = Tree("Content", ["ε"])
        out["index"] = ind
        return out


def Block(ind):
    out = {}
    if Match(Scanner.TokenType.Dotimes, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Dotimes, Scanner.TokenType.OpenParenthesis, Scanner.TokenType.Identifier, Scanner.TokenType.Number,
                   Scanner.TokenType.CloseParenthesis, Lists]
        return rule(matches, ind, "block")
    elif Match(Scanner.TokenType.When, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.When, Scanner.TokenType.OpenParenthesis, Expression, Scanner.TokenType.CloseParenthesis, Lists]
        return rule(matches, ind, "block")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Expression(ind):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                  Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp,
                  Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp,
                  Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp,
                  Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read], ind, False):
        matches = [Function]
        return rule(matches, ind, "expression")
    elif Match(Scanner.TokenType.LogicalTrue, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LogicalTrue]
        return rule(matches, ind, "expression")
    elif Match(Scanner.TokenType.LogicalFalse, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LogicalFalse]
        return rule(matches, ind, "expression")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Function(ind):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write, Scanner.TokenType.Sin, Scanner.TokenType.Cos,
                  Scanner.TokenType.Tan], ind, False):
        matches = [UnaryFunction]
        return rule(matches, ind, "function")
    elif lookahead([Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp,
                    Scanner.TokenType.ModOp, Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                    Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp], ind,
                   False):
        matches = [BinaryFunction]
        return rule(matches, ind, "function")
    elif Match(Scanner.TokenType.Identifier, ind, False)["node"] != ["error"]:
        matches = [OtherFunction]
        return rule(matches, ind, "function")
    elif Match(Scanner.TokenType.Read, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Read]
        return rule(matches, ind, "function")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def UnaryFunction(ind):
    matches = [UnaryFunctionName, Value]
    return rule(matches, ind, "unaryfunction")


def UnaryFunctionName(ind):
    out = {}
    if lookahead([Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp], ind, False):
        matches = [UnaryOperator]
        return rule(matches, ind, "unaryfunctionname")
    elif Match(Scanner.TokenType.Write, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Write]
        return rule(matches, ind, "unaryfunctionname")
    elif Match(Scanner.TokenType.Sin, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Sin]
        return rule(matches, ind, "unaryfunctionname")
    elif Match(Scanner.TokenType.Cos, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Cos]
        return rule(matches, ind, "unaryfunctionname")
    elif Match(Scanner.TokenType.Tan, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Tan]
        return rule(matches, ind, "unaryfunctionname")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def BinaryFunction(ind):
    out = {}
    if Match(Scanner.TokenType.Setq, ind, False)["node"] != ["error"]:
        matches = [SetqFunction]
        return rule(matches, ind, "binaryfunction")
    elif lookahead([Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp, Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp,
                    Scanner.TokenType.RemOp, Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp,
                    Scanner.TokenType.GreaterThanOp, Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp], ind,
                   False):
        matches = [BinaryOperatorFunction]
        return rule(matches, ind, "binaryfunction")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def SetqFunction(ind):
    matches = [Scanner.TokenType.Setq, Scanner.TokenType.Identifier, Value]
    return rule(matches, ind, "setqfunction")


def BinaryOperatorFunction(ind):
    matches = [BinaryOperator, Value, Value]
    return rule(matches, ind, "binaryoperatorfunction")


def OtherFunction(ind):
    matches = [Scanner.TokenType.Identifier, Parameters]
    return rule(matches, ind, "otherfunction")


def UnaryOperator(ind):
    out = {}
    if Match(Scanner.TokenType.IncrementOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.IncrementOp]
        return rule(matches, ind, "unaryoperator")
    elif Match(Scanner.TokenType.DecrementOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.DecrementOp]
        return rule(matches, ind, "unaryoperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def BinaryOperator(ind):
    out = {}
    if Match(Scanner.TokenType.PlusOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.PlusOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.MinusOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.MinusOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.MultiplyOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.MultiplyOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.DivideOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.DivideOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.ModOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.ModOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.RemOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.RemOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.GreaterThanOrEqualOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.GreaterThanOrEqualOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.LessThanOrEqualOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LessThanOrEqualOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.GreaterThanOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.GreaterThanOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.LessThanOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LessThanOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.EqualOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.EqualOp]
        return rule(matches, ind, "binaryoperator")
    elif Match(Scanner.TokenType.NotEqualOp, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.NotEqualOp]
        return rule(matches, ind, "binaryoperator")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Parameters(ind):
    out = {}
    if lookahead(
            [Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
             Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
             Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
             Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp,
             Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read,
             Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], ind, False):
        matches = [Value, Parameters_dash]
        return rule(matches, ind, "parameters")
    else:
        out["node"] = Tree("Parameters", ["ε"])
        out["index"] = ind
        return out


def Parameters_dash(ind):
    out = {}
    if lookahead(
            [Scanner.TokenType.Identifier, Scanner.TokenType.Number, Scanner.TokenType.IncrementOp, Scanner.TokenType.DecrementOp, Scanner.TokenType.Write,
             Scanner.TokenType.Sin, Scanner.TokenType.Cos, Scanner.TokenType.Tan, Scanner.TokenType.Setq, Scanner.TokenType.PlusOp, Scanner.TokenType.MinusOp,
             Scanner.TokenType.MultiplyOp, Scanner.TokenType.DivideOp, Scanner.TokenType.ModOp, Scanner.TokenType.RemOp,
             Scanner.TokenType.GreaterThanOrEqualOp, Scanner.TokenType.LessThanOrEqualOp, Scanner.TokenType.GreaterThanOp,
             Scanner.TokenType.LessThanOp, Scanner.TokenType.EqualOp, Scanner.TokenType.NotEqualOp, Scanner.TokenType.Identifier, Scanner.TokenType.Read,
             Scanner.TokenType.LogicalTrue, Scanner.TokenType.LogicalFalse, Scanner.TokenType.String], ind, False):
        matches = [Value, Parameters_dash]
        return rule(matches, ind, "parameters_dash")
    else:
        out["node"] = Tree("Parameters_dash", ["ε"])
        out["index"] = ind
        return out


def Value(ind):
    out = {}
    if lookahead([Scanner.TokenType.Identifier, Scanner.TokenType.Number], ind, False):
        matches = [Atom]
        return rule(matches, ind, "value")
    elif lookahead([Scanner.TokenType.OpenParenthesis], ind, False):
        matches = [Scanner.TokenType.OpenParenthesis, Function, Scanner.TokenType.CloseParenthesis]
        return rule(matches, ind, "value")
    elif Match(Scanner.TokenType.LogicalTrue, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LogicalTrue]
        return rule(matches, ind, "value")
    elif Match(Scanner.TokenType.LogicalFalse, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.LogicalFalse]
        return rule(matches, ind, "value")
    elif Match(Scanner.TokenType.String, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.String]
        return rule(matches, ind, "value")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def Atom(ind):
    out = {}
    if Match(Scanner.TokenType.Identifier, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Identifier]
        return rule(matches, ind, "atom")
    elif Match(Scanner.TokenType.Number, ind, False)["node"] != ["error"]:
        matches = [Scanner.TokenType.Number]
        return rule(matches, ind, "atom")
    else:
        out["mode"] = ["error"]
        out["node"] = ["error"]
        out["index"] = ind
        return out


def is_error(arr):
    return 'mode' in arr[-1].keys() and arr[-1]['mode'] == ['error']


def match_entity(arr, match, position, j):
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


def lookahead(Arr, ind, appendToError):
    for i in Arr:
        if Match(i, ind, appendToError)["node"] != ["error"]:
            return True
    return False


def rule(matches, ind, func_name):
    arr = []
    out = {}
    children = []
    i = 0
    while i < len(matches):
        match = matches[i]
        arr = match_entity(arr, match, i, ind)
        ind = arr[-1]["index"]
        children.append(arr[-1]["node"])
        if is_error(arr):
            while ind < len(Scanner.Tokens) and Scanner.Tokens[ind].lex != ")":
                ind += 1
            arr[-1]["index"] = ind
            if Scanner.TokenType.CloseParenthesis in matches[i:]:
                i = matches[i:].index(Scanner.TokenType.CloseParenthesis) + i
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
        return output


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


def Scan():
    x1 = entry1.get()
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

    node.draw()


frame1 = tk.Frame(root)
button1 = tk.Button(frame1, text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
button1.pack()
canvas1.create_window(200, 180, window=frame1)
root.mainloop()
