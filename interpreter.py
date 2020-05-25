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

            # Perform the command
            self.interpret_command(command)

            # Move the pointer
            self.move_pointer()

    def safe_pop(self):
        # If the stack has run out of values, return 0
        try:
            return self.stack.pop(-1)
        except IndexError:
            return 0

    def interpret_command(self, command):
        # TODO handle stringmode

        # Perform the operation
        if command == '"':
            # Toggle stringmode
            self.stringmode = not self.stringmode
        elif self.stringmode:
            # Push each character's ASCII value
            self.stack.append(ord(command))
        elif command == '+':
            # Addition: Pop two values a and b, then push the result of a+b
            self.stack.append(self.safe_pop() + self.safe_pop())
        elif command == '-':
            # Subtraction: Pop two values a and b, then push the result of b-a
            a = self.safe_pop()
            b = self.safe_pop()
            self.stack.append(b - a)
        elif command == '*':
            # Multiplication: Pop two values a and b, then push the result of a*b
            self.stack.append(self.safe_pop() * self.safe_pop())
        elif command == '/':
            # Integer division: Pop two values a and b, then push the result of b/a, rounded down.
            # According to the specifications, if a is zero, ask the user what result they want.
            a = self.safe_pop()
            b = self.safe_pop()
            self.stack.append(b // a)
            # TODO handle case where denom is zero
        elif command == '%':
            # Modulo: Pop two values a and b, then push the remainder of the integer division of b/a.
            a = self.safe_pop()
            b = self.safe_pop()
            self.stack.append(b % a)
        elif command == '!':
            # Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
            value = self.safe_pop()
            if value == 0:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif command == '`':
            # Greater than: Pop two values a and b, then push 1 if b>a, otherwise zero.
            if self.safe_pop() < self.safe_pop():
                self.stack.append(1)
            else:
                self.stack.append(0)
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
            if self.safe_pop() == 0:
                self.direction = 1
            else:
                self.direction = 3
        elif command == '|':
            # Vertical IF: pop a value; set direction to down if value=0, set to up otherwise
            if self.safe_pop() == 0:
                self.direction = 2
            else:
                self.direction = 0
        elif command == ':':
            # Duplicate top stack value
            value = self.safe_pop()
            self.stack.append(value)
            self.stack.append(value)
        elif command == '\\':
            # Swap top stack values
            value1 = self.safe_pop()
            value2 = self.safe_pop()
            self.stack.append(value1)
            self.stack.append(value2)
        elif command == '$':
            # Pop (remove) top stack value and discard
            self.safe_pop()
        elif command == '.':
            # Pop top of stack and output as integer
            print(self.safe_pop())
        elif command == ',':
            # Pop top of stack and output as ASCII character
            print(chr(self.safe_pop()))
        elif command == '#':
            # Bridge: jump over next command in the current direction of the current PC
            # This is handled by moving the pointer twice
            self.move_pointer()
        elif command == 'g':
            # A "get" call (a way to retrieve data in storage).
            # Pop two values y and x, then push the ASCII value of the character
            # at that position in the program. If (x,y) is out of bounds, push 0
            y = self.safe_pop()
            x = self.safe_pop()
            if x in range(0, self.cols) and y in range(0, self.rows):
                self.stack.append(ord(self.source[y][x]))
            else:
                self.stack.append(0)
        elif command == 'p':
            # A "put" call (a way to store a value for later use).
            # Pop three values y, x and v, then change the character at the
            # position (x,y) in the program to the character with ASCII value v
            y = self.safe_pop()
            x = self.safe_pop()
            v = self.safe_pop()
            self.source[y][x] = v
        elif command == '&':
            # Get integer from user and push it
            valid = False
            while not valid:
                try:
                    self.stack.append(int(input('Enter an integer: ')))
                    valid = True
                except:
                    print('Invalid input')
        elif command == '~':
            # Get character from user and push it
            valid = False
            while not valid:
                try:
                    self.stack.append(ord(input('Enter a character: ')))
                    valid = True
                except:
                    print('Invalid input')
        elif command == '@':
            # End program
            self.done = True
        elif command.isdigit():
            # Push corresponding number onto the stack
            self.stack.append(int(command))

    def move_pointer(self):
        move = self.move_directions[self.direction]
        y = (self.pointer[0] + move[0]) % self.rows
        x = (self.pointer[1] + move[1]) % self.cols
        self.pointer = [y, x]
