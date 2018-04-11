#from copy import copy
from abc import ABCMeta, abstractmethod

class AExp:
    __metaclass__ = ABCMeta
    """Abstract base class for arithmetic expressions"""

    @abstractmethod
    def evaluate(self,state):
        pass

    def __add__(self,other):
        return Operation('+',self,other)

    def __sub__(self,other):
        return Operation('-',self,other)

    def __mul__(self,other):
        return Operation('*',self,other)

    def __eq__(self,other):
        return Comparison('=',self,other)

    def __le__(self,other):
        return Comparison('<=',self,other)


class BExp:
    __metaclass__ = ABCMeta
    """Abstract base class for logical expressions"""

    @abstractmethod
    def evaluate(self,state):
        pass



class Number(AExp):
    """An AExp wrapper for an integer"""
    def __init__(self,number):
        super(Number,self).__init__()
        self.__n = int(number)

    def evaluate(self,state):
        return self.__n

    def __str__(self):
        return str(self.__n)


class Var(AExp):
    """An AExp that represents a variable"""
    def __init__(self,varname):
        super(Var,self).__init__()
        self.__n = varname

    def evaluate(self,state):
        return state.get_val(self.__n)

    def get_name(self):
        return self.__n

    def __str__(self):
        return self.__n

class Operation(AExp):
    """
    An AExp that wraps an operation, such as +,- or * between two Aexp
    """
    def __init__(self,operation,exp1,exp2):
        super(Operation,self).__init__()
        self.__op = operation
        self.__e1 = exp1
        self.__e2 = exp2

    def evaluate(self,state):
        v1 = self.__e1.evaluate(state)
        if v1 == None:
            return None
        v2 = self.__e2.evaluate(state)
        if v2 == None:
            return None
        if self.__op == '+':
            return v1+v2
        if self.__op == '-':
            return v1-v2
        if self.__op == '*':
            return v1*v2
        return None

    def __str__(self):
        return '('+str(self.__e1)+str(self.__op)+str(self.__e2)+')'


class BoolVal(BExp):
    """
    A wrapper for boolean values
    """
    def __init__(self,value):
        super(BoolVal,self).__init__()
        self.__v = value

    def evaluate(self,state):
        return self.__v

    def __str__(self):
        return str(self.__v)


class Not(BExp):
    """
    A BExp for logical negation
    """
    def __init__(self,bexp):
        super(Not,self).__init__()
        self.__e = bexp

    def evaluate(self,state):
        v = self.__e.evaluate(state)
        if v == None:
            return None
        return not v

    def __str__(self):
        return chr(172)+str(self.__e)


class And(BExp):
    """
    A BExp for logical and
    """
    def __init__(self,bexp1,bexp2):
        super(And,self).__init__()
        self.__e1 = bexp1
        self.__e2 = bexp2

    def evaluate(self,state):
        v1 = self.__e1.evaluate(state)
        if v1 == None:
            return None
        v2 = self.__e2.evaluate(state)
        if v2 == None:
            return None
        return v1 and v2

    def __str__(self):
        return '('+str(self.__e1)+' and '+str(self.__e2)+')'


class Comparison(BExp):
    """
    A BExp for comparing AExp with == or <=
    """
    def __init__(self,operator,aexp1,aexp2):
        super(Comparison,self).__init__()
        self.__op = operator
        self.__e1 = aexp1
        self.__e2 = aexp2

    def evaluate(self,state):
        v1 = self.__e1.evaluate(state)
        if v1 == None:
            return None
        v2 = self.__e2.evaluate(state)
        if v2 == None:
            return None
        if self.__op == '=':
            return v1 == v2
        if self.__op == '<=':
            return v1 <= v2
        return None

    def __str__(self):
        return '('+str(self.__e1)+' '+self.__op+' '+str(self.__e2)+')'
