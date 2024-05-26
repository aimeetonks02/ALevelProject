import pypyodbc
import sys

#This module is used for all interactions with the database so that connections do not have to be made every time that something in the database needs to be accessed or changed

#tells the program where the access database is located
databasePath="C:\\Users\\aimzt\\OneDrive\\Documents\\College\\Computing\\Programmingproject\\ProgProj.accdb"

#attempts to connect to the database
try:
    connect = pypyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
        r"Dbq="+databasePath)
    cursor = connect.cursor()

#prints the error message if something goes wrong with the connection
except Exception as e:
    print("Error opening database ",databasePath," Contact Technical Support\n System Message: %s " % str(e) )
    sys.exit()
    print("Connection made")

#used to pull back information from different table, just needs the statement passing in
def query_database(statement, values = []):
  try:
    #executes the statement provided
    cursor.execute(statement, values)
    return cursor.fetchall()
  except Exception as e:
    print("Error querying table. Contact Technical Support\n System Message: %s" % str(e))

#used to insert data into the tables, just needs the statement and the new info passing in
def insert_database(statement, values):
    try:
        cursor.execute (statement, values)
        connect.commit()
        #prints the ID of the record created so that the user knows the new ID
        ID = query_database("SELECT @@IDENTITY")
        print("Record Created. The ID number is", ID[0][0])
        return ID[0][0]
    except Exception as e:
         print("Error inserting record. Contact Technical Support\n System Message: %s" % str(e))
    
#deletes entries from the database, just needs the statement passing in along with which entry is being deleted
def delete_database(statement, values):
    try:
        cursor.execute (statement, values)
        connect.commit()
    except Exception as e:
         print("Error deleting record. Contact Technical Support\n System Message: %s" % str(e))

#used to update preexisting entries in the database, needs the new attributes and the statement passing in
def update_database(statement, values):
    try:
        cursor.execute (statement, values)
        connect.commit()
    except Exception as e:
         print("Error updating table. Contact Technical Support\n System Message: %s" % str(e))

#closes the connection with the database
def close_database():
    cursor.close()
    connect.close()