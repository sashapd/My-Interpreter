import tokens
import parser


def main():
    code = open('program.dix', 'r').read()
    token_list = list(tokens.tokens(code))
    ast_tree = parser.buildAST(token_list)

    memory = {}
    functions = []
    token_list = ast_tree.eval(memory, functions)

    print(memory)


if __name__ == '__main__':
    main()