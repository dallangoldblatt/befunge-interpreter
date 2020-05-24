import random

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
        self.done = False

    def interpret(self):
        while not self.done:
            command = self.source[self.pointer[0]][self.pointer[1]]

            # Make sure the stack has enough items for the command
            validate_command(command)

            # Perform the command
            interpret_command(command)

            # Move the pointer
            move_pointer()

    def validate_command(self, command):
        if command in ['+', '*', '-', '/', '%', '`', '\\', 'g', 'p']:
            assert len(self.stack >= 2), f'Command \'{command}\' requires at least 2 values on the stack'
        elif command in ['!', '_', '|', ':', '$', '.', ',']:
            assert len(self.stack >= 1), f'Command \'{command}\' requires at least 1 value on the stack'

    def interpret_command(self, command):
        # TODO handle stringmode

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
        elif command == '?':
            # Random PC direction
            self.direction = random.choice(self.directions)
        elif command == '_':
            # Horizontal IF: pop a value; set direction to right if value=0, set to left otherwise
            if stack.pop() == 0:
                self.direction = 1
            else:
                self.direction = 3
        elif command == '|':
            # Vertical IF: pop a value; set direction to down if value=0, set to up otherwise
            if stack.pop() == 0:
                self.direction = 2
            else:
                self.direction = 0
        elif command == '"':
            # Toggle stringmode (push each character's ASCII value all the way up to the next ")
            self.stringmode = not self.stringmode
        elif command == ':':
            # Duplicate top stack value
            value = stack.pop()
            stack.push(value)
            stack.push(value)
        elif command == '\\':
            # Swap top stack values
            value1 = stack.pop()
            value2 = stack.pop()
            stack.push(value1)
            stack.push(value2)
        elif command == '$':
            # Pop (remove) top stack value and discard
            stack.pop()
        elif command == '.':
            # Pop top of stack and output as integer
            print(stack.pop())
        elif command == ',':
            # Pop top of stack and output as ASCII character
            print(chr(stack.pop()))
        elif command == '#':
            # Bridge: jump over next command in the current direction of the current PC
            # This is handled by moving the pointer twice
            move_pointer()
        elif command == 'g':
            # A "get" call (a way to retrieve data in storage).
            # Pop two values y and x, then push the ASCII value of the character
            # at that position in the program. If (x,y) is out of bounds, push 0
            y = stack.pop()
            x = stack.pop()
            if x in range(0, self.cols) and y in range(0, self.rows):
                stack.push(ord(self.source[y][x]))
            else:
                stack.push(0)
        elif command == 'p':
            # A "put" call (a way to store a value for later use).
            # Pop three values y, x and v, then change the character at the
            # position (x,y) in the program to the character with ASCII value v
            y = stack.pop()
            x = stack.pop()
            v = stack.pop()
            self.source[y][x] = v
        elif command == '&':
            # Get integer from user and push it
            input = false
            while not input:
                try:
                    stack.push(input('Enter an integer: '))
                    input = True
                except:
                    print('Invalid input')
        elif command == '~':
            # Get character from user and push it
            input = false
            while not input:
                try:
                    stack.push(ord(input('Enter a character: ')))
                    input = True
                except:
                    print('Invalid input')
        elif command == '@':
            # End program
            self.done = True
        elif command.isdigit():
            # Push corresponding number onto the stack
            stack.push(int(command))

    def move_pointer(self):
        move = self.move_directions[self.direction]
        y = (self.pointer[0] + move[0]) % self.rows
        x = (self.pointer[1] + move[1]) % self.cols
        self.pointer = [y, x]
