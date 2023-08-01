import time
import os
import sys

#"6xxx2xxx8x13xxx54xx2x8x4x6xxx2x6x4xx4xx1x2xx9xx5x4x8xxx5x7x3x9xx38xxx21x9xxx1xxx3" - solve in two
#"64752193881367954252983416737296845148615237919534782625178369473849621596xxxxxxx" - solve in one
#"x475219388x367954252x834167372x684514861x237919534x826251783x947384962x596421578x" - solve in one
#"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" - solve in two
#"x1xx4xxxxx2xxx79x1x6x28xxxx8xx1xxxx3xxxx6xxxx4xxxx8xx5xxxx16x7x6x39xxx1xxxxx2xx9x" - solve in one
#"xx53xxxxx8xxxxxx2xx7xx1x5xx4xxxx53xxx1xx7xxx6xx32xxx8xx6x5xxxx9xx4xxxx3xxxxxx97xx"
    
def decodeGrid(grid): #"xx1xxx3xxx8xxxxx2xxx8xx"...
	decodedGrid = []
	
	byRow = []
	for row in range(9):
		newRow = []
		for col in range(9):
			newRow.append(grid[row*9+col])
		byRow.append(newRow)
	decodedGrid.append(byRow)
	
	byCol = []
	for col in range(9):
		newCol = []
		for row in range(9):
			newCol.append(grid[row*9+col])
		byCol.append(newCol)
	decodedGrid.append(byCol)
	
	bySqu = []
	for squ in [0,1,2,9,10,11,18,19,20]:
		newSqu = []
		for additional in [0,1,2,9,10,11,18,19,20]:
			newSqu.append(grid[squ*3+additional])
		bySqu.append(newSqu)
	decodedGrid.append(bySqu)	
	
	return decodedGrid
	
def flattenGrid(grid):
	string = ""
	for row in grid[0]:
		for item in row:
			string = string+item
	return string
	
def check(grid):
	for byType in grid:
		for part in byType:
			for num in range(9):
				if part.count(str(num+1))>1:
					return 0 #case 0: doesn't work
	for row in grid[0]:
		for num in row:
			if not num in "123456789":
				return 1 #case 1: blanks
	return 2 #case 2: perfect

def fillObv(grid):
	flatGrid = flattenGrid(grid)
	for i in range(81):
		if not flatGrid[i] in "123456789":
			possibleValues = []
			for j in range(9):
				if not checkItem(j+1,i,grid):
					possibleValues.append(j+1)
			if len(possibleValues) == 1:
				flatGrid = flatGrid[:i]+str(possibleValues[0])+flatGrid[i+1:]
			elif len(possibleValues) == 0:
				print("Error")
				return 0
	grid = decodeGrid(flatGrid)
	for byType in range(3):
		for part in range(9):
			arr = [1,2,3,4,5,6,7,8,9]
			for i in grid[byType][part]:
				if i in "123456789":
					arr.remove(int(i))
			for i in arr:
				possiblePlaces = []
				arr2 = [0,1,2,3,4,5,6,7,8]
				for j in range(9):
					if grid[byType][part][j] in "1234556789":
						arr2.remove(int(j))
				for place in arr2:
					if byType==0:
						num = part*9+place
					elif byType==1:
						num = part+9*place
					else:
						num = [0,1,2,9,10,11,18,19,20][part]*3+[0,1,2,9,10,11,18,19,20][place]
					if not flatGrid[num] in "123456789":
						if not checkItem(i,num,grid):
							possiblePlaces.append(num)
				if len(possiblePlaces) == 1:
					flatGrid = flatGrid[:possiblePlaces[0]]+str(i)+flatGrid[possiblePlaces[0]+1:]
					grid = decodeGrid(flatGrid)
				elif len(possiblePlaces) == 0:
					print("Error")
					return 0
	return grid
	
def checkItem(item, num, grid):
	row = grid[0][num//9]
	col = grid[1][num%9]
	squ = grid[2][((num//3)%3)+3*(num//27)]
	numExists = False
	for arr in [row,col,squ]:
		if arr.count(str(item))!=0:
			numExists = True
	return numExists

def outputGrid(grid):
	flatGrid = flattenGrid(grid)
	os.system("clear")
	for thirds in range(3):
		for row in range(3):
			string = ""
			for squ in range(3):
				for item in range(3):
					string = string+flatGrid[0]+" "
					flatGrid = flatGrid[1:]
				if squ != 2:
					string = string+"|"
			print(string)
		if row==2 and thirds!=2:
			print("--------------------")

def useHyp(grid,boolean=True):
	flatGrid = flattenGrid(grid)
	allPossVals = []
	for item in range(81):
		possibleValues = []
		if not flatGrid[item] in "123456789":
			for j in range(9):
				if not checkItem(j+1,item,grid):
					possibleValues.append(j+1)
		allPossVals.append(possibleValues)
	for i in range(1,10):
		for j in allPossVals:
			if len(j)==i:
				specialItem = allPossVals.index(j)
				possVals = j
				for k in possVals:
					done = False
					hypGrid = decodeGrid(flatGrid[:specialItem]+str(k)+flatGrid[specialItem+1:])
					while not done:
						newGrid = fillObv(hypGrid)
						if boolean:
							outputGrid(newGrid)
						if newGrid == 0:
							if boolean:
								print("Hypothetical can't work")
							done = True
						elif newGrid == hypGrid:
							newGrid = useHyp(hypGrid,boolean)
							return newGrid
						elif check(newGrid)==2:
							return newGrid
						else:
							hypGrid = newGrid
					possVals.pop(k)
					if len(possVals) == 1:
						grid = decodeGrid(flatGrid[:specialItem]+str(possVals[0])+flatGrid[specialItem+1:])
						g = useHyp(grid)
						try:
							flattenGrid(g)
							return g
						except:
							print("Error")
							time.sleep(10)
	return 0

def findOther(grid):
	solutions = []
	flatGrid = flattenGrid(grid)
	allPossVals = []
	for item in range(81):
		possibleValues = []
		if not flatGrid[item] in "123456789":
			for j in range(9):
				if not checkItem(j+1,item,grid):
					possibleValues.append(j+1)
		allPossVals.append(possibleValues)
	for i in range(10):
		for j in range(81):
			possVals = allPossVals[j]
			if len(possVals)==i and possVals!=[]:
				for k in possVals:
					hypGrid = decodeGrid(flatGrid[:j]+str(k)+flatGrid[j+1:])
					newGrid = useHyp(hypGrid,False)
					if newGrid != 0:
						if check(newGrid)==2:
							solutions.append(newGrid)
					outputSolutions(solutions)

def outputSolutions(array):
	c = len(array)
	i = 0
	while i<c:
		i += 1
		for j in range(array.count(array[i-1])-1):
			array.remove(array[i-1])
			c -= 1
	if len(array)>1:
		sys.stdout.write("\rSo far, "+str(len(array)-1)+" other solutions have been found")
		sys.stdout.flush()

def main():
	solved = False
	empty = True
	while empty:
		gridInp = str(input("Enter your grid: "))
		if len(gridInp) == 81:
			grid = decodeGrid(gridInp)
			empty = False
			if check(grid)==0:
				print("Impossible solve")
				empty = True
			needed = []
			for i in range(9):
				needed.append(9-gridInp.count(str(i+1)))
		else:
			print("Incorrect length")
	start = time.time()
	while not solved:
		newGrid = fillObv(grid)
		outputGrid(newGrid)
		if newGrid==grid:
			try:
				newGrid = useHyp(grid)
				outputGrid(newGrid)
				print("Hypothetical was successful")
				findOther(grid)
			except:
				print("Failed")
				break
		grid = newGrid
		if check(grid)==2:
			solved = True
			print("Done")
	print(str(time.time()-start)+"s")
main()
