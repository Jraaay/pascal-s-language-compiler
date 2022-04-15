from compiler import Parser
import json


class TestParser(object):
    myParser = Parser.Parser()

    def __int__(self):
        pass

    def test_parser_gcd(self):
        """
        id="44"
        """
        ans = None
        expected = None
        with open('./test/gcd.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_bug(self):
        """
        id="47"
        """
        ans = None
        expected = None
        with open('./test/gcd_bug.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_bug.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_bug_2(self):
        """
        id="50"
        """
        ans = None
        expected = None
        with open('./test/gcd_bug_2.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_bug_2.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_no_blank(self):
        """
        id="53"
        """
        ans = None
        expected = None
        with open('./test/gcd_no_blank.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_no_blank.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_knapsack(self):
        """
        id="56"
        """
        ans = None
        expected = None
        with open('./test/knapsack.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/knapsack.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_kruskal(self):
        """
        id="59"
        """
        ans = None
        expected = None
        with open('./test/kruskal.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/kruskal.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_quicksort(self):
        """
        id="62"
        """
        ans = None
        expected = None
        with open('./test/quicksort.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/quicksort.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_record(self):
        """
        id="65"
        """
        ans = None
        expected = None
        with open('./test/record.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/record.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_record_period_error(self):
        """
        id="69"
        """
        ans = None
        expected = None
        with open('./test/record_period_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/record_period_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_c02_error(self):
        """
        id="72"
        """
        ans = None
        expected = None
        with open('./test/gcd_c02_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_c02_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_c03_error(self):
        """
        id="75"
        """
        ans = None
        expected = None
        with open('./test/gcd_c03_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_c03_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_w01_warn(self):
        """
        id="78"
        """
        ans = None
        expected = None
        with open('./test/gcd_w01_warn.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/gcd_w01_warn.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c04_error(self):
        """
        id="81"
        """
        ans = None
        expected = None
        with open('./test/c04_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/c04_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c05_error(self):
        """
        id="84"
        """
        ans = None
        expected = None
        with open('./test/c05_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/c05_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c06_error(self):
        """
        id="87"
        """
        ans = None
        expected = None
        with open('./test/c06_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/c06_error.out') as f:
            expected = json.load(f)
        assert ans == expected
    
    def test_parser_c07_10_11_error(self):
        """
        id="90"
        """
        ans = None
        expected = None
        with open('./test/c07_10_11_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/c07_10_11_error.out') as f:
            expected = json.load(f)
        assert ans == expected
    
    def test_parser_c09_error(self):
        """
        id="93"
        """
        ans = None
        expected = None
        with open('./test/c09_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./test/c09_error.out') as f:
            expected = json.load(f)
        assert ans == expected