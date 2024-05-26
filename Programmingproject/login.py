try:
    import pypyodbc
    import sys
    
except Exception as e:
    print("Error importing library.  Contact Technical Support\n System Message: %s " % str(e) )
    sys.exit()

databasePath="C:\\Users\\aimzt\\Documents\\College\\Computing\\Programmingproject\\ProgProj.accdb"

class User(object):

    def __init__(self):
        self.user = ""
        self.password = ""

        self.display_menu()


    def display_menu(self):
        print("Login Screen\n")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        option = ""
        while option == "":
            option = input("Please enter an option: ")
            if option == "1":
                self.input_details(option)
            elif option == "2":
                self.input_details(option)
            elif option == "3" or option == "x":
                exit()
            else:
                print("Invalid option input")
                option = ""

    def input_details(self, option):
        print("Enter your details")
        self.user = input("Input your username: ")
        self.password = input("Input your password: ")
        if option == "1":
            self.update_database()
        else:
            self.search_database()
            

    def search_database(self):
        

    def update_database(self):
        try:
            connect = pypyodbc.connect(
                r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                r"Dbq="+databasePath)
            cursor = connect.cursor()

        except Exception as e:
            print("Error opening database ",databasePath," Contact Technical Support\n System Message: %s " % str(e) )
            sys.exit()
        print("Connection made")

        try:
            cursor.execute ("INSERT INTO Users (Username, Password) VALUES (?, ?) ",(self.user,self.password))
            connect.commit()
            print("Record Created")
        except Exception as e:
            print("Error updating project test table. Contact Technical Support\n System Message: %s" % str(e))
    
        cursor.close()
        connect.close()

user_ref = User()
