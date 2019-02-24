# coding: utf-8

from GraphBuilding import *
from GraphTransformer import *
from GraphMatch import *
from Input import *
from Output import *
import random 
import os
import json
import time
from math import log, sqrt

counter = 0

class MCTS():
    """
    启发式搜索: use Monte Carlo Tree Search with UCB
    """

    def __init__(self, graph, rules, goal, time=5, max_actions=1000):

        self.graph = graph
        self.rules = rules
        self.goal = goal
        self.max_actions = max_actions # 每次模拟的最大深度
        self.calculation_time = float(time) # 最大运算时间
        self.confident = 1.96  # UCB中的常数
        self.simu = {} # 模拟总次数
        self.wins = {} # 模拟中得到goal的次数
        self.max_depth = 1


    # 拓展 return （name, mapping）
    def get_action(self):
        global counter

        if len(Match.getMatch(self.graph, self.goal)) > 0:
            print("Goal Matched!")
            return (None, None)

        # 每次取得下一次变换是清空模拟simu表
        self.simu = {} 
        self.wins = {} 
        simulations = 0
        start_time = time.time()
        # 模拟
        while time.time() - start_time < self.calculation_time:
            Graph_copy = copy.deepcopy(self.graph)
            self.run_simulation(Graph_copy)
            simulations += 1

        print("total simulations = ", simulations)

        # 取得模拟之后最好的变换
        (name, mapping) = self.select_best_trans()
        print('Maximum depth searched:', self.max_depth)
        return (name, mapping)         

    # 模拟
    def run_simulation(self, graph):

        simu = self.simu
        wins = self.wins
        expand = True
        goal_match = False
        visited = set()
        availables = []
        for rule in self.rules:
            mappingList = Match.getMatch(graph, rule)
            for mapping in mappingList:
                availables.append((rule.ruleName, mapping))
                #newGraph = rule.transformer.transform(graph, mapping)
        
        for i in range(1, self.max_actions):
            if all(simu.get((name, mapping)) for (name, mapping) in availables):
                log_total = log(
                    sum(simu[(name, mapping)] for (name, mapping) in availables)) 
                value, (name, mapping) = max(((wins[(name, mapping)] / simu[(name, mapping)]) +
                     sqrt(self.confident * log_total / simu[(name, mapping)]), (name, mapping))
                    for (name, mapping) in availables)
            else:
                (name, mapping) = choice(availables)

            rule = (r for r in self.rules if name == r.ruleName)
            graph = rule.transformer.transform(graph, mapping)

            # 每次模拟最多扩展一次，每次扩展只增加一个着法
            if expand and (name, mapping) not in simu:
                expand = False
                simu[(name, mapping)] = 0
                wins[(name, mapping)] = 0
                if i > self.max_depth:
                    self.max_depth = i

            visited.add((name, mapping))

            is_full = not len(availables)
            if len(Match.getMatch(graph, self.goal)) > 0:
                goal_match = True
            if is_full or goal_match:
                break

        # Back-propagation
        for name, mapping in visited:
            if (name, mapping) not in simu:
                continue
            simu[(name, mapping)] += 1 # 当前路径上所有着法的模拟次数加1
            if goal_match:
                wins[(name, mapping)] += 1 # 获胜玩家的所有着法的胜利次数加1




    # 选取 return (name, mapping)
    def select_best_trans(self):
        availables = []
        for rule in self.rules:
            mappingList = Match.getMatch(self.graph, rule)
            for mapping in mappingList:
                availables.append((rule.ruleName, mapping))

        _name, _mapping = max(
            (self.wins.get((name, mapping), 0) /
            self.simu.get((name, mapping), 1),
            (name, mapping)) for (name, mapping) in availables)

        return (_name, _mapping)






if __name__ == '__main__':

    n = 1

    # 八数码问题
    print("----------------------八数码问题----------------------")
    problem = Input.instanceInput("examples//puzzle//instances//trivial3.json")
    rules = Input.rulesInput("examples//puzzle//rules.json")
    goal = Input.goalInput("examples//puzzle//goal.json")
    
    m = MCTS(problem, rules, goal)
    graph = problem
    while(1):
        (name, mapping) = m.get_action()
        rule = (r for r in rules if name == r.ruleName)
        newGraph = rule.transformer.transform(graph, mapping)

        if len(Match.getMatch(newGraph, goal)) > 0:
            print("Goal Matched!")
            break;

        m.graph = newGraph
        graph = newGraph














