from interpreter import Interpreter

filename = 'examples/cat.txt'

if __name__ == '__main__':
    # Read each line into a string, removing trailing whitespace
    with open(filename) as f:
        lines = [line.rstrip() for line in list(f)]

    # Create the interpreter
    interpreter = Interpreter(lines)
    interpreter.interpret()
