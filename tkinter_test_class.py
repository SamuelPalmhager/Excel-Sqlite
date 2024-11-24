# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:17:53 2024

@author: Samuel
"""
#command=lambda: executeButton(input_text_box.get("1.0", "end"))
import tkinter as tk
from tkinter import filedialog 
import pandas as pd
import os
from SQLITE3_test import sqliteHandler
    
class tkInterface:
    
    def __init__(self):
        self.window = tk.Tk()
        self.name = ""
        
    def tkTest(self):
        
        self.window.geometry("1500x900")
        
        self.inputBoxFrame = tk.Frame(self.window, width = 600, height = 900, bg = "grey") 
        self.inputBoxFrame.place(relx=1.0, rely=0.0, anchor="ne")    
        
        global input_text_box
        self.input_text_box = tk.Text(master = self.inputBoxFrame, width = 60, height = 40, font = ("Lucida Console", 10, "bold"))
        self.input_text_box.place(relx=1.0, rely = 0.0, anchor = "ne")
        self.input_text_box.insert("1.0", "UPDATE DataJss13 SET age = 30 WHERE Id = 1")
        
        self.buttonExecute = tk.Button(master = self.inputBoxFrame, width = 10, bg = "white", text = "Execute",                               
                                  font= ("Lucida Console", 10, "bold"), command = self.retrieveSQLQuery)
        self.buttonExecute.place(relx = 0.426, rely = 0.71, anchor = "se")    
        
        self.buttonUpload = tk.Button(master = self.inputBoxFrame, width = 17, bg = "white", text = "Upload excelfile", 
                        font= ("Lucida Console", 10, "bold"), command = self.uploadExcelFile)
        self.buttonUpload.place(relx = 0.985, rely = 0.71 , anchor = "se")
        
        self.buttonFetchAll = tk.Button(master = self.inputBoxFrame, width = 10, bg = "white", text = "Table",                               
                                  font= ("Lucida Console", 10, "bold"), command = self.printTableButton)
        self.buttonFetchAll.place(relx = 0.655, rely = 0.71, anchor = 'se' )
        
        self.buttonSaveChange = tk.Button(master = self.inputBoxFrame, width = 12, bg = "white",
                                             text = "Save Changes", font= ("Lucida Console", 10, "bold"), command = self.askUser)
        self.buttonSaveChange.place(relx = 0.210, rely = 0.71, anchor = 'se' )
        
        self.outputBoxFrame = tk.Frame(self.window, width = 600, height = 700, bg = "black")
        self.outputBoxFrame.place(relx=0.0, rely=0.0, anchor="nw")    
        
        
        global output_text_box
        self.output_text_box = tk.Text()
        self.output_text_box = tk.Text(master = self.outputBoxFrame, width = 90, height = 50)
        self.output_text_box.place(relx=0.0, rely = 0.0, anchor = "nw")
        #output_text_box.config(state = tk.DISABLED)
        
        self.window.mainloop()
        
    def executeButton(self, text):
        self.output_text_box.insert("end", text)
            
    def uploadExcelFile(self):    
        self.file_path = filedialog.askopenfilename(
                title = "Select an excel-file"
                )
        print('.xlsx' in self.checkFileType(self.file_path))
        if ".xlsx" in self.checkFileType(self.file_path):
            print("You have choosen a file")
            #output_text_box.insert("1.0", data)
            self.name = os.path.basename(self.file_path)
            self.setupSQLite(self.name, self.file_path)
        else:
            self.output_text_box.insert("1.0", "You have not choosen an excel file!")
            
    def checkFileType(self, file_path):  
        return os.path.splitext(self.file_path)
        
    def setupSQLite(self, name, file_path):
        global sqlitehandler
        self.sqlitehandler = sqliteHandler(name)
        self.sqlitehandler.clearTable(name, file_path)
        self.sqlitehandler.createTable(name, file_path)
        self.sqlitehandler.populateTable(name, file_path)
        rows, column_names = self.sqlitehandler.fetchTable(name) 
        self.printTable(rows, column_names)
              
    def printTable(self, rows, column_names):
        self.output_text_box.insert("1.0", " | ".join(column_names))
        self.output_text_box.insert(tk.END, "\n")
        for j in range (len(rows)):
            row_string = " | ".join(map(str, rows[j]))
            #output_text_box.insert("1.0", row_string + "\n")
            self.output_text_box.insert(tk.END, row_string + "\n")
        
    def retrieveSQLQuery(self):
        query = self.input_text_box.get("1.0", tk.END)
        result = self.sqlitehandler.executeQuery(query)
        if type(result) is int:
            print(f"The number of rows that was affected is: {result}")
        else: 
            self.printQueryResult(result)
        
    def printQueryResult(self, result):
        self.output_text_box.delete("1.0", tk.END)
        for j in range(len(result)):
            row_string = " | ".join(map(str, result[j]))
            self.output_text_box.insert(tk.END, row_string + "\n")
    
    def printTableButton(self):
        self.output_text_box.delete("1.0", tk.END)
        rows, column_names = self.sqlitehandler.fetchTable(self.name)
        self.printTable(rows, column_names)

    def saveChanges(self):
        print(self.sqlitehandler.saveChanges(self.name, self.file_path))
        
    def askUser(self):
        result = tk.messagebox.askyesno("Confirm", "Are you sure you want to proceed?")
        if result: 
            self.saveChanges()
        else:
            print("Operation cancelled")            

    