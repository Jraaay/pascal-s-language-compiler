import copy
import json


class CodeGenerator:
    targetCode = ''  # 目标代码
    domain = []  # 作用域栈
    headFile = []  # 头文件
    ast = None  # 抽象语法树
    symbolTable = None  # 符号表

    def __init__(self, _ast, _symbolTable):
        self.ast = _ast
        self.symbolTable = _symbolTable

    # 代码格式化：添加换行、缩进
    def code_format(self):
        indent = 0
        in_quote = False
        in_small = 0
        add_indent = False
        code_list = list(self.targetCode)
        for i in range(0, len(code_list)-1):
            add_indent = False
            if code_list[i] == '\"' or code_list[i] == '\'':
                in_quote = ~in_quote
            if code_list[i] == '(':
                in_small += 1
            if code_list[i] == ')':
                in_small -= 1
            if in_quote == False and in_small == 0:
                if code_list[i] == '{':
                    code_list[i] += '\n'
                    indent += 1
                    add_indent = True
                if code_list[i] == '}\n':
                    add_indent = True
                if code_list[i] == ';':
                    code_list[i] += '\n'
                    add_indent = True
                if code_list[i+1] == '}':
                    code_list[i+1] += '\n'
                    indent -= 1
                    add_indent = True
            if add_indent == True:
                for j in range(0, indent):
                    code_list[i] += '\t'
        self.targetCode = ''.join(code_list)

    # 将分析阶段得到的头文件列表加到目标代码中
    def add_headfile(self):
        result = ('').join(self.headFile)
        self.targetCode = result + '\n' + self.targetCode

    def g_programstruct(self):
        '''
        programstruct : program_head ; program_body .
        '''
        node = self.ast
        assert node["type"] == "programstruct"
        result = ""
        result += self.g_program_head(node["program_head"])
        result += self.g_program_body(node["program_body"])
        self.targetCode = result
        self.domain.pop()

    def g_program_head(self, node):
        '''
        program_head : PROGRAM ID LPAREN idlist RPAREN
        '''
        assert node["type"] == "program_head"
        result = ""
        return result

    def g_program_body(self, node):
        '''
        program_body : const_declarations var_declarations subprogram_declarations compound_statement
        '''
        assert node["type"] == "program_body"
        self.domain += "global"
        result = ""
        result += self.g_const_declarations(node["const_declarations"])
        result += self.g_var_declarations(node["var_declarations"])
        result += self.g_subprogram_declarations(node["subprogram_declarations"])
        result += "int main(int argc, char* argv[])"
        self.domain += "main"
        result += self.g_compound_statement(node["compound_statement"])
        return result

    def g_idlist(self, node):
        '''
        idlist : idlist COM ID | ID
        '''
        assert node["type"] == "idlist"
        result = node["ids"]
        return result

    def g_const_declarations(self, node):
        '''
        const_declarations : CONST const_declaration SEMICOLON
                           | empty
        '''
        result = ""
        if node is not None:
            assert node["type"] == "const_declarations"
            result += self.g_const_declaration(node["const_declaration"])
            result += '\n'
        return result

    def g_const_declaration(self, node):
        '''
        const_declaration : const_declaration SEMICOLON ID EQUAL const_value
                          | ID EQUAL const_value
        '''
        assert node["type"] == "const_declaration"
        result = ""
        for it in node["values"]:
            result += 'const '
            if it["const_value"]["_type"] == "NUM":
                if isinstance(it["const_value"]["value"], int):
                    result += 'int '
                if isinstance(it["const_value"]["value"], float):
                    result += 'float '
            if it["const_value"]["_type"] == "LETTER":
                result += 'char '
            result += it["ID"] + ' = '
            result += self.g_const_value(it["const_value"])
            result += ';'
        return result

    def g_const_value(self, node):
        '''
        const_value : NUM | QUO LETTER QUO
        '''
        assert node["type"] == "const_value"
        result = ''
        if node["_type"] == "NUM":
            result += str(node["value"])
        if node["_type"] == "LETTER":
            result += '\'' + node["value"] + '\''
        return result

    def g_var_declarations(self, node):
        '''
        var_declarations : VAR var_declaration SEMICOLON
                        | 
        '''
        result = ''
        if node is not None:
            assert node["type"] == "var_declarations"
            result += self.g_var_declaration(node["var_declaration"])
            result += '\n'
        return result

    def g_var_declaration(self, node):
        '''
        var_declaration : var_declaration SEMICOLON idlist COLON type
                        | idlist COLON type
        '''
        assert node["type"] == "var_declaration"
        result = ''
        for it in node["values"]:
            if it["type"]["_type"] == "ARRAY":
                result += self.g_type(it["type"])
                result += ' '
                range = self.g_period(it["type"]["period"])
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += range
                    result += ', ' if id != idlist[-1] else ';'
            elif it["type"]["_type"] == "RECORD":
                result += 'struct ' + '{'
                result += self.g_multype(it["type"]["multype"])
                result += '}'
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += ', ' if id != idlist[-1] else ';'
            else:
                result += self.g_type(it["type"])
                result += ' '
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += ', ' if id != idlist[-1] else ';'
        return result

    def g_type(self, node):
        '''
        type : basic_type
            | ARRAY LBRACKET period RBRACKET OF basic_type
            | RECORD multype END
        '''
        assert node["type"] == "type"
        result = ''
        if node["_type"] == "ARRAY":
            result += self.g_basic_type(node["basic_type"])
        elif node["_type"] == "RECORD":
            pass
        else:
            result += self.g_basic_type(node["_type"])
        return result

    def g_basic_type(self, node):
        '''
        basic_type : INTEGER
                    | REAL
                    | BOOLEAN
                    | CHAR
        '''
        assert node["type"] == "basic_type"
        if node["_type"] == "INTEGER":
            return "int"
        if node["_type"] == "REAL":
            return "float"
        if node["_type"] == "BOOLEAN":
            self.headFile.append("#include<stdbool.h>\n")
            return "bool"
        if node["_type"] == "CHAR":
            return "char"

    def g_multype(self, node):
        '''
        multype : multype idlist COLON type SEMICOLON
                | idlist COLON type SEMICOLON
        '''
        assert node["type"] == "multype"
        result = ''
        for it in node["values"]:
            if it["type"]["_type"] == "ARRAY":
                result += self.g_type(it["type"])
                result += ' '
                range = self.g_period(it["type"]["period"])
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += range
                    result += ', ' if id != idlist[-1] else ';'
            elif it["type"]["_type"] == "RECORD":
                result += 'struct ' + '{'
                result += self.g_multype(it["type"]["multype"])
                result += '}'
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += ', ' if id != idlist[-1] else ';'
            else:
                result += self.g_type(it["type"])
                result += ' '
                idlist = self.g_idlist(it["idlist"])
                for id in idlist:
                    result += id
                    result += ', ' if id != idlist[-1] else ';'
        return result

    def g_period(self, node):
        '''
        period : period COM DIGITS POINTTO DIGITS
            | DIGITS POINTTO DIGITS
        '''
        assert node["type"] == "period"
        result = ''
        for period in node["values"]:
            size = period["end"]-period["start"]+1
            result += '['+str(size)+']'
        return result

    def g_subprogram_declarations(self, node):
        '''
        subprogram_declarations : subprogram_declarations subprogram SEMICOLON
                                | 
        '''
        result = ''
        if node is not None:
            assert node["type"] == "subprogram_declarations"
            for it in node["subprograms"]:
                result += self.g_subprogram(it)
                result += '\n'
        return result

    def g_subprogram(self, node):
        '''
        subprogram : subprogram_head SEMICOLON subprogram_body
        '''
        assert node["type"] == "subprogram"
        result = ''
        result += self.g_subprogram_head(node["subprogram_head"])
        result += self.g_subprogram_body(node["subprogram_body"])
        self.domain.pop()
        return result

    def g_subprogram_head(self, node):
        '''
        subprogram_head :  seen_PROCEDURE ID formal_parameter
                        | FUNCTION seen_FUNCTION ID formal_parameter COLON basic_type 
        '''
        assert node["type"] == "subprogram_head"
        result = ''
        if node["_type"] == 'PROCEDURE':
            result += 'void '
        else:
            result += self.g_basic_type(node["basic_type"]) + ' '
        result += node["ID"]
        self.domain.append(node["ID"])
        result += self.g_formal_parameter(node["formal_parameter"])
        return result

    def g_formal_parameter(self, node):
        '''
        formal_parameter : LPAREN parameter_list RPAREN
                        | 
        '''
        result = ''
        if node is not None:
            assert node["type"] == "formal_parameter"
            result += '('
            result += self.g_parameter_list(node["parameter_list"])
            result += ')'
        return result

    def g_parameter_list(self, node):
        '''
        parameter_list : parameter_list SEMICOLON parameter
                    | parameter
        '''
        assert node["type"] == "parameter_list"
        result = ''
        for it in node["parameters"]:
            result += self.g_parameter(it)
            result += ', 'if it != node["parameters"][-1] else ''
        return result

    def g_parameter(self, node):
        '''
        parameter : var_parameter
                | value_parameter
        '''
        assert node["type"] == "parameter"
        result = ''
        if node["value"]["type"] == "value_parameter":
            result += self.g_value_parameter(node["value"])
        else:
            result += self.g_var_parameter(node["value"])
        return result

    def g_var_parameter(self, node):
        '''
        var_parameter : VAR value_parameter
        '''
        assert node["type"] == "var_parameter"
        result = ''
        type = self.g_basic_type(node["basic_type"])
        idlist = self.g_idlist(node["idlist"])
        for id in idlist:
            result += type + '* '
            result += id
            result += ', ' if id != idlist[-1] else ''
        return result

    def g_value_parameter(self, node):
        '''
        value_parameter : idlist COLON basic_type
        '''
        assert node["type"] == "value_parameter"
        result = ''
        type = self.g_basic_type(node["basic_type"])
        idlist = self.g_idlist(node["idlist"])
        for id in idlist:
            result += type + ' '
            result += id
            result += ', ' if id != idlist[-1] else ''
        return result

    def g_subprogram_body(self, node):
        '''
        subprogram_body : const_declarations var_declarations compound_statement
        '''
        assert node["type"] == "subprogram_body"
        result = ""
        result += self.g_const_declarations(node["const_declarations"])
        result += self.g_var_declarations(node["var_declarations"])
        result += self.g_compound_statement(node["compound_statement"])
        return result

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
            result += ";"
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
            # var = self.g_expression_list(node["expression_list"])
            # var = var.split(",")
            # __type = node["expression_list"]["__type"]
            # print(var, __type)
            # assert len(var) == len(__type), len(var)
            # assert len(var) > 0
            # format_string = ""
            # var_string = ""
            # for i in range(len(var)):
            #     format_string += "{}: {}\n".format(var[i],
            #                                        format_tag_map[__type[i]])
            #     var_string += "{},".format(var[i])
            # var_string = var_string[0: -1]
            # result += "printf(\"{}\",{})".format(format_string, var_string)
            result += "!!!printf TBD!!!"
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

    def code_generate(self):
        self.g_programstruct()  # 从programstruct节点开始生成目标代码
        self.code_format()  # 代码格式化
        self.add_headfile()  # 添加头文件
        return self.targetCode  # 返回生成的目标代码

    def compound_statement_test(self, node: dict):
        result = self.g_compound_statement(node)
        print(result)
        # self.targetCode = result
        # self.code_format()
        # print(self.targetCode)


if __name__ == "__main__":
    with open("generator_test/test.json") as test:
        obj = json.load(test)
        _ast = obj["ast"]
        _symbolTable = obj["symbolTable"]
    generator = CodeGenerator(_ast, _symbolTable)
    target_code = generator.code_generate()
    with open("generator_test/test.c", 'w') as opt:
        opt.write(target_code)

    '''----单独测试----'''
    with open("generator_test/compound_statement.json") as f:
        node = json.load(f)
    generator.compound_statement_test(node)
