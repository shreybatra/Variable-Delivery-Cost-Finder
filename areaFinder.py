import pandas as pd
import googlemaps
import pickle
from geopy.distance import vincenty


updated = False


class Tree:
    def __init__(self, node):
        self.left = None
        self.right = None
        self.data = node


def insert(root, val, flag):
    if root == None:
        return Tree([val[0], val[1], 0])
     
    if val[flag] <= root.data[flag]:
        root.left = insert(root.left, val, flag^1)
    else:
        root.right = insert(root.right, val, flag^1)
    
    return root

def createSearchTree():
        
    root = None
    data=pd.read_csv("data.csv")

    
    data = data.values.tolist()

    node=()
    for row in data:
        
        
        node = [row[0],row[1]]
        root = insert(root, node, 0)
       
    return root


def searchTree(root, location, flag):
    
    if location[flag] < root.data[flag]:
        
        if root.left==None:
            return root.data
        
        root_dis = ((location[0]-root.data[0])**2 + (location[1]-root.data[1])**2)**0.5
        l_dis = ((location[0]-root.left.data[0])**2 + (location[1]-root.left.data[1])**2)**0.5
        
        if l_dis < root_dis:
            return searchTree(root.left, location, flag^1)
        
        else:
            temp = searchTree(root.left, location, flag^1)

            if((((location[0]-temp[0])**2 + (location[1]-temp[1])**2)**0.5) < root_dis):
                return temp
            else:
                return root.data  

    
    elif location[flag] > root.data[flag]:
        
        if root.right==None:
            return root.data 
        
        root_dis = ((location[0]-root.data[0])**2 + (location[1]-root.data[1])**2)**0.5
        r_dis = ((location[0]-root.right.data[0])**2 + (location[1]-root.right.data[1])**2)**0.5
        
        if r_dis < root_dis:
            return searchTree(root.right, location, flag^1)
        
        else:
            temp = searchTree(root.right, location, flag^1)

            if((((location[0]-temp[0])**2 + (location[1]-temp[1])**2)**0.5) < root_dis):
                return temp
            else:
                return root.data
        
    else:
        root.data[2] += 1        
        return root.data

def ReturnConstituency(latitude, longitude):

    with open('tree.pickle', 'rb') as handle:
        root = pickle.load(handle)

    
    
    node = searchTree(root, [latitude, longitude], 0)

    if node[0]!=latitude or node[1]!=longitude:
        searchTree(root, [node[0], node[1]], 0)

    pickle.dump(root,open('tree.pickle','wb'))
    return node

#pickle.dump(createSearchTree(),open('tree.pickle','wb'))

#print(ReturnConstituency(1,1))