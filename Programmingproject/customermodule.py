#imports the neccessary libraries
import pypyodbc
import database
import hashlib

#takes the parameters provided when the function is called
def create_customer(firstname, surname, email, address):
    try:
        #tries to insert the parameters into the customer table in order to create a new customer
        database.insert_database("INSERT INTO Customer (FirstName, Surname, Email, PostalAddress) VALUES (?, ?, ?, ?)", [firstname, surname, email, address])
        complete = True
    except:
        complete = False
    return complete

def find_customer(firstname, surname):
    try:
        #selects the customerID from the customer table where the name matches the one provided in the parameters
        customerfound = database.query_database("SELECT CustomerID FROM Customer WHERE FirstName = ? AND Surname = ?", [firstname, surname])
        #creates a customer object using the customerID that was found
        found_customer = customer(customerfound[0][0])
    except:
        found_customer = False
    #returns either False or the customer object that was created
    return found_customer


def delete_customer(firstname, surname):
    try:
        #deletes the customer from the database that has a name that matches the parameters
        database.delete_database("DELETE FROM Customer WHERE FirstName = ? AND Surname = ?",[firstname, surname])
        return True
    except:
        return None

def list_customers():
    #creates a blank array
    allcustomers = []
    #selects all the customerIDs from the customer table
    customers = database.query_database("SELECT CustomerID FROM Customer")
    for i in range(len(customers)):
        #for every ID that was pulled, a customer object is made using the ID and is then appended to the array
        nextcustomer = customer(customers[i][0])
        allcustomers.append(nextcustomer)
    #returns the array
    return allcustomers

class customer(object):

    def __init__(self, id):
        #uses the ID to find and fill in the values for the rest of the assets
        customerfound = database.query_database("SELECT FirstName, Surname, Email, PostalAddress FROM Customer WHERE CustomerID = ?", [id])
        #uses the id passed in the parameters
        self.customerID = id
        self.FirstName = customerfound[0][0]
        self.Surname = customerfound[0][1]
        self.Email = customerfound[0][2]
        self.PostalAddress = customerfound[0][3]

    def __str__(self):
        #used for formatting so that all of the assets are printed in plain english rather than an arbitrary object address
        #this is done autotmatically and does not need to be called in order to run
        selflist = ("{},{},{},{},{}".format(self.customerID, self.FirstName, self.Surname, self.Email, self.PostalAddress))
        return selflist

    def change_first_name(self, name):
        #updates the first name in the customer table for the customer with the macthing ID
        database.update_database("UPDATE Customer SET FirstName = ? WHERE CustomerID = ?",[name, self.customerID])
        #updates the name within the object as well as the table
        self.FirstName = name

    def change_surname(self, name):
        #updates the surname in the customer table for the customer with the macthing ID
        database.update_database("UPDATE Customer SET Surname = ? WHERE CustomerID = ?",[name, self.customerID])
        #updates the name within the object as well as the table
        self.Surname = name

    def change_email(self, email):
        #updates the email in the customer table for the customer with the macthing ID
        database.update_database("UPDATE Customer SET Email = ? WHERE CustomerID = ?",[email, self.customerID])
        #updates the email within the object as well as the table
        self.email = email

    def change_address(self, address):
        #updates the address in the customer table for the customer with the macthing ID
        database.update_database("UPDATE Customer SET Postaladdress = ? WHERE CustomerID = ?",[address, self.customerID])
        #updates the address within the object as well as the table
        self.PostalAddress = address
