#Responsible for executing the correct module

import os
import importlib
import sys
import ConfigInteraction

Modules = None

def LoadModules():
    global Modules

    Modules = ConfigInteraction.GetModuleList()

    ModuleList = ""

    for method, module in Modules.items():
        if (module not in ModuleList): #Does not print duplicates
            ModuleList += module + ", "

    if (ModuleList == ""):
        ModuleList = "None"
        return(ModuleList)
    else:
        return(ModuleList[:-2])

def CallFunction(function_name, arguments):
    sys.path.insert(0, os.path.join(os.path.dirname(os.getcwd()), "Modules"))
    for method, module in Modules.items():
        if (method == function_name):
            #Import both the Module and the method
            moduleImport = importlib.import_module(module)
            methodImport = getattr(moduleImport, method)

            if (callable(methodImport)):
                #Differenciate between method calls with arguments, and ones without
                if (arguments == None):
                    return(methodImport())
                else:
                    return(methodImport(arguments))
            else:
                print("Failed to access method " + method + " of module " + module)
                return("Error, could not access module")
            
    return("No such module exists")