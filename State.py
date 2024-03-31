import copy


class State:
    def __init__(self, rows, columns, list, citiesVisited):
        self._stateMatrix = list
        self._rows = rows
        self._columns = columns
        self._rowDeleted = []
        self._columnDeleted = []
        self._citiesVisited = citiesVisited
        self._cost = 0
        self._zeroList = []


    #will check if a row needs update     
    def updateRows(self):
        for i in range(self._rows): 
            if(i in self._rowDeleted):
                pass
            else:
                lowerBound = None
                lowestCord = None
                zeroExist = False
                for j in range(self._columns):
                    currentCost = self._stateMatrix[i][j]
                    if(currentCost == 0):
                        self._zeroList.append((i,j))
                        zeroExist = True
                        break
                    else:
                        if(lowerBound == None):
                            lowestCord = (i,j)
                            lowerBound = currentCost
                        elif(lowerBound > currentCost):
                            lowestCord = (i,j)
                            lowerBound = currentCost
                #if we dont break out and for loop concludes 
                #gaurenteed no zero found 
                if(zeroExist == False):
                    self._cost += lowerBound
                    self._zeroList.append(lowestCord)
                    self.updateRow(i, lowerBound)

    #will update specific row
    def updateRow(self, rowIndex, lowerBound):
        for j in range(self._columns):
            self._stateMatrix[rowIndex][j] = self._stateMatrix[rowIndex][j] - lowerBound
    
    #will check if a row needs update     
    def updateColumns(self):
        for j in range(self._columns): 
            if(j in self._columnDeleted):
                pass
            else:
                lowerBound = None
                zeroExist = False
                for i in range(self._rows):
                    currentCost = self._stateMatrix[i][j]
                    if(currentCost == 0):
                        # self._zeroList.append((i,j))
                        zeroExist = True
                        break
                    else:
                        if(lowerBound == None):
                            lowestCord = (i,j)
                            lowerBound = currentCost
                        elif(lowerBound > currentCost):
                            lowestCord = (i,j)
                            lowerBound = currentCost
                #if we dont break out and for loop concludes 
                #gaurenteed no zero found 
                if(zeroExist == False):
                    self._cost += lowerBound
                    self._zeroList.append(lowestCord)
                    self.updateColumn(j, lowerBound)

    #will update specific row
    def updateColumn(self, columnIndex, lowerBound):
        for i in range(self._rows):
            self._stateMatrix[i][columnIndex] = self._stateMatrix[i][columnIndex] - lowerBound
    #Creates a new state based on the location selected 
    def makeNewState(self, rowIndex, columnIndex):
        newStateMatrix = copy.deepcopy(self._stateMatrix) # copy the matrix
        for j in range(self._columns):
            newStateMatrix[rowIndex][j] = float('inf')
        for i in range(self._rows):
            newStateMatrix[i][columnIndex] = float('inf')
        #add the rowIndex the city we visited to the list 
            self._citiesVisited.append(rowIndex)
        return newStateMatrix
    

    #getters 
    def getZeroList(self):
        return self._zeroList

    def getTotalCost(self):
        return self._cost
    
    def getCost(self, rowIndex, columnIndex):
        return self._stateMatrix[rowIndex][columnIndex]
    
    def getCitiesVisited(self):
        return self._citiesVisited
                    

    