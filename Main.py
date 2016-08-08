# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:39:52 2016

@author: Kozmik
"""
from tkinter import *
import pickle
import JournalWidgets as W
import JournalObject as J
class Main:
    def __init__(self):
        welcome = ("Welcome!\n\nThis entry is an introduction and a bugfix " 
"(working on it!). I know what the date says, but it's not really that " 
"year and the program is not (terribly) broken. A few things to know:\n\n"
"-The main box here is for the body of your thoughts.\n\n-The field " 
"labeled \"Tags\" is for assigning a tag to your body of thoughts. " 
"You can assign multiple tags; just make sure to separate them with " 
"commas.\n\n-The \"Parent Entry\" field is for future implementation"
", a system to link thoughts together. For now, it just holds a date, if "
"applicable.\n\n-The \"Create Linked Entry\""
" button is used to create a thought branching off of the one currently on the "
"screen (something for the \"Display Linked Entries\" button to do, eventually)."
"\n\n-This thing likes to save like crazy, sometimes unnecessarily."
" It shouldn't present too many problems, but you might end up with copies "
"of entries floating around; you can safely delete those using the \"Delete\""
" button.\n\n-Development is ongoing. Have a suggestion? Send me a message."
"\n\nFeel free to do whatever you want with this entry: use it "
"for notes or reference, delete it, write mocking jibes about the project developer in "
"the safety and comfort of your own home, impress your friends by writing mocking"
" jibes about the project developer, the possiblities are endless!\n\n\nGood writing!")
        self.journal = {19000101000000:[welcome, ["Welcome"], None]}
        try:
            fin = open("Reg.bin", "rb")
            self.journal = pickle.load(fin)
        except FileNotFoundError:
            fin = open("Reg.bin", "wb")
        fin.close()
        self.master = Tk()
        self.master.title("Journal")
        self.journal_obj = J.JournalObj(self.journal)
        self.entry = W.EntryFrame(self.master)
        self.date = W.DateFrame(self.master, self.journal_obj, self.entry)
        self.options = W.OptionsFrame(self, self.master, self.date, self.entry, self.journal_obj)
        dframe = self.date.CreateDateFrame().pack(side=TOP)        
        eframe = self.entry.CreateEntryFrame().pack(side=TOP, expand=1, fill=BOTH)
        oframe = self.options.CreateOptionsFrame().pack(side=TOP)
        
        self.master.protocol("WM_DELETE_WINDOW", self.Destroy)
        
    def Run(self):
        self.master.mainloop()
        
    def Destroy(self):
        self.options.checkSaved()
        fout = open("Reg.bin", "wb")
        pickle.dump(self.journal, fout)
        fout.close()
        self.master.destroy()
        
        
app = Main()
app.Run()