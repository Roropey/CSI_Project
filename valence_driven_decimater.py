import obja
import numpy as np
import sys
import random
from collections import deque


class Vertex_removed():
    def __init__(self,index,valence,coordinates,index_vertex1_of_gate,index_vertex2_of_gate):
        self.index = index
        self.valence = valence
        self.coordinates = coordinates
        self.gate = [index_vertex1_of_gate,index_vertex2_of_gate]
    def __init__(self,vertex,gate):
        self.index = vertex.index
        self.valence = len(vertex.faces)
        self.coordinates = vertex.coordinates
        self.gate = [gate[0].index,gate[1].index]

        
class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
        self.list_removed = []
    
    def find_the_gate(self, vertice_center,c_gate, init_gate = []):
        if init_gate != c_gate:
            if init_gate == []:
                init_gate = c_gate 

            for f in vertice_center.faces:
                face = [self.vertices[f.a],self.vertices[f.b],self.vertices[f.c]]
                if c_gate[0] in face and c_gate[1] in face and not vertice_center.index in face:
                    a = face.index(c_gate[1])
                    nv_gate = [self.vertices[f[a]],self.vertices[f[a+1]]] 
                    if nv_gate[0].state != 2 and nv_gate[1].state != 2 : 
                        nv_gate[0].state = 2 
                        nv_gate[1].state = 2
                        self.gate.append(nv_gate)

                    self.find_the_gate(vertice_center,nv_gate, init_gate)
    

    def find_the_gate_4_null_path(self, vertice_center,c_gate):

        #Recherche of the gates for the case of null_path
    
        
        # first I search the face corresponding to the gate and the vertice_center
        for f in vertice_center.faces:
            face = [self.vertices[f.a],self.vertices[f.b],self.vertices[f.c]]
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



    def from_gate_to_face(self, gate_vertex1, gate_vertex2):
        # Visit all faces from the 1st vertex to see if any face is shared in the right order with the 2nd vertex
        # Return the face index and the three vertices of the face that have the gate
        for index_face in gate_vertex1.faces:
            if self.faces[index_face].a == gate_vertex1.index and self.face[index_face].b == gate_vertex2.index :
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].c]]
            elif self.face[index_face].b == gate_vertex1.index and self.face[index_face].c == gate_vertex2.index:
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].a]]
            elif self.face[index_face].c == gate_vertex1.index and self.face[index_face].a == gate_vertex2.index:
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].b]]
                
        raise Exception("The two vertex given doesn't correspond to a gate.")

    


    
    def decimating_conquest(self):

        c_gate = self.gate.popleft()

        # search for the front vertex
        front_vertex = self.from_gate_to_face(c_gate[0], c_gate[1])[3]
        
        
        #if the front vertex is free and has a valence <= 6
        if front_vertex.state == 1 and len(front_vertex.faces)<=6:
            self.find_the_gate(front_vertex,c_gate)
            front_vertex.state = 3
            return Vertex_removed(front_vertex,c_gate)
        
        # else, (if its front vertex is free and has a valence > 6) or (if its front vertex is tagged conquered)
        elif (front_vertex.state == 1 and len(front_vertex.faces)>6) or front_vertex.state == 2 :
            self.find_the_gate_4_null_path(front_vertex,c_gate)
            return None
        
        # else if the front face is tagged conquered or to be removed
        else :
            return None



    def decimateA(self, output):
        # inititialisation 
        index_init = random.randint(0, len(self.faces)) # random index for faces
        faces_init = self.faces[index_init]

        c_gate = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
        self.gate(c_gate)
        
        vertex_remove = self.decimating_conquest()
        if vertex_remove != None:
            # do the retriangulation
            
        
           
"""
    def retriangulation(current_gate)

"""



       

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
