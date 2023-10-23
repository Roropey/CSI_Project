#!/usr/bin/env python3

import sys
import numpy as np
import random
from enum import Enum

class State(Enum):
    Free = 1
    Conquered = 2
    To_be_removed = 3

"""
obja model for python.
"""

class Face:
    """
    The class that holds a, b, and c, the indices of the vertices of the face.
    """

    def __init__(self, a, b, c, visible=True):
        self.a = a
        self.b = b
        self.c = c
        self.visible = visible
        self.state = State.Free   # ajout du state pour les faces
        self.code = 0             # Code pour la possibilité d'attribuer un code, potentiellement utile pour regrouper plusieurs faces/couleur

    def from_array(array):
        """
        Initializes a face from an array of strings representing vertex indices (starting at 1)
        """
        face = Face(0, 0, 0)
        face.set(array)
        face.visible = True
        return face
    
    def from_array_num(array):
        face = Face(array[0],array[1],array[2])
        face.visible = True
        return face

    def set(self, array):
        """
        Sets a face from an array of strings representing vertex indices (starting at 1)
        """
        self.a = int(array[0].split('/')[0]) - 1
        self.b = int(array[1].split('/')[0]) - 1
        self.c = int(array[2].split('/')[0]) - 1
        return self

    def clone(self):
        """
        Clones a face from another face
        """
        return Face(self.a, self.b, self.c, self.visible)

    def copy(self, other):
        """
        Sets a face from another face
        """
        self.a = other.a
        self.b = other.b
        self.c = other.c
        self.visible = other.visible
        return self

    def test(self, vertices, line="unknown"):
        """
        Tests if a face references only vertices that exist when the face is declared.
        """
        if self.a >= len(vertices):
            raise VertexError(self.a + 1, line)
        if self.b >= len(vertices):
            raise VertexError(self.b + 1, line)
        if self.c >= len(vertices):
            raise VertexError(self.c + 1, line)

    def __str__(self):
        return "Face({}, {}, {})".format(self.a, self.b, self.c)

    def __repr__(self):
        return str(self)


class VertexError(Exception):
    """
    An operation references a vertex that does not exist.
    """

    def __init__(self, index, line):
        """
        Creates the error from index of the referenced vertex and the line where the error occured.
        """
        self.line = line
        self.index = index
        super().__init__()

    def __str__(self):
        """
        Pretty prints the error.
        """
        return f"There is no vertex {self.index} (line {self.line})"


class FaceError(Exception):
    """
    An operation references a face that does not exist.
    """

    def __init__(self, index, line):
        """
        Creates the error from index of the referenced face and the line where the error occurred.
        """
        self.line = line
        self.index = index
        super().__init__()

    def __str__(self):
        """
        Pretty prints the error.
        """
        return f'There is no face {self.index} (line {self.line})'


class FaceVertexError(Exception):
    """
    An operation references a face vertex that does not exist.
    """

    def __init__(self, index, line):
        """
        Creates the error from index of the referenced face vertex and the line where the error occured.
        """
        self.line = line
        self.index = index
        super().__init__()

    def __str__(self):
        """
        Pretty prints the error.
        """
        return f'Face has no vertex {self.index} (line {self.line})'


class UnknownInstruction(Exception):
    """
    An instruction is unknown.
    """

    def __init__(self, instruction, line):
        """
        Creates the error from instruction and the line where the error occured.
        """
        self.line = line
        self.instruction = instruction
        super().__init__()

    def __str__(self):
        """
        Pretty prints the error.
        """
        return f'Instruction {self.instruction} unknown (line {self.line})'

class Vertex:
    def __init__(self,index,coordinates):
        self.index = index
        self.coordinates = coordinates
        self.faces = []
        self.state = State.Free         # see class State
        self.retriangulation_type = 0          # +1 => + and -1 => - and 0 => nothing...
        self.visible = True
class Model:
    """
    The OBJA model.
    """

    def __init__(self):
        """
        Initializes an empty model.
        """
        self.vertices = []
        self.faces = []
        # self.fov = [] # liste d'array contenant les indices de faces pour chaque vertices
        # self.state_flags = [] # le sate_flags de chaque vertices
        # self.retirangulation_tags = [] # les tags de chaque vertices pour la retriangulation
        self.line = 0

    """def complete_model(self):
        self.fov = [np.array([],dtype=int) for _ in range(len(self.vertices))]
        for i in range (len(self.faces)) :
            f = self.faces[i]
            self.fov[f.a] = np.append(self.fov[f.a],i)
            self.fov[f.b] = np.append(self.fov[f.b],i)
            self.fov[f.c] = np.append(self.fov[f.c],i)
        self.state_flags = np.zeros(len(self.vertices),dtype=int)
        self.retirangulation_tags = np.zeros(len(self.vertices),dtype=int)
    """
    def memorize_face(self,face):
        self.faces.append(face)
        index_face = len(self.faces) - 1
        self.vertices[face.a].faces.append(index_face)
        self.vertices[face.b].faces.append(index_face)
        self.vertices[face.c].faces.append(index_face)
        
        

    def get_vertex_from_string(self, string):
        """
        Gets a vertex from a string representing the index of the vertex, starting at 1.

        To get the vertex from its index, simply use model.vertices[i].
        """
        index = int(string) - 1
        if index >= len(self.vertices):
            raise FaceError(index + 1, self.line)
        return self.vertices[index].coordinates

    def get_face_from_string(self, string):
        """
        Gets a face from a string representing the index of the face, starting at 1.

        To get the face from its index, simply use model.faces[i].
        """
        index = int(string) - 1
        if index >= len(self.faces):
            raise FaceError(index + 1, self.line)
        print(index)
        print(self.faces[index])
        return self.faces[index]
    
    def remove_face(self,index):
        
        if index >= len(self.faces):
            raise FaceError(index + 1, self.line)
        face = self.faces[index]
        self.vertices[face.a].faces.remove(index)
        self.vertices[face.b].faces.remove(index)
        self.vertices[face.c].faces.remove(index)
        self.faces[index].visible = False       #Removing the face completly will modify the indexation of the faces and maybe will create a shift between faces and rest

    def parse_file(self, path):
        """
        Parses an OBJA file.
        """
        with open(path, "r") as file:
            for line in file.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        """
        Parses a line of obja file.
        """
        self.line += 1

        split = line.split()

        if len(split) == 0:
            return

        if split[0] == "v":

            self.vertices.append(Vertex(len(self.vertices),np.array(split[1:], np.double)))
            # Maybe modify the +2... => need to remove the +2
        elif split[0] == "ev":
            self.get_vertex_from_string(split[1]).set(split[2:])

        elif split[0] == "tv":
            self.get_vertex_from_string(split[1]).translate(split[2:])

        elif split[0] == "f" or split[0] == "tf":
            for i in range(1, len(split) - 2):
                face = Face.from_array(split[i:i + 3])
                face.test(self.vertices, self.line)
                self.memorize_face(face)

        elif split[0] == "ts":
            for i in range(1, len(split) - 2):
                if i % 2 == 1:
                    face = Face.from_array([split[i], split[i + 1], split[i + 2]])
                else:
                    face = Face.from_array([split[i], split[i + 2], split[i + 1]])
                face.test(self.vertices, self.line)
                self.memorize_face(face)

        elif split[0] == "ef":
            self.get_face_from_string(split[1]).set(split[2:])

        elif split[0] == "efv":
            face = self.get_face_from_string(split[1])
            vertex = int(split[2])
            new_index = int(split[3]) - 1
            if vertex == 1:
                self.vertices[face.a].faces.remove(split[1])
                face.a = new_index
                self.vertices[face.a].faces.append(split[1])
            elif vertex == 2:
                self.vertices[face.b].faces.remove(split[1])
                face.b = new_index
                self.vertices[face.b].faces.append(split[1])
            elif vertex == 3:
                self.vertices[face.c].faces.remove(split[1])
                face.c = new_index
                self.vertices[face.c].faces.append(split[1])
            else:
                raise FaceVertexError(vertex, self.line)

        elif split[0] == "df":
            self.get_face_from_string(split[1]).visible = False

        elif split[0] == "#":
            return

        else:
            return
            # raise UnknownInstruction(split[0], self.line)
    """
    # Function to save the model into a obja file by doing first the vertex, and after the faces
    def obj_to_obja_v_then_f(self,output_name):
        # Open the output file
        with open(output_name, 'w') as output:
            # Create obja object
            output_model = Output(output, random_color=False)
            # First put all vertex present
            index_vertex_created = []
            for vertex in self.vertices:
                # A vertex removed is a vertex with no connection (no faces)
                if not(vertex.faces):
                    continue
                elif len(vertex.faces) < 3:
                    raise Exception("Valence of vertex of index {} wrong (<3)".format(vertex.index))
                else:
                    output_model.add_vertex(vertex.index, vertex.coordinates)
                    index_vertex_created.append(vertex.index)

            for index_face in range(len(self.faces)):
                face = self.faces[index_face]
                # A face removed is a not visible face
                if not(face.visible):
                    continue
                if not(face.a in index_vertex_created):
                    raise Exception('Vertex a of index {} not present in face of index {}'.format(face.a, index_face))
                elif not(face.b in index_vertex_created):
                    raise Exception('Vertex b of index {} not present in face of index {}'.format(face.b, index_face))
                elif not(face.c in index_vertex_created):
                    raise Exception('Vertex c of index {} not present in face of index {}'.format(face.c, index_face))
                else:
                    output_model.add_face(index_face, face)
    """

    # Function to save the model into a obja file by doing faces by faces
    def save_with_obja_f_by_f(self,output_name):
        # Open the output file
        with open(output_name, 'w') as output:
            # Create obja object
            output_model = Output(output, random_color=False)
            # First put all vertex present
            index_vertex_created = []
            for index_face in range(len(self.faces)):
                face = self.faces[index_face]
                if not(face.visible):
                    continue
                # if len(self.vertices[face.a].faces) < 3:
                #     raise Exception('Vertex a of index {} from face of index {} has only {} valencies'.format(face.a, index_face, len(self.vertices[face.a].faces)))
                # elif len(self.vertices[face.b].faces) < 3:
                #     raise Exception('Vertex b of index {} from face of index {} has only {} valencies'.format(face.b, index_face, len(self.vertices[face.b].faces)))
                # elif len(self.vertices[face.c].faces) < 3:
                #     raise Exception('Vertex c of index {} from face of index {} has only {} valencies'.format(face.c, index_face, len(self.vertices[face.c].faces)))
                # else:
                if not(face.a in index_vertex_created):
                    output_model.add_vertex(face.a, self.vertices[face.a].coordinates)
                    index_vertex_created.append(face.a)
                if not(face.b in index_vertex_created):
                    output_model.add_vertex(face.b, self.vertices[face.b].coordinates)
                    index_vertex_created.append(face.b)
                if not(face.c in index_vertex_created):
                    output_model.add_vertex(face.c, self.vertices[face.c].coordinates)
                    index_vertex_created.append(face.c)
                output_model.add_face(index_face, face)        

    def print_faces(self):
        for index_face in range(len(self.faces)):
            face = self.faces[index_face]
            print("Face of index {}, composed of:\n\t- a: {}\n\t- b: {}\n\t- c: {}\n\t- visibility: {}\n\t- state: {}".format(index_face,face.a,face.b,face.c,face.visible,face.state))
            
    def print_vertices(self):
        for index_vertex in range(len(self.vertices)):
            vertex = self.vertices[index_vertex]
            print("Vertex :\n\t- index in model: {}\n\t- index in vertex: {}\n\t- coordinates: {}\n\t- faces: {}\n\t- state: {}\n\t- retriangulation type: {}\n\t- visibility: {}".format(index_vertex,vertex.index,vertex.coordinates,vertex.faces,vertex.state,vertex.retriangulation_type,vertex.visible))

    def print_single_face(self,index):
        face = self.faces[index]
        print("Face of index {}, composed of:\n\t- a: {}\n\t- b: {}\n\t- c: {}\n\t- visibility: {}\n\t- state: {}".format(index,face.a,face.b,face.c,face.visible,face.state))
    
    def print_single_vertex(self,index):
        vertex = self.vertices[index]
        print("Vertex :\n\t- index in model: {}\n\t- index in vertex: {}\n\t- coordinates: {}\n\t- faces: {}\n\t- state: {}\n\t- retriangulation type: {}\n\t- visibility: {}".format(index,vertex.index,vertex.coordinates,vertex.faces,vertex.state,vertex.retriangulation_type,vertex.visible))

    def print_count_valencies(self):
        counts = []
        for index_vertex in range(len(self.vertices)):
            vertex = self.vertices[index_vertex]
            while len(counts) <= len(vertex.faces):
                counts.append(0)
            counts[len(vertex.faces)] += 1
        print("Count of vertex per valencies:")
        for valence in range(len(counts)):
            print("\t- {}: {}".format(valence,counts[valence]))


def parse_file(path):
    """
    Parses a file and returns the model.
    """
    model = Model()
    model.parse_file(path)
    return model


class Output:
    """
    The type for a model that outputs as obja.
    """

    def __init__(self, output, random_color=False):
        """
        Initializes the index mapping dictionaries.
        """
        self.vertex_mapping = dict()
        self.face_mapping = dict()
        self.output = output
        self.random_color = random_color

    def add_vertex(self, index, vertex):
        """
        Adds a new vertex to the model with the specified index.
        """
        self.vertex_mapping[index] = len(self.vertex_mapping)
        print('v {} {} {}'.format(vertex[0], vertex[1], vertex[2]), file=self.output)

    def edit_vertex(self, index, vertex):
        """
        Changes the coordinates of a vertex.
        """
        if len(self.vertex_mapping) == 0:
            print('ev {} {} {} {}'.format(index, vertex[0], vertex[1], vertex[2]), file=self.output)
        else:
            print('ev {} {} {} {}'.format(self.vertex_mapping[index] + 1, vertex[0], vertex[1], vertex[2]),
                  file=self.output)

    def add_face(self, index, face):
        """
        Adds a face to the model.
        """
        self.face_mapping[index] = len(self.face_mapping)
        print('f {} {} {}'.format(
            self.vertex_mapping[face.a] + 1,
            self.vertex_mapping[face.b] + 1,
            self.vertex_mapping[face.c] + 1,
        ),
            file=self.output
        )

        if self.random_color:
            print('fc {} {} {} {}'.format(
                len(self.face_mapping),
                random.uniform(0, 1),
                random.uniform(0, 1),
                random.uniform(0, 1)),
                file=self.output
            )

    def edit_face(self, index, face):
        """
        Changes the indices of the vertices of the specified face.
        """
        print('ef {} {} {} {}'.format(
            self.face_mapping[index] + 1,
            self.vertex_mapping[face.a] + 1,
            self.vertex_mapping[face.b] + 1,
            self.vertex_mapping[face.c] + 1
        ),
            file=self.output
        )


def main():
    if len(sys.argv) == 1:
        print("obja needs a path to an obja file")
        return

    model = parse_file(sys.argv[1])
    model.complete_model()

    print(model.vertices)
    print(model.faces)
    print(model.fov)
    print(model.state_flags)
    print(model.retirangulation_tags)



if __name__ == "__main__":
    main()
    
