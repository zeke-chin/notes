```python
import unittest


class TestExceptOrder(unittest.TestCase):
    S = Solution()
    test_func = S.canPartition

    def test_test(self):
        self.test_func()


if __name__ == '__main__':
    unittest.main()

```