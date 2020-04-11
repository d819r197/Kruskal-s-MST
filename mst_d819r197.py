import sys

verbose = True

class Edge():
    def __init__(self, u, v, weight, n):
        global verbose
        if verbose: print("Initilzing Edge (" + str(u) +", " + str(v) + ") with weight: " + str(weight))
        self.u = u
        self.v = v
        self.weight = weight

class Node():
    def __init__(self, n, maxConnections):
        global verbose
        if verbose: print("Initilzing Node " + str(n))
        self.id = n
        self.connectedNodes = [None]*maxConnections

class Graph():
    def __init__(self, nc):
        global verbose
        if verbose: print("Initilzing Graph")
        self.nodeCount = nc
        self.nodeList = []
        self.edgeList = []
        self.setList = []
        for n in range(self.nodeCount):
            self.nodeList.append(Node(n, self.nodeCount))
            self.setList.append([n])

    def printGraph(self):
        for node in self.nodeList:
            print("Node " + str(node.id) + " connected to: " ,end = "")
            for connection in node.connectedNodes:
                print(str(connection) + " ", end = "")
            print(" ")


    def findSet(self, vertex):
        if verbose: print("Running findSet")
        for set in self.setList:
            if verbose: print("Searching for " + str(vertex) + " in " + str(set))
            if vertex in set:
                if verbose: print("Vertex found in set " + str(set))
                return set
        if verbose: print("Error: vertex not found in graph")
        return None

    def union(self, u, v):
        uSet = self.findSet(u)
        vSet = self.findSet(v)
        newSet = uSet
        if vSet != None and uSet != None:
            for vertex in vSet:
                if vertex not in newSet:
                    newSet.append(vertex)
            del self.setList[self.setList.index(uSet)]
            del self.setList[self.setList.index(vSet)]
            self.setList.append(newSet)
        else:
            if verbose: print("Error: find set returned none on u or v")

    #def findMinEdge(self):
    #    minWeight = self.edgeList[0][2]
    #    minWeightInd = 0
    #    for edge in range(len(self.edgeList)):
    #        if verbose: print("Comparing " + str(self.edgeList[edge][2]) + " to " + str(minWeight) + " with current min = " + str(minWeight))
    #        if self.edgeList[edge][2] < minWeight:
    #            minWeight = self.edgeList[edge][2]
    #            minWeightInd = edge
    #            if verbose: print("New Min Set!")
    #    if verbose: print("Min Weight Found =  " + str(minWeight))
    #    return self.edgeList[minWeightInd]

    def runKruskal(self):
        if verbose: print("Running Kruskal's Algorithm")
        A = []
        while len(self.edgeList) != 0:
            currEdge = self.edgeList.pop(0)
            u = currEdge[0]
            v = currEdge[1]
            uSet = self.findSet(u)
            vSet = self.findSet(v)
            if verbose: print("For Vertex: (" + str(u) +"," +str(v) + "), and Comparing sets: " + str(uSet) + " with " + str(vSet))
            if uSet != vSet:
                A.append([u,v])
                self.union(u, v)
        return A

    #def genEdges(self, ogEdgeList):
    #    #newList = removeDups(ogEdgeList)
    #    newList = ogEdgeList
    #    for e in range(len(newList)):
    #        self.edgeList.append(Edge(newList[e][0], newList[e][1], int(newList[e][2]), e))

def importNodes(filePath):
    global verbose
    if verbose: print("Importing: " + filePath)
    file = open(filePath, "r")
    fileLines = file.readlines()
    graphSize = len(fileLines)
    graph = Graph(graphSize)
    nodeIndex = 0
    rawEdgeList = []

    #Iterate through the lines
    for line in fileLines:
        currNode = graph.nodeList[nodeIndex]
        nodeConnections = line.split(' ')
        for nc in range(len(nodeConnections)-1):
            if nc != " " and nc != "\n":
                if verbose: print("Connecting Node " + str(nodeIndex) + " to Node " + str(nc) + " with weight " + nodeConnections[nc])
                currNode.connectedNodes[nc] = int(nodeConnections[nc])
                if int(nodeConnections[nc]) != 0:
                    rawEdgeList.append([nodeIndex, nc, int(nodeConnections[nc])])
        nodeIndex += 1
    rawEdgeList = sorted(rawEdgeList,key=lambda x: x[2])
    graph.edgeList = rawEdgeList
    #graph.genEdges(rawEdgeList)
    return graph

def removeDups(tree):
    global verbose
    newList = []
    for edge in tree:
        edgeFlip = [None] * 3
        edgeFlip[0] = edge[1]
        edgeFlip[1] = edge[0]
        edgeFlip[2] = edge[2]
        if edge not in newList and edgeFlip not in newList:
            if verbose: print("Adding Edge (" + str(edge[0]) + ", " + str(edge[1]) + ") to edgeList")
            newList.append(edge)
    return newList

def main():
    global verbose
    if verbose: print("Starting Program")
    if len(sys.argv) == 2:
        g = importNodes(sys.argv[1])
        #if verbose: print("Num of Edges: " + len(g.edgeList))
        #g.printGraph()
        mst = g.runKruskal()
        if verbose: print("\nSOLUTION\n------------------------------")
        for edge in mst:
            print(str(edge[0]) + " " + str(edge[1]))
    else:
        if verbose: print("Error: Please provide an imput file")

if __name__ == "__main__":
    main()
