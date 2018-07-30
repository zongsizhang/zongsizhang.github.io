# Python Test Strategies and Tools

## test in doc + generated test case

Tests can be written in the same file as code like documentd. See this example as follow.

```python
def add(x, y):
    """ return x + y

    >>> add(2, 2)
    5
    >>> add(1, 2)
    3
    """
    return x + y
```

```bash
python zongsi.zhang$ python examples.py -v                                                
Trying:                                                                                                        
    add(2, 2)                                                                                                  
Expecting:                                                                                                     
    5                                                                                                          
**********************************************************************                                         
File "examples.py", line 4, in __main__.add                                                                    
Failed example:                                                                                                
    add(2, 2)                                                                                                  
Expected:                                                                                                      
    5                                                                                                          
Got:                                                                                                           
    4                                                                                                          
Trying:                                                                                                        
    add(1, 2)                                                                                                  
Expecting:                                                                                                     
    3                                                                                                          
ok                                                                                                             
1 items had no tests:                                                                                          
    __main__                                                                                                   
**********************************************************************                                         
1 items had failures:                                                                                          
   1 of   2 in __main__.add                                                                                    
2 tests in 2 items.                                                                                            
1 passed and 1 failed.                                                                                         
***Test Failed*** 1 failures.
```

Pros and Cons:
+ Very easy to add test
+ A complement of documentation. Makes code easier to use

- Not friendly to complex test logic
- excessive documents, diminish readability and consision of code.

### [Hypothesis](https://hypothesis.readthedocs.io/en/latest/quickstart.html)

As a suplement, Hypothesis can be used to generate test cases that will cover corner cases. Which can help reduce the length of doc tests in code.

a quick example

```python
from hypothesis import given
import hypothesis.strategies as st
from math import pow

def square(a):
    return a * a

@given(x=st.integers())
def test_square(x):
    assert square(x) == pow(x, 2)
if __name__ == '__main__':
    test_square()
```

Run this script, you will get
```bash
Falsifying example: test_square(x=94906273)
......
```

Pros and Cons:

- Not suitable for tests cases that doesn't follow any mathematical distribution. For example inputs are username&password pair, not able to simulate cases that is correct.

+ It can cover a lot of corner cases that human not able to come up with.
+ still support hardcoded test cases.

### A good doc test solution: Hypothesis + Contracts

[contracts](https://github.com/deadpixi/contracts)

+ Contracts offers a set of constraints on method inputs, outputs. Which is a more clean expression of doc test. Mixed together with hypothesis will make very clean tests in code.

- difficult to learn, need good design.

## Pytest

A very well developed test framework.

+ support unittest and functional test
+ extendable
+ easy to use

Here is a comparison with unittest

```python
def func(x):
    return x+1

# pytest test
def test_func():
    assert func(3) == 5

# unittest
import unittest
class TestFuncClass(unittest.TestCase):
    def test_func(self):
        assert func(3) == 5

if __name__ == '__main__':
    unittest.main()
```

Run result of py.test
```bash
plugins: hypothesis-3.66.12                                                                                    
collected 1 item                                                                                               
                                                                                                               
examples.py F                                                                                           [100%] 
                                                                                                               
================================================== FAILURES ===================================================
__________________________________________________ test_func __________________________________________________
                                                                                                               
    def test_func():                                                                                           
>       assert func(3) == 5                                                                                    
E       assert 4 == 5                                                                                          
E        +  where 4 = func(3)                                                                                  
                                                                                                               
examples.py:6: AssertionError                                                                                  
========================================== 1 failed in 0.11 seconds ===========================================
```

Run result of unittest:
```bash
F                                                                                                              
======================================================================                                         
FAIL: test_func (__main__.TestFuncClass)                                                                       
----------------------------------------------------------------------                                         
Traceback (most recent call last):                                                                             
  File "examples.py", line 10, in test_func                                                                    
    assert func(3) == 5                                                                                        
AssertionError                                                                                                 
                                                                                                               
----------------------------------------------------------------------                                         
Ran 1 test in 0.000s                                                                                           
                                                                                                               
FAILED (failures=1)            
```

You will find that pytest has 
+ easier to use
+ more detailed fail report
+ it can detect plugins we installed


## Helpful tools for testing in python

### unittest.mock

provides simulation for multiple popular systems.

### virtualenv

can create a virtual python envrionment that you can do whatever you like without affecting environments of your machine.

[cheat sheet](https://www.michael-noll.com/blog/2010/11/29/virtualenv-cheat-sheet/)










