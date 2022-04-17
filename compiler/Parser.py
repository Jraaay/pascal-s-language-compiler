from ply.lex import lex
from ply.yacc import yacc
import copy


class Parser:
    parser = None
    SymbolTable = {
        "constants": [],
        "variables": [],
        "subFunc": []
    }
    error = []
    warning = []
    id = 0
    curSymbol = {}
    subSymbol = {}
    inSubFun = False
    symbolMap = {}
    subFuncMap = {}

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

        safe_assign = {
            'INTEGER': ['INTEGER', 'REAL'],
            'REAL': ['REAL'],
            'CHAR': ['CHAR', 'INTEGER', 'REAL'],
            'BOOLEAN': ['BOOLEAN', 'INTEGER', 'REAL', 'CHAR'],
            'RECORD': ['RECORD']
        }

        warn_assign = {
            'INTEGER': ['CHAR', 'BOOLEAN'],
            'REAL': ['CHAR', 'BOOLEAN', 'INTEGER'],
            'CHAR': ['BOOLEAN'],
            'BOOLEAN': [],
            'RECORD': []
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
        t_READ = r'(?i)READ'
        t_WRITE = r'(?i)WRITE'
        t_NOT = r'(?i)NOT'
        t_BEGIN = r'(?i)BEGIN'
        t_SEMICOLON = r';'
        t_ADDOP = r'(?i)\+|-|OR'

        def t_PROGRAM(t):
            r'(?i)PROGRAM'
            t.lexer.lineno = 0
            return t

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
            r'[0-9a-zA-Z_][a-zA-Z_0-9]*(\.[0-9a-zA-Z_][a-zA-Z_0-9]*)*'
            if t.value.upper() in reserved:
                t.type = t.value.upper()
            elif t.value.upper() in reserved_2:
                t.type = reserved_2_map[t.value.upper()]
            elif '.' in t.value:
                t.value = t.value.split('.')
                for i in t.value:
                    if t.value[0].isdigit():
                        if not self.error:
                            self.error = []
                        self.error.append({
                            "code": "A-01",
                            "info": {
                                "line": t.lineno,
                                "value": t.value.split('\n')[0],
                                "lexpos": t.lexpos
                            }
                        })
                    while i[0].isdigit():
                        i = i[1:]
            else:
                if t.value[0].isdigit():
                    if not self.error:
                        self.error = []
                    self.error.append({
                        "code": "A-01",
                        "info": {
                            "line": t.lineno,
                            "value": t.value.split('\n')[0],
                            "lexpos": t.lexpos
                        }
                    })
                while t.value[0].isdigit():
                    t.value = t.value[1:]
            return t

        def t_ignore_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count('\n')

        def t_error(t):
            if not self.error:
                self.error = []
            self.error.append({
                "code": "A-02",
                "info": {
                    "line": t.lineno,
                    "value": t.value.split('\n')[0],
                    "lexpos": t.lexpos
                }
            })
            t.lexer.skip(1)

        lexer = lex(debug=debug)

        def p_programstruct(p):
            '''
            programstruct : program_head SEMICOLON program_body POINT
            '''
            p[0] = {
                "length": len(p),
                "type": "programstruct",
                "program_head": p[1],
                "program_body": p[3]
            }
            self.SymbolTable = {
                "constants": p[3]["SymbolTable"]["constants"],
                "variables": p[3]["SymbolTable"]["variables"],
                "subFunc": p[3]["SymbolTable"]["subFunc"]
            }

        def p_program_head(p):
            '''
            program_head : PROGRAM ID LPAREN idlist RPAREN
            '''
            p[0] = {
                "length": len(p),
                "type": "program_head",
                "ID": p[2],
                "idlist": p[4]
            }

        def p_program_head_program_id(p):
            '''
            program_head : PROGRAM ID
            '''
            p[0] = {
                "length": len(p),
                "type": "program_head",
                "ID": p[2],
                "idlist": []
            }

        def p_program_body(p):
            '''
            program_body : const_declarations var_declarations subprogram_declarations compound_statement
            '''
            p[0] = {
                "length": len(p),
                "type": "program_body",
                "const_declarations": p[1],
                "var_declarations": p[2],
                "subprogram_declarations": p[3],
                "compound_statement": p[4]
            }
            p[0]["SymbolTable"] = {
                "constants": p[1]["SymbolTable"] if p[1] else [],
                "variables": p[2]["SymbolTable"] if p[2] else [],
                "subFunc": p[3]["SymbolTable"] if p[3] else []
            }

        def p_idlist(p):
            '''
            idlist : idlist COM ID
            '''
            p[0] = {
                "length": len(p),
                "type": "idlist",
                "ids": p[1]["ids"] + [p[3]] if p[3] else p[1]["ids"]
            }
            if self.inSubFun and p[3] in list(self.subSymbol.keys()) and p[3]:
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[3],
                        "lexpos": p.lexer.lexpos
                    }
                })
            elif not self.inSubFun and p[3] in list(self.curSymbol.keys()) and p[3]:
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[3],
                        "lexpos": p.lexer.lexpos
                    }
                })

        def p_idlist_id(p):
            '''
            idlist : ID
            '''
            p[0] = {
                "length": len(p),
                "type": "idlist",
                "ids": [p[1]]
            }
            if self.inSubFun and p[1] in list(self.subSymbol.keys()) and p[1]:
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[1],
                        "lexpos": p.lexer.lexpos
                    }
                })
            elif not self.inSubFun and p[1] in list(self.curSymbol.keys()) and p[1]:
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[1],
                        "lexpos": p.lexer.lexpos
                    }
                })

        def p_const_declarations(p):
            '''
            const_declarations : CONST const_declaration SEMICOLON
                            | 
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "const_declarations",
                    "const_declaration": p[2]
                }
                p[0]["SymbolTable"] = p[2]["SymbolTable"]
                if not self.inSubFun:
                    # self.curSymbol = p[0]["SymbolTable"]
                    self.curSymbol = {}
                    for i in p[0]["SymbolTable"]:
                        self.curSymbol[i["token"]] = i["id"]
                else:
                    # self.subSymbol = self.subSymbol + p[0]["SymbolTable"]
                    for i in p[0]["SymbolTable"]:
                        self.subSymbol[i["token"]] = i["id"]
            else:
                p[0] = None

        def p_const_declaration(p):
            '''
            const_declaration : const_declaration SEMICOLON ID EQUAL const_value
            '''
            p[0] = {
                "length": len(p),
                "id": self.id,
                "type": "const_declaration",
                "values": p[1]["values"] + [{
                    "ID": p[3],
                    "const_value": p[5]
                }]
            }
            p[0]["SymbolTable"] = p[1]["SymbolTable"] + [{
                "id": self.id,
                "token": p[3],
                "type": "INTEGER" if type(p[5]) == int else ("REAL" if type(p[5]) == float else "CHAR"),
                "value": p[5],
                "positive": True if type(p[5]) != str and p[5] > 0 else False
            }]
            self.symbolMap[self.id] = {
                "id": self.id,
                "token": p[3],
                "type": "INTEGER" if type(p[5]) == int else ("REAL" if type(p[5]) == float else "CHAR"),
                "value": p[5],
                "positive": True if type(p[5]) != str and p[5] > 0 else False
            }
            self.id += 1
            if self.inSubFun and p[3] in list(self.subSymbol.keys()):
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[3],
                        "lexpos": p.lexer.lexpos
                    }
                })
            elif not self.inSubFun and p[3] in list(self.curSymbol.keys()):
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[3],
                        "lexpos": p.lexer.lexpos
                    }
                })

        def p_const_declaration_id(p):
            '''
            const_declaration : ID EQUAL const_value
            '''
            p[0] = {
                "length": len(p),
                "id": self.id,
                "type": "const_declaration",
                "values": [{
                    "ID": p[1],
                    "const_value": p[3]
                }]
            }
            p[0]["SymbolTable"] = [{
                "id": self.id,
                "token": p[1],
                "type": "digits" if type(p[3]) == int else ("NUM" if type(p[3]) == float else "LETTER"),
                "value": p[3],
                "positive": True if type(p[3]) != str and p[3]["value"] > 0 else False
            }]
            self.symbolMap[self.id] = {
                "id": self.id,
                "token": p[1],
                "type": "digits" if type(p[3]) == int else ("NUM" if type(p[3]) == float else "LETTER"),
                "value": p[3],
                "positive": True if type(p[3]) != str and p[3]["value"] > 0 else False
            }
            self.id += 1
            if self.inSubFun and p[1] in list(self.subSymbol.keys()):
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[1],
                        "lexpos": p.lexer.lexpos
                    }
                })
            elif not self.inSubFun and p[1] in list(self.curSymbol.keys()):
                if not self.error:
                    self.error = []
                self.error.append({
                    "code": "C-03",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[1],
                        "lexpos": p.lexer.lexpos
                    }
                })

        def p_const_value_addop(p):
            '''
            const_value : ADDOP NUM
                        | ADDOP DIGITS
            '''
            p[0] = {
                "length": len(p),
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
                "length": len(p),
                "type": "const_value",
                "_type": "NUM",
                "value": p[1]
            }

        def p_const_value_letter(p):
            '''
            const_value : QUO LETTER QUO
            '''
            p[0] = {
                "length": len(p),
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
                    "length": len(p),
                    "type": "var_declarations",
                    "var_declaration": p[2]
                }
                p[0]["SymbolTable"] = p[2]["SymbolTable"]
                if not self.inSubFun:
                    # self.curSymbol = self.curSymbol + p[0]["SymbolTable"]
                    for i in p[0]["SymbolTable"]:
                        self.curSymbol[i["token"]] = i["id"]
                else:
                    # self.subSymbol = self.subSymbol + p[0]["SymbolTable"]
                    for i in p[0]["SymbolTable"]:
                        self.subSymbol[i["token"]] = i["id"]
            else:
                p[0] = None

        def p_var_declaration(p):
            '''
            var_declaration : var_declaration SEMICOLON idlist COLON type
                            | idlist COLON type
            '''
            if len(p) == 6:
                p[0] = {
                    "length": len(p),
                    "type": "var_declaration",
                    "values": p[1]["values"] + [{
                        "idlist": p[3],
                        "type": p[5]
                    }]
                }
                p[0]["SymbolTable"] = p[1]["SymbolTable"]
                for i in p[3]["ids"]:
                    p[0]["SymbolTable"] += [{
                        "id": self.id,
                        "token": i,
                        "type": p[5]["SymbolTable"]["type"],
                        "isArray": p[5]["SymbolTable"]["isArray"],
                        "dimension": p[5]["SymbolTable"]["dimension"],
                        "size": p[5]["SymbolTable"]["size"],
                        "start": p[5]["SymbolTable"]["start"],
                        "recordTable": p[5]["SymbolTable"]["recordTable"]
                    }]
                    self.symbolMap[self.id] = {
                        "id": self.id,
                        "token": i,
                        "type": p[5]["SymbolTable"]["type"],
                        "isArray": p[5]["SymbolTable"]["isArray"],
                        "dimension": p[5]["SymbolTable"]["dimension"],
                        "size": p[5]["SymbolTable"]["size"],
                        "start": p[5]["SymbolTable"]["start"],
                        "recordTable": p[5]["SymbolTable"]["recordTable"]
                    }
                    self.id += 1
            else:
                p[0] = {
                    "length": len(p),
                    "id": self.id,
                    "type": "var_declaration",
                    "values": [{
                        "idlist": p[1],
                        "type": p[3]
                    }]
                }
                p[0]["SymbolTable"] = []
                for i in p[1]["ids"]:
                    p[0]["SymbolTable"] += [{
                        "id": self.id,
                        "token": i,
                        "type": p[3]["SymbolTable"]["type"],
                        "isArray": p[3]["SymbolTable"]["isArray"],
                        "dimension": p[3]["SymbolTable"]["dimension"],
                        "size": p[3]["SymbolTable"]["size"],
                        "start": p[3]["SymbolTable"]["start"],
                        "recordTable": p[3]["SymbolTable"]["recordTable"]
                    }]
                    self.symbolMap[self.id] = {
                        "id": self.id,
                        "token": i,
                        "type": p[3]["SymbolTable"]["type"],
                        "isArray": p[3]["SymbolTable"]["isArray"],
                        "dimension": p[3]["SymbolTable"]["dimension"],
                        "size": p[3]["SymbolTable"]["size"],
                        "start": p[3]["SymbolTable"]["start"],
                        "recordTable": p[3]["SymbolTable"]["recordTable"]
                    }
                    self.id += 1

        def p_type(p):
            '''
            type : basic_type
                | ARRAY LBRACKET period RBRACKET OF basic_type
                | RECORD multype END
            '''
            if not type(p[1]) == dict and p[1].upper() == 'ARRAY':
                p[0] = {
                    "length": len(p),
                    "type": "type",
                    "_type": "ARRAY",
                    "period": p[3],
                    "basic_type": p[5]
                }
                p[0]["SymbolTable"] = {
                    "type": p[6]["SymbolTable"],
                    "isArray": True,
                    "dimension": p[3]["SymbolTable"]["dimension"],
                    "size": p[3]["SymbolTable"]["size"],
                    "start": p[3]["SymbolTable"]["start"],
                    "recordTable": None
                }
            elif not type(p[1]) == dict and p[1].upper() == 'RECORD':
                p[0] = {
                    "length": len(p),
                    "type": "type",
                    "_type": "RECORD",
                    "multype": p[2]
                }
                p[0]["SymbolTable"] = {
                    "type": "RECORD",
                    "isArray": False,
                    "dimension": 0,
                    "size": [],
                    "start": [],
                    "recordTable": p[2]["SymbolTable"]
                }
            else:
                p[0] = {
                    "length": len(p),
                    "type": "type",
                    "_type": p[1]
                }
                p[0]["SymbolTable"] = {
                    "type": p[1]["SymbolTable"],
                    "isArray": False,
                    "dimension": 0,
                    "size": [],
                    "start": [],
                    "recordTable": None
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
                "_type": p[1].upper()
            }
            p[0]["SymbolTable"] = p[1].upper()

        def p_period(p):
            '''
            period : period COM DIGITS POINTTO DIGITS
                | DIGITS POINTTO DIGITS
            '''
            if len(p) == 6:
                if p[3] > p[5]:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-01",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": [p[3], p[5]],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                p[0] = {
                    "length": len(p),
                    "type": "period",
                    "values": p[1]["values"] + [{
                        "start": p[3],
                        "END": p[5]
                    }]
                }
                p[0]["SymbolTable"] = {
                    "dimension": p[1]["SymbolTable"]["dimension"] + 1,
                    "size": p[1]["SymbolTable"]["size"] + [p[5] - p[3] + 1],
                    "start": p[1]["SymbolTable"]["start"] + [p[3]],
                }
            else:
                if p[1] > p[3]:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-01",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": [p[1], p[3]],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                p[0] = {
                    "length": len(p),
                    "type": "period",
                    "values": [{
                        "start": p[1],
                        "END": p[3]
                    }]
                }
                p[0]["SymbolTable"] = {
                    "dimension": 1,
                    "size": [p[3] - p[1] + 1],
                    "start": [p[1]],
                }

        def p_subprogram_declarations(p):
            '''
            subprogram_declarations : subprogram_declarations subprogram SEMICOLON
                                    | 
            '''
            self.inSubFun = False
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "subprogram_declarations",
                    "subprograms": p[1]["subprograms"] + [p[2]] if p[2] else p[1]["subprograms"]
                }
                p[0]["SymbolTable"] = p[1]["SymbolTable"] + [p[2]["SymbolTable"]]
            else:
                p[0] = {
                    "length": len(p),
                    "type": "subprogram_declarations",
                    "subprograms": []
                }
                p[0]["SymbolTable"] = []

        def p_subprogram(p):
            '''
            subprogram : subprogram_head SEMICOLON subprogram_body
            '''
            p[0] = {
                "length": len(p),
                "id": p[1]["SymbolTable"]["id"],
                "type": "subprogram",
                "subprogram_head": p[1],
                "subprogram_body": p[3]
            }
            p[0]["SymbolTable"] = {
                "id": p[1]["SymbolTable"]["id"],
                "token": p[1]["SymbolTable"]["token"],
                "type": p[1]["SymbolTable"]["type"],
                "table": None
            }
            p[0]["SymbolTable"]["table"] = {
                "params": p[1]["SymbolTable"]["params"],
                "references": p[1]["SymbolTable"]["references"],
                "constants": p[3]["SymbolTable"]["constants"],
                "variables": p[1]["SymbolTable"]["variables"] + p[3]["SymbolTable"]["variables"],
            }

        def p_PROCEDURE(p):
            '''
            seen_PROCEDURE :
            '''
            self.inSubFun = True
            self.subSymbol = {}

        def p_FUNCTION(p):
            '''
            seen_FUNCTION :
            '''
            self.inSubFun = True
            self.subSymbol = {}

        def p_subprogram_head(p):
            '''
            subprogram_head : PROCEDURE seen_PROCEDURE ID formal_parameter
                            | FUNCTION seen_FUNCTION ID formal_parameter COLON basic_type 
            '''
            if not type(p[1]) == dict and p[1].upper() == 'PROCEDURE':
                p[0] = {
                    "length": len(p),
                    "type": "subprogram_head",
                    "_type": "PROCEDURE",
                    "ID": p[3],
                    "formal_parameter": p[4]
                }
                p[0]["SymbolTable"] = {
                    "id": self.id,
                    "token": p[3],
                    "type": None,
                    "params": p[4]["SymbolTable"]["params"],
                    "references": p[4]["SymbolTable"]["references"],
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                self.symbolMap[self.id] = {
                    "id": self.id,
                    "token": p[3],
                    "type": None,
                    "params": p[4]["SymbolTable"]["params"],
                    "references": p[4]["SymbolTable"]["references"],
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                self.subSymbol = {p[3]: self.id}
                self.subFuncMap[p[3]] = {
                    "type": None,
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                self.id += 1
            elif not type(p[1]) == dict and p[1].upper() == 'FUNCTION':
                p[0] = {
                    "length": len(p),
                    "type": "subprogram_head",
                    "_type": "FUNCTION",
                    "ID": p[3],
                    "formal_parameter": p[4],
                    "basic_type": p[6]
                }
                p[0]["SymbolTable"] = {
                    "id": self.id,
                    "token": p[3],
                    "type": p[6]["SymbolTable"],
                    "params": p[4]["SymbolTable"]["params"],
                    "references": p[4]["SymbolTable"]["references"],
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                self.symbolMap[self.id] = {
                    "id": self.id,
                    "token": p[3],
                    "type": p[6]["SymbolTable"],
                    "params": p[4]["SymbolTable"]["params"],
                    "references": p[4]["SymbolTable"]["references"],
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                # self.subSymbol = p[0]["SymbolTable"]["variables"]
                self.subSymbol = {p[3]: self.id}
                self.subFuncMap[p[3]] = {
                    "type": p[6]["SymbolTable"],
                    "variables": p[4]["SymbolTable"]["variables"],
                }
                self.id += 1
            for i in p[0]["SymbolTable"]["variables"]:
                self.subSymbol[i["token"]] = i["id"]

        def p_formal_parameter(p):
            '''
            formal_parameter : LPAREN parameter_list RPAREN
                            | 
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "formal_parameter",
                    "parameter_list": p[2]
                }
                p[0]["SymbolTable"] = {
                    "params": p[2]["SymbolTable"]["params"],
                    "references": p[2]["SymbolTable"]["references"],
                    "variables": p[2]["SymbolTable"]["variables"],
                }
            else:
                p[0] = {
                    "length": len(p),
                    "type": "formal_parameter",
                    "parameter_list": None
                }
                p[0]["SymbolTable"] = {
                    "params": 0,
                    "references": [],
                    "variables": [],
                }

        def p_parameter_list(p):
            '''
            parameter_list : parameter_list SEMICOLON parameter
                        | parameter
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "parameter_list",
                    "parameters": p[1]["parameters"] + [p[3]] if p[3] else p[1]["parameters"]
                }
                p[0]["SymbolTable"] = {
                    "params": p[1]["SymbolTable"]["params"] + p[1]["SymbolTable"]["size"],
                    "references": p[1]["SymbolTable"]["references"] + [p[3]["SymbolTable"]["references"]],
                    "variables": p[1]["SymbolTable"]["variables"] + [p[3]["SymbolTable"]["variables"]],
                }
            else:
                p[0] = {
                    "length": len(p),
                    "type": "parameter_list",
                    "parameters": [p[1]]
                }
                p[0]["SymbolTable"] = {
                    "params": p[1]["SymbolTable"]["size"],
                    "references": [p[1]["SymbolTable"]["references"]],
                    "variables": p[1]["SymbolTable"]["variables"],
                }

        def p_parameter(p):
            '''
            parameter : var_parameter
                    | value_parameter
            '''
            p[0] = {
                "length": len(p),
                "type": "parameter",
                "value": p[1]
            }
            p[0]["SymbolTable"] = p[1]["SymbolTable"]

        def p_var_parameter(p):
            '''
            var_parameter : VAR value_parameter
            '''
            p[0] = {
                "length": len(p),
                "type": "var_parameter",
                "value_parameter": p[2]
            }
            p[0]["SymbolTable"] = {
                "references": [True for i in range(p[2]["SymbolTable"]["size"])],
                "variables": p[2]["SymbolTable"]["variables"],
                "size": p[2]["SymbolTable"]["size"]
            }

        def p_value_parameter(p):
            '''
            value_parameter : idlist COLON basic_type
            '''
            p[0] = {
                "length": len(p),
                "type": "value_parameter",
                "idlist": p[1],
                "basic_type": p[3]
            }
            p[0]["SymbolTable"] = {
                "references": [False for i in range(len(p[1]["ids"]))],
                "size": len(p[1]["ids"]),
                "variables": []
            }
            for i in p[1]["ids"]:
                p[0]["SymbolTable"]["variables"] = p[0]["SymbolTable"]["variables"] + [{
                    "id": self.id,
                    "token": i,
                    "type": p[3]["SymbolTable"],
                    "isArray": False,
                    "dimension": 0,
                    "size": [],
                    "start": [],
                    "recordType": None,
                }]
                self.symbolMap[self.id] = {
                    "id": self.id,
                    "token": i,
                    "type": p[3]["SymbolTable"],
                    "isArray": False,
                    "dimension": 0,
                    "size": [],
                    "start": [],
                    "recordType": None,
                }
                self.id += 1

        def p_subprogram_body(p):
            '''
            subprogram_body : const_declarations var_declarations compound_statement
            '''
            p[0] = {
                "length": len(p),
                "type": "subprogram_body",
                "const_declarations": p[1],
                "var_declarations": p[2],
                "compound_statement": p[3]
            }
            p[0]["SymbolTable"] = {
                "constants": p[1]["SymbolTable"] if p[1] else [],
                "variables": p[2]["SymbolTable"] if p[2] else [],
            }

        def p_compound_statement(p):
            '''
            compound_statement : BEGIN statement_list END
            '''
            p[0] = {
                "length": len(p),
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
                    "length": len(p),
                    "type": "statement_list",
                    "statements": p[1]["statements"] + [p[3]] if p[3] else p[1]["statements"]
                }
            else:
                p[0] = {
                    "length": len(p),
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
                    "length": len(p),
                    "type": "statement",
                    "_type": "IF",
                    "expression": p[2],
                    "statement": p[4],
                    "else_part": p[5]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'FOR':
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "FOR",
                    "ID": p[2],
                    "ASSIGNOP": p[3],
                    "expression": p[4],
                    "to_expression": p[6],
                    "statement": p[8]
                }
                if p[2] not in list(self.curSymbol.keys()) and self.inSubFun and p[2] not in list(self.subSymbol.keys()):
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-11",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": p[2],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                id = self.search_symbol(p[2])
                if id:
                    if p[4]["__type"] == "UNDEFINED":
                        if not self.error:
                            self.error = []
                        self.error += [{
                            "code": "C-10",
                            "info": {
                                "line": p.lexer.lineno,
                                "value": p[2],
                                "lexpos": p.lexer.lexpos
                            }
                        }]
                    elif id["type"] not in safe_assign[p[4]["__type"]]:
                        if id["type"] in warn_assign[p[4]["__type"]]:
                            if not self.warning:
                                self.warning = []
                            self.warning += [{
                                "code": "W-01",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [p[2], id["type"], p[4]["__type"]],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]
                        else:
                            if not self.error:
                                self.error = []
                            self.error += [{
                                "code": "C-04",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [p[2], id["type"], p[4]["__type"]],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]
            elif not type(p[1]) == dict and p[1].upper() == 'READ':
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "READ",
                    "variable_list": p[3]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'WRITE':
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "WRITE",
                    "expression_list": p[3]
                }
            elif not type(p[1]) == dict and p[1].upper() == 'WHILE':
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "WHILE",
                    "expression": p[2],
                    "statement": p[4]
                }
            elif p[1]["type"] == "variable":
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "variable",
                    "variable": p[1],
                    "ASSIGNOP": p[2],
                    "expression": p[3]
                }
                if p[1]["__type"] == "UNDEFINED":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-11",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": p[1]["ID"],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                id = self.search_symbol(p[1]["ID"])
                if p[3]["__type"] == "UNDEFINED":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-10",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": p[1]["ID"],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                elif id:
                    if id["type"] not in safe_assign[p[3]["__type"]]:
                        if id["type"] in warn_assign[p[3]["__type"]]:
                            if not self.warning:
                                self.warning = []
                            self.warning += [{
                                "code": "W-01",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [p[1]["ID"], id["type"], p[3]["__type"]],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]
                        else:
                            if not self.error:
                                self.error = []
                            self.error += [{
                                "code": "C-04",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [p[1]["ID"], id["type"], p[3]["__type"]],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]
                else:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-11",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": p[1]["ID"],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
            elif p[1]["type"] == "procedure_call":
                p[0] = {
                    "length": len(p),
                    "type": "statement",
                    "_type": "procedure_call",
                    "procedure_call": p[1]
                }
            elif p[1]["type"] == "compound_statement":
                p[0] = {
                    "length": len(p),
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
                    "length": len(p),
                    "type": "variable_list",
                    "variables": p[1]["variables"] + [p[3]] if p[3] else p[1]["variables"]
                }
            else:
                p[0] = {
                    "length": len(p),
                    "type": "variable_list",
                    "variables": [p[1]]
                }

        def p_variable(p):
            '''
            variable : ID id_varpart
            '''
            p[0] = {
                "length": len(p),
                "type": "variable",
                "__type": self.search_symbol(p[1])["type"] if self.search_symbol(p[1]) else "UNDEFINED",
                "ID": p[1],
                "id_varpart": p[2]
            }
            if type(p[1]) == str and p[1] not in list(self.curSymbol.keys()) and not (self.inSubFun and p[1] in list(self.subSymbol.keys())):

                if not self.error:
                    self.error = []
                self.error += [{
                    "code": "C-02",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": p[1],
                        "lexpos": p.lexer.lexpos
                    }
                }]
            elif type(p[1]) == list:
                possiable_token = list(self.curSymbol.keys(
                )) + (list(self.subSymbol.keys()) if self.inSubFun else [])
                i = p[1][0]
                if i not in possiable_token:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-02",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": i,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                elif self.search_symbol(i)["recordTable"]:
                    possiable_token = [j["token"] for j in self.search_symbol(
                        i)["recordTable"]["variables"]]
                    record_table = self.search_symbol(i)["recordTable"]
                for j in p[1][1:]:
                    if j not in possiable_token:
                        if not self.error:
                            self.error = []
                        self.error += [{
                            "code": "C-02",
                            "info": {
                                "line": p.lexer.lineno,
                                "value": j,
                                "lexpos": p.lexer.lexpos
                            }
                        }]
                    elif self.search_symbol(j, record_table)["recordTable"]:
                        possiable_token = [k["token"] for k in self.search_symbol(
                            j, record_table)["recordTable"]["variables"]]
                        record_table = self.search_symbol(
                            j, record_table)["recordTable"]
                    else:
                        p[0]["__type"] = self.search_symbol(
                            j, record_table)["type"]

        def p_id_varpart(p):
            '''
            id_varpart : LBRACKET expression_list RBRACKET
                       | 
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "id_varpart",
                    "expression_list": p[2]
                }
            else:
                p[0] = {
                    "length": len(p),
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
                    "length": len(p),
                    "type": "procedure_call",
                    "ID": p[1]
                }
            else:
                p[0] = {
                    "length": len(p),
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
                    "length": len(p),
                    "type": "else_part",
                    "statement": p[2]
                }
            else:
                p[0] = {
                    "length": len(p),
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
                    "length": len(p),
                    "type": "expression_list",
                    "__type": p[1]["__type"] + [p[3]["__type"] if p[3] else None],
                    "expressions": p[1]["expressions"] + [p[3]] if p[3] else p[1]["expressions"]
                }
            else:
                p[0] = {
                    "length": len(p),
                    "type": "expression_list",
                    "__type": [p[1]["__type"]],
                    "expressions": [p[1]]
                }

        def p_expression(p):
            '''
            expression : simple_expression RELOP simple_expression
                       | simple_expression
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "expression",
                    "__type": "BOOLEAN",
                    "simple_expression_1": p[1],
                    "RELOP": p[2],
                    "simple_expression_2": p[3]
                }
                if p[1]["__type"] == "UNDEFINED" or p[3]["__type"] == "UNDEFINED":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-09",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                elif p[1]["__type"] == "RECORD" or p[3]["__type"] == "RECORD":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-05",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
            else:
                p[0] = {
                    "length": len(p),
                    "type": "expression",
                    "__type": p[1]["__type"],
                    "simple_expression": p[1]
                }

        def p_expression_equal(p):
            '''
            expression : simple_expression EQUAL simple_expression
            '''
            p[0] = {
                "length": len(p),
                "type": "expression",
                "simple_expression_1": p[1],
                "RELOP": p[2],
                "simple_expression_2": p[3]
            }
            if p[1]["__type"] == "RECORD" or p[3]["__type"] == "RECORD":
                if not self.error:
                    self.error = []
                self.error += [{
                    "code": "C-05",
                    "info": {
                        "line": p.lexer.lineno,
                        "lexpos": p.lexer.lexpos
                    }
                }]

        def p_simple_expression(p):
            '''
            simple_expression : simple_expression ADDOP term
                              | term
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "simple_expression",
                    "simple_expression": p[1],
                    "ADDOP": p[2],
                    "term": p[3]
                }
                if p[1]["__type"] == "UNDEFINED" or p[3]["__type"] == "UNDEFINED":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-07",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "UNDEFINED"
                elif p[1]["__type"] == "RECORD" or p[3]["__type"] == "RECORD":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-06",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "RECORD"
                elif p[1]["__type"] == "REAL" or p[3]["__type"] == "REAL":
                    p[0]["__type"] = "REAL"
                elif p[1]["__type"] == "INTEGER" or p[3]["__type"] == "INTEGER":
                    p[0]["__type"] = "INTEGER"
                elif p[1]["__type"] == "CHAR" or p[3]["__type"] == "CHAR":
                    p[0]["__type"] = "CHAR"
                elif p[1]["__type"] == "BOOLEAN" or p[3]["__type"] == "BOOLEAN":
                    p[0]["__type"] = "BOOLEAN"
                else:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-08",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": [p[1]["__type"], p[3]["__type"]],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "UNDEFINED"
            else:
                p[0] = {
                    "length": len(p),
                    "type": "simple_expression",
                    "__type": p[1]["__type"],
                    "term": p[1]
                }

        def p_term(p):
            '''
            term : term MULOP factor
                 | factor
            '''
            if len(p) == 4:
                p[0] = {
                    "length": len(p),
                    "type": "term",
                    "term": p[1],
                    "factor": p[3]
                }
                if p[1]["__type"] == "UNDEFINED" or p[3]["__type"] == "UNDEFINED":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-07",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "UNDEFINED"
                elif p[1]["__type"] == "RECORD" or p[3]["__type"] == "RECORD":
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-06",
                        "info": {
                            "line": p.lexer.lineno,
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "RECORD"
                elif p[1]["__type"] == "REAL" or p[3]["__type"] == "REAL":
                    p[0]["__type"] = "REAL"
                elif p[1]["__type"] == "INTEGER" or p[3]["__type"] == "INTEGER":
                    p[0]["__type"] = "INTEGER"
                elif p[1]["__type"] == "CHAR" or p[3]["__type"] == "CHAR":
                    p[0]["__type"] = "CHAR"
                elif p[1]["__type"] == "BOOLEAN" or p[3]["__type"] == "BOOLEAN":
                    p[0]["__type"] = "BOOLEAN"
                else:
                    if not self.error:
                        self.error = []
                    self.error += [{
                        "code": "C-08",
                        "info": {
                            "line": p.lexer.lineno,
                            "value": [p[1]["__type"], p[3]["__type"]],
                            "lexpos": p.lexer.lexpos
                        }
                    }]
                    p[0]["__type"] = "UNDEFINED"
            else:
                p[0] = {
                    "length": len(p),
                    "type": "term",
                    "__type": p[1]["__type"],
                    "factor": p[1]
                }

        def p_factor_num(p):
            '''
            factor : NUM
                   | DIGITS
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "NUM",
                "__type": "INTEGER" if type(p[1]) == int else "REAL",
                "NUM": p[1]
            }

        def p_factor_variable(p):
            '''
            factor : variable
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "variable",
                "__type": p[1]["__type"],
                "variable": p[1]
            }

        def p_factor_procedure_id(p):
            '''
            factor : ID LPAREN expression_list RPAREN
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "procedure_id",
                "__type": self.subFuncMap[p[1]]["type"],
                "ID": p[1],
                "expression_list": p[3]
            }
            if len(p[3]["__type"]) != len(self.subFuncMap[p[1]]["variables"]):
                if not self.error:
                    self.error = []
                self.error += [{
                    "code": "C-12",
                    "info": {
                        "line": p.lexer.lineno,
                        "value": [len(p[3]["__type"]), len(self.subFuncMap[p[1]]["variables"])],
                        "lexpos": p.lexer.lexpos
                    }
                }]
            else:
                for i in range(len(p[3]["__type"])):
                    from_type = p[3]["__type"][i]
                    to_type = self.subFuncMap[p[1]]["variables"][i]["type"]
                    if from_type == "UNDEFINED":
                        if not self.error:
                            self.error = []
                        self.error += [{
                            "code": "C-13",
                            "info": {
                                "line": p.lexer.lineno,
                                "value": [from_type, to_type],
                                "lexpos": p.lexer.lexpos
                            }
                        }]
                    elif to_type not in safe_assign[from_type]:
                        if to_type in warn_assign[from_type]:
                            if not self.warning:
                                self.warning = []
                            self.warning += [{
                                "code": "W-02",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [self.subFuncMap[p[1]]["variables"][i]['token'], from_type, to_type],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]
                        else:
                            if not self.error:
                                self.error = []
                            self.error += [{
                                "code": "C-14",
                                "info": {
                                    "line": p.lexer.lineno,
                                    "value": [self.subFuncMap[p[1]]["variables"][i]['token'], from_type, to_type],
                                    "lexpos": p.lexer.lexpos
                                }
                            }]

        def p_factor_expression(p):
            '''
            factor : LPAREN expression RPAREN
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "expression",
                "__type": p[2]["__type"],
                "expression": p[2]
            }

        def p_factor_not(p):
            '''
            factor : NOT factor
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "NOT",
                "__type": p[2]["__type"],
                "factor": p[2]
            }

        def p_factor_uminus(p):
            '''
            factor : UMINUS factor
                   | ADDOP factor
            '''
            p[0] = {
                "length": len(p),
                "type": "factor",
                "_type": "UMINUS" if p[1] == "-" else "NORMAL",
                "__type": p[2]["__type"],
                "factor": p[2]
            }

        def p_multype(p):
            '''
            multype : multype ID COLON type SEMICOLON
                    | ID COLON type SEMICOLON
            '''
            if len(p) == 6:
                p[0] = {
                    "length": len(p),
                    "id": self.id,
                    "type": "multype",
                    "multype": p[1],
                    "ID": p[1]["ID"] + [p[2]],
                    "type": p[1]["type"] + [p[4]]
                }
                p[0]["SymbolTable"] = {
                    "variables": p[1]["SymbolTable"]["variables"] + [{
                        "id": self.id,
                        "token": p[2],
                        "type": p[4]["SymbolTable"]["type"],
                        "isArray": p[4]["SymbolTable"]["isArray"],
                        "dimension": p[4]["SymbolTable"]["dimension"],
                        "size": p[4]["SymbolTable"]["size"],
                        "start": p[4]["SymbolTable"]["start"],
                        "recordTable": p[4]["SymbolTable"]["recordTable"]
                    }]
                }
                self.symbolMap[self.id] = {
                    "id": self.id,
                    "token": p[2],
                    "type": p[4]["SymbolTable"]["type"],
                    "isArray": p[4]["SymbolTable"]["isArray"],
                    "dimension": p[4]["SymbolTable"]["dimension"],
                    "size": p[4]["SymbolTable"]["size"],
                    "start": p[4]["SymbolTable"]["start"],
                    "recordTable": p[4]["SymbolTable"]["recordTable"]
                }
                self.id += 1
            else:
                p[0] = {
                    "length": len(p),
                    "id": self.id,
                    "type": "multype",
                    "ID": [p[1]],
                    "type": [p[3]]
                }
                p[0]["SymbolTable"] = {
                    "variables": [{
                        "id": self.id,
                        "token": p[1],
                        "type": p[3]["SymbolTable"]["type"],
                        "isArray": p[3]["SymbolTable"]["isArray"],
                        "dimension": p[3]["SymbolTable"]["dimension"],
                        "size": p[3]["SymbolTable"]["size"],
                        "start": p[3]["SymbolTable"]["start"],
                        "recordTable": p[3]["SymbolTable"]["recordTable"]
                    }]
                }
                self.symbolMap[self.id] = {
                    "id": self.id,
                    "token": p[1],
                    "type": p[3]["SymbolTable"]["type"],
                    "isArray": p[3]["SymbolTable"]["isArray"],
                    "dimension": p[3]["SymbolTable"]["dimension"],
                    "size": p[3]["SymbolTable"]["size"],
                    "start": p[3]["SymbolTable"]["start"],
                    "recordTable": p[3]["SymbolTable"]["recordTable"]
                }
                self.id += 1

        def p_error(p):
            if not self.error:
                self.error = []
            self.error.append({
                "code": "B-01",
                "info": {
                    "line": p.lineno,
                    "value": p.value,
                    "lexpos": p.lexpos
                }
            })

        self.parser = yacc(debug=debug, write_tables=write_tables)

    def search_symbol(self, token, recordTable=None):
        if recordTable is None:
            if self.inSubFun and token in list(self.subSymbol.keys()):
                return self.symbolMap[self.subSymbol[token]]
            elif token in list(self.curSymbol.keys()):
                return self.symbolMap[self.curSymbol[token]]
        else:
            for i in recordTable["variables"]:
                if i["token"] == token:
                    return i

    def _removeSymbolTable(self, p):
        if type(p) == dict:
            if "SymbolTable" in p:
                del p["SymbolTable"]
            for key in p:
                if type(p[key]) == list:
                    for item in p[key]:
                        if type(item) == dict:
                            self._removeSymbolTable(item)
                elif type(p[key]) == dict:
                    self._removeSymbolTable(p[key])

    def _processAST(self, ast):
        # add father node
        for key in ast:
            if type(ast[key]) == dict and not key == "father":
                ast[key]["father"] = ast
                self._processAST(ast[key])

    def parse(self, data):
        self.SymbolTable = {
            "constants": [],
            "variables": [],
            "subFunc": []
        }
        self.error = []
        self.warning = []
        self.curSymbol = {}
        self.subSymbol = {}
        self.inSubFun = False
        self.id = 0
        self.symbolMap = {}
        self.subFuncMap = {}
        ast = None
        # try:
        ast = self.parser.parse(data)
        # except:
        #     pass
        self._removeSymbolTable(ast)
        ast_raw = copy.deepcopy(ast)
        if ast:
            self._processAST(ast)
        return {
            "ast": ast_raw,
            "symbolTable": self.SymbolTable,
            "error": self.error,
            "warning": self.warning,
            "ast_prod": ast
        }
