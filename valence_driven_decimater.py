import obja
import numpy as np
import sys
import random
class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()

    def dacimateA(self, output):
        print("ok")
        # init
        faces_init = self.faces[random.randint(0, len(self.faces))]
        
       

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
