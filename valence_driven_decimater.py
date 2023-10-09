import obja
import numpy as np
import sys
import random
from collections import deque

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
    
    def find_the_gate(self, vertice_center,c_gate, init_gate = []):
        if init_gate != c_gate:
            if init_gate == []:
                init_gate = c_gate 

            for f in vertice_center.faces:
                face = [f.a,f.b,f.c]
                if c_gate[0] in face and c_gate[1] in face and not vertice_center.index in face:
                    a = face.index(c_gate[1])
                    nv_gate = [f[a],f[a+1]] 
                    if nv_gate[0].state != 2 and nv_gate[1].state != 2 : 
                        nv_gate[0].state = 2 
                        nv_gate[1].state = 2
                        self.gate.append(nv_gate)

                    self.find_the_gate(vertice_center,nv_gate, init_gate)
    

    def find_the_gate_4_null_path(self, vertice_center,c_gate):

        for f in vertice_center.faces:
            face = [f.a,f.b,f.c]
            if c_gate[0] in face and c_gate[1] in face and vertice_center.index in face:
                nv_gate = [c_gate[1],vertice_center] 
                if nv_gate[0].state != 2 and nv_gate[1].state != 2 : 
                    nv_gate[0].state = 2 
                    nv_gate[1].state = 2
                    self.gate.append(nv_gate)
                    
                nv_gate = [c_gate[0],vertice_center] 
                if nv_gate[0].state != 2 and nv_gate[1].state != 2 : 
                    nv_gate[0].state = 2 
                    nv_gate[1].state = 2
                    self.gate.append(nv_gate)





    def dacimateA(self, output):
        
        print("ok")
        # init
        index_init = random.randint(0, len(self.faces))
        faces_init = self.faces[index_init]

        c_gate = [faces_init.a,faces_init.b]
        for i in range (len(self.faces)) :
            f = self.faces[i]
            ptsf = [f.a,f.b,f.c]
            if i != index_init and (faces_init.a in ptsf and faces_init.b in ptsf):
                if not(f.a in c_gate) :
                     vertice_center = f.a  
                elif not(f.b in c_gate) :
                    vertice_center = f.b 
                else : 
                    vertice_center = f.c

        
        if vertice_center.state == 1 and len(vertice_center.faces)<=6:

            find_the_gate(self, vertice_center,c_gate, init_gate = [])


            vertice_center.state == 3
            for f in vertice_center.faces:
                for i in [f.a,f.b,f.c]:
                    if faces_init.c != i:
                        self.vertices[i].state = 2
            

            

            output_val = len(vertice_center.faces)
        
        elif (vertice_center.state == 1 and len(vertice_center.faces)>6) or vertice_center.state == 2 :
            vertice_center.state == 2



            output_val = "NullPatch"

            




       

def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/suzanne.obj')
    model.complete_model()
    model.decimateA()


if __name__ == '__main__':
    main()
