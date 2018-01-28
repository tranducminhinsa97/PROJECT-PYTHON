#!/usr/bin/env python
# -----------------------------------------------
__author__ = "Robin Cochennec"
__version__ = "0.0.1"
# Release Notes ---------------------------------
'''
09/24/2017 : file creation, add constants
09/27/2017 : add inheritances, plus some more classes, deep thoughts around binary convertion
11/23/2017 : patched the axis/hand problem - added axis and functions to convert objects to binary sequence and vice versa
12/07/2017 : finished conversion functions
01/11/2018 : created conversion functions for watches
'''
# -----------------------------------------------

import random as rnd
import math as m


CHANCE_TO_MUTATE = 0.0002
# Gears module
GEARS_MODULE = 0.1
# Possible positions /!\ We're working with natural integers only bits : 11-11-4
X_RANGE = 2048 
Y_RANGE = 2048
Z_RANGE = 16
# Number of teeth - 10 bits
MIN_NB_TEETH = 3
MAX_NB_TEETH = 1000
# Objects code - 4 bits
GEAR_CODE = "0000"
ESCAPE_WHEEL_CODE = "0001"
BARREL_CODE = "0010"
BALANCE_WHEEL_CODE = "0011"
SPRING_CODE = "0100"
HAND_CODE = "0101"
FORK_CODE = "0110"
AXIS_CODE = "0111"
BUG_CODE = "1111"
# Axis rotation - 2 bits
PINNED = "00"
HORIZONTAL = "01"
VERTICAL = "10"

NO_CONNECTION = 0
XY_CONNECTION = 1
Z_CONNECTION = 2

CONNECTION_DISTANCE = 42
PIN_DISTANCE = 21


class Object:
    """
    An Object is a Father-Class used to give any piece of the watch a position in its relative space
    code = the binary version of the Object, containing all the needed informations for crossovers and mutations
    """
    def __init__(self):
        self.x_position = rnd.randint(0, X_RANGE)
        self.y_position = rnd.randint(0, Y_RANGE)
        self.z_position = rnd.randint(0, Z_RANGE)


class Gear(Object):
    """
    Definition of a Gear
    """
    # Creation
    def __init__(self):
        Object.__init__(self)
        self.nb_teeth = rnd.randint(MIN_NB_TEETH, MAX_NB_TEETH)
        self.rotates = False
        self.speed = 0  # In spin by minutes


class EscapeWheel(Gear):
    """
    The escape wheel basically has the same parameters than a gear
    """
    # Creation
    def __init__(self):
        Gear.__init__(self)


class Barrel(Gear):
    """
    Definition of a Barrel
    """
    # Creation
    def __init__(self):
        Gear.__init__(self)


class BalanceWheel(Object):
    """
    Definition of a Balance Wheel
    """
    # Creation
    def __init__(self):
        Object.__init__(self)


class Spring(Object):
    """
    Definition of a Mainspring
    """
    # Creation
    def __init__(self):
        Object.__init__(self)


class Hand(Object):
    """
    Definition of a Hand
    """
    # Creation
    def __init__(self):
        Object.__init__(self)
        self.speed = 0  # In spin by minutes


class Fork(Object):
    """
    Definition of an Fork
    """
    # Creation
    def __init__(self):
        Object.__init__(self)


class Axis(Object):
    """
    Definition of an Axis
    """
    def __init__(self):
        Object.__init__(self)
        self.rotation = rnd.choice([PINNED, HORIZONTAL, VERTICAL])
        self.length = int(rnd.randint(0, Z_RANGE)/2) * 2 + 1


def obj_to_bin(obj):
    # Input : a watch part
    # Output : the binary version of this part
    code = "2"
    if obj.__class__.__name__ == "Gear":
        code += GEAR_CODE
    elif obj.__class__.__name__ == "EscapeWheel":
        code += ESCAPE_WHEEL_CODE
    elif obj.__class__.__name__ == "Barrel":
        code += BARREL_CODE
    elif obj.__class__.__name__ == "BalanceWheel":
        code += BALANCE_WHEEL_CODE
    elif obj.__class__.__name__ == "Spring":
        code += SPRING_CODE
    elif obj.__class__.__name__ == "Hand":
        code += HAND_CODE
    elif obj.__class__.__name__ == "Fork": 
        code += FORK_CODE
    elif obj.__class__.__name__ == "Axis": 
        code += AXIS_CODE
    else:
        code += BUG_CODE

    code += (11-len(bin(obj.x_position)[2::]))*"0"+bin(obj.x_position)[2::]
    code += (11-len(bin(obj.y_position)[2::]))*"0"+bin(obj.y_position)[2::]
    code += (4-len(bin(obj.z_position)[2::]))*"0"+bin(obj.z_position)[2::]

    if isinstance(obj, Gear):
        code += (10-len(bin(obj.nb_teeth)[2::]))*"0"+bin(obj.nb_teeth)[2::]
    elif isinstance(obj, Axis):
        code += obj.rotation
        code += (4-len(bin(obj.length)[2::]))*"0"+bin(obj.length)[2::]
    return code


def bin_to_obj(string):
    # Input : a binary string
    # Output : the object version
    for i in range(4):
        if string[i] == "2":
            string = list(string)
            string[i] = str(rnd.randint(0, 1))
            string = ''.join(string)
    if string[0:4] == GEAR_CODE:
        obj = Gear()
    elif string[0:4] == ESCAPE_WHEEL_CODE:
        obj = EscapeWheel()
    elif string[0:4] == BARREL_CODE:
        obj = Barrel()
    elif string[0:4] == BALANCE_WHEEL_CODE:
        obj = BalanceWheel()
    elif string[0:4] == SPRING_CODE:
        obj = Spring()
    elif string[0:4] == HAND_CODE:
        obj = Hand()
    elif string[0:4] == FORK_CODE:
        obj = Fork()
    elif string[0:4] == AXIS_CODE:
        obj = Axis()
    else:
        obj = Object()

    for i in range(4, 30):
        if string[i] == "2":
            string = list(string)
            string[i] = str(rnd.randint(0, 1))
            string = ''.join(string)
    obj.x_position = int(string[4:15], 2)
    obj.y_position = int(string[15:26], 2)
    obj.z_position = int(string[26:30], 2)

    if isinstance(obj, Gear):
        if len(string) < 40:
            return Object()
        for i in range(30, 40):
            if string[i] == "2":
                string = list(string)
                string[i] = str(rnd.randint(0, 1))
                string = ''.join(string)
        obj.nb_teeth = int(string[30:40], 2)
    elif isinstance(obj, Axis):
        if len(string) < 36:
            return Object()
        for i in range(30, 36):
            if string[i] == "2":
                string = list(string)
                string[i] = str(rnd.randint(0, 1))
                string = ''.join(string)
        obj.rotation = string[30:32]
        obj.length = int(string[32:36], 2)

    return obj


def watch_to_bin(watch: tuple):
    string = ''
    for i in range(1, len(watch)):
        string += obj_to_bin(watch[i])
    return string


def bin_to_watch(string, number):
    watch = [number]
    for i in range(len(string)):
        if string[i] == "2" and len(string[i+1::]) >= 30:
            obj = bin_to_obj(string[i+1::])
            watch += [obj]
    return watch


classes = (Gear, EscapeWheel, Barrel, BalanceWheel, Spring, Hand, Fork, Axis)


def generate(nb_monsters, min_obj, max_obj):
    # Input : the number of watches wanted, plus the min and max number of parts in these watches
    # Output : a list of random watches respecting the inputs
    generation = [[] for _ in range(nb_monsters)]
    for i in range(nb_monsters):
        generation[i] = [i]
        for j in range(rnd.randint(min_obj, max_obj)):
            generation[i] += [rnd.choice(classes)()]
    return generation


def mate(watch1, watch2, number):
    # returns the baby of watch1 and watch2 as another watch. Ask for a number for the first element of the watch
    code = [watch_to_bin(watch1), watch_to_bin(watch2), '']
    segments = []
    for i in range(2):
        cut_map = []
        for j in range(len(code[i])):
            if code[i][j] == "2":
                cut_map += [j]
        for k in range(len(cut_map)-1):
            segments += [code[i][cut_map[k]:cut_map[k+1]]]
            if k == len(cut_map)-1:
                segments += [code[i][cut_map[k+1]::]]
    for _ in range(int(len(segments)/2)):
        index = rnd.randint(0, len(segments)-1)
        code[2] += segments[index]
        del segments[index]
    code[2] = mutate(code[2])
    return bin_to_watch(code[2], number)


def mutate(code):
    code = list(code)
    for i in range(len(code)):
        if rnd.random()+CHANCE_TO_MUTATE >= 1:
            #print('mutation')
            code[i] = str((int(code[i]) + rnd.randint(1, 2)) % 3)
    return ''.join(code)


def owns_axis(watch: list):
    """
    Returns true if there is at least one axis in the watch
    """
    for i in range(1, len(watch)):
        if watch[i].__class__.__name__ == "Axis":
            return True
    return False


def distance_between_objs(obj1: Object, obj2: Object):
    """
    It gives the horizontal distance between 2 objects
    """
    return m.sqrt((obj1.x_position - obj2.x_position) ** 2 + (obj1.y_position - obj2.y_position) ** 2)


def list_connections(watch: list):
    """
    Returns a trinome for every connection in the passed watch using this convention :
    [object_1, object_2, type_of_connection] returns False if the watch doesn't contain any axis
    type of connection can be XY_CONNECTION or Z_CONNECTION
    """
    connections = []
    if not owns_axis(watch):
        return []
    for i in range(1, len(watch)):
        for j in range(i+1, len(watch)):
            connection = connect(watch[i], watch[j])
            if connection[2] != NO_CONNECTION:
                connections += [connection]
    return connections


def connect(obj1: Object, obj2: Object):
    if obj1.__class__.__name__ == "Axis" or obj2.__class__.__name__ == "Axis" and \
            distance_between_objs(obj1, obj2) < PIN_DISTANCE:
        obj1.y_position = obj2.y_position
        obj2.x_position = obj1.x_position
        return [obj1, obj2, Z_CONNECTION]
    if obj1.z_position == obj2.z_position and distance_between_objs(obj1, obj2) < CONNECTION_DISTANCE:
        return [obj1, obj2, XY_CONNECTION]
    elif distance_between_objs(obj1, obj2) < PIN_DISTANCE:
        obj1.y_position = obj2.y_position
        obj2.x_position = obj1.x_position
        return [obj1, obj2, Z_CONNECTION]
    else:
        return [obj1, obj2, NO_CONNECTION]

