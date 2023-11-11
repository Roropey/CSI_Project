import obja
import numpy as np
import sys
import random
from collections import deque
from reconstruction import Reconstructer
from utility import limit_value


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
    
class Decimating_output():
    def __init__(self,init_gate_decimating,init_gate_cleaning,output_val_A,output_val_B):
        self.init_gate_decimating = init_gate_decimating
        self.init_gate_cleaning = init_gate_cleaning
        self.output_val_A = output_val_A
        self.output_val_B = output_val_B
        


        
class Decimater(obja.Model):
    """

    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
        self.list_removed = []
        self.random_seed = 0
        self.count = 0

    def print_gate_index(self):
        print("List index vertices on gates: ", end="")
        for gate in self.gate:
            print("({},{}) ".format(gate[0].index,gate[1].index),end="")
        print()

    def increase_rd_seed(self):        
        self.random_seed += 1
        random.seed(self.random_seed)
         
    
    def decimating_conquest(self):
        c_gate = self.gate.popleft()
        
        
        # search for the front face information
        front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
        front_vertex = front_face_information[3]
        front_face = self.faces[front_face_information[0]]
        #print("Gate analyzed: ({},{})\nVertex possibly removed {}\nFace index possibly removed: {}".format(c_gate[0].index,c_gate[1].index,front_vertex.index,front_face_information[0]))
        # if its front face is tagged conquered or to be removed
        if front_face.state == obja.State.Conquered or front_face.state == obja.State.To_be_removed:
            #print("Tagged conquered or to be removed")
            return None


        #elif the front vertex is free and has a valence <= 6
        elif front_vertex.state == obja.State.Free and len(front_vertex.faces)<=6:
            #print("Free and <=6")
            # The front vertex is flagged to be removed and its incident faces are flagged to be removed.
            front_vertex.state = obja.State.To_be_removed
            for i in front_vertex.faces:
                self.faces[i].state = obja.State.To_be_removed
            

            # search for the gates and the front vertex neighboring vertices are flagged conquered
            self.find_the_gate(front_vertex,c_gate)
            return Vertex_removed(front_vertex,c_gate)
        
        
        # else, (if its front vertex is free and has a valence > 6) or (if its front vertex is tagged conquered)
        elif (front_vertex.state == obja.State.Free and len(front_vertex.faces)>6) or front_vertex.state == obja.State.Conquered :
            #print("(free and >6) or (vertex conquered)")
            # The front face is flagged conquered
            front_face.state = obja.State.Conquered

            # creates the 2 new gate 
            new_gates = [front_face_information[2:],[front_face_information[3],front_face_information[1]]]

            # add the gates to the fifo
            for gate in new_gates:
                gate[0].state = obja.State.Conquered 
                gate[1].state = obja.State.Conquered
                self.gate.append(gate)


            #il faudrait voir comment implémenter le cas Null_patch dans vertex_removed
            return "Null_patch"
        else:

            raise Exception("Error in the decimating conquest")
    

    def cleaning_conquest(self):

    #Cleaning Conquest function for removing redundant vertices and faces in a triangle mesh.

    # Cleaning Conquest is a series of operations performed after removing redundant vertices in a triangle mesh.
    #Its main goal is to ensure that the simplified mesh maintains validity and reasonable topological structure.

    #Parameters:
    #- self: Decimater object containing the triangle mesh model and related data.

    #Returns:

  
        c_gate = self.gate.popleft()
        #print("gate 1: {}, gate 2: {}".format(c_gate[0].index,c_gate[1].index))
        # Find information about the front face
        front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
        #self.print_single_face(front_face_information[0])
        front_vertex = front_face_information[3]
        front_face = self.faces[front_face_information[0]]
        
        self.coloring_vertex_all_similar([0.5,0.5,0.5])
        c_gate[0].coloring_vertex([0,1,0])
        c_gate[1].coloring_vertex([0,0,1])
        front_face_information[3].coloring_vertex([1,0,0])        
        self.save_f_by_f('Results_tests/gate_cleaning_conquest_{}.obj'.format(self.count))

        self.save_selected_f('Results_tests/face_cleaning_conquest_{}.obj'.format(self.count),
                             [front_face_information[0]])
        self.count += 1
        #print("Front face state:{}".format(front_face.state))
        # if its front face is tagged conquered or to be removed
        if front_face.state == obja.State.Conquered or front_face.state == obja.State.To_be_removed:
            return None


        elif len(front_vertex.faces) == 3 and front_vertex.state == obja.State.Free   :

            # Mark the front face for removal
            front_face.state = obja.State.To_be_removed
            
            # find the edge of the patch
            face_up_right = self.gate_to_face(front_vertex,c_gate[1])
            face_up_left = self.gate_to_face(front_vertex, face_up_right[3])

            # Mark the other face for removal
            self.faces[face_up_right[0]].state = obja.State.To_be_removed
            self.faces[face_up_left[0]].state = obja.State.To_be_removed

            # Create two intermediare gates
            intermediaire_gates = [ [face_up_right[3], c_gate[1]] , [face_up_left[3], face_up_right[3]] ]

            # find the other gates 
            for gate in intermediaire_gates:
                gate[0].state = obja.State.Conquered
                gate[1].state = obja.State.Conquered
                f = self.gate_to_face(gate[0],gate[1])

                # Create the two new gates
                new_gates = [[f[3],f[2]], [f[1], f[3]]]

                # Add the new gates to the queue
                for gate in new_gates:
                    gate[0].state = obja.State.Conquered
                    gate[1].state = obja.State.Conquered
                    self.gate.append(gate)
                self.faces[f[0]].state = obja.State.Conquered
            
            front_vertex.state = obja.State.To_be_removed
            return Vertex_removed(front_vertex,c_gate)

        elif front_vertex.state == obja.State.Free or front_vertex.state == obja.State.Conquered :
            
            # Mark the front face as conquered
            front_face.state = obja.State.Conquered

            # Create two new gates
            new_gates = [[front_face_information[3],front_face_information[2]], [front_face_information[1],front_face_information[3]]]

            # Add the new gates to the queue
            for gate in new_gates:
                gate[0].state = obja.State.Conquered
                gate[1].state = obja.State.Conquered
                self.gate.append(gate)

            return "Null_patch"



    def retriangulation_4_cleaning_conquest(self,vertex_to_be_removed):
        #print("Vertex to be removed: {}".format(vertex_to_be_removed.index))
        border_patch = vertex_to_be_removed.gate.copy() # List of all vertices around the vertex to be removed
        vertex_infos = self.vertices[vertex_to_be_removed.index]    # A variable to access directly info to avoid too much code
        while vertex_infos.faces:   # While there is faces to be removed from the "vertex to be removed", we search them
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
            
            #raise Exception("Not found next vertex in the chain around")
        if len(border_patch) != vertex_to_be_removed.valence + 2:   
            # Through this process, since the gate face will be the last processed, the two vertices of the gates will be added in the chain and so being two time in it
            # (Once added when the left face of the gate face will be removed for the left gate vertex, and once the gate face is removed for the right gate vertex)
            # Therefore, the border_patch is required to have two more
            raise Exception("Unexpected valence or border_patch size (!=)")
        else:
            border_patch.pop() # remove the right gate vertex last adding
            border_patch.pop() # remove the left gate vertex last adding


        # Creating faces
        self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
        vertex_infos.visible = False

           
 
    def retriangulation(self,vertex_to_be_removed):
        #print("Vertex to be removed: {}".format(vertex_to_be_removed.index))
        self.save_f_by_f('Results_tests/test1.obj')
        #self.print_single_vertex(vertex_to_be_removed.index)
        #for face in self.vertices[vertex_to_be_removed.index].faces:
        #    self.print_single_face(face)
        border_patch = vertex_to_be_removed.gate.copy() # List of all vertices around the vertex to be removed
        vertex_infos = self.vertices[vertex_to_be_removed.index]    # A variable to access directly info to avoid too much code
        while vertex_infos.faces:   # While there is faces to be removed from the "vertex to be removed", we search them
            not_breaking = True
            for index_face in vertex_infos.faces:   # Visit all faces of the vertex to be removed to see if any face correspond to the next in the chain around
                # Normally with the order of face to be removed should be in the counterclock order, starting with the face next to the gate face
                # The gate face should be the last one to be removed
                # If any face having the center following by the last adding into the chain as a "gate", then this is the next face, and so the third vertex the next vertex in the chain
                # Knowing the chain order is required because removing faces will loose the patch organization information and so we need to memorize it for the retriangulation
                # When found, added the vertex and remove the face, we break the for loop to research again if required
                #print(index_face)
                if self.faces[index_face].a == vertex_to_be_removed.index and self.faces[index_face].b == border_patch[-1]:
                    border_patch.append(self.faces[index_face].c)
                    
                    self.remove_face(index_face)
                    not_breaking = False
                    break 
                elif self.faces[index_face].b == vertex_to_be_removed.index and self.faces[index_face].c == border_patch[-1]:
                    border_patch.append(self.faces[index_face].a)
                    
                    self.remove_face(index_face)
                    not_breaking = False
                    break
                elif self.faces[index_face].c == vertex_to_be_removed.index and self.faces[index_face].a == border_patch[-1]:
                    border_patch.append(self.faces[index_face].b)
                    
                    self.remove_face(index_face)
                    not_breaking = False
                    break
            if not_breaking:
                raise Exception("Not found next vertex in the chain around")
        self.save_f_by_f('Results_tests/test2.obj')
        if len(border_patch) != vertex_to_be_removed.valence + 2:   
            # Through this process, since the gate face will be the last processed, the two vertices of the gates will be added in the chain and so being two time in it
            # (Once added when the left face of the gate face will be removed for the left gate vertex, and once the gate face is removed for the right gate vertex)
            # Therefore, the border_patch is required to have two more
            raise Exception("Unexpected valence or border_patch size (!=)")
        else:
            border_patch.pop() # remove the right gate vertex last adding
            border_patch.pop() # remove the left gate vertex last adding
        
        #print(len(border_patch))
        #for vertex in border_patch:
        #    self.print_single_vertex(vertex)
        
       
        if vertex_to_be_removed.valence == 3:
            #print("Valence of 3")
            # Assigning retriangulation types
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=1
            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
            else : 
                #print(self.vertices[border_patch[0]].retriangulation_type)
                #print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")  
            # Creating faces
            self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
            
        elif vertex_to_be_removed.valence == 4:
            #print("Valence of 4")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                #Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])            

            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                #Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                
            else : raise Exception("Unexpected retriangulation_type for gate vertices")    

        elif vertex_to_be_removed.valence == 5:
            #print("Valence of 5")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.create_face([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[4]].index])                   
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.create_face([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])                 
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.create_face([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[0]].index])
                
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.create_face([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            else : 
                #print("Gate retriangulation type: {} {}".format(self.vertices[border_patch[0]].retriangulation_type, self.vertices[border_patch[1]].retriangulation_type))
                raise Exception("Unexpected retriangulation_type for gate vertices") 
            
        elif vertex_to_be_removed.valence == 6:
            #print("Valence of 6")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                self.vertices[border_patch[5]].retriangulation_type=-1
                
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                self.vertices[border_patch[5]].retriangulation_type=1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                self.vertices[border_patch[5]].retriangulation_type=1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.create_face([self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                self.vertices[border_patch[5]].retriangulation_type=-1
                # Create faces
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.create_face([self.vertices[border_patch[0]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
                self.create_face([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])
            else : raise Exception("Unexpected retriangulation_type for gate vertices")
        else:
            #print()
            raise Exception("Unexpected valence: {} (<3 or >6)".format(vertex_to_be_removed.valence))  
        
        vertex_infos.visible = False
        


    def decimateAB(self):
        # inititialisation 
               
        output_val_A = []
        output_val_B = []
        init_gate_decimating = []
        inds_g = [1,2,3]    # List of integer that determined the choosen gate (will be shuffle)
        save_model = self.clone()
        self.increase_rd_seed()
        ind_4_inds_f = -1   # Index to choose in list of index of faces
        inds_f = random.sample(range(0,len(self.faces)),len(self.faces))   # List of index of faces, generated randomly (random.shuffle doesn't work on range object so use a sample)
        cond_do_decimating = True
        ind_4_inds_g = 0 # Index to choose in list of random integer that determind the gate choosen
        while cond_do_decimating: 
            self.copy(save_model)
            print("Decimating Conquest ",end="")
            cond = ind_4_inds_g != 0 # Condition to find a new face: the index for the gate has made a loop (from 0 to 2)
            while not cond:     #on cherche une face qui est visible
                ind_4_inds_f += 1 # Increasing the index for choosing random index of face
                self.increase_rd_seed() # Modify seed to ensure different shuffle
                random.shuffle(inds_g)  # Shuffling order of gates
                if ind_4_inds_f >= len(self.faces): # If too big, all face index has been tested
                    raise Exception("No faces respect conditions for decimating")
                ind_f = inds_f[ind_4_inds_f]  # Choosing the index of face
                faces_init = self.faces[ind_f] # Take the face
                cond = faces_init.visible           # Condition for decimating: a face that is visible, be present in the model
            ind_g = inds_g[ind_4_inds_g]    # Choose index gate
            if ind_g == 1: # gate will be a and b            
                self.vertices[faces_init.a].retriangulation_type = 1
                self.vertices[faces_init.b].retriangulation_type = -1
                init_gate_decimating = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
            elif ind_g == 2: # gate will be b and c
                self.vertices[faces_init.b].retriangulation_type = 1
                self.vertices[faces_init.c].retriangulation_type = -1
                init_gate_decimating = [self.vertices[faces_init.b],self.vertices[faces_init.c]] # creation of the first gate
            elif ind_g == 3: # gate will be c and a                
                self.vertices[faces_init.c].retriangulation_type = 1
                self.vertices[faces_init.a].retriangulation_type = -1
                init_gate_decimating = [self.vertices[faces_init.c],self.vertices[faces_init.a]] # creation of the first gate
            else:
                raise Exception("Unexpected value for ind_g {}".format(ind_g))

            ind_4_inds_g = limit_value(ind_4_inds_g+1,0,2) # Increasing by one the index for index of gate, but ensuring to stay in border (>2 => =0)
            self.gate.append(init_gate_decimating)

            # decimating_conquest
            while len(self.gate) > 0 :
                print("decimating_conquest ",end="")
                
                c_gate = self.gate[0]
                vertex_remove = self.decimating_conquest()

                if vertex_remove == "Null_patch":
                    output_val_A.append("Null_patch")
                
                elif vertex_remove :
                   
                    output_val_A.append([vertex_remove.valence,vertex_remove.index])
                    self.retriangulation(vertex_remove)
                if self.presence_of_valence_of(2):
                    print("Break")
                    break
            cond_do_decimating = self.presence_of_valence_of(2)
        print()
        
        self.save_f_by_f('Results_tests/After_Decimating_conquest.obj')
        self.set_everything_to_free()
        self.set_everything_to_zeros()
        save_model = self.clone()
        cond_do_cleaning = True
        self.random_seed += 1
        random.seed(self.random_seed)
        ind_4_inds_f = -1
        ind_4_inds_g = 0
        inds_f = random.sample(range(0,len(self.faces)),len(self.faces))
        while cond_do_cleaning:
            output_val_B = []
            self.copy(save_model)
            print("Cleaning Conquest ",end="")
            cond = False
            while not cond:  # on cherche une face qui est visible
                if ind_4_inds_g == 0:
                    ind_4_inds_f += 1
                    if ind_4_inds_f >= len(self.faces):
                        raise Exception("No faces respect conditions for cleaning (ind_4_inds_f: {})".format(ind_4_inds_f))
                
                ind_f = inds_f[ind_4_inds_f]
                faces_init = self.faces[ind_f]
                ind_g = inds_g[ind_4_inds_g] 
                if ind_g == 1: # gate will be a and b            
                    init_gate_cleaning = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
                elif ind_g == 2: # gate will be b and c
                    init_gate_cleaning = [self.vertices[faces_init.b],self.vertices[faces_init.c]] # creation of the first gate
                elif ind_g == 3: # gate will be c and a                
                    init_gate_cleaning = [self.vertices[faces_init.c],self.vertices[faces_init.a]] # creation of the first gate
                else:
                    raise Exception("Unexpected value for ind_g {}".format(ind_g))
                
                ind_4_inds_g = limit_value(ind_4_inds_g+1,0,2)
                if faces_init.visible and not(len(init_gate_cleaning[0].faces) == 3 or len(init_gate_cleaning[1].faces) == 3):
                    cond = True
                
            self.gate.append(init_gate_cleaning)

                
                #self.print_single_face(ind_f)
                
                
            while len(self.gate) > 0 :
                print("cleaning_conquest ",end="")
                
                
                vertex_remove = self.cleaning_conquest()
                    #print("Cleaning passed")
                if vertex_remove == "Null_patch":
                        #print("Is a null patch")
                    output_val_B.append("Null_patch")
                    
                elif vertex_remove :
                        #print("Need to be removed")
                        #print("Vertex to be removed {}".format(vertex_remove.index))
                    output_val_B.append([vertex_remove.valence,vertex_remove.index])
                    self.save_f_by_f('Results_tests/before_cleaning_conquest_{}.obj'.format(self.count))
                    self.retriangulation_4_cleaning_conquest(vertex_remove)

                if self.presence_of_valence_of(2):
                    print("Break")
                    break

            print("\nind_f: {}".format(ind_f))
            cond_do_cleaning = self.presence_of_valence_of(2)
        self.print_count_valencies()
        self.save_f_by_f('Results_tests/After_Cleaning_conquest.obj')
        decimating_output = Decimating_output(init_gate_decimating,init_gate_cleaning,output_val_A,output_val_B)
        return decimating_output
    

    def count_point(self):
        count = 0
        for vertex in self.vertices:
            if vertex.visible:
                count += 1
        return count
        

    def decimate(self,nb_point_end = 15):
        count_iteration = 0
        count_point = self.count_point()
        print("Number of verticies: {}".format(count_point))
        decimating_output = []
        while count_point > nb_point_end:
            count_iteration += 1
            print(f"{count_iteration}ieme decimation")
            decimating_output.append(self.decimateAB())
            self.save_f_by_f(f'Results_tests/Decimate{count_iteration}.obj')
            self.set_everything_to_free()
            self.set_everything_to_zeros()
            count_point = self.count_point()
            print("Number of verticies: {}".format(count_point))
        return decimating_output



def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    #model.parse_file("Test_Objects_low\Icosphere_5&6_valencies.obj")
    model.parse_file('Test_Objects_low/Sphere_4&5&6&7_valencies.obj')
    #model.parse_file('example/suzanne.obj') # Doesn't work because suzanne has valence of 2 since origin
    #model.parse_file('example/fandisk.obj')
    # model.complete_model()
    #model.decimateAB()d
    model.print_count_valencies()
    decimating_output = model.decimate(15)
    
    model.save_f_by_f('Results_tests/DecimateAB_fandisk.obj')


    reco = Reconstructer()
    reco.copy(model)
    reconstruction = reco.reconstruction(decimating_output)


if __name__ == '__main__':
    main()

















# def create_if(self,list_faces):
#         # Function to memorize faces if not existing already (in both direction (ABC and ACB for example))
#         # list_faces: list of Face object already created
#         can_create = True
#         for face_possible in list_faces:
#             points = [face_possible.a,face_possible.b,face_possible.c]
#             for face in self.faces:
#                 if face.visible and (face.a in points and face.b in points and face.c in points):
#                     can_create = False
#         if can_create:
#             for face in list_faces:
#                 face.state = obja.State.Conquered
#                 face.test(self.vertices, self.line)
#                 self.memorize_face(face)
#         return can_create