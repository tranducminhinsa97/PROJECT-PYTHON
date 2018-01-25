
# !/usr/bin/env python
# -----------------------------------------------
__author__ = "Duc Minh TRAN, Tao Duy Chuan LE"
__version__ = "0.0.1"
# -----------------------------------------------

import math
import generation as gen

# HAND VITESSE
VITESSE_SECONDHAND = 1 / 60
VITESSE_MINUTEHAND = 1 / 3600
VITESSE_HOURHAND = 1 / 43200

# POINTS FOR CONNECTIONS
OBJECT_VERTICAL_AXIS = 1  
OBJECT_PINNED_AXIS = 1
GEAR_VERTICAL_GEAR = 2
GEAR_HORIZONTAL_GEAR = 2
GEAR_VERTICAL_HAND = 5
REMONTOIRE_HORIZONTAL_ROCHET = 10
SPRING_VERTICAL_BARREL = 10
BARREL_HORIZONTAL_SPRING = 10
FORK_HORIZONTAL_ESCAPE_WHEEL = 20
BALANCE_WHEEL_VERTICAL_FORK = 20

# INITIAL VITESSE
VITESSE_INITIAL = 2


class Connection(object):
    """
    __init__() functions as the class constructor
    """

    def __init__(self, name=None, point=0):
        self.name = name
        self.point = point

    ConnectionData = []

    def input_database(self):
        """
        Function allows to create a list ( more like database)connection of possible connections in a clock
        """
        for thing in ["Gear", "Escape_Wheel", "Barrel", "Balance_Wheel", "Spring", "Hand", "Fork"]:
            self.ConnectionData.append(Connection([thing, "Axis", gen.PINNED], OBJECT_PINNED_AXIS))
        self.ConnectionData.append(Connection(["Gear", "Gear", gen.Z_CONNECTION], GEAR_VERTICAL_GEAR))
        self.ConnectionData.append(Connection(["Gear", "Gear", gen.XY_CONNECTION], GEAR_HORIZONTAL_GEAR))
        self.ConnectionData.append(Connection(["Gear", "Hand", gen.Z_CONNECTION], GEAR_VERTICAL_HAND))
        self.ConnectionData.append(Connection(["Hand", "Gear", gen.Z_CONNECTION], GEAR_VERTICAL_HAND))
        self.ConnectionData.append(Connection(["Fork", "Escape_Wheel", gen.XY_CONNECTION], FORK_HORIZONTAL_ESCAPE_WHEEL))
        self.ConnectionData.append(Connection(["Escape_Wheel", "Fork", gen.XY_CONNECTION], FORK_HORIZONTAL_ESCAPE_WHEEL))
        self.ConnectionData.append(Connection(["Balance_wheel", "Fork", gen.Z_CONNECTION], BALANCE_WHEEL_VERTICAL_FORK))
        self.ConnectionData.append(Connection(["Fork", "Balance_wheel", gen.Z_CONNECTION], BALANCE_WHEEL_VERTICAL_FORK))
        # self.ConnectionData.append(Connection(["Remontoir","Rochet",HORIZONTAL],REMONTOIRE_HORIZONTAL_ROCHET))
        self.ConnectionData.append(Connection(["Spring", "Barrel", gen.Z_CONNECTION], SPRING_VERTICAL_BARREL))
        self.ConnectionData.append(Connection(["Barrel", "Spring", gen.Z_CONNECTION], SPRING_VERTICAL_BARREL))
        self.ConnectionData.append(Connection(["Spring", "Balance_Wheel", gen.Z_CONNECTION], SPRING_VERTICAL_BARREL))


def is_pinned(obj1, connection_list):
    for i in range(len(connection_list)):
        if connection_list[i][0] == obj1:
            return connection_list[i][1].__class__.__name__ == "Axis" and connection_list[i][1].rotation == gen.PINNED \
                   and connection_list[i][2] == gen.Z_CONNECTION
        if connection_list[i][1] == obj1:
            return connection_list[i][0].__class__.__name__ == "Axis" and connection_list[i][0].rotation == gen.PINNED \
                   and connection_list[i][2] == gen.Z_CONNECTION
    return False


def gears_horizontal_connection(gear1, gear2):
    """
    2 gear connected by teeths,if gear1 spins will train gear 2 to spin
    """
    if (are_horizontally_connected(gear1, gear2)) and (gear1.is_rotate):
        gear2.is_rotate = True
        gear2.rotate_direction = - gear1.rotate_direction
        gear2.vitesse = gear1.vitesse * gear1.nb_teeth / gear2.nb_teeth


def objects_vertical_connection(obj1, obj2):
    """
    If 2 objects in the same axe, obj1 will train vitesse to obj2
    """
    if are_vertically_connected(obj1, obj2) and gear1.is_rotate:
        if obj1.is_rotate():
            obj2.vitesse = obj1.vitesse

def is_rotate(obj):
	if obj.vitesse != 0:
		return True
	return False
"""
class FitnessClock:
    """
    Class that receives the ensemble of parts with its position and list of connections possible
    """

    def __init__(self, connections):
        self.fitness = 0
        self.connection_list = connections
"""
def does_clock_runs(connection_list):
	#INPUT: A LIST OF CONNECTION OF A CLOCK
    # Verify if a clock actually runs or not. Initial a vitesse for escape wheel

    if ((["Spring", "Barrel", gen.Z_CONNECTION] in connection_list) and (
                ["Spring", "Escape_wheel", gen.Z_CONNECTION] in connection_list) and (
                ["Escape_wheel", "Fork", gen.Z_CONNECTION] in connection_list) and (
                ["Remontoir", "Rochet", gen.XY_CONNECTION] in connection_list) and (
                ["Barrel", "Barrel", gen.Z_CONNECTION] in connection_list)):
            #c.Escape_wheel.vitesse = VITESSE_INITIAL-------- > Je veux initialiser la vitesse pour roue d'echappement
        return True
    return False

def fitness(connection_list):
    """
    	INPUT : A LIST OF CONNECTION OF A CLOCK
    	OUTPUT: FITNESS SCORE OF THAT CLOCK
        This part gives score based on connections in a clock that appears in ConnectionData
    """
    for cn in connection_list:
        if cn in Connection.ConnectionData.name:
            fitness_point += Connection.ConnectionData.point

        # EVALUATE THE CLOCK WHEN IT RUNS
    if (does_clock_runs(connection_list)):
        for cn in connection_list:
            if ((cn == ["Gear", "Hand", gen.Z_CONNECTION]) or (cn == ["Hand", "Gear", gen.Z_CONNECTION]) or (
                    cn == ["Gear", "Gear", gen.Z_CONNECTION])):
                    # IF A GEAR AND A HAND CONNECT VERTICALLY THAN THE HAND WILL SPIN
                objects_vertical_connection(cn[0], cn[1])
            if (cn == ("Gear", "Gear", gen.XY_CONNECTION)):
                    # IF 2 GEARS CONNECT HORIZONTALLY THEN THE OTHER GEAR WILL SPIN
                gears_horizontal_connection(cn[0], cn[1])
            if (cn.obj2.name == "Hand"):
                hand = obj2
            if (cn.obj1.name == "Hand"):
                hand = obj1

            """
                    EVALUATE CLOCK
            """
            SEC_SCORE = 1 - abs((abs(hand.vitesse) - VITESSE_SECONDHAND) / VITESSE_SECONDHAND)
            MIN_SCORE = 1 - abs((abs(hand.vitesse) - VITESSE_MINUTEHAND) / VITESSE_MINUTEHAND)
            HOU_SCORE = 1 - abs((abs(hand.vitesse) - VITESSE_HOURHAND) / VITESSE_HOURHAND)
            if SEC_SCORE == max(SEC_SCORE, MIN_SCORE, HOU_SCORE):
                SCORE_HAND = SEC_SCORE
            elif MIN_SCORE == max(SEC_SCORE, MIN_SCORE, HOU_SCORE):
                SCORE_HAND = 60 * MIN_SCORE
            else:
                SCORE_HAND = 3600 * HOU_SCORE
            fitness += SCORE_HAND
    return fitness


"""
The hands are important, the more accurately a hand hand tells time, the better fitness score it gets
Hourhand > Minute Hand > Second Hand by priority ( we must know what hours, then what minute, then what second)
"""


def fitness_population(generation1):
    list_fitness = []
    for clock in generation1:
        list_fitness += [clock,fitness(clock)]
    return list_fitness
