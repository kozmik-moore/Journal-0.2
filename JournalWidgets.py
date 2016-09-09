# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 16:02:20 2016

@author: Kozmik
"""

from tkinter import *
from tkinter.ttk import *
from tkinter import font
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from datetime import datetime
from JournalObject import JGraph
import pdb

class EntryFrame:
    def __init__(self, master, journal):
        self.main = Frame(master)
        self.journal = journal
        body_font = font.Font(family='Microsoft Sans Serif', size=10)
        tags_font = font.Font(family='Microsoft Sans Serif', size=9)
#        style = Style()
#        style.configure()
        body_frame = Frame(self.main)
        self.scrollbar = Scrollbar(body_frame)
        self.body_box = Text(body_frame, font=body_font, yscrollcommand=self.scrollbar.set, wrap=WORD)
        self.scrollbar.config(command=self.body_box.yview)
        self.body_box.pack(side=LEFT, expand=True, fill=BOTH)
        self.scrollbar.pack(side=LEFT, fill=Y)
        body_frame.pack(side=TOP, expand=True, fill=BOTH)
        
        tags_frame = Frame(self.main)
        self.tagslabel = Button(tags_frame, text="Tags:", width=10, command=self.tagSelectDialog)
        self.tagslabel.pack(side=LEFT)
        self.tags_box = Text(tags_frame, font=tags_font, height=1)
        self.tags_box.pack(side=LEFT, expand=True, fill=BOTH)
        tags_frame.pack(side=TOP, expand=True, fill=X)
        
        self.parent_box = None
        
        
    def update(self, body=None, tags=None, parent=None):
        self.body_box.delete("1.0", END)
        self.tags_box.delete("1.0", END)
        self.parent_box = None
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
            self.parent_box = parent
    def getBodyBoxContents(self):
        return self.body_box.get("1.0", END).rstrip()   
    def getTagsBoxContents(self):
        return self.tags_box.get("1.0", END).rstrip()  
    def getParentBoxContents(self):
        return self.parent_box
        
    def tagSelectDialog(self):
        main = Toplevel()
        main.title('Select Tags')
        canvas = Canvas(main, highlightthickness=0)
        tagslist = list()
        for item in self.journal.getDictKeys():
            tags = self.journal.getTags(item)
            for tag in tags:
                if tag not in tagslist:
                    tagslist.append(tag)
        cb = TagsCheckboxCanvas(canvas, sorted(tagslist))
        cbdict = cb.getCheckboxDict()
        index = 0
        row = 10
        col = 0
        while index < len(cbdict.keys()):
            for i in range(0, row):
                try:
                   cbdict[sorted(cbdict.keys())[index]].grid(row=i, column=col, sticky=W)
                   index+=1 
                except IndexError:
                    break
            col+=1
        canvas.pack()
        main.grab_set()
        main.protocol('WM_DELETE_WINDOW', lambda:self.addSelectedTags(main, cb))
        
    def addSelectedTags(self, window, obj):
#        pdb.set_trace()
        string = ''
        state = obj.state()
        index = 0
        tagslist = obj.getCheckboxDict()
        for item in sorted(tagslist):
#            print(tagslist[item][1].get())
            if state[index] is True:
                string += ', ' +item
            index+=1
        if self.getTagsBoxContents():
            self.tags_box.insert(CURRENT, string)
        else:
            self.tags_box.insert(CURRENT, string.lstrip(', '))
        window.destroy()
#        None
            
    def CreateEntryFrame(self):
        return self.main
        
class OptionsFrame:
    def __init__(self, program, master, date, entry, journal, graph):
        self.main = Frame(master)
        self.main_win = program
        self.master = master
        self.entry_obj = entry
        self.journal_obj = journal 
        self.date_obj = date
        self.win = None
        self.graph = graph
        self.is_linked = BooleanVar(self.main, value=False)
        
        self.SAVE = Button(self.main, text="Save", command=self.Save).grid(row=0, column=0, columnspan=2)
        self.LINK = Button(self.main, text="Create Linked Entry", command=self.NewLink).grid(row=0, column=2, columnspan=2, sticky=EW)
        self.NEW = Button(self.main, text="New Entry", command=self.NewEntry).grid(row=0, column=4, columnspan=2)
        self.QUIT = Button(self.main, text="Quit", command=self.Quit).grid(row=1, column=0, columnspan=2)
        self.LINKS = Button(self.main, text="Display Linked Entries", command=self.DisplayLinks).grid(row=1, column=2, columnspan=2)
        self.DELETE = Button(self.main, text="Delete", command=self.Delete).grid(row=1, column=4)
#        self.HASLINKS = Checkbutton(self.main, text="Networked:", state=DISABLED, variable=linked).grid
        self.graph.DFS()
        
    def Save(self):
        b = self.entry_obj.getBodyBoxContents()
        t = sorted(self.entry_obj.getTagsBoxContents().split(','))
        for i in range(0, len(t)):
            tag = t.pop(0).strip()
            if tag:
                t.append(tag)
        if not t:
            while not t:
                t = simpledialog.askstring(title="Enter Tags", prompt="A tag is needed for this entry:\n", parent=self.master)
            t = t.split(',')
            for i in range(0, len(t)):
                t.append(t.pop(0).strip())   
        p = self.entry_obj.getParentBoxContents()
        self.entry_obj.update(b, t, p)
        d = 0
        if self.date_obj.get():
            d = self.date_obj.getDateProgramFormat()
        else:
            self.date_obj.updateDateDisplay()
            d = self.date_obj.getDateProgramFormat()
            self.graph.addVertex(d)
        self.journal_obj.add(d, b, t, p)
        if p:
            self.graph.addArc(p, d)
        if self.win:
            self.win.destroy()
        self.date_obj.addToFilterDict(self.journal_obj.getTags(self.date_obj.getDateProgramFormat()))
        self.date_obj.addToDateRegistry(self.date_obj.getDateProgramFormat())
        self.date_obj.addToCombobox(self.date_obj.getDateUserFormat())
        self.graph.DFS()
        self.date_obj.setNetworkedIndicator()
    def NewLink(self):
        if self.entry_obj.getBodyBoxContents().strip() and self.date_obj.get():
            if not self.checkSaved():
                self.throwSaveWarning()
#            tags = self.journal_obj.getTags(self.date_obj.getDateProgramFormat())
#            tags_string = ''            
#            for item in tags:
#                tags_string += item + ', '
            self.entry_obj.update(None, None, self.date_obj.getDateProgramFormat())
            self.date_obj.clear()
        elif not self.date_obj.get():
            messagebox.showinfo("Error", "There is no entry to link from.")
        elif not self.entry_obj.getBodyBoxContents().strip():
            messagebox.showinfo('Error', 'There is nothing in the body.')
        self.date_obj.clear()
    def NewEntry(self):
        if not self.checkSaved():
            self.throwSaveWarning()
        self.date_obj.clear()
        self.entry_obj.update()
    def DisplayLinks(self):
        date = self.date_obj.getDateProgramFormat()
        if date:
            main = Toplevel()
            main.title('Linked Entries')
            canvas = Canvas(main)
            canvas.pack()
            tree = self.graph.getTree(date)
            tree_tracker = []
            idtags = []
            x = 0
            y = 0
            for item in tree:
                if item not in tree_tracker:
                    tree_tracker.append(item)
                    tmp = Button(canvas, text=self.date_obj.ConvertToUserFormat(item), command=lambda this_date=item: self.openLink(main, this_date))
                    tmp.grid(row=y, column=x, sticky=E+W)
                    idtags.append(tmp)
                    x += 1
                else:
                    x -= 1
                    y += 1
            main.grab_set()
        else:
            messagebox.showinfo('Error', "No date selected.")
    def openLink(self, window, date):
        window.destroy()
        self.date_obj.updateRemote(date)
    def Delete(self):
#        pdb.set_trace()
        selection = messagebox.askyesno("Delete Entry", "Delete this entry?")
        if selection:
            date = self.date_obj.getDateProgramFormat()
            self.entry_obj.update()
            self.graph.deleteVertex(date)
            self.date_obj.removeFromFilterDict(self.journal_obj.getTags(date))
            self.date_obj.removeFromDateRegistry(date)
            self.date_obj.removeFromCombobox(self.date_obj.getDateUserFormat())
            self.journal_obj.delete(date)
            self.date_obj.clear()
            self.graph.DFS()
    def Quit(self):
        self.main_win.destroy()
        
    def isOnlyRoot(self):
        tree = self.graph.getTree()
        if len(tree) == 2:
            self.is_linked.set(False)
            return True
        else:
            self.is_linked.set(True)
            return False
            
    def setLinksButton(self):
        if self.isOnlyRoot():
            self.LINKS.config(state='disabled')
        else:
            self.LINKS.config(state='normal')        
        
    def checkSaved(self):
        body = self.entry_obj.getBodyBoxContents().strip()
        tags = sorted(self.entry_obj.getTagsBoxContents().split(','))
        for i in range(0, len(tags)):
            tag = tags.pop(0).strip()
            if tag:
                tags.append(tag)
        if body:
            date = self.date_obj.getDateProgramFormat()
            if not date:
                date = self.date_obj.getCurrentDate()
            try:
                if body != self.journal_obj.getBody(date).strip() or tags != self.journal_obj.getTags(date):
                    return False
                else:
                    return True
            except KeyError:
                return False
        else:
            return True
                
    def throwSaveWarning(self):
        selection = messagebox.askyesno("Save Entry", "Save before continuing?")
        if selection:
            self.Save()
        
    def CreateOptionsFrame(self):
        return self.main
        
class DateFrame():
    def __init__(self, master, journal, entry, graph):
        self.main = Frame(master)
        self.master = master
        self.journal_obj = journal
        self.entry_obj = entry
        self.graph = graph
        
        self.date_userformat = ""
        self.date_programformat = 0
        
        self.registry = {}
        self.MONTHS = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
        self.UpdateDateRegistry()
        
        self.date = Combobox(self.main, postcommand=self.updateComboboxSelection)
        self.date.bind("<<ComboboxSelected>>", self.Update)
        self.date.grid(row=0, column=8, columnspan=10)
        self.combo_list = []
        for key in sorted(self.registry):
            self.combo_list.append(self.registry[key])
        
        FILTER = Button(self.main, text="Filter", command=self.createFilterDialog).grid(row=0, column=18)
        self.filter_count = dict()
        self.filter_tracker = []
        for key in self.journal_obj.getDictKeys():
            self.addToFilterDict(self.journal_obj.getTags(key))        
        self.search_type = StringVar(name="Search Type", value="OR")
        
        self.style = Style()
        self.style.configure('NetInd.TLabel', foreground='black')       
        self.is_linked = StringVar(self.main, value='No Entry')
        self.HASLINKS = Label(self.main, width=12, anchor=CENTER, textvariable=self.is_linked, style='NetInd.TLabel').grid(row=0, column=0, sticky=E)
        
    def Update(self, event):
        self.date_userformat = self.date.get()
        self.date_programformat = list(self.registry.keys())[list(self.registry.values()).index(self.date_userformat)]
        body = self.journal_obj.getBody(self.date_programformat)
        tags = self.journal_obj.getTags(self.date_programformat)
        parent = self.journal_obj.getParent(self.date_programformat)
        self.entry_obj.update(body, tags, parent)
        self.setNetworkedIndicator()
    def updateRemote(self, date):
        self.date.set(self.ConvertToUserFormat(date))
        self.date_userformat = self.date.get()
        self.date_programformat = date
        body = self.journal_obj.getBody(date)
        tags = self.journal_obj.getTags(date)
        parent = self.journal_obj.getParent(date)
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
        stringdate = str(date)
        if stringdate != '':
            datestr = ''
            datestr = stringdate[6:8] + ' ' + self.MONTHS[stringdate[4:6]] + ' ' + stringdate[:4] + ', ' + stringdate[8:]
            return datestr
            
            
    def UpdateDateRegistry(self):
        self.registry = {}
        for item in self.journal_obj.getDictKeys():
            self.registry[item] = self.ConvertToUserFormat(item)
    def addToDateRegistry(self, key):
        self.registry[key] = self.ConvertToUserFormat(key)
    def removeFromDateRegistry(self, key):
        del self.registry[key]
        
        
    def updateComboboxSelection(self):
#        self.clear()
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
        self.date_userformat = self.ConvertToUserFormat(self.date_programformat)
        self.date.set(self.date_userformat)
#        self.setNetworkedIndicator()
    def clear(self):
        self.date.set('')
        self.date_programformat = 0
        self.date_userformat = ''
        self.setNetworkedIndicator()
        
        
    def addToFilterDict(self, tags):
        for tag in tags:
            if tag not in self.filter_count:
                self.filter_count[tag] = 1
                self.filter_tracker.append([tag, BooleanVar(value=True, name=tag), None])
            else:
                self.filter_count[tag] += 1
    def removeFromFilterDict(self, tags):
        for tag in tags:
            if self.filter_count[tag] > 0:
                self.filter_count[tag] -= 1
            if self.filter_count[tag] == 0:
                for item in self.filter_tracker:
                    if item[0] == tag:
                        self.filter_tracker.remove(item)
    def getFilterDict(self):
        return self.filter_count
    def getFilterTracker(self):
        return self.filter_tracker
    def getFilterSearchVar(self):
        return self.search_type
    def setFilterSearchType(self, string):
        self.search_type.set(string)        
    def implementFilters(self):
        filtered_tags = []
        if self.search_type.get() == 'OR(P)':
            self.combo_list = []
            for key in sorted(self.registry):
                self.combo_list.append(self.registry[key])
            for item in self.filter_tracker:
                if item[1].get() == False:
                    filtered_tags.append(item[0])
            for key in sorted(self.journal_obj.getDictKeys()):
                for tag in self.journal_obj.getTags(key):
                    if tag in filtered_tags:
                        self.removeFromCombobox(self.ConvertToUserFormat(key))
        elif self.search_type.get() == 'OR':
            self.combo_list = []
            for item in self.filter_tracker:
                if item[1].get() == True:
                    filtered_tags.append(item[0])        
            for key in sorted(self.journal_obj.getDictKeys()):
                for tag in self.journal_obj.getTags(key):
                    if tag in filtered_tags:
                        self.addToCombobox(self.ConvertToUserFormat(key))
        elif self.search_type.get() == 'AND':
            self.combo_list = []
            for key in sorted(self.registry):
                self.combo_list.append(self.registry[key])
            for item in self.filter_tracker:
                if item[1].get() == True:
                    filtered_tags.append(item[0])
            for key in sorted(self.journal_obj.getDictKeys()):
                if len(self.journal_obj.getTags(key)) != len(filtered_tags):
                    self.removeFromCombobox(self.ConvertToUserFormat(key))
                else:
                    for tag in self.journal_obj.getTags(key):
                        if tag not in filtered_tags:
                            self.removeFromCombobox(self.ConvertToUserFormat(key))
    
    def createFilterDialog(self):
        main = Toplevel()
        top = Frame(main)
        middle = Frame(main)
        bottom = Frame(main)
        
        scrollbar = Scrollbar(middle)
        cb_canvas = Canvas(middle, highlightthickness=0)
        main.title("Filters")
        filter_list = []
        for tag in sorted(list(self.filter_count.keys())):
            for item in self.filter_tracker:
                if item[0] == tag:
                    filter_list.append(item)
        for item in filter_list:
            item[2] = (Checkbutton(cb_canvas, text=item[0], onvalue=True, offvalue=False, variable=item[1]))
        ORPTYPE = Radiobutton(top, text="OR(P)", value="OR(P)", variable=self.getFilterSearchVar())
        ORPTYPE.grid(row=0, column=1, sticky=W)
        ORTYPE = Radiobutton(top, text="OR", value="OR", variable=self.getFilterSearchVar())
        ORTYPE.grid(row=0, column=0, sticky=W)
        ANDTYPE = Radiobutton(top, text="AND", value="AND", variable=self.getFilterSearchVar())
        ANDTYPE.grid(row=0, column=2, sticky=W)
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
        INVERT = Button(bottom, text="Invert", command=lambda:self.invertSelection(filter_list))
        ALL.grid(row=2, column=0)
        NONE.grid(row=2, column=1)
        INVERT.grid(row=2, column=2)
        top.pack(side=TOP)
        middle.pack(side=TOP)
        bottom.pack(side=TOP)
        main.grab_set()
        self.clear()
        self.entry_obj.update()
        return main
        
    def selectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(True)
    def deselectAllCheckboxes(self, filter_list):
        for i in range(0, len(filter_list)):
            filter_list[i][1].set(False)
    def invertSelection(self, filter_list):
        for i in range(0, len(filter_list)):
            if filter_list[i][1].get() == True:
                filter_list[i][1].set(False)
            else:
                filter_list[i][1].set(True)
                
    def setNetworkedIndicator(self):
        date = self.getDateProgramFormat()
        if date:
            tree = self.graph.getTree(date)
            if len(tree) == 2:
                self.is_linked.set('Not Linked')
                self.style.configure('NetInd.TLabel', foreground='gray')
            else:
                self.is_linked.set('Linked')
                self.style.configure('NetInd.TLabel', foreground='blue')
        else: 
            self.is_linked.set('No Entry')
            self.style.configure('NetInd.TLabel', foreground='black')
        
    def CreateDateFrame(self):
        return self.main
        
class TagsCheckboxCanvas:
    def __init__(self, parent=None, tags=[], sticky=W):
        self.vars_dict = {}
        self.vars = []
#        self.cb_list = []
        for tag in sorted(tags): 
            var = BooleanVar()
            self.vars_dict[tag] = Checkbutton(parent, text=tag, variable=var)
#            self.cb_list.append(chk)
#           chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
    def state(self):
        return list(map((lambda var: var.get()), self.vars))
    def getCheckboxDict(self):
        return self.vars_dict
        
class StatsModule:
    def __init__(self, journal):
        self.journal_obj = journal
        
        self.number_entries = 0
        self.most_common_tag = ''
        self.number_entries_per_tag = {}
        self.longest_linked_number = 0
        self.longest_linked_name = ''
        self.longest_entry = 0
        self.longest_entry_name = ''
        
    def numberEntriesByYear(self):
        None
    def numberEntriesbyMonth(self):
        None
    def numberEntriesbyQuarter(self):
        None
    def createBarPlot(self):
        None
    def createPiePlot(self):
        None