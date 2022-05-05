from compiler import CodeGenerator
import json


class TestGenerator(object):
    generator = CodeGenerator.CodeGenerator()

    def test_generator_gcd(self):
        with open("generator_test_sample/gcd.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/gcd.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_knapsack(self):
        with open("generator_test_sample/knapsack.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/knapsack.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_kruskal(self):
        with open("generator_test_sample/kruskal.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/kruskal.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_noAST(self):
        with open("generator_test_sample/noAST.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/noAST.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_period(self):
        with open("generator_test_sample/period.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/period.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_quicksort(self):
        with open("generator_test_sample/quicksort.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/quicksort.c') as f:
            expected = f.read()
        assert result == expected

    def test_generator_record(self):
        with open("generator_test_sample/record.out") as f:
            out = json.load(f)
            result = self.generator.code_generate(_ast=out["ast"], _symbolTable=out["symbolTable"])
        with open('generator_test_sample/record.c') as f:
            expected = f.read()
        assert result == expected
