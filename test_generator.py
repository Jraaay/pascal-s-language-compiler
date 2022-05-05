from compiler import CodeGenerator
import json


class TestGenerator(object):
    generator = CodeGenerator.CodeGenerator()

    def __int__(self):
        pass

    def test_generator_gcd(self):
        test_file_path = "generator_test_sample/gcd.out"
        with open(test_file_path, "r") as f:
            out = json.load(f)
        result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open(test_file_path.replace(".out", ".c"), "w") as f:
            f.write(result)
