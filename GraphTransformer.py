# codeint: utf-8

import copy
from GraphBuilding import *

def getDiff(left, right):
		leftList = list(left)
		rightList = list(right)

		if len(leftList) == 0:
			return []
		elif len(rightList) == 0:
			return leftList

		for r in rightList:
			for l in leftList:
				if l == r:
					leftList.remove(l)
					break
		return leftList

class Rule:

	def __init__(self, ruleName, lhs, rhs, nacs):
		self.ruleName = ruleName
		self.lhs = lhs
		self.rhs = rhs
		self.nacs = nacs
		self.transformer = Transformer(lhs,rhs)

	def getDistant(self):
		distant = 0
		distant += len(self.transformer.nodeToAdd);
		distant += len(self.transformer.nodeToDel);
		distant += len(self.transformer.edgeToAdd);
		distant += len(self.transformer.edgeToDel);
		return distant

	def print(self):
		print("# rule name: " + self.ruleName)
		print("# lhs: ")
		self.lhs.print()
		print("# rhs: ")
		self.rhs.print()
		if len(self.nacs) != 0:
			print("# nacs: ")
			for nac in self.nacs:
				nac.print()
		else:
			print("# nacs: no nacs!")
		print("# transformer: ")
		self.transformer.print()


class Transformer:
	
	#  nodeToAdd : [(nodeName , nodeType)] 
	#  nodeToDel : [nodeName] ,  
	#  edgeToAdd : [(fromNode , ToNode , edgeType)] 
	#  edgeToDel : [(fromNode , ToNode , edgeType)] 
	def __init__(self, lhs, rhs):
		self.nodeToAdd = []
		nodes = getDiff(rhs.getAllNodes(), lhs.getAllNodes())
		for node in nodes:
			self.nodeToAdd.append((node, rhs.getNodeType(node)))
		self.nodeToDel = getDiff(lhs.getAllNodes(), rhs.getAllNodes())

		self.edgeToAdd = getDiff(rhs.getAllEdges(), lhs.getAllEdges())
		self.edgeToDel = getDiff(lhs.getAllEdges(), rhs.getAllEdges())

		self.nodeChangeNum = len(self.nodeToAdd) + len(self.nodeToDel)
		self.edgeChangeNum = len(self.edgeToAdd) + len(self.edgeToDel)
	
	def ChangeNum(self):
		return (self.nodeChangeNum, self.edgeChangeNum)

	def transform(self, graph, mapping):
		for (nodeName, nodeType) in self.nodeToAdd:
			mapping[nodeName] = nodeName
		newGraph = copy.deepcopy(graph)

		for (fromNode, ToNode, edgeType) in self.edgeToDel:
			newGraph.delEdge(mapping[fromNode], mapping[ToNode], edgeType)

		for nodeName in self.nodeToDel:
			newGraph.delNode(mapping[nodeName])

		for (nodeName, nodeType) in self.nodeToAdd:
			newGraph.addNode(mapping[nodeName], nodeType)

		for (fromNode, ToNode, edgeType) in self.edgeToAdd:
			newGraph.addEdge(mapping[fromNode], mapping[ToNode], edgeType)
		
		return newGraph

	def getTransInfo(self):
		transInfo = {}
		transInfo["nodeToAdd"] = self.nodeToAdd
		transInfo["nodeToDel"] = self.nodeToDel
		transInfo["edgeToAdd"] = self.edgeToAdd
		transInfo["edgeToDel"] = self.edgeToDel
		return transInfo

	def print(self):
		print("nodeToAdd :" , self.nodeToAdd )
		print("nodeToDel :" , self.nodeToDel )
		print("edgeToAdd :" , self.edgeToAdd )
		print("edgeToDel :" , self.edgeToDel ) 
		#print(transInfo)

 

if __name__ == '__main__':

	# test
	g = Graph("test")
	g.addNode("apple", "fruit")
	g.addNode("pear", "fruit")
	g.addNode("grape", "fruit")
	g.addEdge("apple", "pear", "next_to")
	g.addEdge("pear", "apple", "next_to")
	g.addEdge("apple", "grape", "next_to")
	g.addEdge("grape", "apple", "next_to")
	#g.addEdge("pear", "table", "on")
	
	lhs = copy.deepcopy(g)
	rhs = copy.deepcopy(g)
	
	g.addNode("table", "wood")
	g.addEdge("apple", "table", "on")
	g.print()
	print(g.getAllEdges())
	
	
	rhs.delNode("pear")
	rhs.delEdge("grape", "apple", "next_to")
	
	rhs.addNode("Mango", "fruit")
	rhs.addEdge("apple", "Mango", "next_to")
	rhs.addEdge("grape", "Mango", "next_to")
	rhs.addEdge("Mango", "grape", "next_to")
	
	#mapping = {}
	rule = Rule("trans", lhs, rhs, "nacs")
	rule.print()
	print(rule.transformer.getTransInfo())
	newGraph = rule.transformer.transform(g)
	newGraph.print()
	
	
#	g.delNode("pear")
#	g.print()
#	print(g.getAllEdges())
#	
#	g.delEdge("grape", "apple", "next_to")
#	g.print()
#	print(g.getAllEdges())





