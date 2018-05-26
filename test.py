import unittest
from parser import *
from tokens import *

class TestAST(unittest.TestCase):
    def test_value(self):
        n = ASTValue([Token('hello')])
        self.assertEqual(n.eval({'hello': 5}, []), 5)

        n = ASTValue([Token('3')])
        self.assertEqual(n.eval({}, []), 3)

        n = ASTValue([Token('"hello"')])
        self.assertEqual(n.eval({}, []), 'hello')

    def test_expression(self):
        tokns = list(tokens('3 + 4'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 7)

        tokns = list(tokens('(3 + 4)'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 7)

        tokns = list(tokens('(2 + 2) * 2'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 8)

        tokns = list(tokens('2 + 2 * 2'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 6)

        tokns = list(tokens('(2 + (6 * 9)) * 2'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 112)

        tokns = list(tokens('2 / 2'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), 1)

        tokns = list(tokens('2 == 2'))
        n = ASTExpression(tokns)
        self.assertEqual(n.eval({}, []), True)






if __name__ == '__main__':
    unittest.main()