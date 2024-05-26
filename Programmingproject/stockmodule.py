import pypyodbc
import database
import hashlib
import itemmodule

#used to create a new item in stock
def create_stock(id, price, amount, lowamount):  
    #looks to see if an item already exists in stock with that itemID
    IDgood = database.query_database("SELECT * FROM Stock WHERE ItemID = ?", [id])
    itemgood = database.query_database("SELECT * FROM Items WHERE ItemID = ?", [id])
    #if anything is found, returns False
    if len(IDgood) != 0:
        return False
    
    if len(itemgood) == 0:
        return False
    #creates a new entry in the stock table using the variables passed into the function
    try:
        database.insert_database("INSERT INTO Stock (ItemID, SellPrice, QtyInStock, MinStockLvl) VALUES (?, ?, ?, ?)", [id, price, amount, lowamount])
        return True
    except Exception as e:
        print("Error updating database.  Contact Technical Support\n System Message: %s " % str(e) )
        return None

#used to list all items in stock
def list_stock():
    #creates an empty array
    allstock = []
    #selects all stockIDs
    stocks = database.query_database("SELECT StockID FROM Stock")
    #for every stockID pulled, creates an object using the StockID and appends it to the allstock array
    for i in range(len(stocks)):
        nextstock = stock(stocks[i][0])
        allstock.append(nextstock)
    return allstock


#used to check if any items in stock need reordering
def reorder():
    #selects the IDs, current quantity, and minimum stock level for every item where the current level is less than or equal to the minimum
    stockitems = database.query_database("SELECT StockID, ItemID, QtyInStock, MinStockLvl FROM Stock WHERE QtyInStock <= MinStockLvl")
    #runs if stockitems has found any items
    if len(stockitems) != 0:
        for i in range(len(stockitems)):
            #double checks that the item has a low quantity
            if stockitems[0][2] <= stockitems[0][3]:
                #creates an object out of each ID and tells the user what they're low on and what supplier sells it
                item = itemmodule.item(stockitems[0][1])
                print("You are low on ID: ", item.itemID, "name: ", item.name, "\nWhich is avaliable to buy from: ", item.supplier)
                #checks to see if the reorder found is already saved in the Reorder table
                alreadydatabase = database.query_database("SELECT ReorderID FROM Reorder WHERE StockID = ?", [stockitems[0][0]])
                #if it isn't, the reorder gets saved to the database
                if len(alreadydatabase) == 0:
                    database.insert_database("INSERT INTO Reorder (StockID, Reordered) VALUES (?, ?)", [stockitems[0][0], "no"])
        return True
    else:
        return False

def find_reorder(id):
    found = database.query_database("SELECT * FROM Reorder WHERE StockID = ?", [id])
    if len(found) != 0:
        return True
    else:
        return False

#used to make objects for individual items in stock
class stock(object):
    #used to instantiate the object with only the StockID provided
    def __init__(self, id):
        #searches for any other attributes in the stock table that match the stockID provided to fill in the rest of the attributes
        stockfound = database.query_database("SELECT ItemID, SellPrice, QtyInStock FROM Stock WHERE StockID = ?", [id])
        self.stockID = id
        #instantiates an item object and stores it in self.item
        self.item = itemmodule.item(stockfound[0][0])
        self.price = stockfound[0][1]
        self.quantity = stockfound[0][2]

    #used so that objects are printed as a list of their attributes rather than a meaningless object location
    def __str__(self):
        selflist = ("{},{},{},{}".format(self.stockID, self.item, self.price, self.quantity))
        return selflist

    #used to change the price of a stock item
    def change_price(self):
        new = input("What do you want the new price to be? ")
        #updates the stock table and the object with the new price
        database.update_database("UPDATE Stock SET SellPrice = ? WHERE StockID = ?",[new, self.stockID])
        self.price = new

    #used to change the quantity of a stock item
    def change_quantity(self):
        new = input("What do you want the new quantity to be? ")
        #updates the stock table and the object with the new quantity
        database.update_database("UPDATE Stock SET QtyInStock = ? WHERE StockID = ?",[new, self.stockID])
        self.desc = new

    #used to confirm that a reorder has been made
    def confirm_reorder(self):
        try:
            #deletes the reorder from the reorder table
            database.delete_database("DELETE FROM Reorder WHERE StockID = ?", [self.stockID])
            return True
        except:
            print("Something went wrong whilst trying to update the database. Please contact technical support.")
            return False
        