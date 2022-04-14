from ply.lex import lex
from ply.yacc import yacc
import json


class Parser:
    parser = None
    SymbolTable = {
        "constants": [],
        "variables": [],
        "subFunc": []
    }

    def __init__(self, debug=False, write_tables=False):
        tokens = ('REAL', 'COLON', 'LBRACKET', 'LPAREN',
                  'DIGITS', 'ASSIGNOP', 'FOR', 'DO', 'QUO',
                  'UMINUS', 'RECORD', 'OF', 'NUM', 'EQUAL',
                  'ELSE', 'CONST', 'COM', 'RPAREN', 'ARRAY',
                  'INTEGER', 'THEN', 'POINTTO', 'CHAR', 'MULOP',
                  'POINT', 'TO', 'PROCEDURE', 'WHILE', 'LETTER',
                  'RELOP', 'VAR', 'BOOLEAN', 'IF', 'FUNCTION',
                  'END', 'RBRACKET', 'PROGRAM', 'READ',
                  'WRITE', 'NOT', 'BEGIN', 'SEMICOLON', 'ADDOP', 'ID')

        reserved = ['REAL', 'FOR', 'DO', 'RECORD', 'OF', 'ELSE', 'CONST', 'TO',
                    'ARRAY', 'INTEGER', 'THEN', 'CHAR', 'PROCEDURE', 'WHILE',
                    'VAR', 'BOOLEAN', 'IF', 'FUNCTION', 'END', 'PROGRAM',
                    'READ', 'WRITE', 'NOT', 'BEGIN']

        reserved_2 = ['DIV', 'MOD', 'AND', 'OR']
        reserved_2_map = {
            'DIV': 'MULOP',
            'MOD': 'MULOP',
            'AND': 'MULOP',
            'OR': 'ADDOP',
        }

        t_ignore = ' \t'

        t_REAL = r'(?i)REAL'
        t_COLON = r':'
        t_LBRACKET = r'\['
        t_LPAREN = r'\('
        t_ASSIGNOP = r':='
        t_FOR = r'(?i)FOR'
        t_DO = r'(?i)DO'
        t_QUO = r'\''
        t_RECORD = r'(?i)RECORD'
        t_OF = r'(?i)OF'
        t_EQUAL = r'='
        t_ELSE = r'(?i)ELSE'
        t_CONST = r'(?i)CONST'
        t_COM = r','
        t_RPAREN = r'\)'
        t_ARRAY = r'(?i)ARRAY'
        t_INTEGER = r'(?i)INTEGER'
        t_THEN = r'(?i)THEN'
        t_POINTTO = '\.\.'
        t_CHAR = r'(?i)CHAR'
        t_MULOP = r'(?i)\*|\/|DIV|MOD|AND'
        t_POINT = r'\.'
        t_TO = r'(?i)TO'
        t_PROCEDURE = r'(?i)PROCEDURE'
        t_WHILE = r'(?i)WHILE'
        t_LETTER = r'[a-zA-Z]'
        t_RELOP = r'<=|>=|<>|<|>'
        t_VAR = r'(?i)VAR'
        t_BOOLEAN = r'(?i)BOOLEAN'
        t_IF = r'(?i)IF'
        t_FUNCTION = r'(?i)FUNCTION'
        t_END = r'(?i)END'
        t_RBRACKET = r'\]'
        t_PROGRAM = r'(?i)PROGRAM'
        t_READ = r'(?i)READ'
        t_WRITE = r'(?i)WRITE'
        t_NOT = r'(?i)NOT'
        t_BEGIN = r'(?i)BEGIN'
        t_SEMICOLON = r';'
        t_ADDOP = r'(?i)\+|-|OR'

        def t_ignore_COMMENT(t):
            r'\{.*\}|//.*|\(\*(.|\n)*\*\)'
            t.lexer.lineno += t.value.count('\n')
            pass

        def t_NUM(t):
            r'\d+\.\d+'
            t.value = float(t.value)
            return t

        def t_DIGITS(t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)*'
            if t.value.upper() in reserved:
                t.type = t.value.upper()
            elif t.value.upper() in reserved_2:
                t.type = reserved_2_map[t.value.upper()]
            elif '.' in t.value:
                t.value = t.value.split('.')
            return t

        def t_ignore_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count('\n')

        def t_error(t):
            print(f'Illegal character at line {t.lineno} : {t.value}')
            t.lexer.skip(1)

        lexer = lex(debug=debug)

        def p_programstruct(p):
            '''
            programstruct : program_head SEMICOLON program_body POINT
            '''
            p[0] = {
                "type": "programstruct",
                "program_head": p[1],
                "program_body": p[3]
            }

        def p_program_head(p):
            '''
            program_head : PROGRAM ID LPAREN idlist RPAREN
            '''
            p[0] = {
                "type": "program_head",
                "ID": p[2],
                "idlist": p[4]
            }

        def p_program_head_program_id(p):
            '''
            program_head : PROGRAM ID
            '''
            p[0] = {
                "type": "program_head",
                "ID": p[2],
                "idlist": []
            }

        def p_program_body(p):
            '''
            program_body : const_declarations var_declarations subprogram_declarations compound_statement
            '''
            p[0] = {
                "type": "program_body",
                "const_declarations": p[1],
                "var_declarations": p[2],
                "subprogram_declarations": p[3],
                "compound_statement": p[4]
            }

        def p_idlist(p):
            '''
            idlist : idlist COM ID
            '''
            p[0] = {
                "type": "idlist",
                "ids": p[1]["ids"] + [p[3]] if p[3] else p[1]["ids"]
            }

        def p_idlist_id(p):
            '''
            idlist : ID
            '''
            p[0] = {
                "type": "idlist",
                "ids": [p[1]]
            }

        def p_const_declarations(p):
            '''
            const_declarations : CONST const_declaration SEMICOLON
                            | 
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "const_declarations",
                    "const_declaration": p[2]
                }
            else:
                p[0] = None

        def p_const_declaration(p):
            '''
            const_declaration : const_declaration SEMICOLON ID EQUAL const_value
            '''
            p[0] = {
                "type": "const_declaration",
                "values": p[1]["values"] + [{
                    "ID": p[3],
                    "const_value": p[5]
                }]
            }

        def p_const_declaration_id(p):
            '''
            const_declaration : ID EQUAL const_value
            '''
            p[0] = {
                "type": "const_declaration",
                "values": [{
                    "ID": p[1],
                    "const_value": p[3]
                }]
            }

        def p_const_value_addop(p):
            '''
            const_value : ADDOP NUM
            '''
            p[0] = {
                "type": "const_value",
                "_type": "NUM",
                "value": p[2] if p[1] == '+' else -p[2]
            }

        def p_const_value(p):
            '''
            const_value : NUM
                        | DIGITS
            '''
            p[0] = {
                "type": "const_value",
                "_type": "NUM",
                "value": p[1]
            }

        def p_const_value_letter(p):
            '''
            const_value : QUO LETTER QUO
            '''
            p[0] = {
                "type": "const_value",
                "_type": "LETTER",
                "value": p[2]
            }

        def p_var_declarations(p):
            '''
            var_declarations : VAR var_declaration SEMICOLON
                            | 
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "var_declarations",
                    "var_declaration": p[2]
                }
            else:
                p[0] = []

        def p_var_declaration(p):
            '''
            var_declaration : var_declaration SEMICOLON idlist COLON type
                            | idlist COLON type
            '''
            if len(p) == 6:
                p[0] = {
                    "type": "var_declaration",
                    "values": p[1]["values"] + [{
                        "idlist": p[3],
                        "type": p[5]
                    }]
                }
            else:
                p[0] = {
                    "type": "var_declaration",
                    "values": [{
                        "idlist": p[1],
                        "type": p[3]
                    }]
                }

        def p_type(p):
            '''
            type : basic_type
                | ARRAY LBRACKET period RBRACKET OF basic_type
                | RECORD multype END
            '''
            if not type(p[1]) == dict and p[1].upper() == 'ARRAY':
                p[0] = {
                    "type": "type",
                    "_type": "ARRAY",
                    "period": p[3],
                    "basic_type": p[5]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'RECORD':
                p[0] = {
                    "type": "type",
                    "_type": "RECORD",
                    "multype": p[2]
                }
            else:
                p[0] = {
                    "type": "type",
                    "_type": p[1]
                }

        def p_basic_type(p):
            '''
            basic_type : INTEGER
                        | REAL
                        | BOOLEAN
                        | CHAR
            '''
            p[0] = {
                "type": "basic_type",
                "_type": p[1]
            }

        def p_period(p):
            '''
            period : period COM DIGITS POINTTO DIGITS
                | DIGITS POINTTO DIGITS
            '''
            if len(p) == 5:
                p[0] = {
                    "type": "period",
                    "values": p[1]["values"] + [{
                        "start": p[3],
                        "END": p[5]
                    }]
                }
            else:
                p[0] = {
                    "type": "period",
                    "values": [{
                        "start": p[1],
                        "END": p[3]
                    }]
                }

        def p_subprogram_declarations(p):
            '''
            subprogram_declarations : subprogram_declarations subprogram SEMICOLON
                                    | 
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "subprogram_declarations",
                    "subprograms": p[1]["subprograms"] + [p[2]] if p[2] else p[1]["subprograms"]
                }
            else:
                p[0] = {
                    "type": "subprogram_declarations",
                    "subprograms": []
                }

        def p_subprogram(p):
            '''
            subprogram : subprogram_head SEMICOLON subprogram_body
            '''
            p[0] = {
                "type": "subprogram",
                "subprogram_head": p[1],
                "subprogram_body": p[3]
            }

        def p_subprogram_head(p):
            '''
            subprogram_head : PROCEDURE ID formal_parameter
                            | FUNCTION ID formal_parameter COLON basic_type 
            '''
            if not type(p[1]) == dict and p[1].upper() == 'PROCEDURE':
                p[0] = {
                    "type": "subprogram_head",
                    "_type": "PROCEDURE",
                    "ID": p[2],
                    "formal_parameter": p[3]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'FUNCTION':
                p[0] = {
                    "type": "subprogram_head",
                    "_type": "FUNCTION",
                    "ID": p[2],
                    "formal_parameter": p[3],
                    "basic_type": p[5]
                }

        def p_formal_parameter(p):
            '''
            formal_parameter : LPAREN parameter_list RPAREN
                            | 
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "formal_parameter",
                    "parameter_list": p[2]
                }
            else:
                p[0] = {
                    "type": "formal_parameter",
                    "parameter_list": None
                }

        def p_parameter_list(p):
            '''
            parameter_list : parameter_list SEMICOLON parameter
                        | parameter
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "parameter_list",
                    "parameters": p[1]["parameters"] + [p[3]] if p[3] else p[1]["parameters"]
                }
            else:
                p[0] = {
                    "type": "parameter_list",
                    "parameters": [p[1]]
                }

        def p_parameter(p):
            '''
            parameter : var_parameter
                    | value_parameter
            '''
            p[0] = {
                "type": "parameter",
                "value": p[1]
            }

        def p_var_parameter(p):
            '''
            var_parameter : VAR value_parameter
            '''
            p[0] = {
                "type": "var_parameter",
                "value_parameter": p[2]
            }

        def p_value_parameter(p):
            '''
            value_parameter : idlist COLON basic_type
            '''
            p[0] = {
                "type": "value_parameter",
                "idlist": p[1],
                "basic_type": p[3]
            }

        def p_subprogram_body(p):
            '''
            subprogram_body : const_declarations var_declarations compound_statement
            '''
            p[0] = {
                "type": "subprogram_body",
                "const_declarations": p[1],
                "var_declarations": p[2],
                "compound_statement": p[3]
            }

        def p_compound_statement(p):
            '''
            compound_statement : BEGIN statement_list END
            '''
            p[0] = {
                "type": "compound_statement",
                "statement_list": p[2]
            }

        def p_statement_list(p):
            '''
            statement_list : statement_list SEMICOLON statement
                        | statement
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "statement_list",
                    "statements": p[1]["statements"] + [p[3]] if p[3] else p[1]["statements"]
                }
            else:
                p[0] = {
                    "type": "statement_list",
                    "statements": [p[1]]
                }

        def p_statement(p):
            '''
            statement : variable ASSIGNOP expression
                    | procedure_call
                    | compound_statement
                    | IF expression THEN statement else_part
                    | FOR ID ASSIGNOP expression TO expression DO statement
                    | READ LPAREN variable_list  RPAREN
                    | WRITE LPAREN expression_list RPAREN
                    | WHILE expression DO statement
                    | 
            '''
            if len(p) == 1:
                p[0] = None
            elif not type(p[1]) == dict and p[1].upper() == 'IF':
                p[0] = {
                    "type": "statement",
                    "_type": "IF",
                    "expression": p[2],
                    "statement": p[4],
                    "else_part": p[5]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'FOR':
                p[0] = {
                    "type": "statement",
                    "_type": "FOR",
                    "ID": p[2],
                    "ASSIGNOP": p[3],
                    "expression": p[4],
                    "to_expression": p[6],
                    "statement": p[8]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'READ':
                p[0] = {
                    "type": "statement",
                    "_type": "READ",
                    "variable_list": p[3]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'WRITE':
                p[0] = {
                    "type": "statement",
                    "_type": "WRITE",
                    "expression_list": p[3]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'WHILE':
                p[0] = {
                    "type": "statement",
                    "_type": "WHILE",
                    "expression": p[2],
                    "statement": p[4]
                }
            elif p[1]["type"] == "variable":
                p[0] = {
                    "type": "statement",
                    "_type": "variable",
                    "variable": p[1],
                    "ASSIGNOP": p[2],
                    "expression": p[3]
                }
            elif p[1]["type"] == "procedure_call":
                p[0] = {
                    "type": "statement",
                    "_type": "procedure_call",
                    "procedure_call": p[1]
                }
            elif p[1]["type"] == "compound_statement":
                p[0] = {
                    "type": "statement",
                    "_type": "compound_statement",
                    "compound_statement": p[1]
                }
            else:
                p[0] = None

        def p_variable_list(p):
            '''
            variable_list : variable_list COM variable
                        | variable
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "variable_list",
                    "variables": p[1]["variables"] + [p[3]] if p[3] else p[1]["variables"]
                }
            else:
                p[0] = {
                    "type": "variable_list",
                    "variables": [p[1]]
                }

        def p_variable(p):
            '''
            variable : ID id_varpart
            '''
            p[0] = {
                "type": "variable",
                "ID": p[1],
                "id_varpart": p[2]
            }

        def p_id_varpart(p):
            '''
            id_varpart : LBRACKET expression_list RBRACKET
                       | 
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "id_varpart",
                    "expression_list": p[2]
                }
            else:
                p[0] = {
                    "type": "id_varpart",
                    "expression_list": None
                }

        def p_procedure_call(p):
            '''
            procedure_call : ID
                           | ID LPAREN expression_list RPAREN
            '''
            if len(p) == 2:
                p[0] = {
                    "type": "procedure_call",
                    "ID": p[1]
                }
            else:
                p[0] = {
                    "type": "procedure_call",
                    "ID": p[1],
                    "expression_list": p[3]
                }

        def p_else_part(p):
            '''
            else_part : ELSE statement
                      | 
            '''
            if len(p) == 3:
                p[0] = {
                    "type": "else_part",
                    "statement": p[2]
                }
            else:
                p[0] = {
                    "type": "else_part",
                    "statement": None
                }

        def p_expression_list(p):
            '''
            expression_list : expression_list COM expression
                            | expression
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "expression_list",
                    "expressions": p[1]["expressions"] + [p[3]] if p[3] else p[1]["expressions"]
                }
            else:
                p[0] = {
                    "type": "expression_list",
                    "expressions": [p[1]]
                }

        def p_expression(p):
            '''
            expression : simple_expression RELOP simple_expression
                       | simple_expression
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "expression",
                    "simple_expression_1": p[1],
                    "RELOP": p[2],
                    "simple_expression_2": p[3]
                }
            else:
                p[0] = {
                    "type": "expression",
                    "simple_expression": p[1]
                }

        def p_expression_equal(p):
            '''
            expression : simple_expression EQUAL simple_expression
            '''
            p[0] = {
                "type": "expression",
                "simple_expression_1": p[1],
                "RELOP": p[2],
                "simple_expression_2": p[3]
            }

        def p_simple_expression(p):
            '''
            simple_expression : simple_expression ADDOP term
                              | term
            '''
            if len(p) == 4:
                p[0] = {
                    "type": "simple_expression",
                    "simple_expression": p[1],
                    "ADDOP": p[2],
                    "term": p[3]
                }
            else:
                p[0] = {
                    "type": "simple_expression",
                    "term": p[1]
                }

        def p_term(p):
            '''
            term : term MULOP factor
                 | factor
            '''
            if len(p) == 3:
                p[0] = {
                    "type": "term",
                    "MULOP": p[1],
                    "factor": p[2]
                }
            else:
                p[0] = {
                    "type": "term",
                    "factor": p[1]
                }

        def p_factor_num(p):
            '''
            factor : NUM
                   | DIGITS
            '''
            p[0] = {
                "type": "factor",
                "_type": "NUM",
                "NUM": p[1]
            }

        def p_factor_variable(p):
            '''
            factor : variable
            '''
            p[0] = {
                "type": "factor",
                "_type": "variable",
                "variable": p[1]
            }

        def p_factor_procedure_id(p):
            '''
            factor : ID LPAREN expression_list RPAREN
            '''
            p[0] = {
                "type": "factor",
                "_type": "procedure_id",
                "ID": p[1],
                "expression_list": p[3]
            }

        def p_factor_expression_list(p):
            '''
            factor : LPAREN expression_list RPAREN
            '''
            p[0] = {
                "type": "factor",
                "_type": "expression_list",
                "expression_list": p[2]
            }

        def p_factor_not(p):
            '''
            factor : NOT factor
            '''
            p[0] = {
                "type": "factor",
                "_type": "NOT",
                "factor": p[2]
            }

        def p_factor_uminus(p):
            '''
            factor : UMINUS factor
            '''
            p[0] = {
                "type": "factor",
                "_type": "UMINUS",
                "factor": p[2]
            }

        def p_multype(p):
            '''
            multype : multype ID COLON type SEMICOLON
                    | ID COLON type SEMICOLON
            '''
            p[0] = {
                "type": "MULOP",
                "_type": p[1],
                "ID": p[2]
            }

        def p_error(p):
            print(f'Syntax error at line {p.lineno} : {p.value}')

        self.parser = yacc(debug=debug, write_tables=write_tables)

    def parse(self, data):
        self.SymbolTable = {
            "constants": [],
            "variables": [],
            "subFunc": []
        }
        return self.parser.parse(data)
