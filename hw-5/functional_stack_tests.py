import unittest

from functional_stack import Stack, push, pop, top, is_empty


class TestFunctionalStack(unittest.TestCase):

    def test_push(self):
        pre = Stack(storage=[1])
        self.assertEqual(top(pre), 1)
        post = push(pre, 2)
        self.assertEqual(top(post), 2)

    def test_pop(self):
        pre = Stack(storage=[1, 2])
        self.assertEqual(top(pre), 2)
        post = pop(pre)
        self.assertEqual(top(post), 1)

    def test_is_empty(self):
        pre = Stack(storage=[1])
        self.assertFalse(is_empty(pre))
        post = pop(pre)
        self.assertTrue(is_empty(post))

    def test_top(self):
        pre = Stack(storage=[1, 2])
        self.assertEqual(top(pre), 2)
        post1 = pop(pre)
        self.assertEqual(top(post1), 1)
        post2 = push(post1, 3)
        self.assertEqual(top(post2), 3)


if __name__ == '__main__':
    unittest.main()
