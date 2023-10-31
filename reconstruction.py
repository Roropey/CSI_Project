import obja
from collections import deque


class Reconstructer(obja.Model):

    def __init__(self,output_name='.\Output_reconstruction.obja'):
        super().__init__()
        self.deleted_faces = set()
        self.gate = deque()
        self.list_removed = []
        with open(output_name, 'w') as output:
            self.output = obja.Output(output, random_color=False)


    def decimating_reconquest(self,output_val):
        print("Start function decimating")
        compte = len(output_val) - 1
        
        while compte>=0:
            c_gate = self.gate.popleft()

            # search for the front face information
            front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
            front_face = self.faces[front_face_information[0]]

            # if its front face is tagged conquered 
            if front_face.state == obja.State.Conquered:
                pass

            #elif  valence <= 6
            elif output_val[compte][0] in [3,4,5,6]:
                
                self.retriangulation(output_val[compte],c_gate)
                front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
                front_vertex = front_face_information[3]

                # search for the gates and the front vertex neighboring vertices are flagged conquered
                self.find_the_gate(front_vertex,c_gate)

                front_vertex.state = obja.State.Conquered 
                for i in front_vertex.faces:
                    self.faces[i].state = obja.State.Conquered 

            # else Null_patch
            elif output_val[compte] == "Null_patch":
                # The front face is flagged conquered
                front_face.state = obja.State.Conquered

                # creates the 2 new gate 
                new_gates = [front_face_information[2:],[front_face_information[3],front_face_information[1]]]

                # add the gates to the fifo
                for gate in new_gates:
                    gate[0].state = obja.State.Conquered 
                    gate[1].state = obja.State.Conquered
                    self.gate.append(gate)

            else:
                raise Exception("Error in the output list of the decimating reconquest")
            
            compte = compte - 1
        
        if compte>0 and len(self.gate)==0:
            raise Exception("Error in the decimating reconquest")
        

    def cleaning_reconquest(self, output):

        #function for reconstruction of cleaning-conquest
        print("start the reconstruction of cleaning conquest:")
        
        compte = len(output)-1

        while compte >=0 and len(self.gate)>0:
            c_gate = self.gate.popleft()
            # Find information about the front face
            front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
            front_face = self.faces[front_face_information[0]]

            # if its front face is tagged conquered
            if front_face == obja.State.Conquered:
                pass

            elif output[compte][0] == 3:

                self.retriangulation(output[compte],c_gate)

                front_face_information = self.gate_to_face(c_gate[0], c_gate[1])
                front_vertex = front_face_information[3]
                front_face = self.faces[front_face_information[0]]

                # find the edge of the patch
                face_up_right = self.gate_to_face(front_vertex,c_gate[1])
                face_up_left = self.gate_to_face(front_vertex, face_up_right[3])

                # Mark the face conquered
                self.faces[face_up_right[0]].state = obja.State.Conquered
                self.faces[face_up_left[0]].state = obja.State.Conquered
                front_face.state = obja.State.Conquered

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
                
                front_vertex.state = obja.State.Conquered


            # else Null_patch
            elif output[compte] == "Null_patch":
                
                # Mark the front face as conquered
                front_face.state = obja.State.Conquered

                # Create two new gates
                new_gates = [[front_face_information[3],front_face_information[2]], [front_face_information[1],front_face_information[3]]]

                # Add the new gates to the queue
                for gate in new_gates:
                    gate[0].state = obja.State.Conquered
                    gate[1].state = obja.State.Conquered
                    self.gate.append(gate)
            else:
                raise Exception("Error in the output list of cleaning reconquest")

            compte = compte - 1

        if compte>0 and len(self.gate)==0:
            raise Exception("Error in the cleaning reconquest")

  

    def recreate_faces(self,coordinates,border_patch,face_existing):
        # Create the vertex (on the model and the ouput)
        self.vertices.append(obja.Vertex(len(self.vertices), coordinates, [],obja.State.Conquered))
        self.output.add_vertex(len(self.vertices) - 1, coordinates)
        # Remove all existing faces (on the model and the ouput)
        for face_index in face_existing:
            self.remove_face(face_index)
            self.output.remove_face(face_index)
        # Create the new faces (on the model and the ouput)
        for i in range(len(border_patch)):
            j = i + 1
            if j >= len(border_patch):
                j = j - len(border_patch)
            index_face = self.create_face([border_patch[i], border_patch[j], len(self.vertices) - 1])
            self.output.add_face(index_face, self.faces[index_face])


    def retriangulation(self,output,gate):
        valence = output[0]
        coordinates = output[1]
        border_patch = gate.copy()
        face_existing = []
        info_face_1 = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[1]])
        face_existing.append(info_face_1[0])
        border_patch.append(info_face_1[3].index)
        self.vertices[border_patch[2]].retriangulation_type = 1
        if valence == 3:
            pass
        elif valence == 4:
            info_face_2 = []
            if self.vertices[border_patch[0]].retriangulation_type == -1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.insert(0,info_face_2[0])
                border_patch.insert(2,info_face_2[3].index)
            elif self.vertices[border_patch[0]].retriangulation_type == 1 and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]],self.vertices[border_patch[2]])
                face_existing.append(info_face_2[0])
                border_patch.append(info_face_2[3].index)
            else:
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")
            self.vertices[info_face_2[3]].retriangulation_type = -1
        elif valence == 5:
            if self.vertices[border_patch[0]].retriangulation_type == 1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.insert(0, info_face_2[0])
                border_patch.insert(2, info_face_2[3].index)
                self.vertices[border_patch[2]].retriangulation_type = -1
                info_face_3 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.append(info_face_3[0])
                border_patch.append(info_face_3[3].index)
                self.vertices[border_patch[4]].retriangulation_type = -1
            elif self.vertices[border_patch[0]].retriangulation_type == 1 and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]], self.vertices[border_patch[2]])
                face_existing.append(info_face_2[0])
                border_patch.append(info_face_2[3].index)
                self.vertices[info_face_2[3]].retriangulation_type = 1
                info_face_3 = self.gate_to_face(self.vertices[info_face_2[3]], self.vertices[info_face_1[3]])
                face_existing.insert(1,info_face_3[0])
                border_patch.insert(3,info_face_3[3].index)
                self.vertices[info_face_3[3]].retriangulation_type = -1
            elif self.vertices[border_patch[0]].retriangulation_type == -1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                face_existing.insert(0, info_face_2[0])
                border_patch.insert(2, info_face_2[3].index)
                self.vertices[info_face_2[3]].retriangulation_type = 1
                info_face_3 = self.gate_to_face(self.vertices[info_face_1[3]], self.vertices[info_face_2[3]])
                face_existing.insert(1,info_face_3[0])
                border_patch.insert(3,info_face_3[3].index)
                self.vertices[info_face_3[3]].retriangulation_type = -1
            else:
                print(self.vertices[border_patch[0]].retriangulation_type)
                print(self.vertices[border_patch[1]].retriangulation_type)
                raise Exception("Unexpected retriangulation_type for gate vertices")
        elif valence == 6:
            if self.vertices[border_patch[0]].retriangulation_type == 1 and self.vertices[border_patch[1]].retriangulation_type == -1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[0]], self.vertices[border_patch[2]])
                info_face_3 = self.gate_to_face(info_face_2[3],self.vertices[border_patch[2]])
                info_face_4 = self.gate_to_face(self.vertices[border_patch[0]],info_face_2[3])
                face_existing.append(info_face_3[0])
                face_existing.append(info_face_2[0])
                face_existing.append(info_face_4[0])
                border_patch.append(info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
                border_patch.append(info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                border_patch.append(info_face_4[3].index)
                self.vertices[info_face_4[3].index].retriangulation_type = -1
            elif self.vertices[border_patch[0]].retriangulation_type == -1 and self.vertices[border_patch[1]].retriangulation_type == 1:
                info_face_2 = self.gate_to_face(self.vertices[border_patch[2]], self.vertices[border_patch[1]])
                info_face_3 = self.gate_to_face(info_face_2[3], self.vertices[border_patch[1]])
                info_face_4 = self.gate_to_face(self.vertices[border_patch[2]], info_face_2[3])
                face_existing.insert(0, info_face_3[0])
                face_existing.insert(1, info_face_2[0])
                face_existing.insert(2, info_face_4[0])
                border_patch.insert(2,info_face_3[3].index)
                self.vertices[info_face_3[3].index].retriangulation_type = -1
                border_patch.insert(3,info_face_2[3].index)
                self.vertices[info_face_2[3].index].retriangulation_type = 1
                border_patch.insert(4,info_face_4[3].index)
                self.vertices[info_face_4[3].index].retriangulation_type = -1



        self.recreate_faces(coordinates,border_patch,face_existing)


    

                
