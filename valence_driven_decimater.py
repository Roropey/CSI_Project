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

    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
        self.list_removed = []
    
    def find_the_gate(self, vertice_center,current_gate, init_gate = None):
        """
        Recursive function to find gates when the front vertex is to be removed.

        Parameters:
        - vertice_center: The front vertex of the current gate.
        - current_gate: The current gate being explored.
        - init_gate: The initial gate used as a reference to stop the recursion.

        """
        
        # Set the initial gate
        if init_gate is None:
            init_gate = current_gate.copy() 

        # find the next_gate
        gate_face = self.gate_to_face(vertice_center, current_gate[1])
        new_gate = gate_face[2:]

        # Check if the vertices of the new gate have state 2 and if it is different from the initial gate
        if new_gate[0].state != 2 and new_gate[1].state != 2 and init_gate != new_gate : 
            new_gate[0].state = 2 
            new_gate[1].state = 2
            self.gate.append(new_gate)

        # Check if the new gate is different from the initial gate to avoid infinite recursion
        if init_gate != new_gate:
            self.find_the_gate(vertice_center,new_gate, init_gate)



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
    
    def cleaning_conquest(self):
        val_output = []

        # inititialisation 
        index_init = random.randint(0, len(self.faces)) # random index for faces
        faces_init = self.faces[index_init]

        init_gate = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
        self.gate(init_gate)


        

        while len(self.gate) != 0:

            c_gate = self.gate.popleft()

            # search for the front face information
            front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
            front_vertex = front_face_information[3]
            front_face = self.faces[front_face_information[0]]
            if len(front_vertex.faces) == 3:
                val_output.append(3)

                 # The front face is flagged to be removed
                front_face.state = 3

                # creates the 2 new gate 
                new_gates = [[front_face_information[2:]],[front_face_information[3,1]]]

                # add the gates to the fifo
                for gate in new_gates:
                    gate[0].state = 2 
                    gate[1].state = 2
                    self.gate.append(gate)



            else :
                val_output.append("Null_patch")
                 # The front face is flagged conquered
                front_face.state = 2

                # creates the 2 new gate 
                new_gates = [[front_face_information[2:]],[front_face_information[3,1]]]

                # add the gates to the fifo
                for gate in new_gates:
                    gate[0].state = 2 
                    gate[1].state = 2

                self.find_the_gate( vertice_center,new_gates[0], init_gate = None)
                self.find_the_gate( vertice_center,new_gates[1], init_gate = None)

                

        

    


    
    def decimating_conquest(self):

        c_gate = self.gate.popleft()

        # search for the front face information
        front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
        front_vertex = front_face_information[3]
        front_face = self.faces[front_face_information[0]]


        # if its front face is tagged conquered or to be removed
        if front_face == 2 or front_face == 3:
            return None

        #elif the front vertex is free and has a valence <= 6
        elif front_vertex.state == 1 and len(front_vertex.faces)<=6:

            # The front vertex is flagged to be removed and its incident faces are flagged to be removed.
            front_vertex.state = 3
            for i in front_vertex.faces:
                self.faces[i].state = 3
            

            # search for the gates and the front vertex neighboring vertices are flagged conquered
            self.find_the_gate(front_vertex,c_gate)

            return Vertex_removed(front_vertex,c_gate)
        
        
        # else, (if its front vertex is free and has a valence > 6) or (if its front vertex is tagged conquered)
        elif (front_vertex.state == 1 and len(front_vertex.faces)>6) or front_vertex.state == 2 :
            # The front face is flagged conquered
            front_face.state = 2

            # creates the 2 new gate 
            new_gates = [[front_face_information[2:]],[front_face_information[3,1]]]

            # add the gates to the fifo
            for gate in new_gates:
                gate[0].state = 2 
                gate[1].state = 2
                self.gate.append(gate)


            #il faudrait voir comment implémenter le cas Null_patch dans vertex_removed
            return "Null_patch"
        
        raise Exception("Error in the decimating conquest")
        
        



    def decimateA(self, output):
        # inititialisation 
        index_init = random.randint(0, len(self.faces)) # random index for faces
        faces_init = self.faces[index_init]

        c_gate = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
        self.gate(c_gate)
        
        vertex_remove = self.decimating_conquest()
        if vertex_remove == "Null_patch":
            print("todo")
        
        elif vertex_remove :
            print("todo")
            # do the retriangulation
            
    def recreate_faces(self,indices):
        face = obja.Face.from_array(indices)
        face.test(self.vertices, self.line)
        self.memorize_face(face)

           
 
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
            # Therefore, the border_patch is required to have two more
            raise Exception("Unexpected valence or border_patch size (!=)")
        else:
            border_patch.remove(-1) # remove the right gate vertex last adding
            border_patch.remove(-1) # remove the left gate vertex last adding
        
        match vertex_to_be_removed.valence:
            case 3:
                print("Valence of 3")
                # Assigning retriangulation types
                if (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=1
                elif (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                else : raise Exception("Unexpected retriangulation_type for gate vertices")  
                # Creating faces
                self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                
            case 4:
                print("Valence of 4")
                if (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[3].index])

                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                    border_patch[3].retriangulation_type=1
                    #Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[3].index])
                    self.recreate_faces([border_patch[1].index,border_patch[2].index,border_patch[3].index])            

                elif (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                    border_patch[3].retriangulation_type=1
                    #Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[3].index])
                    self.recreate_faces([border_patch[1].index,border_patch[2].index,border_patch[3].index])
                    
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[3].index])
                    
                else : raise Exception("Unexpected retriangulation_type for gate vertices")    

            case 5:
                print("Valence of 5")
                if (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    border_patch[4].retriangulation_type=1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[4].index])
                    self.recreate_faces([border_patch[2].index,border_patch[3].index,border_patch[4].index])

                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    border_patch[4].retriangulation_type=1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])                   
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[4].index])
                    self.recreate_faces([border_patch[2].index,border_patch[3].index,border_patch[4].index])

                elif (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                    border_patch[3].retriangulation_type=1
                    border_patch[4].retriangulation_type=-1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[3].index])                 
                    self.recreate_faces([border_patch[1].index,border_patch[2].index,border_patch[3].index])
                    self.recreate_faces([border_patch[3].index,border_patch[4].index,border_patch[0].index])
                    
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    border_patch[4].retriangulation_type=1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[4].index])
                    self.recreate_faces([border_patch[2].index,border_patch[3].index,border_patch[4].index])

                else : raise Exception("Unexpected retriangulation_type for gate vertices") 
                
            case 6:
                print("Valence of 6")
                if (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    border_patch[4].retriangulation_type=1
                    border_patch[5].retriangulation_type=-1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[4].index])
                    self.recreate_faces([border_patch[0].index,border_patch[4].index,border_patch[5].index])
                    self.recreate_faces([border_patch[2].index,border_patch[3].index,border_patch[4].index])
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                    border_patch[3].retriangulation_type=1
                    border_patch[4].retriangulation_type=-1
                    border_patch[5].retriangulation_type=1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[5].index])
                    self.recreate_faces([border_patch[1].index,border_patch[2].index,border_patch[3].index])
                    self.recreate_faces([border_patch[1].index,border_patch[3].index,border_patch[5].index])
                    self.recreate_faces([border_patch[3].index,border_patch[4].index,border_patch[5].index])
                elif (border_patch[0].retriangulation_type==1) and (border_patch[1].retriangulation_type==1):
                    border_patch[2].retriangulation_type=-1
                    border_patch[3].retriangulation_type=1
                    border_patch[4].retriangulation_type=-1
                    border_patch[5].retriangulation_type=1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[5].index])
                    self.recreate_faces([border_patch[1].index,border_patch[2].index,border_patch[3].index])
                    self.recreate_faces([border_patch[1].index,border_patch[3].index,border_patch[5].index])
                    self.recreate_faces([border_patch[3].index,border_patch[4].index,border_patch[5].index])
                elif (border_patch[0].retriangulation_type==-1) and (border_patch[1].retriangulation_type==-1):
                    border_patch[2].retriangulation_type=1
                    border_patch[3].retriangulation_type=-1
                    border_patch[4].retriangulation_type=1
                    border_patch[5].retriangulation_type=-1
                    # Create faces
                    self.recreate_faces([border_patch[0].index,border_patch[1].index,border_patch[2].index])
                    self.recreate_faces([border_patch[0].index,border_patch[2].index,border_patch[4].index])
                    self.recreate_faces([border_patch[0].index,border_patch[4].index,border_patch[5].index])
                    self.recreate_faces([border_patch[2].index,border_patch[3].index,border_patch[4].index])
                else : raise Exception("Unexpected retriangulation_type for gate vertices")
            case _:
                raise Exception("Unexpected valence (<3 or >6)")  
        # TO DO : create the if statements depending the + and - for attributing + and - and creating face (create a Face object and use memorize_face of Model for adding it in the model)        


def obj_to_obja(model_obj,output_name):
    # Open the output file
    with open(output_name, 'w') as output:
        # Create obja object
        output_model = obja.Output(output, random_color=False)
        # First put all vertex present
        index_vertex_created = []
        for vertex in model_obj.vertices:
            # A vertex removed is a vertex with no connection (no faces)
            if not(vertex.faces):
                continue
            elif len(vertex.faces) < 3:
                raise Exception("Valence of vertex of index {} wrong (<3)".format(vertex.index))
            else:
                output_model.add_vertex(vertex.index, vertex.coordinates)
                index_vertex_created.append(vertex.index)

        for index_face in range(len(model_obj.faces)):
            face = model_obj.faces[index_face]
            # A face removed is a not visible face
            if not(face.visible):
                continue
            if not(face.a) in index_vertex_created:
                raise Exception('Vertex a of index {} not present in face of index {}'.format(face.a, index_face))
            elif not(face.b) in index_vertex_created:
                raise Exception('Vertex b of index {} not present in face of index {}'.format(face.b, index_face))
            elif not(face.c) in index_vertex_created:
                raise Exception('Vertex c of index {} not present in face of index {}'.format(face.c, index_face))
            else:
                output_model.add_face(index_face, face)




       

def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/suzanne.obj')
    # model.complete_model()
    model.decimateA()


if __name__ == '__main__':
    main()
