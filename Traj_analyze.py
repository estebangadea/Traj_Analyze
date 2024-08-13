#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :menu.py
#description     :This program displays an interactive menu on CLI
#author          :
#date            :
#version         :0.1
#usage           :python menu.py
#notes           :
#python_version  :2.7.6  
#=======================================================================
 
# Import the modules needed to run the script.
import sys, getopt
import os
import math
from dumpnatoms import Dump_Fix
#from clusteranalisys import Cluster_Analisys
from clusteranalisys_small import Cluster_Analisys
from currentfunction import Current
from collections import Counter
from depositmap import Deposit_map
from gridplot import Grid_Plot
from grid_linear import Grid_Linear
from zaxis_density import Zaxis_Dens
from density_level import Dens_Level
 
# Main definition - constants
menu_actions  = {}
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():
    os.system('clear')
    
    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Normalize number of atoms")
    print("2. Extract the size of the bigest cluster")
    print("3. Extract number of reacctions along trajectory")
    print("4. Extract density grid from trajectory")
    print("5. Plot a map of reaction sites")
    print("6. Plot and export a 1D axial density profile")
    print("7. Plot a 2D density profile and export a level curve")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
 
    return
 
# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return
 
# Menu 1
def menu1():
    TRAJNAME = input(" trajectory:  ")
    Dump_Fix(TRAJNAME)
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return
 
 
# Menu 2
def menu2():
    TRAJNAME = input(" trajectory:  ")
    cluster_type = int(input(" Type to clusterize:  "))
    cutoff = float(input(" Cutoff:  "))
    tstep = int(input (" Timestep:  "))
    Cluster_Analisys(TRAJNAME, cluster_type, cutoff, tstep)
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return
    
# Menu 3
def menu3():
	OUTNAME = input(" Out File:  ")
	tstep = input(" Timestep:  ")
	Current(OUTNAME, tstep)
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)
	return
	
 # Menu 4
def menu4():
	TRAJNAME = input(" trajectory:  ")
	atom_type = int(input(" Type:  "))
	rgrid = int(input(" Radial Grid (RMax/2):  "))
	zgrid = int(input(" Z axis Grid (ZMax/2):  "))
	tstep = int(input(" Timestep:  "))
	sampletime = input(" Time interval, start-end in ns (default = all):  ")
	if sampletime=="all":
		#Grid_Linear(TRAJNAME, atom_type, rgrid, zgrid, tstep, "all")
		Grid_Plot(TRAJNAME, atom_type, rgrid, zgrid, tstep, "all")
	else:
		#Grid_Linear(TRAJNAME, atom_type, rgrid, zgrid, tstep, sampletime)
		Grid_Plot(TRAJNAME, atom_type, rgrid, zgrid, tstep, sampletime)
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)
	return
	
# Menu 5
def menu5():
	OUTNAME = input(" Out File:  ")
	boxlength = int(input(" Box Size:  "))
	tstep = int(input(" Timestep:  "))
	sampletime = input(" Time interval, start-end in ns (default = all):  ")
	if sampletime=="":
		Deposit_map(OUTNAME, boxlength, tstep, "all")
	else:
		Deposit_map(OUTNAME, boxlength, tstep, sampletime)
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)
	return
 
# Menu 6
def menu6():
	GRIDNAME = input(" Grid File:  ")
	Zaxis_Dens(GRIDNAME)
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)
	return
	
# Menu 7
def menu7():
	GRIDNAME = input(" Grid File:  ")
	LEVEL = input(" Level value:  ")
	if LEVEL=="":
		Dens_Level(GRIDNAME)
	else:
		Dens_Level(GRIDNAME, float(LEVEL))
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)
	return

# Back to main menu
def back():
    menu_actions['main_menu']()
 
# Exit program
def exit():
    sys.exit()
 
# =======================
#    MENUS DEFINITIONS
# =======================
 
# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '6': menu6,
    '7': menu7,
    '9': back,
    '0': exit,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program

if __name__ == "__main__":
    # Launch main menu
    main_menu()

