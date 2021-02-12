from maillage import Point, Segment, Triangle, Mesh
import numpy as np
from scipy.sparse import coo_matrix

def phiRef(element, i:int, param:[float]):
    if element.name=="Triangle":
        if i==0:
            return(1-param[0]-param[1])
        elif i==1:
            return(param[0])
        elif i==2:
            return(param[1])
        else:
            print("Bad i")
            sys.exit(1)
    

def grad_phi(element, i):
    if element.name=="Triangle":
        if i==0:
            return(np.array([-1,-1]))
        elif i==1:
            return(np.array([1,0]))
        elif i==2:
            return(np.array([0,1]))

class Triplet:
    def __init__(self):
        self.data = ([], ([], []))
    def __str__(self):
        return str(self.data)
    def append(self, I, J, val):
        self.data[0].append(val)
        self.data[1][0].append(I)
        self.data[1][1].append(J)
    def at(self, mon_i, mon_j):
        return(coo_matrix(self.data).toarray()[mon_i][mon_j])
        
def mass_elem(element, triplets, alpha =1.):
    if element.name=="Triangle":
        coef = element.area()
        coef *= 1/12
        coef *= alpha
        triplets.append(0,0,coef*2.)
        triplets.append(1,1,coef*2.)
        triplets.append(2,2,coef*2.)
        triplets.append(0,1,coef)
        triplets.append(0,2,coef)
        triplets.append(1,0,coef)
        triplets.append(1,2,coef)
        triplets.append(2,0,coef)
        triplets.append(2,1,coef)
    return triplets

def rigidite_elem(element, triplets, alpha =1.):
    if element.name=="Triangle":
        coef = element.area()
        Bp=element.Bp()
        for i in range(3):
            for j in range(3):
                res = grad_phi(element,j)
                res = np.matmul(res,np.transpose(Bp))
                res = np.matmul(res,Bp)
                res = np.matmul(res,np.transpose(grad_phi(element,i)))
                triplets.append(i,j,coef*res)
    return triplets

def Mass(msh, dim, physical_tag, triplets):
    elements=msh.getElements(dim,physical_tag)
    print("[ASSEMBLAGE] Remplissage de la matrice de masse")
    for p in range(len(elements)):
        matrice_locale=Triplet()
        matrice_locale = mass_elem(msh.Triangles[p],matrice_locale)
        for i in range(3):
            I = msh.Loc2Glob(p, i);
            for j in range(3):
                J = msh.Loc2Glob(p,j)
                triplets.append(I, J, matrice_locale.at(i,j))
    return triplets

def Rigidite(msh, dim, physical_tag, triplets):
    elements=msh.getElements(dim,physical_tag)
    print("[ASSEMBLAGE] Remplissage de la matrice de rigidité")
    for p in range(len(elements)):
        matrice_locale=Triplet()
        matrice_locale = rigidite_elem(msh.Triangles[p],matrice_locale)
        for i in range(3):
            I = msh.Loc2Glob(p, i);
            for j in range(3):
                J = msh.Loc2Glob(p,j)
                triplets.append(I, J, matrice_locale.at(i,j))
    return triplets

def Integrale(msh:Mesh, dim:int, physical_tag:int, f, B:np.array, order=2):
    M=3 if order==2 else 1
    elements=msh.getElements(dim,physical_tag)
    print("[ASSEMBLAGE] Calcul des quadratures")
    for p,elem in enumerate(elements):
        omega,c_param,c_phys=elem.gaussPoint(order)
        coef=elem.jac()
        for i in range(3):
            I=msh.Loc2Glob(p,i)
            for m in range(M):
                B[I]+=coef*omega[m]*f(c_phys[m][0],c_phys[m][1])*phiRef(elem,i,c_param[m])

def Dirichlet(msh, dim, physical_tag, g, triplets, B):
    points=msh.getPoints(dim,physical_tag)
    print("[ASSEMBLAGE] Application de la condition de Dirichlet pour le physical_tag "+str(physical_tag))
    for p in points:
        I=p.id
        for indice in range(len(triplets.data[0])):
            if triplets.data[1][0][indice]==I:
                triplets.data[0][indice]=0
        triplets.append(I,I,1)
        B[I]=g(p.x,p.y)
    return
