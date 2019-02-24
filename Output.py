# coding : utf-8
from GraphBuilding import  *
import json

class Output:
    def graphOutput(graph, changeSet, graphPath, changeSetPath):
        graphjson = {}
        graphjson["objects"] = [{"id": node, "type": graph.getNodeType(node)} for node in graph.getAllNodes()]
        graphjson["relations"]=[]

        for fromNode in graph.getAllNodes():
            for toNode in graph.getAllNodes():
                edge = graph.getEdges(fromNode, toNode)
                if len(edge) == 0:
                    continue
                for edgetype in edge:
                    graphjson["relations"].append({"type": edgetype, "source": fromNode, "target": toNode})

        with open(graphPath, 'w') as p1:    
            json.dump(graphjson, p1)
        #这里是输出changeSet，即每次移动的集合，放在一个txt文件里
        with open(changeSetPath, 'w') as p2:  
            for change in changeSet:
                p2.write(str(change))
                p2.write('\n')



