# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 16:02:20 2016

@author: Kozmik
"""

from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox
from datetime import datetime
from typing import TypeVar, Generic

EntryFrame = TypeVar('EntryFrame')

class EntryFrame:
    def __init__(self, master):
        self.main = Frame(master)
#        style = ttk.Style()
#        style.configure()
        self.scrollbar = Scrollbar(self.main)
        self.body_box = Text(self.main, yscrollcommand=self.scrollbar.set, wrap=WORD)
        self.scrollbar.config(command=self.body_box.yview)
        self.body_box.grid(row=4, column=2, rowspan=11, columnspan=29, sticky = NSEW, pady=3)
        self.scrollbar.grid(row=4, column=32, rowspan=11, sticky=NS)
        
        self.tagslabel = Label(self.main, text="Tags:", width=10, anchor=CENTER)
        self.tagslabel.grid(row=16, column=8)
        self.tags_box = Text(self.main, height=1)
        self.tags_box.grid(row=16, column=10, columnspan=14, sticky=EW)
        
        self.parentlabel = Label(self.main, text="Parent Entry:", width=15, anchor =CENTER).grid(row=17, column=8)
        self.parent_box = Text(self.main, height=1)
        self.parent_box.grid(row=17, column=10, columnspan=8)
        
        
    def update(self, body=None, tags=None, parent=None):
        self.body_box.delete("1.0", END)
        self.tags_box.delete("1.0", END)
        self.parent_box.delete("1.0", END)
        if body:
            self.body_box.insert(CURRENT, body)
        if tags:
            i = 1
            sorted_tags = sorted(tags)
            self.tags_box.insert(CURRENT, sorted_tags[0])
            while i < len(sorted_tags):
                self.tags_box.insert(CURRENT, ', ' + sorted_tags[i])
                i+=1
        if parent:
            self.parent_box.insert(CURRENT, parent)
    def getBodyBoxContents(self):
        return self.body_box.get("1.0", END)   
    def getTagsBoxContents(self):
        return self.tags_box.get("1.0", END)   
    def getParentBoxContents(self):
        if self.parent_box.get("1.0", END):
            return self.parent_box.get("1.0", END)
        else:
            return None
        
        
    def CreateEntryFrame(self):
        return self.main
        
class OptionsFrame:
    def __init__(self, program, master, date, entry, journal):
        self.main = Frame(master)
        self.main_win = program
        self.master = master
        self.entry_obj = entry
        self.journal_obj = journal 
        self.date_obj = date
        self.win = None
        
        self.SAVE = Button(self.main, text="Save", command=self.Save).grid(row=0, column=0, columnspan=2)
        self.LINK = Button(self.main, text="Create Linked Entry", command=self.NewLink).grid(row=0, column=2, columnspan=2, sticky=EW)
        self.NEW = Button(self.main, text="New Entry", command=self.NewEntry).grid(row=0, column=4, columnspan=2)
        self.QUIT = Button(self.main, text="Quit", command=self.Quit).grid(row=1, column=0, columnspan=2)
        self.LINKS = Button(self.main, text="Display Linked Entries", command=self.DisplayLinks).grid(row=1, column=2, columnspan=2)
        self.DELETE = Button(self.main, text="Delete", command=self.Delete).grid(row=1, column=4)
        
        
    def Save(self):
        b = self.entry_obj.getBodyBoxContents()
        t = self.entry_obj.getTagsBoxContents()
        p = self.entry_obj.getParentBoxContents()
        d = 0
        if self.date_obj.get():
            d = self.date_obj.getDateProgramFormat()
        else:
            self.date_obj.updateDateDisplay()
            d = self.date_obj.getDateProgramFormat()
        self.journal_obj.add(d, b, t, p)
        if self.win:
            self.win.destroy()
        self.date_obj.addToFilterDict(self.journal_obj.getTags(self.date_obj.getDateProgramFormat()))
        self.date_obj.addToDateRegistry(self.date_obj.getDateProgramFormat())
        self.date_obj.addToCombobox(self.date_obj.getDateUserFormat())
    def NewLink(self):
        if self.date_obj.get():
            self.checkSaved()
            self.entry_obj.update(None, None, self.date_obj.getDateProgramFormat())
            self.date_obj.clear()
        else:
            messagebox.showinfo("Link Entry", "There is no entry to link from.")
    def NewEntry(self):
        self.checkSaved()
        self.date_obj.clear()
        self.entry_obj.update()
    def DisplayLinks(self):
        self.journal_obj.getGraph()
    def Delete(self):
        selection = messagebox.askyesno("Delete Entry", "Delete this entry?")
        if selection:
            self.entry_obj.update()
            self.date_obj.removeFromFilterDict(self.journal_obj.getTags(self.date_obj.getDateProgramFormat()))
            self.date_obj.removeFromDateRegistry(self.date_obj.getDateProgramFormat())
            self.date_obj.removeFromCombobox(self.date_obj.getDateUserFormat())
            self.journal_obj.delete(self.date_obj.getDateProgramFormat())
            self.date_obj.clear()
    def Quit(self):
        self.main_win.Destroy()
        
        
    def checkSaved(self):
        if self.entry_obj.getBodyBoxContents().strip():
            try:
                parent = 0                    
                if self.entry_obj.getParentBoxContents():
                    parent = self.entry_obj.getParentBoxContents()
                else:
                    parent = None
                d = self.date_obj.getDateProgramFormat()
                if self.entry_obj.getBodyBoxContents().strip() != self.journal_obj.getBody(d).strip() \
                or self.entry_obj.getTagsBoxContents().strip().split(', ') != sorted(self.journal_obj.getTags(d))\
                or parent != self.journal_obj.getParent(d):
                    self.throwSaveWarning()
            except KeyError:
                self.throwSaveWarning()
                
    def throwSaveWarning(self):
        selection = messagebox.askyesno("Save Entry", "Save before continuing?")
        if selection:
            self.Save()
        
    def CreateOptionsFrame(self):
        return self.main
        
class DateFrame():
    def __init__(self, master, journal, entry):
        self.main = Frame(master)
        self.master = master
        self.journal_obj = journal
        self.entry_obj = entry
        
        self.date_userformat = ""
        self.date_programformat = 0
        
        self.registry = {}
        self.MONTHS = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        self.UpdateDateRegistry()
        
        self.date = Combobox(self.main, postcommand=self.updateCombobox)
        self.date.bind("<<ComboboxSelected>>", self.Update)
        self.date.grid(row=0, column=8, columnspan=10)
        self.combo_list = []
        for key in sorted(self.registry):
            self.combo_list.append(self.registry[key])
        
        FILTER = Button(self.main, text="Filter", command=self.showFilters).grid(row=0, column=18)
        self.filter_dict = dict()
        for key in self.journal_obj.getDictKeys():
            for tag in self.journal_obj.getTags(key):
                if tag not in self.filter_dict:
                    self.filter_dict[tag] = 1
                elif tag in self.filter_dict:
                    self.filter_dict[tag] += 1
        self.filter_tracker = []
        for item in sorted(list(self.filter_dict.keys())):
            self.filter_tracker.append([item, BooleanVar(value=True, name=item), None])
        self.search_type = StringVar(name="Search Type", value="OR")
        self.filter_window = ''
        
    def Update(self, event):
        self.date_userformat = self.date.get()
        self.date_programformat = list(self.registry.keys())[list(self.registry.values()).index(self.date_userformat)]
        body = self.journal_obj.getBody(self.date_programformat)
        tags = self.journal_obj.getTags(self.date_programformat)
        parent = self.journal_obj.getParent(self.date_programformat)
        self.entry_obj.update(body, tags, parent)
    def getDateUserFormat(self):
        return self.date_userformat
    def getDateProgramFormat(self):
        return self.date_programformat
    def getCurrentDate(self): #Program format
        date=datetime.today()
        return int(datetime.strftime(date, '%Y%m%d%H%M%S'))
    def get(self):
        return self.date.get()
    def ConvertToUserFormat(self, date):
        if date != '':
            datestr = ''
            datestr = date[6:8] + ' ' + self.MONTHS[date[4:6]] + ' ' + date[:4] + ', ' + date[8:]
            return datestr
            
            
    def UpdateDateRegistry(self):
        self.registry = {}
        for item in self.journal_obj.getDictKeys():
            self.registry[item] = self.ConvertToUserFormat(str(item))
    def addToDateRegistry(self, key):
        self.registry[key] = self.ConvertToUserFormat(str(key))
    def removeFromDateRegistry(self, key):
        del self.registry[key]
        
        
    def updateCombobox(self):
        self.clear()
        self.implementFilters()
        self.date['values'] = self.combo_list
    def addToCombobox(self, value):
        if value not in self.combo_list:
            self.combo_list.append(value)
    def removeFromCombobox(self, value):
        if value in self.combo_list:
            self.combo_list.remove(value)
    def updateDateDisplay(self):
        self.date_programformat = self.getCurrentDate()
        self.date_userformat = self.ConvertToUserFormat(str(self.date_programformat))
        self.date.set(self.date_userformat)
    def clear(self):
        self.date.set('')
        self.date_programformat = 0
        self.date_userformat = ''
        
        
    def addToFilterDict(self, tags):
        for tag in tags:
            if tag not in self.filter_dict:
                self.filter_dict[tag] = 1
            elif tag in self.filter_dict:
                self.filter_dict[tag] += 1
    def removeFromFilterDict(self, tags):
        for tag in tags:
            if self.filter_dict[tag] != 0:
                self.filter_dict[tag] -= 1
    def getFilterDict(self):
        return self.filter_dict
    def getFilterTracker(self):
        return self.filter_tracker
    def getFilterSearchVar(self):
        return self.search_type
    def setFilterSearchType(self, string):
        self.search_type.set(string)
    def showFilters(self):
        win = self.createFilterDialog()        
    def implementFilters(self):
        filtered_tags = []
        if self.search_type.get() == 'AND':
            self.combo_list = []
            for key in sorted(self.registry):
                self.combo_list.append(self.registry[key])
            for item in self.filter_tracker:
                if item[1].get() == False:
                    filtered_tags.append(item[0])
            for key in sorted(self.journal_obj.getDictKeys()):
                for tag in self.journal_obj.getTags(key):
                    if tag in filtered_tags:
                        self.removeFromCombobox(self.ConvertToUserFormat(str(key)))
        elif self.search_type.get() == 'OR':
            self.combo_list = []
            for item in self.filter_tracker:
                if item[1].get() == True:
                    filtered_tags.append(item[0])        
            for key in sorted(self.journal_obj.getDictKeys()):
                for tag in self.journal_obj.getTags(key):
                    if tag in filtered_tags:
                        self.addToCombobox(self.ConvertToUserFormat(str(key)))
                        
    
    def createFilterDialog(self):
        main = Toplevel()
        top = Frame(main)
        middle = Frame(main)
        bottom = Frame(main)
        
        scrollbar = Scrollbar(middle)
        cb_canvas = Canvas(middle, highlightthickness=0)
        main.title("Filters")
        filter_list = self.getFilterTracker().copy()
        for item in filter_list:
            item[2] = (Checkbutton(cb_canvas, text=item[0], onvalue=True, offvalue=False, variable=item[1]))
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.getFilterSearchVar())
        ANDTYPE.grid(row=0, column=0, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.getFilterSearchVar())
        ORTYPE.grid(row=0, column=1, sticky=W)
        item = 0
        row = 10
        col = 0
        while item < len(filter_list):
            for i in range(0, row):
                try:
                    filter_list[item][2].grid(row=i, column=col, sticky=W)
                    item+=1
                except IndexError:
                    break
            col+=1
        cb_canvas.grid(row=1, column=0, rowspan=10, columnspan=2)
        ALL = Button(bottom, text="All", command=lambda:self.selectAllCheckboxes(filter_list))
        NONE = Button(bottom, text="None", command=lambda:self.deselectAllCheckboxes(filter_list))
        ALL.grid(row=2, column=0, sticky=W)
        NONE.grid(row=2, column=1, sticky=E)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        main.grab_set()
        return main
        
    def selectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(True)
    def deselectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(False)
        
    def CreateDateFrame(self):
        return self.main
        
class Dialog:
    def __init__(self, parent=None):
        self.parent_obj = parent
        
    def throwSaveWarning(self):
        main = Toplevel()
        main.title("Warning!")
        message = Message(main, text="Save before continuing?", anchor=CENTER).grid(row=0, column=1)
        SAVE = Button(main, text="Save", command=self.parent_obj.Save)
        SAVE.grid(row=1, column=0, columnspan=2)
        DONTSAVE = Button(main, text="Don't Save", command=main.destroy)
        DONTSAVE.grid(row=1, column=2, columnspan=2)
        return main 
    def throwDeleteWarning(self):
        main = Toplevel()
        main.title("Warning")
        message = Message(main, text="Are you sure you want to delete this entry?").grid(row=0, column=1, columnspan=2, sticky=EW)
        DELETE = Button(main, text="Yes", command=self.parent_obj.Delete).grid(row=1, column=0, columnspan=2, sticky=E)
        DONTDELETE = Button(main, text="No", command=main.destroy).grid(row=1, column=2, columnspan=2, sticky=W)
        return main
    def createFilterDialog(self):
        main = Toplevel()
        top = Frame(main)
        middle = Frame(main)
        bottom = Frame(main)
        
        scrollbar = Scrollbar(middle)
        cb_canvas = Canvas(middle)
        main.title("Filters")
        filter_list = self.parent_obj.getFilterTracker().copy()
        for item in filter_list:
            item[2] = (Checkbutton(cb_canvas, text=item[0], onvalue=True, offvalue=False, variable=item[1]))
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.parent_obj.getFilterSearchVar())
        ANDTYPE.grid(row=0, column=0, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.parent_obj.getFilterSearchVar())
        ORTYPE.grid(row=0, column=1, sticky=W)
        item = 0
        row = 10
        col = 0
        while item < len(filter_list):
            for i in range(0, row):
                try:
                    filter_list[item][2].grid(row=i, column=col, sticky=W)
                    item+=1
                except IndexError:
                    break
            col+=1
        cb_canvas.grid(row=1, column=0, rowspan=10, columnspan=2)
        ALL = Button(bottom, text="All", command=lambda:self.selectAllCheckboxes(filter_list))
        NONE = Button(bottom, text="None", command=lambda:self.deselectAllCheckboxes(filter_list))
        ALL.grid(row=2, column=0, sticky=W)
        NONE.grid(row=2, column=1, sticky=E)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        return main
        
    def selectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(True)
    def deselectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(False)
        
        