# coding: utf-8

# 有向图模型(有重复边)
class Edge:
	def __init__(self, fromNode, ToNode, edgeType):
		self.fromNode = fromNode
		self.ToNode = ToNode
		self.edgeType = edgeType

	def getFromNode(self):
		return self.fromNode

	def getToNode(self):
		return self.ToNode

	def getEdgeType(self):
		return self.edgeType

	def print(self):
		print(self.fromNode + "-->" + self.ToNode + " edgeType: " + self.edgeType)
		
class Node:		
	def __init__(self, nodeName, nodeType):
		self.nodeName = nodeName
		self.nodeType = nodeType
		self.edges = {}   # { ToNode : [(Edge)] }

	def addEdge(self, ToNode, edgeType):
		e = Edge(self.nodeName, ToNode, edgeType)
		if ToNode in self.edges:
			self.edges[ToNode].append(e)
		else:
			self.edges[ToNode] = [e]			

	def delEdge(self, ToNode, edgeType):
		for edge in self.edges[ToNode]:
			if edge.edgeType == edgeType:
				self.edges[ToNode].remove(edge)
				return
		raise IndexError("delEdge in Node: No edge matches!")
	
	def delEdges(self, ToNode):
		if ToNode in self.edges:
			del self.edges[ToNode]
		else:
			raise IndexError("delEdges in Node: No edges matches!")

	def delAllEdges(self):
		self.edges = {}

	# return [(ToNode , edge.edgeType)]
	def getAllEdges(self):
		allEdges = []
		for ToNode in self.edges.keys():
			for edge in self.edges[ToNode]:
				allEdges.append((ToNode, edge.edgeType))
		return allEdges

	# return [(edge.edgeType)]
	def getAllEdges2(self):
		allEdges = []
		for ToNode in self.edges.keys():
			for edge in self.edges[ToNode]:
				allEdges.append(edge.edgeType)
		return allEdges

	def getToNodes(self):
		return list(self.edges.keys())

	def getName(self):
		return self.nodeName

	def getType(self):
		return self.nodeType

	def print(self):
		print("#Node name: " + self.nodeName + "	#Node type: " + self.nodeType)
		if len(self.edges) == 0:
			#print("No edge")
			return
		for ToNode in self.edges:
			for edge in self.edges[ToNode]:
				print("ToNode: " + edge.ToNode + "		#edgeType: " + edge.edgeType)
		
		
class Graph:

	def __init__(self, graphName):
		self.graphName = graphName
		self.nodeList = {} # nodename : []

	def hasNode(self, nodeName):
		return nodeName in self.nodeList

	def addNode(self, nodeName, nodeType):
		self.nodeList[nodeName] = Node(nodeName, nodeType)

	def delNode(self, nodeName):
		if self.hasNode(nodeName):
			del self.nodeList[nodeName]
			for _nodeName in self.nodeList.keys():
				if nodeName in self.nodeList[_nodeName].edges:
					self.nodeList[_nodeName].delEdges(nodeName)
		else:
			raise IndexError("delNode in Graph: No node matches!")

	def addEdge(self, fromNode, ToNode, edgeType):
		self.nodeList[fromNode].addEdge(ToNode, edgeType)

	def delEdge(self, fromNode, ToNode, edgeType):
		if self.hasNode(fromNode) and self.hasNode(ToNode):
			if ToNode not in self.nodeList[fromNode].edges.keys():
				raise IndexError("delEdge in Graph: fromNode has no edge to ToNode!")
			for edge in self.nodeList[fromNode].edges[ToNode]:
				if edge.edgeType == edgeType:
					self.nodeList[fromNode].edges[ToNode].remove(edge)
					return
		raise IndexError("delEdge in Graph: No fromNode or ToNode or edge!")

	def getNodeType(self, nodeName):
		if self.hasNode(nodeName):
			return self.nodeList[nodeName].nodeType
		raise IndexError("getNodeType in Graph: No node matches!")

	# return [(Edge)]
	def getEdges(self, fromNode, ToNode):
		if self.hasNode(fromNode) and self.hasNode(ToNode):
			rtnEdges = []
			if ToNode not in self.nodeList[fromNode].edges.keys():
				return rtnEdges
			for edge in self.nodeList[fromNode].edges[ToNode]:
				rtnEdges.append(edge.edgeType)
			return rtnEdges
		else:
			raise IndexError("getEdges in Graph: No node matches!")
		
	# return [nodeName]
	def getAllNodes(self):
		return self.nodeList.keys()
		
	# return { nodeName : [(ToNode , edge.edgeType)] }
	def getAllEdges2(self):
		allEdges = {} # string : []
		for nodeName in self.nodeList.keys():
			allEdges[nodeName] = self.nodeList[nodeName].getAllEdges()
		return allEdges

	# return [(fromNode , ToNode , edge.edgeType)]
	def getAllEdges(self):
		allEdges = [] # string : []
		for fromNode in self.nodeList.keys():
			edges = self.nodeList[fromNode].getAllEdges()
			for edge in edges:
				allEdges.append((fromNode, edge[0] , edge[1]))
		return allEdges
		
	def getNodeNum(self):
		return len(self.nodeList.keys())
	
	def getEdgeNum(self):
		edgeNum = 0
		for nodeName in self.nodeList.keys():
			edgeNum += len(self.nodeList[nodeName].getAllEdges())
		return edgeNum		

	def print(self):
		print("Node Num: " , self.getNodeNum())
		print("Edge Num: " , self.getEdgeNum())
		print("")
		for nodeName in self.nodeList.keys():
			self.nodeList[nodeName].print();
			print("")
		


if __name__ == '__main__':
	
	# test 
	v = Node("2", "center")
	v.addEdge("1", "right_of")
	v.addEdge("3", "left_of")
	v.addEdge("1", "bigger_than")
	v.addEdge("1", "smaller_than")
	v.delEdge("1", "smaller_than")
	v.print()
	print(v.getName())
	print(v.getType())
	print(v.getAllEdges())
	print(v.getToNodes())
	
	v.delAllEdges();
	v.print()
	print(v.getAllEdges())

	print("------------------------")
	
	g = Graph("test1")
	g.addNode("table", "wood")
	g.addNode("apple", "fruit")
	g.addNode("pear", "fruit")
	g.addEdge("apple", "pear", "next_to")
	g.addEdge("pear", "apple", "next_to")
	g.addEdge("apple", "table", "on")
	g.addEdge("pear", "table", "on")
	g.print()
	
	g.delNode("pear")
	g.print()
	
	
	print("------------------------")

	g = Graph("test2")
	g.addNode("Block_0", "Block")
	g.addNode("Block_1", "Block")
	g.addNode("Block_2", "Block")
	g.addNode("Block_3", "Block")
	g.addNode("Block_4", "Block")
	g.addNode("Block_5", "Block")
	g.addNode("Block_6", "Block")
	g.addNode("Block_7", "Block")
	g.addNode("Block_8", "Block")
	
	g.addNode("Tile_0", "Tile")
	g.addNode("Tile_1", "Tile")
	g.addNode("Tile_2", "Tile")
	g.addNode("Tile_3", "Tile")
	g.addNode("Tile_4", "Tile")
	g.addNode("Tile_5", "Tile")
	g.addNode("Tile_6", "Tile")
	g.addNode("Tile_7", "Tile")
	g.addNode("Tile_8", "Tile")
	
	g.addNode("Label_0", "Label")
	g.addNode("Label_1", "Label")
	g.addNode("Label_2", "Label")
	g.addNode("Label_3", "Label")
	g.addNode("Label_4", "Label")
	g.addNode("Label_5", "Label")
	g.addNode("Label_6", "Label")
	g.addNode("Label_7", "Label")
	g.addNode("Label_8", "Label")

	g.addEdge("Block_0", "Label_0", "is")
	g.addEdge("Block_1", "Label_1", "is")
	g.addEdge("Block_2", "Label_2", "is")
	g.addEdge("Block_3", "Label_3", "is")
	g.addEdge("Block_4", "Label_4", "is")
	g.addEdge("Block_5", "Label_5", "is")
	g.addEdge("Block_6", "Label_6", "is")
	g.addEdge("Block_7", "Label_7", "is")
	g.addEdge("Block_8", "Label_8", "is")
	
	g.addEdge("Tile_0", "Label_0", "is")
	g.addEdge("Tile_1", "Label_1", "is")
	g.addEdge("Tile_2", "Label_2", "is")
	g.addEdge("Tile_3", "Label_3", "is")
	g.addEdge("Tile_4", "Label_4", "is")
	g.addEdge("Tile_5", "Label_5", "is")
	g.addEdge("Tile_6", "Label_6", "is")
	g.addEdge("Tile_7", "Label_7", "is")
	g.addEdge("Tile_8", "Label_8", "is")
	
	g.addEdge("Block_0", "Tile_0", "on")
	g.addEdge("Block_1", "Tile_1", "on")
	g.addEdge("Block_2", "Tile_2", "on")
	g.addEdge("Block_3", "Tile_3", "on")
	g.addEdge("Block_4", "Tile_4", "on")
	g.addEdge("Block_5", "Tile_5", "on")
	g.addEdge("Block_6", "Tile_6", "on")
	g.addEdge("Block_7", "Tile_7", "on")
	g.addEdge("Block_8", "Tile_8", "on")
	
	if g.hasNode("Block_0") and g.hasNode("Tile_4") and g.hasNode("Label_8"):
		print("*********YES************")
	
	g.print()
	print(g.getAllNodes())
	print(g.getAllEdges() , "\n")
	print(g.getAllEdges())
	
	
	print("--------------")

	g = Graph("metamodel")
	g.addNode("Farmer", "Farmer")
	g.addNode("Wolf", "Wolf")
	g.addNode("Goat", "Goat")
	g.addNode("Vegetable", "Vegetable")
	g.addNode("Side", "Side")
	g.addNode("Goal", "Goal")
	g.addNode("StartingPoint", "StartingPoint")

	if g.hasNode("Farmer"):
		print("YES")

	g.addEdge("Farmer", "Side", "on")
	g.addEdge("Wolf", "Side", "on")
	g.addEdge("Goat", "Side", "on")
	g.addEdge("Vegetable", "Side", "on")
	g.addEdge("Side", "Side", "next to")
	g.addEdge("Side", "Goal", "is")
	g.addEdge("Side", "StartingPoint", "is")
	print("*********************************************")
	print(g.getEdges("Goat", "Farmer"))
	g.print()

	print("____________________")
	g.delEdge("Farmer", "Side", "on")
	g.delEdge("Side", "Side", "next to")
	g.delNode("Vegetable")
	g.print()
	print(g.getAllNodes())






			
