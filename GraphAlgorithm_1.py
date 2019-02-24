# coding: utf-8

from GraphBuilding import *
from GraphTransformer import *
from GraphMatch import *
from Input import *
from Output import *
import heapq
import time
import math
import random

counter = 0
class Item:
	def __init__(self, priority, item):
		self.priority = priority
		self.item = item
	def __lt__(self, item):
		return self.priority <= item.priority

class PriorityQueue:
	def __init__(self):
		self.elements= []

	def getLen(self):
		return len(self.elements)

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, Item(priority, item))

	def get(self):
		return heapq.heappop(self.elements).item


# return (finalGraph, changeSet)
def bfs(problem, goal, rules, num):
	queue = [(problem, [])]  # [(problem, changeSet)]
	global counter
	counter =0
	n = 0
	#print(n)
	while len(queue) != 0:
		n += 1

		counter += 1
		#print("搜索结点数: ", n)
		graph = queue[0][0]
		changeSet = queue[0][1]
		queue.pop(0)
		if len(Match.getMatch(graph, goal)[0]) > num:
			#print("Goal Matched!", n)
			return (graph, changeSet)
		#print("rule", n)
		for rule in rules:
			#print(rule.ruleName)
			#rule.print()
			mappingList = Match.getMatch(graph, rule)[0]
			# print("len of mappingList : ",len(mappingList))
			# for m in mappingList:
			# 	print("&&&", m)
			for mapping in mappingList:
				#print(rule.ruleName, " applied")
				newGraph = rule.transformer.transform(graph, mapping)
				newChangeSet = list(changeSet)
				newChangeSet.append(rule.ruleName)
				queue.append((newGraph, newChangeSet))
	return (None, None)

#判断g1和g2是否相同，用于搜索时判断graph是否与goal相同
def isMatch(graph1, goal):
	graph2 = goal.lhs
	edges1 = graph1.getAllEdges()
	edges2 = graph2.getAllEdges()
	edges1Len = len(edges1)
	edges2Len = len(edges2)
	nodes1 = graph1.getAllNodes()
	nodes2 = graph2.getAllNodes()
	nodes1Len = len(nodes1)
	nodes2Len = len(nodes2)
	flag = False
	nodeChangeNum = abs(nodes2Len -nodes1Len)
	edgeChangeNum = abs(edges2Len - edges1Len)
	(mappingList, score) = Match.getMatch(graph1, goal)
	mappingListLen = len(mappingList)
	if mappingListLen > 0:
		flag = True
	return (flag, nodeChangeNum, edgeChangeNum ,score)


def transformCost(nodeNum, edgeNum):
	return 0.5*nodeNum + edgeNum

def heuristic(nodeChangeNum, edgeChangeNum, score):
	return math.sqrt(nodeChangeNum*nodeChangeNum + edgeChangeNum*edgeChangeNum) + score

def aStar(problem, goal, rules):
	#visitedNum = 0
	global counter
	counter = 0
	openList = PriorityQueue()
	openList.put(problem, 0)
	cameFrom = {}
	costSoFar = {}
	cameFrom[problem] = None
	costSoFar[problem] = 0

	while not openList.empty():
		currentGraph = openList.get()
		counter += 1
		#visitedNum += 1
		(flag, nodeChangeNum, edgeChangeNum ,score1) = isMatch(currentGraph, goal)
		if flag == True:
			return (currentGraph, cameFrom)

		for rule in rules:
			(mappingList, score2) = Match.getMatch(currentGraph, rule)
			for map in mappingList:
				newGraph = rule.transformer.transform(currentGraph, map)
				changeNum = rule.transformer.ChangeNum()
				newCost = costSoFar[currentGraph] + transformCost(changeNum[0], changeNum[1])
				if newGraph not in costSoFar or newCost < costSoFar[newGraph]:
					costSoFar[newGraph] = newCost
					h=heuristic(nodeChangeNum, edgeChangeNum, score2)
					priority = newCost + h
					print(priority, newCost, h, score2)
					openList.put(newGraph, priority)
					cameFrom[newGraph] = currentGraph
	return (None, None)

if __name__ == '__main__':
	n = 1

	# test
	# 推箱子问题
	# print("----------------------推箱子问题----------------------")
	# problem = Input.instanceInput("examples//sokoban_game//instances//trivial.json")
	# rules = Input.rulesInput("examples//sokoban_game//rules.json")
	# goal = Input.goalInput("examples//sokoban_game//goal.json")
	# # (finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	#
	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.time()
	# 	(finalGraph, changeSet) = aStar(problem, goal, rules)
	# 	#(finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	# 	counter = len(changeSet)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解推箱子问题平均搜索节点数： %.6f" % average_node)
	# print("解推箱子问题平均耗时： %.6fms" % average_time )

	# test isMatch
	#rules[0].lhs.print()
	#problem.print()
	#(finalGraph, changeSet) = aStar(problem, goal, rules)
	# if finalGraph != None:
	# 	print("####### final result: ")
	# 	finalGraph.print()
	# 	print("####### The changes: ")
	# 	for i in changeSet:
	# 		print(i)
	# 	# 输出
	# 	Output.graphOutput(finalGraph, changeSet, "examples//sokoban_game//instances//output.json",
	# 					   "examples//sokoban_game//instances//changeSet.txt")
		# check_and_visualize.py生成问题和结果图片
		# os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//trivial.json")
		# os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//output.json")

	   # 过河问题
	# print("----------------------过河问题----------------------")
	# problem = Input.instanceInput("examples//cross_river//instances//trivial.json")
	# rules = Input.rulesInput("examples//cross_river//rules.json")
	# goal = Input.goalInput("examples//cross_river//goal.json")
	# # (finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.time()
	# 	(finalGraph, changeSet) = aStar(problem, goal, rules)
	# 	#(finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	# 	#counter = len(changeSet)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000 / n
	# average_node /= n
	# print("解过河问题平均搜索节点数： %.6f" % average_node)
	# print("解过河问题平均耗时： %.6fms" % average_time)
	# (finalGraph, changeSet) = aStar(problem, goal, rules)
	# if finalGraph != None:
	# 	print("####### final result: ")
	# 	finalGraph.print()
	# 	print("####### The changes: ")
	# 	for i in changeSet:
	# 		print(i)
	# 	Output.graphOutput(finalGraph, changeSet, "examples//cross_river//instances//output.json",
	# 					   "examples//cross_river//instances//changeSet.txt")
	# 	# os.system("python3 utils/check_and_visualize.py cross_river --instance instances//trivial.json")
	# 	# os.system("python3 utils/check_and_visualize.py cross_river --instance instances//output.json")

	# 句法分析问题
	# print("----------------------句法分析问题----------------------")
	# problem = Input.instanceInput("examples//parsing//instances//trivial1.json")
	# rules = Input.rulesInput("examples//parsing//rules.json")
	# goal = Input.goalInput("examples//parsing//goal.json")
	# # (finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.clock()
	# 	(finalGraph, changeSet) = aStar(problem, goal, rules)
	# 	#(finalGraph, changeSet) = bfs(problem, goal, rules, 0)
	# 	counter = len(changeSet)
	# 	during_time = (time.clock() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解parsing问题平均搜索节点数： %.6f" % average_node)
	# print("解parsing问题平均耗时： %.6fms" % average_time )
	# (finalGraph, changeSet) = aStar(problem, goal, rules)
	# if finalGraph != None:
	# 	print("####### final result: ")
	# 	finalGraph.print()
	# 	print("####### The changes: ")
	# 	for i in changeSet:
	# 		print(i)
	# else:
	# 	print("No output")

	# # # 八数码问题
	print("----------------------数码问题----------------------")
	problem = Input.instanceInput("examples//eight_puzzles//instances//trivial.json")
	rules = Input.rulesInput("examples//eight_puzzles//rules.json")
	goal = Input.goalInput("examples//eight_puzzles//goal.json")
	average_time = 0
	average_node = 0
	for i in range(n):
		start_time = time.clock()
		(finalGraph, changeSet) = aStar(problem, goal, rules)
		#(finalGraph, changeSet) = bfs(problem, goal, rules, 0)
		#counter = len(changeSet)
		during_time = (time.clock() - start_time)
		average_time += during_time
		average_node += counter
	average_time *= 1000/n
	average_node /= n
	print("解数码问题平均搜索节点数： %.6f" % average_node)
	print("解数码问题平均耗时： %.6fms" % average_time )
	#(finalGraph, changeSet) = aStar(problem, goal, rules)
	# if finalGraph != None:
	#     print("####### final result: ")
	#     finalGraph.print()
	#     print("####### The changes: ")
	#     for i in changeSet:
	#         print(i)
	# Output.graphOutput(finalGraph, changeSet, "examples//eight_puzzles//instances//output.json", "examples//eight_puzzles//instances//changeSet.txt")
	# # os.system("python3 utils/check_and_visualize.py eight_puzzles --instance instances//trivial2.json")
	# # os.system("python3 utils/check_and_visualize.py eight_puzzles --instance instances//output.json")
	# # else:
	# #     print("No output")





