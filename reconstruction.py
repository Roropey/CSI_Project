import obja
from collections import deque
from utility import limit_value

class Reconstructer(obja.Model):

    def __init__(self,output_name='.\Output_reconstruction.obja'):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
        self.list_removed = []
        #with as output:
        self.file = open(output_name, 'w')
        self.output = obja.Output(self.file , random_color=False)
        self.count = 0
        self.count_bis = 0


    def decimating_reconquest(self,output_val):
        print("Start function redecimating")
        
        nb_output = len(output_val)-1
        compte = 0
        while compte <= nb_output or len(self.gate)>0:
            
            c_gate = self.gate.popleft()

            # search for the front face information
            front_face_information = self.gate_to_face(self.vertices[c_gate[0]], self.vertices[c_gate[1]])
            front_face = self.faces[front_face_information[0]]
            self.coloring_vertex_all_similar([0.5,0.5,0.5])
            #
            self.vertices[c_gate[0]].coloring_vertex([1,0,0])
            #
            #
            self.vertices[c_gate[1]].coloring_vertex([0,1,0])
            #
            # front_face_information[3].coloring_vertex([1,0,0])
            #
            # self.print_single_vertex(c_gate[0].index)
            # self.print_single_vertex(c_gate[1].index)
            # self.print_single_vertex(front_face_information[3].index)
            # self.print_single_face(front_face_information[0])
            # self.save_selected_f('Results_tests/face_gate_decimating_{}.obj'.format(self.count),[front_face_information[0]])
            # self.count += 1

            self.count += 1
            self.save_f_by_f('Results_tests/re_decimating_conquest_{}_before.obj'.format(self.count))
            
            #self.save_v_and_f('Results_tests/gate_re_decimating_conquest_{}_bis.obj'.format(self.count))
            #self.save_selected_f('Results_tests/face_re_cleaning_conquest_{}.obj'.format(self.count),[front_face_information[0]])

            
            # if its front face is tagged conquered 
            if front_face.state == obja.State.Conquered:
                print(f"Itération decimating reconstruction {self.count}, compte {compte} pass")
                pass

            #elif  valence <= 6
            elif output_val[compte][0] in [3,4,5,6]:
                
                print(f"Itération decimating reconstruction {self.count}, compte {compte} retriangulation {output_val[compte][0]}")
                self.print_single_vertex(output_val[compte][1])
                self.print_single_vertex(c_gate[0])
                self.print_single_vertex(c_gate[1])
                print("retriangulation")
                self.retriangulation(output_val[compte],[self.vertices[c_gate[0]],self.vertices[c_gate[1]]])

                #c_gate[0] = self.vertices[c_gate[0].index]
                #c_gate[1] = self.vertices[c_gate[1].index]

                self.save_f_by_f('Results_tests/re_decimating_conquest_{}_retriangulation.obj'.format(self.count))
                #c_gate = [self.vertices[c_gate[0].index], self.vertices[c_gate[1].index]] # Recupering last versions of verticies of c_gate
                front_face_information = self.gate_to_face(self.vertices[c_gate[0]],self.vertices[c_gate[1]])
                front_vertex = front_face_information[3]
                self.print_single_vertex(output_val[compte][1])
                self.print_single_vertex(c_gate[0])
                self.print_single_vertex(c_gate[1])
                self.print_single_vertex(front_vertex.index)
                self.print_single_face(front_face_information[0])
                # search for the gates and the front vertex neighboring vertices are flagged conquered
                self.find_the_gate_index(front_vertex,[self.vertices[c_gate[0]],self.vertices[c_gate[1]]])

                front_vertex.state = obja.State.Conquered 
                for i in front_vertex.faces:
                    self.faces[i].state = obja.State.Conquered 
                
                compte = compte + 1

            # else Null_patch
            elif output_val[compte] == "Null_patch":
                print(f"Itération decimating reconstruction {self.count}, compte {compte} Null_patch")
                # The front face is flagged conquered
                front_face.state = obja.State.Conquered

                # creates the 2 new gate 
                new_gates = [[front_face_information[2].index, front_face_information[3].index],[front_face_information[3].index,front_face_information[1].index]]

                # add the gates to the fifo
                for gate in new_gates:
                    self.vertices[gate[0]].state = obja.State.Conquered
                    self.vertices[gate[1]].state = obja.State.Conquered
                    self.gate.append(gate)
                
                compte = compte + 1

            else:
                raise Exception("Error in the output list of the decimating reconquest")
        

    def cleaning_reconquest(self, output):

        #function for reconstruction of cleaning-conquest
        print("start the reconstruction of cleaning conquest:")
        
        nb_output = len(output)-1
        compte = 0
        while compte <= nb_output or len(self.gate)>0:

            c_gate = self.gate.popleft()
            # Find information about the front face
            front_face_information = self.gate_to_face(self.vertices[c_gate[0]], self.vertices[c_gate[1]])
            front_face = self.faces[front_face_information[0]]
            #self.print_single_vertex(front_face_information[3].index)
            self.coloring_vertex_all_similar([0.5,0.5,0.5])

            self.vertices[c_gate[0]].coloring_vertex([0,1,0])
            #front_face_information[1].coloring_vertex([0,1,0])

            self.vertices[c_gate[1]].coloring_vertex([0,0,1])
            #front_face_information[2].coloring_vertex([0,0,1])
            self.count += 1
            front_face_information[3].coloring_vertex([1,0,0])
            #self.print_single_vertex(c_gate[0].index)
            #self.print_single_vertex(c_gate[1].index)
            #self.print_single_vertex(front_face_information[3].index)
            #self.print_single_face(front_face_information[0])
            #self.save_f_by_f('Results_tests/re_cleaning_conquest_{}.obj'.format(self.count))
            #self.save_v_and_f('Results_tests/gate_re_cleaning_conquest_{}_bis.obj'.format(self.count))
            #self.save_selected_f('Results_tests/face_re_cleaning_conquest_{}.obj'.format(self.count),[front_face_information[0]])
            
            self.coloring_vertex_all_similar([0.5, 0.5, 0.5])


            # if its front face is tagged conquered
            if front_face.state == obja.State.Conquered:
                print(f"Itération cleaning reconstruction {self.count}, etat du output {compte} pass")
                pass

            elif output[compte][0] == 3:
                print(f"Itération cleaning reconstruction {self.count}, etat du output {compte} retriangulation")
                print(output[compte][0])

                self.retriangulation(output[compte],[self.vertices[c_gate[0]],self.vertices[c_gate[1]]])

                #self.print_single_vertex(c_gate[0].index)
                #self.print_single_vertex(c_gate[1].index)
                #self.print_single_vertex(output[compte][1])

                #c_gate[0] = self.vertices[c_gate[0].index]
                #c_gate[1] = self.vertices[c_gate[1].index]

                #self.save_f_by_f('Results_tests/re_cleaning_conquest_{}_retriangulation.obj'.format(self.count))

                front_face_information = self.gate_to_face(self.vertices[c_gate[0]],self.vertices[c_gate[1]])
                front_vertex = front_face_information[3]
                front_face = self.faces[front_face_information[0]]

                #self.print_single_vertex(front_vertex.index)

                

                # find the edge of the patch
                face_up_right = self.gate_to_face(front_vertex,self.vertices[c_gate[1]])
                face_up_left = self.gate_to_face(front_vertex, face_up_right[3])

                # Mark the face conquered
                self.faces[face_up_right[0]].state = obja.State.Conquered
                self.faces[face_up_left[0]].state = obja.State.Conquered
                front_face.state = obja.State.Conquered

                # Create two intermediare gates
                intermediaire_gates = [ [face_up_right[3].index, c_gate[1]] , [face_up_left[3].index, face_up_right[3].index] ]

                # find the other gates 
                for gate in intermediaire_gates:
                    self.vertices[gate[0]].state = obja.State.Conquered
                    self.vertices[gate[1]].state = obja.State.Conquered
                    f = self.gate_to_face(self.vertices[gate[0]],self.vertices[gate[1]])

                    # Create the two new gates
                    new_gates = [[f[3].index,f[2].index], [f[1].index, f[3].index]]

                    # Add the new gates to the queue
                    for gate in new_gates:
                        self.vertices[gate[0]].state = obja.State.Conquered
                        self.vertices[gate[1]].state = obja.State.Conquered
                        self.gate.append(gate)
                    self.faces[f[0]].state = obja.State.Conquered
                
                front_vertex.state = obja.State.Conquered
                compte = compte + 1


            # else Null_patch
            elif output[compte] == "Null_patch":
                print(f"Itération cleaning reconstruction {self.count}, etat du output {compte} Null_patch")
                
                # Mark the front face as conquered
                front_face.state = obja.State.Conquered

                # Create two new gates
                new_gates = [[front_face_information[3].index,front_face_information[2].index], [front_face_information[1].index,front_face_information[3].index]]

                # Add the new gates to the queue
                for gate in new_gates:
                    self.vertices[gate[0]].state = obja.State.Conquered
                    self.vertices[gate[1]].state = obja.State.Conquered
                    self.gate.append(gate)
                compte = compte + 1
            else:
                raise Exception("Error in the output list of cleaning reconquest")


        if (compte<nb_output and len(self.gate)==0):
            raise Exception("Error in the cleaning reconquest")
        
        #raise Exception("Stop")

  

    def recreate_faces(self,index_to_added,border_patch,face_existing):

        # Create the vertex (on the model and the ouput)
        self.coloring_vertex_based_type_retriang()
        index_faces = []
        for tuple_index in face_existing:
            if tuple_index:
                index_faces.append(tuple_index[0])
        self.save_selected_f('Results_tests/border_patch_{}.obj'.format(self.count_bis),index_faces)
        self.save_f_by_f('Results_tests/all_{}.obj'.format(self.count_bis))
        vertex_to_be_added = self.vertices[index_to_added]
        self.vertices[index_to_added].coloring_vertex([0,1,0])
        self.vertices[index_to_added].visible = True
        self.output.add_vertex(vertex_to_be_added.index, vertex_to_be_added.coordinates)
        # Remove all existing faces (on the model and the ouput)
        for tuple_index in face_existing:
            if tuple_index:
                self.remove_face(tuple_index[0])
                self.output.remove_face(tuple_index[0])
        # Create the new faces (on the model and the ouput)
        for i in range(len(border_patch)):
            j = i + 1
            if j >= len(border_patch):
                j = j - len(border_patch)
            index_face = self.create_face([border_patch[i], border_patch[j], vertex_to_be_added.index])
            self.output.add_face(index_face, self.faces[index_face])
        

    def retriangulation(self,output,gate):
        valence = output[0]
        print("Valence {}".format(valence))

        index_to_added = output[1]
        # List of the verticies around in the order of the batch (from gate to before gate in the trigonometric order)
        border_patch = [gate[0].index,gate[1].index] #gate.copy()
        self.coloring_vertex_all_similar([0.5, 0.5, 0.5])
        front_face_information = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[1]])
        self.vertices[border_patch[0]].coloring_vertex([1, 0, 0])
        self.vertices[border_patch[1]].coloring_vertex([0, 1, 0])
        self.save_selected_f('Results_tests/start_border_patch_{}.obj'.format(self.count_bis), [front_face_information[0]])
        self.count_bis += 1
        # List of tuple or None: first element of tuple corresponding face index, and second to vertex to be modified (1 for a, 2 for b and 3 for c, 0 for removing (case of valence 6 with face in center))
        # The None corresponding to face to be created and not modified
        # The list correspond to the list of existing face and the vertex to be modified, or None in the order of the border patch 
        # (first tuple for the face shared by border_patch 0 and 1, second tuple for 1 and 2, etc and None for not existing face that required to be created between the two verticies)
        # Goal: knowing which face(s) to be reused by modifiying the vertex to the created one.
        face_existing = []
        info_face_1 = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[1]])
        face_existing.append((info_face_1[0],info_face_1[4]))
        border_patch.append(info_face_1[3].index)
        self.vertices[border_patch[2]].retriangulation_type = 1
        if valence == 3:
            face_existing.append(None)
            face_existing.append(None)
        elif valence == 4:
            info_face_2 = []
            if (self.vertices[border_patch[0]].retriangulation_type == -1 or self.vertices[border_patch[0]].retriangulation_type == 1) and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                # The position given in the 5th position of info_face_2 correspond to the 3rd vertex of the border patch, but we want to keep the face to be connected to
                # the 2nd and 3rd verticies, so we need to send in the tuple the position of the 4th vertex in the face to be modified, so applied a +1 and ensure to be less than 3
                # +1 for the left of the gate, -1 for the right of the gate
                face_existing.append((info_face_2[0],limit_value(info_face_2[4]+1,1,3)))
                face_existing.append(None)
                face_existing.append(None)
                border_patch.insert(2,info_face_2[3].index)
            elif (self.vertices[border_patch[0]].retriangulation_type == 1 or self.vertices[border_patch[0]].retriangulation_type == -1) and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[2]])
                # Face shared by border patch 2 and 3 is the same as the face of border patch 1 and 2, required to create a new face, so None
                face_existing.append(None)
                face_existing.append((info_face_2[0],limit_value(info_face_2[4]+1,1,3)))
                border_patch.append(info_face_2[3].index)
            else:
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                self.coloring_vertex_based_type_retriang()
                self.save_f_by_f('Results_tests/problem_type.obj')
                front_face_information = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[1]])
                self.coloring_vertex_all_similar([0.5,0.5,0.5])
                self.vertices[border_patch[0]].coloring_vertex([1,0,0])
                self.vertices[border_patch[1]].coloring_vertex([0,1,0])
                self.save_selected_f('Results_tests/problem_type_border_patch.obj',[front_face_information[0]])
                raise Exception("Unexpected retriangulation_type for gate vertices")
            self.vertices[info_face_2[3].index].retriangulation_type = -1
        elif valence == 5:
            if self.vertices[border_patch[0]].retriangulation_type == 1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.append((info_face_2[0],limit_value(info_face_2[4]+1,1,3)))
                face_existing.append(None)
                border_patch.insert(2, info_face_2[3].index)
                self.vertices[border_patch[2]].retriangulation_type = -1
                info_face_3 = self.gate_to_face(self.vertices[border_patch[0]], self.vertices[border_patch[3]])
                face_existing.append(None)
                face_existing.append((info_face_3[0],limit_value(info_face_3[4]-1,1,3)))
                border_patch.append(info_face_3[3].index)
                self.vertices[border_patch[4]].retriangulation_type = -1
            elif (self.vertices[border_patch[0]].retriangulation_type == 1 or self.vertices[border_patch[0]].retriangulation_type == -1) and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]], self.vertices[border_patch[2]])
                face_existing.append(None)
                border_patch.append(info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                info_face_3 = self.gate_to_face(info_face_2[3], info_face_1[3])
                face_existing.append((info_face_3[0],limit_value(info_face_3[4]+1,1,3)))
                face_existing.append(None)
                face_existing.append((info_face_2[0],limit_value(info_face_2[4]-1,1,3)))
                border_patch.insert(3,info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
            elif self.vertices[border_patch[0]].retriangulation_type == -1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.append((info_face_2[0],limit_value(info_face_2[4]+1,1,3)))
                border_patch.insert(2, info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                info_face_3 = self.gate_to_face(info_face_1[3], info_face_2[3])
                face_existing.append((info_face_3[0],limit_value(info_face_3[4]+1,1,3)))
                face_existing.append(None)
                face_existing.append(None)
                border_patch.insert(3,info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
            else:
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")
        elif valence == 6:
            if (self.vertices[border_patch[0]].retriangulation_type == 1 or self.vertices[border_patch[0]].retriangulation_type == -1) and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]], self.vertices[border_patch[2]])
                info_face_3 = self.gate_to_face(info_face_2[3],self.vertices[border_patch[2]])
                info_face_4 = self.gate_to_face(self.vertices[border_patch[0]],info_face_2[3])
                face_existing.append((info_face_2[0],0))
                face_existing.append((info_face_3[0],limit_value(info_face_3[4]+1,1,3)))
                face_existing.append(None)
                face_existing.append((info_face_4[0],limit_value(info_face_4[4]+1,1,3)))
                face_existing.append(None)
                border_patch.append(info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
                border_patch.append(info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                border_patch.append(info_face_4[3].index)
                self.vertices[info_face_4[3].index].retriangulation_type = -1
            elif (self.vertices[border_patch[0]].retriangulation_type == -1 or self.vertices[border_patch[0]].retriangulation_type == 1) and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                info_face_3 = self.gate_to_face(info_face_2[3], self.vertices[border_patch[1]])
                info_face_4 = self.gate_to_face(self.vertices[border_patch[2]], info_face_2[3])
                face_existing.append((info_face_3[0],limit_value(info_face_3[4]+1,1,3)))
                face_existing.append((info_face_2[0],0))
                face_existing.append((info_face_4[0],limit_value(info_face_4[4]+1,1,3)))
                face_existing.append(None)
                face_existing.append(None)
                border_patch.insert(2,info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
                border_patch.insert(3,info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                border_patch.insert(4,info_face_4[3].index)
                self.vertices[info_face_4[3].index].retriangulation_type = -1
            else:
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")

        if valence != len(border_patch):
            raise Exception("Not every vertices around have been taken")
        self.recreate_faces(index_to_added,border_patch,face_existing)

    def init_mode(self):
        index_vertex_created = []
        for index_face in range(len(self.faces)):
            face = self.faces[index_face]
            if not(face.visible):
                continue        
            if not(face.a in index_vertex_created):
                if self.vertices[face.a].color:
                    self.output.add_colored_vertex(face.a, self.vertices[face.a].coordinates, self.vertices[face.a].color)
                else:
                    self.output.add_vertex(face.a, self.vertices[face.a].coordinates)
                index_vertex_created.append(face.a)
            if not(face.b in index_vertex_created):
                if self.vertices[face.b].color:
                    self.output.add_colored_vertex(face.b, self.vertices[face.b].coordinates, self.vertices[face.b].color)
                else:
                    self.output.add_vertex(face.b, self.vertices[face.b].coordinates)
                index_vertex_created.append(face.b)
            if not(face.c in index_vertex_created):
                if self.vertices[face.c].color:
                    self.output.add_colored_vertex(face.c, self.vertices[face.c].coordinates, self.vertices[face.c].color)
                else:
                    self.output.add_vertex(face.c, self.vertices[face.c].coordinates)
                index_vertex_created.append(face.c)
            self.output.add_face(index_face, face)


    
    def reconstruction(self,decimating_output):
        nb_it = len(decimating_output)
        print(nb_it)
        decimating_output.reverse()
        self.init_mode()

        for i in range (nb_it):
            print(f"Itération AB:{i}")
            
            self.count = 0


            self.set_everything_to_free()
            self.set_everything_to_zeros()

            decimating_output_AB = decimating_output[i]
            print(decimating_output_AB.num_iteration)
            output_B = decimating_output_AB.output_val_B
            output_A = decimating_output_AB.output_val_A

            print(f"longeur du output B :{len(output_B)}")
            print(output_B)

            init_gate = [decimating_output_AB.init_gate_cleaning[0].index, decimating_output_AB.init_gate_cleaning[1].index]
            self.gate.append(init_gate)
            self.vertices[self.gate[0][0]].retriangulation_type = -1
            self.vertices[self.gate[0][1]].retriangulation_type = 1

            self.cleaning_reconquest(output_B)
            self.save_f_by_f('Results_tests/after_cleaning_reconquest_{}.obj'.format(i))

            self.set_everything_to_free()
            self.set_everything_to_zeros()

            if len(self.gate)>0:
                raise Exception("il reste des gates apres un cleaning")

            init_gate = [decimating_output_AB.init_gate_decimating[0].index, decimating_output_AB.init_gate_decimating[1].index]
            self.gate.append(init_gate)
            self.vertices[self.gate[0][0]].retriangulation_type = -1
            self.vertices[self.gate[0][1]].retriangulation_type = 1
            
            self.count = 0

            self.decimating_reconquest(output_A)
            self.save_f_by_f('Results_tests/after_decimating_reconquest_{}.obj'.format(i))
            
        return None

                
