# Progressive Compression for Lossless Transmission of Triangle Meshes Implementation

As a project for the courses Modélisation, Compression, Streaming, Interactions 3D of the formation Image et MultiMédia of Sciences du Numérique Department of ENSEEIHT school, we have to implement a 3D object compression method for streaming. The file "ProjetCSI2023.pdf" corresponds to the project description.  This git deposit is based on the git deposit: https://gitea.tforgione.fr/tforgione/obja. This implementation has for goal to take a manifold 3D obj model to generate the decimation based on the paper "Progressive Compression for Lossless Transmission of Triangle Meshes" (4.AlliezDesbrun01.pdf file). The decimation is implemented in valence_driven_decimater.py program and the reconstruction based on the decimation output and decimation model is done by reconstruction.py.
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

## script.py

script.py program correspond to an execution of the decimation and reconstruction of multiple obj model in example folder. The goal is to produce the obja file of the reconstruction with the color at each step of reconstruction and a colorless version to have a less big file to be upload on a measurement file.

## Original git, js and src folder, server.py and index.html

The folder "Original git" contains the original README and decimate.py program given by the https://gitea.tforgione.fr/tforgione/obja deposit. "jc" and "src" folder are used by server.py and are from the git deposit.
The files are from the git deposit and are used in the server.py program for display obja files in a browser. See "https://gitea.tforgione.fr/tforgione/obja" for how to execute.

## Results_obja

This folder contains produced obja from the recreating program.

## Test_Objects_low and example

This 2 folder containsobj model used to develop, test and measure the implementation. Some version of the obj are modified (_bis version) to be watertight (no hole) and so may change the manifold level.

## Precedent_version_test_program

The precedent version and test of the programs valence_driven_decimater.py and reconstruction.py are stocked in this folder.
The v0 programs doesn't handle creation of valence 2 well compared to actual implementation: the v0 is more computation hungry because it tries the decimation on every gate possible until finding a decimation that do not produce a valence of 2. In addition of being too long to be used, it doesn't work on certain model like bunny_bis.obj where at the first decimation, all gates possible (all faces times 3) are tried but without success, and so no decimation done.
The test programs is a quick try to handle valence of 2 decimation, but without success. This is because having gates that share two faces cause problems (errors) in many part of the implementation and correcting it would required a full reimplementation of everything, something that cann't be done in the remaining time (before the project end).

## Elements_of_presentation 

This folder contains elements (like videos) related to the presentation done the 24/11/2023.

## Elements of progress

Due to lacking time, some ideas of progression were not implemented.

### Reuse of existing faces

In the implementation, when the retriangulation occured, we remove faces by making them invisible and create new one (in both decimation and reconstruction). This implementation causes to increase the size of the model by having more and more faces unused and created a second time in the reconstruction. The idea of reusing faces during retriangulation is to just modified previously decimated by changing one or 2 vertex of the face. This idea of implementation can decrease the number of line in the obja file by changing two line of removing and creating a face to a line with the command "efv". We can observed the suppression in the obja retriangulation because we can see holes some time, but we can hope to less view hope by using the "efv" command instead of removing all faces and after creating new one.

### Finding solutions for not watertight model, valence of 1 and 2

One the model given is "pokemon.obj". This model block with our implementation because of vertices with valence of 1 and 2 in the original file. This case of valence of 1 and 2 are not managed by our implemenation. This forced us to modified some model to be used. Better research and time can be used to find implementable solution.

### Stopping decimation by face

At the moment, the decimation stopped by a limit of iteration and a minimum number of vertices (or proportion compared to the original), but we can think of counting also the faces to be limit of decimation.

### Stopping decimation based on metrics

As before, we can change the condition of stopping the decimation with another one. By implementing a metrics, we could choose to decomposed the model until reaching a certain amount of loss in detail. This could help producing at the output of the decimation different level of detail (LoD) model to be used in an application like a game of an 3D animation.
