#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import random
from State import State
from PriorityQueue import PriorityQueue

class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)#give only array and you get the bssf generated 
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		count = 0
		bssf = None
		start_time = time.time()
		for i in range(ncities):
			isFinished = False
			route = []
			while time.time()-start_time < time_allowance and isFinished == False:
				baseCity = cities[i] #get a random number in range of 0 to last element in cities
				route.append(baseCity)
				while (len(route) != ncities):
					self.lowestCostRoute = [None, None]	
					for j in range(ncities):
						if(cities[j] in route): # if the city[i] is in the route we dont use it
							pass
						else:
							self.findLowestRoute(baseCity, cities[j])
					if(self.lowestCostRoute != None):
						route.append(self.lowestCostRoute[1])
						baseCity = self.lowestCostRoute[1]
					count += 1 # currently counting for the number of times we have added a route
				tempcost = TSPSolution(route)
				if(tempcost.cost != np.inf):
					if(bssf == None):
						bssf = tempcost
					if(bssf.cost > tempcost.cost):
						bssf = tempcost
				isFinished = True
		end_time = time.time()
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results 
	
	def findLowestRoute( self, baseCity, visitingCity):
		tempCost = baseCity.costTo(visitingCity)
		if(self.lowestCostRoute[0] == None):
			self.lowestCostRoute[0] = tempCost
			self.lowestCostRoute[1] = visitingCity #index here 
		elif(self.lowestCostRoute[0] > tempCost):
			self.lowestCostRoute[0] = tempCost
			self.lowestCostRoute[1] = visitingCity #index here 


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound(self, time_allowance=300.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		pruned = 0
		count = 0
		route = []
		bssf = None
		start_time = time.time()
		tempList =  [[0 for _ in range(ncities)] for _ in range(ncities)]
		priorityQueue = PriorityQueue()
		citiesVisited = []
		columnsNegated = []
		isPQEmpty = False
		depth = 0 
		cost = 0


		# build initalMatrix
		for i in range(ncities):
			currentCity = cities[i]
			for j in range(ncities):	
				tempList[i][j] = currentCity.costTo(cities[j])
		#initialize the matrix
		baseMatrix = State(ncities, ncities, tempList, citiesVisited, columnsNegated, cost, 0)
		#update the matrix 
		baseMatrix.updateRows()
		baseMatrix.updateColumns()
		initialbssf = self.greedy()['cost'] # get inital bssf 
		bssf = initialbssf
		#inital check 
		if(bssf < baseMatrix.getTotalCost()): # your done 
			end_time = time.time()
			results['cost'] = 0 # since the inital bssf was the best 
			results['time'] = end_time - start_time
			results['count'] = count
			results['soln'] = bssf
			results['max'] = None
			results['total'] = None
			results['pruned'] = None
			return results 
		#time.time()-start_time < time_allowance and
		while isPQEmpty == False:
			#create all the possible states
			zeroList = baseMatrix.getZeroList()
			#Create all states 
			for i in range(len(zeroList)):
				#set the base cost
				cost = baseMatrix.getTotalCost()#TODO: keep cost actually the cost 
				rowIndex = zeroList[i][0]
				columnIndex =  zeroList[i][1]
				# #TODO: add chosen cost but wouldn't it be always zero so no point in doing this? 
				# cost += stateMatrix.getCost(rowIndex, columnIndex)
				#update visited cities 
				# TODO: PROBLEM HERE dont use stateMatrix as it will be the base for everything try to leave everything out of stateMatrix
				citiesVisited = baseMatrix.getCitiesVisited()
				citiesVisited.append(rowIndex)
				columnsNegated = baseMatrix.getColumnsDeteleted()
				columnsNegated.append(columnIndex)
				#Make state 
				newState = baseMatrix.makeNewState(rowIndex, columnIndex)
				depth = baseMatrix.getDepth() + 1
				newStateMatrix = State(ncities, ncities, newState, citiesVisited, columnsNegated, cost, depth)
				newStateMatrix.updateRows()
				newStateMatrix.updateColumns()
				#update cost after updating the rows
				cost = newStateMatrix.getTotalCost()
				#only add when cost is less than bssf
				if(cost <= bssf):
					if(len(citiesVisited) == ncities): 
						if(self.cityCheck(cities, citiesVisited)):
							bssf = cost
							route = self.makeRoute(cities, citiesVisited)
						else: 
							priorityQueue.push(newStateMatrix, cost - newStateMatrix.getDepth())
					else:
						priorityQueue.push(newStateMatrix, cost - newStateMatrix.getDepth())
				else: # prune/ dont add
					pruned = pruned + 1
			#out of for loop
			getBaseMatrix = True
			while(getBaseMatrix == True and isPQEmpty == False): # basically allows for the bssf to be compared to priority queue
				if(len(priorityQueue) == 0): # check for empty 
					isPQEmpty = True
				else:
					baseMatrix = priorityQueue.pop()
					if(baseMatrix.getTotalCost() > bssf):
						pruned = pruned + 1
						getBaseMatrix = True
					else:
						getBaseMatrix = False

		if len(route) == 0: 
			bssf = np.inf
		else:
			bssf = TSPSolution(route)

		#end
		end_time = time.time()
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = pruned
		return results 
	
	def cityCheck(self, cities, citiesVisited):
		for i in range(len(cities)):
			if(i not in citiesVisited):
				return False
		return True
	def makeRoute(self, cities, citiesVisited):
		tempRoute = []
		for i in range(len(citiesVisited)):
			tempRoute.append(cities[citiesVisited[i]])
		return tempRoute
	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
