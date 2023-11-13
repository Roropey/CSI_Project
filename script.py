import valence_driven_decimater as decimater
import reconstruction as reconstructor

with open('results_ouput.txt', 'w') as output:
    
    try:
        model = decimater.Decimater()
        model.parse_file('example/bunny_bis.obj')
        decimating_output = model.decimate(250,20)
        model.save_f_by_f('Results_tests/DecimateAB_bunny_bis.obj')
        reco = reconstructor.Reconstructer(True,'Results_obja/bunny_bis_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work bunny_bis\n')
    except:
        output.write('Fail bunny_bis\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/suzanne_bis.obj')
        decimating_output = model.decimate(50,20)
        model.save_f_by_f('Results_tests/DecimateAB_suzanne_bis.obj')
        reco = reconstructor.Reconstructer(True,'Results_obja/suzanne_bis_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work suzanne_bis\n')
    except:
        output.write('Fail suzanne_bis\n')

    try:
        model = decimater.Decimater()
        model.parse_file('example/cow.obj')
        decimating_output = model.decimate(290,20)
        model.save_f_by_f('Results_tests/DecimateAB_cow.obj')
        reco = reconstructor.Reconstructer(True,'Results_obja/cow_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work cow\n')
    except:
        output.write('Fail cow\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/fandisk.obj',15641)
        decimating_output = model.decimate(2000,20)
        model.save_f_by_f('Results_tests/DecimateAB_fandisk.obj')
        reco = reconstructor.Reconstructer(True,'Results_obja/fandisk_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work fandisk\n')
    except:
        output.write('Fail fandisk\n')
    try:
        model = decimater.Decimater()
        model.parse_file('example/hippo.obj')
        decimating_output = model.decimate(3200,20)
        model.save_f_by_f('Results_tests/DecimateAB_hippo.obj')
        reco = reconstructor.Reconstructer(True,'Results_obja/hippo_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work hippo\n')
    except:
        output.write('Fail hippo\n')

    output.close()