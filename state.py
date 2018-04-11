import re

class State:
    """
    This class represents a particolar state.
    States are immutable; state transitions produce new States
    """
    def __init__(self,state=None):
        self.__s = state

    @staticmethod
    def load(filename):
        """
        load a state from the file in the path filename
        the state must respect this sintax:
            [varname = int \n]*
        otherwise an exception is raised
        """
        state = dict()
        pattern = re.compile("^((\s*)([a-z]+[a-z0-9]*)(\s*)=(\s*)(-?)([0-9]+)(\s*)(\\n+))*$")
        with open(filename,'r') as f:
            raw_memory = f.read()
            if pattern.match(raw_memory):
                for m in raw_memory.split('\n'):
                    if len(m)>0:
                        sep = m.find('=')
                        key = m[:sep].replace(' ','')
                        value = int(m[sep+1:])
                        state[key] = value
            else:
                raise ValueError(
                    "Invalid sintax in memory file\n"+
                    "[varname = int \\n]*")
        return State(state)

    def save(self,filename):
        """
        Save to filename the current State
        """
        dump = ""
        for k in self.__s.keys():
            val = str(self.__s[k])
            dump += k+" = "+val+"\n"
        with open(filename,'w') as o:
            o.write(dump)

    def get_val(self,varname):
        """
        Return the value of a variable if it is defined, None otherwise
        """
        if self.__s == None:
            return None
        if varname in self.__s:
            return self.__s[varname]
        return None

    def update(self,var,val):
        """
        Return a copy of the current state with the update of variable var to value val
        """
        s_copy = None
        if self.__s != None:
            s_copy = dict()
            for k in self.__s.keys():
                s_copy[k] = self.__s[k]
        state = State(s_copy)
        if state.__s == None:
            state.__s = dict()
        state.__s[var] = val
        return state

    def is_undef(self):
        """
        Check if the state is undefined
        """
        if self.__s == None or len(self.__s.keys())==0:
            return True
        for k in self.__s.keys():
            if self.__s[k] == None:
                return True
        return False

    def null_state(self):
        """
        Return an undefined State
        """
        return State()

    def get_copy(self):
        s_copy = None
        if self.__s != None:
            s_copy = dict()
            for k in self.__s.keys():
                s_copy[k] = self.__s[k]
        return State(s_copy)

    def __str__(self):
        return str(self.__s)


if __name__ == '__main__':
    s = State.load('test/test.state')
    s = s.update('x',9)
    print s.is_undef()
    s = s.null_state()
    print s.is_undef()
    s = s.update('wqrgr',123)
    s.save('test/k.state')
