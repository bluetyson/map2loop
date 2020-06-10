# from map2loop import m2l_topology
import networkx as nx
import random
import numpy as np
import pandas as pd
import os


##########################################################################
# Save out and compile taskfile needed to generate geomodeller model using the geomodellerbatch engine
#
# loop2geomodeller(test_data_path,tmp_path,output_path,save_faults,compute_etc)
# Args:
# test_data_path root directory of test data
# tmp_path directory of temporary outputs
# output_path directory of outputs
# ave_faults flag for saving faults or not
# compute_etc flag for actual calculations or just project output
#
# Creates geomodeller taskfile files from varous map2loop outputs
##########################################################################
def loop2geomodeller(model_name,test_data_path,tmp_path,output_path,dtm_file,bbox,model_top,model_base,save_faults,compute_etc,workflow):

    f=open(test_data_path+'/'+model_name+'/m2l.taskfile','w')
    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Project Header-----------------------\n')
    f.write('#---------------------------------------------------------------\n')
    f.write('name: "UWA_Intrepid"\n')
    f.write('description: "Automate_batch_Model"\n')
    f.write('    GeomodellerTask {\n')
    f.write('    CreateProject {\n')
    f.write('        name: "Hamersley"\n')
    f.write('        author: "Mark"\n')
    f.write('        date: "23/10/2019  0: 0: 0"\n')
    f.write('        projection { map_projection: "GDA94 / MGA50"}\n')
    f.write('        version: "2.0"\n')
    f.write('        units: meters\n')
    f.write('        precision: 1.0\n')
    f.write('        Extents {\n')
    f.write('            xmin: '+str(bbox[0])+'\n')
    f.write('            ymin: '+str(bbox[1])+'\n')
    f.write('            zmin: '+str(model_base)+'\n')
    f.write('            xmax: '+str(bbox[2])+'\n')
    f.write('            ymax: '+str(bbox[3])+'\n')
    f.write('            zmax: '+str(model_top)+'\n')
    f.write('        }\n')
    f.write('        deflection2d: 0.001\n')
    f.write('        deflection3d: 0.001\n')
    f.write('        discretisation: 10.0\n')
    f.write('        referenceTop: false\n')
    f.write('        CustomDTM {\n')
    f.write('            Extents {\n')
    f.write('            xmin: '+str(bbox[0])+'\n')
    f.write('            ymin: '+str(bbox[1])+'\n')
    f.write('            xmax: '+str(bbox[2])+'\n')
    f.write('            ymax: '+str(bbox[3])+'\n')
    f.write('            }\n')
    f.write('            name: "Topography"\n')
    f.write('            filename {\n')
    f.write('                Grid_Name: "'+dtm_file+'"\n')
    f.write('            }\n')
    f.write('            nx: 10\n')
    f.write('            ny: 10\n')
    f.write('        }\n')
    f.write('    }\n')
    f.write('}\n')


    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')

    empty_fm=[]

    for indx,afm in all_sorts.iterrows():
        foundcontact=False
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] in afm['code']):
                foundcontact=True
                break
        foundorientation=False
        for indx3,ano in orientations.iterrows():
            if(ano['formation'] in afm['code']):
                foundorientation=True
                break
        if(not foundcontact or not foundorientation):
            empty_fm.append(afm['code'])

    #print(empty_fm)

    all_sorts=np.genfromtxt(tmp_path+'all_sorts_clean.csv',delimiter=',',dtype='U100')
    nformations=len(all_sorts)

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Create Formations-----------------------\n')
    f.write('#---------------------------------------------------------------\n')
       
    for i in range (1,nformations):
        if( not all_sorts[i,4] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('CreateFormation {\n')

            ostr='    name: "'+all_sorts[i,4].replace("\n","")+'"\n'
            f.write(ostr)

            ostr='    red: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            ostr='    green: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            ostr='    blue: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Set Stratigraphic Pile------------------\n')
    f.write('#---------------------------------------------------------------\n')
      
             
    for i in range (1,nformations):
    #for i in range (nformations-1,0,-1):
        if(all_sorts[i,2]==str(1)):
            f.write('GeomodellerTask {\n')
            f.write('SetSeries {\n')

            ostr='    name: "'+all_sorts[i][5].replace("\n","")+'"\n'
            f.write(ostr)

            ostr='    position: 1\n'
            f.write(ostr)

            ostr='    relation: "erode"\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')

            for j in range(nformations-1,0,-1):
    #        for j in range(1,nformations):
                if(all_sorts[j,1]==all_sorts[i,1]):
                    if( not all_sorts[j][4] in empty_fm):
                        f.write('GeomodellerTask {\n')
                        f.write('AddFormationToSeries {\n')

                        ostr='    series: "'+all_sorts[j][5]+'"\n'
                        f.write(ostr)

                        ostr='    formation: "'+all_sorts[j][4]+'"\n'
                        f.write(ostr)

                        f.write('    }\n')
                        f.write('}\n')    

    if(save_faults):
        output_path=test_data_path+'output/'

        faults_len=pd.read_csv(output_path+'fault_dimensions.csv')

        n_allfaults=len(faults_len)

        fcount=0
        for i in range(0,n_allfaults):
            f.write('GeomodellerTask {\n')
            f.write('CreateFault {\n')
            ostr='    name: "'+faults_len.iloc[i]["Fault"]+'"\n'
            f.write(ostr)

            ostr='    red: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            ostr='    green: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            ostr='    blue: '+str(random.randint(1,256)-1)+'\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')
            fcount=fcount+1
            
            f.write('GeomodellerTask {\n')
            f.write('    Set3dFaultLimits {\n')
            f.write('        Fault_name: "'+faults_len.iloc[i]["Fault"]+ '"\n')
            f.write('        Horizontal: '+str(faults_len.iloc[i]["HorizontalRadius"])+ '\n')
            f.write('        Vertical: '+str(faults_len.iloc[i]["VerticalRadius"])+ '\n')
            f.write('        InfluenceDistance: '+str(faults_len.iloc[i]["InfluenceDistance"])+ '\n')
            f.write('    }\n')
            f.write('}\n')
            

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Import 3D contact data ---Base Model----\n')
    f.write('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(afm[0])
        if( not afm['code'] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('    Add3DInterfacesToFormation {\n')
            f.write('          formation: "'+str(afm['code'])+'"\n')

            for indx2,acontact in contacts.iterrows():
                if(acontact['formation'] in afm['code'] ):
                    ostr='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                    f.write(ostr)
            f.write('    }\n')
            f.write('}\n')
    f.write('#---------------------------------------------------------------\n')
    f.write('#------------------Import 3D orientation data ---Base Model-----\n')
    f.write('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(groups[agp])
        if( not afm['code'] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('    Add3DFoliationToFormation {\n')
            f.write('          formation: "'+str(afm['code'])+'"\n')
            for indx2,ano in orientations.iterrows():
                if(ano['formation'] in afm['code']):
                    f.write('           foliation {\n')
                    ostr='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                    f.write(ostr)
                    ostr='                  direction: '+str(ano['azimuth'])+'\n'
                    f.write(ostr)
                    ostr='                  dip: '+str(ano['dip'])+'\n'
                    f.write(ostr)
                    if(ano['polarity']==1):
                        ostr='                  polarity: Normal_Polarity\n'
                    else:
                        ostr='                  polarity: Reverse_Polarity\n'
                    f.write(ostr)            
                    ostr='           }\n'
                    f.write(ostr)
            f.write('    }\n')
            f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Import 3D fault data ---Base Model------\n')
    f.write('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'faults.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        f.write('GeomodellerTask {\n')
        f.write('    Add3DInterfacesToFormation {\n')
        f.write('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] == afault['Fault']):
                ostr='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                f.write(ostr)
        f.write('    }\n')
        f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#------------------Import 3D fault orientation data ------------\n')
    f.write('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'fault_orientations.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        f.write('GeomodellerTask {\n')
        f.write('    Add3DFoliationToFormation {\n')
        f.write('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,ano in orientations.iterrows():
            if(ano['formation'] == afault['Fault']):
                f.write('           foliation {\n')
                ostr='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                f.write(ostr)
                ostr='                  direction: '+str(ano['DipDirection'])+'\n'
                f.write(ostr)
                if(ano['dip'] == -999):
                    ostr='                  dip: '+str(random.randint(60,90))+'\n'
                else:    
                    ostr='                  dip: '+str(ano['dip'])+'\n'
                f.write(ostr)
                if(ano['DipPolarity']==1):
                    ostr='                  polarity: Normal_Polarity\n'
                else:
                    ostr='                  polarity: Reverse_Polarity\n'
                f.write(ostr)            
                ostr='           }\n'
                f.write(ostr)
        f.write('    }\n')
        f.write('}\n')

    if(save_faults):
        G=nx.read_gml(tmp_path+"fault_network.gml",label='label')
        #nx.draw(G, with_labels=True, font_weight='bold')
        edges=list(G.edges)
        #for i in range(0,len(edges)):
            #print(edges[i][0],edges[i][1])
        cycles=list(nx.simple_cycles(G))
        #display(cycles)
        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Link faults with faults ----------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    LinkFaultsWithFaults {\n')

        for i in range(0,len(edges)):
                found=False
                for j in range(0,len(cycles)):
                    if(edges[i][0]== cycles[j][0] and edges[i][1]== cycles[j][1]):
                        found=True # fault pair is first two elements in a cycle list so don't save to taskfile
                if(not found):
                    ostr='        FaultStopsOnFaults{ fault: "'+edges[i][1]+'"; stopson: "'+edges[i][0]+'"}\n'
                    f.write(ostr)

        f.write('    }\n')
        f.write('}\n')

    if(save_faults):
        all_fault_group=np.genfromtxt(output_path+'group-fault-relationships.csv',delimiter=',',dtype='U100')
        ngroups=len(all_fault_group)
        all_fault_group=np.transpose(all_fault_group)
        nfaults=len(all_fault_group)

        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Link series with faults ----------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    LinkFaultsWithSeries {\n')

        for i in range(1,nfaults):
            first=True
            for j in range(1,ngroups):
                if(all_fault_group[i,j]==str(1)):
                    if(first):
                        ostr='    FaultSeriesLinks{ fault: "'+all_fault_group[i,0]+'"; series: ['
                        f.write(ostr)
                        ostr='"'+all_fault_group[0,j]+'"'
                        f.write(ostr)
                        first=False
                    else:
                        ostr=', "'+all_fault_group[0,j]+'"'
                        f.write(ostr)
            if(not first):
                ostr=']}\n'
                f.write(ostr)

        f.write('    }\n')
        f.write('}\n')
    

    f.write('GeomodellerTask {\n')
    f.write('    SaveProjectAs {\n')
    f.write('        filename: "./'+model_name+'.xml"\n')
    f.write('    }\n')
    f.write('}\n')
    f.close()
    

    if(compute_etc):
        f=open(test_data_path+model_name+'/'+'m2l_compute.taskfile','w')
        f.write('#---------------------------------------------------------------\n')
        f.write('#----------------------------Load Model----------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    OpenProjectNoGUI {\n')
        f.write('        filename: "./'+model_name+'.xml"\n')
        f.write('    }\n')
        f.write('}\n')
     
        f.write('#---------------------------------------------------------------\n')
        f.write('#----------------------------Compute Model----------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
        f.write('GeomodellerTask {\n')
        f.write('    ComputeModel {\n')
        f.write('        SeriesList {\n')
        f.write('            node: "All" \n')
        f.write('        }\n')
        f.write('        SectionList {\n')
        f.write('            node: "All"\n')
        f.write('        }\n')
        f.write('        FaultList {\n')
        f.write('            node: "All"\n')
        f.write('        }\n')
        f.write('        radius: 10.0\n')
        f.write('    }\n')
        f.write('}\n')

        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Add geophysical Properties--------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('#--------------------------Export Lithology Voxet---------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    SaveLithologyVoxet {\n')
        f.write('        nx: 25\n')
        f.write('        ny: 25\n')
        f.write('        nz: 40\n')
        f.write('        LithologyVoxetFileStub: "./Litho_Voxet/LithoVoxet.vo"\n')
        f.write('    }\n')
        f.write('}\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('#--------------------------Save As Model------------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
    
        f.write('GeomodellerTask {\n')
        f.write('    SaveProjectAs {\n')
        f.write('        filename: "/'+model_name+'.xml"\n')
        f.write('    }\n')
        f.write('}\n')   
        f.write('GeomodellerTask {\n')
        f.write('    CloseProjectNoGUI {\n')
        f.write('    }\n')
        f.write('}\n')

        f.close()
        
# same same expect it builds a list that then gets written all at once (this version is slower!)        
def loop2geomodeller2(model_name,test_data_path,tmp_path,output_path,dtm_file,bbox,save_faults,compute_etc,workflow):

    f=open(test_data_path+'/'+model_name+'/m2l.taskfile','w')
    ostr=[]
    
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Project Header-----------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('name: "UWA_Intrepid"\n')
    ostr.append('description: "Automate_batch_Model"\n')
    ostr.append('    GeomodellerTask {\n')
    ostr.append('    CreateProject {\n')
    ostr.append('        name: "Hamersley"\n')
    ostr.append('        author: "Mark"\n')
    ostr.append('        date: "23/10/2019  0: 0: 0"\n')
    ostr.append('        projection { map_projection: "GDA94 / MGA50"}\n')
    ostr.append('        version: "2.0"\n')
    ostr.append('        units: meters\n')
    ostr.append('        precision: 1.0\n')
    ostr.append('        Extents {\n')
    ostr.append('            xmin: '+str(bbox[0])+'\n')
    ostr.append('            ymin: '+str(bbox[1])+'\n')
    ostr.append('            zmin: -7000\n')
    ostr.append('            xmax: '+str(bbox[2])+'\n')
    ostr.append('            ymax: '+str(bbox[3])+'\n')
    ostr.append('            zmax: 1200\n')
    ostr.append('        }\n')
    ostr.append('        deflection2d: 0.001\n')
    ostr.append('        deflection3d: 0.001\n')
    ostr.append('        discretisation: 10.0\n')
    ostr.append('        referenceTop: false\n')
    ostr.append('        CustomDTM {\n')
    ostr.append('            Extents {\n')
    ostr.append('            xmin: '+str(bbox[0])+'\n')
    ostr.append('            ymin: '+str(bbox[1])+'\n')
    ostr.append('            xmax: '+str(bbox[2])+'\n')
    ostr.append('            ymax: '+str(bbox[3])+'\n')
    ostr.append('            }\n')
    ostr.append('            name: "Topography"\n')
    ostr.append('            filename {\n')
    ostr.append('                Grid_Name: "'+dtm_file+'"\n')
    ostr.append('            }\n')
    ostr.append('            nx: 10\n')
    ostr.append('            ny: 10\n')
    ostr.append('        }\n')
    ostr.append('    }\n')
    ostr.append('}\n')


    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')

    empty_fm=[]

    for indx,afm in all_sorts.iterrows():
        foundcontact=False
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] in afm['code']):
                foundcontact=True
                break
        foundorientation=False
        for indx3,ano in orientations.iterrows():
            if(ano['formation'] in afm['code']):
                foundorientation=True
                break
        if(not foundcontact or not foundorientation):
            empty_fm.append(afm['code'])

    #print(empty_fm)

    all_sorts=np.genfromtxt(tmp_path+'all_sorts_clean.csv',delimiter=',',dtype='U100')
    nformations=len(all_sorts)

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Create Formations-----------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
       
    for i in range (1,nformations):
        if( not all_sorts[i,4] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('CreateFormation {\n')

            ostr2='    name: "'+all_sorts[i,4].replace("\n","")+'"\n'
            ostr.append(ostr2)

            ostr2='    red: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    green: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    blue: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Set Stratigraphic Pile------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
      
             
    for i in range (1,nformations):
    #for i in range (nformations-1,0,-1):
        if(all_sorts[i,2]==str(1)):
            ostr.append('GeomodellerTask {\n')
            ostr.append('SetSeries {\n')

            ostr2='    name: "'+all_sorts[i][5].replace("\n","")+'"\n'
            ostr.append(ostr2)

            ostr2='    position: 1\n'
            ostr.append(ostr2)

            ostr2='    relation: "erode"\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')

            for j in range(nformations-1,0,-1):
    #        for j in range(1,nformations):
                if(all_sorts[j,1]==all_sorts[i,1]):
                    if( not all_sorts[j][4] in empty_fm):
                        ostr.append('GeomodellerTask {\n')
                        ostr.append('AddFormationToSeries {\n')

                        ostr2='    series: "'+all_sorts[j][5]+'"\n'
                        ostr.append(ostr2)

                        ostr2='    formation: "'+all_sorts[j][4]+'"\n'
                        ostr.append(ostr2)

                        ostr.append('    }\n')
                        ostr.append('}\n')    

    if(save_faults):
        output_path=test_data_path+'output/'

        faults_len=pd.read_csv(output_path+'fault_dimensions.csv')

        n_allfaults=len(faults_len)

        fcount=0
        for i in range(0,n_allfaults):
            ostr.append('GeomodellerTask {\n')
            ostr.append('CreateFault {\n')
            ostr2='    name: "'+faults_len.iloc[i]["Fault"]+'"\n'
            ostr.append(ostr2)

            ostr2='    red: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    green: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    blue: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')
            fcount=fcount+1
            
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Set3dFaultLimits {\n')
            ostr.append('        Fault_name: "'+faults_len.iloc[i]["Fault"]+ '"\n')
            ostr.append('        Horizontal: '+str(faults_len.iloc[i]["HorizontalRadius"])+ '\n')
            ostr.append('        Vertical: '+str(faults_len.iloc[i]["VerticalRadius"])+ '\n')
            ostr.append('        InfluenceDistance: '+str(faults_len.iloc[i]["InfluenceDistance"])+ '\n')
            ostr.append('    }\n')
            ostr.append('}\n')
            

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Import 3D contact data ---Base Model----\n')
    ostr.append('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(afm[0])
        if( not afm['code'] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Add3DInterfacesToFormation {\n')
            ostr.append('          formation: "'+str(afm['code'])+'"\n')

            for indx2,acontact in contacts.iterrows():
                if(acontact['formation'] in afm['code'] ):
                    ostr2='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                    ostr.append(ostr2)
            ostr.append('    }\n')
            ostr.append('}\n')
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#------------------Import 3D orientation data ---Base Model-----\n')
    ostr.append('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(groups[agp])
        if( not afm['code'] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Add3DFoliationToFormation {\n')
            ostr.append('          formation: "'+str(afm['code'])+'"\n')
            for indx2,ano in orientations.iterrows():
                if(ano['formation'] in afm['code']):
                    ostr.append('           foliation {\n')
                    ostr2='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                    ostr.append(ostr2)
                    ostr2='                  direction: '+str(ano['azimuth'])+'\n'
                    ostr.append(ostr2)
                    ostr2='                  dip: '+str(ano['dip'])+'\n'
                    ostr.append(ostr2)
                    if(ano['polarity']==1):
                        ostr2='                  polarity: Normal_Polarity\n'
                    else:
                        ostr2='                  polarity: Reverse_Polarity\n'
                    ostr.append(ostr2)            
                    ostr2='           }\n'
                    ostr.append(ostr2)
            ostr.append('    }\n')
            ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Import 3D fault data ---Base Model------\n')
    ostr.append('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'faults.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        ostr.append('GeomodellerTask {\n')
        ostr.append('    Add3DInterfacesToFormation {\n')
        ostr.append('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] == afault['Fault']):
                ostr2='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                ostr.append(ostr2)
        ostr.append('    }\n')
        ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#------------------Import 3D fault orientation data ------------\n')
    ostr.append('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'fault_orientations.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        ostr.append('GeomodellerTask {\n')
        ostr.append('    Add3DFoliationToFormation {\n')
        ostr.append('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,ano in orientations.iterrows():
            if(ano['formation'] == afault['Fault']):
                ostr.append('           foliation {\n')
                ostr2='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                ostr.append(ostr2)
                ostr2='                  direction: '+str(ano['DipDirection'])+'\n'
                ostr.append(ostr2)
                if(ano['dip'] == -999):
                    ostr2='                  dip: '+str(random.randint(60,90))+'\n'
                else:    
                    ostr2='                  dip: '+str(ano['dip'])+'\n'
                ostr.append(ostr2)
                if(ano['DipPolarity']==1):
                    ostr2='                  polarity: Normal_Polarity\n'
                else:
                    ostr2='                  polarity: Reverse_Polarity\n'
                ostr.append(ostr2)            
                ostr2='           }\n'
                ostr.append(ostr2)
        ostr.append('    }\n')
        ostr.append('}\n')

    if(save_faults):
        G=nx.read_gml(tmp_path+"fault_network.gml",label='label')
        #nx.draw(G, with_labels=True, font_weight='bold')
        edges=list(G.edges)
        #for i in range(0,len(edges)):
            #print(edges[i][0],edges[i][1])
        cycles=list(nx.simple_cycles(G))
        #display(cycles)
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Link faults with faults ----------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    LinkFaultsWithFaults {\n')

        for i in range(0,len(edges)):
                found=False
                for j in range(0,len(cycles)):
                    if(edges[i][0]== cycles[j][0] and edges[i][1]== cycles[j][1]):
                        found=True # fault pair is first two elements in a cycle list so don't save to taskfile
                if(not found):
                    ostr2='        FaultStopsOnFaults{ fault: "'+edges[i][1]+'"; stopson: "'+edges[i][0]+'"}\n'
                    ostr.append(ostr2)

        ostr.append('    }\n')
        ostr.append('}\n')

    if(save_faults):
        all_fault_group=np.genfromtxt(output_path+'group-fault-relationships.csv',delimiter=',',dtype='U100')
        ngroups=len(all_fault_group)
        all_fault_group=np.transpose(all_fault_group)
        nfaults=len(all_fault_group)

        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Link series with faults ----------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    LinkFaultsWithSeries {\n')

        for i in range(1,nfaults):
            first=True
            for j in range(1,ngroups):
                if(all_fault_group[i,j]==str(1)):
                    if(first):
                        ostr2='    FaultSeriesLinks{ fault: "'+all_fault_group[i,0]+'"; series: ['
                        ostr.append(ostr2)
                        ostr2='"'+all_fault_group[0,j]+'"'
                        ostr.append(ostr2)
                        first=False
                    else:
                        ostr2=', "'+all_fault_group[0,j]+'"'
                        ostr.append(ostr2)
            if(not first):
                ostr2=']}\n'
                ostr.append(ostr2)

        ostr.append('    }\n')
        ostr.append('}\n')
    

    ostr.append('GeomodellerTask {\n')
    ostr.append('    SaveProjectAs {\n')
    ostr.append('        filename: "./'+model_name+'.xml"\n')
    ostr.append('    }\n')
    ostr.append('}\n')
    f.close()
    

    if(compute_etc):
        f=open(test_data_path+model_name+'/'+'m2l_compute.taskfile','w')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#----------------------------Load Model----------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    OpenProjectNoGUI {\n')
        ostr.append('        filename: "./'+model_name+'.xml"\n')
        ostr.append('    }\n')
        ostr.append('}\n')
     
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#----------------------------Compute Model----------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    ComputeModel {\n')
        ostr.append('        SeriesList {\n')
        ostr.append('            node: "All" \n')
        ostr.append('        }\n')
        ostr.append('        SectionList {\n')
        ostr.append('            node: "All"\n')
        ostr.append('        }\n')
        ostr.append('        FaultList {\n')
        ostr.append('            node: "All"\n')
        ostr.append('        }\n')
        ostr.append('        radius: 10.0\n')
        ostr.append('    }\n')
        ostr.append('}\n')

        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Add geophysical Properties--------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
        ostr.append('\n')
        ostr.append('\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#--------------------------Export Lithology Voxet---------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    SaveLithologyVoxet {\n')
        ostr.append('        nx: 25\n')
        ostr.append('        ny: 25\n')
        ostr.append('        nz: 40\n')
        ostr.append('        LithologyVoxetFileStub: "./Litho_Voxet/LithoVoxet.vo"\n')
        ostr.append('    }\n')
        ostr.append('}\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#--------------------------Save As Model------------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
    
        ostr.append('GeomodellerTask {\n')
        ostr.append('    SaveProjectAs {\n')
        ostr.append('        filename: "/'+model_name+'.xml"\n')
        ostr.append('    }\n')
        ostr.append('}\n')   
        ostr.append('GeomodellerTask {\n')
        ostr.append('    CloseProjectNoGUI {\n')
        ostr.append('    }\n')
        ostr.append('}\n')
        f.writelines(ostr)
        f.close()

from pyamg import solve
def solve_pyamg(A,B):
    return solve(A,B,verb=False,tol=1e-8)

##########################################################################
# Import outputs from map2loop to LoopStructural and view with Lavavu
#
# loop2LoopStructural(thickness_file,orientation_file,contacts_file,bbox)
# Args:
# thickness_file path of fornation thickness file
# orientation_file path of orientations file
# contacts_file path of contacts file
# bbox model bounding box
#
# Calculates model and displays in LavaVu wthin notebook
##########################################################################
def loop2LoopStructural(thickness_file,orientation_file,contacts_file,tmp_path,bbox):
    from LoopStructural import GeologicalModel
    from LoopStructural.visualisation import LavaVuModelViewer
    import lavavu

    all_sorts = pd.read_csv(tmp_path+'all_sorts_clean.csv')

    df = pd.read_csv(thickness_file)
    
    thickness = {}
    for f in df['formation'].unique():
        thickness[f] = np.mean(df[df['formation']==f]['thickness'])

    #display(thickness)
    order={}
    for ind,fm in all_sorts.iterrows():
        if(fm['code'] in df['formation'].unique()):
            order[fm['code']]=fm['code']
    """order = ['P__TKa_xs_k','P__TKo_stq','P__TKk_sf','P__TK_s',
    'A_HAu_xsl_ci', 'A_HAd_kd', 'A_HAm_cib', 'A_FOj_xs_b',
    'A_FO_xo_a', 'A_FO_od', 'A_FOu_bbo',
    'A_FOp_bs', 'A_FOo_bbo', 'A_FOh_xs_f', 'A_FOr_b']"""
    strat_val = {}
    val = 0
    for o in order:
        if o in thickness:
            strat_val[o] = val
            val+=thickness[o]


    #display(strat_val)    
    
    orientations = pd.read_csv(orientation_file)
    contacts = pd.read_csv(contacts_file) 
    
    contacts['val'] = np.nan 

    for o in strat_val:
        contacts.loc[contacts['formation']==o,'val'] = strat_val[o]
    data = pd.concat([orientations,contacts],sort=False)
    data['type'] = np.nan
    for o in order:
        data.loc[data['formation']==o,'type'] = 's0'
    data     
    
    boundary_points = np.zeros((2,3))
    boundary_points[0,0] = bbox[0] 
    boundary_points[0,1] = bbox[1] 
    boundary_points[0,2] = -5000 
    boundary_points[1,0] = bbox[2] 
    boundary_points[1,1] = bbox[3] 
    boundary_points[1,2] = 1200
    
    model = GeologicalModel(boundary_points[0,:],boundary_points[1,:])
    model.set_model_data(data)
    strati = model.create_and_add_foliation('s0', #identifier in data frame
                                                        interpolatortype="FDI", #which interpolator to use
                                                        nelements=400000, # how many tetras/voxels
                                                        buffer=0.1, # how much to extend nterpolation around box
                                                        solver='external',
                                                        external=solve_pyamg
                                                       )   
    #viewer = LavaVuModelViewer()
    viewer = LavaVuModelViewer(model)
    viewer.add_data(strati['feature'])
    viewer.add_isosurface(strati['feature'],
    #                       nslices=10,
                          slices= strat_val.values(),
    #                     voxet={'bounding_box':boundary_points,'nsteps':(100,100,50)},
                          paint_with=strati['feature'],
                          cmap='tab20'

                         )
    #viewer.add_scalar_field(model.bounding_box,(100,100,100),
   #                           'scalar',
    ##                             norm=True,
    #                         paint_with=strati['feature'],
    #                         cmap='tab20')
    viewer.add_scalar_field(strati['feature'])
    viewer.set_viewer_rotation([-53.8190803527832, -17.1993350982666, -2.1576387882232666])
    #viewer.save("fdi_surfaces.png")
    viewer.interactive()
    
    
##########################################################################
# Import outputs from map2loop to gempy and view with pyvtk
# loop2gempy(test_data_name,tmp_path,vtk_pth,orientations_file,contacts_file,groups_file,dtm_reproj_file,bbox,model_base, model_top,vtk)
# Args:
# test_data_name root name of project
# tmp_path path of temp files directory
# vtk_pth path of vtk output directory
# orientations_file path of orientations file
# contacts_file path of contacts file
# groups_file path of groups file
# dtm_reproj_file path of dtm file
# bbox model bounding box
# model_base z value ofbase of model 
# model_top z value of top of model
# vtk flag as to wether to save out model to vtk
#
# Calculates model and displays in external vtk viewer
##########################################################################
def loop2gempy(test_data_name: str, tmp_path: str, vtk_path: str, orientations_file: str,
               contacts_file: str, groups_file:str,
               bbox: tuple, model_base: float, model_top: float, vtk: bool, dtm_reproj_file:str = None,
               va=None,
               verbose: bool = False, compute: bool = True):
    """

    :param test_data_name:
    :param tmp_path:
    :param vtk_path:
    :param orientations_file:
    :param contacts_file:
    :param groups_file:
    :param bbox:
    :param model_base:
    :param model_top:
    :param vtk:
    :param dtm_reproj_file:
    :param va: vertical anisotropy. Factor by which all Z coordinates are multiplied by
    :param verbose:
    :param compute:
    :return:
    """
    import gempy as gp
    from gempy import plot
    print("this one running")

    geo_model = gp.create_model(test_data_name)

    # If depth coordinates are much smaller than XY the whole system of equations becomes very unstable. Until
    # I fix it properly in gempy this is a handcrafted hack
    if va is None:
        va = (float(bbox[0]) - float(bbox[2])) / (model_base - model_top)/2

        if va < 3:
            va = 0
        else:
            print('The vertical exageration is: ', va)

    gp.init_data(geo_model, extent=[bbox[0], bbox[2], bbox[1], bbox[3], model_base * va, model_top * va],
                 resolution=(50, 50, 50),
                 path_o=orientations_file,
                 path_i=contacts_file)

    geo_model.modify_surface_points(geo_model.surface_points.df.index, Z=geo_model.surface_points.df['Z'] * va)

    if dtm_reproj_file is not None:
    #if dtm_reproj_file is None:
        # Load reprojected topography to model

        fp = dtm_reproj_file
        geo_model.set_topography(source='gdal', filepath=fp)
        #geo_model.set_topography()
        #geo_model.set_topography(source='random')
		
        print("va", va, "fp",fp)
        print(type(geo_model.grid))
        # Rescaling topography:
        #print("tv b4", geo_model.grid.topography.shape)
        ####geo_model.grid.topography.values[:, 2] *= va
        geo_model._grid.topography.values[:, 2] *= va
        #print("va", geo_model.grid.topography.values)
        ####geo_model.grid.update_grid_values()
        ####geo_model.update_from_grid()
        geo_model._grid.update_grid_values()
        geo_model.update_from_grid()

    # Pile processing:
    contents = np.genfromtxt(groups_file,
                             delimiter=',', dtype='U100')

    # Init dictionary Series:Surfaces
    map_series_to_surfaces = {}
    choice = 0
    for group in contents:
        # Reading surfaces groups
        surfaces_g = np.atleast_2d(np.genfromtxt(tmp_path + group + '.csv', delimiter=',', dtype='U100'))

        # Check if there are several choices
        if surfaces_g.shape[1] > 1:
            surfaces_g = surfaces_g[choice]
        # Deleting the first element since it is not a surface
        surfaces_g = surfaces_g[1:]
        # Creating the mapping dictionary
        map_series_to_surfaces[group] = surfaces_g.tolist()

    if verbose is True:
        print(map_series_to_surfaces)

    # Setting pile to model
    gp.map_series_to_surfaces(geo_model, map_series_to_surfaces, remove_unused_series=False)

    if('Default series' in map_series_to_surfaces):

        #    Removing related data
        del_surfaces = geo_model.surfaces.df.groupby('series').get_group('Default series')['surface']
        geo_model.delete_surfaces(del_surfaces, remove_data=True)

        # Removing series that have not been mapped to any surface
        geo_model.delete_series('Default series')

    if compute is True:
        gp.set_interpolator(geo_model, theano_optimizer='fast_run', dtype='float64')
        gp.compute_model(geo_model)

    # Visualise Model
    p3d = gp.plot_3d(geo_model, plotter_type='background', notebook=False)

    p3d3 = gp.plot_3d(geo_model, notebook=True)
	

    # Save model as vtk
    if vtk:
        gp.plot.export_to_vtk(geo_model, path=vtk_path, name=test_data_name + '.vtk', voxels=False, block=None,
                              surfaces=True)

    return geo_model


def loop2gempy_(test_data_name, tmp_path, vtk_path, orientations_file, contacts_file, groups_file, dtm_reproj_file,
                bbox, model_base, model_top, vtk):
    import gempy as gp
    from gempy import plot
    geo_model = gp.create_model(test_data_name)
    print("this one running")

    # If depth coordinates are much smaller than XY the whole system of equations becomes very unstable. Until
    # I fix it properly in gempy this is a handcrafted hack
    ve = (bbox[0] - bbox[2]) / (model_base - model_top)

    if ve < 3:
        ve = 0
    else:
        print('The vertical exageration is: ', ve)

    gp.init_data(geo_model, extent=[bbox[0], bbox[2], bbox[1], bbox[3], model_base*ve, model_top*ve],
        resolution = (50,50,50),
          path_o = orientations_file,
          path_i = contacts_file, default_values=True);

    # Show example lithological points
    #gp.get_data(geo_model, 'surface_points').head()

    # Show example orientations
    #gp.get_data(geo_model, 'orientations').head()

    # Plot some of this data
    #gp.plot.plot_data(geo_model, direction='z')

    geo_model.modify_surface_points(geo_model.surface_points.df.index, Z=geo_model.surface_points.df['Z']*ve)

    # Load reprojected topgraphy to model

    fp = dtm_reproj_file
    geo_model.set_topography(source='gdal',filepath=fp)

    contents=np.genfromtxt(groups_file,delimiter=',',dtype='U100')
    ngroups=len(contents)

    faults = gp.Faults()
    series = gp.Series(faults)
    #series.df

    #display(ngroups,contents)
    groups = []

    for i in range (0,ngroups):
        groups.append(contents[i].replace("\n",""))
        series.add_series(contents[i].replace("\n",""))
        print(contents[i].replace("\n",""))

    series.delete_series('Default series')

    #series

    # Load surfaces and assign to series
    surfaces = gp.Surfaces(series)

    print(ngroups,groups)
    for i in range(0,ngroups):
        contents=np.genfromtxt(tmp_path+groups[i]+'.csv',delimiter=',',dtype='U100')
        nformations=len(contents.shape)

        if(nformations==1):
            for j in range (1,len(contents)):
                surfaces.add_surface(str(contents[j]).replace("\n",""))
                d={groups[i]:str(contents[j]).replace("\n","")}
                surfaces.map_series({groups[i]:(str(contents[j]).replace("\n",""))}) #working but no gps
        else:
            for j in range (1,len(contents[0])):
                surfaces.add_surface(str(contents[0][j]).replace("\n",""))
                d={groups[i]:str(contents[0][j]).replace("\n","")}
                surfaces.map_series({groups[i]:(str(contents[0][j]).replace("\n",""))}) #working but no gps

    # Set Interpolation Data
    id_only_one_bool = geo_model.surface_points.df['id'].value_counts() == 1
    id_only_one = id_only_one_bool.index[id_only_one_bool]
    single_vals = geo_model.surface_points.df[geo_model.surface_points.df['id'].isin(id_only_one)]
    for idx, vals in single_vals.iterrows():
        geo_model.add_surface_points(vals['X'], vals['Y'], vals['Z'], vals['surface'])

    geo_model.update_structure()

    gp.set_interpolation_data(geo_model,
                              compile_theano=True,
                              theano_optimizer='fast_compile',
                              verbose=[])

    # Provide summary data on model

    #geo_model.additional_data.structure_data

    #Calculate Model
    gp.compute_model(geo_model)

    # Extract surfaces to visualize in 3D renderers
    #gp.plot.plot_section(geo_model, 49, direction='z', show_data=False)

    ver, sim = gp.get_surfaces(geo_model)

    # import winsound
    # duration = 700  # milliseconds
    # freq = 1100  # Hz
    # winsound.Beep(freq, duration)
    # winsound.Beep(freq, duration)
    # winsound.Beep(freq, duration)

    #Visualise Model
    #gp.plot.plot_3D(geo_model, render_data=False)
    p3d = gp.plot_3d(geo_model, plotter_type='background', notebook=False)

    #Save model as vtk
    if(vtk):
        gp.plot.export_to_vtk(geo_model, path=vtk_path, name=test_data_name+'.vtk', voxels=False, block=None, surfaces=True)

    return geo_model
