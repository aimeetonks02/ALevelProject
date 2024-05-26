#imports the module we are wanting to access
import menumodule

#assigns next menu to the name of the first menu (function) needing to be accessed
nextmenu = "main_menu"
currentuser = None

#runs the program until "EXIT" is returned from the menu module
while nextmenu != "EXIT":
    #brings up the next menu function based on what string is returned
    #the string that is returned from the menu module is the name of the next function needing to be accessed
    func = getattr(menumodule, nextmenu, None)
    if func:
        nextmenu = func()
