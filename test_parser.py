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
