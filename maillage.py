import itertools
import gmsh
import numpy as np


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

def psiRef(element, i:int, param:[float]):
    return(phiRef(element,i,param))    

class Point():
    id_iter = itertools.count()
    def __init__(self,x,y):
        self.id=next(Point.id_iter)
        self.x=x
        self.y=y

class Segment():
    id_iter = itertools.count()
    def __init__(self,a,b,tag=-1):
        self.id=next(Segment.id_iter)
        self.points=[a,b]
        self.tag=tag
        self.name="Segment"
        x1=self.points[0].x
        x2=self.points[1].x
        y1=self.points[0].y
        y2=self.points[1].y
        self._area=np.sqrt((x1-x2)**2+(y1-y2)**2)
    def area(self):
        return(self._area)
    def jac(self):
        return(self._area)
    def gaussPoint(self,order=2):
        pass
        
class Triangle():
    id_iter = itertools.count()
    def __init__(self,a,b,c,tag=-1):
        self.id=next(Triangle.id_iter)
        self.points=[a,b,c]
        self.tag=tag
        self.name="Triangle"
        x0=self.points[0].x
        x1=self.points[1].x
        x2=self.points[2].x
        y0=self.points[0].y
        y1=self.points[1].y
        y2=self.points[2].y
        self._area=1/2*abs((x1-x0)*(y2-y0)-(x2-x0)*(y1-y0))
        self._intermediaire=np.array([[y2-y0,y0-y1],[x0-x2,x1-x0]])
    def area(self):
        return(self._area)
    def jac(self):
        return(2*self._area)
    def Bp(self):
        return((1/self.jac())*self._intermediaire)
    def gaussPoint(self,order=2):
        if order==1:
            poids=[1/6]
            coord_param=[[1/3,1/3]]
        elif order==2:
            poids=[1/6,1/6,1/6]
            coord_param=[[1/6,1/6],[4/6,1/6],[1/6,4/6]]
        else:
            print("Bad order")
            sys.exit(1)
        coord_phys=[]
        for j in range(len(coord_param)):
            coord_x=sum([psiRef(self,i,coord_param[j])*self.points[i].x for i in range(3)])
            coord_y=sum([psiRef(self,i,coord_param[j])*self.points[i].y for i in range(3)])
            coord_phys.append([coord_x,coord_y])
        return(poids,coord_param,coord_phys)

class Mesh():
    def __init__(self):
        self.Points = []
        self.Segments = []
        self.Triangles = []
    def getElements(self, dim, physical_tag):
        if(dim==1):
            return([i for i in self.Segments if i.tag==physical_tag])
        elif(dim==2):
            return([i for i in self.Triangles if i.tag==physical_tag])
        else:
            print("Bad dimension")
            sys.exit(1)
    def getPoints(self, dim, physical_tag):
        Points=[]
        for elem in self.getElements(dim,physical_tag):
            Points+=[i for i in elem.points]
        return list(set(Points))
    def GmshToMesh(self,h=0.08,filename=""):
        if filename:
            gmsh.open(filename)
        else :
            #mesh par defaut
            gmsh.model.geo.addPoint(0,0,0,h,1);
            gmsh.model.geo.addPoint(0,1,0,h,2);
            gmsh.model.geo.addPoint(1,1,0,h,3);
            gmsh.model.geo.addPoint(1,0,0,h,4);
            gmsh.model.geo.addLine(1,2);
            gmsh.model.geo.addLine(2,3);
            gmsh.model.geo.addLine(3,4);
            gmsh.model.geo.addLine(4,1);
            gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
            gmsh.model.geo.addPlaneSurface([1],1)
            gmsh.model.geo.addPhysicalGroup(1, [1,2,3,4], 7)
            gmsh.model.geo.addPhysicalGroup(2, [1], 5)
            gmsh.model.geo.synchronize()
            gmsh.model.mesh.generate(2)
        #Points
        res=gmsh.model.mesh.getNodes()
        X=np.array([res[1][i] for i in range(0,len(res[1]),3)])
        Y=np.array([res[1][i] for i in range(1,len(res[1]),3)])
        for i in range(len(X)):
            p=Point(X[i],Y[i])
            self.Points.append(p)
        self.Npts=len(self.Points)
        #Entites
        phys_groups=gmsh.model.getPhysicalGroups()
        for (dim,tag) in phys_groups:
            ids_gmsh=gmsh.model.getEntitiesForPhysicalGroup(dim,tag)
            if dim==1:
                #segments
                for id_gmsh in ids_gmsh:
                    res=gmsh.model.mesh.getElements(dim,id_gmsh)
                    ids_segments=res[1][0]
                    points_segments=res[2][0]
                    A=[self.Points[int(points_segments[i])-1] for i in range(0,len(points_segments),2)]
                    B=[self.Points[int(points_segments[i])-1] for i in range(1,len(points_segments),2)]
                    for i in range(len(ids_segments)):
                        s=Segment(A[i],B[i],tag)
                        self.Segments.append(s)
            elif dim==2:
                #triangles
                for id_gmsh in ids_gmsh:
                    res=gmsh.model.mesh.getElements(dim,id_gmsh)
                    ids_triangles=res[1][0]
                    points_triangles=res[2][0]
                    A=[self.Points[int(points_triangles[i])-1] for i in range(0,len(points_triangles),3)]
                    B=[self.Points[int(points_triangles[i])-1] for i in range(1,len(points_triangles),3)]
                    C=[self.Points[int(points_triangles[i])-1] for i in range(2,len(points_triangles),3)]
                    for i in range(len(ids_triangles)):
                        t=Triangle(A[i],B[i],C[i],tag)
                        self.Triangles.append(t)
    def Loc2Glob(self,p,i):
        return(self.Triangles[p].points[i].id)
