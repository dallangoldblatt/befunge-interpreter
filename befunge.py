import getopt
import sys
from interpreter import Interpreter

if __name__ == '__main__':
    argv = sys.argv[1:]

    # Handle help request
    if len(argv) < 1 or '-h' in argv or '--help' in argv:
        print('Usage: befunge.py <filename> [-v]')
        sys.exit(0)

    # Parse other args
    filename = argv[0]
    visualize = '-v' in argv

    # Read each line into a string, removing trailing whitespace
    try:
        with open(filename) as f:
            lines = [line.rstrip() for line in list(f)]
    except FileNotFoundError:
        print(f'File \'{filename}\' not found')
        print('Usage: befunge.py <filename> [-v]')
        sys.exit(0)

    # Create the interpreter
    interpreter = Interpreter(lines, visualize=visualize)
    interpreter.interpret()
