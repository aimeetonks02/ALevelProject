import pypyodbc
import database
import hashlib

#used to add new suppliers
def add_supplier():
        print("Add a Supplier")
        auth = False   
        phonetrue = False
        #runs until a name is given that isn't already in the database
        while auth == False:  
            name = input("Input the supplier's name: ")
            email = input("Enter the Supplier's email address: ")
            address = input("Input the supplier's address (separate lines by commas and press enter when you are done): ") 
            #runs until a valid phone no is entered
            while phonetrue == False:
                try:
                    phone = int(input("Enter the supplier's phone number: "))
                    if len(phone) > 11:
                        print("Please enter a valid phone number")
                    elif len(phone) < 11:
                        print("Please enter a valid phone number")
                    else:
                        phonetrue = True

                except:
                    print("Please enter a valid phone number")
            #selects all the information on suppliers with the name provided
            namegood = database.query_database("SELECT * FROM Supplier WHERE SupplierName = ?", [name])

            #if there is no supplier with that name, add the info to the supplier table
            if len(namegood) == 0:
                database.insert_database("INSERT INTO Supplier (SupplierName, Email, PostalAddress, PhoneNo) VALUES (?, ?, ?, ?)", [name,email,address,phone])
                input("Supplier Added Successfully")
                auth = True
            else:
                input("This Supplier name is already in the database; if you would like to edit this supplier please choose the 'Edit' option")

#used to find suppliers by name rather than ID
def find_supplier_by_name():
    print("Find a Supplier")
    findsupplier = input("Which supplier do you want to find?\nInput the supplier's name: ")
    #finds the ID for the supplier with that name
    supplierfound = database.query_database("SELECT SupplierID FROM Supplier WHERE SupplierName = ?", [findsupplier])
    #instantiates a supplier object with that ID
    found_supplier = supplier(supplierfound[0][0])
    return found_supplier

#used to delete suppliers that the shop no longer buys from
def delete_supplier():
    print("Delete a Supplier")
    findsupplier = input("Which supplier do you want to Delete?\nInput their name: ")
    #deletes the entry with a matching supplier name
    userfound = database.delete_database("DELETE FROM Supplier WHERE SupplierName = ?",[findsupplier])
    print("Supplier Deleted")

#used to describe a single supplier
class supplier(object):
    #instantiates aa single supplier object using the supplier ID
    def __init__(self, id):
        #finds all info on the supplier with that ID
        supplierfound = database.query_database("SELECT SupplierName, Email, PostalAddress, PhoneNo FROM Supplier WHERE SupplierID = ?", [id])
        self.SupplierID = id
        self.SupplierName = supplierfound[0][0]
        self.Email = supplierfound[0][1]
        self.PostalAddress = supplierfound[0][2]
        self.PhoneNo = supplierfound[0][3]

    #makes it so the object is printed as a list of its attributes rather than a meaningless object location
    def __str__(self):
        selflist = ("{},{},{},{},{}".format(self.SupplierID, self.SupplierName, self.Email, self.PostalAddress, self.PhoneNo))
        return selflist

    #used to change the supplier name
    def change_name(self):
        new = input("What do you want the new name to be? ")
        #updates the name in the supplier table and the object
        database.update_database("UPDATE Supplier SET SupplierName = ? WHERE SupplierID = ?",[new, self.SupplierID])
        self.SupplierName = new

    #used to change the supplier email
    def change_email(self):
        new = input("What do you want the new email to be? ")
        #updates the email in the supplier table and the object
        database.update_database("UPDATE Supplier SET Email = ? WHERE SupplierID = ?",[new, self.SupplierID])
        self.Email = new

    #used to change the supplier address
    def change_address(self):
        new = input("What do you want the new address to be? ")
        #updates the address in the supplier table and the object
        database.update_database("UPDATE Supplier SET PostalAddress = ? WHERE SupplierID = ?",[new, self.SupplierID])
        self.PostalAddress = new

    #used to change the supplier phone number
    def change_phone(self):
        new = input("What do you want the new number to be? ")
        #updates the phone number in the supplier table and the object
        database.update_database("UPDATE Supplier SET PhoneNo = ? WHERE SupplierID = ?",[new, self.SupplierID])
        self.PhoneNo = new