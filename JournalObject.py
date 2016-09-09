# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 16:08:09 2016

@author: Kozmik
"""

import sys
import pdb

class JournalObj:
    def __init__(self, journal_file=None):
        """Expects a dictionary of lists, each int(key) pointing to a list 
           containing ["body", "tags[]", "int(parent)"]"""
        self.dict = {}
        self.dict = journal_file
        self.graph = JGraph(self)
        
    def __str__(self):
        string = str()
        for date in self.dict:
            string += "\nDATE: " + str(date) + "\nBODY:\n" + self.dict[date][0] + "\nTAGS:"
            i = 1
            string += self.dict[date][1][0]
            while i < len(self.dict[date][1]):
                string += ", " + self.dict[date][1][1]
            string += '\nPARENT:\n' + str(self.dict[date][2])
        return string
        
    def getBody(self, key):
        return self.dict[key][0]
        
    def getTags(self, key):
        return self.dict[key][1]
        
    def getParent(self, key):
        return self.dict[key][2]
            
    def getDict(self):
        return self.dict
        
    def getDictKeys(self):
        return sorted(list(self.dict.keys()))
        
    def add(self, key, body, tags, parent=None):
        self.dict[key] = []
        self.dict[key].append(body)
        self.dict[key].append(tags)
        self.dict[key].append(parent)
        
    def delete(self, key):
        del self.dict[key]
        
    def changeParent(self, key, parent=None):
        if key in self.dict:
            self.dict[key][2] = parent
        
    def isEntry(self, key):
        if key in self.dict:
            return True
        else:
            return False
            
class JGraph:
    def __init__(self, journal):
        self.journal = journal
        self.number_vertices = 0
        self.adjacency = {}
        self.parent = {}
        self.color = {}
        self.discovered = {}
        self.finished = {}
        self.time = 0
        for date in self.journal.getDictKeys():
            self.adjacency[date] = []
            parent = self.journal.getParent(date)
            if parent:
                self.adjacency[parent].append(date)
            self.number_vertices += 1
        self.tree_list = []
            
    def DFS(self):
        for date in self.journal.getDictKeys():
            self.color[date] = 'white'
            self.parent[date] = None
        self.time = 0
        self.tree_list = list(0 for x in range(0, self.number_vertices*2))
        for date in self.journal.getDictKeys():
            if self.color[date] == 'white':
                self.DFSVisit(date)
    def DFSVisit(self, date):
        self.time += 1
        self.discovered[date] = self.time
        self.tree_list[self.time-1] = date
        self.color[date] = 'gray'
        for item in self.adjacency[date]:
            if self.color[item] == 'white':
                self.parent[item] = date
                self.DFSVisit(item)
        self.color[date] = 'black'
        self.time += 1
        self.finished[date] = self.time
        self.tree_list[self.time-1] = date
            
    def addVertex(self, vertex):
        self.adjacency[vertex] = []
        self.number_vertices += 1
    def addArc(self, parent, child):
        if parent in self.adjacency:
            if child in self.adjacency:
                self.adjacency[parent].append(child)
                self.parent[child] = parent
    def deleteVertex(self, vertex):
#        pdb.set_trace()
        if vertex in self.adjacency:
            while len(self.adjacency[vertex]) > 0:
                child = self.adjacency[vertex][0]
                self.deleteArc(vertex, child)
                self.journal.changeParent(child, None)
            del self.adjacency[vertex]
            self.number_vertices -= 1
    def deleteArc(self, parent, child):
        if self.parent[child] == parent:
            self.parent[child] = None
            self.adjacency[parent].remove(child)
            
    def getGraph(self):
        None
    def getTreeRoot(self, date):
        if not self.parent:
            self.DFS()
        parent = self.parent[date]
        root = date
        while parent:
            root = parent
            parent = self.parent[parent]
        return root
    def getDiscovered(self, date=None):
        if not date:
            return self.discovered
        else:
            return self.discovered[date]
    def getFinished(self, date=None):
        if not date:
            return self.finished
        else:
            return self.finished[date]
    def getAdjacency(self):
        return self.adjacency
    def getParentDict(self):
        return self.parent
    def getTreeList(self):
        return self.tree_list
    def getTree(self, date):
        self.DFS()
        root = self.getTreeRoot(date)        
        top = self.tree_list.index(root)
        bottom = self.tree_list.index(root, top+1)
        return self.tree_list[top: bottom+1]
            