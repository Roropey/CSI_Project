# Progressive Compression for Lossless Transmission of Triangle Meshes Implementation

As a project for the courses Modélisation, Compression, Streaming, Interactions 3D of the formation Image et MultiMédia of Sciences du Numérique Department of ENSEEIHT school. This git deposit is based on the git deposit: https://gitea.tforgione.fr/tforgione/obja. This implementation has for goal to take a manifold 3D obj model to generate the decimation based on the paper "Progressive Compression for Lossless Transmission of Triangle Meshes". The decimation is implemented in valence_driven_decimater.py program and the reconstruction based on the decimation output and decimation model is done by reconstruction.py.
The reconstruction.py program produced an obja file that shows the reconstruction progression iterations.

## decimate_and_recreate.py

This program is callable program to execute the implementation fully : from an input model to generate the obja output.

### Arguments

###### -it or --iterations

This arguments defined the maximum iteration number of decimating operations done to obtain the low resolution.
An integer is expected. The default value is 1000.
If the minimum number of vertices is reached before the maximum number of iteration, the decimation stopped.

###### -minPts or --minimum_points

This arguments defined the minimum number of vertices expected for the low resolution model output of the decimation. 
An integer is expected. The default value is 4.
If the maximum iteration number is reached before, the decimation stopped. 
The minimum vertices number is the maximum between this argument and the result of the minimum proportion argument.

###### -minProp or --minimum_proportion

This arguments defined the minimum number of vertices of the low resolution decimation result model based on the original vertices number.
A float is expected. The default value is None.
If the maximum iteration number is reached before, the decimation stopped. 
The minimum vertices number is the maximum between this argument time the original vertices number and the minimum point argument.

###### -input or --input_model

This argument corresponds to the path to the input/original model to be decimated.
A string is expected.

###### -outputDecimate or --output_decimating

This argument corresponds to the path or name of the low resolution model resulting from the decimation.
Put nothing if not wanted because the default value is None.
A string is expected.

###### -outputRecreate or --output_recreating

This argument corresponds to the path or name the reconstruction obja output that contains the reconstruction step.
A string is expected. The default value is "Output_Recreate.obja".

###### -colorintRecreating or --coloring_the_recreating

This argument is a boolean indicating if the obja output should contains patch coloration or not.
A boolean is expected. The default value is True.

###### -colorintRecreating or --coloring_the_recreating

This argument is a boolean indicating if at each recreating steps, the faces colors should be reset (put to white). Better to see the patch evolution at each step.
A boolean is expected. The default value is True.

## obja.py

This program is the based of the model manipulation and a modified version from the tforgione obja deposit. The modification contains function usefull for debugging program and manipulating model.

## valence_driven_decimater.py

This program contains the decimation part of the implementation. From a input model, it generates series of outputs and low resolution model.

## reconstruction.py

This program contains the reconstruction part of the implementationFrom a low resolution model and series of outputs, it produces an obja file that shows the reconstruction iterations.

## server.py and index.html

This files are from "https://gitea.tforgione.fr/tforgione/obja" and are used in the server.py program for display obja files in a browser. See "https://gitea.tforgione.fr/tforgione/obja" for how to execute.

## Original git files

This folder contains the original README and decimate.py program given by the https://gitea.tforgione.fr/tforgione/obja deposit.

## Results_obja

This folder contains produced obja from the recreating program.

## Test_Objects_low

In this folder are obj model made to develop and test the implementation.

## example

This folder contains the obj model used to test and measure the implementation. Some version of the obj are modified to be watertight (no hole) and so may change the manifold level.

## js and src

This two folders are used by server.py and are from the "https://gitea.tforgione.fr/tforgione/obja" deposit.
