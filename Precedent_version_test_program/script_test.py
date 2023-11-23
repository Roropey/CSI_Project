import valence_driven_decimater_test as decimater
import reconstruction_test as reconstructor

with open('results_ouput_tests.txt', 'w') as output:

    try:
        model = decimater.Decimater()
        model.parse_file('example/Icosphere_2562_vertices.obj')
        decimating_output = model.decimate(250,20)
        model.save_f_by_f('Results_tests/DecimateAB_Icosphere_test.obj')
    except:
        output.write('Fail Icosphere at decimating\n')
# try:
    reco = reconstructor.Reconstructer(True,'Results_obja/Icosphere_test_reset_color.obja')
    reco.copy(model)
    reconstruction = reco.reconstruction(decimating_output)
    reco.file.close()
    output.write('Work suzanne_bis\n')
# v:
    output.write('Fail Icosphere at reconstruction\n')

    try:
        model = decimater.Decimater()
        model.parse_file('example/suzanne_bis.obj')
        decimating_output = model.decimate(50,20)
        model.save_f_by_f('Results_tests/DecimateAB_suzanne_bis_test.obj')
    except:
        output.write('Fail suzanne_bis at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/suzanne_bis_test_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work suzanne_bis\n')
    except:
        output.write('Fail suzanne_bis at reconstruction\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/bunny_bis_bis.obj')
        decimating_output = model.decimate(250,20)
        model.save_f_by_f('Results_tests/DecimateAB_bunny_bis_bis_test.obj')
    except:
        output.write('Fail bunny_bis_bis at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/bunny_bis_bis_test_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work bunny_bis_bis\n')
    except:
        output.write('Fail bunny_bis_bis at reconstruction\n')
    

    try:
        model = decimater.Decimater()
        model.parse_file('example/cow.obj')
        decimating_output = model.decimate(290,20)
        model.save_f_by_f('Results_tests/DecimateAB_cow_test.obj')
    except:
        output.write('Fail cow at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/cow_test_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work cow\n')
    except:
        output.write('Fail cow at reconstruction\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/fandisk.obj',15641)
        decimating_output = model.decimate(2000,20)
        model.save_f_by_f('Results_tests/DecimateAB_fandisk_test.obj')
    except:
        output.write('Fail fandisk at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/fandisk_test_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work fandisk\n')
    except:
        output.write('Fail fandisk at reconstruction\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/hippo.obj')
        decimating_output = model.decimate(3200,20)
        model.save_f_by_f('Results_tests/DecimateAB_hippo_test.obj')
    except:
        output.write('Fail hippo at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/hippo_test_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work hippo\n')
    except:
        output.write('Fail hippo at reconstruction\n')

    output.close()