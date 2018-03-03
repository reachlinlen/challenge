#skiing in Singapore - RedMart
#
import numpy as np
#
global maxi
global maxj
# i - row, j - col, move in 4 directions & find all paths
def traverse(sketch,i,j,path,player):
    player.append(sketch[i][j])
    if (i+1) < maxi:			#not last column,so can move right
        if sketch[i][j] > sketch[i+1][j]:
            traverse(sketch,i+1,j,path,player)
    if (j+1) < maxj:			#not last row, so can move down
        if sketch[i][j] > sketch[i][j+1]:
            traverse(sketch,i,j+1,path,player)
    if j!= 0:                   #not 0th col, so can move left
        if sketch[i][j] > sketch[i][j-1]:
            traverse(sketch,i,j-1,path,player)
    if i!=0:                    #not 0th row, so can move up
        if sketch[i][j] > sketch[i-1][j]:
            traverse(sketch,i-1,j,path,player)
    path.append(list(player))
    player.pop()

#remove all short paths by finding length of drop & sorting out shortest ones
def remShortPath(path):
    pathwithLen = {}
    for k in range(len(path)):
        pathwithLen[k] = len(path[k])  
    sortedPath = sorted(pathwithLen.items(),key=lambda t:t[1],reverse=True)
    sortedList = []
#find out indexes in path that are long
    for k,l in sortedPath:
        if len(sortedList) == 0:
            sortedList.append(k)
            length = l
        elif length == l:
            sortedList.append(k)
        else:
            break
    for index in range(len(sortedList)):
        sortedList[index] = path[sortedList[index]]
    return sortedList

#create numpy array to hold data after reading skiing sketch
sketch = np.arange(1000000).reshape(1000,1000)
maxi,maxj = sketch.shape
index = 0
with open("map.txt") as m:
    while True:
        row = m.readline()
        if row != '':
            arr_list = row.rstrip('\n').split(' ')
            sketch[index] = arr_list
            index += 1
        else:
            break
# Move across the array to get all paths
allLongPath,rowwisePath,player = [],[],[]
for row in range(maxi):
    for col in range(maxj):
        traverse(sketch,row,col,rowwisePath,player)
        allLongPath.extend(remShortPath(rowwisePath))
        allLongPath = remShortPath(allLongPath)
        rowwisePath,player = [],[]
#   
print(allLongPath)
#x = findLongPath(allLongPath)
highDrop = 0
for path in allLongPath:
    drop = path[0] - path[len(path)-1]
    print("Drop of {0} is {1}".format(path,drop))
    if drop > highDrop:
        highDrop = drop
print("Highest drop is {0}".format(highDrop))