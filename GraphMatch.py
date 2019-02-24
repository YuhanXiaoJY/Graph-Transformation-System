# coding : utf-8

from GraphTransformer import *
from Input import Input
from math import sqrt, log
	
class Match:
	# return [(mapping)] mapping: {} rule.lhs -> graph
	def getMatch(graph, rule):
		mappingList = Match.getAllMapping(rule.lhs, graph, {})
		score = 0

		# deal with nacs 
		for mapping in mappingList:
			nacMatched = False
			for nac in rule.nacs:
				mapped = {}
				nacNodes = nac.getAllNodes()
				for i in mapping.keys():
					if i in nacNodes:
						mapped[i] = mapping[i]

				nacMappingList = Match.getAllMapping(nac, graph, mapped)
				if len(nacMappingList) != 0 and nacMappingList != [{}]:
					score += (len(nacMappingList))
					#score += 1
					nacMatched = True
					#break
			if nacMatched == True:
				mappingList.remove(mapping)

		#score = -len(mappingList)
		return (mappingList, score)


	# return [(mapping)]
	# 在G2中寻找G1的同构子图
	def getAllMapping(graph1, graph2, mapped):
		mapping = {}        # mapping: g1 -> g2 
		mappingList = []    # [(mapping)]
		unMappedNodes1 = [] # nodes not mapped in G1: [(node)]
		unMappedNodes2 = [] # nodes not mapped in G2: [(node)]

		for i in graph1.getAllNodes():
			if i in mapped.keys():
				mapping[i] = mapped[i]
			else:
				mapping[i] = None

		for i in graph1.getAllNodes():
			if mapping[i] == None:
				unMappedNodes1.append(i)
		for i in graph2.getAllNodes():
			if i not in mapping.values():
				unMappedNodes2.append(i)

		# 深搜遍历所有可能的mapping组合
		def searchMapping(graph1, graph2, mapped, mappingList, unMappedNodes1, unMappedNodes2):
			if len(unMappedNodes1) == 0:
				mappingList.append(dict(mapped))
				return
			if len(unMappedNodes2) == 0:
				return 
			i = unMappedNodes1.pop(0)     # 弹出第一个
			for j in [j for j in unMappedNodes2 if graph1.getNodeType(i) == graph2.getNodeType(j)]:
				if Match.check(graph1, graph2, i , j) == False:
					continue
				mapped[i] = j
				unMappedNodes2.remove(j)
				searchMapping(graph1, graph2, mapped, mappingList, unMappedNodes1, unMappedNodes2)
				unMappedNodes2.append(j)
				mapped[i] = None
			unMappedNodes1.append(i)

		searchMapping(graph1, graph2, mapping, mappingList, unMappedNodes1, unMappedNodes2)

		mappingToDel = []
		for m in mappingList:
			if Match.checkMapping(graph1, graph2, m) == False:
				mappingToDel.append(m)
		for m in mappingToDel:
			mappingList.remove(m)

		return mappingList

	# check剪枝
	def check(graph1, graph2, i, j):
		edges1 = graph1.nodeList[i].getAllEdges2() # [(edgeType)]
		edges2 = graph2.nodeList[j].getAllEdges2()
		if len(getDiff(edges1, edges2)) != 0:
			return False
		return True


	# 检查mapping是否边类型也一样
	def checkMapping(graph1, graph2, mapping):
		for node1 in mapping.keys():
			for node2 in mapping.keys():
				edgesInG1 = graph1.getEdges(node1, node2)  # [(Edge.edgeType)]
				edgesInG2 = graph2.getEdges(mapping[node1], mapping[node2])
				if len(getDiff(edgesInG1, edgesInG2)) != 0:
					return False
		return True


if __name__ == '__main__':

	# test matcher
	print("Graph Match Test")
	instance = Input.instanceInput("examples//sokoban_game//instances//trivial.json")
	rules = Input.rulesInput("examples//sokoban_game//rules.json")

	instance.print()
	rules[0].print()
	rules[1].print()
	rules[2].print()
	rules[3].print()

	mappingList = Match.getMatch(instance, rules[1])
	print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" , mappingList)


	



	