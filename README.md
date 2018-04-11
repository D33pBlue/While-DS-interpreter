# While-DS-interpreter
An interpreter for Denotational Semantics of While language

## Abstract
The interpreter _I_ takes in input a _While_ program _S_ and a state _s_, and applies the Denotational Semantics in order to return the final state _I_(_S_,_s_)=S_ds[_S_]_s_. S_ds[_S_]_s_=_undef_ if and only if _I_(_S_,_s_) does not terminate. The interpreter relies on Kleene-Knaster-Tarski fixpoint iteration sequence for evaluating the while statements.

## Architecture
![alt text](documentation/Class_Diagram.png?raw=true "Class Diagram")
