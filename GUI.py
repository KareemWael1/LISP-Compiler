import Scanner
import Parser

parse_button = Scanner.tk.Button(Scanner.root, text="parse Input", command=Parser.parse, bg = 'lightblue', width=12)
parse_button.pack()

def main():
    Scanner.root.mainloop()


if __name__ == "__main__":
    main()

