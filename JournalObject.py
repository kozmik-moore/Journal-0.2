# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 16:08:09 2016

@author: Kozmik
"""

from Graph import SimpleGraph as graph
import sys

class JournalObj:
    def __init__(self, dict=None):
        """Expects a dictionary of lists, each int(key) pointing to a list 
           containing ["body", "tags[]", "int(parent)"]"""
        self.dict = {}
        self.dict = dict
        self.graph = graph()
        
    def __str__(self):              #WIP: print whole journal to string
        print("Test")
        
    def getBody(self, key):
        return self.dict[key][0]
        
    def getTags(self, key):
        return self.dict[key][1]
        
    def getParent(self, key):
        return self.dict[key][2]
            
    def getDict(self):
        return self.dict
        
    def getDictKeys(self):
        return list(self.dict.keys())
        
#    def getGraph(self):
#        return self.graph
        
    def add(self, key, body, tags, parent=None):
        self.dict[key] = []
        self.dict[key].append(body)
        tmp = tags.strip()
        tmp = tmp.split(',')
        for i in range(0, len(tmp)):
            tmp[i] = tmp[i].strip()
        self.dict[key].append(tmp)
        self.dict[key].append(parent)
#        self.graph.addVertex(key)
#        if parent.strip():
#            self.graph.addEdge(key, int(parent.strip()))
        
    def delete(self, key):
        del self.dict[key]
#        for link in self.graph.getAdjList(key):
#            self.graph.removeParent(link)
#            self.graph.deleteVertex(key)
        
    def isEntry(self, key):
        if key in self.dict:
            return True
        else:
            return False
     
#    def makeGraph(self):
#        sorted_list = sorted(self.dict)
#        for i in sorted_list:
#            self.graph.addVertex(i)
#            parent = self.dict[i][2]
#            if parent:
##                parent.strip()
##                parent.split(',')
##                for j in range(0, len(parent)):
#                if parent in self.dict:
#                    self.graph.addEdge(i, parent)
        