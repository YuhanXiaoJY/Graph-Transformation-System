# coding: utf-8

import json
from GraphBuilding import *
from GraphTransformer import *

class Input:

    # metamodel: -> Graph
    def metamodelInput(path):       
        with open(path) as p:
            metamodel = json.load(p)
        g = Graph("metamodel")
        if "classes" not in metamodel:
            raise IndexError("No classes in metamodel")
        if "relations" not in metamodel:
            raise IndexError("No relations in metamodel")
        for classes in metamodel["classes"]:
            g.addNode(classes["id"], classes["id"])
        for relations in metamodel["relations"]:
            g.addEdge(relations["source"], relations["target"], relations["id"])
        return g

    # rules: -> [(Rule(id, lhs, rhs, nacs=[(Graph)]))]
    def rulesInput(path):       
        with open(path) as p:
            rules = json.load(p)
        rule = []
        for condition in rules:
            if "id" not in condition:
                raise IndexError("Rules: No id in the condition")
            if "lhs" not in condition:
                raise IndexError("Rules: No lhs in the condition")
            if "rhs" not in condition:
                raise IndexError("Rules: No rhs in the condition")

            # lhs: stored in a Graph
            lhs = Graph(condition["id"] + ": " + "lhs")           
            if "objects" not in condition["lhs"]:
                raise IndexError("Rules conditon: No objects in the lhs")
            if "relations" not in condition["lhs"]:
                raise IndexError("Rules condition: No relations in the lhs")
            for objects in condition["lhs"]["objects"]:
                lhs.addNode(objects["id"], objects["type"])
            for relations in condition["lhs"]["relations"]:
                lhs.addEdge(relations["source"], relations["target"], relations["type"])

            # rhs: stored in a Graph
            rhs = Graph(condition["id"] + ": " + "rhs")         
            if "objects" not in condition["rhs"]:
                raise IndexError("Rules conditon: No objects in the rhs")
            if "relations" not in condition["rhs"]:
                raise IndexError("Rules condition: No relations in the rhs")
            for objects in condition["rhs"]["objects"]:
                rhs.addNode(objects["id"], objects["type"])
            for relations in condition["rhs"]["relations"]:
                rhs.addEdge(relations["source"], relations["target"], relations["type"])
                
            # nacs: stored in a list [(Graph)]
            nacs = []                    
            number = 0
            if "nacs" in condition:
                for nac in condition["nacs"]:
                    g = Graph(condition["id"] + ": " + "nac" + str(number))
                    if "objects" in nac.keys():
                        for objects in nac["objects"]:
                            g.addNode(objects["id"], objects["type"])
                    if "relations" in nac.keys():
                        for relations in nac["relations"]:
                            g.addEdge(relations["source"], relations["target"], relations["type"])
                    nacs.append(g)
                    number += 1
            rule.append(Rule(condition["id"], lhs, rhs, nacs))
        return rule

    # goal: -> Graph
    def goalInput(path):            
        with open(path) as p:
            goal = json.load(p)
        # goal: stored in a Graph
        g = Graph("goal")         
        if "objects" in goal["graph"]:
            for objects in goal["graph"]["objects"]:
                g.addNode(objects["id"],objects["type"])
        if "relations" in goal["graph"]:
            for relations in goal["graph"]["relations"]:
                g.addEdge(relations["source"],relations["target"],relations["type"])

        trivial = Graph("trivial")

        # nacs: stored in a list [(Graph)]
        nacs=[]                
        number = 0
        if "nacs" in goal:
            for nac in goal["nacs"]:
                _g = Graph("nac" + str(number))
                if "objects" in nac.keys():
                    for objects in nac["objects"]:
                        _g.addNode(objects["id"], objects["type"])
                if "relations" in nac.keys():
                    for relations in nac["relations"]:
                        _g.addEdge(relations["source"], relations["target"], relations["type"])
                nacs.append(_g)
                number += 1
        Goal = Rule("goal", g, trivial, nacs)
        return Goal

    # instance: -> Graph
    def instanceInput(path):            
        with open(path, encoding='UTF-8') as p:
            instance = json.load(p)
        g = Graph("instance")
        if "objects" not in instance:
            raise IndexError("No objects in instance")
        if "relations" not in instance:
            raise IndexError("No relations in instance")

        for objects in instance["objects"]:
            g.addNode(objects["id"], objects["type"])
        for relations in instance["relations"]:
            g.addEdge(relations["source"], relations["target"], relations["type"])
        return g


if __name__ == "__main__":

    # test
    print("Test metamodelInput")
    metamodel = Input.metamodelInput("examples//eight_puzzles//metamodel.json")
    metamodel.print()

    print("*****************************")
    print("Test rulesInput")
    rules = Input.rulesInput("examples//eight_puzzles//rules.json")
    for rule in rules:
        print("------------")
        rule.print()

    print("*****************************")
    print("Test goalInput")
    goal = Input.goalInput("examples//eight_puzzles//goal.json")
    goal.print()

    print("*****************************")
    print("Test instanceInput")
    instance = Input.instanceInput("examples//eight_puzzles//instances//trivial.json")
    instance.print()













        