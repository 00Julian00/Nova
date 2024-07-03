import os
import json
import ast
import importlib.util

script_dir = os.path.dirname(os.path.realpath(__file__))
modulePath = os.path.join(os.path.dirname(script_dir), 'Modules')

def GetModuleFolders():
    entries = os.listdir(modulePath)

    directories = [entry for entry in entries if os.path.isdir(os.path.join(modulePath, entry))]

    return directories

def CheckModuleValidity(folder):
    EntryScript = ""
    EntryFunction = ""
    Name = ""
    Description = ""
    ParameterCount = 0
    
    if os.path.exists(os.path.join(modulePath, folder, "manifest.json")):
        with open(os.path.join(modulePath, folder, "manifest.json"), 'r') as file:
            manifest = json.load(file)
            try:
                EntryScript = manifest["EntryScript"]
                EntryFunction = manifest["EntryFunction"]
                Name = manifest["ModuleName"]
                Description = manifest["ModuleDescription"]
                ParameterCount = len(manifest["Parameters"])
            except:
                return False

            if (EntryScript == "" or EntryFunction == "" or Name == "" or Description == ""): #Check if the manifest contains baisc necessary info
                return False
            
        if os.path.exists(os.path.join(modulePath, folder, EntryScript)):
            with open(os.path.join(modulePath, folder, EntryScript), 'r') as file:
                tree = ast.parse(file.read())
        
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == EntryFunction:
                    # Count parameters
                    params = len(node.args.args)

                    if (ParameterCount == params): #Check if the entry function takes as many parameters as specified in the manifest
                        return True
    
        return False

def ScanModules():
    validModules = 0
    invalidModules = 0
    for folder in GetModuleFolders():
        if (CheckModuleValidity(folder)):
            validModules += 1
        else:
            invalidModules += 1
    
    return (validModules, invalidModules)

def GetModules():
    #Constructs a valid json object of all modules
    modules = []
    for folder in GetModuleFolders():
        if (CheckModuleValidity(folder)):
            with open(os.path.join(modulePath, folder, "manifest.json"), 'r') as file:
                manifest = json.load(file)
                data = {
                    "type": "function",
                    "function": {
                        "name": manifest["ModuleName"],
                        "description": manifest["ModuleDescription"],
                        "parameters": manifest["Parameters"]
                    }
                }
                modules.append(data)
    return modules

def CallFunction(name, parameters):
    for folder in GetModuleFolders():
        if (CheckModuleValidity(folder)):
            with open(os.path.join(modulePath, folder, "manifest.json"), 'r') as file:
                manifest = json.load(file)

                if (manifest["ModuleName"] == name):
                    script_path = os.path.join(modulePath, folder, manifest["EntryScript"])
                    function_name = manifest["EntryFunction"]
                    
                    # Load the module
                    spec = importlib.util.spec_from_file_location("module.name", script_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Get the function
                    func = getattr(module, function_name)

                    if (len(parameters) > len(manifest["Parameters"])):
                        return f"Too many parameters. Expected {len(manifest['Parameters'])}, got {len(parameters)}"

                    #Extract the parameters
                    ExtractedParams = []
                    for param_name, param_info in parameters.items():
                        # Check if the parameter is provided
                        if param_name in parameters:
                            # Get the provided value
                            value = parameters[param_name]

                            ExtractedParams.append(value)

                    while (len(ExtractedParams) < len(manifest["Parameters"])):
                        ExtractedParams.append(None)
                    
                    #Call the function
                    if isinstance(ExtractedParams, dict):
                        result = func(**ExtractedParams)
                    elif isinstance(ExtractedParams, (list, tuple)):
                        result = func(*ExtractedParams)
                    else:
                        result = func(ExtractedParams)

                    if result == None:
                        result = True
                    
                    return result
            
    return False