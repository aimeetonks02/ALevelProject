import pypyodbc
import database
import hashlib

#creates a new user, passing the username and password provided where the function is called
def create_user(username, password):
    auth = False   
    while auth == False:  
        password = hashlib.sha384(password.encode()).hexdigest() 
        #brings back all information on a user if one already exists under that username
        passgood = database.query_database("SELECT * FROM Users WHERE Username = ?", [username])

        #checks the length of the array that is brought back
        if len(passgood) == 0:
            #creates a new user in the Users database table
            database.insert_database("INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)", [username,password, "Staff"])
            auth = True
        return auth

def login(username, password):
    match = False

    #selects username, password, and ID from the database where the username matches the one provided
    retrieved = database.query_database("SELECT Username, Password, UserID FROM Users WHERE Username = ?", [username])
    if len(retrieved) == 0:
        return match
    else:
        founduser = retrieved[0][0]
        foundpass = retrieved[0][1]
    #encodes the password so it can be checked against the encoded passwords stored in the database
    password = hashlib.sha384(password.encode()).hexdigest()
    if foundpass == password and founduser == username:
        match = True
        global currentuser
        #makes a user object using the userID that was found in the querey
        currentuser = user(retrieved[0][2])
    return match

def find_user(username):
    try:
        #finds a userID and then creates a user object using it
        userfound = database.query_database("SELECT UserID FROM Users WHERE Username = ?", [username])
        found_user = user(userfound[0][0])
    except:
        found_user = False
    return found_user

def delete_user(username):
    try:
        exist = find_user(username)
        if exist == False:
            return None
        #deletes the appropriate user from the users table
        database.delete_database("DELETE FROM Users WHERE Username = ?",[username])
        return True
    except:
        return None 

def list_users():
    #creates an empty array
    allusers = []
    #selects all the userIDs in the users table
    users = database.query_database("SELECT UserID FROM Users")
    #creates a loop that makes each userID into a user object and then appends them to the array
    for i in range(len(users)):
        nextuser = user(users[i][0])
        allusers.append(nextuser)
    return allusers

def current_user_role():
    #gets the role using the global current user variable
    return currentuser.role

class user(object):
    
    def __init__(self, id):
        #uses the ID provided to pull the details of that user from the database and fill in the rest of the attributes
        userfound = database.query_database("SELECT Username, Role, Email FROM Users WHERE UserID = ?", [id])
        self.userID = id
        self.username = userfound[0][0]
        self.role = userfound[0][1]
        self.email = userfound[0][2]

    def __str__(self):
        #used so that when objects are printed, all of the attributes are printed rather than an object location which is meaningless ot an end user
        selflist = ("{},{},{},{}".format(self.userID, self.username, self.role, self.email))
        return selflist

    def change_username(self, newusername):
        #updates the database and then the objects attributes
        database.update_database("UPDATE Users SET Username = ? WHERE UserID = ?",[newusername, self.userID])
        self.username = newusername

    def change_role(self, newrole):
        #updates the database and then the objects attributes
        database.update_database("UPDATE Users SET Role = ? WHERE UserID = ?",[newrole, self.userID])
        self.role = newrole

    def change_email(self, newemail):
        #updates the database and then the objects attributes
        database.update_database("UPDATE Users SET Email = ? WHERE UserID = ?",[newemail, self.userID])
        self.email = newemail
