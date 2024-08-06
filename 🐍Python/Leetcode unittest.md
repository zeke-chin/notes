```python
import unittest  
  
S = Solution()  
test_func = S.canPartition  
  
  
class TestExceptOrder(unittest.TestCase):  
  
    def test_test(self):  
        self.assertEqual(test_func([1, 5, 11, 5]), True)  
  
    def test_test2(self):  
        self.assertEqual(test_func([1, 2, 3, 5]), False)

```