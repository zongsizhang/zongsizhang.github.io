import unittest
def func(x):
    return x+1
 
def test_func():
    assert func(3) == 5

class TestFuncClass(unittest.TestCase):
    def test_func(self):
        assert func(3) == 5

if __name__ == '__main__':
    unittest.main()