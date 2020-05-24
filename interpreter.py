class Interpreter():

    def __init__(self, lines):
        # Set pointer bounds
        self.rows = len(lines)
        self.cols = len(max(lines, key=len))

        # Covert program source into a two dimentional array of characters
        # Right-pad each string to the appropriate number of columns
        self.source = [[*line.ljust(self.cols)] for line in lines if len(line) > 0]

        # Pointer move directions in order: North, East, South, West
        self.move_directions = {0: [-1, 0], 1: [0, 1], 2: [1, 0], 3: [0, -1]}
        self.directions = [0, 1, 2, 3]

        # Set pointer initital values
        self.pointer = [0, 0]
        self.direction = 1

        # Create program stack
        self.stack = []

        self.stringmode = False
        self.stop = False

    def interpret(self):
        while not self.stop:
            command = self.source[self.pointer[0]][self.pointer[1]]

            # Make sure the stack has enough items for the command
            validate_command(command)

            # Perform the command
            interpret_command(command)

            # Move the pointer

            self.stop = True

    def validate_command(self, command):
        if command in ['+', '*', '-', '/', '%', '`', '\\', 'g', 'p']:
            assert len(self.stack >= 2), f'Command \'{command}\' requires at least 2 values on the stack'
        elif command in ['!', '_', '|', ':', '$', , '.', ',']:
            assert len(self.stack >= 1), f'Command \'{command}\' requires at least 1 value on the stack'

    def interpret_command(self, command):
        # Perform the operation
        if command == '+':
            # Addition: Pop two values a and b, then push the result of a+b
            stack.push(stack.pop() + stack.pop())
        elif command == '-':
            # Subtraction: Pop two values a and b, then push the result of b-a
            stack.push(stack.pop() - stack.pop())
        elif command == '*':
            # Multiplication: Pop two values a and b, then push the result of a*b
            stack.push(stack.pop() * stack.pop())
        elif command == '/':
            # Integer division: Pop two values a and b, then push the result of b/a, rounded down.
            # According to the specifications, if a is zero, ask the user what result they want.
            stack.push(stack.pop() // stack.pop())
            # TODO handle case where denom is zero
        elif command == '%':
            # Modulo: Pop two values a and b, then push the remainder of the integer division of b/a.
            stack.push(stack.pop() % stack.pop())
        elif command == '!':
            # Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
            value = stack.pop()
            if value == 0:
                stack.push(1)
            else:
                stack.push(0)
        elif command == '`':
            # Greater than: Pop two values a and b, then push 1 if b>a, otherwise zero.
            if stack.pop() < stack.pop():
                stack.push(1)
            else:
                stack.push(0)
        elif command == '>':
            # PC direction right
            self.direction = 1
        elif command == '<':
            # PC direction left
            self.direction = 3
        elif command == '>':
            # PC direction right
            self.direction = 1
        elif command == '^':
            # PC direction up
            self.direction = 0
        elif command == 'v':
            # PC direction down
            self.direction = 2
