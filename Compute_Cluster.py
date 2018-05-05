import pickle
import os

threshold = 4


class Tree:
    def __init__(self, node):
        self.left = None
        self.right = None
        self.data = node



def insert(root, val, flag):
    if root == None:
        return Tree(val)
     
    if val[flag] <= root.data[flag]:
        root.left = insert(root.left, val, flag^1)
    else:
        root.right = insert(root.right, val, flag^1)
    
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
        return root.data

def find_closest_request(latitude, longitude, cluster_count):

    with open('requests.pickle', 'rb') as handle:
        root = pickle.load(handle)
        
    if root == None:
        root = insert(root, [latitude, longitude, cluster_count], 0)
        pickle.dump(root, open("requests.pickle", "wb" ))
        return [-1,-1]
        
    node = searchTree(root, [latitude, longitude], 0)
    
    
    distance = ((node[0]-latitude)**2 + (node[1]-longitude)**2)**0.5
    
    if distance > threshold:
        root = insert(root, [latitude, longitude, cluster_count], 0)
    else:
        root = insert(root, [latitude, longitude, node[2]], 0)
    pickle.dump(root, open("requests.pickle", "wb" ))
        
    return [distance, node[2]]


def adjust_clusters(latitude, longitude):
    

    cluster_count=0
    for root, dirs, files, in os.walk("clusters"):
        for cluster in files:
            cluster_count+=1
    #print(cluster_count)
    
    data = find_closest_request(latitude, longitude, cluster_count)
    
    if(data[0]==-1 or data[0] > threshold):
        new_cluster = [[latitude, longitude]]
        pickle.dump(new_cluster, open("clusters/cluster"+str(cluster_count)+".pickle", "wb" ))
        
        #return cluster_count
    
    else:
        with open('clusters/cluster'+ str(data[1]) +'.pickle', 'rb') as handle:
            cluster = pickle.load(handle)
        cluster.append([latitude, longitude]) 
        pickle.dump(cluster, open('clusters/cluster'+ str(data[1]) +'.pickle', "wb" ))
        
        #return data[1]

