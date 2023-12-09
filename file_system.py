"""
File:    file_system.py
Author:  Shrijan Regmi
Date:    12/9/2022
E-mail:  sregmi@umbc.edu
Description:
  A simple Linux file system and shell simulator. Has the capabilities of the ls, pwd, mkdir, touch, cd, rm, and locate commands.
"""


"""
All 3 of my helper functions below
"""

SLASH = "/"
NO_INPUT = False
YES_INPUT = True
def check_input(user_input):
    #CHECK IF USER INPUT EXISTS, USED THROUGHOUT VARIOUS FUNCTIONS, RETURNS BOOLEAN OF WHETHER THE USER INPUT EXISTS OR NOT.
    if not user_input:
        return NO_INPUT
    else:
        return YES_INPUT


def move_up(cwd):
    #HELPER FUNCTION FOR cd(), RETURNS CWD AFTER MOVING UP ONE DIRECTORY
    if cwd == SLASH:
        print("The current directory cannot move up further.")
    else:
        cwd_parts = cwd.split("/")
        if len(cwd_parts) > 2:
            cwd = SLASH.join(cwd_parts[:-1])
        else:
            cwd = SLASH
    return cwd

def directory_exists(file_system, cwd, dir_name):
    #HELPER FUNCTION FOR cd() AND mkdir(), RETURNS TRUE IF THE DIRECTORY IS IN THE CWD
    return dir_name in file_system[cwd]


"""
All 3 of my helper functions above
"""


def pwd(cwd):


#PRESENT WORKING DIRECTORY
    if len(cwd) == 1: #IF IT IS THE HOME DIRECTORY, THERE IS NO NEED FOR THE "/" TO BE ADDED AFTER.
        return cwd

    else:
        return cwd[1:] + "/" #FORMATTING


def ls(file_system, cwd, user_input):
    if not check_input(user_input):
        contents = "\n     ".join(file_system[cwd])
    elif user_input[0][0] == SLASH:
        cwd = SLASH + cwd[:-1]
        contents = "\n     ".join(file_system[cwd])
    else:
        contents = "\n     ".join(file_system[cwd])

    print(f"{prompt}Contents for {cwd[1:]}/:")
    print(f"     {contents}\n     ...")


def mkdir(cwd, user_input):


    if check_input(user_input) == False: #IF USER DOES NOT SPECIFY DIRECTORY NAME, RETURN AN ERROR
        print("Invalid, no directory name specified.")
    elif user_input[0] == '..':
        print("INVALID DIRECTORY NAME.")
    else:
        dir_name = user_input[0]
        if directory_exists(file_system, cwd, dir_name): #CHECK FOR PRE-EXISTING DIRECTORY OF SAME NAME
            print(f"{dir_name} already exists.")
        else:
            file_system[cwd].append(dir_name)
            file_system[f"{cwd}/{dir_name}"] = [] #ADD TO DICTIONARY


'''vvv keeping this code here incase implementing the helper function and absolute paths breaks something vvv'''
# def cd(cwd, user_input): #CHANGE DIRECTORY


#     if (check_input(user_input) == False) or user_input[0] == SLASH: #IF USER ONLY TYPES CD, CHANGE THE DIRECTORY TO HOME
#         cwd = SLASH
#     else:
#         dir_name = user_input[0] #SEND USER TO THE DIRECTORY GIVEN
#         if dir_name == "..": #MOVE UP ONE DIRECTORY
#             cwd_parts = cwd.split("/") 

#             if len(cwd_parts) > 2:
#                 cwd = SLASH.join(cwd_parts[:-1])
                
#             else:
#                 cwd = SLASH

#         elif dir_name not in file_system[cwd]:
#             print(f"The directory {dir_name} does not exist.")
#         else:
#             cwd = f"{cwd}/{dir_name}"
#     return cwd #RETURNS CHANGED DIRECTORY :)
'''^^^keeping this code here incase implementing helper function and absolute paths breaks something^^^'''


def cd(cwd, user_input): #CHANGE DIRECTORY
    if not check_input(user_input) or user_input[0] == SLASH:
        cwd = SLASH
    else:
        dir_name = user_input[0]
        if dir_name == "..": #MOVE UP ONE DIRECTORY
            cwd = move_up(cwd)
        elif dir_name[0] == SLASH:
            if dir_name[-1] != SLASH:
                print("Invalid path. Did you forget a slash at the end?")
            else:
                cwd = dir_name
        elif not directory_exists(file_system, cwd, dir_name):
            print(f"The directory {dir_name} does not exist.")
        else:
            cwd = f"{cwd}/{dir_name}"

    return cwd #RETURNS CHANGED DIRECTORY :)

def touch(file_system, cwd, user_input):


    if check_input(user_input) == False: #MAKE SURE THERE IS A FILE NAME PROVIDED
        print("Invalid file name.")
    else:

        file_name = user_input[0]

        if file_name[0] == SLASH:
            path_parts = file_name.split("/")
            file_name = path_parts[-1]

            if file_name in file_system["/"]:
                print(f"The file {file_name} already exists.")
                return

            file_system["/"].append(file_name)

            #HANDLING ABSOLUTE PATHS, may return keyerror.

            current_dir = file_system["/"]

            for i in range(1, len(path_parts) - 1):

                dir_name = path_parts[i]

                if dir_name not in current_dir:
                    current_dir.append(dir_name)
                    file_system[f"{cwd}/{dir_name}"] = []

            if user_input[0][0] == SLASH:

                if user_input[0][-1] != SLASH:
                    print("Invalid path. Did you forget a slash at the end?")

                else:
                    print(current_dir)
                    current_dir = file_system[f"{cwd[1:]}/{dir_name}"]

            else:
                current_dir = file_system[f"{cwd}/{dir_name}/"]

        else:
            #RELATIVE PATHS
            path_parts = file_name.split("/")
            file_name = path_parts[-1]

            if file_name in file_system[cwd]:
                print(f"The file {file_name} already exists. ")
                return

            file_system[cwd].append(file_name)

            #HANDLE SUBDIRECTORIES
            current_dir = file_system[cwd]
            for i in range(1, len(path_parts) - 1):
                dir_name = path_parts[i]
                if dir_name not in current_dir:
                    current_dir.append(dir_name)
                    file_system[f"{cwd}/{dir_name}"] = []
                current_dir = file_system[f"{cwd}/{dir_name}"]


def locate(file_system, cwd, user_input):


    if check_input(user_input) == False:
        print("Invalid input.")

    else:
        #RECURSION (yay!)
        def search_directory(current_dir, file_name, path): #Is this technically a helper function? I wasnt sure so I didnt put it at the top. But I think its easier if its down here
            #sEARCH FOR FILES IN CURRENT DIRECTORY
            if file_name in current_dir:
                found_paths.append(path) #WHEN YOU FIND IT

            else:
                #RECURSIVE SEARCH, IF FILE ISNT FOUND IN THE ABOVE IF STATEMENT
                for subdir in current_dir:
                    search_directory(file_system[f"{path}/{subdir}"], file_name, f"{path}/{subdir}")

        file_name = user_input[0]
        found_paths = [] #just a list of paths that were found
        search_directory(file_system[cwd], file_name, cwd)

        if found_paths:
            print("A file with that name was found at the following paths:")
            for path in found_paths:
                print(f"     {path[1:]}")
        else:
            print("No file with that name was found")


def rm(file_system, cwd, user_input):


    if check_input(user_input) == False: #again, just checking for an actual input

        print("Invalid input. No file name provided.")

    else:

        #REMOVING IT
        if user_input[0] not in file_system[cwd]:
            print("That file isnt in this directory")
        else:
            file_system[cwd].remove(user_input[0])


if __name__ == '__main__':

    #LIST OF COMMANDS
    EXIT = "exit"
    PWD = "pwd"
    LS = "ls"
    CD = "cd"
    MKDIR = "mkdir"
    TOUCH = "touch"
    RM = "rm"
    LOCATE = "locate"

    file_system = {
        "/": []
    }

    #CURRENT WORKING DIRECTORY
    cwd = SLASH

    #just the thing that comes before each line
    prompt = "[user@linux]$ "

    run = True
    while run:

        command = input(f"{prompt}")
        command_parts = command.split(" ")

        if command_parts[0] == EXIT:
            run = False


        if command_parts[0] == PWD:
            print(pwd(cwd))


        if command_parts[0] == LS:
            user_input = command_parts[1:]
            ls(file_system, cwd, user_input)

        if command_parts[0] == CD:
            user_input = command_parts[1:]
            cwd = cd(cwd, user_input)


        if command_parts[0] == MKDIR:

            user_input = command_parts[1:]
            mkdir(cwd, user_input)


        if command_parts[0] == TOUCH:

            user_input = command_parts[1:]
            touch(file_system, cwd, user_input)

 
        if command_parts[0] == RM:

            user_input = command_parts[1:]
            rm(file_system, cwd, user_input)


        if command_parts[0] == LOCATE:

            user_input = command_parts[1:]
            locate(file_system, cwd, user_input)
