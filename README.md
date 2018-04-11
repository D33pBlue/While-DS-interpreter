# While-DS-interpreter
An interpreter for Denotational Semantics of While language

## Abstract
The interpreter _I_ takes in input a _While_ program _S_ and a state _s_, and applies the Denotational Semantics in order to return the final state _I_(_S_,_s_)=S_ds[_S_]_s_. S_ds[_S_]_s_=_undef_ if and only if _I_(_S_,_s_) does not terminate. The interpreter relies on Kleene-Knaster-Tarski fixpoint iteration sequence for evaluating the while statements.

## Architecture
![alt text](documentation/Class_Diagram.png?raw=true "Class Diagram")

## Example
The following code implements in _While_ language a function that stores on variable y the factorial of x and assigns 1 to x if x is a number greater or equal to 1 and does not terminate otherwise.

```
y := 1;
while !x=1 do(
  y := y*x;
  x := x-1
)
```

Let now define a state s = <x=4,y=10,z=3>. The interpreter with the statements above and the state s returns as final state <x=1,y=24,z=3> as expected.
