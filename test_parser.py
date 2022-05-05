from compiler import Parser
import json


class TestParser(object):
    myParser = Parser.Parser()

    def test_parser_gcd(self):
        """
        id="44"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_bug(self):
        """
        id="47"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_bug.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_bug.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_bug_2(self):
        """
        id="50"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_bug_2.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_bug_2.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_no_blank(self):
        """
        id="53"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_no_blank.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_no_blank.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_knapsack(self):
        """
        id="56"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/knapsack.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/knapsack.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_kruskal(self):
        """
        id="59"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/kruskal.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/kruskal.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_quicksort(self):
        """
        id="62"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/quicksort.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/quicksort.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_record(self):
        """
        id="65"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/record.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/record.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_record_period_error(self):
        """
        id="69"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/record_period_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/record_period_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_c02_error(self):
        """
        id="72"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_c02_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_c02_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_c03_error(self):
        """
        id="75"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_c03_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_c03_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_gcd_w01_warn(self):
        """
        id="78"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/gcd_w01_warn.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/gcd_w01_warn.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c04_error(self):
        """
        id="81"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c04_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c04_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c05_error(self):
        """
        id="84"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c05_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c05_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c06_error(self):
        """
        id="87"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c06_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c06_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c07_10_11_error(self):
        """
        id="90"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c07_10_11_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c07_10_11_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c09_error(self):
        """
        id="93"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c09_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c09_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_f01_error(self):
        """
        id="96"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/f01_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/f01_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c12_error(self):
        """
        id="98"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c12_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c12_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c13_error(self):
        """
        id="100"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c13_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c13_error.out') as f:
            expected = json.load(f)
        assert ans == expected

    def test_parser_c14_error(self):
        """
        id="102"
        """
        ans = None
        expected = None
        with open('./parser_test_sample/c14_error.pas') as f:
            ans = self.myParser.parse(f.read())
        with open('./parser_test_sample/c14_error.out') as f:
            expected = json.load(f)
        assert ans == expected
