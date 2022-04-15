from email import parser
from compiler import Parser


class TestParser(object):
    myParser = Parser.Parser()

    def __int__(self):
        pass

    def test_parser_gcd(self):
        ans = None
        with open('./test/gcd.pas') as f:
            ans = self.myParser.parse(f.read())
        assert ans == {
            "ast": {
                "type": "programstruct",
                "program_head": {
                    "type": "program_head",
                    "ID": "example",
                    "idlist": {
                        "type": "idlist",
                        "ids": [
                            "input",
                            "output"
                        ]
                    }
                },
                "program_body": {
                    "type": "program_body",
                    "const_declarations": None,
                    "var_declarations": {
                        "type": "var_declarations",
                        "var_declaration": {
                            "type": "var_declaration",
                            "values": [
                                {
                                    "idlist": {
                                        "type": "idlist",
                                        "ids": [
                                            "x",
                                            "y"
                                        ]
                                    },
                                    "type": {
                                        "type": "type",
                                        "_type": {
                                            "type": "basic_type",
                                            "_type": "integer"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "subprogram_declarations": {
                        "type": "subprogram_declarations",
                        "subprograms": [
                            {
                                "type": "subprogram",
                                "subprogram_head": {
                                    "type": "subprogram_head",
                                    "_type": "FUNCTION",
                                    "ID": "gcd",
                                    "formal_parameter": {
                                        "type": "formal_parameter",
                                        "parameter_list": {
                                            "type": "parameter_list",
                                            "parameters": [
                                                {
                                                    "type": "parameter",
                                                    "value": {
                                                        "type": "value_parameter",
                                                        "idlist": {
                                                            "type": "idlist",
                                                            "ids": [
                                                                "a",
                                                                "b"
                                                            ]
                                                        },
                                                        "basic_type": {
                                                            "type": "basic_type",
                                                            "_type": "integer"
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    "basic_type": {
                                        "type": "basic_type",
                                        "_type": "integer"
                                    }
                                },
                                "subprogram_body": {
                                    "type": "subprogram_body",
                                    "const_declarations": None,
                                    "var_declarations": [],
                                    "compound_statement": {
                                        "type": "compound_statement",
                                        "statement_list": {
                                            "type": "statement_list",
                                            "statements": [
                                                {
                                                    "type": "statement",
                                                    "_type": "IF",
                                                    "expression": {
                                                        "type": "expression",
                                                        "simple_expression_1": {
                                                            "type": "simple_expression",
                                                            "term": {
                                                                "type": "term",
                                                                "factor": {
                                                                    "type": "factor",
                                                                    "_type": "variable",
                                                                    "variable": {
                                                                        "type": "variable",
                                                                        "ID": "b",
                                                                        "id_varpart": {
                                                                            "type": "id_varpart",
                                                                            "expression_list": None
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        "RELOP": "=",
                                                        "simple_expression_2": {
                                                            "type": "simple_expression",
                                                            "term": {
                                                                "type": "term",
                                                                "factor": {
                                                                    "type": "factor",
                                                                    "_type": "NUM",
                                                                    "NUM": 0
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "statement": {
                                                        "type": "statement",
                                                        "_type": "variable",
                                                        "variable": {
                                                            "type": "variable",
                                                            "ID": "gcd",
                                                            "id_varpart": {
                                                                "type": "id_varpart",
                                                                "expression_list": None
                                                            }
                                                        },
                                                        "ASSIGNOP": ":=",
                                                        "expression": {
                                                            "type": "expression",
                                                            "simple_expression": {
                                                                "type": "simple_expression",
                                                                "term": {
                                                                    "type": "term",
                                                                    "factor": {
                                                                        "type": "factor",
                                                                        "_type": "variable",
                                                                        "variable": {
                                                                            "type": "variable",
                                                                            "ID": "a",
                                                                            "id_varpart": {
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
                                                        "type": "else_part",
                                                        "statement": {
                                                            "type": "statement",
                                                            "_type": "variable",
                                                            "variable": {
                                                                "type": "variable",
                                                                "ID": "gcd",
                                                                "id_varpart": {
                                                                    "type": "id_varpart",
                                                                    "expression_list": None
                                                                }
                                                            },
                                                            "ASSIGNOP": ":=",
                                                            "expression": {
                                                                "type": "expression",
                                                                "simple_expression": {
                                                                    "type": "simple_expression",
                                                                    "term": {
                                                                        "type": "term",
                                                                        "factor": {
                                                                            "type": "factor",
                                                                            "_type": "procedure_id",
                                                                            "ID": "gcd",
                                                                            "expression_list": {
                                                                                "type": "expression_list",
                                                                                "expressions": [
                                                                                    {
                                                                                        "type": "expression",
                                                                                        "simple_expression": {
                                                                                            "type": "simple_expression",
                                                                                            "term": {
                                                                                                "type": "term",
                                                                                                "factor": {
                                                                                                    "type": "factor",
                                                                                                    "_type": "variable",
                                                                                                    "variable": {
                                                                                                        "type": "variable",
                                                                                                        "ID": "b",
                                                                                                        "id_varpart": {
                                                                                                            "type": "id_varpart",
                                                                                                            "expression_list": None
                                                                                                        }
                                                                                                    }
                                                                                                }
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                    {
                                                                                        "type": "expression",
                                                                                        "simple_expression": {
                                                                                            "type": "simple_expression",
                                                                                            "term": {
                                                                                                "type": "term",
                                                                                                "factor": {
                                                                                                    "type": "term",
                                                                                                    "factor": {
                                                                                                        "type": "factor",
                                                                                                        "_type": "variable",
                                                                                                        "variable": {
                                                                                                            "type": "variable",
                                                                                                            "ID": "a",
                                                                                                            "id_varpart": {
                                                                                                                "type": "id_varpart",
                                                                                                                "expression_list": None
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
                        "type": "compound_statement",
                        "statement_list": {
                            "type": "statement_list",
                            "statements": [
                                {
                                    "type": "statement",
                                    "_type": "READ",
                                    "variable_list": {
                                        "type": "variable_list",
                                        "variables": [
                                            {
                                                "type": "variable",
                                                "ID": "x",
                                                "id_varpart": {
                                                    "type": "id_varpart",
                                                    "expression_list": None
                                                }
                                            },
                                            {
                                                "type": "variable",
                                                "ID": "y",
                                                "id_varpart": {
                                                    "type": "id_varpart",
                                                    "expression_list": None
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "statement",
                                    "_type": "WRITE",
                                    "expression_list": {
                                        "type": "expression_list",
                                        "expressions": [
                                            {
                                                "type": "expression",
                                                "simple_expression": {
                                                    "type": "simple_expression",
                                                    "term": {
                                                        "type": "term",
                                                        "factor": {
                                                            "type": "factor",
                                                            "_type": "procedure_id",
                                                            "ID": "gcd",
                                                            "expression_list": {
                                                                "type": "expression_list",
                                                                "expressions": [
                                                                    {
                                                                        "type": "expression",
                                                                        "simple_expression": {
                                                                            "type": "simple_expression",
                                                                            "term": {
                                                                                "type": "term",
                                                                                "factor": {
                                                                                    "type": "factor",
                                                                                    "_type": "variable",
                                                                                    "variable": {
                                                                                        "type": "variable",
                                                                                        "ID": "x",
                                                                                        "id_varpart": {
                                                                                            "type": "id_varpart",
                                                                                            "expression_list": None
                                                                                        }
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "type": "expression",
                                                                        "simple_expression": {
                                                                            "type": "simple_expression",
                                                                            "term": {
                                                                                "type": "term",
                                                                                "factor": {
                                                                                    "type": "factor",
                                                                                    "_type": "variable",
                                                                                    "variable": {
                                                                                        "type": "variable",
                                                                                        "ID": "y",
                                                                                        "id_varpart": {
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
            },
            "symbolTable": {
                "constants": [],
                "variables": [
                    {
                        "id": 0,
                        "token": "x",
                        "type": "integer",
                        "isArray": False,
                        "dimension": 0,
                        "size": [],
                        "start": [],
                        "recordTable": None
                    },
                    {
                        "id": 1,
                        "token": "y",
                        "type": "integer",
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
                        "type": "integer",
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
                                [
                                    {
                                        "id": 2,
                                        "token": "a",
                                        "type": "integer",
                                        "isArray": False,
                                        "dimension": 0,
                                        "size": [],
                                        "start": [],
                                        "recordType": None
                                    },
                                    {
                                        "id": 3,
                                        "token": "b",
                                        "type": "integer",
                                        "isArray": False,
                                        "dimension": 0,
                                        "size": [],
                                        "start": [],
                                        "recordType": None
                                    }
                                ]
                            ]
                        }
                    }
                ]
            },
            "error": None
        }
