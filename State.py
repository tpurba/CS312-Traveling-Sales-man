class State:
    def __init__(self, rows, columns, list):
        self._stateMatrix = list
        self._rows = rows
        self._columns = columns
        self._rowDeleted = []
        self._columnDeleted = []
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
        newStateMatrix = self._stateMatrix
        for j in range(self._columns):
            newStateMatrix[rowIndex][j] = float('inf')
        for i in range(self._rows):
            newStateMatrix[i][columnIndex] = float('inf')
        return newStateMatrix
    

    #getters 
    def getZeroList(self):
        return self._zeroList

    def getTotalCost(self):
        return self._cost
    
    def getCost(self, rowIndex, columnIndex):
        
                    

    