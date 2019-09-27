# Masking water areas in digital elevation models

Digital elevation models (dem) can contain a lot of errors at water areas. The sea areas of Finnish 2m dem for example, can contain several meters of value differences on both sides of 0. This is why it is usually good practice to mask sea areas to value 0 before running any further analyses on them. In the image 1 you can see clearly dem value differences at the sea areas.

<img src='https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/images/value_difference.png'>

Image 1. Water areas of digital elevation models can contain value errors that affect spatial analyses. 

A good practice is to use vector format polygons for masking the water areas. In Finland you can use Topographic database (Maastotietokanta) data. In this example we want to mask the sea areas to value 0 so we use the MTK-Vakavesi geopackage layer "meri". Example of the sea polygons on top of the dem in Image 2.

<img src='https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/images/sea_polygons.PNG'>
Image 2. MTK-Vakavesi polygons intersecting our dem file. Polygons can be used in masking of the water areas.

## Data
All the data needed in this example are stored in Taito under wrk/project_ogiir-csc folder. 
If you don't have acceess to Taito, you can download the MTK-Vakavesi geopackage from [Paituli][1].
The 2m and 10m dem data of Finland is availabe at [File service of open data][2] by NLS. 

## Workflow
The script [Dem_masker.py][5] goes through wanted 2m dem files in Taito and masks them with sea areas of MTK-Vakavesi -geopackage. Run the script by using [the batch script][6]. Here is a detailed walk through of the script:

You can define the area of dem files by using [the utm map sheet division][3]. We are going to mask all the 2m dem files in the areas of 'L3' and 'K3' map sheets.The 2m dem data is stored in 6km x 6km mapsheets like the one presented in Images 1 and 2. The masking process is good to do one dem file at the time. Once we have found the wanted dem file we can open the file connection using python library called rasterio.

```pythonscript
# directory of the MTK-Vakavesi in Taito
seafp = r'/wrk/project_ogiir-csc/mml/maastotietokanta/2019/gpkg/MTK-vakavesi_19-01-23.gpkg

# directory of the 2m dem files in Taito
demdir =r'/wrk/project_ogiir-csc/mml/dem2m/2008_latest'

# list of the wanted map sheets
mapsheets = ['L3','K3']

#loop through the files ad folders of the root. 
for subdir, dirs, files in os.walk(demdir): 
    for filename in files:
            # Open only tif files that start with the codes at the mapsheet list
            if filename.endswith(".tif") and filename[0:2] in maplist:
                # construct a filepath if the filename fills the requirements
                filepath = os.path.join(subdir,filename)
                # open file connection to filepath
                with rasterio.open(filepath) as demdata:
```
Next step is to find the intersecting sea polygons with our dem file. This is good to do by using the spatial indexing of the MTK-Vakavesi geopackage. By using the bounds of the dem file, we can efficiently find the intersecting features. 

```pythonscript
                    # bounds of the dem file
                    bounds = demdata.bounds
                    # open the sea areas with fiona 
                    with fiona.open(seafp, layer= 'meri') as sea:
                        # use the spatial indexing of the sea polygons to check if any of them intersects with the dem bounds 
                        hits = sea.items(bbox=(bounds.left,bounds.bottom,bounds.right,bounds.top))
                        items = [i for i in hits]
```
If intersecting features were found, the 'items' variable should now contain information of those polygons. We can use the geometry of the polygons in masking. Masking is done with rasterio while reading the dem file as numpy array. 'invert= True' states that the areas under the polygon geometries will be masked, not vise versa. The default masking value is 0. More about rasterio mask function at [Rasterio documentation][4]

``` pythonscript
                    if len(items) > 0:
                        # read the geometries of the polygons
                        geoms = [item[1]['geometry'] for item in items]
                        # read the demdata as array and mask the sea areas to 0 with the geoms. 
                        demarr, out_transform = mask(demdata,geoms, invert=True)
```
After masking we can save the file. Before saving we need to copy the metadata of the orginal dem file and construct a new filename. 

```pythonscript
                        # copy the metadata of the orginal file
                        out_meta = demdata.meta.copy()
                        # name the new file 
                        outname = os.path.join(outdir1,'{}_masked.tif'.format(filename[0:6]))
                        # save the file in the masked file directory using rasterio
                        with rasterio.open(outname,"w", **out_meta) as dest:
                            dest.write(demarr)
```  
Thats it! Now you should have some neatly masked dem files ready for further analyses!

<img src="https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/images/process.png">

### Terms of use
When using the scripts or CSC.s computation services, please cite the oGIIR project: "We made use of geospatial data/instructions/computing resources provided by CSC and the Open Geospatial Information Infrastructure for Research (oGIIR, urn:nbn:fi:research-infras-2016072513) funded by the Academy of Finland."

Authored by Akseli Toikka and the Department of Geoinformatics and Cartography at FGI

[1]:https://avaa.tdata.fi/web/paituli/latauspalvelu?data_id=mml_maasto_10k_2019_gpkg_euref
[2]:https://tiedostopalvelu.maanmittauslaitos.fi/tp/kartta?lang=en
[3]:https://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/old/UTM_lehtijakopdf.pdf
[4]:https://rasterio.readthedocs.io/en/stable/topics/masking-by-shapefile.html
[5]:https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/Dem_masker.py
[6]:https://github.com/geoportti/DEM-masking-with-sea-polygons/blob/master/masker_batch
