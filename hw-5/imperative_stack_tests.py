import unittest

from imperative_stack import Stack


class TestFunctionalStack(unittest.TestCase):

    def test_push(self):
        stack = Stack(storage=[1])
        self.assertEqual(stack.top(), 1)
        stack.push(2)
        self.assertEqual(stack.top(), 2)

    def test_pop(self):
        stack = Stack(storage=[1, 2])
        self.assertEqual(stack.top(), 2)
        stack.pop()
        self.assertEqual(stack.top(), 1)

    def test_is_empty(self):
        stack = Stack(storage=[1])
        self.assertFalse(stack.is_empty())
        stack.pop()
        self.assertTrue(stack.is_empty())

    def test_top(self):
        stack = Stack(storage=[1, 2])
        self.assertEqual(stack.top(), 2)
        stack.pop()
        self.assertEqual(stack.top(), 1)
        stack.push(3)
        self.assertEqual(stack.top(), 3)


if __name__ == '__main__':
    unittest.main()
