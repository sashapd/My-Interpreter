import interpreter

def main():
    code = open('program.dix', 'r').read()
    interpreter.interpret(code)


if __name__ == '__main__':
    main()