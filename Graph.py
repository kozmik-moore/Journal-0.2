# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:24:50 2016

@author: Kozmik
"""
import sys

class SimpleGraph:
    def __init__(self):
        self.adjacency = {}
        self.parent = {}
        self.vertices = 0
        
    def addVertex(self, vertex):
        self.adjacency[vertex] = []
        self.vertices += 1
        
    def deleteVertex(self, vertex):
        if vertex in self.adjacency:
            del self.adjacency[vertex]
            self.vertices -= 1
        else:
            self.throwError("deleteVertex()", vertex)
        
    def addEdge(self, key, value):
        if key in self.adjacency:
            if value in self.adjacency:
                self.adjacency[value].append(key)
                self.parent[key] = value
            else:
                print("Graph Error: addEdge() called on non-existent child " + str(value), 
                      file=sys.stderr)
        else:
            self.throwError("addEdge()", key)
          
    def deleteEdge(self, key, value):
        if key in self.adjacency:
            if value in self.adjacency[key]:
                self.adjacency[key].remove(value)
                del self.parent[value]
            else:
                print("Graph Error: deleteEdge() called on non-existent edge", 
                      file=sys.stderr)
        else:
            self.throwError("deleteEdge()", key)
    
    def deleteAdjList(self, vertex):
        if vertex in self.adjacency:
            self.adjacency[vertex] = []
        else:
            self.throwError("deleteAdjList()", vertex)
    
    def removeParent(self, key):
        if key in self.parent:
            del self.parent[key]
        else:
            self.throwError("removeParent()", key)
                  
    def clearNetwork(self):
        for key in self.adjacency:
            self.adjacency[key] = []
            del self.parent[key]
    
    def getVertices(self):
        return self.vertices
        
    def getAdjList(self, key):
        if key in self.adjacency:
            return self.adjacency[key]
        else:
            self.throwError("getAdjList()", key)
        
    def getParent(self, key):
        if key in self.parent:
            return self.parent[key]
        else:
            self.throwError("getParent()", key)
                  
    def __str__(self):
        string = ""
        sorted_list = sorted(self.adjacency)
        for key in sorted_list:
            string += str(key) +": "+str(self.adjacency[key])+"\n"
        return string
        
    def throwError(self, method, key):
        print("\nGraph Error: " + method + " called on non-existent key \"" + 
        str(key) + "\"", file=sys.stderr)