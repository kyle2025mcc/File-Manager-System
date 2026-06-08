import os
import math
import time
import shutil
import sys
# Constants needed for functions
byte_Conversion_MB = 1e6     # 1e6 Bytes = MB
byte_Conversion_GB = 1e9     # 1e9 Bytes = GB
byte_Conversion_KB = 1e3     # 1e3 Bytes = KB
moveSwap = False
clusterSize = 4096     #Windows cluster size is 4096 bytes 
pathExhists = True
#Allows user to configure the path used 
print("Please enter the path of a folder that the program can opperate in (program won't access folders that come before the path entered): ")
print("Enter a 0 to Use default path which is C:\\.")
print("Otherwise enter path.")
path = input()
if (path == "0"):
    path = "C:\\"
if (not (os.path.exists(path))):
    print("Error: path doesn't exhist exiting program.")
    time.sleep(1)
    sys.exit(1)
    






# Prints all files above a certain file size given by the user 
def find_File_Size():
    fileFound = False
    # Takes user input on what measurement they want file sizes to be returned in 
    while True : 
        measurement = input("Enter unit of size (GB, MB, KB, Bytes): ")
        byte_Conversion = 1
        unit = " Bytes"
        if measurement == "GB" :
            byte_Conversion = byte_Conversion_GB
            unit = "GB"
            break
        elif measurement == "MB" :
            byte_Conversion = byte_Conversion_MB
            unit = "MB"
            break
        elif measurement == "KB":
            byte_Conversion = byte_Conversion_KB
            unit = "KB"
            break
        elif measurement == "Bytes" :
            break
        else :
            "Enter a valid unit."
    

    #Takes minimum file size to print out
    size = input("Enter the minimum file size: ")
    print()
    size = int(size)
    byte_Conversion = int(byte_Conversion)
    byteSize = size * byte_Conversion      #Calculates user input into bytes to compare

    #Looks through all files and prints those that have greater file size
    for root, dirs, files in os.walk(path):
        for i in files:
            try:
                currentFile = root + "\\" + i
                fileSize = os.path.getsize(currentFile)
                diskSize = math.ceil(fileSize/clusterSize)*clusterSize    #Estimates Disk size (isn't entirely accurate) 
                if (fileSize == 0):
                    diskSize = 0 
                if diskSize >= byteSize:
                    print(i + " at location " +currentFile + " : " + str(math.ceil(diskSize / byte_Conversion)) + unit)
                    fileFound = True
                    print()
            except FileNotFoundError:
                i = 1
                
            except OSError:
                i = 1
            
    if (not fileFound):
                print("No file found above the size of " + str(size) + measurement)

# Used as a part of other functions
# Finds a folder location based on what the user inputs
# If there are multiple with the same name asks user to pick which one they want
# Returns tuple with (FolderName, Path)
def find_Folder():
    folderWithName = []
    folderPathStorage = []
    folderPath = ""
    finalFolder = ()
    while True: 
        # Finds folders with the name and stores them in array folderWithName
        folderName = input("Please enter the folder's name: ")
        print()
        for root, dirs, files in os.walk(path):
            for i in dirs :
                if i == folderName :
                    folderWithName.append(i)
                    folderPath = root + "\\" + i
                    folderPathStorage.append(folderPath)
        # Returns correct folder
        if (len(folderWithName) == 1):
            finalFolder = (folderWithName[0], folderPathStorage[0])
            return finalFolder
        
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
                except ValueError:
                    print("Invalid input.")
                    continue
                # Checks to see if input is in the valid range
                if (correctFolder > len(folderWithName) or correctFolder <= 0):
                    print("Invalid number.")
                    continue
                # Returns choosen folder
                correctFolder = correctFolder - 1
                finalFolder = (folderWithName[correctFolder], folderPathStorage[correctFolder])
                return finalFolder
        else :
            print("Folder name entered doesn't exhist. Please try a different name.")
            print()
            find_Folder()
                


# Either swaps contents of folder or moves contents of one folder to another 
# moveSwap is false if move and true if swap 
# folder1 will be one to move contents from and folder2 will be the one to recieve
def moveorswap_Contents() :
    #Checks to see if user wants to move or swap contents
    print("Do you want to move contents of folder to another or swap contents of two folders?")
    while True:
        user_Input = input("Please enter either move or swap: ")
        if user_Input == "move" :
            moveSwap = False
            break
        if user_Input == "swap" :
            moveSwap = True
            break
        print("Please enter a valid input.")
        print()

    if not moveSwap:
        print()
        print("Choose a folder to move contents of.")
        folder1 = find_Folder()
        print()
        print("Enter folder to move contents to.")
        folder2 = find_Folder()
        move_Contents(folder1, folder2)
    else:
        print()
        print("Enter first folder.")
        folder1 = find_Folder()
        print()
        print("Enter second folder.")
        folder2 = find_Folder()
        swap_folder_Contents(folder1, folder2)
    
    # With the two folders utilize correct function to move or swap
    
    #Called by moveorswap_Contents() and moves files in one folder to another (folder 1 to folder 2 )


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
            except FileNotFoundError:
                print("Can't be moved by the system: " + currentDir)
                print()
                
            except OSError:

                print("Can't be moved by the system: " + currentDir)
                print()
            
        # Runs through all files and changes location to other folder
        for f in files:
            currentFile = os.path.join(root, f)
            try:
                os.rename(currentFile, os.path.join(Path2, f))
                
            # Error code
            except FileNotFoundError:
                print("Can't be moved by the system: " + currentFile)
                print()
              
            except OSError:

                print("Can't be moved by the system: " + currentFile)
                print()
    


# Move folder contents called by moveorswap_Contents() 
# Moves folder1 contents to folder2
def move_Contents(folder1, folder2):
    # Checks is user wants to delete the folder contents are moved from. 
    delete = False
    while True :
        delete = input("Would you like to delete the folder you are moving from (Y/N): ")
        print()

        if (delete == "Y") :
            delete = True
            break
        elif (delete == "N"):
            delete = False
            break
        else :
            print("Please enter either Y or N.")
            print()

    # Calls function to move folder contents         
    moveFolderContents(folder1[1], folder2[1])

    # Deletes files if delete is true and print success message
    if (delete) :
        os.rmdir(folder1[1])
        print("Succesfully moved the contents of " + folder1[0] + " to " + folder2[0] + " and deleted " + folder1[0] + ".")
    else :
        print("Succesfully moved the contents of " + folder1[0] + " to " + folder2[0] + ".")
    
    
# Called by moveorswap_Contents 
# Swaps contents of folder1 and folder 2
def swap_folder_Contents(folder1, folder2):
    # Create a temporary folder to store contents of the first folder
    tempFolderPath = os.path.join("C:\\", "Temp")
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

            

# Find a file or folder based on keyword
def find_Folder_Keyword() :
    print("Enter a keyword to find a file or folder that contains the keyword in it's name: ")
    keyword = input()
    fileFound = False
    error = False
    print("Do you want to delete any of these files: \n1: Don't delete any files.\n2: Delete only specific files (will be asked after each file is found).\n3: Delete all files found.")
    delete = input()
    
    for root, dirs, files in os.walk(path) :
        try:
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

        
        except FileNotFoundError:
            error = True
        except OSError:
            error = True
    if (not fileFound):
                print("Was unable to find any folder with keyword " + keyword + ".")
                


def main():

    #Allows user to configure the path used 
    # Main program that finds out what user wants to do 
    
    if (not pathExhists):
        return
    
    while (True):
        # User picks what function they want to call
        print("What would you like to do (type in number that corresponds with the options below): ")
        selection = input("1: Find files above a certain size.\n2: Move/Swap the contents of two folders.\n3: Find a file or folder based on a keyword entered.\n0: Exit the program\n")
        selection = int(selection)
        print()
        if (selection == 0):
            break
        elif (selection == 1):
            find_File_Size()
            time.sleep(2)
            print()
        elif (selection == 2):
            moveorswap_Contents()
            time.sleep(2)
            print()
        elif (selection == 3):
            find_Folder_Keyword()
            time.sleep(2)
            print()
        else:
            print("Invalid input. Please enter a valid number.\n")
                

main()
print("Exited program successfully.")