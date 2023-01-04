import os
from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import colorama as cr
from colorama import init, Style, Fore, Back
import time
import keyboard

# Program Setup
init(autoreset = True) # print formatting stuff

setup_limit = False # if program set up has been complete

folders_name = np.array(['Completed', 'Models', "Need to finish", "ready to print"])


# ****************************************** # ******************************************


def get_filenames(folder_name):
    path = main_path + f'/{folder_name}'
    names = [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]
    return np.sort(list(set(names)))

def folder_contains(folder1, folder2):
    '''
    Function to check if files in folder1 are in folder2

    Returns: 2 arrays: files that are both, files in folder1 only
    '''
    ids = np.isin(folder1, folder2)
    both =  folder1[ids]
    folder1_only = folder1[np.where(ids == False)]
    return both, folder1_only

def get_Completed():
    both, not_completed = folder_contains(ALL_MODELS, COMPLETED)
    both, not_completed
    return both, not_completed

def get_Need():
    _, not_done = folder_contains(ALL_MODELS, COMPLETED)
    return not_done

def get_Ready():
    files = get_filenames(f'{folders_name[3]}')
    return files

def detect_folders():
    '''
    Function to determine the nessecary folders exist.

    if there are any missing folders, they returned:
            '''
    tmp = [f for f in listdir(main_path) if isdir(f)] # getting folders in main directory
    ids = np.isin(folders_name, tmp)
    missing = folders_name[np.where(ids == False)]

    if len(missing):
        return missing
    else:
        return False

def ready_and_completed():
    '''
    Function to return files that in the ready and completed folder.
    '''
    both, _ = folder_contains(READY, COMPLETED)
    if both:
        return both
    else:
        return False

# ****************************************** # ******************************************

def clear_screen():
    '''
    Function to clear screen.
    '''
    print(cr.ansi.clear_screen())

def quit_program():
    '''
    Function to terminate program.
    '''
    # clear_screen()
    print("Program Closing...")
    time.sleep(0.250)
    os._exit(os.X_OK)

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kargs):
    '''
    Utility function wrapping the regular `print()` function 
    but with colors and brightness
    '''
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kargs)

def show_commands():
    '''
    Function to print possible commands
    '''
    txt = '   esc - Quit Program.\n'\
          '   c   - Clear Screen.\n'\
          '   s   - Show Commands.\n'\
          '\n'\
          '   1 - Show all Info.\n'\
          '   2 - Show completed files.\n'\
          '   3 - Show files that need to be finished.\n'\
          '   4 - Show files that are ready to print.\n'
    print_with_color("Possible Commands:", color=Fore.BLUE, brightness=Style.BRIGHT)
    print(txt, '\n')

def show_Completed():
    print_with_color("Completed Files:", Fore.GREEN)
    files = get_filenames(f'{folders_name[0]}')
    print(files, '\n')

    both = ready_and_completed()
    if len(both):
        print_with_color("Warning", Fore.RED, Style.BRIGHT)
        txt = 'The following files are in both the'

def show_Need():
    _, not_done = folder_contains(ALL_MODELS, COMPLETED)
    print_with_color("Need to be Sliced:", Fore.RED)
    print(not_done, '\n')

def show_Ready():
    print_with_color("Ready to print:", Fore.YELLOW)
    files = get_filenames(f'{folders_name[3]}')
    print(files, '\n')

def show_all():
    '''
    Function to show info about files.
    '''
    show_Need()
    show_Ready()
    show_Completed()

# ****************************************** # ******************************************


# Making hotkeys for master commands.
keyboard.add_hotkey('esc', quit_program)
keyboard.add_hotkey('c', clear_screen)
keyboard.add_hotkey('s', show_commands)


while(True):
    '''
    Main Function to run program
    '''

    if not setup_limit: # setup stuff
        clear_screen()
        print_with_color('******** Welcome to the Program ********\n', Fore.GREEN, Style.BRIGHT)
        txt = 'Note: This program requries folders with the following names:\n'\
              '       {}.\n'.format(', '.join(folders_name))
        print_with_color(txt, Fore.WHITE)
        print_with_color('Otherwise the program will thrown an error.\n\n', Fore.WHITE)
        main_path = input("Enter the filepath of your desired folder (blank for current directory): ")
        if len(main_path) == 0:
            main_path = os.getcwd()

        missing = detect_folders()
        if missing:
            print_with_color("The following folders are missing:")
            print(missing)

        if not main_path:
            main_path = os.getcwd()
            print("     Using current working directory.\n")
        ALL_MODELS = get_filenames(folders_name[1])
        COMPLETED = get_filenames(folders_name[0])
        NEED = get_filenames(folders_name[2])
        READY = get_filenames(folders_name[3])        
        show_commands()
        setup_limit = True

    else:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            # clear_screen() is not put here since it would clear the screen when any key is pressed.
            if event.name == 's':
                clear_screen()
                show_commands()
            elif event.name == '1':
                clear_screen()
                show_all()
                show_commands()
            elif event.name == '2':
                clear_screen()
                show_Completed()
                show_commands()
            elif event.name == '3':
                clear_screen()
                show_Need()
                show_commands()
            elif event.name == '4':
                clear_screen()
                show_Ready()
                show_commands()


        




