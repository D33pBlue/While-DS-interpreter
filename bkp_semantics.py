from abc import ABCMeta, abstractmethod

class Function:
    __metaclass__ = ABCMeta
    """Abstract base class for state transition functions"""

    @abstractmethod
    def evaluate(self,state,verbose):
        pass


class Identity(Function):
    """
    The Identity function that does not change the state
    """
    def __init__(self):
        super(Identity,self).__init__()

    def evaluate(self,state,verbose):
        return state.get_copy()

    def __str__(self):
        return "id"


class Undef(Function):
    """
    The function that is always undefined (bottom)
    """
    def __init__(self):
        super(Undef,self).__init__()

    def evaluate(self,state,verbose):
        return state.null_state()

    def __str__(self):
        return '_'


class Update(Function):
    """
    The function that change the state updating the value of a variable
    """
    def __init__(self,varname,expr):
        super(Update,self).__init__()
        self.__v = varname
        self.__e = expr

    def evaluate(self,state,verbose):
        val = self.__e.evaluate(state)
        return state.update(self.__v,val)

    def __str__(self):
        return "\s.s["+self.__v+"/A["+str(self.__e)+"]s]"


class Composition(Function):
    """
    The composition of two state transition functions
    """
    def __init__(self,first_function,second_function):
        super(Composition,self).__init__()
        self.__f1 = first_function
        self.__f2 = second_function

    def evaluate(self,state,verbose):
        s1 = self.__f1.evaluate(state,verbose)
        return self.__f2.evaluate(s1,verbose)

    def __str__(self):
        return '('+str(self.__f2)+') o ('+str(self.__f1)+')'


class Cond(Function):
    """
    \s.cond(b,s1,s2) = | s1 if B[b]s == tt
                       | s2 otherwise
    """
    def __init__(self,bexp,S1,S2):
        super(Cond,self).__init__()
        self.__b = bexp
        self.__s1 = S1
        self.__s2 = S2

    def evaluate(self,state,verbose):
        condition = self.__b.evaluate(state)
        if condition == True:
            return self.__s1.evaluate(state,verbose)
        if condition == False:
            return self.__s2.evaluate(state,verbose)
        return state.null_state()

    def __str__(self):
        return 'cond(B['+str(self.__b)+'],'+str(self.__s1)+','+str(self.__s2)+')'


class FixF(Function):
    """
    Fix point of F g = cond(b,g o Sds[S],id)
    """
    def __init__(self,condition,body):
        super(FixF,self).__init__()
        self.__b = condition
        self.__s = body

    def evaluate(self,state,verbose):
        i = 10
        s = Undef().evaluate(state,False)
        while s.is_undef():
            print "evaluating F^"+str(i)+" _"
            f = self.__Fn_bottom(i)
            s = f.evaluate(state,False)
            i += 100
        return s

    def __Fn_bottom(self,n):
        k = 0
        fn = Undef()
        while k<n:
            fn = Cond(
                self.__b,
                Composition(
                    self.__s,
                    fn
                    ),
                Identity()
                )
            k += 1
        return fn

    def __str__(self):
        return 'FIX(\\g.cond(\n\tB['+str(self.__b)+'],\n\tg o ('+str(self.__s)+'),\n\tid\n\t))'
