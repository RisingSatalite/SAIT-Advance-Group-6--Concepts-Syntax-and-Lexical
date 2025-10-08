# Lexical Analyser
import re

token_specification = [
    # Keywords
    ('LET', r'\blet\b'),
    ('FOR', r'\bfor\b'),
    ('IN', r'\bin\b'),
    ('RETURN', r'\breturn\b'),

    # Identifiers, Numbers, Operators, etc.
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('NUMBER', r'\d+'),
    ('OPERATOR', r'==|=|\+|-|\*|/'),
    ('DELIMITER', r'[\[\](),;.:]'),
    ('STRING', r'"[^"]*"'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),  # Skip spaces and tabs
    ('MISMATCH', r'.'),  # Any other character
]
# tokenize input
token_regex_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)


def tokenize(code):
    tokens = []
    for line in re.finditer(token_regex_pattern, code):
        cluster = line.lastgroup
        value = line.group()

        if cluster == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
        elif cluster in ('LET', 'FOR', 'IN', 'RETURN'):
            tokens.append((cluster, value))
        elif cluster == 'IDENTIFIER':
            tokens.append(('IDENTIFIER', value))
        elif cluster == 'OPERATOR':
            tokens.append(('OPERATOR', value))
        elif cluster == 'DELIMITER':
            tokens.append(('DELIMITER', value))
        elif cluster == 'STRING':
            tokens.append(('STRING', value))
        elif cluster == 'NEWLINE':
            continue
        elif cluster == 'SKIP':
            continue
        elif cluster == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r}')

    return tokens


# Parser

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def next(self):
        token = self.peek()
        self.position += 1
        return token

    def expect(self, expected_type, expected_value=None):
        token = self.peek()
        if not token:
            raise SyntaxError(f"Expected {expected_type}, but reached end of input")

        token_type, token_value = token

        if token_type != expected_type:
            raise SyntaxError(f"Expected token type {expected_type}, but found {token_type} ({token_value})")

        if expected_value is not None and token_value != expected_value:
            raise SyntaxError(f"Expected token value {expected_value}, but found {token_value}")

        return self.next()

    # program ::= statement +
    def parse_program(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.parse_statement())
        return "Program", statements

    # statement ::= declaration | forloop | return_stmt | assignment
    def parse_statement(self):
        token = self.peek()
        if not token:
            return None
        if token[0] == 'LET':
            return self.parse_declaration()
        elif token[0] == 'FOR':
            return self.parse_forloop()
        elif token[0] == 'RETURN':
            return self.parse_return()
        elif token[0] == 'IDENTIFIER':
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token {token}")

    # declaration ::= "let" IDENTIFIER "=" expression ";"
    def parse_declaration(self):
        self.expect('LET')
        var = self.expect('IDENTIFIER')
        self.expect('OPERATOR')  # '='
        nums = self.parse_number_set()
        if self.peek() and self.peek()[0] == 'DELIMITER':
            self.next()  # consume ';'
        return "Declaration", var, nums

    # number_set ::= [ number_list ]
    def parse_number_set(self):
        self.expect('DELIMITER', '[')
        numlist = self.parse_number_list()
        self.expect('DELIMITER', ']')
        return 'number_set', numlist

    # number_list ::= NUMBER | NUMBER "," number_list
    def parse_number_list(self):
        numbers = [self.expect('NUMBER')]

        while self.peek() and self.peek()[0] == 'DELIMITER' and self.peek()[1] == ',':
            self.expect('DELIMITER', ',')
            numbers.append(self.expect('NUMBER'))

        return 'number_list', numbers

    # assignment ::= variable "=" addition ";"
    def parse_assignment(self):
        var = self.expect('IDENTIFIER')  #
        self.expect('OPERATOR', '=')
        expr = self.parse_addition()
        self.expect('DELIMITER', ';')
        return 'assignment', var, expr

    # count ::= variable "=" addition ";"
    def parse_count(self):
        var = self.expect('IDENTIFIER')  # <variable>
        self.expect('OPERATOR', '=')  # '='
        expr = self.parse_addition()  # <addition>
        self.expect('DELIMITER', ';')  # ';'
        return 'count', var, expr

    # forloop ::= "for" IDENTIFIER "in" IDENTIFIER statement
    def parse_forloop(self):
        self.expect('FOR')
        var = self.expect('IDENTIFIER')
        self.expect('IN')
        iterable = self.parse_number_set()  # parse the list [ ... ]
        self.expect('DELIMITER', ':')  # expecting ':' to separate header and body
        assignment = self.parse_assignment()
        count_stmt = self.parse_count()
        return 'forloop', var, iterable, assignment, count_stmt

    # return_stmt ::= "return" <variable> "/" <variable>
    def parse_return(self):
        self.expect('RETURN')
        left = self.expect('IDENTIFIER')
        self.expect('OPERATOR', '/')
        right = self.expect('IDENTIFIER')

        return "ReturnStmt", ("Division", left, right)

    def parse_addition(self):
        left = self.parse_term()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] == '+':
            op = self.expect('OPERATOR', '+')
            right = self.parse_term()
            left = ('addition', left, op, right)
        return left

    def parse_term(self):
        token = self.peek()
        if token and token[0] == 'NUMBER':
            return self.expect('NUMBER')
        elif token and token[0] == 'IDENTIFIER':
            return self.expect('IDENTIFIER')
        else:
            raise SyntaxError(f"Unexpected token {token} in term")