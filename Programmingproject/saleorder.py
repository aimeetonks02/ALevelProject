import pypyodbc
import database
import hashlib
import itemmodule
import customermodule
from datetime import date


#used to create new sales, only needs the customerID as an input
def create_sale_order(id):
    auth = False   
    #loops until the user confirms that the right customer has been found
    while auth == False:  
        #selects all info in the customer table that relates to the given customerID
        custgood = database.query_database("SELECT * FROM Customer WHERE CustomerID = ?", [id])
        #if anything is returned, the info is printed to the screen
        if len(custgood) != 0:
            print("\nThis is the customer we found with that ID:")
            print(custgood)
            right = input("Is this the customer you wanted?(Y/N) ").lower()
            if right == "y":
                auth = True
            else:
                print("Please check you have inputted the ID correctly and try again")
                return False
        else:
            print("There is no customer in the database with that ID. Please try again")
            return False
    #retrieves todays date
    dateorder = date.today()
    try:
        #inserts the new info into the saleorder table
        database.insert_database("INSERT INTO SaleOrder (CustomerID, DatePurch, Completed) VALUES (?,?,?)", [id, dateorder, "no"])
        input("Sale Created Successfully")
        ID = database.query_database("SELECT @@IDENTITY FROM SaleOrder")
        return ID[0][0]
    except Exception as e:
        print("Error updating database.  Contact Technical Support\n System Message: %s " % str(e) )
        return

#used to list all the sales in the saleorder table
def list_sales():
    #sets up a blank array
    allsales = []
    sales = database.query_database("SELECT SaleID FROM SaleOrder")
    #for each ID in sales, a saleorder object is made and appended to the allsales array
    for i in range(len(sales)):
        nextsale = saleorder(sales[i][0])
        allsales.append(nextsale)
    return allsales

def find_sale(id):
    salefound = database.query_database("SELECT * FROM SaleOrder WHERE SaleID = ?", [id])
    if len(salefound) != 0:
        return True
    else:
        return False

#used to make sale objects
class saleorder(object):
    #used to initialise all of the sale attributes using the saleID 
    def __init__(self, id):
        #searches for all the other attributes related to the ID in the saleorder table and fills out the rest of the funciton
        saleorderfound = database.query_database("SELECT CustomerID, DatePurch, TotalCost, Completed FROM SaleOrder WHERE SaleID = ?", [id])
        #finds any items in that sale
        itemslist = database.query_database("SELECT ItemID, Quantity FROM SaleItem Where SaleID = ?", [id])
        self.saleID = id
        #makes a customer object using the customer module and stores it as the customer attribute
        self.customerID = customermodule.customer(saleorderfound[0][0])
        self.datepurch = saleorderfound[0][1]
        self.totalcost = saleorderfound[0][2]
        self.items = []
        self.completed = saleorderfound[0][3]

        #for each ID in itemslist, an object is instantiated and appended to the self.items array
        for i in itemslist:
            item = itemmodule.item(i[0], i[1])
            self.items.append(item)

    #used to print objects as a list of their attributes and not a meaningless object location
    def __str__(self):
        selflist = ("{},{},{},{},{}".format(self.saleID, self.customerID, self.datepurch, self.items, self.totalcost))
        return selflist

    #used to remove items from the sale
    def remove_item(self, itemID):
        #looks to see if the provided itemID matches any of the ones in the sale
        delitem = self.find_object(itemID)
        #removes the item from the items array in the object if it does exist in the sale
        self.items.remove(delitem)
        #removes the item from the saleitem table
        database.delete_database("DELETE * FROM SaleItem WHERE ItemID = ? AND SaleID = ?",[itemID, self.saleID])
        #recalculates the new total cost for the sale
        self.calculate_total()

    #used to add new items to the sale
    def add_item(self, itemID, quantity = 1):
        try:
            #looks to see if the item is already registered in the sale
            exists = self.find_object(itemID)
            #if the item doesn't exist in the sale, it is made into an object using the ID and then appended to the items list and the database
            if exists == None:
                item = itemmodule.item(itemID, quantity)
                self.items.append(item)
                database.insert_database("INSERT INTO SaleItem (SaleID, ItemID, Quantity, UnitPurchPrice) VALUES (?, ?, ?, ?)", [self.saleID, itemID, quantity, item.price])
            else:
                #if the item is already in the sale, the quantity is incremented by the amount specified in the parameters
                self.increment_quantity(itemID, quantity)
            #recalculates the total cost of the sale
            self.calculate_total()
            return True
        except:
            return False

    #used to list all of the items in a sale
    def list_items(self):
        #prints every item in the items array to the screen
        for i in range(len(self.items)):
            print(self.items[i])
        #tells the user the list is empty if there is nothing in there
        if len(self.items) == 0:
            print("The list is empty")
        
        #prints the total cost of the sale
        print("The total cost is: ", self.totalcost)

    #used to find specific items in a sale
    def find_object(self, itemID):
        #checks the provided itemID to the itemID of every item in the sale
        for i in self.items:
            if i.itemID == itemID:
                #returns the item if any of the IDs match
                return i
        return None

    #used to edit the quantity of any item in the sale
    def edit_quantity(self, itemID, quantity):
        #finds the item in the sale and then sets the quantity to the new one
        self.find_object(itemID).quantity = quantity
        #updates the quantity in the saleitem table
        database.update_database("UPDATE SaleItem SET Quantity = ? WHERE ItemID = ? AND SaleID = ?",[quantity, itemID, self.saleID])
        #recalculates the total cost for the sale
        self.calculate_total()

    #used to increment quantities of items that are already in the sale
    def increment_quantity(self, itemID, quantity):
        #finds the current quntity and adds the new amount to it
        self.find_object(itemID).quantity = self.find_object(itemID).quantity + quantity
        #updates the quantity for the current item to the new quantity in the saleitem table
        database.update_database("UPDATE SaleItem SET Quantity = ? WHERE ItemID = ? AND SaleID = ?",[self.find_object(itemID).quantity, itemID, self.saleID])
        #recalculates the total cost for the sale
        self.calculate_total()

    #used to calculate the total cost for the sale
    def calculate_total(self):
        #sets it to 0 to begin with as there are no costs added yet
        self.totalcost = 0
        #for each item in the sale, multiply the cost by the quantity and add it to the total for the sale object
        for item in self.items:
            self.totalcost = self.totalcost + (item.price * item.quantity)
        #updates the total cost in the saleorder table
        database.update_database("UPDATE SaleOrder SET TotalCost = ? WHERE SaleID = ?",[self.totalcost, self.saleID])

    #used to say that a sale has been completed
    def complete_sale(self, id):
        #checks to see if the sale has already been completed and will only run if not
        if self.completed == "no":
            #runs for every item in the sale
            for i in self.items:
                try:
                    #brings back the quantity in stock for the current item and removes as many as were sold
                    item = database.query_database("SELECT QtyInStock FROM Stock WHERE ItemID = ?", [i.itemID])
                    if len(item) > 0:
                        newquantity = item[0][0] - i.quantity
                        #sets the item's new quantity in the stock table
                        database.update_database("UPDATE Stock SET QtyInStock = ? WHERE ItemID = ?", [newquantity, i.itemID])
                    else:
                        return False
                except:
                    print("Something went wrong whilst trying to update the database. Please contact technical support.")
            #sets completed to yes so that the sale can't be registered as completed more than once in both the object and the database
            database.update_database("UPDATE PurchaseOrder SET Completed = ? WHERE SaleID = ?", ["yes", id])
            self.delivered = True
        else:
            #prints this if the order has already been completed so the user can't complete it again
            input("This order has already been registered as delivered")
