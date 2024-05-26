import database

database.insert_database("INSERT INTO Users (Username, Password) VALUES (?, ?)", ["mark","tonks"])

record = database.query_database("SELECT * FROM Users WHERE Username = 'mark'")
print(record)

database.update_database("UPDATE Users SET Password = 'password' WHERE Username = ?",["mark"])

check = database.query_database("SELECT * FROM Users WHERE Username = 'mark'")
print(check)

database.delete_database("DELETE FROM Users WHERE Username = ?",["mark"])
