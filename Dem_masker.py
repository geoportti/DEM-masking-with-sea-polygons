#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:39:27 2019

@author: toikkaak


This script will find wanted 2m digital elevation model (dem) files in Taito folder
and mask the sea areas to value 0 using rasterio mask function and the MTK-Vakavesi geopackage 
of Topographic Database.

In this example we will mask all the dem files that start with the map sheet codes 'L3' and 'K3'.
If you would like to mask dems from smaller area, you can just give the maplist longer codes like 'L33' and 'K34'
and then change the if sentence to read the first three characters of the filename: filename[0:3] in maplist
 
More about rasterio mask function: https://rasterio.readthedocs.io/en/stable/topics/masking-by-shapefile.html
You can find map sheet descriptions at: https://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/old/UTM_lehtijakopdf.pdf

"""
import os
import rasterio
import fiona
from rasterio.mask import mask

#directory of the 2m dem files
demdir =r'/wrk/project_ogiir-csc/mml/dem2m/2008_latest'

#directory of the MTK-Vakavesi geopackage
seafp = r'/wrk/project_ogiir-csc/mml/maastotietokanta/2019/gpkg/MTK-vakavesi_19-01-23.gpkg'

#filepaths for the output in your own work directory
outdir1 = r'filepath for masked demfiles'

#list of the wanted areas. 
mapsheets = ['L3','K3']

#loop through the files ad folders of the root. 
for subdir, dirs, files in os.walk(demdir): 
    for filename in files:
            # Open only tif files that start with the codes at the mapsheet list
            if filename.endswith(".tif") and filename[0:2] in mapsheets:
                #construct a filepath if the filename fills the requirements
                filepath = os.path.join(subdir,filename)
                # open file connection to filepath
                with rasterio.open(filepath) as demdata:
                   #read the bounds of the dem file
                   bounds = demdata.bounds
                   #open the sea areas with fiona 
                   with fiona.open(seafp, layer= 'meri') as sea:
                        #use the spatial indexing of the sea polygons to check if any of them intersects with the dem bounds.
                        # save the found 
                        hits = sea.items(bbox=(bounds.left,bounds.bottom,bounds.right,bounds.top))
                        items = [i for i in hits] 
                   #if intersecting sea polygons exists 
                   if len(items) > 0:
                        #read the geometries of the polygons
                        geoms = [item[1]['geometry'] for item in items]
                        # read the demdata as array and mask the sea areas to 0 with the geoms.
                        # invert = True states that the areas under the polygons will be masked. 
                        demarr, out_transform = mask(demdata,geoms, invert=True)
                        #copu the metadata of the orginal file
                        out_meta = demdata.meta.copy()
                        #name the new file 
                        outname = os.path.join(outdir1,'{}_masked.tif'.format(filename[0:6]))
                        #save the file in the masked file directory using rasterio
                        with rasterio.open(outname,"w", **out_meta) as dest:
                            dest.write(demarr)
                        print('masked',filename,'saved')
                   #if there is no intersecting polygons, continue
                   else:
                        continue

                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        