class State:
    def __init__(self, rows, columns, list):
        self._stateMatrix = list
        self._rows = rows
        self._columns = columns
        self._rowDeleted = []
        self._columnDeleted = []

    #will check if a row needs update     
    def updateRows(self):
        for i in range(self._rows): 
            if(i in self._rowDeleted):
                pass
            else:
                lowerBound = None
                zeroExist = False
                for j in range(self._columns):
                    currentCost = self._stateMatrix[i][j]
                    if(currentCost == 0):
                        zeroExist = True
                        break
                    else:
                        if(lowerBound == None):
                            lowerBound = currentCost
                        elif(lowerBound > currentCost):
                            lowerBound = currentCost
                #if we dont break out and for loop concludes 
                #gaurenteed no zero found 
                if(zeroExist == False):
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
                        zeroExist = True
                        break
                    else:
                        if(lowerBound == None):
                            lowerBound = currentCost
                        elif(lowerBound > currentCost):
                            lowerBound = currentCost
                #if we dont break out and for loop concludes 
                #gaurenteed no zero found 
                if(zeroExist == False):
                    self.updateColumn(j, lowerBound)

    #will update specific row
    def updateColumn(self, columnIndex, lowerBound):
        for i in range(self._rows):
            self._stateMatrix[i][columnIndex] = self._stateMatrix[i][columnIndex] - lowerBound
                        
                    

    