# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 18:58:06 2024

@author: Samuel
"""

import sqlite3
import pandas as pd
import os


"""
1. Should setup the local sqlite database and cursor.
2. Create table if it does not exists.
3. Fill the table with the same number of columns as the excel file has
4. Populate each row with the same value as the row in the excelfile
5. Present the table for the user in the tkinter gui
6. Extract the SQL query from the input text box
7. Execute the SQL query and check if it yields an output or affects rows.

@param excelfile
"""
class sqliteHandler:

    def __init__(self, filename):
        global dbFileName 
        dbFileName = filename.split(".")[0] + "(1)"
        self.conn = sqlite3.connect(filename.split(".")[0] + ".db")
        print("Skapade databas om den inte fanns")
        self.cursor = self.conn.cursor()
        
    def createTable(self, filename, file_path):
        tablename = filename.split(".")[0]
        try: 
            data = pd.read_excel(file_path)
            data_dict = data.to_dict(orient = 'list')
            tablename = filename.split(".")[0]
            query =  f"CREATE TABLE IF NOT EXISTS {tablename} ({', '.join([f'[{column}] DECIMAL' for column in data_dict.keys()])})"
            self.cursor.execute(query)
            self.conn.commit();   
            print(tablename)
        except Exception as e:
             print(f"Error creating table: {e}")

           
    def populateTable(self, filename, file_path):
        tablename = filename.split(".")[0]
    
        data = pd.read_excel(file_path)
        print(data.head())
        
        for row in data.itertuples(index = False):
            query = f"INSERT INTO {tablename} ({', '.join(data.columns)}) VALUES ({', '.join(['?'] * len(data.columns))})"
            try:
                self.cursor.execute(query, tuple(row))
            except Exception as e:
                print(f"Error inserting data: {e}")
                
        self.conn.commit()

            
    def fetchTable(self, filename):
        self.cursor.execute('SELECT * FROM {}'.format(filename.split(".")[0]))
        columns_name = [description[0] for description in self.cursor.description]
        rows = self.cursor.fetchall()
        return rows, columns_name
        self.conn.close()
        
    def clearTable(self, filename, file_path):
        global tablename
        tablename = filename.split(".")[0]

        print(f"DB-file name: {dbFileName}")
        print(f"Tablename: {tablename}")
        tablename = filename.split(".")[0]
        self.cursor.execute(f"DROP TABLE IF EXISTS {tablename}")
        self.conn.commit()
        print(f"Table {tablename} dropped.")

    def executeQuery(self, query):
        if query.strip().upper().startswith("SELECT"):
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if rows:
                print("The query yielded an result!")
                return rows
            else: 
                print("The query yielded no results")
                
        else:
            self.cursor.execute(query)
            self.conn.commit()
            rowscount = self.cursor.rowcount
            if rowscount > 0:
                print(f"The number of affected rows was: {rowscount}")
                return rowscount
            else:
                print("There was no affected rows")
                return rowscount
        return "There was an error"
    
    
    """
    1. Skapa ett dataframe.to_excel objekt med nuvarande filnamn som parameter.
    2. Populera dataframen med innehållet i .db filen.
    3. Skriv över table till excel-filen. 
    4. Eftersom objektet har filnamnet som parameter, skriver det över innehålleti excel-filen med det i dataframen.
    """
    
    def saveChanges(self, filename, file_path):
        tablename = filename.split(".")[0]
        dataframe = pd.read_sql_query(f'SELECT * FROM {tablename}', self.conn)
        try:
            dataframe.to_excel(f"{filename}", index = False)
            return f"Successfully saved changes to filename"
        except Exception as e:
            return f"Error saving data {e}"
        return dataframe
        print("yalla")
        