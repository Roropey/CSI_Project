import valence_driven_decimater_v2 as decimater
import reconstruction_v2 as reconstructor
import obja
with open('results_ouputs.txt', 'w') as output:

    # try:
    model = decimater.Decimater()
    model.parse_file('example/cow.obj')
    decimating_output = model.decimate(4,1000)
    model.save_f_by_f('Results_tests/DecimateAB_cow.obj')
    # except:
    #     output.write('Fail cow at decimating\n')
    # try:
    reco = reconstructor.Reconstructer(True,True,'Results_obja/cow_reset_color.obja')
    reco.copy(model)
    reconstruction = reco.reconstruction(decimating_output)
    reco.file.close()
    output.write('Work cow\n')
    # except:
    #     output.write('Fail cow at reconstruction\n')
    
    raise Exception('Stop')
    try:
        model = decimater.Decimater()
        model.parse_file('example/icosphere.obj')
        decimating_output = model.decimate(4,20)
        model.save_f_by_f('Results_tests/DecimateAB_icosphere.obj')
    except:
        output.write('Fail icosphere at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/icosphere_reset_color_v2.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        m=obja.Model()
        m.parse_file('example/icosphere.obj')
        print(m.equal(reco))
        print(reco.equal(m))
        output.write('Work icosphere\n')
    except:
        output.write('Fail icosphere at reconstruction\n')
    
    try:
        model = decimater.Decimater()
        model.parse_file('example/bunny_bis_bis.obj')
        decimating_output = model.decimate(250,20)
        model.save_f_by_f('Results_tests/DecimateAB_bunny_bis_bis.obj')
    except:
        output.write('Fail bunny_bis_bis at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/bunny_bis_bis_reset_color.obja')
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
        model.save_f_by_f('Results_tests/DecimateAB_cow.obj')
    except:
        output.write('Fail cow at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/cow_reset_color.obja')
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
        model.save_f_by_f('Results_tests/DecimateAB_fandisk.obj')
    except:
        output.write('Fail fandisk at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/fandisk_reset_color.obja')
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
        model.save_f_by_f('Results_tests/DecimateAB_hippo.obj')
    except:
        output.write('Fail hippo at decimating\n')
    try:
        reco = reconstructor.Reconstructer(True,'Results_obja/hippo_reset_color.obja')
        reco.copy(model)
        reconstruction = reco.reconstruction(decimating_output)
        reco.file.close()
        output.write('Work hippo\n')
    except:
        output.write('Fail hippo at reconstruction\n')

    output.close()
