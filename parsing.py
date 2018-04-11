import lark
from arithmetics import *
from semantics import *
from lark.tree import pydot__tree_to_png


class Parser:
    """A parser for while language"""
    def __init__(self):
        grammar = ""
        with open ("while_grammar.txt", "r") as f:
            grammar=" ".join(f.readlines())
        self.__parser = lark.Lark(grammar, start='statement')

    def parse(self,filename):
        text = ""
        with open (filename, "r") as myfile:
            for line in myfile.readlines():
                l = line.strip()
                if len(l) and l[0]!='#':
                    text +=line
        print("Program:\n"+text)
        tree = self.__parser.parse(text)
        #self.saveTreeImg(tree)
        return self.__get_function(tree)

    def saveTreeImg(self,tree):
        pydot__tree_to_png(tree, "syntaxTree.png")

    def __get_function(self,node):
        #first node must be a statement
        members = [self.__is_leaf(c) for c in node.children]
        for i in range(len(members)):
            if not members[i][0]:
                if members[i][1]=='x':
                    members[i]=(True,self.__get_var(node.children[i]))
        nchildren = len(members)
        if nchildren==1:
            # skip or (statement)
            if members[0][0]:
                #skip because it is a leaf => id function
                return Identity()
            # (statement)
            return self.__get_function(node.children[0])
        if nchildren==4:
            b = self.__get_BExp(node.children[1])
            s1 = self.__get_function(node.children[2])
            s2 = self.__get_function(node.children[3])
            return Cond(b,s1,s2)
        if members[1][0] and members[1][1]=='ASSIGN':
            var = members[0][1]
            val = self.__get_AExp(node.children[2])
            return Update(var.get_name(),val)
        if members[1][0] and members[1][1]=='CONCAT':
            s1 = self.__get_function(node.children[0])
            s2 = self.__get_function(node.children[2])
            return Composition(s1,s2)
        if members[0][0] and members[0][1]=='WHILE':
            b = self.__get_BExp(node.children[1])
            S = self.__get_function(node.children[2])
            return FixF(b,S)

    def __is_leaf(self,node):
        if node.__class__==lark.lexer.Token:
            return True,node.type
        return False,node.data

    def __get_var(self,node):
        return Var(node.children[0].value)

    def __get_n(self,node):
        return Number(int(node.children[0].value))

    def __get_b(self,node):
        if node.value=='true':
            return BoolVal(True)
        return BoolVal(False)

    def __get_BExp(self,node):
        nchildren = len(node.children)
        if nchildren==1:
            # node->true or node->false
            return self.__get_b(node.children[0])
        if nchildren==2:
            # for grammar it can be only the case "not b"
            return Not(self.__get_BExp(node.children[1]))
        # operation is always in b.children[1] and
        # can be: = <= and
        operator = node.children[1].value
        k1 = node.children[0]
        k2 = node.children[2]
        if operator=='=':
            return self.__get_AExp(k1)==self.__get_AExp(k2)
        if operator=='<=':
            return self.__get_AExp(k1)<=self.__get_AExp(k2)
        if operator=='&':
            return And(self.__get_BExp(k1),self.__get_BExp(k2))

    def __get_AExp(self,node):
        nchildren = len(node.children)
        if node.data=='n':
            return self.__get_n(node)
        if node.data=='x':
            return self.__get_var(node)
        if nchildren==1:
            child = node.children[0]
            if child.data=='n':
                return self.__get_n(child)
            if child.data=='x':
                return self.__get_var(child)
            if child.data=='a':
                return self.__get_AExp(child)
        if nchildren==2:
            operator = node.children[0].value
            a1 = node.children[1]
            return Number(0)-self.__get_AExp(a1)
        # 3 children: a1 op a2 for the grammar definition
        operator = node.children[1].value
        a1 = node.children[0]
        a2 = node.children[2]
        if operator=='+':
            return self.__get_AExp(a1)+self.__get_AExp(a2)
        if operator=='-':
            return self.__get_AExp(a1)-self.__get_AExp(a2)
        if operator=='*':
            return self.__get_AExp(a1)*self.__get_AExp(a2)
