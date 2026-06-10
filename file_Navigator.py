import os
import math
import shutil
import sys
import time

# Constants needed for functions
clustor_size = 4096
size_found = False # Needed for the find file size function


# Dictionary for correct default root
root_dict = {
    "nt" : "C:\\",
    "posix" : "/"
}


# Class repersenting the user's operating system information
# operating_system will be 1 if windows and 0 if linux
class operating_system_class:
    def __init__ (self):
        self.path = root_dict[os.name]

    def set_path (self, newPath):
        self.path = newPath
    


# Dictionary for sizes utilized in find_File_size()
measure_dict = {
    "gb" : (1e9, "GB"),  # 1e9 Bytes = GB
    "mb" : (1e6, "MB"),  # 1e6 Bytes = MB
    "kb" : (1e3, "KB"),  # 1e3 Bytes = KB
    "bytes" : (1, "Bytes")
}


def find_size_recur(path, size, measurement):
    global size_found
    with os.scandir(path) as list:
        for f in list:
            try:
                if (f.is_file()):
                    disk_size = math.ceil(f.stat().st_size/clustor_size)*clustor_size
                    if (f.stat().st_size == 0):
                        disk_size = 0
                    if disk_size >= size:
                        byte_conversion, unit = measure_dict[measurement.casefold()]
                        print(f.name + " at location " + f.path + " : " + str(disk_size / byte_conversion) + " " + unit + "\n")
                        size_found = True
                elif (f.is_dir()):
                    find_size_recur(f.path, size, measurement)
            except:
                pass
                




# Prints all files above a certain file size given by the user 
def find_File_Size(operating_system):
    global size_found
    size_found = False # Setting variable to false just in case function has already been ran
    # Takes user input on what measurement they want file sizes to be returned in 
    while True : 
        measurement = input("Enter unit of size (GB, MB, KB, Bytes): ")
        try:
            byte_conversion, unit = measure_dict[measurement.casefold()]
            break
        except:
            print("Error: Enter a valid unit!")
    

    #Takes minimum file size to print out
    size = input("Enter the minimum file size: ")
    print()
    
    byteSize = int(size) * int(byte_conversion)      #Calculates user input into bytes to compare

    
    #Looks through all files and prints those that have greater file size
    find_size_recur(operating_system.path, byteSize, measurement)

    if not size_found:
        print("No file found above the size of " + str(size) + measurement)
        return

# Called by the find_Folder function to recursively go through every folder
# Method is used because it is faster and otherwise linux is too slow
def find_folder_recur(path, folder_with_name, folder_path_storage, folder_name):
    try: 
        with os.scandir(path) as d:
                    for f in d:
                        if f.is_dir():
                            if f.name == folder_name:
                                folder_with_name.append(f.name)
                                folder_path_storage.append(f.path)
                            find_folder_recur(f.path, folder_with_name, folder_path_storage, folder_name)
    except:
        pass


# Used as a part of other functions
# Finds a folder location based on what the user inputs
# If there are multiple with the same name asks user to pick which one they want
# Returns tuple with (FolderName, Path)
def find_Folder(operating_system):
    folderWithName = []
    folderPathStorage = []
    
    while True: 
        # Finds folders with the name and stores them in array folderWithName
        folderName = input("Please enter the folder's name: ")
        print()
        find_folder_recur(operating_system.path, folderWithName, folderPathStorage, folderName)
        # Returns correct folder with name and path
        if (len(folderWithName) == 1):
            return (folderWithName[0], folderPathStorage[0])
        
        # If more than one folder has user pick the correct one by looking at the path
        elif (len(folderWithName) > 1):  
            number = 1 
            for j in folderPathStorage:
                print(str(number) + " " + j)
                number = number + 1
            print("Found multiple folders with the same name and printed the paths out above.")

            while True:
                correctFolder = input("Pick which folder you want by entering the corresponding number (seen before each path): ")
                #Checks to see if input is a number
                try : 
                    correctFolder = int(correctFolder)
                except:
                    print("Invalid input.")
                    continue

                # Checks to see if input is in the valid range
                if (correctFolder > len(folderWithName) or correctFolder <= 0):
                    print("Invalid number.")
                    continue

                # Returns choosen folder
                correctFolder = correctFolder - 1
                return (folderWithName[correctFolder], folderPathStorage[correctFolder])
        else :
            print("Folder name entered doesn't exhist. Please try a different name.\n")
            find_Folder()
                



# Called by moveorswap_Contents 
# Swaps contents of folder1 and folder 2
def swap_folder_Contents(folder1, folder2):
    # Create a temporary folder to store contents of the first folder
    tempFolderPath = os.path.join(root_dict[os.name], "Temp")
    os.mkdir(tempFolderPath)

    # Move contents of first folder to temporary folder in folder 2
    moveFolderContents(folder1[1], tempFolderPath)

    # Move contents of second folder to first folder
    moveFolderContents(folder2[1], folder1[1])

    # Move contents from temporary folder to second folder
    moveFolderContents(tempFolderPath, folder2[1])

    # Delete temporary folder
    os.rmdir(tempFolderPath)
    print("Successfully swapped contents of " + folder1[0] + " and " + folder2[0] + ".")


# Move folder contents called by moveorswap_Contents() 
# Moves folder1 contents to folder2
def move_Contents(folder1, folder2):
    # Checks is user wants to delete the folder contents are moved from. 
    delete = False
    while True :
        delete = input("Would you like to delete the folder you are moving from (Y/N): ")

        if (delete.casefold() == "y") :
            delete = True
            break
        elif (delete.casefold() == "n"):
            delete = False
            break
        else :
            print("Please enter either Y or N.\n")

    # Calls function to move folder contents         
    moveFolderContents(folder1[1], folder2[1])

    # Deletes files if delete is true and print success message
    if (delete) :
        os.rmdir(folder1[1])
        print("Succesfully moved the contents of " + folder1[0] + " to " + folder2[0] + " and deleted " + folder1[0] + ".")
    else :
        print("Succesfully moved the contents of " + folder1[0] + " to " + folder2[0] + ".")



# Dictionary to remove redundent code for moveorswap_Contents function
moveswap_dict = {
    True : ("\nEnter first folder.", "\nEnter second folder.", swap_folder_Contents),
    False : ("\nChoose a folder to move contents of.", "\nEnter folder to move contents to.", move_Contents)
}


# Either swaps contents of folder or moves contents of one folder to another 
# moveSwap is false if move and true if swap 
# folder1 will be one to move contents from and folder2 will be the one to recieve
def moveorswap_Contents(operating_system) :
    #Checks to see if user wants to move or swap contents
    print("Do you want to move contents of folder to another or swap contents of two folders?")
    while True:
        user_Input = input("Please enter either move or swap: ")
        if user_Input.casefold() == "move" :
            moveSwap = False
            break
        if user_Input.casefold() == "swap" :
            moveSwap = True
            break
        print("Error: Please enter a valid input.\n")

    string_one, string_two, action = moveswap_dict[moveSwap]
    print(string_one)
    folder1 = find_Folder(operating_system)
    print(string_two)
    folder2 = find_Folder(operating_system)
    action(folder1, folder2)
    


# Moves files and folders in Path1 to Path2 
# Used in other functions in order to move contents from one folder to another
def moveFolderContents(Path1, Path2) :
    # Runs through folder being moved and changes location
    for root, dirs, files in os.walk(Path1) :
        # Runs through folders and changes location to other folder
        for d in dirs :
            try: 
                currentDir = os.path.join(root, d)
                os.rename(currentDir, os.path.join(Path2, d))

            # Error code
            except :
                print("Can't be moved by the system: " + currentDir + "\n")                
            
        # Runs through all files and changes location to other folder
        for f in files:
            currentFile = os.path.join(root, f)
            try:
                os.rename(currentFile, os.path.join(Path2, f))
                
            # Error code
            except :
                print("Can't be moved by the system: " + currentFile + "\n")
               
    



    
    

            

# Find a file or folder based on keyword
def find_Folder_Keyword(operating_system) :
    print("Enter a keyword to find a file or folder that contains the keyword in it's name: ")
    keyword = input()
    fileFound = False
    print("Do you want to delete any of these files: \n1: Don't delete any files.\n2: Delete only specific files (will be asked after each file is found).\n3: Delete all files found.")
    delete = input()
    print()
    
    for root, dirs, files in os.walk(operating_system.path) :
        try:
            # Look through all folders/directories
            for d in dirs :
                if (keyword.casefold() in d.casefold()):
                    print("Folder found: " + os.path.join(root, d) + "\n")
                    if (delete == "3" ):
                        shutil.rmtree(os.path.join(root, d))
                    elif (delete == "2"):
                        print("Do you want to delete this folder Y/N: ")
                        deleteComp = input()
                        if (deleteComp == "Y"):
                            shutil.rmtree(os.path.join(root, d))
                    fileFound = True
            # Look through all files
            for j in files :
                if (keyword.casefold() in j.casefold()):
                    print("File found: " + os.path.join(root, j) + "\n")
                    if (delete == "3" ):
                        os.rmdir(os.path.join(root, j))
                    elif (delete == "2"):
                        print("Do you want to delete this file Y/N: ")
                        deleteComp = input()
                        if (deleteComp == "Y"):
                            os.remove(os.path.join(root, j))
                    fileFound = True

        
        except:
            pass
    if (not fileFound):
                print("Was unable to find any folder/file with keyword " + keyword + ".")
                


def change_path(operating_system):
    print("\nEnter a new file path:")
    while (True):
        new_path = input()
        if (os.path.exists(new_path)):
            operating_system.set_path(new_path)
            print("Successfully changed the file path.")
            time.sleep(0.5)
            break
        else:
            print("Invalid file path. Please enter one that exhists:")



# Dictionary utilized for calling the correct function
main_dict = {
    1 : find_File_Size,
    2 : moveorswap_Contents,
    3 : find_Folder_Keyword,
    -1 : change_path
}


def main():

    #Allows user to configure the path used 
    print("Please enter the path of a folder that the program can opperate in (program won't access folders that come before the path entered): ")
    print("Enter a 0 to use default path which is C:\\ for windows and / for linux based systems.")
    print("Otherwise enter a path.")
    path = input()
    operating_system = operating_system_class()
    if (path != "0"):
        operating_system.set_path(path)

    # Check to make sure path given does exhist
    if (not (os.path.exists(operating_system.path))):
        print("Error: path doesn't exhist exiting program.")
        time.sleep(1)
        sys.exit(1)
    
    
    while (True):
        # User picks what function they want to call
        print("\nWhat would you like to do (type in number that corresponds with the options below): ")
        selection = input("1: Find files above a certain size.\n2: Move/Swap the contents of two folders.\n3: Find a file or folder based on a keyword entered.\n-1: Change the path the program can operate in.\n0: Exit the program\n")
        selection = int(selection)
        if (selection == 0):
            print("Exiting program.")
            break
        # Utilizing main_dict to call the correct function
        try:
            main_dict[selection](operating_system)
            time.sleep(1)
        # Invalid input user needs to try again.
        except KeyError:
            print("Invalid input. Please enter a valid number.\n")
            time.sleep(1)

                

if __name__ == "__main__":
    main()