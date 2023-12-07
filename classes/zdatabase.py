import mysql.connector

class Database():

   connection = None
   cursor = None

   def __init__(self):
      if Database.connection is None:
         try:
            Database.connection = mysql.connector.connect(host="localhost",port=3307, user="root", password="", database="")
            Database.cursor = Database.connection.cursor()
         except Exception as error:
            print(f"Error: Connection not established {error}")
         else:
            pass

      self.connection = Database.connection
      self.cursor = Database.cursor
    
