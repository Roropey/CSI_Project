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



    def gate_to_face(self, gate_vertex1, gate_vertex2):
        # Visit all faces from the 1st vertex to see if any face is shared in the right order with the 2nd vertex
        # Return the face index and the three vertices of the face that have the gate
        for index_face in gate_vertex1.faces:
            if self.faces[index_face].a == gate_vertex1.index and self.faces[index_face].b == gate_vertex2.index :
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].c]]
            elif self.faces[index_face].b == gate_vertex1.index and self.faces[index_face].c == gate_vertex2.index:
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].a]]
            elif self.faces[index_face].c == gate_vertex1.index and self.faces[index_face].a == gate_vertex2.index:
                return [index_face,gate_vertex1,gate_vertex2,self.vertices[self.faces[index_face].b]]
                
        raise Exception("The two vertex given doesn't correspond to a gate.")

    


    
    def decimating_conquest(self):

        c_gate = self.gate.popleft()

        # search for the front vertex
        front_vertex = self.gate_to_face(c_gate[0], c_gate[1])[3]
        
        
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
            
        
           

    def retriangulation(self,vertex_to_be_removed):
        border_patch = vertex_to_be_removed.gate.copy() # List of all vertices around the vertex to be removed
        vertex_infos = self.vertices[vertex_to_be_removed.index]    # A variable to access directly info to avoid too much code
        while vertex_infos.faces:   # While there is faces to be removed from the "vertex to be removed", we search them
            Advance = False
            for index_face in vertex_infos.faces:   # Visit all faces of the vertex to be removed to see if any face correspond to the next in the chain around
                # Normally with the order of face to be removed should be in the counterclock order, starting with the face next to the gate face
                # The gate face should be the last one to be removed
                # If any face having the center following by the last adding into the chain as a "gate", then this is the next face, and so the third vertex the next vertex in the chain
                # Knowing the chain order is required because removing faces will loose the patch organization information and so we need to memorize it for the retriangulation
                # When found, added the vertex and remove the face, we break the for loop to research again if required
                if self.faces[index_face].a == vertex_to_be_removed.index and self.faces[index_face].b == border_patch[-1]:
                    border_patch.append(self.faces[index_face].c)
                    self.remove_face(index_face)
                    break 
                elif self.faces[index_face].b == vertex_to_be_removed.index and self.faces[index_face].c == border_patch[-1]:
                    border_patch.append(self.faces[index_face].a)
                    self.remove_face(index_face)
                    break
                elif self.faces[index_face].c == vertex_to_be_removed.index and self.faces[index_face].a == border_patch[-1]:
                    border_patch.append(self.faces[index_face].b)
                    self.remove_face(index_face)
                    break

            raise Exception("Not found next vertex in the chain around")
        if len(border_patch) != vertex_to_be_removed.valence + 2:   
            # Through this process, since the gate face will be the last processed, the two vertices of the gates will be added in the chain and so being two time in it
            # (Once added when the left face of the gate face will be removed for the left gate vertex, and once the gate face is removed for the right gate vertex)
            #Therefore, the border_patch is required to have two more
            raise Exception("Unexpected valence or border_patch size (!=)")
        else:
            border_patch.remove(-1) #remove the right gate vertex last adding
            border_patch.remove(-1) #remove the left gate vertex last adding
        
        match vertex_to_be_removed.valence:
            case 3:
                print("Valence of 3")
            case 4:
                print("Valence of 4")
            case 5:
                print("Valence of 5")
            case 6:
                print("Valence of 6")
            case _:
                raise Exception("Unexpected valence (<3 or >6)")  
        # TO DO : create the if statements depending the + and - for attributing + and - and creating face (create a Face object and use memorize_face of Model for adding it in the model)
        #            




       

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
