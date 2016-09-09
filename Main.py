# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:39:52 2016

@author: Kozmik
"""
from tkinter import *
from tkinter import filedialog as filedialog
import tkinter.messagebox as messagebox
import pickle
import JournalWidgets as W
import JournalObject as J
import os
from inspect import getsourcefile
from os.path import abspath
from datetime import datetime
import pdb
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
#        pdb.set_trace()
        self.journal = {19000101000000:[welcome, ["Welcome"], None]}
        self.master = Tk()
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (w*.9, h*.8))
#        self.master.rowconfigure(0, weight=1)
#        self.master.columnconfigure(0, weight=1)
        self.master.title("Journal")
        self.config_path = abspath(getsourcefile(lambda:0)).strip('Main.py')
        self.ini = {'SAVE LOCATION': None, 'BACKUP LOCATION': None, 'LAST BACKUP': None, 'BACKUP INTERVAL': -1}
        
        try:
            fin = open(self.config_path + "Journal.ini", "rb")
            self.ini = pickle.load(fin)
        except FileNotFoundError:
            self.changeSaveDirectory()
            fin = open(self.config_path + "Journal.ini", "wb")
            pickle.dump(self.ini, fin)
        fin.close()
        
        try:
            fin = open(self.ini['SAVE LOCATION'] + "Reg.jdb", "rb")
            self.journal = pickle.load(fin)
        except FileNotFoundError:
            fin = open(self.ini['SAVE LOCATION'] + "Reg.jdb", "wb")
        fin.close()
        
        self.journal_obj = J.JournalObj(self.journal)
        self.graph = J.JGraph(self.journal_obj)
        self.entry = W.EntryFrame(self.master, self.journal_obj)
        self.date = W.DateFrame(self.master, self.journal_obj, self.entry, self.graph)
        self.options = W.OptionsFrame(self, self.master, self.date, self.entry, self.journal_obj, self.graph)
                
        dframe = self.date.CreateDateFrame().pack(side=TOP)      
        eframe = self.entry.CreateEntryFrame().pack(side=TOP, expand=True, fill=BOTH)
        oframe = self.options.CreateOptionsFrame().pack(side=TOP)
       
        menubar = Menu(self.master)
        pref_menu = Menu(menubar, tearoff=0)
        pref_menu.add_command(label="Save Directory", command=self.changeSaveDirectory)
        backup_menu = Menu(pref_menu, tearoff=0)
        backup_menu.add_command(label='Select Backup Directory', command=self.changeBackupDirectory)
        interval_menu = Menu(backup_menu, tearoff=0)
        interval_menu.add_command(label='Immediately', command=self.backupDatabase)
        interval_menu.add_command(label='Day', command=lambda:self.changeBackupSchedule(24))
        interval_menu.add_command(label='3 Days', command=lambda:self.changeBackupSchedule(72))
        interval_menu.add_command(label='Week', command=lambda:self.changeBackupSchedule(168))
        interval_menu.add_command(label='Never', command=lambda:self.changeBackupSchedule(-1))
        backup_menu.add_cascade(label='Backup Database Every: ', menu=interval_menu)
        pref_menu.add_cascade(label='Backup Options', menu=backup_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.createAboutWindow)
        
        menubar.add_cascade(label="Preferences", menu=pref_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.master.config(menu=menubar)
        
        self.master.protocol("WM_DELETE_WINDOW", self.destroy)
        
        if self.ini['BACKUP INTERVAL'] != -1:
            if self.ini['BACKUP LOCATION']:
                self.checkBackup()
            else:
                self.changeBackupDirectory()
                self.checkBackup()        
        
    def run(self):
        self.master.mainloop()
        
    def destroy(self):
        if not self.options.checkSaved():
            self.options.throwSaveWarning()
        fout = open(self.ini['SAVE LOCATION'] + "Reg.jdb", "wb")
        pickle.dump(self.journal, fout)
#        pdb.set_trace()
        fout.close()
        fout = open(self.config_path + 'Journal.ini', 'wb')
        pickle.dump(self.ini, fout)
        fout.close()
        self.master.destroy()
        
        
    def changeSaveDirectory(self):
        self.dir_opt = options = {}
        if not self.ini['SAVE LOCATION']:
            options['initialdir'] = self.config_path
        else:
            options['initialdir'] = self.ini['SAVE LOCATION']
        options['mustexist'] = False
        options['parent'] = self.master
        options['title'] = 'Choose a Save Location'
        location = filedialog.askdirectory(**self.dir_opt)
        if location != '':
            self.ini['SAVE LOCATION'] = location + "/"
        
    def changeBackupDirectory(self):
        self.backup_opt = options = {}
        if not self.ini['BACKUP LOCATION']:
            options['initialdir'] = self.config_path
        else:
            options['initialdir'] = self.ini['BACKUP LOCATION']
        options['mustexist'] = False
        options['parent'] = self.master
        options['title'] = 'Choose a Backup Location'
        location = filedialog.askdirectory(**self.backup_opt)
        if location != '':
            self.ini['BACKUP LOCATION'] = location + "/Backup/"
            if not os.path.exists(self.ini['BACKUP LOCATION']):
                os.makedirs(self.ini['BACKUP LOCATION'])
            
    def changeBackupSchedule(self, time):
        self.ini['BACKUP INTERVAL'] = time
        
    def checkBackup(self):
        today = datetime.today()
        if self.ini['LAST BACKUP']:
            if (today-self.ini['LAST BACKUP']).total_seconds() > self.ini['BACKUP INTERVAL']*3600:
                self.backupDatabase()
        else:
            self.backupDatabase()
        
        
    def backupDatabase(self):
        if self.ini['BACKUP LOCATION']:
            fout = open(self.ini['BACKUP LOCATION'] + "Reg.jdb", "wb")
        else:
            self.changeBackupDirectory()
            fout = open(self.ini['BACKUP LOCATION'] + "Reg.jdb", "wb")
        pickle.dump(self.journal, fout)
        fout.close()
        self.ini['LAST BACKUP'] = datetime.today()
            
    def getDirectory(self):
        return self.ini['SAVE LOCATION']
        
    def createAboutWindow(self):
        message = "Author: kozmik-moore @ GitHub\nDeveloped using the Anaconda 3 Python Suite"
        main = messagebox.Message(title="About", message=message)
        main.show()
        
        
app = Main()
app.run()