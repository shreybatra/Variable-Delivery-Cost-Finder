import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

def takeFirst(elem):
    return elem[0]

def calculate_centroid(cluster):
        
    size=len(cluster)
    
    if size == 1:
        return [cluster[0][0], cluster[0][1], size]
    
    cluster.sort(key=takeFirst)
    
    A=0
    x=0;y=0
    for i in range(size):
        temp = (cluster[i][0]*cluster[(i+1)%size][1] - cluster[(i+1)%size][0]*cluster[i][1])
        A += temp
        x += (cluster[i][0]+cluster[(i+1)%size][0])*temp
        y += (cluster[i][1]+cluster[(i+1)%size][1])*temp
    
    if A == 0:
        return [cluster[0][0], cluster[0][1], size]
    
    x//=int(3*A)
    y//=int(3*A)
    
    return [x,y,size]

def new_warehouse():
    
    clusters=[]
    for root, dirs, files, in os.walk("clusters"):
        for cluster in files:
            if cluster[-8]>='0' and cluster[-8]<='9':
                with open('clusters/'+ cluster, 'rb') as handle:
                    cluster = pickle.load(handle)
                clusters.append(cluster)

    #print(clusters)
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], frameon=False)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)

    zer = np.zeros(41)
    x_axis = np.arange(-20,21)

    plt.plot(x_axis,zer,c='black', linewidth=0.5)
    plt.plot(zer,x_axis,c='black', linewidth=0.5)
    plt.xlabel('X - AXIS')
    plt.ylabel('Y - AXIS')

    c = 0
    colo = ['red','blue','green','yellow','purple','magenta','black','cyan','aqua','gold','beige','chocolate','fuchsia','maroon']

    for l in clusters:
        l = np.array(l)
        #print(l)
        ax.scatter(l[:,0],l[:,1],c=colo[c],s=15)
        c += 1
        if c==len(colo):
            c = 0


    

    centroids=[] 
    for cluster in clusters:
        centroids.append(calculate_centroid(cluster))


    temp=0
    x=0;y=0
    for centroid in centroids:
        x += centroid[0]*centroid[2]
        y += centroid[1]*centroid[2]
        temp += centroid[2]

    ax.scatter(x//temp,y//temp,c='blue',s=100)
    plt.show()
    return [x//temp, y//temp]

print(new_warehouse())

