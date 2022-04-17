import copy
from ctypes.wintypes import tagRECT
import json

from numpy import fromstring


class CodeGenerator:
    targetCode = ''  # 目标代码
    domain = []  # 作用域栈
    headFile = []  # 头文件
    ast = None  # 抽象语法树
    symbolTable = None  # 符号表

    def __init__(self, _ast, _symbolTable):
        ast = _ast
        symbolTable = _symbolTable

    # 将生成的代码添加进目标代码
    def code_append(self, code):
        self.target_code += code

    # 代码格式化：添加换行、缩进
    def code_format(self):
        indent = 0
        in_quote = False
        in_small = 0
        add_indent = False
        code_list = list(self.targetCode)
        for it in code_list:
            add_indent = False
            if it == '\"' or it == '\'':
                in_quote = ~in_quote
            if it == '(':
                in_small += 1
            if it == ')':
                in_small -= 1
            if in_quote == False and in_small == 0:
                if it == '{':
                    it += '\n'
                    indent += 1
                    add_indent = True
                elif it == '}':
                    it += '\n'
                    indent -= 1
                    add_indent = True
                elif it == ';':
                    it += '\n'
                    add_indent = True
            if add_indent == True:
                for i in range(0, indent):
                    it += '\t'
        self.targetCode = ''.join(code_list)

    # 将分析阶段得到的头文件列表加到目标代码中
    def add_headfile(self):
        for it in self.headFile:
            self.targetCode = it + self.targetCode

    # programstruct : program_head ; program_body .
    def g_programstruct(self, node):
        result = ""
        # self.g_program_head(node["program_head"])
        result.append(self.g_program_head(node["program_head"]))
        # self.g_program_body(node["program_body"])
        result.append(self.g_program_body(node["program_body"]))

        self.targetCode = result

        self.domain.pop()

    def g_program_head(self, node):
        pass

    def g_program_body(self, node):
        pass

    def g_idlist(self, node):
        pass

    def g_const_declarations(self, node):
        pass

    def g_const_declaration(self, node):
        pass

    def g_const_value(self, node):
        pass

    def g_var_declarations(self, node):
        pass

    def g_var_declaration(self, node):
        pass

    def g__type(self, node):
        pass

    def g_basic_type(self, node):
        pass

    def g_period(self, node):
        pass

    def g_record_type(self, node):
        pass

    def g_field_list(self, node):
        pass

    def g_fixed_fields(self, node):
        pass

    def g_subprogram_declarations(self, node):
        pass

    def g_subprogram(self, node):
        pass

    def g_subprogram_head(self, node):
        pass

    def g_formal_parameter(self, node):
        pass

    def g_parameter_list(self, node):
        pass

    def g_parameter(self, node):
        pass

    def g_var_parameter(self, node):
        pass

    def g_value_parameter(self, node):
        pass

    def g_subprogram_body(self, node):
        pass

    # <---------------------------------分割线------------------------------------>
    def g_compound_statement(self, node):
        '''
        compound_statement -> begin statement_list end
        compound_statement -> {statement_list}
        '''
        assert node["type"] == "compound_statement"
        result = ""
        result += "{"
        result += self.g_statement_list(node["statement_list"])
        result += "}"
        return result

    def g_statement_list(self, node):
        '''
        statement_list -> statement_list ; statement | statement
        statement_list -> statement_list statement | statement
        '''
        assert node["type"] == "statement_list", "type:{}".format(node["type"])
        result = ""
        assert len(node["statements"]) > 0
        if len(node["statements"]) == 1:
            result += self.g_statement(node["statements"][0])
        elif len(node["statements"]) > 1:
            tmp_node = copy.deepcopy(node)
            statement = tmp_node["statements"].pop()
            result += self.g_statement_list(tmp_node)
            # result += " "
            result += self.g_statement(statement)
        return result

    def g_statement(self, node):
        '''
        Pascal:                                                     C:
        statement ->                                                statement ->
        variable assignop expression                                variable = expression
        | procedure_call                                            | procedure_call
        | compound_statement                                        | compound_statement
        | if expression then statement else_part                    | if(expression){statement}else_part
        | for id assignop expression to expression do statement     | for(id=expression;id<expression;id++){statement}
        | read ( variable_list )                                    | scanf("format_string",var1,var2)
        | write ( expression_list )                                 | printf("format_string",var1,var2)
        | while expression do statement                             | while(expression){statement}
        | ε                                                         | TBD
        '''
        if(node == None):
            return ""
        assert node["_type"] in ["variable", "procedure_call", "compound_statement",
                                 "IF", "FOR", "READ", "WRITE", "WHILE"], "_type:{}".format(node["_type"])
        format_tag_map = {"INTEGER": "%d",
                          "REAL": "%f", "BOOLEAN": "%d", "CHAR": "%c"}
        type = node["_type"]
        result = ""
        if type == "variable":
            result += self.g_variable(node["variable"])[0]
            result += "="
            result += self.g_expression(node["expression"])
        elif type == "procedure_call":
            pass
        elif type == "compound_statement":
            pass
        elif type == "IF":
            result += "if("
            result += self.g_expression(node["expression"])
            result += ")"
            result += "{"
            result += self.g_statement(node["statement"])
            result += "}"
            result += self.g_else_part(node["else_part"])
            pass
        elif type == "FOR":
            result += "for("
            result += node["ID"]
            result += "="
            result += self.g_expression(node["expression"])
            result += ";"
            result += node["ID"]
            result += "<"
            result += self.g_expression(node["to_expression"])
            result += node["ID"]
            result += "++"
            result += "){"
            result += self.g_statement(node["statement"])
            result += "}"
            pass
        elif type == "READ":
            var, __type = self.g_variable_list(node["variable_list"])
            var = var.split(",")
            assert len(var) == len(__type)
            assert len(var) > 0
            format_string = ""
            var_string = ""
            for i in range(len(var)):
                format_string += "{}".format(format_tag_map[__type[i]])
                var_string += "&{},".format(var[i])
            var_string = var_string[0: -1]
            result += "scanf(\"{}\",{})".format(format_string, var_string)
            pass
        elif type == "WRITE":
            var = self.g_expression_list(node["expression_list"])
            var = var.split(",")
            __type = node["expression_list"]["__type"]
            print(var, __type)
            assert len(var) == len(__type), len(var)
            assert len(var) > 0
            format_string = ""
            var_string = ""
            for i in range(len(var)):
                format_string += "{}: {}\n".format(var[i],
                                                   format_tag_map[__type[i]])
                var_string += "{},".format(var[i])
            var_string = var_string[0: -1]
            result += "printf(\"{}\",{})".format(format_string, var_string)
            pass
        elif type == "WHILE":
            pass
        if type in ["variable", "procedure_call", "READ", "WRITE"]:
            result += ";"
        return result

    def g_variable_list(self, node):
        """
        variable_list -> variable_list , variable | variable
        """
        assert node["type"] == "variable_list", "type:{}".format(node["type"])
        result = ""
        typelist = []
        assert len(node["variables"]) > 0
        if len(node["variables"]) == 1:
            var, __type = self.g_variable(node["variables"][0])
            result += var
            typelist.append(__type)
        elif len(node["variables"]) > 1:
            tmp_node = copy.deepcopy(node)
            variable = tmp_node["variables"].pop()
            var, __type = self.g_variable_list(tmp_node)
            typelist.extend(__type)
            result += var
            result += ","
            var, __type = self.g_variable(variable)
            result += var
            typelist.append(__type)
        return result, typelist
        pass

    def g_variable(self, node):
        """
        variable -> id id_varpart
        """
        assert node["type"] == "variable"
        result = ""
        result += node["ID"]
        result += self.g_id_varpart(node["id_varpart"])
        return result, node["__type"]

    def g_id_varpart(self, node):
        """
        id_varpart -> [ expression_list ] | ε       #[1,2,3] 
        id_varpart -> expression_list | ε           #[1][2][3]
        """
        assert node["type"] == "id_varpart"
        result = ""
        if node["expression_list"] == None:
            return result
        else:
            result += self.g_expression_list(
                node["expression_list"], for_array=True)
            return result
        pass

    def g_procedure_call(self, node):
        """
        procedure_call -> id | id ( expression_list )
        """
        pass

    def g_else_part(self, node):
        """
        else_part -> else statement | ε
        """
        assert node["type"] == "else_part"
        result = ""
        if node["length"] == 3:
            result += "else{"
            result += self.g_statement(node["statement"])
            result += "}"
        return result
        pass

    def g_expression_list(self, node, for_array: bool = False, return_list=False):
        """
        expression_list -> expression_list , expression | expression
        """
        assert node["type"] == "expression_list"
        assert len(node["expressions"]) > 0
        result = ""
        result_list = []  # for printf format string
        if for_array == True:
            if len(node["expressions"]) == 1:
                tmp = "[{}]".format(self.g_expression(node["expressions"][0]))
                result += tmp
                result_list.append(tmp)
            elif len(node["expressions"]) > 1:
                tmp_node = copy.deepcopy(node)
                expression = tmp_node["expressions"].pop()
                tmp = "{}[{}]".format(self.g_expression_list(
                    tmp_node, for_array=for_array), self.g_expression(expression))
                result += tmp
                result_list.append(tmp)

        else:
            if len(node["expressions"]) == 1:
                tmp = self.g_expression(node["expressions"][0])
                result += tmp
                result_list.append(tmp)

            elif len(node["expressions"]) > 1:
                tmp_node = copy.deepcopy(node)
                expression = tmp_node["expressions"].pop()
                result += self.g_expression_list(tmp_node, for_array=for_array)
                result += ","
                result += self.g_expression(expression)
        return result

    def g_expression(self, node):
        """
        expression -> simple_expression relop simple_expression | simple_expression | simple_expression equal simple_expression
        """
        assert node["type"] == "expression"
        assert node["length"] in [2, 4]
        result = ""
        if node["length"] == 2:
            assert node["simple_expression"], "key missing: simple_expression"
            result += self.g_simple_expression(node["simple_expression"])
        elif node["length"] == 4:
            assert node["simple_expression_1"], "key missing: simple_expression_1"
            assert node["RELOP"], "key missing: RELOP"
            assert node["simple_expression_2"], "key missing: simple_expression_2"
            result += self.g_simple_expression(node["simple_expression_1"])
            if node["RELOP"] == "=":
                result += "=="
            else:
                result += node["RELOP"]
            result += self.g_simple_expression(node["simple_expression_2"])
        return result

    def g_simple_expression(self, node):
        """
        simple_expression -> simple_expression addop term | term
        """
        assert node["type"] == "simple_expression"
        assert node["length"] in [2, 4]
        result = ""
        if node["length"] == 2:
            assert node["term"], "key missing: term"
            result += self.g_term(node["term"])
            pass
        elif node["length"] == 4:
            assert node["simple_expression"], "key missing: simple_expression"
            assert node["ADDOP"], "key missing: ADDOP"
            assert node["term"], "key missing: term"
            result += self.g_simple_expression(node["simple_expression"])
            if node["ADDOP"].lower() == "or":
                result += "||"
            else:
                result += node["ADDOP"]
            result += self.g_term(node["term"])
            pass
        return result

    def g_term(self, node):
        """
        term -> term mulop factor | factor
        """
        assert node["type"] == "term"
        assert node["length"] in [2, 4]
        result = ""
        if node["length"] == 2:
            assert node["factor"], "key missing: factor"
            result += self.g_factor(node["factor"])
            pass
        elif node["length"] == 4:
            assert node["term"], "key missing: term"
            assert node["MULOP"], "key missing: MULOP"
            assert node["factor"], "key missing: factor"
            result += self.g_term(node["term"])
            if node["MULOP"].lower() == "mod":
                result += " mod "
            elif node["MULOP"].lower() in ["/", "div"]:
                result += "/"
            elif node["MULOP"].lower() == "and":
                result += "&&"
            else:
                result += node["MULOP"]
            result += self.g_factor(node["factor"])
            pass
        return result

    def g_factor(self, node):
        """
        factor -> num | digits | variable | id ( expression_list ) | ( expression ) | not factor | uminus factor | addop factor
        """
        assert node["type"] == "factor"
        assert node["_type"] in ["NUM", "variable", "procedure_id",
                                 "expression", "NOT", "UMINUS", "NORMAL"]
        result = ""
        type = node["_type"]
        if type == "NUM":
            result += str(node["NUM"])
            pass
        elif type == "variable":
            result += self.g_variable(node["variable"])[0]
            pass
        elif type == "procedure_id":
            result += "{}({})".format(node["ID"],
                                      self.g_expression_list(node["expression_list"]))
            pass
        elif type == "expression":
            result += "("
            result += self.g_expression_list(node["expression"])
            result += ")"
            pass
        elif type == "NOT":
            result += "!"
            result += self.g_factor(node["factor"])
            pass
        elif type == "UMINUS":
            result += "-"
            result += self.g_factor(node["factor"])
            pass
        elif type == "NORMAL":
            result += self.g_factor(node["factor"])
            pass

        return result

    def g_multype(self, node):
        """
        multype -> multype ID COLON type SEMICOLON | ID COLON type SEMICOLON
        """
        return "multype TBD"
        pass

    def code_generate(self):
        self.g_programstruct(self.ast)  # 从programstruct节点开始生成目标代码
        self.code_format()  # 代码格式化
        self.add_headfile()  # 添加头文件
        return self.targetCode  # 返回生成的目标代码

    def compound_statement_test(self, node: dict):
        result = self.g_compound_statement(node)
        print(result)
        # self.targetCode = result
        # self.code_format()
        # print(self.targetCode)


_ast = {
    "length": 5,
    "type": "programstruct",
    "program_head": {
        "length": 6,
        "type": "program_head",
        "ID": "example",
        "idlist": {
            "length": 4,
            "type": "idlist",
            "ids": [
                "input",
                "output"
            ]
        }
    },
    "program_body": {
        "length": 5,
        "type": "program_body",
        "const_declarations": None,
        "var_declarations": {
            "length": 4,
            "type": "var_declarations",
            "var_declaration": {
                "length": 4,
                "id": 0,
                "type": "var_declaration",
                "values": [
                    {
                        "idlist": {
                            "length": 4,
                            "type": "idlist",
                            "ids": [
                                "x",
                                "y"
                            ]
                        },
                        "type": {
                            "length": 2,
                            "type": "type",
                            "_type": {
                                "type": "basic_type",
                                "_type": "INTEGER"
                            }
                        }
                    }
                ]
            }
        },
        "subprogram_declarations": {
            "length": 4,
            "type": "subprogram_declarations",
            "subprograms": [
                {
                    "length": 4,
                    "id": 4,
                    "type": "subprogram",
                    "subprogram_head": {
                        "length": 7,
                        "type": "subprogram_head",
                        "_type": "FUNCTION",
                        "ID": "gcd",
                        "formal_parameter": {
                            "length": 4,
                            "type": "formal_parameter",
                            "parameter_list": {
                                "length": 2,
                                "type": "parameter_list",
                                "parameters": [
                                    {
                                        "length": 2,
                                        "type": "parameter",
                                        "value": {
                                            "length": 4,
                                            "type": "value_parameter",
                                            "idlist": {
                                                "length": 4,
                                                "type": "idlist",
                                                "ids": [
                                                    "a",
                                                    "b"
                                                ]
                                            },
                                            "basic_type": {
                                                "type": "basic_type",
                                                "_type": "INTEGER"
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        "basic_type": {
                            "type": "basic_type",
                            "_type": "INTEGER"
                        }
                    },
                    "subprogram_body": {
                        "length": 4,
                        "type": "subprogram_body",
                        "const_declarations": None,
                        "var_declarations": None,
                        "compound_statement": {
                            "length": 4,
                            "type": "compound_statement",
                            "statement_list": {
                                "length": 2,
                                "type": "statement_list",
                                "statements": [
                                    {
                                        "length": 6,
                                        "type": "statement",
                                        "_type": "IF",
                                        "expression": {
                                            "length": 4,
                                            "type": "expression",
                                            "simple_expression_1": {
                                                "length": 2,
                                                "type": "simple_expression",
                                                "__type": "INTEGER",
                                                "term": {
                                                    "length": 2,
                                                    "type": "term",
                                                    "__type": "INTEGER",
                                                    "factor": {
                                                        "length": 2,
                                                        "type": "factor",
                                                        "_type": "variable",
                                                        "__type": "INTEGER",
                                                        "variable": {
                                                            "length": 3,
                                                            "type": "variable",
                                                            "__type": "INTEGER",
                                                            "ID": "b",
                                                            "id_varpart": {
                                                                "length": 1,
                                                                "type": "id_varpart",
                                                                "expression_list": None
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "RELOP": "=",
                                            "simple_expression_2": {
                                                "length": 2,
                                                "type": "simple_expression",
                                                "__type": "INTEGER",
                                                "term": {
                                                    "length": 2,
                                                    "type": "term",
                                                    "__type": "INTEGER",
                                                    "factor": {
                                                        "length": 2,
                                                        "type": "factor",
                                                        "_type": "NUM",
                                                        "__type": "INTEGER",
                                                        "NUM": 0
                                                    }
                                                }
                                            }
                                        },
                                        "statement": {
                                            "length": 4,
                                            "type": "statement",
                                            "_type": "variable",
                                            "variable": {
                                                "length": 3,
                                                "type": "variable",
                                                "__type": "INTEGER",
                                                "ID": "gcd",
                                                "id_varpart": {
                                                    "length": 1,
                                                    "type": "id_varpart",
                                                    "expression_list": None
                                                }
                                            },
                                            "ASSIGNOP": ":=",
                                            "expression": {
                                                "length": 2,
                                                "type": "expression",
                                                "__type": "INTEGER",
                                                "simple_expression": {
                                                    "length": 2,
                                                    "type": "simple_expression",
                                                    "__type": "INTEGER",
                                                    "term": {
                                                        "length": 2,
                                                        "type": "term",
                                                        "__type": "INTEGER",
                                                        "factor": {
                                                            "length": 2,
                                                            "type": "factor",
                                                            "_type": "variable",
                                                            "__type": "INTEGER",
                                                            "variable": {
                                                                "length": 3,
                                                                "type": "variable",
                                                                "__type": "INTEGER",
                                                                "ID": "a",
                                                                "id_varpart": {
                                                                    "length": 1,
                                                                    "type": "id_varpart",
                                                                    "expression_list": None
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "else_part": {
                                            "length": 3,
                                            "type": "else_part",
                                            "statement": {
                                                "length": 4,
                                                "type": "statement",
                                                "_type": "variable",
                                                "variable": {
                                                    "length": 3,
                                                    "type": "variable",
                                                    "__type": "INTEGER",
                                                    "ID": "gcd",
                                                    "id_varpart": {
                                                        "length": 1,
                                                        "type": "id_varpart",
                                                        "expression_list": None
                                                    }
                                                },
                                                "ASSIGNOP": ":=",
                                                "expression": {
                                                    "length": 2,
                                                    "type": "expression",
                                                    "__type": "INTEGER",
                                                    "simple_expression": {
                                                        "length": 2,
                                                        "type": "simple_expression",
                                                        "__type": "INTEGER",
                                                        "term": {
                                                            "length": 2,
                                                            "type": "term",
                                                            "__type": "INTEGER",
                                                            "factor": {
                                                                "length": 5,
                                                                "type": "factor",
                                                                "_type": "procedure_id",
                                                                "__type": "INTEGER",
                                                                "ID": "gcd",
                                                                "expression_list": {
                                                                    "length": 4,
                                                                    "type": "expression_list",
                                                                    "__type": [
                                                                        "INTEGER",
                                                                        "INTEGER"
                                                                    ],
                                                                    "expressions": [
                                                                        {
                                                                            "length": 2,
                                                                            "type": "expression",
                                                                            "__type": "INTEGER",
                                                                            "simple_expression": {
                                                                                "length": 2,
                                                                                "type": "simple_expression",
                                                                                "__type": "INTEGER",
                                                                                "term": {
                                                                                    "length": 2,
                                                                                    "type": "term",
                                                                                    "__type": "INTEGER",
                                                                                    "factor": {
                                                                                        "length": 2,
                                                                                        "type": "factor",
                                                                                        "_type": "variable",
                                                                                        "__type": "INTEGER",
                                                                                        "variable": {
                                                                                            "length": 3,
                                                                                            "type": "variable",
                                                                                            "__type": "INTEGER",
                                                                                            "ID": "b",
                                                                                            "id_varpart": {
                                                                                                "length": 1,
                                                                                                "type": "id_varpart",
                                                                                                "expression_list": None
                                                                                            }
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        },
                                                                        {
                                                                            "length": 2,
                                                                            "type": "expression",
                                                                            "__type": "INTEGER",
                                                                            "simple_expression": {
                                                                                "length": 2,
                                                                                "type": "simple_expression",
                                                                                "__type": "INTEGER",
                                                                                "term": {
                                                                                    "length": 4,
                                                                                    "type": "term",
                                                                                    "term": {
                                                                                        "length": 2,
                                                                                        "type": "term",
                                                                                        "__type": "INTEGER",
                                                                                        "factor": {
                                                                                            "length": 2,
                                                                                            "type": "factor",
                                                                                            "_type": "variable",
                                                                                            "__type": "INTEGER",
                                                                                            "variable": {
                                                                                                "length": 3,
                                                                                                "type": "variable",
                                                                                                "__type": "INTEGER",
                                                                                                "ID": "a",
                                                                                                "id_varpart": {
                                                                                                    "length": 1,
                                                                                                    "type": "id_varpart",
                                                                                                    "expression_list": None
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                    "factor": {
                                                                                        "length": 2,
                                                                                        "type": "factor",
                                                                                        "_type": "variable",
                                                                                        "__type": "INTEGER",
                                                                                        "variable": {
                                                                                            "length": 3,
                                                                                            "type": "variable",
                                                                                            "__type": "INTEGER",
                                                                                            "ID": "b",
                                                                                            "id_varpart": {
                                                                                                "length": 1,
                                                                                                "type": "id_varpart",
                                                                                                "expression_list": None
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                    "__type": "INTEGER"
                                                                                }
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        },
        "compound_statement": {
            "length": 4,
            "type": "compound_statement",
            "statement_list": {
                "length": 4,
                "type": "statement_list",
                "statements": [
                    {
                        "length": 5,
                        "type": "statement",
                        "_type": "READ",
                        "variable_list": {
                            "length": 4,
                            "type": "variable_list",
                            "variables": [
                                {
                                    "length": 3,
                                    "type": "variable",
                                    "__type": "INTEGER",
                                    "ID": "x",
                                    "id_varpart": {
                                        "length": 1,
                                        "type": "id_varpart",
                                        "expression_list": None
                                    }
                                },
                                {
                                    "length": 3,
                                    "type": "variable",
                                    "__type": "INTEGER",
                                    "ID": "y",
                                    "id_varpart": {
                                        "length": 1,
                                        "type": "id_varpart",
                                        "expression_list": None
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "length": 5,
                        "type": "statement",
                        "_type": "WRITE",
                        "expression_list": {
                            "length": 2,
                            "type": "expression_list",
                            "__type": [
                                "INTEGER"
                            ],
                            "expressions": [
                                {
                                    "length": 2,
                                    "type": "expression",
                                    "__type": "INTEGER",
                                    "simple_expression": {
                                        "length": 2,
                                        "type": "simple_expression",
                                        "__type": "INTEGER",
                                        "term": {
                                            "length": 2,
                                            "type": "term",
                                            "__type": "INTEGER",
                                            "factor": {
                                                "length": 5,
                                                "type": "factor",
                                                "_type": "procedure_id",
                                                "__type": "INTEGER",
                                                "ID": "gcd",
                                                "expression_list": {
                                                    "length": 4,
                                                    "type": "expression_list",
                                                    "__type": [
                                                        "INTEGER",
                                                        "INTEGER"
                                                    ],
                                                    "expressions": [
                                                        {
                                                            "length": 2,
                                                            "type": "expression",
                                                            "__type": "INTEGER",
                                                            "simple_expression": {
                                                                "length": 2,
                                                                "type": "simple_expression",
                                                                "__type": "INTEGER",
                                                                "term": {
                                                                    "length": 2,
                                                                    "type": "term",
                                                                    "__type": "INTEGER",
                                                                    "factor": {
                                                                        "length": 2,
                                                                        "type": "factor",
                                                                        "_type": "variable",
                                                                        "__type": "INTEGER",
                                                                        "variable": {
                                                                            "length": 3,
                                                                            "type": "variable",
                                                                            "__type": "INTEGER",
                                                                            "ID": "x",
                                                                            "id_varpart": {
                                                                                "length": 1,
                                                                                "type": "id_varpart",
                                                                                "expression_list": None
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "length": 2,
                                                            "type": "expression",
                                                            "__type": "INTEGER",
                                                            "simple_expression": {
                                                                "length": 2,
                                                                "type": "simple_expression",
                                                                "__type": "INTEGER",
                                                                "term": {
                                                                    "length": 2,
                                                                    "type": "term",
                                                                    "__type": "INTEGER",
                                                                    "factor": {
                                                                        "length": 2,
                                                                        "type": "factor",
                                                                        "_type": "variable",
                                                                        "__type": "INTEGER",
                                                                        "variable": {
                                                                            "length": 3,
                                                                            "type": "variable",
                                                                            "__type": "INTEGER",
                                                                            "ID": "y",
                                                                            "id_varpart": {
                                                                                "length": 1,
                                                                                "type": "id_varpart",
                                                                                "expression_list": None
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
}

_symbolTable = {
    "constants": [],
    "variables": [
        {
            "id": 0,
            "token": "x",
            "type": "INTEGER",
            "isArray": False,
            "dimension": 0,
            "size": [],
            "start": [],
            "recordTable": None
        },
        {
            "id": 1,
            "token": "y",
            "type": "INTEGER",
            "isArray": False,
            "dimension": 0,
            "size": [],
            "start": [],
            "recordTable": None
        }
    ],
    "subFunc": [
        {
            "id": 4,
            "token": "gcd",
            "type": "INTEGER",
            "table": {
                "params": 2,
                "references": [
                    [
                        False,
                        False
                    ]
                ],
                "constants": [],
                "variables": [
                    {
                        "id": 2,
                        "token": "a",
                        "type": "INTEGER",
                        "isArray": False,
                        "dimension": 0,
                        "size": [],
                        "start": [],
                        "recordType": None
                    },
                    {
                        "id": 3,
                        "token": "b",
                        "type": "INTEGER",
                        "isArray": False,
                        "dimension": 0,
                        "size": [],
                        "start": [],
                        "recordType": None
                    }
                ]
            }
        }
    ]
}

if __name__ == "__main__":
    generator = CodeGenerator(_ast, _symbolTable)
    with open("generator_test/compound_statement.json") as f:
        node = json.load(f)
    generator.compound_statement_test(node)
