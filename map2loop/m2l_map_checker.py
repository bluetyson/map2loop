import geopandas as gpd
from shapely.geometry import  LineString, Polygon,MultiLineString
import os.path
from map2loop import m2l_utils      
import warnings
   
#explodes polylines and modifies objectid for exploded parts
def explode_polylines(indf,c_l):                                        
    #indf = gpd.GeoDataFrame.from_file(indata)                  
    outdf = gpd.GeoDataFrame(columns=indf.columns)              
    for idx, row in indf.iterrows():                            
        if type(row.geometry) == LineString:                    
            outdf = outdf.append(row,ignore_index=True)         
        if type(row.geometry) == MultiLineString:               
            multdf = gpd.GeoDataFrame(columns=indf.columns)     
            recs = len(row.geometry)                            
            multdf = multdf.append([row]*recs,ignore_index=True)
            i=0
            for geom in range(recs):                            
                multdf.loc[geom,'geometry'] = row.geometry[geom]
                multdf.loc[geom,c_l['o']]=str(multdf.loc[geom,c_l['o']])+'_'+str(i)
                print('Fault_'+multdf.loc[geom,c_l['o']],'is one of a set of duplicates, so renumbering')
                i=i+1
            outdf = outdf.append(multdf,ignore_index=True)      
    return outdf                                                
    
def check_map(structure_file,geology_file,fault_file,mindep_file,tmp_path,bbox,c_l,dst_crs,local_paths):
    
    if(local_paths):
        for file_name in (structure_file,geology_file,fault_file,mindep_file):
            if not os.path.isfile(structure_file):
                error='map2loop error: file '+file_name+' not found'
                raise NameError(error)
    
    orientations = gpd.read_file(structure_file,bbox=bbox)
    
    
    if(len(orientations)<2):
        raise NameError('map2loop error: Not enough orientations to complete calculations (need at least 2)')
    unique_o=set(orientations[c_l['gi']])
    
    if(not len(unique_o) == len(orientations)):
        warnings.warn('map2loop error: Duplicate orientation point unique IDs')
    
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
        warnings.warn('map2loop error: Duplicate geology polygon unique IDs')
    
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
            
    mindeps = gpd.read_file(mindep_file,bbox=bbox) 
    
    for code in ('msc','msn','mst','mtc','mscm','mcom'):
        if not c_l[code] in mindeps.columns:
            error='map2loop error: field named '+str(c_l[code])+' not found in mineral deposits file'
        nans=mindeps[c_l[code]].isnull().sum() 
        if(nans>0):
            error='map2loop error: '+str(nans)+' NaN/blank found in column '+str(c_l[code])+' of mineral deposits file'
            raise NameError(error)     
            
    # explode fault/fold multipolylines
    # sometimes faults go off map and come back in again which after clipping creates multipolylines
    
    all_faults=gpd.read_file(fault_file,bbox=bbox)
    
    y_point_list = [bbox[1], bbox[1], bbox[3], bbox[3], bbox[1]]
    x_point_list = [bbox[0], bbox[2], bbox[2], bbox[0], bbox[0]]
    
    bbox_geom = Polygon(zip(x_point_list, y_point_list))
    
    polygo = gpd.GeoDataFrame(index=[0], crs=dst_crs, geometry=[bbox_geom]) 
    
    faults_clip=m2l_utils.clip_shp(all_faults,polygo)
    
    faults_explode=explode_polylines(faults_clip,c_l)     
    if(len(faults_explode)>len(faults_clip)):
        warnings.warn('map2loop warning: some faults are MultiPolyLines, and have been split')
    faults_explode.crs = dst_crs
    fault_file=tmp_path+'faults_clip.shp'
    faults_explode.to_file(fault_file)    
    
    print('No errors found')