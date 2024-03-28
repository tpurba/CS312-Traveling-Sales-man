class Matrix:
    def __init__(self, rows, columns):
        self._array = [[0 for _ in range(rows)] for _ in range(columns)]
        self._rows = rows
        self._columns = columns
        self._rowDeleted = []
        self._columnDeleted = []

    def addToArray(self, exiting, entering, cost):
        self._array[exiting][entering] = cost

    #will check if a row needs update     
    def updateRows(self):
        for i in range(self._rows): 
            if(i in self._rowDeleted):
                pass
            else:
                lowerBound = None
                for j in range(self._columns):
                    currentCost = self._array[i][j]
                    if(currentCost == 0):
                        break
                    else:
                        if(lowerBound == None):
                            lowerBound = currentCost
                        elif(lowerBound > currentCost):
                            lowerBound = currentCost
                #if we dont break out and for loop concludes 
                #gaurenteed no zero found 
                self.updateRow(i, lowerBound)

    #will update specific row
    def updateRow(self, rowIndex, lowerBound):
        for j in range(self._columns):
            self._array[rowIndex][j] = self._array[rowIndex][j] - lowerBound
                        
                    

    