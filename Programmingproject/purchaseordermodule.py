import pypyodbc
import database
import hashlib
import itemmodule
import suppliermodule
import stockmodule
from datetime import date

#used to create new purchase orders
def create_purchase_order():
    auth = False   
    #loops until the user verifies that the program found the right supplier
    while auth == False: 
        good = False
        #loops until the user inputs a valid supplierID
        while good == False:
            try: 
                supplierID = int(input("\nInput the ID of the supplier you wish to buy from: "))
                #selects all the data in the suppliers table with that ID to check if the supplier exists
                suppgood = database.query_database("SELECT * FROM Supplier WHERE SupplierID = ?", [supplierID])
                good = True
            except:
                print("Please enter a valid value")

        #if the length of the array is 0, the supplier doesn't exist
        #if it's more than one, a supplier has been found and the details are printed
        if len(suppgood) != 0:
            print("\nThis is the supplier we found with that ID:")
            print(suppgood)
            right = input("Is this the supplier you wanted?(Y/N) ").lower()
            if right == "y":
                auth = True
            else:
                print("Please check you have inputted the ID correctly and try again")
        else:
            print("There is no supplier in the database with that ID. Please try again")
    #gets today's date
    dateorder = date.today()
    try:
        #creates a new entry in the purchaseorder table using the information provided by calling to the database module
        database.insert_database("INSERT INTO PurchaseOrder (SupplierID, DatePurchased, Delivered) VALUES (?,?,?)", [supplierID, dateorder, "no"])
        ID = database.query_database("SELECT @@IDENTITY FROM PurchaseOrder")
        return ID[0][0]
    except Exception as e:
        print("Error updating database.  Contact Technical Support\n System Message: %s " % str(e) )

def find_order(id):
    orderfound = database.query_database("SELECT * FROM PurchaseOrder WHERE PurchaseID = ?", [id])
    if len(orderfound) != 0:
        return True
    else:
        return False

#used to make individual purchases into objects
class purchaseorder(object):

    #takes in the ID so that the rest of the attributes can be filled directly from the table
    def __init__(self, id):
        #selects all the other attributes from the purchaseorder table using the ID provided
        purchaseorderfound = database.query_database("SELECT SupplierID, DatePurchased, TotalCost, Delivered FROM PurchaseOrder WHERE PurchaseID = ?", [id])
        #finds any items in the purchaseitem table that belong in this order and puts them in an array
        itemslist = database.query_database("SELECT ItemID, Quantity FROM PurchaseItem Where PurchaseID = ?", [id])
        self.purchaseID = id
        #makes a supplier object using the supplierID found in the initial querey for this order and stores it here
        self.supplier = suppliermodule.supplier(purchaseorderfound[0][0])
        self.datepurch = purchaseorderfound[0][1]
        self.totalcost = purchaseorderfound[0][2]
        self.items = []
        self.delivered = purchaseorderfound[0][3]

        #loops until every item in the itemslist has been appended to the self.items array
        for i in itemslist:
            #creates an object for each item in the list by calling to the item module
            item = itemmodule.item(i[0], i[1])
            self.items.append(item)

    #makes sure objects print as a list of all their attributes rather than meaningless object locations
    def __str__(self):
        selflist = ("{},{},{},{}".format(self.purchaseID, self.supplier, self.datepurch, self.totalcost, self.items, self.delivered))
        return selflist

    #allows for items to be removed from the order
    def remove_item(self, itemID):
        #takes the item ID and tries to see if the item is in that order
        delitem = self.find_object(itemID)
        #if the item is in the order, removes it from the self.items list and from the purchaseitems table in the datbase
        if delitem != None:
            self.items.remove(delitem)
            database.delete_database("DELETE * FROM PurchaseItem WHERE ItemID = ? AND PurchaseID = ?",[itemID, self.purchaseID])
            #recalculates the total now that there is one less item
            self.calculate_total()
            #returns true if everything goes well
            return True
        else:
            #returns false if the item was not originally in the order
            return False

    #allows for an item to be added to the order, automatically presumes that the quantity of the item is 1 unless specified otherwise
    def add_item(self, itemID, quantity = 1):
        try:
            #looks to see if that item is already in the order
            exists = self.find_object(itemID)
            if exists == None:
                #if the item is not in the order, it makes it an object using the item module, appends it to the self.items list and adds it to the database 
                item = itemmodule.item(itemID, quantity)
                self.items.append(item)
                database.insert_database("INSERT INTO PurchaseItem (PurchaseID, ItemID, Quantity, UnitPurchPrice) VALUES (?, ?, ?, ?)", [self.purchaseID, itemID, quantity, item.price])
            else:
                #if the item was already in the order, it calls to a function that just increments the quantity to the new one specified
                self.increment_quantity(itemID, quantity)
            self.calculate_total()
            return True
        except:
            return False

    #used to list all items in an order
    def list_items(self):
        #for the length of self.items, it will print every item in the order
        for i in range(len(self.items)):
            print(self.items[i])

        #will print that the order is empty if there are no items in the list
        if len(self.items) == 0:
            print("The list is empty")
        
        #prints the total cost of the order
        print("Your total cost is: ", self.totalcost)

    #used to find if specific items are already in the order
    def find_object(self, itemID):
        for i in self.items:
            #checks the itemID provided against each itemID in the order
            if i.itemID == itemID:
                #returns i if the two IDs match
                return i
        #returns None if none of the IDs match the one provided
        return None

    #allows for the editing of quantites of items already in the order
    def edit_quantity(self, itemID, quantity):
        try:
            #finds the object in the order by the itemID and chnges its quantity to the one provided in the parameters
            self.find_object(itemID).quantity = quantity
            #updates the quantity in the database as well
            database.update_database("UPDATE PurchaseItem SET Quantity = ? WHERE ItemID = ? AND PurchaseID = ?",[quantity, itemID, self.purchaseID])
            #recalculates the total with more or less items now being in the order
            self.calculate_total()
            return True
        except:
            return False

    #used to increment the quantity instead of having the same item in the order several times
    def increment_quantity(self, itemID, quantity):
        #finds the quantity of the appropriate item via the ID and then adds the extra quantity to it 
        self.find_object(itemID).quantity = self.find_object(itemID).quantity + quantity
        #updates the quantity in the purchaseitem table as well
        database.update_database("UPDATE PurchaseItem SET Quantity = ? WHERE ItemID = ? AND PurchaseID = ?",[self.find_object(itemID).quantity, itemID, self.purchaseID])
        #recalculates the total with more items now in the order
        self.calculate_total()

    #used to calculate the total cost of the order
    def calculate_total(self):
        #initially sets it to 0 as there is no items in the order
        self.totalcost = 0
        #for each item in the list, finds the price and multiplies it by the quantity before adding that to the total cost
        for item in self.items:
            self.totalcost = self.totalcost + (item.price * item.quantity)
        #updates the total cost in the purchaseorder table for that order
        database.update_database("UPDATE PurchaseOrder SET TotalCost = ? WHERE PurchaseID = ?",[self.totalcost, self.purchaseID])

    #used to keep track of when a purchase has been delivered
    def deliver_purchase(self):
        #only carries out the function if the order hasn't already been registered as delivered
        if self.delivered == "no":
            #repeats for every item in the order
            for i in self.items:
                try:
                    #pulls the quantity from the stock table for the current item
                    item = database.query_database("SELECT QtyInStock FROM Stock WHERE ItemID = ?", [i.itemID])
                    #if the list length is more than 0 it means that the store currently has some of that item in stock
                    if len(item) > 0:
                        #adds the quantity in the order to the quantity in stock
                        newquantity = item[0][0] + i.quantity
                        #updates the stock table to have the new quantity
                        database.update_database("UPDATE Stock SET QtyInStock = ? WHERE ItemID = ?", [newquantity, i.itemID])
                    #if the list length is 0, the store doesn't have any of that item in stock
                    else:
                        #sets the quantity to the quantity in the order
                        newquantity = i.quantity
                        #makes a new record in the stock table with the item from the order
                        database.insert_database("INSERT INTO Stock (ItemID, SellPrice, QtyInStock) VALUES (?,?,?)", [i.itemID, i.price, i.quantity])
                except:
                    print("Something went wrong whilst trying to update the database. Please contact technical support.")
            #updates the delivered status of the order in the database to be yes so it can't be delievered again
            database.update_database("UPDATE PurchaseOrder SET Delivered = ? WHERE PurchaseID = ?", ["yes", self.purchaseID])
            #also updates the delievered status in the order object
            self.delivered = "yes"
        else:
            #prints this message telling the user they've already registered this order as delivered
            input("This order has already been registered as delivered")
            return False