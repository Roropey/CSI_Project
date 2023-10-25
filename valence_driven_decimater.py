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

    def print_gate_index(self):
        print("List index vertices on gates: ", end="")
        for gate in self.gate:
            print("({},{}) ".format(gate[0].index,gate[1].index),end="")
        print()
    
    def set_everything_to_free(self):
        for face in self.faces:
            if face.visible:
                face.state = obja.State.Free
        for vertex in self.vertices:
            if len(vertex.faces) > 0:
                vertex.state = obja.State.Free
            
    def set_everything_to_zeros(self):
        for vertex in self.vertices:
            if len(vertex.faces) > 0:
                vertex.retriangulation_type = 0


    
    def find_the_gate(self, vertice_center,current_gate, init_gate = None ,count = 0):
        """
        Recursive function to find gates when the front vertex is to be removed.

        Parameters:
        - vertice_center: The front vertex of the current gate.
        - current_gate: The current gate being explored.
        - init_gate: The initial gate used as a reference to stop the recursion.

        """
        #print("Start find gate, counting: {}".format(count))
        count += 1
        # Set the initial gate
        if init_gate is None:
            init_gate = [current_gate[1],current_gate[0]] 
            # inverse in the self.gate all gate orientation as well as the init 
            # => except of the first gate (init), all gate need to point in the future outside of the batch
            current_gate = init_gate
            #print("Init gate initialized: ({},{})".format(init_gate[0].index,init_gate[1].index))
        #print("Gate_to_face")
        # find the next_gate
        gate_face = self.gate_to_face(vertice_center, current_gate[0])
        #print("new_face: {}".format(gate_face[0]))
        new_gate = [gate_face[3],gate_face[2]] # Inversing the gate orientation
        #print("new_gate: ({},{})".format(new_gate[0].index,new_gate[1].index))

        # Check if the vertices of the new gate have state 2 and if it is different from the initial gate
        if not(new_gate[0].state == obja.State.Conquered  and new_gate[1].state == obja.State.Conquered)  and init_gate != new_gate : 
            #print("Not conquered gate")
            new_gate[0].state = obja.State.Conquered  
            new_gate[1].state = obja.State.Conquered 
            self.gate.append(new_gate)
            self.print_gate_index()

        # Check if the new gate is different from the initial gate to avoid infinite recursion
        if init_gate != new_gate and count<10 :
            #print("Different new than init => continue")
            self.find_the_gate(vertice_center,new_gate, init_gate,count)
        if count>=10:
            raise Exception("ça tourne en boucle")
        



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
        #self.print_faces()
        #info_previous = self.gate_to_face(gate_vertex2,gate_vertex1)
        #print("Possible previous face: {}")
        #self.print_vertices()
        #self.print_vertices()
        raise Exception("The two vertex given (index {} and {}) doesn't correspond to a gate.".format(gate_vertex1.index,gate_vertex2.index))
    
                

        
    
    def decimating_conquest(self):
        print("Start function decimating")
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
            #self.print_faces()
            raise Exception("Error in the decimating conquest")
    

    def cleaning_conquest(self):

    #Cleaning Conquest function for removing redundant vertices and faces in a triangle mesh.

    # Cleaning Conquest is a series of operations performed after removing redundant vertices in a triangle mesh.
    #Its main goal is to ensure that the simplified mesh maintains validity and reasonable topological structure.

    #Parameters:
    #- self: Decimater object containing the triangle mesh model and related data.

    #Returns:

  
        c_gate = self.gate.popleft()

        # Find information about the front face
        front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
        front_vertex = front_face_information[3]
        front_face = self.faces[front_face_information[0]]
        #print("Front face state:{}".format(front_face.state))
        # if its front face is tagged conquered or to be removed
        if front_face == obja.State.Conquered or front_face == obja.State.To_be_removed:
            return None


        elif len(front_vertex.faces) == 3 and front_vertex.state == obja.State.Free :

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

        elif front_vertex.state == obja.State.Free or front_vertex == obja.State.Conquered :
            
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

                

    



    def decimateAB(self):
        # inititialisation 
        output_val_A = []
        output_val_B = []
        print("Choosing first gate")
        cond = False
        while not cond:     #on cherche une face qui est visible
            index_init = random.randint(0, len(self.faces)-1) # random index for faces
            faces_init = self.faces[index_init]
            cond = faces_init.visible

        self.vertices[faces_init.a].retriangulation_type = 1
        self.vertices[faces_init.b].retriangulation_type = -1
        init_gate_decimating = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
        self.gate.append(init_gate_decimating)
        #self.print_faces()
        #self.print_vertices()
        #print('taille de la queue {}'.format(len(self.gate)))
        i=0
        # decimating_conquest
        while len(self.gate) > 0 :
            print("decimating_conquest")
            c_gate = self.gate[0]
            vertex_remove = self.decimating_conquest()
            #print("\tanalyzing result decimating")
            if vertex_remove == "Null_patch":
                output_val_A.append("Null_patch")
            
            elif vertex_remove :
                Copy = self.copy()
                Copy.coloring_vertex_all_similar((0.5,0.5,0.5))
                Copy.vertices[c_gate[0].index].coloring_vertex((1,0,0))
                Copy.vertices[c_gate[1].index].coloring_vertex((1,0,0))
                Copy.vertices[vertex_remove.index].coloring_vertex((0,0,1))
                Copy.save_with_obja_f_by_f(f'Results_tests/before_retriangulation_{i}.obj')

                #output_val_A.append(len(vertex_remove.faces))
                output_val_A.append([vertex_remove.valence,vertex_remove.coordinates])
                self.retriangulation(vertex_remove)
                self.save_with_obja_f_by_f('Results_tests/after_retriangulation.obj')
                Copy = self.copy()
                Copy.coloring_vertex_based_type_retriang()
                Copy.save_with_obja_f_by_f(f'Results_tests/after_retriangulation_type_colored_{i}.obj')
                i += 1
            #print('taille de la queue {}'.format(len(self.gate)))
        self.save_with_obja_f_by_f('Results_tests/After_Decimating_conquest.obj')
        self.set_everything_to_free()
        #self.set_everything_to_zeros()

        print("Start cleaning conquest")
        # cleaning_conquest
        cond = True
        while cond:
            index_init = random.randint(0, len(self.faces)-1) # random index for faces
            faces_init = self.faces[index_init]
            if faces_init.visible and not(len(self.vertices[faces_init.a].faces) == 3 or len(self.vertices[faces_init.b].faces) == 3):
                cond = False
        
        init_gate_cleaning = [self.vertices[faces_init.a],self.vertices[faces_init.b]] # creation of the first gate
        self.gate.append(init_gate_cleaning)

        self.print_single_vertex(init_gate_cleaning[0].index)
        self.print_single_vertex(init_gate_cleaning[1].index)
        self.print_single_face(index_init)
        
        
        while len(self.gate) > 0 :
        
            vertex_remove = self.cleaning_conquest()
            #print("Cleaning passed")
            if vertex_remove == "Null_patch":
                #print("Is a null patch")
                output_val_B.append("Null_patch")
            
            elif vertex_remove :
                #print("Need to be removed")
                output_val_B.append([vertex_remove.valence,vertex_remove.coordinates])
                self.retriangulation_4_cleaning_conquest(vertex_remove)
        print(index_init)
        self.print_count_valencies()
        self.save_with_obja_f_by_f('Results_tests/After_Cleaning_conquest.obj')
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
        print(count_point)
        decimating_output = []
        while count_point > nb_point_end:
            count_iteration += 1
            print(f"{count_iteration}ieme decimation")
            decimating_output.append(self.decimateAB())
            self.save_with_obja_f_by_f(f'Results_tests/Decimate{count_iteration}.obj')
            self.set_everything_to_free()
            self.set_everything_to_zeros()
            count_point = self.count_point()
            print(count_point)
        return decimating_output

    
            
    
    def recreate_faces(self,indices):
        face = obja.Face.from_array_num(indices)
        face.state = obja.State.Conquered
        face.test(self.vertices, self.line)
        self.memorize_face(face)

    def retriangulation_4_cleaning_conquest(self,vertex_to_be_removed):
        print("Vertex to be removed: {}".format(vertex_to_be_removed.index))
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
        self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
        vertex_infos.visible = False

           
 
    def retriangulation(self,vertex_to_be_removed):
        print("Vertex to be removed: {}".format(vertex_to_be_removed.index))
        self.save_with_obja_f_by_f('Results_tests/test1.obj')
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
        self.save_with_obja_f_by_f('Results_tests/test2.obj')
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
            print("Valence of 3")
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
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")  
            # Creating faces
            self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
            
        elif vertex_to_be_removed.valence == 4:
            print("Valence of 4")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                #Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])            

            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                #Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                
            else : raise Exception("Unexpected retriangulation_type for gate vertices")    

        elif vertex_to_be_removed.valence == 5:
            print("Valence of 5")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.recreate_faces([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[4]].index])                   
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.recreate_faces([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index])                 
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.recreate_faces([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[0]].index])
                
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.recreate_faces([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])

            else : 
                print("Gate retriangulation type: {} {}".format(self.vertices[border_patch[0]].retriangulation_type, self.vertices[border_patch[1]].retriangulation_type))
                raise Exception("Unexpected retriangulation_type for gate vertices") 
            
        elif vertex_to_be_removed.valence == 6:
            print("Valence of 6")
            if (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                self.vertices[border_patch[5]].retriangulation_type=-1
                
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                self.vertices[border_patch[5]].retriangulation_type=1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==1) and (self.vertices[border_patch[1]].retriangulation_type==1):
                self.vertices[border_patch[2]].retriangulation_type=-1
                self.vertices[border_patch[3]].retriangulation_type=1
                self.vertices[border_patch[4]].retriangulation_type=-1
                self.vertices[border_patch[5]].retriangulation_type=1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index])
                self.recreate_faces([self.vertices[border_patch[1]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
            elif (self.vertices[border_patch[0]].retriangulation_type==-1) and (self.vertices[border_patch[1]].retriangulation_type==-1):
                self.vertices[border_patch[2]].retriangulation_type=1
                self.vertices[border_patch[3]].retriangulation_type=-1
                self.vertices[border_patch[4]].retriangulation_type=1
                self.vertices[border_patch[5]].retriangulation_type=-1
                # Create faces
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[1]].index,self.vertices[border_patch[2]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[2]].index,self.vertices[border_patch[4]].index])
                self.recreate_faces([self.vertices[border_patch[0]].index,self.vertices[border_patch[4]].index,self.vertices[border_patch[5]].index])
                self.recreate_faces([self.vertices[border_patch[2]].index,self.vertices[border_patch[3]].index,self.vertices[border_patch[4]].index])
            else : raise Exception("Unexpected retriangulation_type for gate vertices")
        else:
            print()
            raise Exception("Unexpected valence: {} (<3 or >6)".format(vertex_to_be_removed.valence))  
        
        vertex_infos.visible = False
        


def main():
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('Test_Objects_low/Sphere_4&5&6&7_valencies.obj')
    # model.complete_model()
    
    model.decimateAB()
    #model.decimate(15)
    model.save_with_obja_f_by_f('Results_tests/DecimateAB_sphere_4567.obj')


if __name__ == '__main__':
    main()
