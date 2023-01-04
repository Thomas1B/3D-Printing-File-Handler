'''
This program is for handling 3D printing files such as .STL, .gcode and .x3g.

Depending on the user inputs, it will show completed files, files need to be sliced,
moves files and much more!

'''



# ****************************************** # ******************************************


import numpy as np
import os
from os import listdir
from os.path import isdir, exists
from myPyPackages.myPrints import color_txt, print_color, warning, clear_screen, quit_program
from myPyPackages.mySystem import get_dirs, get_files, delete, move_file
from myPyPackages.myData import check_matches


# ****************************************** # ******************************************

setup_limit = False  # if program set up has been complete
quit_check = False  # do double check when quitting the program.

folders_name = np.array(['Completed', 'Models', "Need to Slice", "Ready to Print"])

# ****************************************** # ******************************************


def get_allModels():
    '''Function get all models'''
    return get_files(folders_name[1])


def get_Completed():
    '''
    Function to get files that need to be completed.
    '''
    return get_files(folders_name[0])


def get_Need():
    '''Function to get files in the need to finish folder'''
    return get_files(folders_name[2])


def get_NeedSlicing():
    '''Function to get files that need to be sliced'''
    _, needs_Sliced, _ = check_matches(ALL_MODELS, get_Completed())
    _, needs_Sliced, _ = check_matches(needs_Sliced, get_Ready())
    return needs_Sliced


def get_Ready():
    '''
    Function to get files that are ready to print
    '''
    files = get_files(f'{folders_name[3]}')
    return files


def detect_missingfolders():
    '''
    Function to determine the nessecary folders exist.
        If there are any missing folders, they are returned as an array.
    '''
    tmp = [f for f in listdir(main_path) if isdir(
        f)]  # getting folders in main directory
    ids = np.isin(folders_name, tmp)
    missing = folders_name[np.where(ids == False)]
    return missing


def ready_and_completed():
    '''
    Function to return files that in the ready AND completed folder.

        Returns: array of files, False if there are none. 
    '''
    ready = get_Ready()
    completed = get_Completed()

    gcode_r = []
    x3g_r = []
    gcode_c = []
    x3g_c = []

    for file in ready:
        tmp = file+'.gcode'
        if tmp in ready:
            gcode_r.append(tmp)
        tmp = file+'.x3g'
        if tmp in ready:
            x3g_r.append(tmp)

    for file in completed:
        tmp = file+'.gcode'
        if tmp in completed:
            gcode_c.append(tmp)
        tmp = file+'.x3g'
        if tmp in completed:
            x3g_c.append(tmp)

    both1, _, _ = check_matches(gcode_r, get_Completed())
    both2, _, _ = check_matches(x3g_r, get_Completed())

    if len(both1):
        warning()
        txt = 'The following files are in both the "Ready" and "Completed" folders:'
        print(txt)
        print(color_txt(both1, color='red', attrs=['bold']), '\n')
        user = input(
            'Would you like to delete the files from the "ready" folder? (y/n): ')
        if user == 'y':
            for file in folders_name[3]:
                delete(file)
    elif len(both2):
        warning()
        txt = 'The following files are in both the "Ready" and "Completed" folders:'
        print(txt)
        print(color_txt(both2, color='red', attrs=['bold']), '\n')
        user = input(
            'Would you like to delete the files from the "ready" folder? (y/n): ')
        if user == 'y':
            for file in folders_name[3]:
                delete(file)


def need_and_completed():
    '''
    Function to return files that in the need AND completed folder.

        Returns: array of files, False if there are none. 
    '''

    need = get_Need()
    completed = get_Completed()

    gcode_n = []
    x3g_n = []
    gcode_c = []
    x3g_c = []

    for file in need:
        tmp = file+'.gcode'
        if tmp in need:
            gcode_n.append(tmp)
        tmp = file+'.x3g'
        if tmp in need:
            x3g_n.append(tmp)

    for file in completed:
        tmp = file+'.gcode'
        if tmp in ready:
            gcode_c.append(tmp)
        tmp = file+'.x3g'
        if tmp in ready:
            x3g_c.append(tmp)

    both1, _, _ = check_matches(gcode_n, get_Completed())
    both2, _, _ = check_matches(x3g_n, get_Completed())

    if len(both1):
        warning()
        txt = 'The following files are in both the "Need" and "Completed" folders:'
        print(txt)
        print(color_txt(both1, color='red', attrs=['bold']), '\n')
        user = input(
            'Would you like to delete the files from the "ready" folder? (y/n): ')
        if user == 'y':
            for file in folders_name[2]:
                delete(file)
    elif len(both2):
        warning()
        txt = 'The following files are in both the "Need" and "Completed" folders:'
        print(txt)
        print(color_txt(both2, color='red', attrs=['bold']), '\n')
        user = input(
            'Would you like to delete the files from the "ready" folder? (y/n): ')
        if user == 'y':
            for file in folders_name[2]:
                delete(file)


def checkDuplicates(msg=False):
    '''Function to check for duplicates in complete and need, complete and ready'''

    completed = get_Completed()
    ready = get_Ready()
    need = get_Need()

    gcode_r, x3g_r, gcode_c, x3g_c, gcode_n, x3g_n = [], [], [], [], [], []

    for file in ready:
        tmp = file+'.gcode'
        if tmp in ready:
            gcode_r.append(tmp)
        tmp = file+'.x3g'
        if tmp in ready:
            x3g_r.append(tmp)

    for file in completed:
        tmp = file+'.gcode'
        if tmp in completed:
            gcode_c.append(tmp)
        tmp = file+'.x3g'
        if tmp in completed:
            x3g_c.append(tmp)

    for file in need:
        tmp = file+'.gcode'
        if tmp in need:
            gcode_n.append(tmp)
        tmp = file+'.x3g'
        if tmp in need:
            x3g_n.append(tmp)

    need1, _, _ = check_matches(gcode_n, gcode_c)
    need2, _, _ = check_matches(x3g_n, x3g_c)

    ready1, _, _ = check_matches(gcode_r, gcode_c)
    ready2, _, _ = check_matches(x3g_r, x3g_c)

    txt = 'The following files are in both the "{}" and "Completed" Folders:'
    deleteMSG = 'Would you like to delete the files from the "{}" folder? (y/n): '

    need_txt = "Need to Finish"
    ready_txt = "Ready to Print"
    if len(need1):
        warning()
        print(txt.format(need_txt))
        print(color_txt(need1, color='red', highlight='yellow'), '\n')
        user = input(deleteMSG.format(need_txt))
        if user == 'y':
            for file in need1:
                delete(file)
    elif msg == True:
        print(f'No gcode duplicates between "{need_txt}" and "Completed".')

    if len(need2):
        warning()
        print(txt.format(need_txt))
        print(color_txt(need2, color='red', highlight='yellow'), '\n')
        user = input(deleteMSG.format(need_txt))
        if user == 'y':
            for file in need2:
                delete(file)
    elif msg == True:
        print(f'No x3g duplicates between "{need_txt}" and "Completed".')

    if len(ready1):
        warning()
        print(txt.format(ready_txt))
        print(color_txt(ready1, color='red', highlight='yellow'), '\n')
        user = input(deleteMSG.format(need_txt))
        if user == 'y':
            for file in ready1:
                delete(file)
    elif msg == True:
        print(f'No gcode duplicates between "{ready_txt}" and "Completed".')

    if len(ready2):
        warning()
        print(txt.format(ready_txt))
        print(color_txt(ready2, color='red', highlight='yellow'), '\n')
        user = input(deleteMSG.format(ready_txt))
        if user == 'y':
            for file in ready2:
                delete(file)
    elif msg == True:
        print(f'No x3g duplicates between "{ready_txt}" and "Completed".\n')


# ****************************************** # ******************************************


def show_Completed():
    '''
    Function to show completed files.
    '''
    models = get_allModels()
    complete, _, _ = check_matches(models, get_Completed())
    print_color(f"Completed, {len(complete)}/{len(models)}:", color='green')
    print(complete, '\n')


def show_NeedFinish():
    '''
    Function to show what files are in the "Need to slice" folder.
    '''
    print_color("Need to Slice:", color='red')
    need = get_Need()
    print(need, '\n')


def show_NeedsSliced():
    '''Function to show files that need to be sliced'''
    print_color("The following files need to be sliced:",
                color='red', attrs=['bold'])
    needs_sliced = get_NeedSlicing()
    print(needs_sliced, '\n')


def show_Ready():
    '''Function to show what files are ready to print'''
    print_color("Ready to print:", color='yellow')
    files = get_Ready()
    print(files, '\n')


def show_models():
    '''
    Function to print all models
    '''
    models = get_allModels()
    print_color(f"3D Models, Count = {len(models)}:", color='cyan')
    print(models, '\n')


def show_commands():
    '''
    Function to print possible commands
    '''
    txt = '   q - Quit Program, c - Clear Screen, s - Show Commands.\n' \
        '\n' \
        '   1 - Show all Info.             4 - Show files that need to be finished.\n' \
        '   2 - Check for duplices.        5 - Show files are ready to print\n' \
        '   3 - Show completed files.\n' \
        '\n' \
        '   m1 - Move files from "Models" folder to "Need to Slice" folder.\n'\
        '   m2 - Move files from "Ready to Print" folder to "Completed" folder.\n'
    # '   m3 - Move files from "Ready to Print" folder to "Completed" folder.\n'

    print_color("Possible Commands:", color='blue', attrs=['bold'])
    print(txt, '\n')


def show_all():
    '''
    Function to show info about files.
    '''
    show_models()
    show_Completed()
    show_Ready()
    show_NeedFinish()
    show_NeedsSliced()


# ****************************************** # ******************************************

while (True):
    '''
    Main Function to run program
    '''

    if not setup_limit:  # setup stuff
        clear_screen()
        print_color(
            '******** Welcome to the 3D File Handler ********\n',
            color='green',
            attrs=['bold']
        )
        txt = f'{color_txt("Note", color="cyan")}: This program requries folders with the following names:\n'\
              f'      {", ".join(folders_name)}.\n'
        print(txt)

        while (True):
            txt = "Enter the filepath of your desired folder (blank - for current directory): "
            main_path = input(txt)
            if len(main_path) == 0:
                main_path = os.getcwd()
                print(main_path, '\n')
                break
            elif not exists(main_path):
                print()
                warning()
                print(f"Filpath {color_txt(main_path, color='cyan')} doesn't exists...")
                print("Try again.\n")

        missing = detect_missingfolders()
        if len(missing):
            print("The following folders are missing:")
            print(missing)
            user = input("\nWould you like to create them? (y/n): ")
            if user == 'y':
                print()
                for dir in missing:
                    os.makedirs(dir)
                    if exists(dir):
                        print_color(
                            f'"{dir}" was created succesfully.', color='green')
                    else:
                        print_color(
                            f'\nCreating "{dir}" was  unsuccesfully.', color='green')
                print()

        ALL_MODELS = get_files(folders_name[1])
        COMPLETED = get_files(folders_name[0])
        NEED = get_files(folders_name[2])
        READY = get_files(folders_name[3])
        checkDuplicates()
        show_commands()
        setup_limit = True

    else:
        user = input("Command: ")
        # clear_screen() is not put here since it would clear the screen when any key is pressed.
        match user:
            case 'q':
                quit_program(quit_check)
                break
            case 'c':
                clear_screen()
            case 's':
                clear_screen()
                show_commands()
            case '1':
                clear_screen()
                show_all()
                show_commands()
            case '2':
                clear_screen()
                checkDuplicates(True)
                show_commands()
            case '3':
                clear_screen()
                show_Completed()
                show_commands()
            case '4':
                clear_screen()
                show_NeedsSliced()
                show_commands()
            case '5':
                clear_screen()
                show_Ready()
                show_commands()
            case 'm1':
                need = get_NeedSlicing()
                if len(need) == 0:
                    print("\nThere are 0 files to move!\n")
                else:
                    txt = f'\nThere are {len(need)} files. Would you like to move them all? (y/n): '
                    user = input(txt)
                    if user == 'y':
                        for file in need:
                            result = move_file(
                                folders_name[1], folders_name[2], file+'.STL', check_move=False, remove=False)
                        show_commands()
                    else:
                        print(f'\nType "{color_txt("quit", color="blue", attrs=["bold"])}" to leave the loop.')
                        for i, file in enumerate(need):
                            print(f'\nCount {i+1}/{len(need)}:')
                            result = move_file(
                                folders_name[1], folders_name[2], file+'.STL', remove=False)
                            if result == 'quit':
                                break
                        print()
                    show_commands()
            case 'm2':
                ready = get_Ready()
                if len(ready) == 0:
                    print('\nThere are 0 files to move!\n')
                else:
                    txt = f'\nThere are {len(ready)*2} files. Would you like to move them all? (y/n): '
                    user = input(txt)
                    if user == 'n' and len(ready) == 1:
                        clear_screen()
                        show_commands()
                    elif user == 'y':
                        print()
                        for file in ready:
                            result = move_file(
                                folders_name[3], folders_name[0], file+'.gcode', check_move=False)
                            result = move_file(
                                folders_name[3], folders_name[0], file+'.x3g', check_move=False)
                        print()
                        show_commands()
                    else:
                        print(f'\nType "{color_txt("quit", color="blue", attrs=["bold"])}" to leave the loop.')
                        i = 0
                        for file in ready:
                            print(f'\nCount {i+1}/{len(ready)*2}:')
                            result = move_file(
                                folders_name[3], folders_name[0], file+'.gcode')
                            if result == 'quit':
                                break
                            print(f'\nCount {i+2}/{len(ready)*2}:')
                            result = move_file(
                                folders_name[3], folders_name[0], file+'.x3g')
                            if result == 'quit':
                                break
                            i += 2
                        print()
                        show_commands()

            case _:
                clear_screen()
                show_commands()
