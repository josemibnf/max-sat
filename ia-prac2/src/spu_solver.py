#!/usr/bin/env python3
# -*- coding: utf -*-

""""
Práctica 2.
Código fuente : spu_solver.py
18068091G José Miguel Avellana Lopez.
X8592934L Yassine El Kihal.
"""

import argparse
import collections
import itertools
import os
import sys
import wcnf
import msat_runner

class form():
    def __init__(self):
        self.wcnfformula = wcnf.WCNFFormula()
        self.nodes={} #dict key=str, value=int
        self.dependencies=[] #list of list of int
        self.conflicts=[] #list of list of int

def readInstance(file):
    #Initialize formula
    formula = form()
    #Read nodes
    linea=file.readline()
    if linea[0]!="p":
        print("Error de formato: debe de ser p")
        print(linea)
        sys.exit()
    n_nodes = int(linea[6:])
    for i in range(n_nodes):
        formula.wcnfformula.new_var()
        formula.nodes[file.readline()[2:-1]]=i+1
    #Read dependencies
    #Lee la linea y comprueba que no sea el final del fichero.
    linea=file.readline()
    if linea == "":
        return formula
    #Comprueba que el primer elemento sea uno de los posibles.
    if linea[0]!="d" and linea[0]!="c":
        print("Error de formato: debe de ser d o c")
        print(linea)
        sys.exit()
    #Lee todas las dependencias, si no hay saltará el bucle.
    while linea[0]=="d":
        dependencie=[]
        for n in linea.split()[1:]:
            try:
                dependencie.append(formula.nodes.get(n))
            except:
                print("Error: No existe ese atributo.")
                sys.exit()
        formula.dependencies.append(dependencie)
        linea=file.readline()
        if linea == "":
            return formula
    #Comprueba que el primer elemento sea uno de los posibles.
    if  linea[0]!="c":
        print("Error de formato: debe de ser c")
        print(linea)
        sys.exit()
    #Lee todos los conflitos.
    while linea[0]=="c":
        conflict=[]
        for n in linea.split()[1:]:
            try:
                conflict.append(formula.nodes.get(n))
            except:
                print("Error: No existe ese atributo.")
                sys.exit()
        formula.conflicts.append(conflict)
        linea=file.readline()
        if linea == "":
            return formula

if __name__ == "__main__":
    #fichero de instancia.
    file=open(sys.argv[2], "r", encoding="utf-8")
    #lee la formula del archivo file.
    formula=readInstance(file)
    #Create soft clauses
    for n in formula.nodes:
        formula.wcnfformula.add_clause([formula.nodes.get(n)], weight=1)
    #Create hard clauses
    for n in formula.dependencies:
        clause=[]
        for i in range(0, len(n)):
            clause.append(n[i])
        clause[0]=-n[0]
        formula.wcnfformula.add_clause(clause, weight=wcnf.TOP_WEIGHT)
    for n in formula.conflicts:
        formula.wcnfformula.add_clause([-n[0],-n[1]], weight=wcnf.TOP_WEIGHT)
    #Solve formula
    solver=msat_runner.MaxSATRunner(sys.argv[1])
    opt, model = solver.solve(formula.wcnfformula)

    print("o ", opt)
    print("v", end="")
    for n in model:
        if n < 0:
            print("  pkg",-n, end="")
    print("")