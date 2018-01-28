
# !/usr/bin/env python
# -----------------------------------------------
__author__ = "Duc Minh TRAN, Tao Duy Chuan LE"
__version__ = "0.0.1"
# -----------------------------------------------

import math
import generation as gen
import random

# HAND VITESSE
VITESSE_SECONDHAND = 1 / 60
VITESSE_MINUTEHAND = 1 / 3600
VITESSE_HOURHAND = 1 / 43200

# POINTS FOR CONNECTIONS
OBJECT_Z_AXIS = 0.01  
OBJECT_PINNED_AXIS = 0.01
GEAR_Z_GEAR = 0.02
GEAR_XY_GEAR = 0.02
GEAR_Z_HAND = 0.02
REMONTOIRE_XY_ROCHET = 0.10
SPRING_Z_BARREL = 0.010
BARREL_XY_SPRING = 0.010
FORK_XY_ESCAPE_WHEEL = 0.020
SPRING_XY_FORK = 0.010
BARREL_XY_GEAR = 0.010
BARREL_Z_BARREL = 0.010
SPRING_Z_BALANCEWHEEL = 0.010
GEAR_XY_ESCAPE_WHEEL = 0.02
# INITIAL VITESSE
VITESSE_INITIAL = 2

#NUMBER OF GENERATIONS:
NUMBER_INDIVIDUALS = 10
NUMBER_GENERATIONS = 1000

class Connection():
    """
    __init__() functions as the class constructor
    """

    def __init__(self, name=None, point=0):
        self.name = name
        self.point = point

ConnectionData = []

def input_database():
	"""
	Function allows to create a list ( more like database)connection of possible connections in a clock
	"""
	for thing in ["Gear", "Escape_Wheel", "Barrel", "Balance_Wheel", "Spring", "Hand", "Fork"]:
		ConnectionData.append(Connection([thing, "Axis", gen.Z_CONNECTION], OBJECT_PINNED_AXIS))
	ConnectionData.append(Connection(["Gear", "Gear", gen.Z_CONNECTION], GEAR_Z_GEAR))
	ConnectionData.append(Connection(["Gear", "Gear", gen.XY_CONNECTION], GEAR_XY_GEAR))
	ConnectionData.append(Connection(["Gear", "Hand", gen.Z_CONNECTION], GEAR_Z_HAND))
	ConnectionData.append(Connection(["Hand", "Gear", gen.Z_CONNECTION], GEAR_Z_HAND))
	ConnectionData.append(Connection(["Fork", "EscapeWheel", gen.XY_CONNECTION], FORK_XY_ESCAPE_WHEEL))
	ConnectionData.append(Connection(["EscapeWheel", "Fork", gen.XY_CONNECTION], FORK_XY_ESCAPE_WHEEL))
	ConnectionData.append(Connection(["Spring","Fork", gen.XY_CONNECTION], SPRING_XY_FORK))
	ConnectionData.append(Connection(["Fork", "Spring", gen.XY_CONNECTION], SPRING_XY_FORK))
	ConnectionData.append(Connection(["EscapeWheel", "Gear", gen.XY_CONNECTION],GEAR_XY_ESCAPE_WHEEL))
	ConnectionData.append(Connection(["Gear", "EscapeWheel", gen.XY_CONNECTION], GEAR_XY_ESCAPE_WHEEL))
	# ConnectionData.append(Connection(["Remontoir","Rochet",HORIZONTAL],REMONTOIRE_XY_ROCHET))
	ConnectionData.append(Connection(["Spring", "Barrel", gen.Z_CONNECTION], SPRING_Z_BARREL))
	ConnectionData.append(Connection(["Barrel", "Spring", gen.Z_CONNECTION], SPRING_Z_BARREL))
	ConnectionData.append(Connection(["Spring", "BalanceWheel", gen.Z_CONNECTION], SPRING_Z_BALANCEWHEEL))
	ConnectionData.append(Connection(["BalanceWheel", "Spring", gen.Z_CONNECTION], SPRING_Z_BALANCEWHEEL))
	ConnectionData.append(Connection(["Barrel", "Gear", gen.XY_CONNECTION], BARREL_XY_GEAR))
	ConnectionData.append(Connection(["Gear", "Barrel", gen.XY_CONNECTION], BARREL_XY_GEAR))
	ConnectionData.append(Connection(["Barrel", "Barrel", gen.Z_CONNECTION], BARREL_Z_BARREL))


def is_pinned(obj1, connection_list):
    for i in range(len(connection_list)):
        if connection_list[i][0] == obj1:
            return connection_list[i][1].__class__.__name__ == "Axis" and connection_list[i][1].rotation == gen.PINNED \
                   and connection_list[i][2] == gen.Z_CONNECTION
        if connection_list[i][1] == obj1:
            return connection_list[i][0].__class__.__name__ == "Axis" and connection_list[i][0].rotation == gen.PINNED \
                   and connection_list[i][2] == gen.Z_CONNECTION
    return False


def gears_XY_connection(obj1,obj2):
	"""
	2 gear connected by teeths,if gear1 spins will train gear 2 to spin
	"""
	if (obj1.y_position == obj2.y_position) and (obj2.x_position == obj1.x_position) and distance_between_objs(obj1, obj2) < PIN_DISTANCE and (obj1.is_rotate() or obj2.is_rotate()):
		obj2.rotates = True
		obj2.speed = gear1.speed * gear1.nb_teeth / gear2.nb_teeth


def objects_Z_connection(obj1,obj2):
	"""
	If 2 objects in the same axe, obj1 will train vitesse to obj2
	"""
	if obj1.z_position == obj2.z_position :
		if obj1.is_rotate():
			obj2.rotates = True
			obj2.speed = obj1.speed

def is_rotate(obj):
	if obj.speed != 0:
		return True
	return False
"""
class FitnessClock:
    "

    def __init__(self, connections):
        self.fitness = 0
        self.connection_list = connections
"""
def does_clock_runs(connection_list):
	#INPUT: A LIST OF CONNECTION OF A CLOCK
    # Verify if a clock actually runs or not. Initial a vitesse for escape wheel

    if ((["Spring", "BalanceWheel", gen.Z_CONNECTION] in connection_list) and (
                ["Spring","Fork", gen.XY_CONNECTION] in connection_list) and (
                ["Fork", "EscapeWheel", gen.XY_CONNECTION] in connection_list) and (
                ["EscapeWheel", "Gear", gen.XY_CONNECTION] in connection_list) and (
                ["Gear", "Barrel", gen.XY_CONNECTION] in connection_list) and (
                ["Gear", "Hand", gen.Z_CONNECTION] in connection_list)and (
                ["Spring", "Barrel", gen.Z_CONNECTION] in connection_list)):
        return True
    return False
def initial_clock_runs(clock):
	#INPUT : LIST OF OBJECTS OF A CLOCK
	#OUTPUT : IF THE CLOCK RUNS< INITIALIZE THE MOVEMENT OF ESCAPE WHEEL.
	connection_list = gen.list_connections(clock)
	if does_clock_runs(connection_list):
		for i in range(1, len(clock)):
			if clock[i].__class__.__name__ == "EscapeWheel":
				clock[i].speed = VITESSE_INITIAL

def i_in_connectdata(connection1):
	#INPUT : A list type [object, object, type of connection]
	#OUTPUT : A Point correspond with the connection in ConnectionData, 0 if the input connection doesn't appear in ConnectionData
	for i in range(len(ConnectionData)):
		x = [connection1[0].__class__.__name__,connection1[1].__class__.__name__,connection1[2]]
		if (x[0]==(ConnectionData[i].name)[0]) and (x[1]==(ConnectionData[i].name)[1]) and (x[2]==(ConnectionData[i].name)[2]):
			# THIS STEP COMPARE NAME OF OBJECT1, NAME OF OBJECT 2, TYPE OF CONNECTION
			return ConnectionData[i].point
	return 0

def fitness(clock):
	"""
	INPUT : A LIST OF CONNECTION OF A CLOCK
	OUTPUT: FITNESS SCORE OF THAT CLOCK
	This part gives score based on connections in a clock that appears in ConnectionData
	"""
	connection_list = gen.list_connections(clock)
	score = 0
	for cn in connection_list:
		if (i_in_connectdata(cn)!=0):
			score += i_in_connectdata(cn)

	# EVALUATE THE CLOCK WHEN IT RUNS
	if (does_clock_runs(connection_list)):
		initial_clock_runs(clock)
		for cn in connection_list:
			print("Tick Tock Tick Tock Tick Tock")
			if ((cn == [gen.Gear, gen.Hand, gen.Z_CONNECTION]) or (cn == [gen.Hand, gen.Gear, gen.Z_CONNECTION]) or (
				cn == [gen.Gear, gen.Gear, gen.Z_CONNECTION])):
				# IF A GEAR AND A HAND CONNECT VERTICALLY THAN THE HAND WILL SPIN
				objects_Z_connection(cn[0], cn[1])
			if (cn == (gen.Gear, gen.Gear, gen.XY_CONNECTION)):
				# IF 2 GEARS CONNECT HORIZONTALLY THEN THE OTHER GEAR WILL SPIN
				gears_XY_connection(cn[0], cn[1])
			if (cn[1] == gen.Hand):
				hand = cn[1]
			if (cn[0] == gen.Hand):
				hand = cn[0]
			"""
			EVALUATE CLOCK
			"""
			SEC_SCORE = 1 - abs((abs(hand.speed) - VITESSE_SECONDHAND) / VITESSE_SECONDHAND)
			MIN_SCORE = 1 - abs((abs(hand.speed) - VITESSE_MINUTEHAND) / VITESSE_MINUTEHAND)
			HOU_SCORE = 1 - abs((abs(hand.speed) - VITESSE_HOURHAND) / VITESSE_HOURHAND)
			if SEC_SCORE == max(SEC_SCORE, MIN_SCORE, HOU_SCORE):
				SCORE_HAND = SEC_SCORE
			elif MIN_SCORE == max(SEC_SCORE, MIN_SCORE, HOU_SCORE):
				SCORE_HAND = 60 * MIN_SCORE
			else:
				SCORE_HAND = 3600 * HOU_SCORE
			score += SCORE_HAND
	return round(score,3)


"""
The hands are important, the more accurately a hand hand tells time, the better fitness score it gets
Hourhand > Minute Hand > Second Hand by priority ( we must know what hours, then what minute, then what second)
"""


def fitness_population(population1):
	list_fitness = []
	for clock in population1:
		list_fitness += [fitness(clock)]
	return list_fitness
def fitness_average(population1):
	sum_fitness =0
	for clock in population1:
		sum_fitness += fitness(clock)
	return sum_fitness/len(population1)
def crossing(population1):
	for i in range(0,100):
		obj1 = population1.pop(random.randrange(len(population1)))
		obj2 = population1.pop(random.randrange(len(population1)))
		obj3 = population1.pop(random.randrange(len(population1)))
		#INPUT
		"""
		Choose randomly 3 clock from population
		Remove the one with the lowest fitness score
		Mate (Crossing) the other two to create a new baby clock
		Add the new baby clock to the population
		"""
		#OUTPUT
		a = fitness(obj1)
		b = fitness(obj2)
		c = fitness(obj3)
		if a == min(a,b,c):
			destroyed_clock = obj1
			dad_clock = obj2
			mom_clock = obj3
		elif b == min(a,b,c):
			destroyed_clock = obj2
			dad_clock = obj1
			mom_clock = obj3
		else:
			destroyed_clock = obj3
			dad_clock = obj2
			mom_clock = obj1
		baby_clock = gen.mate(dad_clock,mom_clock, 2)
		population1.append(dad_clock)
		population1.append(mom_clock)
		population1.append(baby_clock)

		

def natural_selection(population1):
	for j in range(0,NUMBER_GENERATIONS):
		crossing(population1)
		print("Generation",j)
		print("AVERAGE SCORE: ",fitness_average(population1))
		#for clock in population1:
		#	if fitness(clock) <= fitness_average(population1):
		#		population1.remove(clock)
		print(fitness_population(population1))		
		best_cl = best_clock(population1)
		print("BEST CLOCK FITNESS SCORE:",fitness(best_cl))
		#display_clock(best_cl)
		
def best_clock(population1):
	#RETURN THE BEST CLOCK
	maxi =0
	best_clock = []
	for i in range(0,len(population1)):
		temp = fitness(population1[i])
		if temp > maxi:
			maxi = temp
			best_clock = population[i]
	return best_clock

def display_clock(clock):
	connection_list = gen.list_connections(clock)
	for i in range(0,len(connection_list)):
		print (connection_list[i][0].__class__.__name__,connection_list[i][1].__class__.__name__,connection_list[i][2])

"""
	Test
"""
input_database()
population = gen.generate(100,1,25)
natural_selection(population)
#best = best_clock(population)
#print("BEST CLOCK FITNESS SCORE:",fitness(best))

