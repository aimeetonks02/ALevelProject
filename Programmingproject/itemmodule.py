import pypyodbc
import database
import hashlib
import suppliermodule

def create_item(name, desc, price):
    try:
        #inserts the given values into the items table
        database.insert_database("INSERT INTO Items (ItemName, Description, UnitPrice) VALUES (?, ?, ?)", [name, desc, price])
        return True
    except Exception as e:
        #prints the exception if something fails
        print("Error updating database.  Contact Technical Support\n System Message: %s " % str(e) )
        return False


def find_item_by_name(item):
    try:
        #finds the itemID of the named item and makes it into an item object
        itemfound = database.query_database("SELECT ItemID FROM Items WHERE ItemName = ?", [item])
        found_item = item(itemfound[0][0])
        return found_item
    except:
        return False
    #returns either False or the item object

def find_item(id):
    found = database.query_database("SELECT * FROM Items WHERE ItemID = ?", [id])
    if len(found) == 0:
        return False
    else:
        return True

def delete_item():
    print("Delete an Item")
    finditem = input("Which item do you want to Delete?\nInput the name: ")
    itemfound = database.delete_database("DELETE FROM Items WHERE ItemName = ?",[finditem])
    print("Item Deleted")

def list_items(supplierID):
    allitems = []
    items = database.query_database("SELECT ItemID FROM Items WHERE SupplierID = ?", [supplierID])
    for i in range(len(items)):
        nextitem = item(items[i][0])
        allitems.append(nextitem)
    return allitems

class item(object):

    def __init__(self, id, quantity = 1):
        itemfound = database.query_database("SELECT SupplierID, ItemName, Description, UnitPrice FROM Items WHERE ItemID = ?", [id])
        self.itemID = id
        self.supplier = suppliermodule.supplier(itemfound[0][0])
        self.name = itemfound[0][1]
        self.desc = itemfound[0][2]
        self.price = itemfound[0][3]
        self.quantity = quantity

    def __str__(self):
        selflist = ("{},{},{},{},{},{}".format(self.itemID, self.supplier, self.name, self.desc, self.price, self.quantity))
        return selflist
