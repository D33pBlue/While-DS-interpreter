import sys
from parsing import Parser
from state import State

prog = sys.argv[1]
state = sys.argv[2]
s = State.load(state)#'test/test.state')
print "Initial state:",s
parser = Parser()
f = parser.parse(prog)#"test/test.while")
print f,s
final_state = f.evaluate(s,True)
print "Final state:",final_state
final_state.save("test/result.state")
