import scipy.sparse as sparse
from scipy.sparse import coo_matrix, linalg
import numpy as np
import sys
import gmsh
import matplotlib.pylab as plt
import matplotlib.cm as cm

from assemblage import *
from maillage import Point, Segment, Triangle, Mesh  

#Données
PIECE=1
MUR=1
RADIATEUR=2
FENETRE=3

def f(x,y):
    return 0

def dirichlet_fenetre(x,y):
    return -10

def dirichlet_radiateur(x,y):
    return 25

#Initialisation GMSH
m=Mesh()

gmsh.initialize(sys.argv)
model = gmsh.model
model.add("mon_modele")

m.GmshToMesh(filename="mesh_pb.msh")
t=Triplet()

#Calcul du membre de gauche
# Pas de masse comme c=0 ici
# Mass(m,dim=2,physical_tag=PIECE,triplets=t)
Rigidite(m,dim=2,physical_tag=PIECE,triplets=t)

b=np.zeros(m.Npts)
Dirichlet(m,1,RADIATEUR,dirichlet_radiateur,t,b)
Dirichlet(m,1,FENETRE,dirichlet_fenetre,t,b)

#Calcul du membre de droite
Integrale(m,2,PIECE,f,b,2)

# Résolution
A = (coo_matrix(t.data)).tocsr()
U = linalg.spsolve(A, b)

# Visualisation
x = [pt.x for pt in m.Points]
y = [pt.y for pt in m.Points]
connectivity=[]
for tri in m.Triangles:
  connectivity.append([p.id for p in tri.points])

cmap = cm.get_cmap(name='coolwarm', lut=None)
plt.tricontourf(x, y, connectivity, U, cmap=cmap)
plt.colorbar()
plt.show()


gmsh.finalize()
