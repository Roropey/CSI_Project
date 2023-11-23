import valence_driven_decimater as decimater
import reconstruction as reconstructor
import obja
with open('results_ouputs.txt', 'w') as output:

    # try:
    #     model = decimater.Decimater()
    #     model.parse_file('example/icosphere.obj')
    #     decimating_output = model.decimate(4,1000)
    #     model.save_f_by_f('Results_tests/DecimateAB_icosphere.obj')
    #     output.write('Work icosphere at decimating\n')
    # except:
    #     output.write('Fail icosphere at decimating\n')
    # try:
    #     decimating_output_bis = decimating_output.copy()
    #     reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/icosphere_reset_color.obja')
    #     reco_reset_color.copy(model)
    #     reconstruction = reco_reset_color.reconstruction(decimating_output)
    #     reco_reset_color.file.close()
    #     reco_white = reconstructor.Reconstructer(False,False,'Results_obja/icosphere_pure.obja')
    #     reco_white.copy(model)
    #     reconstruction = reco_white.reconstruction(decimating_output_bis)
    #     reco_white.file.close()
    #     output.write('Work icosphere at reconstruction\n')
    # except:
    #     output.write('Fail icosphere at reconstruction\n')

    # try:
    model = decimater.Decimater()
    model.parse_file('example/sphere_bis.obj')
    decimating_output = model.decimate(4,1000)
    model.save_f_by_f('Results_tests/DecimateAB_sphere_bis.obj')
    output.write('Work sphere_bis at decimating\n')
    # except:
    #     output.write('Fail sphere_bis at decimating\n')
    # try:
    decimating_output_bis = decimating_output.copy()
    reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/sphere_bis_reset_color.obja')
    reco_reset_color.copy(model)
    reconstruction = reco_reset_color.reconstruction(decimating_output)
    reco_reset_color.file.close()
    reco_white = reconstructor.Reconstructer(False,False,'Results_obja/sphere_bis_pure.obja')
    reco_white.copy(model)
    reconstruction = reco_white.reconstruction(decimating_output_bis)
    reco_white.file.close()
    output.write('Work sphere_bis at reconstruction\n')
    # except:
    #     output.write('Fail sphere_bis at reconstruction\n')

    # try:
    model = decimater.Decimater()
    model.parse_file('example/bunny_bis.obj')
    decimating_output = model.decimate(4,1000)
    model.save_f_by_f('Results_tests/DecimateAB_bunny_bis.obj')
    output.write('Work bunny_bis at decimating\n')
    # except:
    #     output.write('Fail bunny_bis at decimating\n')
    # try:
    decimating_output_bis = decimating_output.copy()
    reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/bunny_bis_reset_color.obja')
    reco_reset_color.copy(model)
    reconstruction = reco_reset_color.reconstruction(decimating_output)
    reco_reset_color.file.close()
    reco_white = reconstructor.Reconstructer(False,False,'Results_obja/bunny_bis_pure.obja')
    reco_white.copy(model)
    reconstruction = reco_white.reconstruction(decimating_output_bis)
    reco_white.file.close()
    output.write('Work bunny_bis at reconstruction\n')
    # except:
    #     output.write('Fail bunny_bis at reconstruction\n')

    # try:
    model = decimater.Decimater()
    model.parse_file('example/cow.obj')
    decimating_output = model.decimate(4,1000)
    model.save_f_by_f('Results_tests/DecimateAB_cow.obj')
    output.write('Work cow at decimating\n')
    # except:
    #     output.write('Fail cow at decimating\n')
    # try:
    decimating_output_bis = decimating_output.copy()
    reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/cow_reset_color.obja')
    reco_reset_color.copy(model)
    reconstruction = reco_reset_color.reconstruction(decimating_output)
    reco_reset_color.file.close()
    reco_white = reconstructor.Reconstructer(False,False,'Results_obja/cow_pure.obja')
    reco_white.copy(model)
    reconstruction = reco_white.reconstruction(decimating_output_bis)
    reco_white.file.close()
    output.write('Work cow at reconstruction\n')
    # except:
    #     output.write('Fail cow at reconstruction\n')

    # try:
    model = decimater.Decimater()
    model.parse_file('example/suzanne_bigger_bis.obj')
    decimating_output = model.decimate(4,1000)
    model.save_f_by_f('Results_tests/DecimateAB_suzanne_bigger_bis.obj')
    output.write('Work suzanne_bigger_bis at decimating\n')
    # except:
    #     output.write('Fail suzanne_bigger_bis at decimating\n')
    # try:
    decimating_output_bis = decimating_output.copy()
    reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/suzanne_bigger_bis_reset_color.obja')
    reco_reset_color.copy(model)
    reconstruction = reco_reset_color.reconstruction(decimating_output)
    reco_reset_color.file.close()
    reco_white = reconstructor.Reconstructer(False,False,'Results_obja/suzanne_bigger_bis_pure.obja')
    reco_white.copy(model)
    reconstruction = reco_white.reconstruction(decimating_output_bis)
    reco_white.file.close()
    output.write('Work suzanne_bigger_bis at reconstruction\n')
    # except:
    #     output.write('Fail suzanne_bigger_bis at reconstruction\n')

    try:
        model = decimater.Decimater()
        model.parse_file('example/fandisk.obj')
        decimating_output = model.decimate(4,1000)
        model.save_f_by_f('Results_tests/DecimateAB_fandisk.obj')
        output.write('Work fandisk at decimating\n')
    except:
        output.write('Fail fandisk at decimating\n')
    try:
        decimating_output_bis = decimating_output.copy()
        reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/fandisk_reset_color.obja')
        reco_reset_color.copy(model)
        reconstruction = reco_reset_color.reconstruction(decimating_output)
        reco_reset_color.file.close()
        reco_white = reconstructor.Reconstructer(False,False,'Results_obja/fandisk_pure.obja')
        reco_white.copy(model)
        reconstruction = reco_white.reconstruction(decimating_output_bis)
        reco_white.file.close()
        output.write('Work fandisk at reconstruction\n')
    except:
        output.write('Fail fandisk at reconstruction\n')

    try:
        model = decimater.Decimater()
        model.parse_file('example/pokemon.obj')
        decimating_output = model.decimate(104,1000)
        model.save_f_by_f('Results_tests/DecimateAB_pokemon.obj')
        output.write('Work pokemon at decimating\n')
    except:
        output.write('Fail pokemon at decimating\n')
    try:
        decimating_output_bis = decimating_output.copy()
        reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/pokemon_reset_color.obja')
        reco_reset_color.copy(model)
        reconstruction = reco_reset_color.reconstruction(decimating_output)
        reco_reset_color.file.close()
        reco_white = reconstructor.Reconstructer(False,False,'Results_obja/pokemon_pure.obja')
        reco_white.copy(model)
        reconstruction = reco_white.reconstruction(decimating_output_bis)
        reco_white.file.close()
        output.write('Work pokemon at reconstruction\n')
    except:
        output.write('Fail pokemon at reconstruction\n')

    try:
        model = decimater.Decimater()
        model.parse_file('example/hippo.obj')
        decimating_output = model.decimate(12,1000)
        model.save_f_by_f('Results_tests/DecimateAB_hippo.obj')
        output.write('Work hippo at decimating\n')
    except:
        output.write('Fail hippo at decimating\n')
    try:
        decimating_output_bis = decimating_output.copy()
        reco_reset_color = reconstructor.Reconstructer(True,True,'Results_obja/hippo_reset_color.obja')
        reco_reset_color.copy(model)
        reconstruction = reco_reset_color.reconstruction(decimating_output)
        reco_reset_color.file.close()
        reco_white = reconstructor.Reconstructer(False,False,'Results_obja/hippo_pure.obja')
        reco_white.copy(model)
        reconstruction = reco_white.reconstruction(decimating_output_bis)
        reco_white.file.close()
        output.write('Work hippo at reconstruction\n')
    except:
        output.write('Fail hippo at reconstruction\n')


    output.close()
