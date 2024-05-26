#imports all of the necessary modules
from os import system
import usermodule
import stockmodule
import purchaseordermodule
import saleorder
import itemmodule
import customermodule

def main_menu():
    #used so only registered users can use the system
    validoption = False
    print("----------------------------------")
    print("Welcome to the Store Sales System")
    print("----------------------------------")
    print("\nMenu Options")
    print("\n1. Sign Up")
    print("2. Login")
    print("3. Exit")
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            return "sign_up_screen"
        elif option == "2":
            validoption = True
            return "login_screen"
        elif option == "3":
            validoption = True
            print("\n--------")
            print("Goodbye")
            print("--------")
            return "EXIT"
        else:
            print("\nPlease choose a valid option")

def sign_up_screen():
    #clears the screen at the beginning of a new function
    system("cls")
    print("---------------")
    print("Sign Up Screen")
    print("---------------")
    successful = False
    while successful == False:
        username = input("\nWhat would you like your username to be: ")
        password = input("\nWhat would you like your password to be: ")
        #accessing the user module to create a new user
        auth = usermodule.create_user(username, password)
        if auth == True:
            system("cls")
            print("\nSuccessfully Signed Up\n")
            successful = True
            #returning the name of the next module in a string so that the user will be redirected there
            return "menu_access_screen"
        else:
            print("\nThis Username Was Already Taken. Please Try Again.\n")


def login_screen():
    system("cls")
    print("-------------")
    print("Login Screen")
    print("-------------")
    successful = False
    while successful == False:
        username = input("\nWhat is your Username: ")
        password = input("\nWhat is your Password: ")
        #accessing the login function within the user module
        match = usermodule.login(username, password)
        if match == True:
            system("cls")
            print("\nSuccessfully Logged In\n")
            successful = True
            return "menu_access_screen"
        else:
            print("\nThis Username Or Password Is Incorrect. Please Try Again.\n")


def menu_access_screen():
    system("cls")
    print("-------------------")
    print("Menu Access Screen")
    print("-------------------")
    print("\nMenu Options")
    print("\n1. User Menu")
    print("2. Stock Menu")
    print("3. Sales Menu")
    print("4. Customer Menu")
    print("5. Log Out and Exit")
    validoption = False
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            system('cls')
            return "user_menu"
        elif option == "2":
            validoption = True
            system("cls")
            return "stock_menu"
        elif option == "3":
            validoption = True
            system("cls")
            return "sales_menu"
        elif option == "4":
            validoption = True
            system("cls")
            return "customer_menu"
        elif option == "5":
            validoption = True
            system("cls")
            print("\n--------")
            print("Goodbye")
            print("--------")            
            return "EXIT"
        else:
            print("\nPlease Enter a Valid Value")
    return


#==================================================================================

def user_menu():
    system("cls")
    validoption = False
    print("-----------------------")
    print("User Interactions Menu")
    print("-----------------------")
    print("\nMenu Options")
    print("\n1. Edit a User")
    print("2. Delete a User")
    print("3. Find A User")
    print("4. List All Users")
    print("5. Return to Main Menu")
    print("6. Exit")
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            system("cls")
            return "edit_user_screen"
        elif option == "2":
            validoption = True
            system("cls")
            return "delete_user_screen"
        elif option == "3":
            validoption = True
            system("cls")
            return "find_user_screen"
        elif option == "4":
            validoption = True
            system("cls")
            return "list_users_screen"
        elif option == "5":
            validoption = True
            system("cls")
            print("\nReturning you to the main menu\n")
            return "menu_access_screen"
        elif option == "6":
            validoption = True
            system("cls")
            print("\n--------")
            print("Goodbye")
            print("--------")            
            return "EXIT"
        else:
            print("\nPlease enter a valid option\n")


def edit_user_screen():
    system("cls")
    print("------------")
    print("Edit A User")
    print("------------")
    #checking what the role of the current user is in order to decide if they are allowed to access this function
    currentrole = usermodule.current_user_role()
    #only admins are allowed to delete users
    if currentrole == "Admin":
        found = False
        while found == False:
            try:
                user = int(input("\nWhich user would you like to edit the details of? Enter their UserID: "))
                #creating a user object in the users class in the user module
                userobject = usermodule.user(user)
                found = True
            except:
                input("Please enter a valid UserID")
        goodchoice = False
        while goodchoice == False:
            #prints the current values of all the possible assets the admin may want to change
            print("\n1. Change Username (", userobject.username, ")")
            print("2. Change Role (", userobject.role, ")")
            print("3. Change Email (", userobject.email, ")")
            print("4. Return to Main Menu")
            choice = input("What would you like to change: ")
            if choice == "1":
                newuser = input("What would you like the new username to be: ")
                #changing the assets of the object
                userobject.change_username(newuser)
                goodchoice = True
            elif choice == "2":
                print("\nStaff\nManager\nAdmin")
                newrole = input("What would you like the new role to be: ")
                userobject.change_role(newrole)
                goodchoice = True
            elif choice == "3":
                newemail  = input("What would you like the new email address to be: ")
                userobject.change_email(newemail)
                goodchoice = True
            elif choice == "4":
                input("Okay. Press Enter to return to the User Menu")
                return "user_menu"
                goodchoice = True
            else:
                input("Please enter a valid option")
        
        input("Change successful. Press Enter to return to the User Menu")
        return "user_menu"
    else:
        input("You are not allowed to make these changes. Please press Enter to be returned to the User Menu")
        return "user_menu"

def delete_user_screen():
    system("cls")
    print("--------------")
    print("Delete A User")
    print("--------------")
    #checking if the current role of the user is admin
    currentrole = usermodule.current_user_role()
    if currentrole == "Admin":
        correct = False
        while correct == False:
            finduser = input("What is the username of the user you would like to delete: ")
            #checks if that is definitely the user wanting to be deleted
            confirmation = input("The username you put was: {}\n Is this correct (Y/N): ".format(finduser)).lower()
            if confirmation == "y":
                #uses the user module to delete the appropriate user's record from the database
                delete = usermodule.delete_user(finduser)
                if delete == None:
                    print("There is no user with that name in the database. Please check you entered the name correctly and try again.")
                else:
                    input("User Deleted. Press Enter to return to the User Menu.")
                    correct = True
                    return "user_menu"
    else:
        input("You are not allowed to carry out this function. Please choose another")
        return "user_menu"

def find_user_screen():
    system("cls")
    print("-----------")
    print("Find  User")
    print("-----------")
    rightuser = False
    while rightuser == False:    
        finduser = input("\nWhich user do you want to find?\nInput their username: ")
        #finds and retrieves the user that has that username
        userfound = usermodule.find_user(finduser)
        if userfound == False:
            print("\nThere are no records with that usernme. Please make sure you have entered the username correctly and try again.\n")
        else:
            print("\nHere is the user we found with that username:")
            print(userfound)
            correct = input("\nIs this the user you were looking for? (Y/N) ").lower()
            if correct == "y":
                input("\nOkay. Press Enter when you are done to return to the User Menu")
                rightuser = True
                return "user_menu"
            else:
                input("\nPlease make sure you have entered the username correctly and try again.\n")

def list_users_screen():
    system("cls")
    print("---------------")
    print("List All Users")
    print("---------------")

    #lists all the users in the User module
    allusers = usermodule.list_users()
    for i in allusers:
        print(i)
        print("")

    input("\n\nPress Enter when you are done to return to the User Menu")
    return "user_menu"



#=========================================================================


def stock_menu():
    system("cls")
    validoption = False
    print("-----------")
    print("Stock Menu")
    print("-----------")
    print("\nMenu Options")
    print("\n1. See Stock")
    print("2. Add a Item to Stock")
    print("3. Find an Item in Stock")
    print("4. Make a Purchase")
    print("5. Edit A Purchase")
    print("6. Confirm A Delivery")
    print("7. Check For Reorders")
    print("8. Confirm A Reorder")
    print("9. Return to Main Menu")
    print("10. Exit")
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            system("cls")
            return "see_stock_screen"
        elif option == "2":
            validoption = True
            system("cls")
            return "add_stock_screen"
        elif option == "3":
            validoption = True
            system("cls")
            return "find_stock_screen"
        elif option == "4":
            validoption = True
            system("cls")
            return "make_purchase_screen"
        elif option == "5":
            validoption = True
            system("cls")
            return "edit_purchase_screen"
        elif option == "6":
            validoption = True
            system("cls")
            return "confirm_delivery_screen"
        elif option == "7":
            validoption = True
            system("cls")
            return "reorder_screen"
        elif option == "8":
            validoption = True
            system("cls")
            return "reorder_confirmation_screen"
        elif option == "9":
            validoption = True
            system("cls")
            print("\nReturning you to the main menu\n")
            return "menu_access_screen"
        elif option == "10":
            validoption = True
            system("cls")
            print("\n--------")
            print("Goodbye")
            print("--------")            
            return "EXIT"
        else:
            print("\nPlease enter a valid option\n")


def see_stock_screen():
    system("cls")
    print("---------------")
    print("List All Stock")
    print("---------------")

    #lists all of the stock in the Stock table
    allstock = stockmodule.list_stock()
    for i in allstock:
        print("")
        print(i)
        print("")

    input("\n\nPress Enter when you are done to return to the main menu")
    return "menu_access_screen"

def add_stock_screen():
    print("-----------------")
    print("Add Stock Screen")
    print("-----------------")
    validid = False
    while validid == False:
        try:
            id = int(input("\nInput the item ID: "))
            goodid = itemmodule.find_item(id)
            if goodid == True:
                validid = True
            else:
                print("\nPlease enter a valid ID")
        except:
            print("\nPlease enter a valid ID")
    number = False
    while number == False:
        try:
            price = float(input("\nPlease enter a unit price for the item in pounds with 2 decimal places. You do not need to add the pound sign: "))
            number = True
        except:
            print("\nPlease enter a valid value")
    while number == True:    
        try:
            amount = int(input("\nHow many of this item do you have in stock: "))
            number = False
        except:
            print("\nPlease enter a valid value")
    while number == False:
        try:
            lowamount = int(input("\nHow many of this item do you want to have left when the reorder is placed: "))
            number = True
        except:
            print("\nPlease enter a valid value")
    adding = stockmodule.create_stock(id, price, amount, lowamount)
    if adding == True:
        input("Stock item successfully created. Please press Enter to be returned to the Stock Menu")
        return "stock_menu"
    elif adding == False:
        print("\nThis item is already in the stock database, please try a different ID or go to the edit function if you wish to edit a preexisting item.")
        input("Please press Enter to be returned to the Stock Menu")
        return "stock_menu"
    else:
        input("There was an issue creating the item. Please press Enter to be returned to the Stock Menu")
        return "stock_menu"


def find_stock_screen():
    print("-------------")
    print("Find an Item")
    print("-------------")
    number = False
    while number == False:
        try:
            finditem = int(input("Which item do you want to find?\nInput the ID: "))
            result = itemmodule.find_item(finditem)
            number = True
        except:
            print("\nPlease enter a valid ID")
    if result == False:
        input("\nSorry, we could not find an item with that ID. Please press Enter to be returned to the stock menu")
        return "stock_menu"
    else:
        item = itemmodule.item(finditem)
        print("\nHere is the item we found:\n", item)
        input("Press Enter when you re ready to be returned to the stock module")
        return "stock_menu"

def make_purchase_screen():
    system("cls")
    print("----------------")
    print("Make A purchase")
    print("----------------\n")
    #checks if role is either admin or manager
    role = usermodule.current_user_role()
    if role == "Admin" or role == "Manager":
        end = False
        while end == False: 
            #creates purchase using the purchase order module
            orderID = purchaseordermodule.create_purchase_order()
            order = purchaseordermodule.purchaseorder(orderID)   
            print("\nThe Supplier ID you gave is: ", order.supplier.SupplierID)
            print("Please only add items from this supplier in this order. If you wish to order items from another supplier, please create a new purchase order.")
            #finds all items that are sold by that supplier
            allitems = itemmodule.list_items(order.supplier.SupplierID)
            if len(allitems) != 0:
                print("\nThese are the items avaliable to buy from that supplier:")
                for i in allitems:
                    if i.supplier.SupplierID == order.supplier.SupplierID:
                        #prints just the ID and the name of the item
                        print("\n", [i.itemID, i.name])
                accepted = False
                while accepted == False:
                    try:
                        add = int(input("What is the Item ID of the item you would like to add:"))
                        amount = int(input("How many of this item would you like to purchase: "))
                        accepted = True
                    except:
                        input("\nPlease enter a valid ID")
                #adds item to the order
                intoorder = order.add_item(add, amount)
                if intoorder == True:
                    print("Item added to the order")
                else:
                    print("There was an issue adding that item to the order")
                finished = input("Would you like to add another item form that supplier to the order (Y/N): ").lower()
                if finished == "n":
                    end = True
                    print("Okay. Returning you to the Stock Menu")
                    return "stock_menu"
                else:
                    system("cls")
                    print("Okay. Add another item.")
            else:
                system("cls")
                print("This Supplier does not currently have any items avaliable for purchase. Please try another supplier")
    else:
        input("You are not allowed to carry out this function. Press Enter to be returned to the stock menu")
        return "stock_menu"



def edit_purchase_screen():
    system("cls")
    print("------------------")
    print("Edit Order Screen")
    print("------------------")
    accepted = False
    goodID = False
    while goodID == False:
        while accepted == False:
            try:
                orderID = int(input("\nWhat is the PurchaseID of the order you would like to edit: "))
                accepted = True
            except:
                input("\nPlease enter a valid ID")
        #finds the order based on the order ID
        found = purchaseordermodule.find_order(orderID)
        if found == True:
            ordertoedit = purchaseordermodule.purchaseorder(orderID)
            goodID = True
        else:
            print("\nThere is no order with that ID. Please try another ID")
            accepted = False
    if len(ordertoedit.items) != 0:
        print("\nHere is a list of the items that are already in that order:")
        for i in ordertoedit.items:
            print(i)
    else:
        print("This Order is currently empty.")
    print("\n1. Add An Item")
    print("2. Delete An Item")
    print("3. Edit A Quantity")
    print("4. Return to Stock Menu")
    option = input("\nWhich option would you like to choose: ")
    if option == "1":
        valid = False
        while valid == False:
            try:
                item = int(input("\nWhat is the itemID of the item you would like to add:"))
                quantity = int(input("How many of this item would you like to add"))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        #adds items to the order
        added = ordertoedit.add_item(item, quantity)
        if added == True:
            system("cls")
            input("Item Added to the order. Press Enter to return to the Edit Purchase screen")
            return "edit_purchase_screen"
        else:
            input("That Item could not be found. Press Enter to return to the Edit Purchase Screen.")
            return "edit_purchase_screen"
    elif option == "2":
        valid = False
        while valid == False:
            try:
                item = int(input("What is the ItemID of the item you would like to delete from the order: "))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        #removes items from the order
        deleted = ordertoedit.remove_item(item)
        if deleted == True:
            system("cls")
            input("Item has been removed from the order. Press Enter to return to the Edit Purchase screen.")
            return "edit_purchase_screen"
        else:
            system("cls")
            input("This Item was not in the purchase. Please press Enter to be returned to the Edit Purchase screen.")
            return "edit_purchase_screen"
    elif option == "3":
        valid = False
        while valid == False:
            try:
                itemid = int(input("What is the ItemID of the item you would like to edit: "))
                newquantity = int(input("\nWhat would you like the new quantity to be: "))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        #edits the quantity of that specific item in the order
        edit = ordertoedit.edit_quantity(itemid, newquantity)
        if edit == True:
            system("cls")
            input("\nQuantity successfully edited. Press Enter to return to the Edit Purchase screen.")
            return "edit_purchase_screen"
        else:
            system("cls")
            input("There was an error when trying to update that item. Please press Enter to be returned to the Edit Purchase screen")
            return "edit_purchase_screen"
    elif option == "4":
        input("Okay. Please press Enter to be returned to the Stock Menu")
        return "stock_menu"
    else:
        system("cls")
        input("Please enter a valid value")
        return "edit_purchase_screen"


def confirm_delivery_screen():
    system("cls")
    print("------------------------")
    print("Confirm Delivery Screen")
    print("------------------------")
    print("\nPlease only use this function when all of an order has been delivered")
    option = input("Has all of this order been delivered? (Y/N) ").lower()
    if option == "y":
        valid = False
        while valid == False:
            try:
                delivered = int(input("\nWhat is the PurchaseID of the item that has been delivered: "))
                real = purchaseordermodule.find_order(delivered)
                if real == True:
                    valid = True
                else:
                    print("\nThere was no Purchase found with that ID. Please try again.")
            except:
                input("\nPlease enter a valid ID")
        #finds the order that has been delivered and marks it as such
        order = purchaseordermodule.purchaseorder(delivered)
        orderdelivered = order.deliver_purchase()
        if orderdelivered != False:
            input("Purchase successfully delivered. Press Enter to return to the Stock Menu")
            return "stock_menu"
        else:
            input("\nReturning you to the stock menu. Press Enter when you are ready")
            return "stock_menu"
    else:
        print("Please wait until all of the order has been delivered before using this function.")
        input("Please press Enter to be returned to the stock menu")
        return "stock_menu"

def reorder_screen():
    system("cls")
    print("------------------------------------")
    print("Checking Stock Levels. Please Wait.")
    print("------------------------------------\n")
    #checks to see if there are any items in stock that need reordering
    reordered = stockmodule.reorder()
    if reordered == True:
        input("\nPress Enter to be returned to the Stock Menu")
        return "stock_menu"
    else:
        print("\nThere are no items in stock that are needing to be reordered")
        input("Press Enter to be returned to the Stock Menu")
        return "stock_menu"

def reorder_confirmation_screen():
    system("cls")
    print("---------------------")
    print("Reorder Confirmation")
    print("---------------------")
    print("\nPlease use this function when you have placed a order for more stock of this item")
    choice = input("\nHave you placed an order for the item? (Y/N) ").lower()
    if choice == "y":
        item = int(input("\nWhat is the stock ID of the item you have reordered: "))
        #makes a stock object for the item being reordered and then then confirms that it has been reordered 
        exists = stockmodule.find_reorder(item)
        if exists == True:
            reorder = stockmodule.stock(item)
            completed = reorder.confirm_reorder()
            if completed == True:
                input("Reorder Registered. Press Enter to be returned to the Stock Menu")
                return "stock_menu"
            else:
                input("Something went wrong. Press Enter to be returned to the Stock Menu")
                return "stock_menu"
        else:
            input("\nThat item is not on the list of items needing to be reordered. Press Enter to return to the Stock Menu")
            return "stock_menu"
    else:
        input("\nOkay. Please press Enter to be returned to the stock menu.")
        return "stock_menu"

#=========================================================================================

def sales_menu():
    system("cls")
    validoption = False
    print("-----------")
    print("Sales Menu")
    print("-----------")
    print("\nMenu Options")
    print("\n1. See Sales")
    print("2. Register A Sale")
    print("3. Edit A Sale")
    print("4. Complete A Sale")
    print("5. Return to Main Menu")
    print("6. Exit")
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            system("cls")
            return "see_sales_screen"
        elif option == "2":
            validoption = True
            system("cls")
            return "register_sale_screen"
        elif option == "3":
            validoption = True
            system("cls")
            return "edit_sale_screen"
        elif option == "4":
            validoption = True
            system("cls")
            return "complete_sale_screen"
        elif option == "5":
            validoption = True
            system("cls")
            print("\nReturning you to the main menu\n")
            return "menu_access_screen"
        elif option == "6":
            validoption = True
            system("cls")
            print("\n--------")
            print("Goodbye")
            print("--------")            
            return "EXIT"
        else:
            print("\nPlease enter a valid option\n")

def see_sales_screen():
    system("cls")
    print("---------------")
    print("List All Sales")
    print("---------------")
    #shows what order the attributes will be printed in
    print("\nItemID; CustomerID; Customer's First Name, Surname, and Email; Customer's Postal Address; Date Sold; Items Sold; Total Cost\n")
    allsales = saleorder.list_sales()
    for i in allsales:
        print("")
        print(i)
        print("")

    input("\n\nPress Enter when you are done to return to the sales menu")
    return "sales_menu"

def register_sale_screen():
    system("cls")
    print("----------------")
    print("Register A Sale")
    print("----------------\n")
    end = False
    validid = False
    exists = False
    while exists == False:
        while validid == False:
            try:
                customerID = int(input("\nInput the ID of the customer: "))
                validid = True
            except:
                print("\nPlease enter a valid ID")
        orderID = saleorder.create_sale_order(customerID)
        if orderID != False:
            exists = True
        else:
            validid = False
    order = saleorder.saleorder(orderID)
    while end == False:    
        print("\nThe Customer ID you gave is: ", order.customerID)
        print("Please only add items from this customer in this sale. If you wish to register a sale with another customer, please create a new sale.")
        allitems = stockmodule.list_stock()
        if allitems != 0:
            print("\nThese are the items avaliable to be sold from stock:")
            for i in allitems:
                if i.quantity != 0:
                    print("\n", [i.item.itemID, i.item.name, i.quantity])
            accepted = False
            while accepted == False:
                try:
                    add = int(input("What is the Item ID of the item you would like to add:"))
                    amount = int(input("How many of this item would you like to sell: "))
                    accepted = True
                except:
                    input("\nPlease enter a valid ID")
            intosale = order.add_item(add, amount)
            if intosale == True:
                print("Item added to the sale")
            else:
                print("There was an issue adding that item to the sale")
            finished = input("Would you like to add another item for that customer to the sale (Y/N): ").lower()
            if finished == "n":
                end = True
                print("Okay. Returning you to the Sales Menu")
                return "sales_menu"
            else:
                system("cls")
                print("Okay. Add another item.")
        else:
            system("cls")
            print("There are currently no items in stock to sell. Please add some items to the stock table and try again")

def edit_sale_screen():
    system("cls")
    print("------------------")
    print("Edit Sale Screen")
    print("------------------")
    accepted = False
    found = False
    while found == False:
        while accepted == False:
            try:
                saleID = int(input("\nWhat is the SaleID of the sale you would like to edit: "))
                accepted = True
            except:
                input("\nPlease enter a valid ID")
        exists = saleorder.find_sale(saleID)
        if exists == True:
            saletoedit = saleorder.saleorder(saleID)
            found = True
        else:
            print("\nThere is no sale under that ID. Please try again.")
            accepted = False
    if len(saletoedit.items) != 0:
        print("\nHere is a list of the items that are already in that sale:")
        for i in saletoedit.items:
            print("")
            print(i)
            print("")
    else:
        print("This sale is currently empty.")
    print("\n1. Add An Item")
    print("2. Delete An Item")
    print("3. Edit A Quantity")
    print("4. Return to Sale Menu")
    option = input("\nWhich option would you like to choose: ")
    if option == "1":
        valid = False
        while valid == False:
            try:
                item = int(input("\nWhat is the itemID of the item you would like to add:"))
                quantity = int(input("How many of this item would you like to add"))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        added = saletoedit.add_item(item, quantity)
        if added == True:
            system("cls")
            input("Item Added to the sale. Press Enter to return to the Edit Sale screen")
            return "edit_sale_screen"
        else:
            input("That Item could not be found. Press Enter to return to the Edit Sale screen.")
            return "edit_sale_screen"
    elif option == "2":
        valid = False
        while valid == False:
            try:
                item = int(input("What is the ItemID of the item you would like to delete from the sale: "))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        deleted = saletoedit.remove_item(item)
        if deleted == True:
            system("cls")
            input("Item has been removed from the sale. Press Enter to return to the Edit Sale screen.")
            return "edit_sale_screen"
        else:
            system("cls")
            input("This Item was not in the sale. Please press Enter to be returned to the Edit Sale screen.")
            return "edit_sale_screen"
    elif option == "3":
        valid = False
        while valid == False:
            try:
                itemid = int(input("What is the ItemID of the item you would like to edit: "))
                newquantity = int(input("\nWhat would you like the new quantity to be: "))
                valid = True
            except:
                input("\nPlease enter a valid ID")
        #edits the quantity of the item
        edit = saletoedit.edit_quantity(itemid, newquantity)
        if edit == True:
            system("cls")
            input("\nQuantity successfully edited. Press Enter to return to the Edit Sale screen.")
            return "edit_sale_screen"
        else:
            system("cls")
            input("There was an error when trying to update that item. Please press Enter to be returned to the Edit Sale screen")
            return "edit_sale_screen"
    elif option == "4":
        input("Okay. Please press Enter to be returned to the Sales Menu")
        return "sales_menu"
    else:
        system("cls")
        input("Please enter a valid value")
        return "edit_sale_screen"

def complete_sale_screen():
    system("cls")
    print("--------------------")
    print("Confirm Sale Screen")
    print("--------------------")
    print("\nPlease only use this function when a sale has been completed and the items are no longer within the shop")
    option = input("Has all of this sale been completed? (Y/N) ").lower()
    found = False
    if option == "y":
        while found == False:
            valid = False
            while valid == False:
                try:
                    delivered = int(input("What is the SaleID of the sale that has been completed: "))
                    valid = True
                except:
                    input("\nPlease enter a valid ID")
            exists = saleorder.find_sale(delivered)
            if exists == True:
                #creates a sale order object using the given ID
                sale = saleorder.saleorder(delivered)
                saledelivered = sale.complete_sale(delivered)
                #completes the sale in the sale order module
                if saledelivered != False:
                    input("\nSale successfully completed. Press Enter to be returned to the Sales Menu")
                    return "sales_menu"
                else:
                    input("\nOne or more of the items in this sale have a quantity greater than what is registered as in stock. Please check the order against the database and try again.")
                    input("Press Enter to be returned to the Sales Menu")
                    return "sales_menu"
            else:
                print("\nThere is no sale under that ID. Please try again.")
                valid = False
    else:
        print("Please wait until all of the order has been delivered before using this function.")
        input("Please press Enter to be returned to the sales menu")
        return "sales_menu"

#=========================================================================

def customer_menu():
    system("cls")
    validoption = False
    print("-----------------------")
    print("Customer Interactions Menu")
    print("-----------------------")
    print("\nMenu Options")
    print("\n1. Add A Customer")
    print("2. Edit A Customer")
    print("3. Delete A Customer")
    print("4. Find A Customer")
    print("5. List All Customers")
    print("6. Return to Main Menu")
    print("7. Exit")
    while validoption == False:
        option = input("\nWhich option would you like to choose? ")
        if option == "1":
            validoption = True
            system("cls")
            return "add_customer_screen"
        elif option == "2":
            validoption = True
            system("cls")
            return "edit_customer_screen"
        elif option == "3":
            validoption = True
            system("cls")
            return "delete_customer_screen"
        elif option == "4":
            validoption = True
            system("cls")
            return "find_customer_screen"
        elif option == "5":
            validoption = True
            system("cls")
            return "list_customers_screen"
        elif option == "6":
            validoption = True
            system("cls")
            print("\nReturning you to the main menu\n")
            return "menu_access_screen"
        elif option == "7":
            validoption = True
            system("cls")
            print("\n--------")
            print("Goodbye")
            print("--------")            
            return "EXIT"
        else:
            print("\nPlease enter a valid option\n")


def add_customer_screen():
    system("cls")
    print("----------------")
    print("Add User Screen")
    print("----------------")
    nameright = False
    while nameright == False:
        firstname = input("\nWhat is their first name: ")
        surname = input("What is their surname: ")
        choice = input("The name you put was: {} {}\nIs this correct (Y/N): ".format(firstname, surname)).lower()
        if choice == "y":
            nameright = True
        else:
            print("\nPlease make sure you enter the name correctly and try again.")
    #uses the customer module's find customer function with the two inputs provided
    exists = customermodule.find_customer(firstname, surname)
    if exists == False:
        email = input("What is the customer's email address: ")
        address = input("What is the customer's address: ")
        #creates a customer using the inputs given
        added = customermodule.create_customer(firstname, surname, email, address)
        if added == True:
            input("Customer successfully created. Please press Enter to be retuned to the Customer Menu.")
            return "customer_menu"
        else:
            input("There was an issue when adding that customer to the database. Press Enter to be returned to the Customer Menu")
            return "customer_menu"
    else:
        input("A customer with this name already exists in the database. Press Enter to be returned to the Customer Menu")
        return "customer_menu"

def edit_customer_screen():
    system("cls")
    print("------------")
    print("Edit A Customer")
    print("------------")
    #checking what the role of the current user is in order to decide if they are allowed to access this function
    currentrole = usermodule.current_user_role()
    #only admins are allowed to delete users
    if currentrole == "Admin":
        found = False
        while found == False:
            try:
                customer = int(input("\nWhich customer would you like to edit the details of? Enter their CustomerID: "))
                #creating a user object in the customer class in the user module
                customerobject = customermodule.customer(customer)
                found = True
            except:
                input("Please enter a valid CustomerID")
        goodchoice = False
        while goodchoice == False:
            #prints the current values of all the possible assets the admin may want to change
            print("\n1. Change First Name (", customerobject.FirstName, ")")
            print("2. Change Surname (", customerobject.Surname, ")")
            print("3. Change Email (", customerobject.Email, ")")
            print("4. Change Address (", customerobject.PostalAddress, ")")
            print("5. Return to Customer Menu")
            choice = input("What would you like to change: ")
            if choice == "1":
                new = input("What would you like the new First Name to be: ")
                #changing the assets of the object
                customerobject.change_first_name(new)
                goodchoice = True
            elif choice == "2":
                new = input("What would you like the new Surname to be: ")
                customerobject.change_surname(new)
                goodchoice = True
            elif choice == "3":
                new  = input("What would you like the new email address to be: ")
                customerobject.change_email(new)
                goodchoice = True
            elif choice == "4":
                new = input("What would you like the new address to be: ")
                customerobject.change_address(new)
                goodchoice = True
            elif choice == "5":
                input("Okay. Press Enter to return to the User Menu")
                return "customer_menu"
                goodchoice = True
            else:
                input("Please enter a valid option")
        
        input("Change successful. Press Enter to return to the Customer Menu")
        return "customer_menu"
    else:
        input("You are not allowed to make these changes. Please press Enter to be returned to the Customer Menu")
        return "customer_menu"

def delete_customer_screen():
    system("cls")
    print("--------------")
    print("Delete A Customer")
    print("--------------")
    #checking if the current role of the user is admin
    currentrole = usermodule.current_user_role()
    if currentrole == "Admin":
        correct = False
        while correct == False:
            findcustomer = input("Which customer do you want to Delete?\nInput their first name: ")
            findcustomer2 = input("and their surname: ")
            #checks if that is definitely the user wanting to be deleted
            confirmation = input("The name you put was: {}{}\n Is this correct (Y/N): ".format(findcustomer, findcustomer2)).lower()
            if confirmation == "y":
                found = customermodule.find_customer(findcustomer, findcustomer2)
                if found != False:
                    #uses the user module to delete the appropriate user's record from the database
                    delete = customermodule.delete_customer(findcustomer, findcustomer2)
                    if delete == None:
                        print("There is no customer with that name in the database. Please check you entered the name correctly and try again.")
                    else:
                        input("Customer Deleted. Press Enter to return to the Customer Menu.")
                        correct = True
                        return "customer_menu"
                else:
                    print("\nThere is no customer with that name. Please try again")
    else:
        input("You are not allowed to carry out this function. Please choose another")
        return "customer_menu"

def find_customer_screen():
    system("cls")
    print("-----------")
    print("Find A Customer")
    print("-----------")
    rightuser = False
    while rightuser == False:    
        findcustomer = input("Which Customer do you want to find?\nInput their first name: ")
        findcustomer2 = input("and their surname: ")
        #uses the find customer function in the customer module with the two inputs in order to find the right customer
        customerfound = customermodule.find_customer(findcustomer, findcustomer2)
        if customerfound == False:
            print("\nThere are no records with that name. Please make sure you have entered the name correctly and try again.\n")
        else:
            print("\nHere is the customer we found with that name:")
            print(customerfound)
            correct = input("\nIs this the customer you were looking for? (Y/N) ").lower()
            if correct == "y":
                input("\nOkay. Press Enter when you are done to return to the Customer Menu")
                rightuser = True
                return "customer_menu"
            else:
                input("\nPlease make sure you have entered the name correctly and try again.\n")

def list_customers_screen():
    system("cls")
    print("---------------")
    print("List All Customers")
    print("---------------")
    
    #calls to the customer module to list all of the customers
    allcustomers = customermodule.list_customers()
    for i in allcustomers:
        print(i)
        print("")

    input("\n\nPress Enter when you are done to return to the Customer Menu")
    return "customer_menu"