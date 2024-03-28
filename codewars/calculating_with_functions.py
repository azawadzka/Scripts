# Calculating with Functions
# 
# https://www.codewars.com/kata/525f3eda17c7cd9f9e000b39
# 
# seven(times(five())) # must return 35
# four(plus(nine())) # must return 13
# eight(minus(three())) # must return 5
# six(divided_by(two())) # must return 3
# 
# Requirements:
# 
# There must be a function for each number from 0 ("zero") to 9 ("nine")
# There must be a function for each of the following mathematical operations: plus, minus, times, divided_by
# Each calculation consist of exactly one operation and two numbers
# The most outer function represents the left operand, the most inner function represents the right operand
# Division should be integer division. For example, this should return 2, not 2.666666...:

def number(func):
    n = func()
    def wrapper(op=None):
        if op:
            return op(n)
        else:
            return n
    return wrapper

@number
def zero(op=None): return 0
@number
def one(op=None): return 1
@number
def two(op=None): return 2
@number
def three(op=None): return 3
@number
def four(op=None): return 4
@number
def five(op=None): return 5
@number
def six(op=None): return 6
@number
def seven(op=None): return 7
@number
def eight(op=None): return 8
@number
def nine(op=None): return 9

def plus(y): return lambda x: x + y
def minus(y): return lambda x: x - y
def times(y): return lambda x: x * y
def divided_by(y): return lambda x: x // y

assert seven(times(five())) == 35
assert four(plus(nine())) == 13
assert eight(minus(three())) == 5
assert six(divided_by(two())) == 3

# Most inspired by solution:
# id_ = lambda x: x
# number = lambda x: lambda f=id_: f(x)
# zero, one, two, three, four, five, six, seven, eight, nine = map(number, range(10))
