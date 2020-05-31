import geopandas as gpd
from shapely.geometry import  LineString
import os.path

def check_map(structure_file,geology_file,fault_file,mindep_file,bbox,c_l):
    
    for file_name in (structure_file,geology_file,fault_file,mindep_file):
        if not os.path.isfile(structure_file):
            error='map2loop error: file '+file_name+' not found'
            raise NameError(error)
    
    orientations = gpd.read_file(structure_file,bbox=bbox)
    
    
    if(len(orientations)<2):
        raise NameError('map2loop error: Not enough orientations to complete calculations (need at least 2)')
    unique_o=set(orientations[c_l['gi']])
    
    if(not len(unique_o) == len(orientations)):
        raise NameError('map2loop error: Duplicate orientation point unique IDs')
    
    for code in ('d','dd','sf','gi'):
        if not c_l[code] in orientations.columns:
            error='map2loop error: field named '+str(c_l[code])+' not found in orientations file'
            raise NameError(error)
        nans=orientations[c_l[code]].isnull().sum() 
        if(nans>0):
            error='map2loop error: '+str(nans)+' NaN/blank found in column '+str(c_l[code])+' of orientations file'
            raise NameError(error)
            
    geology = gpd.read_file(geology_file,bbox=bbox)    
    unique_g=set(geology[c_l['o']])
    
    if(not len(unique_g) == len(geology)):
        raise NameError('map2loop error: Duplicate geology polygon unique IDs')
    
    for code in ('c','ds','u','r1','min','max'):
        if not c_l[code] in geology.columns:
            error='map2loop error: field named '+str(c_l[code])+' not found in geology file'
        nans=geology[c_l[code]].isnull().sum() 
        if(nans>0):
            error='map2loop error: '+str(nans)+' NaN/blank found in column '+str(c_l[code])+' of geology file'
            raise NameError(error)

    for code in ('c'):
        commas=geology[geology[c_l[code]].str.contains(",")]
        if(len(commas)>0):
            error='map2loop error: comma found in column '+str(c_l[code])+' of geology file'
            raise NameError(error)
        
    fault_folds = gpd.read_file(fault_file,bbox=bbox)    
    unique_f=set(fault_folds[c_l['o']])
    
    if(not len(unique_f) == len(fault_folds)):
        raise NameError('map2loop error: Duplicate fault/fold polyine unique IDs')
    
    for code in ('f','o'):
        if not c_l[code] in fault_folds.columns:
            error='map2loop error: field named '+str(c_l[code])+' not found in fault/fold file'
        nans=fault_folds[c_l[code]].isnull().sum() 
        if(nans>0):
            error='map2loop error: '+str(nans)+' NaN/blank found in column '+str(c_l[code])+' of fault/fold file'
            raise NameError(error)
    
    for ind,f in fault_folds.iterrows():
        if((not f.geometry.type == 'LineString') and f[c_l['o']]== f[c_l['fault']]):
            error='map2loop error: Fault_'+f[c_l['o']]+' is not of type LineString/PolyLine so map2loop cannot process it, sorry'
            raise NameError(error)
            
    mindeps = gpd.read_file(mindep_file,bbox=bbox) 
    
    for code in ('msc','msn','mst','mtc','mscm','mcom'):
        if not c_l[code] in mindeps.columns:
            error='map2loop error: field named '+str(c_l[code])+' not found in mineral deposits file'
        nans=mindeps[c_l[code]].isnull().sum() 
        if(nans>0):
            error='map2loop error: '+str(nans)+' NaN/blank found in column '+str(c_l[code])+' of mineral deposits file'
            raise NameError(error)
    
    print('No errors found')