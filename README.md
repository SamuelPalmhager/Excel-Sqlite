# Excel-Sqlite
Project for Excel management and manipulation with pandas and sqlite.

This is a Python-based application which allows the user to interact with a Excel file with SQL-queries through a friendly and easy to use Tkinter GUI. 
The project bridges the gap between spreadsheet data and database management, allowing a user to perform data manipulation without needing a dedicated setup. 

Project motivations:
 - Problem statement: It is common to store large amounts of data in Excel, however Excel lacks advanced querying capabilities. This projects bridges that gap.
 - Learning objective: Further deepening my knowledge in Python, pandas and to introduce myself to SQLite. 

Features: 
  - Excel file upload: Through the button titled 'Upload excelfile' the user can easily load a .xlsx file to the applocation.
  - SQL query execition: Run SQL queries directly on the Excel file through a embedded SQLite engine.
  - Data manipulation: Extract, inject and aggregate data seamlessly.
  - Export results: Save the changes made to the chosen Excel file.

How it works:
  - Load an Excel file: The application converts the spreadsheet to an SQLite database, do this by pressing the button labeled 'Upload excelfile'.
  - Display the spreadsheet: The application can show the contents of the spreadsheet by pressing the button labeled 'Tabel'.  
  - Write SQL queries: Users can input their chosen SQL-query and execute it by pressing the button labeled 'Execute'.
  - Confirm changes: The application can extract and save the changes made to the database by extracting it to a Excel file.  

Challanges and solutions:
- Ensuring seamless compatabillity between pandas dataframes and SQLite.
  1. Copying the contents of a Excel file dataframe to a SQLite database file. This was solved through a SQL-query that utilises placeholder values, ensuring that any data can be injected to the database.
  2. Differentiating between SQL queries that yield an result and manipulate the table. This was solved through splitting the query and checking if the keyword SELECT is the first. If the word is present the query will yield      a result and not manipulate the table.   

Technologies used:
  - Python: Main programming language.
  - Tkinter: For building the GUI.
  - SQLite: For database functionality.
  - Pandas: For data manipulation and conversion between Excel and SQLite.
