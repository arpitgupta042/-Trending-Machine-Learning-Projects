import os
import string
import sys
import numpy

from itertools import chain
from glob import glob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from numpy import dot, sqrt

def cosine_distance(u, v, binary=False):
    """Return the cosine distance between two vectors."""
    if binary:
        return cosine_distance_binary(u, v)
    return 1.0 - dot(u, v) / (sqrt(dot(u, u)) * sqrt(dot(v, v)))
    
def cosine_distance_binary(u, v):
    u = binarize_vector(u)
    v = binarize_vector(v)
    return (1.0 * (u * v).sum()) / numpy.sqrt((u.sum() * v.sum()))

def similarity_measure(a,b):
        x=[]
        for z in a:
                x.append(z[1])
               
        y=[]
        for z in b:
                y.append(z[1])
        common=sorted(list(set(x) & set(y)))
##        print(a)
##        print(b)
##        print(x)
##        print(y)
##        print(common)
        fa=[]
        fb=[]
        j=0
##        print(len(common))
        for i in range(len(common)):
                while ((a[j][1])!=common[i]):
                        j=j+1
                fa.append(a[j][0])
        j=0
        for i in range(len(common)):
                while ((b[j][1])!=common[i]):
                        j=j+1
                fb.append(b[j][0])
        
##        print(fa)
##        print(fb)
        return cosine_distance(fa,fb)


class Cluster:
    def __init__(self):
        pass
    def __repr__(self):
        return '(%s,%s)' % (self.left, self.right)
    def add(self, clusters, grid, lefti, righti,finallist):
        #from here the code of merging follows
        
        a=finallist[lefti]
        b=finallist[righti]
##        print(a)
##        print(b)
        x=[]
        for z in a:
                x.append(z[1])
               
        y=[]
        for z in b:
                y.append(z[1])
        common=sorted(list(set(x) & set(y)))
        ##        print(a)
        ##        print(b)
        ##        print(x)
        ##        print(y)
        ##        print(common)
        fa=[]
        fb=[]
        j=0
        ll=[]
        uncommon=[]
        for i in range(len(common)):
                while ((a[j][1])!=common[i]):
                        uncommon.append(a[j])
                        j=j+1
                fa.append(a[j][0])
        j=0
        for i in range(len(common)):
                while ((b[j][1])!=common[i]):
                        uncommon.append(b[j])
                        j=j+1
                fb.append(b[j][0])
        for i in range(len(fa)):
                ll.append((fa[i]+fb[i])/2)
        k=len(fa)
        nn=[]
        thresh=20
        for i in range(0,k):
              nn.append([ll[i],common[i]])
        nn=sorted(nn, key=lambda student: student[0],reverse=True)
##        print(nn)
        if k>=thresh:
                nn=nn[0:thresh]
        else:
                uncommon=sorted(uncommon, key=lambda student: student[0],reverse=True)
                nn+=uncommon[0:thresh-k]
                
        nn=sorted(nn, key=lambda student: student[1])
##        print(nn)
##        print(finallist)
        finallist[lefti]=nn
        finallist.pop(righti)
##        print(finallist)

        self.left = clusters[lefti]
        self.right = clusters[righti]
        # merge columns grid[row][righti] and row grid[righti] into corresponding lefti
##        for r in grid:
##            r[lefti] = min(r[lefti], r.pop(righti))
##        grid[lefti] = list(map(min, zip(grid[lefti], grid.pop(righti))))
        grid=[]
        for d1 in finallist:
                row=[]
                for d2 in finallist:
                      row.append(similarity_measure(d1,d2))
                grid.append(row)
        clusters.pop(righti)
        return (clusters, grid,finallist)

def agglomerate(labels, grid,finallist):
    """
    given a list of labels and a 2-D grid of distances, iteratively agglomerate
    hierarchical Cluster
    """
    clusters = labels
    while len(clusters) > 1:
        # find 2 closest clusters
        print("\nThe current clusters are :")
        print(clusters)
        print()
        distances = list()
        
        for i in range(1,len(grid)):
                        for j in range(0,i):
                            distances += [(i, j, grid[i][j])]
            
        j,i,_ = min(distances, key=lambda x:x[2])
        print("Now cluster #"+(str)(i+1)+" and #"+(str)(j+1)+" from the above set will be merged")
        print("Similarity Measure found--> "+(str)(_))
        
        # merge i<-j
        c = Cluster()
        clusters, grid ,finallist= c.add(clusters, grid, i, j,finallist)
        clusters[i] = c
##        print()
##        print(grid)
    return clusters.pop()

if __name__ == '__main__':

    sys.stdout = open("H:/ml project/out.txt", "w")

    path_wfv = 'H:/ml project/wfv'
    mainlist = []
    for filename in os.listdir(path_wfv):
            templist = []
            with open(path_wfv+'/'+filename, 'r') as inf:
                    for line in inf:
                            #print(type(line))
                            line = line.replace(')','')
                            line = line.replace('(','')
                            line = line.replace('\n','')
                            line = line.replace("'",'')
                            line = line.replace(",",'')
                            line=line.split()
                            templist.append([(float)(line[0]),line[1]])
                    mainlist.append(templist)
    #print(mainlist)

    ##for doc in mainlist:
    ##        print('Document--->')
    ##        for f in doc:
    ##                print(f)
    finallist=[]
    for doc in mainlist:
            doc=sorted(doc, key=lambda student: student[1])
            finallist.append(doc)

    #print(finallist)
    grid=[]
    for d1 in finallist:
            row=[]
            for d2 in finallist:
                row.append(similarity_measure(d1,d2))
            grid.append(row)
    #print(grid)
    
    labels = list(range(1,len(finallist)+1))
    #print(labels)
    #print(len(finallist))
##    print(grid)
##    print()
    print(agglomerate(labels, grid,finallist))


