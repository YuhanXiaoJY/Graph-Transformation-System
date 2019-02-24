# coding: utf-8

from GraphBuilding import *
from GraphTransformer import *
from GraphMatch import *
from Input import *
from Output import *
import random 
import heapq
import os
import json
import time
import math


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
def bfs(problem, goal, rules):
	global counter

	# 双队列实现随机选择下一层结点
	queue1 = [(problem, [])]  # [(problem, changeSet)]
	queue2 = []
	counter = 0
	queue = queue1
	_queue = queue2
	while len(queue) != 0:
		counter += 1
		index = int(random.random()*len(queue))
		item = queue.pop(index)
		graph = item[0]
		changeSet = item[1]

		if len(Match.getMatch(graph, goal)[0]) > 0:
			print("Goal Matched! 共搜索结点数: ", counter)
			return (graph, changeSet)

		for rule in rules:
			mappingList = Match.getMatch(graph, rule)[0]
			for mapping in mappingList:
				#print(rule.ruleName, " applied")
				newGraph = rule.transformer.transform(graph, mapping)
				newChangeSet = list(changeSet)
				newChangeSet.append(rule.ruleName)
				_queue.append((newGraph, newChangeSet))

		# 此时换队列
		if len(queue) == 0:
			if len(queue1) == 0:
				queue = queue2
				_queue = queue1
			elif len(queue2) == 0:
				queue = queue1
				_queue = queue2
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
					#print(priority, newCost, h, score2)
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
	# 
	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.time() 
	# 	(finalGraph, changeSet) = aStar(problem, goal, rules)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解推箱子问题平均搜索节点数: %.1f" % average_node)
	# print("解推箱子问题平均耗时: %.1fms" % average_time) 
	
	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	finalGraph.print()
	# 	print("The ChangeSet: ")
	# 	for i in changeSet:
	# 		print(i)
		# 输出
		#Output.graphOutput(finalGraph, changeSet, "examples//sokoban_game//instances//output.json", "examples//sokoban_game//instances//changeSet.txt")
		# check_and_visualize.py生成问题和结果图片
		#os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//trivial.json")
		#os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//output.json")
	# else:
	# 	print("No output")

	


	# 过河问题 
	# print("----------------------过河问题----------------------")
	# problem = Input.instanceInput("examples//cross_river//instances//trivial.json")
	# rules = Input.rulesInput("examples//cross_river//rules.json")
	# goal = Input.goalInput("examples//cross_river//goal.json")

	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.time()
	# 	(finalGraph, changeSet) = aStar(problem, goal, rules)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解过河问题平均搜索节点数: %.1f" % average_node)
	# print("解过河问题平均耗时: %.1fms" % average_time)

	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	finalGraph.print()
		# print("The ChangeSet: ")
	# 	# for i in changeSet:
	# 	# 	print(i)
	# 	# Output.graphOutput(finalGraph, changeSet, "examples//cross_river//instances//output.json", "examples//cross_river//instances//changeSet.txt")
	# 	# os.system("python3 utils/check_and_visualize.py cross_river --instance instances//trivial.json")
	# 	# os.system("python3 utils/check_and_visualize.py cross_river --instance instances//output.json")
	# else:
	# 	print("No output")




	#句法分析问题
	# print("----------------------句法分析问题----------------------")
	# problem = Input.instanceInput("examples//parsing//instances//trivial1.json")
	# rules = Input.rulesInput("examples//parsing//rules.json")
	# goal = Input.goalInput("examples//parsing//goal.json")

	# average_time = 0
	# average_node = 0
	# for i in range(n):
	# 	start_time = time.time()
	# 	(finalGraph, changeSet) = bfs(problem, goal, rules)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解句法问题平均搜索节点数: %.1f" % average_node)
	# print("解句法问题平均耗时: %.1fms" % average_time)

	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	finalGraph.print()
		# print("The ChangeSet: ")
		# for i in changeSet:
		# 	print(i)
	# else:
	# 	print("No output")




	# 八数码问题
	print("----------------------八数码问题----------------------")
	problem = Input.instanceInput("examples//puzzle//instances//trivial3.json")
	rules = Input.rulesInput("examples//puzzle//rules.json")
	goal = Input.goalInput("examples//puzzle//goal.json")
	
	average_time = 0
	average_node = 0
	for i in range(n): 
		start_time = time.time()
		(finalGraph, changeSet) = aStar(problem, goal, rules)	
		during_time = (time.time() - start_time)
		average_time += during_time
		average_node += counter
	average_time *= 1000/n
	average_node /= n
	print("解八数码问题平均搜索节点数: %.1f" % average_node)
	print("解八数码问题平均耗时: %.1fms" % average_time)

	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	finalGraph.print()
		# print("The ChangeSet: ")
		# for i in changeSet:
		# 	print(i)
		# Output.graphOutput(finalGraph, changeSet, "examples//puzzle//instances//output.json", "examples//puzzle//instances//changeSet.txt")
		# os.system("python3 utils/check_and_visualize.py puzzle --instance instances//trivial.json")
		# os.system("python3 utils/check_and_visualize.py puzzle --instance instances//output.json")
	# else:
	# 	print("No output")
	





