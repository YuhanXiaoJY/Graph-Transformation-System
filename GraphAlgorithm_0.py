# coding: utf-8

from GraphBuilding import *
from GraphTransformer import *
from GraphMatch_0 import *
from Input import *
from Output import *
import random 
import os
import json
import time


counter = 0

# return (finalGraph, changeSet)
def bfs(problem, goal, rules):
	global counter

	queue = [(problem, [])]  # [(problem, changeSet)]
	counter = 0
	while len(queue) != 0:
		counter += 1
		item = queue.pop(0)
		graph = item[0]
		changeSet = item[1]

		if len(Match.getMatch(graph, goal)) > 0:
			print("Goal Matched! 共搜索结点数: ", counter)
			return (graph, changeSet)

		for rule in rules:
			mappingList = Match.getMatch(graph, rule)
			for mapping in mappingList:
				#print(rule.ruleName, " applied")
				newGraph = rule.transformer.transform(graph, mapping)
				newChangeSet = list(changeSet)
				newChangeSet.append(rule.ruleName)
				queue.append((newGraph, newChangeSet))

	return (None, None)


if __name__ == '__main__':

	# test
	# 推箱子问题
	# print("----------------------推箱子问题----------------------")
	# problem = Input.instanceInput("examples//sokoban_game//instances//trivial.json")
	# rules = Input.rulesInput("examples//sokoban_game//rules.json")
	# goal = Input.goalInput("examples//sokoban_game//goal.json")

	n = 100
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
	# print("解推箱子问题平均搜索节点数: %.1f" % average_node)
	# print("解推箱子问题平均耗时: %.1fms" % average_time) 
	
	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	finalGraph.print()
	# 	print("The ChangeSet: ")
	# 	for i in changeSet:
	# 		print(i)
	# 	# 输出
	# 	#Output.graphOutput(finalGraph, changeSet, "examples//sokoban_game//instances//output.json", "examples//sokoban_game//instances//changeSet.txt")
	# 	# check_and_visualize.py生成问题和结果图片
	# 	#os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//trivial.json")
	# 	#os.system("python3 utils/check_and_visualize.py sokoban_game --instance instances//output.json")
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
	# 	(finalGraph, changeSet) = bfs(problem, goal, rules)
	# 	during_time = (time.time() - start_time)
	# 	average_time += during_time
	# 	average_node += counter
	# average_time *= 1000/n
	# average_node /= n
	# print("解过河问题平均搜索节点数: %.1f" % average_node)
	# print("解过河问题平均耗时: %.1fms" % average_time)

	# if finalGraph != None:
	# 	print("Final Result: ")
	# 	#finalGraph.print()
	# 	print("The ChangeSet: ")
	# 	for i in changeSet:
	# 		print(i)
	# 	#Output.graphOutput(finalGraph, changeSet, "examples//cross_river//instances//output.json", "examples//cross_river//instances//changeSet.txt")
	# 	#os.system("python3 utils/check_and_visualize.py cross_river --instance instances//trivial.json")
	# 	#os.system("python3 utils/check_and_visualize.py cross_river --instance instances//output.json")
	# else:
	# 	print("No output")




	#句法分析问题
	# print("----------------------句法分析问题----------------------")
	# problem = Input.instanceInput("examples//parsing//instances//trivial.json")
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
	# 	print("The ChangeSet: ")
	# 	for i in changeSet:
	# 		print(i)
	# else:
	# 	print("No output")




	# 八数码问题
	print("----------------------八数码问题----------------------")
	problem = Input.instanceInput("examples//puzzle//instances//trivial.json")
	rules = Input.rulesInput("examples//puzzle//rules.json")
	goal = Input.goalInput("examples//puzzle//goal.json")
	
	average_time = 0
	average_node = 0
	for i in range(n):
		start_time = time.time()
		(finalGraph, changeSet) = bfs(problem, goal, rules)	
		during_time = (time.time() - start_time)
		average_time += during_time
		average_node += counter
	average_time *= 1000/n
	average_node /= n
	print("解八数码问题平均搜索节点数: %.1f" % average_node)
	print("解八数码问题平均耗时: %.1fms" % average_time)

	if finalGraph != None:
		print("Final Result: ")
		finalGraph.print()
		print("The ChangeSet: ")
		for i in changeSet:
			print(i)
		#Output.graphOutput(finalGraph, changeSet, "examples//puzzle//instances//output.json", "examples//puzzle//instances//changeSet.txt")
		#os.system("python3 utils/check_and_visualize.py puzzle --instance instances//trivial.json")
		#os.system("python3 utils/check_and_visualize.py puzzle --instance instances//output.json")
	else:
		print("No output")
	





